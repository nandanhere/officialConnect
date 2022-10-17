import time
import time
from json import dumps
from decimal import Decimal
import json



import boto3
from operator import add
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table("proctor")
studtable = dynamodb.Table("students")
 
 


def add_proctor(data):
    
    print("add_proctor")
    table = dynamodb.Table("proctor") 
    proctor_name = data['proctor_name']
    proctor_email = data['proctor_email']
    if proctor_name and proctor_email:
        try:
            table.put_item(Item={
                "proctor_email":proctor_email,
                "proctor_name":proctor_name,
                "enrolled_set" :set([""]),
                "requests_set" : set([""]),
                "enrolled":[],
                "messages":[],
                "requests":[]
            })
            return dumps({"message":"SUCCESS"})
        except Exception as e:
            print(e)
            return {"result":"error", "Issue":e}


def request_proctor(data):
    try:
        
        print("request_proctor")
        proctor_email = data['proctor_email']
        details = data['details']
        if proctor_email:
            result = table.update_item(
                        Key={
                            'proctor_email': proctor_email,
                        },
                        UpdateExpression='SET requests = list_append(requests, :student_obj) ADD requests_set :usn',
                        ConditionExpression="(NOT contains(requests_set, :usnstr)) AND (NOT contains(enrolled_set,:usnstr))",
                        ExpressionAttributeValues={
            ":student_obj": [
                    details
            ],
            ":usn":set([details['usn']]),
                        ":usnstr":details['usn']

        },)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})


# Note that this will never get usn which is not in requests

def accept_proctee(data):
    try:
        
        print("accept_proctee")
        usn = data['usn']
        proctor_email = data['proctor_email']
        if proctor_email:
            response = table.get_item(Key={'proctor_email': proctor_email,})
            requests = response['Item']['requests']
            print(requests)
            newreq = []
            enrolled = None
            for i in requests:
                if i and i['usn'] == usn:
                    enrolled = i
                else:
                    newreq.append(i)
            try:
                table.update_item(
                        Key={
                            'proctor_email': proctor_email,
                        },
                        UpdateExpression='SET requests = :student_obj , enrolled = list_append(enrolled, :new) DELETE requests_set :usnobj ADD enrolled_set :usnobj',
                        ExpressionAttributeValues={
                        ":usnobj":set([usn]),":new":[enrolled],
            ":student_obj": 
                    newreq
            ,},)
                studtable.put_item(Item={
                "usn":usn,
                "proctor_email":proctor_email,
            })
            except Exception as e:
                dumps({'error' : str(e)})
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})


def reject_proctee(data):
    try:
        
        print("reject_proctee")
        proctor_email = data['proctor_email']
        usn = data['usn']
        if proctor_email:
            response = table.get_item(Key={'proctor_email': proctor_email,})
            requests = response['Item']['requests']
            newreq = []
            for i in requests:
                if i and i['usn'] != usn:
                    newreq.append(i)
            try:
                table.update_item(
                        Key={
                            'proctor_email': proctor_email,
                        },
                        UpdateExpression='SET requests = :student_obj DELETE requests_set :usnobj',
                        ExpressionAttributeValues={
                        ":usnobj":set([usn]),
            ":student_obj": 
                    newreq
            ,},)
            except Exception as e:
                dumps({'error' : str(e)})
            return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})




def send_message(data):
    try:
        
        print("send_message")
        proctor_email = data['proctor_email']
        if proctor_email:
            t = time.time()
            print(t)
            res = table.update_item(
                        Key={
                            'proctor_email': proctor_email,
                        },
                        UpdateExpression='SET messages = list_append(messages, :message_obj)',
                        ExpressionAttributeValues={
                                         ":message_obj":  
                                                [{
                                     "message_title":data['message_title'],
                                    "proctor_name":data['proctor_name'],
                                    "message_body":data['message_body'],
                                    "usn_list":data['usn_list'],
                                    "time": Decimal(t)
                                }],
                                },
                            )
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})


def delete_message(data):
    try:
        
        proctor_email = data['proctor_email']
        t = data['time']
        if proctor_email:
            response = table.get_item(Key={'proctor_email': proctor_email,})
            requests = response['Item']['messages']
            newreq = []
            for i in requests:
                print(i["time"] == t)
                if i and i['time'] != t:
                    newreq.append(i)
            try:
                table.update_item(
                        Key={
                            'proctor_email': proctor_email,
                        },
                        UpdateExpression='SET messages = :messages',
                        ExpressionAttributeValues={
            ":messages": 
                    newreq
            ,},)
            except Exception as e:
                print(e)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})


def get_messages(usn):
    try:
        
        x = studtable.get_item(Key={"usn":usn})
        if "Item" not in x:
            print("not registered")
            return dumps({'message' : 'not_registered'})        # if the usn is not registered in any way
        # print(x["Item"]["proctor_email"])
        try:
            x = x['Item']
            if x and x['proctor_email']:
                email = x['proctor_email']
                response = table.get_item(Key={'proctor_email': email})
                # print(response["Item"]["messages"])
                xx = response['Item']["messages"]
                ret = []
                proctor_name = ""
                for message in xx:
                    
                    if message and usn in message['usn_list']:
                        proctor_name  = message["proctor_name"]
                        message["time"] = float(message["time"])
                        ret.append(message)
                return dumps({'message' : 'SUCCESS','messages':ret,"proctor_email":email,"proctor_name":proctor_name})
        except Exception as e:
            return dumps({'error' : str(e)})
    except Exception as e:
        return dumps({'error' : str(e)})


def remove_proctee(data):
    print("remove_proctee")
    try:
        
        usn = data['usn']
        proctor_email = data['proctor_email']
        if proctor_email:
            response = table.get_item(Key={'proctor_email': proctor_email,})
            print(response["Item"])
            enrolled = response['Item']['enrolled']
            newreq = []
            for i in enrolled:
                if i and i['usn'] != usn:
                    newreq.append(i)
            try:
                table.update_item(
                        Key={
                            'proctor_email': proctor_email,
                        },
                        UpdateExpression='SET enrolled = :student_obj DELETE enrolled_set :usnobj',
                        ExpressionAttributeValues={
                        ":usnobj":set([usn]),
            ":student_obj": 
                    newreq
            ,},)
                studtable.delete_item(Key={
                "usn":usn,
             })
            except Exception as e:
                return dumps({'error' : str(e)})
            return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})


def get_proctor_details(data):
    
    print("get_proctor_details")
    try:
        email = data['proctor_email']
        response = table.get_item(Key={'proctor_email': email,})
        item = response['Item']
        messages = item["messages"]
        for i in range(len(messages)):
            if messages[i]:
                messages[i]['time'] = float(messages[i]['time'])
        return dumps({
                "proctor_email":email,
                "proctor_name":item["proctor_name"],
                "enrolled":item["enrolled"],
                "messages":messages,
                "requests":item["requests"]
            })
    except Exception as e:
        return dumps({'error':str(e)})

 

def lambda_handler(event, context):
    function = event['queryStringParameters']["function"]
    body = {}
    if function == "get_messages":
        usn = event['queryStringParameters']["usn"]
        body = get_messages(usn)
    else:
        data = json.loads(event['body'])
    if function == "get_proctor_details":
        body = get_proctor_details(data)
    elif function == "remove_proctee":
        body = remove_proctee(data)
    elif function == "add_proctor":
        body = add_proctor(data)
    elif function == "delete_message":
        body = delete_message(data)
    elif function == "send_message":
        body = send_message(data)
    elif function == "reject_proctee":
        body = reject_proctee(data)
    elif function == "accept_proctee":
        body = accept_proctee(data)
    elif function == "request_proctor":
        body = request_proctor(data)
     
    return {
        'statusCode':200,
        'body':body
    }
 