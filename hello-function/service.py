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



def handler(event, context):
    print "Hello World12"
    dynamodb0 = boto3.resource('dynamodb', region_name='us-west-2')
    table0 = dynamodb0.Table('Orders')
    # Your code goes here!
    e = event.get("menu_id")
    f = event.get("order_id")
    g = event.get("customer_name")
    h = event.get("customer_email")
    response = table0.put_item(
                              Item={
                              'menu_id': e,
                              'order_id': f,
                              'customer_name': g,
                              'customer_email': h,
                              'orders': {
                                  'selection':"NULL",
                                  'size': "NULL",
                                  'cost':"NULL",
                                  'order_time': "NULL"
                                }
                                }
                              )
    #print(json.dumps(response, indent=4, cls=DecimalEncoder))
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('PizzaShopMenu')
    response = table.get_item(ProjectionExpression="selection",
                          Key={
                          'menu_id': e
                          }
                          )
    item = response['Item']
    t = json.dumps(item['selection'])
    choice_list = t[1:-1:1].split(",")
    string = " "
    for i,choice in enumerate(choice_list,start=1):
        string = string + str(i)+". "+choice.split('"')[1]+"    "
    return "Message: Hi "+event.get("customer_name")+ ", please choose one of these selection:"+ string[:-4:]


