import json 
import boto3


def detect_sentiment(text, language_code='en'):
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    response = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return response


def lambda_handler(event, context):
    print('request: {}'.format(json.dumps(event)))
    
    
    text = event["queryStringParameters"]["text"]
    sentiment = detect_sentiment(text=text)
    print('sentiment: {}'.format(sentiment))
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "text ": text,
            "sentiment ": sentiment
        })
    }
    
