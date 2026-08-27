import json
import os

import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    try:
        # API Gateway HTTP API:
        # GET /users/{id}
        user_id = event.get("pathParameters", {}).get("id")

        if not user_id:
            return response(400, {"error": "Missing user id"})

        result = table.get_item(Key={"id": user_id})

        item = result.get("Item")

        if not item:
            return response(404, {"error": "User not found"})

        return response(200, item)

    except ClientError as e:
        print(f"DynamoDB error: {e}")

        return response(500, {"error": "Internal server error"})

    except Exception as e:
        print(f"Unexpected error: {e}")

        return response(500, {"error": "Internal server error"})
