import json
import base64
from constants import *
import datetime
import boto3
from kafka import KafkaConsumer


def append_transaction_details(data):
    """
    append transaction details to dynamoDB
    """
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(DYNAMO_DB_NAME)
    print("data to append", data)
    result = table.update_item(
        Key={'username': str(data['username'])},
        UpdateExpression="SET statements = list_append(if_not_exists("
                         "statements, :empty_list), :i)",
        ExpressionAttributeValues={
            ":i": [data],
            ":empty_list": {"statements": []},
        },
        ReturnValues="UPDATED_NEW"
    )


def lambda_handler(event, context):
    print(json.dumps(event))
    msgs = event['records'].values()
    for lst in msgs:
        for record in lst:
            print(record['value'], base64.b64decode(record['value']))
            information = json.loads(
                base64.standard_b64decode(record['value']).decode('utf-8'))
            append_transaction_details(information)
            print("finished")
    # producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    # print('publish approved transactions...')
    # for _ in range(10):
    #     time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    #     producer.send(topic="Approved", value=str.encode(time))
    # producer.flush()
    # print('finished')
    return {
        'statusCode': 200,
        'body': json.dumps('OK!')
    }


def main():
    consumer = KafkaConsumer(
        APPROVED_TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id='status',
        auto_offset_reset='latest'
    )
    print('test consumer running')
    limit = 500  # consume at most 50 messages
    for idx, res in enumerate(consumer):
        if idx >= limit:
            break
        information = json.loads(res.value)
        print(information)
        append_transaction_details(information)
        consumer.commit()
    consumer.commit()


if __name__ == '__main__':
    main()