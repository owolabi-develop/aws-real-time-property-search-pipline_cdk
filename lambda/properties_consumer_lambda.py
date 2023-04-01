import boto3
import base64
import json
import logging
import datetime
import os


def handler(event,context):
    BUCKET_NAME = os.environ['BUCKET_NAME']
    dynamodb = boto3.resource('dynamodb')
    s3_client = boto3.client('s3')
    table = dynamodb.Table("Latestproperty")
    for record in event['Records']:
        record_data = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        data = json.loads(record_data)
        table.put_item(
            Item=data
        )
       
       
    