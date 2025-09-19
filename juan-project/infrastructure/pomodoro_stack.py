from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_s3_deployment as s3deploy,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class PomodoroStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket para frontend
        frontend_bucket = s3.Bucket(
            self, "PomodoroFrontend",
            website_index_document="index.html",
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Lambda function para backend
        pomodoro_lambda = _lambda.Function(
            self, "PomodoroFunction",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset("../lambda"),
        )

        # API Gateway
        api = apigw.RestApi(
            self, "PomodoroApi",
            rest_api_name="Pomodoro Service",
            description="API para Pomodoro Timer",
            default_cors_preflight_options=apigw.CorsOptions(
                allow_origins=apigw.Cors.ALL_ORIGINS,
                allow_methods=apigw.Cors.ALL_METHODS,
                allow_headers=["Content-Type", "X-Amz-Date", "Authorization"]
            )
        )

        # Integração Lambda com API Gateway
        lambda_integration = apigw.LambdaIntegration(pomodoro_lambda)
        api.root.add_resource("timer").add_method("POST", lambda_integration)

        # CloudFront distribution
        distribution = cloudfront.CloudFrontWebDistribution(
            self, "PomodoroDistribution",
            origin_configs=[
                cloudfront.SourceConfiguration(
                    s3_origin_source=cloudfront.S3OriginConfig(
                        s3_bucket_source=frontend_bucket
                    ),
                    behaviors=[cloudfront.Behavior(is_default_behavior=True)]
                )
            ]
        )

        # Deploy frontend para S3
        s3deploy.BucketDeployment(
            self, "DeployFrontend",
            sources=[s3deploy.Source.asset("../")],
            destination_bucket=frontend_bucket,
            include=["*.html", "*.css", "*.js"]
        )

        # Outputs
        CfnOutput(self, "WebsiteURL", value=distribution.distribution_domain_name)
        CfnOutput(self, "ApiURL", value=api.url)