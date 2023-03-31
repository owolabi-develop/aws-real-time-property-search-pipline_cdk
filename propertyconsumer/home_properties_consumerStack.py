from constructs import Construct
from aws_cdk import (
    Stack,
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb,
    Duration,
    aws_lambda_event_sources,
    aws_kinesis as kinesis,
    aws_s3,
    RemovalPolicy,
    aws_apigateway
    
)
STREAM_ARN= "arn:aws:kinesis:us-east-1:521427190825:stream/Latestproperty"

ENVIRONMENT = {
    "BUCKET_NAME":"properties-bucket"
}
class ConsumerStack(Stack):
     def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope,construct_id, **kwargs)
        
        lambda_consumer_role = iam.Role(
            self,
            id="lambdaRole",
             assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
             managed_policies=[
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"),
             ]
        )
        
        
        latestproperty_data_Consumerdb = _dynamodb.Table(self,
                                               id= "latestpropertydataConsumer",
                                               table_name="Latestproperty",
                                               partition_key=_dynamodb.Attribute(
                                                   name='city',type=_dynamodb.AttributeType.STRING),
                                               sort_key=_dynamodb.Attribute(
                                                   name='status',
                                                   type=_dynamodb.AttributeType.STRING
                                                   )
                                               )
         
        
        
        
        lambda_latestproperty_data_consumer = _lambda.Function(self,
                                             "lambdalatestpropertydataconsumer",
                                             runtime=_lambda.Runtime.PYTHON_3_10,
                                             code=_lambda.Code.from_asset("lambda"),
                                             handler="properties_consumer_lambda.handler",
                                             timeout=Duration.seconds(60),
                                             role=lambda_consumer_role,
                                             environment=ENVIRONMENT,
                                             )
        
        ### api gateaway lambda function 
        lambda_latestproperty_apigateway = _lambda.Function(self,
                                             "lambdalatestpropertyapigateway",
                                             runtime=_lambda.Runtime.PYTHON_3_10,
                                             code=_lambda.Code.from_asset("lambda"),
                                             handler="apigateway_lambda.handler",
                                             timeout=Duration.seconds(60),
                                             role=lambda_consumer_role,
                                             environment=ENVIRONMENT,
                                             )
        api_getway_role = iam.Role(
            self,
            id="apiGatewayRole",
             assumed_by=iam.ServicePrincipal("apigateway.amazonaws.com"),
             managed_policies=[
                 #iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                 iam.ManagedPolicy.from_aws_managed_policy_name("AWSLambda_FullAccess"),
             ]
        )
        
        ### api gatway -----------------------
        api_lambda_gateway = aws_apigateway.LambdaRestApi(
            self,"apilambdagateway",
            handler=lambda_latestproperty_apigateway,
            proxy=False,
            integration_options= aws_apigateway.LambdaIntegrationOptions(
                 allow_test_invoke=False,
                 timeout=Duration.seconds(1),
                 credentials_role=api_getway_role
            )
        )
         ## add resources
        propertie =  api_lambda_gateway.root.add_resource("properties")
        propertie.add_method("GET")
        propertie.add_resource("{city}")
        
        
       
        
         ## grant lambda_latestproperty_apigateway  full access to dynamodb
        latestproperty_data_Consumerdb.grant_full_access(lambda_latestproperty_apigateway)
        
        
        
        property_bucket = aws_s3.Bucket(self,
                                            id="Propertybucket",
                                            bucket_name="properties-bucket",
                                            removal_policy=RemovalPolicy.DESTROY,
                                            auto_delete_objects=True,
                                            encryption=aws_s3.BucketEncryption.KMS
                                            )
        
        property_bucket.grant_read_write(lambda_latestproperty_data_consumer)
        
        stream = kinesis.Stream.from_stream_arn(self,
                                                "LatestPropertiesStream",
                                                stream_arn=STREAM_ARN)
        
        lambda_latestproperty_data_consumer.add_event_source(
            aws_lambda_event_sources.KinesisEventSource(
                stream=stream,
                batch_size=100,
                starting_position=_lambda.StartingPosition.LATEST
                
            )
        )
        
        
        
        
        
        
        