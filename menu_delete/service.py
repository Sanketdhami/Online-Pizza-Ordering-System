import boto3
import json
import subprocess
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto.dynamodb
from boto.dynamodb2.table import Table
import time


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)



def handler(event,context):
    g = event.get("menu_id")
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('PizzaShopMenu')
    response = table.delete_item(
                                Key={
                          'menu_id': event['menu_id']
                          }
        )
    return {}
    
