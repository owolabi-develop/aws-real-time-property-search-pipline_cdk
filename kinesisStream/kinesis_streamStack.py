from constructs import Construct
import aws_cdk as cdk
from  aws_cdk import (
    Stack,
    aws_kinesis as _kinesis,
    Duration,
)




class KinesisStreamStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **Kwargs):
        super().__init__(scope, construct_id, **Kwargs)
        
        property_stream = _kinesis.Stream(self,
                                             "KinesisStreamFireHoseDelivery",
                                             shard_count=1,
                                             stream_name="Latestproperty",
                                             retention_period=Duration.hours(24)
                                             )
      