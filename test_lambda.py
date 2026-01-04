import unittest
import boto3
from moto import mock_aws

from lambda_function import lambda_handler


@mock_aws
class TestVisitorCounterLambda(unittest.TestCase):

    def setUp(self):
        # Create a fake DynamoDB table
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        self.table = dynamodb.create_table(
            TableName="cloud-resume-counter",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST",
        )

        # Seed initial counter value
        self.table.put_item(
            Item={
                "id": "visitor-counter",
                "visits": 0
            }
        )

    def test_lambda_increments_counter(self):
        # Call the Lambda handler
        response = lambda_handler({}, {})

        # Validate HTTP response
        self.assertEqual(response["statusCode"], 200)

        # Validate DynamoDB update
        item = self.table.get_item(
            Key={"id": "visitor-counter"}
        )["Item"]

        self.assertEqual(item["visits"], 1)


if __name__ == "__main__":
    unittest.main()