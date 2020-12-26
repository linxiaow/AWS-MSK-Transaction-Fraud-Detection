from constants import *
import json
import datetime
import time
import random
from kafka import KafkaProducer, KafkaConsumer
from constants import STATUS_TOPIC_NAME, APPROVED_TOPIC_NAME


def generate_detail_transaction(data):
    """
    assume data is already a dictionary
    """
    data["amount"] = random.randint(100, 1000)
    data["description"] = "Buy something in " + data["location"]
    data["process_time"] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    return data


def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    consumer = KafkaConsumer(
        STATUS_TOPIC_NAME,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        group_id='status',
        auto_offset_reset='latest'
    )
    print('consumer running')

    # for _ in range(10):
    #     time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    #     producer.send(topic=TOPIC_NAME, value=str.encode(time))
    limit = 500  # consume at most 50 messages
    for idx, res in enumerate(consumer):
        print(idx)
        if idx >= limit:
            break
        data = json.loads(res.value)
        print(data)
        print("This transaction has been", data["status"])
        if data["status"] == "approved":
            details = generate_detail_transaction(data)
            print("details", details)
            producer.send(topic=APPROVED_TOPIC_NAME,
                          value=str.encode(json.dumps(details)))
            print("sent to {} topic".format(APPROVED_TOPIC_NAME))
        consumer.commit()
    producer.close()
    consumer.commit()


if __name__ == '__main__':
    main()
