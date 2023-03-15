import json
import boto3

def lambda_handler(event, context):
    request = 'request: {}'.format(json.dumps(event))
    print(request)
    return {
    "statusCode": 200,
    "headers": {
    "Content-Type": "application/json"
    },
    "body": json.dumps({
    "request ": request,
    "test_string ": "This is a test string",
    })
    }