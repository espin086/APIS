import json 
import boto3


def detect_talking_points(text, language_code='en'):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_key_phrases(Text=text, LanguageCode=language_code)
    return response


def lambda_handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    
    
    text = event["queryStringParameters"]["text"]
    talking_points = detect_talking_points(text=text)
    print('sentiment: {}'.format(talking_points))
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "text ": text,
            "talking_points ": talking_points
        })
    }
    
