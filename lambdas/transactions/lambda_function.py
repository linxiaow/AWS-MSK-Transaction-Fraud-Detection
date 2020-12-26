import json
import base64
from kafka import KafkaProducer
from constants import *
import datetime
import boto3


def verify_user(username, location):
    """
    user dynamoDB to verify user transaction simply based on location
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(DYNAMO_DB_NAME)
    response = table.get_item(
        Key={'username': username},
        ConsistentRead=True
    )
    if 'Item' not in response:
        print("no user record shown")
        return False
    db_location = response['Item']['location']
    if location != db_location:
        print("user location does not match db location!")
        return False
    print("user verified")
    return True

def publish_kafka_topics(producer, topic_name, data):
    print('publish to {} topic'.format(topic_name))
    producer.send(topic=topic_name, value=str.encode(data))
    producer.flush()
    print("finished publishing to {} topic".format(topic_name))
    
def lambda_handler(event, context):
    print(json.dumps(event))
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    msgs = event['records'].values()
    for lst in msgs:
        for record in lst:
            print(record['value'], base64.b64decode(record['value']))
            information = json.loads(base64.standard_b64decode(record['value']).decode('utf-8'))
            username = information['username']
            location = information['location']
            timestamp = information['timestamp']
            print("generated at timestamp", timestamp)
            print(username, location)
            if verify_user(username, location):
                information["status"] = "approved"
                print("data is approved", information)
            else:
                information["status"] = "rejected"
                print("data is rejected", information)
            publish_kafka_topics(producer, "Status", json.dumps(information))
            # producer.flush()
            # producer.close()
    # producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    # print('publish approved transactions...')
    # for _ in range(10):
    #     time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    #     producer.send(topic="Approved", value=str.encode(time))
    # producer.flush()
    # print('finished')
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }