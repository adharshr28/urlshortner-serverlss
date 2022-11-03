import os
import json
import boto3
from string import ascii_letters, digits
from random import choice, randint
from time import strftime, time
from urllib import parse

app_url =  'https://test.com/'  #The app_url will be your domain name, as this will be returned to the client with the short id os.getenv('APP_URL')
min_char = 6 #min number of characters in short url unique string
max_char = 8 #max number of characters in short url unique string
string_format = ascii_letters + digits

ddb = boto3.resource('dynamodb', region_name = 'ap-northeast-1').Table('URL-Shortener') #Set region and Dynamo DB table

def generate_timestamp():
    response = strftime("%Y-%m-%dT%H:%M:%S")
    return response

def expiry_date():
    response = int(time()) + int(604800) #generate expiration date for the url based on the timestamp
    return response

def check_id(short_id):
    if 'Item' in ddb.get_item(Key={'shortid': short_id}):
        response = generate_id()
    else:
        return short_id

def generate_id():
    print(min_char,max_char)
    short_id = "".join(choice(string_format) for x in range(randint(min_char, max_char))) #generate unique value for the short url
    print(short_id)
    response = check_id(short_id)
    return response

def lambda_handler(event, context):
    analytics = {}
    print(event)
    short_id = generate_id()
    short_url = app_url + short_id
    # long_url = json.loads(event.get('body')).get('long_url')
    long_url = event['long_url']
    timestamp = generate_timestamp()
    ttl_value = expiry_date()

    #put value in dynamodb table
    response = ddb.put_item(
        Item={
            'shortid': short_id,
            'created_at': timestamp,
            'ttl': int(ttl_value),
            'short_url': short_url,
            'long_url': long_url
        }
    )
    body_new = '{"shortid":"' +short_url+'","long_url":"'+long_url+'"}'
    return {"statusCode": 200,"body": body_new} #return the body with long and short url
