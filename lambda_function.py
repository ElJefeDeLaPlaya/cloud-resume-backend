import json
import boto3
from botocore.exceptions import ClientError

def get_table():
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    return dynamodb.Table("cloud-resume-counter")
    
def lambda_handler(event, context):
    try:
        table = get_table()

        response = table.update_item(
            Key={"id": "visitor-counter"},
            UpdateExpression="ADD visits :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW",
        )

        visits = int(response["Attributes"]["visits"])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"visits": visits}),
        }

    except ClientError as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
        }