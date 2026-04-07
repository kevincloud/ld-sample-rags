"""
RAG query utility for the InvestmentAdvisorRAG DynamoDB table.

Embeds a user question using Amazon Titan Text Embeddings V2, scans the DynamoDB table,
and returns the top-K most relevant chunks ranked by cosine similarity.

Usage:
    python rag/query.py "What is a Roth IRA?"
    python rag/query.py "How should a 30-year-old invest?" --top-k 5
    python rag/query.py "Tell me about bonds" --content-type FAQ
    python rag/query.py "Market outlook" --content-type MARKET_COMMENTARY --top-k 3
"""

import argparse
import json
import math
import os
from decimal import Decimal

import boto3
from boto3.dynamodb.conditions import Attr

TABLE_NAME = "InvestmentAdvisorRAG"
EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"


def get_region():
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=get_region())


def get_dynamo_table():
    dynamodb = boto3.resource("dynamodb", region_name=get_region())
    return dynamodb.Table(TABLE_NAME)


def embed_text(bedrock_client, text: str) -> list[float]:
    body = json.dumps({"inputText": text})
    response = bedrock_client.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


def cosine_similarity(a: list, b: list) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(float(x) * float(y) for x, y in zip(a, b))
    norm_a = math.sqrt(sum(float(x) ** 2 for x in a))
    norm_b = math.sqrt(sum(float(x) ** 2 for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def scan_all_items(table, content_type: str | None = None) -> list[dict]:
    """Scan all items from DynamoDB, optionally filtered by content_type."""
    kwargs = {}
    if content_type:
        kwargs["FilterExpression"] = Attr("content_type").eq(content_type)

    items = []
    response = table.scan(**kwargs)
    items.extend(response.get("Items", []))

    while "LastEvaluatedKey" in response:
        kwargs["ExclusiveStartKey"] = response["LastEvaluatedKey"]
        response = table.scan(**kwargs)
        items.extend(response.get("Items", []))

    return items


def query(
    question: str,
    top_k: int = 5,
    content_type: str | None = None,
    show_scores: bool = True,
) -> list[dict]:
    """
    Embed a question, scan DynamoDB, and return top-K chunks by cosine similarity.

    Args:
        question: The user's query string.
        top_k: Number of results to return.
        content_type: Optional filter — PRODUCT | FAQ | MARKET_COMMENTARY | CLIENT_SCENARIO.
        show_scores: Whether to include similarity scores in output.

    Returns:
        List of dicts with keys: chunk_id, content_type, title, text, score, metadata.
    """
    bedrock = get_bedrock_client()
    table = get_dynamo_table()

    print(f"Embedding question...")
    query_embedding = embed_text(bedrock, question)

    print(f"Scanning table{f' (filter: {content_type})' if content_type else ''}...")
    items = scan_all_items(table, content_type)
    print(f"Retrieved {len(items)} items. Computing similarities...")

    scored = []
    for item in items:
        if "embedding" not in item:
            continue
        score = cosine_similarity(query_embedding, item["embedding"])
        scored.append({
            "chunk_id": item.get("chunk_id"),
            "content_type": item.get("content_type"),
            "title": item.get("title"),
            "text": item.get("text"),
            "metadata": item.get("metadata", {}),
            "score": score,
        })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]


def format_results(results: list[dict], question: str) -> None:
    print(f"\n{'='*70}")
    print(f"Query: {question}")
    print(f"Top {len(results)} results:")
    print(f"{'='*70}\n")

    for i, r in enumerate(results, 1):
        print(f"[{i}] {r['title']}")
        print(f"    Type:  {r['content_type']}")
        print(f"    Score: {r['score']:.4f}")
        print(f"    Text:  {r['text'][:300]}{'...' if len(r['text']) > 300 else ''}")
        print()


def build_context(results: list[dict]) -> str:
    """Format retrieved chunks as context string for an LLM prompt."""
    context_parts = []
    for i, r in enumerate(results, 1):
        context_parts.append(
            f"[Source {i}: {r['title']} ({r['content_type']})]\n{r['text']}"
        )
    return "\n\n---\n\n".join(context_parts)


def query_and_answer(question: str, top_k: int = 5, content_type: str | None = None) -> str:
    """
    Full RAG pipeline: retrieve relevant chunks, then generate an answer using Claude.

    Returns the LLM's response string.
    """
    results = query(question, top_k=top_k, content_type=content_type)
    context = build_context(results)

    bedrock = boto3.client("bedrock-runtime", region_name=get_region())
    prompt = (
        f"You are a knowledgeable banking investment advisor assistant. "
        f"Use the following reference material to answer the client's question accurately and helpfully.\n\n"
        f"Reference Material:\n{context}\n\n"
        f"Client Question: {question}\n\n"
        f"Provide a clear, professional response. If the reference material doesn't fully address the question, "
        f"say so and provide general guidance based on sound financial principles."
    )

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
    }

    response = bedrock.invoke_model(
        modelId="us.anthropic.claude-opus-4-6-v1",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query the investment advisor RAG system.")
    parser.add_argument("question", help="The question to ask.")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return (default: 5).")
    parser.add_argument(
        "--content-type",
        choices=["PRODUCT", "FAQ", "MARKET_COMMENTARY", "CLIENT_SCENARIO"],
        default=None,
        help="Filter results by content type.",
    )
    parser.add_argument(
        "--answer",
        action="store_true",
        help="Generate a full LLM answer using retrieved chunks as context.",
    )
    args = parser.parse_args()

    if args.answer:
        print(f"\nGenerating RAG answer for: {args.question}\n")
        answer = query_and_answer(args.question, top_k=args.top_k, content_type=args.content_type)
        print(f"{'='*70}")
        print("Answer:")
        print(f"{'='*70}")
        print(answer)
    else:
        results = query(args.question, top_k=args.top_k, content_type=args.content_type)
        format_results(results, args.question)
