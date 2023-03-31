from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    Duration,
    aws_iam as _iam,
    aws_s3 as _s3,
    aws_lambda as _lambda,
    aws_events,
    aws_events_targets,
    
)

ENVIRONMENT = {
    "STREAM_NAME":"Latestproperty"
}


class HomePropertiesStack(Stack):
     def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        lambda_role = _iam.Role(
            self,
            "lambdaRole",
             assumed_by=_iam.ServicePrincipal("lambda.amazonaws.com"),
             managed_policies=[
                 _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                 _iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                 _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                
             ]
        )
        
        homeharvest_data_layer = _lambda.LayerVersion(
            self,
            "homeharvestdatalayer",
            code=_lambda.AssetCode("layer/property_layer")
        )
        
        
        
        lambda_properties_data_producer = _lambda.Function(self,
                                             "propertiesdataproducer",
                                             runtime=_lambda.Runtime.PYTHON_3_10,
                                             code=_lambda.Code.from_asset("lambda"),
                                             handler="properties_producer_lambda.handler",
                                             timeout=Duration.minutes(3),
                                             layers=[homeharvest_data_layer],
                                             role=lambda_role,
                                             environment=ENVIRONMENT
                                             )
        
        properties_data_rule = aws_events.Rule(self,
                                            "propertiesdata",
                                            enabled=True,
                                            schedule=aws_events.Schedule.rate(Duration.minutes(1))
                                            )
        properties_data_target = aws_events_targets.LambdaFunction(
            handler= lambda_properties_data_producer,
            retry_attempts=3
        )
        properties_data_rule.add_target(properties_data_target)