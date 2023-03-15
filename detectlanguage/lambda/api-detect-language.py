import json
import boto3


def detect_language(text):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_dominant_language(Text=text)
    return response


def lambda_handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    
    
    text = event["queryStringParameters"]["text"]
    result = detect_language(text=text)
    print('result: {}'.format(result))
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "text ": text,
            "result ": result
        })
    }

