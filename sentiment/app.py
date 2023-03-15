#!/usr/bin/env python3

import aws_cdk as cdk

from api_text_sentiment.api_text_sentiment_stack import ApiTextSentimentStack


app = cdk.App()
ApiTextSentimentStack(app, "api-text-sentiment")

app.synth()
