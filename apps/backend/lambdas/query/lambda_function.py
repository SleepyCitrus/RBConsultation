import json

from botocore.exceptions import ClientError
from query.aggregation.aggregation_service import AggregationService
from shared.database.ddb_service import DDBService

ddbService = DDBService()
aggService = AggregationService(ddbService=ddbService)


def response(status_code, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps(body),
    }


def lambda_handler(event, context):
    try:
        set_name = event["set_name"]

        items = aggService.get_aggregation_by_set(set_name)
        print(items)

        return response(200, items)

    except ClientError as e:
        print(f"DynamoDB error: {e}")

        return response(500, {"error": "Internal server error"})

    except Exception as e:
        print(f"Unexpected error: {e}")

        return response(500, {"error": "Internal server error"})
