import boto3
import json
import subprocess
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import boto.dynamodb
from boto.dynamodb2.table import Table
import time

def handler(event, context):
    g = event.get("menu_id")
    o = event.get("selection")
    selection = json.dumps(o)[1:-1:1]
    print selection
    print o
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('PizzaShopMenu')
    test = json.dumps(o)
    print test
    response = table.update_item(
                                Key={
                          'menu_id': g
                          },
        UpdateExpression="set selection= :r",
        ExpressionAttributeValues={
            ':r': o
        },
        ReturnValues="UPDATED_NEW"
        )
    
    
