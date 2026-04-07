/**
 * RAG Agent — Claude-powered banking assistant with 5 RAG tools.
 *
 * Uses the AWS Bedrock Converse API with tool use so Claude can intelligently
 * route each question to the right knowledge base(s), call multiple tools when
 * a question spans domains, and synthesize a grounded answer.
 *
 * Tools:
 *   search_investments   → InvestmentAdvisorRAG
 *   search_loans         → LoansAndCreditRAG
 *   search_accounts      → AccountManagementRAG
 *   search_transfers     → TransferTransactionsRAG
 *   search_support       → CustomerSupportRAG
 *
 * Usage:
 *   node rag/agent.js "What is a Roth IRA?"          # single question
 *   node rag/agent.js                                  # interactive chat mode
 */

import { BedrockRuntimeClient, ConverseCommand } from "@aws-sdk/client-bedrock-runtime";
import { readFileSync } from "fs";
import { createInterface } from "readline";
import { retrieve } from "./retrieval.js";

// Load .env from parent directory if present
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
    if (key && !(key in process.env)) process.env[key] = value;
  }
} catch {
  // No .env file — rely on environment variables
}

const MODEL_ID = "us.anthropic.claude-opus-4-6-v1";

const SYSTEM_PROMPT = `You are a knowledgeable banking assistant. You have access to five specialized \
knowledge bases. Always search the most relevant one(s) before answering — do not answer from \
memory alone. You may call multiple tools if a question spans domains.

Knowledge bases:
- search_investments: Investment products, retirement accounts (IRA, 401k), ETFs, bonds, asset allocation, market commentary
- search_loans: Mortgages, HELOCs, personal/auto/student loans, credit cards
- search_accounts: Checking, savings, CDs, money market accounts, interest rates
- search_transfers: Wire transfers, ACH, Zelle, bill pay, international payments
- search_support: Customer service channels, mobile app, online banking, card services`;

// ---------------------------------------------------------------------------
// Tool definitions (Bedrock Converse format)
// ---------------------------------------------------------------------------

const TOOL_SPECS = [
  {
    name: "search_investments",
    description:
      "Search the investment advisor knowledge base for information about investment products, " +
      "retirement accounts (IRAs, 401k), ETFs, mutual funds, bonds, stocks, asset allocation " +
      "strategies, market commentary, and financial planning scenarios.",
  },
  {
    name: "search_loans",
    description:
      "Search the loans and credit knowledge base for information about mortgages, HELOCs, " +
      "home equity loans, personal loans, auto loans, student loans, credit cards, and " +
      "loan application processes.",
  },
  {
    name: "search_accounts",
    description:
      "Search the account management knowledge base for information about checking accounts, " +
      "savings accounts, CDs (certificates of deposit), money market accounts, interest rates, " +
      "account features, and how to open or manage accounts.",
  },
  {
    name: "search_transfers",
    description:
      "Search the transfers and payments knowledge base for information about wire transfers, " +
      "ACH transfers, Zelle, bill pay, peer-to-peer payments, international transfers, and " +
      "payment processing timelines.",
  },
  {
    name: "search_support",
    description:
      "Search the customer support knowledge base for information about support channels " +
      "(phone, live chat, branch), the mobile banking app, online banking features, " +
      "card services, and general customer assistance.",
  },
];

const INPUT_SCHEMA = {
  json: {
    type: "object",
    properties: {
      query: {
        type: "string",
        description: "The question or topic to search for",
      },
      content_type: {
        type: "string",
        enum: ["PRODUCT", "FAQ", "MARKET_COMMENTARY", "CLIENT_SCENARIO"],
        description: "Optional: filter results to a specific content category",
      },
      top_k: {
        type: "integer",
        description: "Number of results to return (default: 5)",
      },
    },
    required: ["query"],
  },
};

const TOOL_CONFIG = {
  tools: TOOL_SPECS.map((spec) => ({
    toolSpec: { name: spec.name, description: spec.description, inputSchema: INPUT_SCHEMA },
  })),
};

// Maps tool names → retrieve() source keys
const TOOL_SOURCE_MAP = {
  search_investments: "investments",
  search_loans:       "loans",
  search_accounts:    "accounts",
  search_transfers:   "transfers",
  search_support:     "support",
};

// ---------------------------------------------------------------------------
// Tool execution
// ---------------------------------------------------------------------------

async function executeTool(name, input) {
  const source = TOOL_SOURCE_MAP[name];
  if (!source) throw new Error(`Unknown tool: ${name}`);

  const results = await retrieve(input.query, {
    source,
    topK: input.top_k ?? 5,
    contentType: input.content_type ?? null,
  });

  if (!results.length) return "No relevant results found in this knowledge base.";

  return results
    .map(
      (r, i) =>
        `[${i + 1}] ${r.title} (${r.content_type}, relevance: ${r.score.toFixed(4)})\n${r.text}`
    )
    .join("\n\n---\n\n");
}

// ---------------------------------------------------------------------------
// Agentic loop
// ---------------------------------------------------------------------------

async function runTurn(bedrock, messages) {
  while (true) {
    const response = await bedrock.send(
      new ConverseCommand({
        modelId: MODEL_ID,
        system: [{ text: SYSTEM_PROMPT }],
        messages,
        toolConfig: TOOL_CONFIG,
      })
    );

    const assistantMessage = response.output.message;
    messages.push(assistantMessage);

    // Done — return the final text response
    if (response.stopReason !== "tool_use") {
      return assistantMessage.content.find((b) => b.text)?.text ?? "";
    }

    // Execute all tool calls in this turn
    const toolResults = [];
    for (const block of assistantMessage.content) {
      if (!block.toolUse) continue;
      const { toolUseId, name, input } = block.toolUse;
      console.error(
        `\n  [${name}] querying: "${input.query}"` +
          (input.content_type ? ` · type: ${input.content_type}` : "")
      );

      let resultText;
      let status;
      try {
        resultText = await executeTool(name, input);
      } catch (err) {
        resultText = `Error: ${err.message}`;
        status = "error";
      }

      toolResults.push({
        toolResult: {
          toolUseId,
          content: [{ text: resultText }],
          ...(status && { status }),
        },
      });
    }

    messages.push({ role: "user", content: toolResults });
  }
}

// ---------------------------------------------------------------------------
// Public API — importable for use in other modules
// ---------------------------------------------------------------------------

/**
 * Ask the banking assistant a single question.
 * @param {string} question
 * @returns {Promise<string>} The assistant's answer
 */
export async function ask(question) {
  const bedrock = new BedrockRuntimeClient({
    region: process.env.AWS_REGION ?? process.env.AWS_DEFAULT_REGION ?? "us-east-1",
  });
  const messages = [{ role: "user", content: [{ text: question }] }];
  return runTurn(bedrock, messages);
}

/**
 * Start an interactive multi-turn conversation session.
 * Returns a function to send messages; conversation history is maintained.
 * @returns {{ send: (question: string) => Promise<string>, reset: () => void }}
 */
export function createSession() {
  const bedrock = new BedrockRuntimeClient({
    region: process.env.AWS_REGION ?? process.env.AWS_DEFAULT_REGION ?? "us-east-1",
  });
  const messages = [];

  return {
    async send(question) {
      messages.push({ role: "user", content: [{ text: question }] });
      return runTurn(bedrock, messages);
    },
    reset() {
      messages.length = 0;
    },
  };
}

// ---------------------------------------------------------------------------
// CLI entry point
// ---------------------------------------------------------------------------

import { fileURLToPath } from "url";
const isMain = process.argv[1] === fileURLToPath(import.meta.url);

if (isMain) {
  const args = process.argv.slice(2);

  if (args.length > 0) {
    // Single-question mode
    const question = args.join(" ");
    console.log(`\nQuestion: ${question}\n`);
    const answer = await ask(question);
    console.log("\n" + "=".repeat(70));
    console.log("Answer:");
    console.log("=".repeat(70));
    console.log(answer);
  } else {
    // Interactive chat mode
    const bedrock = new BedrockRuntimeClient({
      region: process.env.AWS_REGION ?? process.env.AWS_DEFAULT_REGION ?? "us-east-1",
    });
    const messages = [];

    const rl = createInterface({ input: process.stdin, output: process.stdout });
    console.log("\nBanking Assistant (RAG-powered) · type 'exit' to quit\n");

    const prompt = () => {
      rl.question("You: ", async (input) => {
        const question = input.trim();
        if (!question) { prompt(); return; }
        if (question.toLowerCase() === "exit") { rl.close(); return; }

        messages.push({ role: "user", content: [{ text: question }] });
        try {
          const answer = await runTurn(bedrock, messages);
          console.log(`\nAssistant: ${answer}\n`);
        } catch (err) {
          console.error(`Error: ${err.message}`);
        }
        prompt();
      });
    };

    prompt();
  }
}
