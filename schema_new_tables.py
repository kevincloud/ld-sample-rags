"""
Creates, describes, and deletes the four new RAG DynamoDB tables:
  - LoansAndCreditRAG
  - AccountManagementRAG
  - TransferTransactionsRAG
  - CustomerSupportRAG

Usage:
    python rag/schema_new_tables.py create      # create all four tables
    python rag/schema_new_tables.py describe    # describe all four tables
    python rag/schema_new_tables.py delete      # delete all four tables (with confirmation)
"""

import boto3
import os
import sys
from botocore.exceptions import ClientError

TABLES = [
    "LoansAndCreditRAG",
    "AccountManagementRAG",
    "TransferTransactionsRAG",
    "CustomerSupportRAG",
]


def get_region():
    return os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))


def get_client():
    return boto3.client("dynamodb", region_name=get_region())


def _create_one(client, table_name: str) -> bool:
    try:
        response = client.create_table(
            TableName=table_name,
            KeySchema=[
                {"AttributeName": "chunk_id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "chunk_id", "AttributeType": "S"},
                {"AttributeName": "content_type", "AttributeType": "S"},
                {"AttributeName": "created_at", "AttributeType": "S"},
            ],
            GlobalSecondaryIndexes=[
                {
                    "IndexName": "ContentTypeIndex",
                    "KeySchema": [
                        {"AttributeName": "content_type", "KeyType": "HASH"},
                        {"AttributeName": "created_at", "KeyType": "RANGE"},
                    ],
                    "Projection": {"ProjectionType": "ALL"},
                }
            ],
            BillingMode="PAY_PER_REQUEST",
        )
        print(f"Table '{table_name}' creation initiated. Status: {response['TableDescription']['TableStatus']}")

        print(f"Waiting for '{table_name}' to become ACTIVE...")
        table = boto3.resource("dynamodb", region_name=get_region()).Table(table_name)
        table.wait_until_exists()
        print(f"Table '{table_name}' is now ACTIVE.")
        return True

    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "ResourceInUseException":
            print(f"Table '{table_name}' already exists — skipping.")
            return True
        raise


def create_tables():
    client = get_client()
    for table_name in TABLES:
        _create_one(client, table_name)


def describe_tables():
    client = get_client()
    for table_name in TABLES:
        try:
            response = client.describe_table(TableName=table_name)
            table = response["Table"]
            print(f"\nTable: {table['TableName']}")
            print(f"  Status: {table['TableStatus']}")
            print(f"  Item count: {table.get('ItemCount', 0)}")
            print(f"  Billing mode: {table.get('BillingModeSummary', {}).get('BillingMode', 'PROVISIONED')}")
            print(f"  GSIs: {[g['IndexName'] for g in table.get('GlobalSecondaryIndexes', [])]}")
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "ResourceNotFoundException":
                print(f"\nTable '{table_name}': NOT FOUND")
            else:
                raise


def delete_tables():
    client = get_client()
    confirm = input(f"Type 'DELETE ALL' to confirm deletion of all 4 new RAG tables: ")
    if confirm != "DELETE ALL":
        print("Deletion cancelled.")
        return
    for table_name in TABLES:
        try:
            client.delete_table(TableName=table_name)
            print(f"Table '{table_name}' deletion initiated.")
        except ClientError as e:
            code = e.response["Error"]["Code"]
            if code == "ResourceNotFoundException":
                print(f"Table '{table_name}' not found — skipping.")
            else:
                raise


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "create"

    if command == "create":
        create_tables()
    elif command == "describe":
        describe_tables()
    elif command == "delete":
        delete_tables()
    else:
        print(f"Unknown command: {command}. Use: create | describe | delete")
