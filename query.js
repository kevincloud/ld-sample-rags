/**
 * RAG query utility for the InvestmentAdvisorRAG DynamoDB table.
 *
 * Embeds a user question using Amazon Titan Text Embeddings V2, scans the DynamoDB table,
 * and returns the top-K most relevant chunks ranked by cosine similarity.
 *
 * Usage:
 *   node rag/query.js "What is a Roth IRA?"
 *   node rag/query.js "How should a 30-year-old invest?" --top-k 5
 *   node rag/query.js "Tell me about bonds" --content-type FAQ
 *   node rag/query.js "Market outlook" --content-type MARKET_COMMENTARY --top-k 3
 *   node rag/query.js "What should I do with an inheritance?" --answer
 */

import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, ScanCommand } from "@aws-sdk/lib-dynamodb";
import { readFileSync } from "fs";
import { parseArgs } from "util";

// Load .env file from parent directory if present
try {
  const envPath = new URL("../.env", import.meta.url).pathname;
  const envContent = readFileSync(envPath, "utf8");
  for (const line of envContent.split("\n")) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith("#")) continue;
    const eqIdx = trimmed.indexOf("=");
    if (eqIdx === -1) continue;
    const key = trimmed.slice(0, eqIdx).trim();
    const value = trimmed.slice(eqIdx + 1).trim();
    if (key && !(key in process.env)) {
      process.env[key] = value;
    }
  }
} catch {
  // No .env file — rely on environment variables already set
}

const TABLE_NAME = "InvestmentAdvisorRAG";
const EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0";
const CLAUDE_MODEL_ID = "us.anthropic.claude-opus-4-6-v1";

function getRegion() {
  return process.env.AWS_REGION ?? process.env.AWS_DEFAULT_REGION ?? "us-east-1";
}

function getBedrockClient() {
  return new BedrockRuntimeClient({ region: getRegion() });
}

function getDynamoClient() {
  const dynamo = new DynamoDBClient({ region: getRegion() });
  return DynamoDBDocumentClient.from(dynamo, {
    marshallOptions: { convertClassInstanceToMap: true },
  });
}

/**
 * Embed a text string using Amazon Titan Text Embeddings V2.
 * @param {BedrockRuntimeClient} client
 * @param {string} text
 * @returns {Promise<number[]>}
 */
async function embedText(client, text) {
  const command = new InvokeModelCommand({
    modelId: EMBED_MODEL_ID,
    body: JSON.stringify({ inputText: text }),
    contentType: "application/json",
    accept: "application/json",
  });
  const response = await client.send(command);
  const result = JSON.parse(Buffer.from(response.body).toString("utf8"));
  return result.embedding;
}

/**
 * Compute cosine similarity between two numeric vectors.
 * @param {number[]} a
 * @param {number[]} b
 * @returns {number}
 */
function cosineSimilarity(a, b) {
  let dot = 0;
  let normA = 0;
  let normB = 0;
  for (let i = 0; i < a.length; i++) {
    const ai = Number(a[i]);
    const bi = Number(b[i]);
    dot += ai * bi;
    normA += ai * ai;
    normB += bi * bi;
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Scan all items from DynamoDB, optionally filtered by content_type.
 * Handles pagination automatically.
 * @param {DynamoDBDocumentClient} client
 * @param {string|null} contentType
 * @returns {Promise<object[]>}
 */
async function scanAllItems(client, contentType = null) {
  const items = [];
  let lastKey = undefined;

  do {
    const params = {
      TableName: TABLE_NAME,
      ...(contentType && {
        FilterExpression: "content_type = :ct",
        ExpressionAttributeValues: { ":ct": contentType },
      }),
      ...(lastKey && { ExclusiveStartKey: lastKey }),
    };

    const response = await client.send(new ScanCommand(params));
    items.push(...(response.Items ?? []));
    lastKey = response.LastEvaluatedKey;
  } while (lastKey);

  return items;
}

/**
 * Embed a question, scan DynamoDB, and return top-K chunks by cosine similarity.
 * @param {string} question
 * @param {object} options
 * @param {number} [options.topK=5]
 * @param {string|null} [options.contentType=null]
 * @returns {Promise<object[]>}
 */
async function query(question, { topK = 5, contentType = null } = {}) {
  const bedrock = getBedrockClient();
  const dynamo = getDynamoClient();

  console.log("Embedding question...");
  const queryEmbedding = await embedText(bedrock, question);

  const filterLabel = contentType ? ` (filter: ${contentType})` : "";
  console.log(`Scanning table${filterLabel}...`);
  const items = await scanAllItems(dynamo, contentType);
  console.log(`Retrieved ${items.length} items. Computing similarities...`);

  const scored = items
    .filter((item) => item.embedding)
    .map((item) => ({
      chunk_id: item.chunk_id,
      content_type: item.content_type,
      title: item.title,
      text: item.text,
      metadata: item.metadata ?? {},
      score: cosineSimilarity(queryEmbedding, item.embedding),
    }));

  scored.sort((a, b) => b.score - a.score);
  return scored.slice(0, topK);
}

/**
 * Format and print results to stdout.
 * @param {object[]} results
 * @param {string} question
 */
function formatResults(results, question) {
  console.log("\n" + "=".repeat(70));
  console.log(`Query: ${question}`);
  console.log(`Top ${results.length} results:`);
  console.log("=".repeat(70) + "\n");

  for (let i = 0; i < results.length; i++) {
    const r = results[i];
    const preview = r.text.length > 300 ? r.text.slice(0, 300) + "..." : r.text;
    console.log(`[${i + 1}] ${r.title}`);
    console.log(`    Type:  ${r.content_type}`);
    console.log(`    Score: ${r.score.toFixed(4)}`);
    console.log(`    Text:  ${preview}`);
    console.log();
  }
}

/**
 * Format retrieved chunks as a context string for an LLM prompt.
 * @param {object[]} results
 * @returns {string}
 */
function buildContext(results) {
  return results
    .map((r, i) => `[Source ${i + 1}: ${r.title} (${r.content_type})]\n${r.text}`)
    .join("\n\n---\n\n");
}

/**
 * Full RAG pipeline: retrieve relevant chunks, then generate an answer using Claude.
 * @param {string} question
 * @param {object} options
 * @param {number} [options.topK=5]
 * @param {string|null} [options.contentType=null]
 * @returns {Promise<string>}
 */
async function queryAndAnswer(question, { topK = 5, contentType = null } = {}) {
  const results = await query(question, { topK, contentType });
  const context = buildContext(results);

  const bedrock = getBedrockClient();
  const prompt =
    `You are a knowledgeable banking investment advisor assistant. ` +
    `Use the following reference material to answer the client's question accurately and helpfully.\n\n` +
    `Reference Material:\n${context}\n\n` +
    `Client Question: ${question}\n\n` +
    `Provide a clear, professional response. If the reference material doesn't fully address the question, ` +
    `say so and provide general guidance based on sound financial principles.`;

  const body = {
    anthropic_version: "bedrock-2023-05-31",
    max_tokens: 1024,
    messages: [{ role: "user", content: prompt }],
  };

  const command = new InvokeModelCommand({
    modelId: CLAUDE_MODEL_ID,
    body: JSON.stringify(body),
    contentType: "application/json",
    accept: "application/json",
  });

  const response = await bedrock.send(command);
  const result = JSON.parse(Buffer.from(response.body).toString("utf8"));
  return result.content[0].text;
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

const VALID_CONTENT_TYPES = ["PRODUCT", "FAQ", "MARKET_COMMENTARY", "CLIENT_SCENARIO"];

const { values, positionals } = parseArgs({
  args: process.argv.slice(2),
  options: {
    "top-k": { type: "string", default: "5" },
    "content-type": { type: "string" },
    answer: { type: "boolean", default: false },
  },
  allowPositionals: true,
});

const question = positionals[0];
if (!question) {
  console.error('Usage: node rag/query.js "<question>" [--top-k N] [--content-type TYPE] [--answer]');
  console.error(`  --content-type: one of ${VALID_CONTENT_TYPES.join(", ")}`);
  process.exit(1);
}

const topK = parseInt(values["top-k"], 10);
const contentType = values["content-type"] ?? null;

if (contentType && !VALID_CONTENT_TYPES.includes(contentType)) {
  console.error(`Invalid --content-type "${contentType}". Must be one of: ${VALID_CONTENT_TYPES.join(", ")}`);
  process.exit(1);
}

if (values.answer) {
  console.log(`\nGenerating RAG answer for: ${question}\n`);
  const answer = await queryAndAnswer(question, { topK, contentType });
  console.log("=".repeat(70));
  console.log("Answer:");
  console.log("=".repeat(70));
  console.log(answer);
} else {
  const results = await query(question, { topK, contentType });
  formatResults(results, question);
}
