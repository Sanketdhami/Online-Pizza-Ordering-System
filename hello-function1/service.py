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
    print "Hello World"
    
    dynamodb0 = boto3.resource('dynamodb', region_name='us-west-2')
    table0 = dynamodb0.Table('Orders')
                # Your code goes here!
    g = event.get("input")
    o = event.get("order_id")
    selection_number = int(json.dumps(g)[1:-1:1])-1

    response = table0.get_item(ProjectionExpression="menu_id, orders.selection",
                          Key={
                          'order_id': o
                          }
                          )
    item1 = response['Item']
    t = item1['menu_id']
    t2 = item1['orders']['selection']

    if(t2 == "NULL"):
        print "True"
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('PizzaShopMenu')
        response1 = table.get_item(ProjectionExpression="selection",
                            Key={
                            'menu_id': t
                            }
                            )
        item = response1['Item']
        test = json.dumps(item['selection'])
        choice_list = test[1:-1:1].split(",")
        choice =  (choice_list[selection_number])[1:-1:1]
        if (choice[0].isalpha()==False) :
            choice = choice[1:]

        dynamodb0 = boto3.resource('dynamodb', region_name='us-west-2')
        table0 = dynamodb0.Table('Orders')
        response = table0.update_item(
                                    Key={
                                        'order_id': o
                                },
        UpdateExpression="set orders.selection = :r, order_status  = :a",
        ExpressionAttributeValues={
            ':r': choice,
            ':a': "processing"
        },
        ReturnValues="UPDATED_NEW"
        )

        dynamodb1 = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb1.Table('PizzaShopMenu')
        response = table.get_item(ProjectionExpression="size",
                            Key={
                            'menu_id': t
                            }
                            )
        item = response['Item']
        t = json.dumps(item['size'])
        size_list = t[1:-1:1].split(",")
        string = " "
        for i,size in enumerate(size_list,start=1):
            string = string + str(i)+". "+size.split('"')[1]+"    "
        return "Message : Which size do you want?"+ string[:-4:]

    else:
        dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
        table = dynamodb.Table('PizzaShopMenu')
        response1 = table.get_item(ProjectionExpression="size,price",
                            Key={
                            'menu_id': t
                            }
                            )
        item = response1['Item']
        test = json.dumps(item['size'])
        choice_list = test[1:-1:1].split(",")
        choice =  (choice_list[selection_number])[1:-1:1]
        if (choice[0].isalpha()==False) :
            choice = choice[1:]
        
        test3 = item['price']
        costs =  test3[selection_number]
        print costs
        localtime   = time.localtime()
        timeString  = time.strftime("%m-%d-%Y@%H:%M:%S", localtime)

        dynamodb0 = boto3.resource('dynamodb', region_name='us-west-2')
        table0 = dynamodb0.Table('Orders')
        response = table0.update_item(
                                    Key={
                                        'order_id': o
                                },
        UpdateExpression="set orders.size = :r, orders.cost = :p, orders.order_time = :q",
        ExpressionAttributeValues={
            ':r': choice,
            ':p': costs,
            ':q': timeString
        },
        ReturnValues="UPDATED_NEW"
        )

        #todays =  str(datetime.date.today())
        #date_time = datetime.datetime.strptime(todays, '%m-%d-%Y')
        #print date_time

        return "Message : Your order costs $"+str(costs)+". We will email you when the order is ready. Thank you!"


