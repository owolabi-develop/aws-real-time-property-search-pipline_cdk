import json
import boto3
import os
from homeharvest import scrape_property
import random

    
def handler(event,context):
    locations = ['Dallas, TX',"San Diego, CA"]
    listing_types = ["sold","for_sale","for_rent","pending"]
    past_days = [_ for _ in range(10,50)]
    
    kinesis_client = boto3.client('kinesis')
    
    properties = scrape_property(
    radius=30.5,
    location=random.choice(locations),
    listing_type=random.choice(listing_types), 
    past_days=random.choice(past_days),
   )
   
    properties_data = json.loads(properties.to_json(orient='records'))
    
    for properties in properties_data:
        response = kinesis_client.put_record(
            StreamName=os.environ['STREAM_NAME'],
            Data=json.dumps(properties).encode('utf-8'),
            PartitionKey=properties['year_built']
        )
    return response
    
    
    