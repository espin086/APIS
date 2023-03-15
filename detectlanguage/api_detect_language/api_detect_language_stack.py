from constructs import Construct
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam)

class ApiDetectLanguageStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

      # create new IAM group and user
        group = iam.Group(self, "ComprehendGroup")
        user = iam.User(self, "ComprehendUser")
        # add IAM user to the new group
        user.add_to_group(group)
        
        
        #Defines and AWS Lambda resource
        my_lambda = _lambda.Function(
            self, 'api-detect-language-lambda',
            runtime=_lambda.Runtime.PYTHON_3_7,
            code=_lambda.Code.from_asset('lambda'),
            handler='api-detect-language.lambda_handler',
            )
            
            
        # add Comprehend permissions for Lambda function
        statement = iam.PolicyStatement()
        statement.add_actions("comprehend:*")
        statement.add_actions("execute-api:*")
        statement.add_resources("*")
        my_lambda.add_to_role_policy(statement)    
        
        #defines api gateway    
        apigw.LambdaRestApi(
            self, 'api-detect-language-api',
            handler=my_lambda,
            )

