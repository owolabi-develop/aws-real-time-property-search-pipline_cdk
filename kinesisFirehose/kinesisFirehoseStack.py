from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    aws_kinesis as _kinesis,
    Duration,
    aws_kinesisfirehose as _firehose,
    aws_iam as _iam,
    aws_s3 as _s3,
    aws_glue as _glue,
    aws_s3_deployment as _s3deploy,
    aws_lakeformation as _lakeformation,
    RemovalPolicy,
    aws_sqs as _sqs ,
    aws_events as _events,
    aws_s3_notifications as s3n,
)
import aws_cdk.aws_s3_deployment as s3deploy





class KinesisFireHoseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        firehose_role = _iam.Role(self,
                             "firshoserole",
                             assumed_by=_iam.ServicePrincipal('firehose.amazonaws.com'),
                             managed_policies=[
                                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
                                _iam.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"),
                                _iam.ManagedPolicy.from_aws_managed_policy_name("AmazonKinesisFullAccess"),
                                #_iam.ManagedPolicy.from_aws_managed_policy_name("AmazonRedshiftFullAccess"),
                                _iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
                             ]
                             
                             )
        
        
        raw_zone_bucket = _s3.Bucket(self,
                                     "Rawzonebucket",
                                     bucket_name='property-raw-zone',
                                     removal_policy=RemovalPolicy.DESTROY,
                                     auto_delete_objects=True
                              )
        
        consumption_zone_bucket = _s3.Bucket(self,
                                             "ConsumptionZonebucket",
                                            bucket_name='property-consumption-zone',
                                            removal_policy=RemovalPolicy.DESTROY,
                                            auto_delete_objects=True
                              )
        
       
        
        
        
        
        ## kinesis firehose delivery stream
        firehose_delivery = _firehose.CfnDeliveryStream(self,id="firehose_delivery",
            
            ## kinesis connection
            kinesis_stream_source_configuration= _firehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty(
                kinesis_stream_arn= property_stream.stream_arn,
                role_arn=firehose_role.role_arn
            ),
            s3_destination_configuration=_firehose.CfnDeliveryStream.S3DestinationConfigurationProperty(
                bucket_arn= raw_zone_bucket.bucket_arn,
                role_arn=firehose_role.role_arn,    
            ),
            
            delivery_stream_name="property-data",
            delivery_stream_type="KinesisStreamAsSource",  
        )
        
       
       
        
        
        ## glue script bucket
        glue_script_bucket = _s3.Bucket(self,
                                             "gluescriptbucket",
                                            bucket_name='property-glue-script-bucket',
                                            removal_policy=RemovalPolicy.DESTROY,
                                            auto_delete_objects=True
                              )
        
        ### deploy the glue script 
        
        s3deploy.BucketDeployment(self,"deployment",
                                  sources=[s3deploy.Source.asset('glue/')],
                                  destination_bucket=glue_script_bucket)
        
        
        
        ## sqs que to trigger glue
        glue_queue = _sqs.Queue(self, 'glue_queue')
        raw_zone_bucket.add_event_notification(_s3.EventType.OBJECT_CREATED, s3n.SqsDestination(glue_queue))
        
        
        glue_role = _iam.Role(self, 'glue_role',
                      role_name='GlueRole',
                      description='Role for Glue services to access S3',
                      assumed_by=_iam.ServicePrincipal('glue.amazonaws.com'),
                      inline_policies={'glue_policy': _iam.PolicyDocument(
                          statements=[_iam.PolicyStatement(
                            effect=_iam.Effect.ALLOW,
                            actions=['s3:*', 'glue:*', 'iam:*', 'logs:*',
                            'cloudwatch:*', 'sqs:*', 'ec2:*','cloudtrail:*'],
                            resources=['*'])])})

        glue_database = _glue.CfnDatabase(self, 'propertydatabase',
                                        catalog_id=cdk.Aws.ACCOUNT_ID,
                                        database_input=_glue.CfnDatabase.DatabaseInputProperty(
                                            name='property-database',
                                            description='Database to store property details'))

        _lakeformation.CfnPermissions(self, 'lakeformation_permission',
                    data_lake_principal=_lakeformation.CfnPermissions.DataLakePrincipalProperty(
                        data_lake_principal_identifier=glue_role.role_arn),
                    resource=_lakeformation.CfnPermissions.ResourceProperty(
                        database_resource=_lakeformation.CfnPermissions.DatabaseResourceProperty(
                            catalog_id=glue_database.catalog_id,
                            name='property-database')),
                    permissions=['ALL'])
        
        
        
        _glue.CfnCrawler(self, 'glue_crawler',
                 name='property_crawler',
                 role=glue_role.role_arn,
                 database_name='property-database',
                 targets=_glue.CfnCrawler.TargetsProperty(
                     s3_targets=[_glue.CfnCrawler.S3TargetProperty(
                         path=f's3://{raw_zone_bucket.bucket_name}/',
                         event_queue_arn=glue_queue.queue_arn)]),
                 recrawl_policy=_glue.CfnCrawler.RecrawlPolicyProperty(
                     recrawl_behavior='CRAWL_EVENT_MODE'))

        glue_job = _glue.CfnJob(self, 'glue_job',
                                name='glue_job',
                                command=_glue.CfnJob.JobCommandProperty(
                                    name='pythonshell',
                                    python_version='3.9',
                                    script_location=f's3://{glue_script_bucket.bucket_name}/glue_job.py'),
                                role=glue_role.role_arn,
                                glue_version='3.0',
                                timeout=3)
        
        
        
        glue_workflow = _glue.CfnWorkflow(self, 'glue_workflow',
                                  name='glue_workflow',
                                  description='Workflow to process the coffee data.')

        _glue.CfnTrigger(self, 'glue_crawler_trigger',
                        name='glue_crawler_trigger',
                        actions=[_glue.CfnTrigger.ActionProperty(
                            crawler_name='property_crawler',
                            notification_property=_glue.CfnTrigger.NotificationPropertyProperty(notify_delay_after=3),
                            timeout=3)],
                        type='EVENT',
                        workflow_name=glue_workflow.name)

        _glue.CfnTrigger(self, 'glue_job_trigger',
                        name='glue_job_trigger',
                        actions=[_glue.CfnTrigger.ActionProperty(
                            job_name=glue_job.name,
                            notification_property=_glue.CfnTrigger.NotificationPropertyProperty(notify_delay_after=3),
                            timeout=3)],
                        type='CONDITIONAL',
                        start_on_creation=True,
                        workflow_name=glue_workflow.name,
                        predicate=_glue.CfnTrigger.PredicateProperty(
                            conditions=[_glue.CfnTrigger.ConditionProperty(
                                crawler_name='property_crawler',
                                logical_operator='EQUALS',
                                crawl_state='SUCCEEDED')]))
        
        rule_role = _iam.Role(self, 'rule_role',
                      role_name='EventBridgeRole',
                      description='Role for EventBridge to trigger Glue workflows.',
                      assumed_by=_iam.ServicePrincipal('events.amazonaws.com'),
                      inline_policies={
                          'eventbridge_policy': _iam.PolicyDocument(statements=[_iam.PolicyStatement(
                              effect=_iam.Effect.ALLOW,
                              actions=['events:*', 'glue:*'],
                              resources=['*'])])})

        _events.CfnRule(self, 'rule_s3_glue',
                        name='rule_s3_glue',
                        role_arn=rule_role.role_arn,
                        targets=[_events.CfnRule.TargetProperty(
                            arn=f'arn:aws:glue:{cdk.Aws.REGION}:{cdk.Aws.ACCOUNT_ID}:workflow/glue_workflow',
                            role_arn=rule_role.role_arn,
                            id=cdk.Aws.ACCOUNT_ID)],
                        event_pattern={
                            "detail-type": ["Object Created"],
                            "detail": {
                                "bucket": {"name": [f"{raw_zone_bucket.bucket_name}"]}},
                            "source": ["aws.s3"]})