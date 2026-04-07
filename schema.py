import boto3
import os
from botocore.exceptions import ClientError

TABLE_NAME = "InvestmentAdvisorRAG"


def get_client():
    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("dynamodb", region_name=region)


def create_table():
    client = get_client()

    try:
        response = client.create_table(
            TableName=TABLE_NAME,
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
        print(f"Table '{TABLE_NAME}' creation initiated.")
        print(f"Status: {response['TableDescription']['TableStatus']}")

        print("Waiting for table to become ACTIVE...")
        waiter = boto3.resource(
            "dynamodb",
            region_name=os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        ).Table(TABLE_NAME)
        waiter.wait_until_exists()
        print(f"Table '{TABLE_NAME}' is now ACTIVE.")
        return True

    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "ResourceInUseException":
            print(f"Table '{TABLE_NAME}' already exists — skipping creation.")
            return True
        raise


def describe_table():
    client = get_client()
    response = client.describe_table(TableName=TABLE_NAME)
    table = response["Table"]
    print(f"Table: {table['TableName']}")
    print(f"Status: {table['TableStatus']}")
    print(f"Item count: {table.get('ItemCount', 0)}")
    print(f"Billing mode: {table.get('BillingModeSummary', {}).get('BillingMode', 'PROVISIONED')}")
    print(f"GSIs: {[g['IndexName'] for g in table.get('GlobalSecondaryIndexes', [])]}")


def delete_table():
    client = get_client()
    client.delete_table(TableName=TABLE_NAME)
    print(f"Table '{TABLE_NAME}' deletion initiated.")


if __name__ == "__main__":
    import sys

    command = sys.argv[1] if len(sys.argv) > 1 else "create"

    if command == "create":
        create_table()
    elif command == "describe":
        describe_table()
    elif command == "delete":
        confirm = input(f"Type '{TABLE_NAME}' to confirm deletion: ")
        if confirm == TABLE_NAME:
            delete_table()
        else:
            print("Deletion cancelled.")
    else:
        print(f"Unknown command: {command}. Use: create | describe | delete")
