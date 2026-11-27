import os
from pathlib import Path

from aws_cdk import App, CfnOutput, Duration, Environment, Stack
from aws_cdk import aws_ecr_assets as ecr_assets
from aws_cdk import aws_lambda as lambda_
from constructs import Construct


class SeleniumStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, *, env: Environment) -> None:
        super().__init__(scope, construct_id, env=env)

        function = lambda_.DockerImageFunction(
            self,
            "SeleniumFunction",
            code=lambda_.DockerImageCode.from_image_asset(
                str(Path(__file__).resolve().parent / "src"),
                platform=ecr_assets.Platform.LINUX_AMD64,
                # Export a Docker image manifest without an OCI attestation index.
                outputs=["type=docker,oci-mediatypes=false"],
            ),
            architecture=lambda_.Architecture.X86_64,
            memory_size=2048,
            timeout=Duration.seconds(120),
        )

        CfnOutput(self, "FunctionName", value=function.function_name)
        CfnOutput(self, "FunctionArn", value=function.function_arn)


app = App()
SeleniumStack(
    app,
    "SeleniumStack",
    env=Environment(
        account=os.environ.get("CDK_DEFAULT_ACCOUNT"),
        region=os.environ.get("CDK_DEFAULT_REGION"),
    ),
)
app.synth()
