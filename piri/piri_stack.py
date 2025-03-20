from aws_cdk import (
    Duration,
    Stack,
    core as cdk,
    aws_lambda as lambda_,
    aws_apigateway as apigw
)
from constructs import Construct

class PiriStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "PiriQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )

        # Definir Lambda
        flask_lambda = lambda_.Function(
            self, "FlaskLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.lambda_handler",
            code=lambda_.Code.from_asset("lambda"),
            memory_size=512,
            timeout=cdk.Duration.seconds(30),
        )

        # API Gateway para exponer el servicio Flask
        api = apigw.LambdaRestApi(
            self, "FlaskApi",
            handler=flask_lambda,
            proxy=True
        )

        cdk.CfnOutput(self, "APIEndpoint", value=api.url)
