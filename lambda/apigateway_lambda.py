import boto3
import base64
import json
import logging
import datetime
import os

from decimal import Decimal
client = boto3.client('dynamodb')
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table('Latestproperty')
tableName = 'Latestproperty'


def handler(event,context):
    body = {}
    
    if event['routeKey'] == "GET /properties/{city}":
        prop = table.get_item(
                Key={'city': event['pathParameters']['city'],
                     "status":"sold"
                     })
        
        body = prop["Item"]
         

    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(body)
    } 
         
    return response