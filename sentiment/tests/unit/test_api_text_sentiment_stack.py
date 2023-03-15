import aws_cdk as core
import aws_cdk.assertions as assertions
from api_text_sentiment.api_text_sentiment_stack import ApiTextSentimentStack


def test_sqs_queue_created():
    app = core.App()
    stack = ApiTextSentimentStack(app, "api-text-sentiment")
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::SQS::Queue", {
        "VisibilityTimeout": 300
    })


def test_sns_topic_created():
    app = core.App()
    stack = ApiTextSentimentStack(app, "api-text-sentiment")
    template = assertions.Template.from_stack(stack)

    template.resource_count_is("AWS::SNS::Topic", 1)
