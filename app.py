import os
from aws_cdk import Tags
import aws_cdk as cdk
from kinesisStream.kinesis_stream_firehosedeliveryStack import KinesisStreamFireHoseDeliveryStack
from propertyconsumer.home_properties_consumerStack import ConsumerStack
from propertyproducer.home_properties_producerStack import HomePropertiesStack



app = cdk.App()
env_US = cdk.Environment(account="521427190825",region='us-east-1')

KinesisStreamFireHoseDeliveryStack(app,"KinesisStreamFireHoseDeliveryStack",env=env_US)
ConsumerStack(app,"ConsumerStack",env=env_US)
HomePropertiesStack(app,"HomePropertiesStack",env=env_US)

Tags.of(app).add("ProjectOwner","Owolabi akintan")
Tags.of(app).add("ProjectName","real-time-properties-search-pipline")

app.synth()
