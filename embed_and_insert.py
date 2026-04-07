"""
Embeds each chunk from rag/data/chunks.json using Amazon Titan Text Embeddings V2
and inserts them into the InvestmentAdvisorRAG DynamoDB table.

Usage:
    python rag/embed_and_insert.py              # embed and insert all chunks
    python rag/embed_and_insert.py --dry-run    # generate embeddings but skip DynamoDB write
    python rag/embed_and_insert.py --reset      # delete all items and re-insert from scratch
"""

import argparse
import json
import os
import time
import uuid
from datetime import datetime, timezone
from decimal import Decimal

import boto3
from botocore.exceptions import ClientError

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "chunks.json")
TABLE_NAME = "InvestmentAdvisorRAG"
EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"
BATCH_SIZE = 25  # DynamoDB batch_writer handles batching internally; this controls progress reporting


def get_region():
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=get_region())


def get_dynamo_table():
    dynamodb = boto3.resource("dynamodb", region_name=get_region())
    return dynamodb.Table(TABLE_NAME)


def embed_text(bedrock_client, text: str) -> list[float]:
    """Embed a single text string using Titan Text Embeddings V2."""
    body = json.dumps({"inputText": text})
    response = bedrock_client.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


def floats_to_decimal(floats: list[float]) -> list[Decimal]:
    """Convert float list to Decimal list for DynamoDB compatibility."""
    return [Decimal(str(round(f, 8))) for f in floats]


def load_chunks() -> list[dict]:
    with open(DATA_PATH) as f:
        return json.load(f)


def reset_table(table):
    """Delete all items from the table (for a clean re-insert)."""
    print("Scanning for existing items to delete...")
    scan = table.scan(ProjectionExpression="chunk_id")
    items = scan.get("Items", [])

    while "LastEvaluatedKey" in scan:
        scan = table.scan(
            ProjectionExpression="chunk_id",
            ExclusiveStartKey=scan["LastEvaluatedKey"],
        )
        items.extend(scan.get("Items", []))

    if not items:
        print("Table is already empty.")
        return

    print(f"Deleting {len(items)} existing items...")
    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={"chunk_id": item["chunk_id"]})
    print("Table cleared.")


def embed_and_insert(dry_run: bool = False, reset: bool = False):
    chunks = load_chunks()
    print(f"Loaded {len(chunks)} chunks from {DATA_PATH}")

    bedrock = get_bedrock_client()
    table = get_dynamo_table() if not dry_run else None

    if reset and not dry_run:
        reset_table(table)

    errors = []
    inserted = 0
    skipped = 0
    start_time = time.time()

    print(f"\nEmbedding model: {EMBED_MODEL_ID}")
    print(f"Target table: {TABLE_NAME}")
    print(f"Dry run: {dry_run}\n")

    with (table.batch_writer() if not dry_run else _null_batch_writer()) as batch:
        for i, chunk in enumerate(chunks, 1):
            try:
                embedding = embed_text(bedrock, chunk["text"])

                item = {
                    "chunk_id": str(uuid.uuid4()),
                    "content_type": chunk["content_type"],
                    "title": chunk["title"],
                    "text": chunk["text"],
                    "embedding": floats_to_decimal(embedding),
                    "metadata": _convert_metadata(chunk.get("metadata", {})),
                    "created_at": datetime.now(timezone.utc).isoformat(),
                }

                if not dry_run:
                    batch.put_item(Item=item)
                    inserted += 1
                else:
                    skipped += 1

                if i % 10 == 0 or i == len(chunks):
                    elapsed = time.time() - start_time
                    rate = i / elapsed
                    remaining = (len(chunks) - i) / rate if rate > 0 else 0
                    print(
                        f"  [{i:3d}/{len(chunks)}] {chunk['content_type']:<20} "
                        f"| {elapsed:.0f}s elapsed | ~{remaining:.0f}s remaining"
                    )

                # Respect Bedrock rate limits
                time.sleep(0.1)

            except ClientError as e:
                code = e.response["Error"]["Code"]
                msg = e.response["Error"]["Message"]
                print(f"  ERROR [{i}] {chunk['title'][:50]}: {code} - {msg}")
                errors.append({"index": i, "title": chunk["title"], "error": f"{code}: {msg}"})
                if code == "ThrottlingException":
                    print("  Throttled — waiting 5 seconds...")
                    time.sleep(5)

    total_time = time.time() - start_time
    print(f"\n{'='*60}")
    if dry_run:
        print(f"Dry run complete — {len(chunks)} embeddings generated, nothing written to DynamoDB.")
    else:
        print(f"Insert complete: {inserted} items written to '{TABLE_NAME}'.")
    print(f"Errors: {len(errors)}")
    print(f"Total time: {total_time:.1f}s ({total_time/len(chunks):.2f}s per chunk)")

    if errors:
        error_path = os.path.join(os.path.dirname(__file__), "data", "insert_errors.json")
        with open(error_path, "w") as f:
            json.dump(errors, f, indent=2)
        print(f"Error details written to {error_path}")


def _convert_metadata(metadata: dict) -> dict:
    """Recursively convert any float values in metadata to Decimal for DynamoDB."""
    result = {}
    for k, v in metadata.items():
        if isinstance(v, float):
            result[k] = Decimal(str(v))
        elif isinstance(v, list):
            result[k] = [Decimal(str(x)) if isinstance(x, float) else x for x in v]
        elif isinstance(v, dict):
            result[k] = _convert_metadata(v)
        else:
            result[k] = v
    return result


class _null_batch_writer:
    """No-op context manager for dry runs."""
    def __enter__(self):
        return self
    def __exit__(self, *args):
        pass
    def put_item(self, **kwargs):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed chunks and insert into DynamoDB.")
    parser.add_argument("--dry-run", action="store_true", help="Generate embeddings but skip DynamoDB writes.")
    parser.add_argument("--reset", action="store_true", help="Delete all existing items before inserting.")
    args = parser.parse_args()

    embed_and_insert(dry_run=args.dry_run, reset=args.reset)
