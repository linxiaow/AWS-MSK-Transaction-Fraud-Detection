CLUSTER_ARN = 'arn:aws:kafka:us-east-1:358643568593:cluster/6998-indepth-msk/f6f16a5b-9234-4ff3-b3fa-780d03219791-9'
BOOTSTRAP_SERVERS = ['b-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9092','b-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9092']
INITIAL_TOPIC_NAME = 'Transactions'
STATUS_TOPIC_NAME = "Status"
APPROVED_TOPIC_NAME = "Approved"
# REPLICATION_FACTOR = 2
# PARTITION = 2
ZOOKEEPER = "z-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-3.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181"

BootstrapBrokerStringTls = 'b-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9094,b-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9094'

DYNAMO_DB_NAME = "6998-Indepth-User-Information"

"""


aws kafka get-bootstrap-brokers --region us-east-1 --cluster-arn arn:aws:kafka:us-east-1:358643568593:cluster/6998-indepth-msk/f6f16a5b-9234-4ff3-b3fa-780d03219791-9

./kafka-topics.sh --create --zookeeper z-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-3.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181 --replication-factor 2 --partitions 2 --topic topic1

./kafka-console-consumer.sh --bootstrap-server b-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9094 --consumer.config client.properties --topic topic1 
"""
