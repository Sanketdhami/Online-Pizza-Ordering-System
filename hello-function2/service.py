import boto3
import json
import subprocess
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto.dynamodb
from boto.dynamodb2.table import Table

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



def handler(event,context):
    g = event.get("order_id")
    dynamodb0 = boto3.resource('dynamodb', region_name='us-west-2')
    table0 = dynamodb0.Table('Orders')
                # Your code goes here!

    response = table0.get_item(
                          Key={
                          'order_id': g
                          }
                          )
    item1 = response['Item']
    return item1