"""
generate data to dynamoDB
"""
import boto3
from constants import DYNAMO_DB_NAME


def storeInDynamoDB(user_location, dynamodb=None):
    if dynamodb is None:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table(DYNAMO_DB_NAME)
    scan = table.scan()
    # remove first
    with table.batch_writer() as batch:
        for each in scan['Items']:
            batch.delete_item(
                Key={
                    'username': each['username']
                }
            )
    print("successfully delete all items")

    print("Uploading new data to dynamoDB...")
    print(user_location)

    with table.batch_writer() as batch:
        # speed up
        # also need to upgrade the timeout in lambda
        for record in user_location:
            item = {
                "username": record[0],
                "location": record[1],
                "statements": []
            }
            # item["username"] = record[0]  # Primary key
            # item["location"] = record[1]  # sort key
            # item["statements"] = []
            batch.put_item(Item=item)
    print("data uploaded!")


def main():
    user_location_list = [("Linxiao", "New York"), ("Zixuan", "New York"), ("Michael", "California"), ("Xin", "Michigan")]
    for i in range(100):
        user_name = "Zzz-" + str(i)
        user_location_list.append((user_name, "New York"))
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    storeInDynamoDB(user_location_list, dynamodb)


if __name__ == '__main__':
    main()