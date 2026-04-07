"""
Generates, embeds, and inserts demo data for all four new RAG tables:
  - LoansAndCreditRAG        (data/loans_chunks.json)
  - AccountManagementRAG     (data/accounts_chunks.json)
  - TransferTransactionsRAG  (data/transfers_chunks.json)
  - CustomerSupportRAG       (data/support_chunks.json)

Each topic's chunks are embedded with Amazon Titan Text Embeddings V2 and
inserted into its corresponding DynamoDB table.

Usage:
    python rag/embed_and_insert_new_tables.py                        # all four topics
    python rag/embed_and_insert_new_tables.py --topic loans          # loans only
    python rag/embed_and_insert_new_tables.py --topic accounts       # accounts only
    python rag/embed_and_insert_new_tables.py --topic transfers      # transfers only
    python rag/embed_and_insert_new_tables.py --topic support        # support only
    python rag/embed_and_insert_new_tables.py --dry-run              # skip DynamoDB writes
    python rag/embed_and_insert_new_tables.py --reset                # clear table before inserting
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

EMBED_MODEL_ID = "amazon.titan-embed-text-v2:0"

TOPIC_CONFIG = {
    "loans": {
        "data_file": "loans_chunks.json",
        "table_name": "LoansAndCreditRAG",
        "generate_module": "generate_loans_data",
    },
    "accounts": {
        "data_file": "accounts_chunks.json",
        "table_name": "AccountManagementRAG",
        "generate_module": "generate_accounts_data",
    },
    "transfers": {
        "data_file": "transfers_chunks.json",
        "table_name": "TransferTransactionsRAG",
        "generate_module": "generate_transfers_data",
    },
    "support": {
        "data_file": "support_chunks.json",
        "table_name": "CustomerSupportRAG",
        "generate_module": "generate_support_data",
    },
}

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


def get_region():
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=get_region())


def get_dynamo_table(table_name: str):
    dynamodb = boto3.resource("dynamodb", region_name=get_region())
    return dynamodb.Table(table_name)


def embed_text(bedrock_client, text: str) -> list:
    body = json.dumps({"inputText": text})
    response = bedrock_client.invoke_model(
        modelId=EMBED_MODEL_ID,
        body=body,
        contentType="application/json",
        accept="application/json",
    )
    result = json.loads(response["body"].read())
    return result["embedding"]


def floats_to_decimal(floats: list) -> list:
    return [Decimal(str(round(f, 8))) for f in floats]


def _convert_metadata(metadata: dict) -> dict:
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


def load_chunks(data_file: str) -> list:
    path = os.path.join(DATA_DIR, data_file)
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Data file not found: {path}\n"
            f"Generate it first with the corresponding generate_*.py script."
        )
    with open(path) as f:
        return json.load(f)


def reset_table(table):
    print("  Scanning for existing items to delete...")
    scan = table.scan(ProjectionExpression="chunk_id")
    items = scan.get("Items", [])
    while "LastEvaluatedKey" in scan:
        scan = table.scan(
            ProjectionExpression="chunk_id",
            ExclusiveStartKey=scan["LastEvaluatedKey"],
        )
        items.extend(scan.get("Items", []))

    if not items:
        print("  Table is already empty.")
        return

    print(f"  Deleting {len(items)} existing items...")
    with table.batch_writer() as batch:
        for item in items:
            batch.delete_item(Key={"chunk_id": item["chunk_id"]})
    print("  Table cleared.")


def process_topic(topic_key: str, dry_run: bool = False, reset: bool = False):
    config = TOPIC_CONFIG[topic_key]
    table_name = config["table_name"]
    data_file = config["data_file"]

    print(f"\n{'='*65}")
    print(f"Topic: {topic_key.upper()}  →  Table: {table_name}")
    print(f"Data file: {data_file}")
    print(f"{'='*65}")

    chunks = load_chunks(data_file)
    print(f"Loaded {len(chunks)} chunks.")

    bedrock = get_bedrock_client()
    table = get_dynamo_table(table_name) if not dry_run else None

    if reset and not dry_run:
        reset_table(table)

    errors = []
    inserted = 0
    skipped = 0
    start_time = time.time()

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
                # Use individual put_item to avoid batch_writer timeout on large embedding payloads
                table.put_item(Item=item)
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

            time.sleep(0.1)  # Bedrock rate limit courtesy

        except ClientError as e:
            code = e.response["Error"]["Code"]
            msg = e.response["Error"]["Message"]
            print(f"  ERROR [{i}] {chunk['title'][:50]}: {code} - {msg}")
            errors.append({"index": i, "title": chunk["title"], "error": f"{code}: {msg}"})
            if code == "ThrottlingException":
                print("  Throttled — waiting 5 seconds...")
                time.sleep(5)

    total_time = time.time() - start_time
    if dry_run:
        print(f"\n  Dry run complete — {len(chunks)} embeddings generated, nothing written.")
    else:
        print(f"\n  Insert complete: {inserted} items written to '{table_name}'.")
    print(f"  Errors: {len(errors)}  |  Total time: {total_time:.1f}s")

    if errors:
        error_path = os.path.join(DATA_DIR, f"{topic_key}_insert_errors.json")
        with open(error_path, "w") as f:
            json.dump(errors, f, indent=2)
        print(f"  Error details → {error_path}")

    return len(errors) == 0


def ensure_data_files(topics: list):
    """Generate any missing data files by importing and running the generate scripts."""
    import importlib.util
    import sys

    rag_dir = os.path.dirname(__file__)
    os.makedirs(DATA_DIR, exist_ok=True)

    for topic_key in topics:
        config = TOPIC_CONFIG[topic_key]
        data_path = os.path.join(DATA_DIR, config["data_file"])
        if not os.path.exists(data_path):
            print(f"Data file missing for '{topic_key}' — generating now...")
            module_file = os.path.join(rag_dir, f"{config['generate_module']}.py")
            spec = importlib.util.spec_from_file_location(config["generate_module"], module_file)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            chunks = mod.build_chunks()
            with open(data_path, "w") as f:
                json.dump(chunks, f, indent=2)
            print(f"  Generated {len(chunks)} chunks → {data_path}")
        else:
            with open(data_path) as f:
                n = len(json.load(f))
            print(f"Data file for '{topic_key}' already exists ({n} chunks).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Embed and insert new RAG topic data into DynamoDB.")
    parser.add_argument(
        "--topic",
        choices=list(TOPIC_CONFIG.keys()) + ["all"],
        default="all",
        help="Which topic to process (default: all)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Generate embeddings but skip DynamoDB writes.")
    parser.add_argument("--reset", action="store_true", help="Clear the table before inserting.")
    args = parser.parse_args()

    topics = list(TOPIC_CONFIG.keys()) if args.topic == "all" else [args.topic]

    print(f"Topics to process: {', '.join(topics)}")
    print(f"Dry run: {args.dry_run} | Reset: {args.reset}")

    ensure_data_files(topics)

    all_ok = True
    for topic in topics:
        ok = process_topic(topic, dry_run=args.dry_run, reset=args.reset)
        if not ok:
            all_ok = False

    print(f"\n{'='*65}")
    print("ALL DONE" if all_ok else "COMPLETED WITH ERRORS — check error files in data/")
