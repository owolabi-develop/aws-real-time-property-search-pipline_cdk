import boto3
import base64
import json
import logging
import datetime
import os


def handler(event,context):
    dynamodb = boto3.resource('dynamodb')
   
       
    