#!/usr/bin/env python3
import os

import aws_cdk as cdk




app = cdk.App()
env_US = cdk.Environment(account="521427190825",region='us-east-1')

app.synth()
