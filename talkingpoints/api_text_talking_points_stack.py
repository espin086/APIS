from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam
)


class ApiTextTalkingPointsStack(Stack):

   def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        
        # create new IAM group and user
        group = iam.Group(self, "ComprehendGroup")
        user = iam.User(self, "ComprehendUser")
        # add IAM user to the new group
        user.add_to_group(group)
        
        
        #Defines and AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'api_text_talking_points',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='api_text_talking_points.lambda_handler',
            )
            
            
        # add Rekognition permissions for Lambda function
        statement = iam.PolicyStatement()
        statement.add_actions("comprehend:DetectKeyPhrases")
        statement.add_actions("execute-api:*")
        statement.add_resources("*")
        my_lambda.add_to_role_policy(statement)    
        
        #defines api gateway    
        apigw.LambdaRestApi(
            self, 'api-text-talking-points',
            handler=my_lambda,
            )