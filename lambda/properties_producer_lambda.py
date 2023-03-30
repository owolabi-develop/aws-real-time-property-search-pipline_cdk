import json
import boto3
import base64
from homeharvest import scrape_property
import datetime
from pprint import pprint
import os

    
def handler(event,context):
    finnhub_client_data = finnhub.Client(api_key=os.environ['API_KEY'])
    ## finnhub_client_data return covid19 data as list of dict
    kinesis_client = boto3.client('kinesis')
    for covid_data in finnhub_client_data.covid19():
        response = kinesis_client.put_record(
            StreamName=os.environ['STREAM_NAME'],
            Data=json.dumps(covid_data).encode('utf-8'),
            PartitionKey=covid_data['updated']
        )
    return response
    
    
    