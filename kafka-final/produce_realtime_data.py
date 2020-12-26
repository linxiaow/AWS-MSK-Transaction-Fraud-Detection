from constants import *
import json
import datetime
import time
from kafka import KafkaProducer

SAMPLE_USERS = ["Linxiao", "Michael", "Zixuan", "Xin"]
SAMPLE_LOCATION = ["New York", "California", "Michigan"]


def generate_data_json(user, location):
    data = {}
    data["username"] = user
    data["location"] = location
    data["timestamp"] = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S.%f')[:-3]
    return data

def main():
    producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
    print('running')

    # for _ in range(10):
    #     time = datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
    #     producer.send(topic=TOPIC_NAME, value=str.encode(time))
    producer_array = []
    for user in SAMPLE_USERS:
        for loc in SAMPLE_LOCATION:
            data_dict = generate_data_json(user, loc)
            producer_array.append(data_dict)
            time.sleep(0.2)

    # produce every 5 seconds, 360 times
    messages = 360
    sleepTime = 5
    idx = 0
    request_id = 0
    while messages > 0:
        messages = messages - 1
        data_piece = producer_array[idx]

        data_piece["request_id"] = request_id
        print(data_piece)
        producer.send(
            topic=INITIAL_TOPIC_NAME, value=str.encode(json.dumps(data_piece))
        )
        time.sleep(sleepTime)
        idx += 1
        request_id += 1
        if idx == len(producer_array):
            idx = 0
    # producer.flush()
    producer.close()


if __name__ == '__main__':
    main()


