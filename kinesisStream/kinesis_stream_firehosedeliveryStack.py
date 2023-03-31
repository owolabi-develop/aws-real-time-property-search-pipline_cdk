from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    aws_kinesis as _kinesis,
    Duration,
    aws_kinesisfirehose as _firehose,
    aws_iam as _iam,
    aws_s3 as _s3
    
)





class KinesisStreamFireHoseDeliveryStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        property_stream = _kinesis.Stream(self,
                                             "KinesisStreamFireHoseDelivery",
                                             shard_count=1,
                                             stream_name="Latestproperty",
                                             retention_period=Duration.hours(24)
                                             )
        # firehose_role = _iam.Role(self,
        #                      "firshoserole",
        #                      assumed_by=_iam.ServicePrincipal('firehose.amazonaws.com'),
        #                      managed_policies=[
        #                         #_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRedshiftFullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        #                      ]
                             
        #                      )
        
        # redshift_role = _iam.Role(self,
        #                      "firshoserole",
        #                      assumed_by=_iam.ServicePrincipal('redshift.amazonaws.com'),
        #                      managed_policies=[
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFirehoseFullAccess"),
        #                         _iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
        #                      ]
                             
        #                      )
        
        # redshift_bucket = _s3.Bucket(self,"redshfitbucket",
        #                              bucket_name='redshift-result'
        #                       )
        
        # firehose_delivery = _firehose.CfnDeliveryStream(
            
        #     ## kinesis connection
        #     kinesis_stream_source_configuration= _firehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(
        #         kinesis_stream_arn= property_stream.stream_arn,
        #         role_arn=firehose_role.role_arn
        #     ),
            
        #     delivery_stream_name="property-data",
        #     delivery_stream_type="KinesisStreamAsSource",
            
        #     ## redshift connection option
        #     redshift_destination_configuration= _firehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty(
        #         cluster_jdbcurl="jdbc:redshift://property-cluster-1.c45bn1ihlinj.us-east-1.redshift.amazonaws.com:5439/dev",
        #         copy_command=_firehose.CfnDeliveryStream.CopyCommandProperty(
        #         data_table_name="dataTableName",
                  
        # ),
        #     s3_configuration=_firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
        #     bucket_arn=redshift_bucket.bucket_arn,
        #     role_arn=redshift_role.role_arn,
        #     ),
            
                
        #         password="84563320Owo",
        #         username="owolabi84",
        #         role_arn= redshift_role.role_arn
        #     )
              
        # )
        
        
        # redshift_bucket.grant_read_write(firehose_delivery)