/**
 * RAG retrieval utility supporting all five banking topic tables.
 *
 * Embeds a user question using Amazon Titan Text Embeddings V2, scans the chosen
 * DynamoDB table, and returns the top-K most relevant chunks ranked by cosine similarity.
 * No LLM call is made — raw retrieval only.
 *
 * Available data sources (--source):
 *   investments   → InvestmentAdvisorRAG       (default)
 *   loans         → LoansAndCreditRAG
 *   accounts      → AccountManagementRAG
 *   transfers     → TransferTransactionsRAG
 *   support       → CustomerSupportRAG
 *
 * Usage:
 *   node rag/retrieval.js "What is a Roth IRA?"
 *   node rag/retrieval.js "What is a mortgage?" --source loans
 *   node rag/retrieval.js "How do I open an account?" --source accounts --top-k 5
 *   node rag/retrieval.js "How do wire transfers work?" --source transfers
 *   node rag/retrieval.js "I lost my card" --source support --content-type FAQ
 */

import { BedrockRuntimeClient, InvokeModelCommand } from "@aws-sdk/client-bedrock-runtime";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";
import { DynamoDBDocumentClient, ScanCommand } from "@aws-sdk/lib-dynamodb";
import { readFileSync } from "fs";
import { parseArgs } from "util";
import { fileURLToPath } from "url";

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

const EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0";

const SOURCES = {
  investments: "InvestmentAdvisorRAG",
  loans:       "LoansAndCreditRAG",
  accounts:    "AccountManagementRAG",
  transfers:   "TransferTransactionsRAG",
  support:     "CustomerSupportRAG",
};

const DEFAULT_SOURCE = "investments";

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

function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    const ai = Number(a[i]), bi = Number(b[i]);
    dot += ai * bi;
    normA += ai * ai;
    normB += bi * bi;
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

async function scanAllItems(client, tableName, contentType = null) {
  const items = [];
  let lastKey = undefined;

  do {
    const params = {
      TableName: tableName,
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
 * Embed a question, scan a DynamoDB table, and return top-K chunks by cosine similarity.
 * @param {string} question
 * @param {object} options
 * @param {number} [options.topK=5]
 * @param {string|null} [options.contentType=null]
 * @param {string} [options.source="investments"]  One of: investments, loans, accounts, transfers, support
 * @returns {Promise<Array<{chunk_id, content_type, title, text, metadata, score}>>}
 */
export async function retrieve(question, { topK = 5, contentType = null, source = DEFAULT_SOURCE } = {}) {
  const tableName = SOURCES[source];
  if (!tableName) {
    throw new Error(`Unknown source "${source}". Valid options: ${Object.keys(SOURCES).join(", ")}`);
  }

  const bedrock = getBedrockClient();
  const dynamo = getDynamoClient();

  console.log(`Embedding question... (source: ${source} → ${tableName})`);
  const queryEmbedding = await embedText(bedrock, question);

  const filterLabel = contentType ? ` (filter: ${contentType})` : "";
  console.log(`Scanning table${filterLabel}...`);
  const items = await scanAllItems(dynamo, tableName, contentType);
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

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

const isMain = process.argv[1] === fileURLToPath(import.meta.url);

const VALID_CONTENT_TYPES = ["PRODUCT", "FAQ", "MARKET_COMMENTARY", "CLIENT_SCENARIO"];

if (isMain) {
  const { values, positionals } = parseArgs({
    args: process.argv.slice(2),
    options: {
      "top-k":        { type: "string", default: "5" },
      "content-type": { type: "string" },
      "source":       { type: "string", default: DEFAULT_SOURCE },
    },
    allowPositionals: true,
  });

  const question = positionals[0];
  if (!question) {
    console.error('Usage: node rag/retrieval.js "<question>" [--source SOURCE] [--top-k N] [--content-type TYPE]');
    console.error(`  --source:       one of ${Object.keys(SOURCES).join(", ")} (default: ${DEFAULT_SOURCE})`);
    console.error(`  --content-type: one of ${VALID_CONTENT_TYPES.join(", ")}`);
    process.exit(1);
  }

  const topK = parseInt(values["top-k"], 10);
  const contentType = values["content-type"] ?? null;
  const source = values["source"];

  if (!SOURCES[source]) {
    console.error(`Invalid --source "${source}". Must be one of: ${Object.keys(SOURCES).join(", ")}`);
    process.exit(1);
  }

  if (contentType && !VALID_CONTENT_TYPES.includes(contentType)) {
    console.error(`Invalid --content-type "${contentType}". Must be one of: ${VALID_CONTENT_TYPES.join(", ")}`);
    process.exit(1);
  }

  const results = await retrieve(question, { topK, contentType, source });
  formatResults(results, question);
}
