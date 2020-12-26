# Kafka

## Create a topic 
Discribe stack
```sh
aws kafka describe-cluster --region us-east-1 --cluster-arn "ClusterArn"
```
In my case:
```sh
aws kafka describe-cluster --region us-east-1 --cluster-arn arn:aws:kafka:us-east-1:358643568593:cluster/6998-indepth-msk/f6f16a5b-9234-4ff3-b3fa-780d03219791-9
```
In the describe json, there is `"ZookeeperConnectString"`, which will be useful in the next step

```sh
bin/kafka-topics.sh --create --zookeeper ZookeeperConnectString --replication-factor 3 --partitions 1 --topic AWSKafkaTutorialTopic
```

In my case, create a topic called `Approved`

```sh
bin/kafka-topics.sh --create --zookeeper z-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-3.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181 --replication-factor 2 --partitions 2 --topic Approved
```
Other useful commands

- Create a new topic called “heartbeat” on Kafka;
- List the topics available on our Kafka instance;
- Reduce the topic message retention time to 1 Hour.

```
./bin/kafka-topics.sh --zookeeper ec2-XX-XXX-XXX-XX.sa-east-1.compute.amazonaws.com:2181 --create --topic heartbeat --partitions 2 --replication-factor 1

./bin/kafka-topics.sh --zookeeper ec2-XX-XXX-XXX-XX.sa-east-1.compute.amazonaws.com:2181 --list

./bin/kafka-topics.sh --zookeeper ec2-XX-XXX-XXX-XX.sa-east-1.compute.amazonaws.com:2181 --alter --topic heartbeat --config retention.ms=3600000
```

for example

```
./bin/kafka-topics.sh --zookeeper z-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181,z-3.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:2181 --list
```
## Product and consume data
https://docs.aws.amazon.com/msk/latest/developerguide/produce-consume.html

In this example we use the JVM truststore to talk to the MSK cluster. To do this, first create a folder named /tmp on the client machine. Then, go to the bin folder of the Apache Kafka installation and run the following command, replacing JDKFolder with the name of your JDK folder. For example, the name of the JDK folder on your instance might be java-1.8.0-openjdk-1.8.0.201.b09-0.amzn2.x86_64.

```sh
cp /usr/lib/jvm/JDKFolder/jre/lib/security/cacerts /tmp/kafka.client.truststore.jks
```

in my case
```
sudo cp /usr/lib/jvm/jre/lib/security/cacerts /tmp/kafka.client.truststore.jks
```

While still in the bin folder of the Apache Kafka installation on the client machine, create a text file named client.properties with the following contents.

```
security.protocol=SSL
ssl.truststore.location=/tmp/kafka.client.truststore.jks
```

get the bootstrap server:
```sh
aws kafka get-bootstrap-brokers --region us-east-1 --cluster-arn ClusterArn
```

In my case:
```sh
aws kafka get-bootstrap-brokers --region us-east-1 --cluster-arn arn:aws:kafka:us-east-1:358643568593:cluster/6998-indepth-msk/f6f16a5b-9234-4ff3-b3fa-780d03219791-9
```

will get `BootstrapBrokerStringTls`

use console consumer
```sh
./kafka-console-consumer.sh --bootstrap-server BootstrapBrokerStringTls --consumer.config client.properties --topic AWSKafkaTutorialTopic --from-beginning
```

In my case:
```sh
./kafka-console-consumer.sh --bootstrap-server b-1.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9094,b-2.6998-indepth-msk.z5b8ke.c9.kafka.us-east-1.amazonaws.com:9094 --consumer.config client.properties --topic Approved --from-beginning
```
## Stop kafka

need to stop both
```
./bin/kafka-server-stop.sh
./bin/zookeeper-server-stop.sh
```
## Reference
https://docs.aws.amazon.com/msk/latest/developerguide/create-topic.html

# Set up Pyspark on Mac

## Check Dependencies: JDK, Scala, Git

```sh
java -version; javac -version; scala -version; git --version;
```

I don't have a scala, so Install scala: Using homebrew

```sh
brew install scala
```
## download spark
http://spark.apache.org/downloads.html

```sh
wget https://apache.claz.org/spark/spark-3.0.1/spark-3.0.1-bin-hadoop2.7.tgz
```

unzip:
```sh
tar -xzf spark-3.0.1-bin-hadoop2.7.tgz
```

move the file to the /opt folder

```sh
sudo mv spark-3.0.1-bin-hadoop2.7 /opt/spark-3.0.1
```
And create a symbolic link
```sh
sudo ln -s /opt/spark-3.0.1 /opt/spark
```

> What’s happening here? By creating a symbolic link to our specific version (3.0.1) we can have multiple versions installed in parallel and only need to adjust the symlink to work with them.

for example

```sh
ln -s my_file.txt my_link.txt
ls -l my_link.txt
```
the ouput will be 
```
lrwxrwxrwx 1 linuxize users  4 Nov  2 23:03  my_link.txt -> my_file.txt
```

## Change the .zshrc or .bashrc to tell the terminal to find spark

```
export SPARK_HOME="/opt/spark"
export PATH=$SPARK_HOME/bin:$PATH
export SPARK_LOCAL_IP='127.0.0.1'
```

Hyun uses:
```
export PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
```

Now tell Pyspark to use Jupyter: in your ~/.bashrc/~/.zshrc file, add

```
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'
```

If you want to use Python 3 with Pyspark (see step 3 above), you also need to add:

```
export PYSPARK_PYTHON=python3
```

```
source ~/.zshrc
```

## Use a jupyer notebook to start pypark
Make yourself a new folder somewhere, like ~/coding/pyspark-project and move into it
```
cd ~/coding/pyspark-project
```
Create a new environment
```
pipenv install pyspark
```
Install Jupyter
```
pipenv install jupyter
```

To start Pyspark and open up Jupyter, you can simply run $ pyspark. You only need to make sure you’re inside your pipenv environment. That means:

```
Go to your pyspark folder ($ cd ~/coding/pyspark project)
Type $ pipenv shell
Type $ pyspark
```

## Test

Start standalone master server
```
start-master.sh
```

Go to local host to have a look
```
http://127.0.0.1:8080/
```

Run the slave server
```
start-slave.sh spark://master:port
```

For example, the master server is in 7077, so run slave server

```
start-slave.sh spark://127.0.0.1:7077
```

go to 8081 to have a look
```
http://127.0.0.1:8081/
```

Then, run pyspark. This will open a jupyter notebook
```
pyspark
```

Run sample code
```
bigData = range(1000)
rdd = sc.parallelize(bigData, 2)
odds = rdd.filter(lambda x: x % 2 != 0)
odds.take(5)
```

stop master
```
stop-master.sh
```
## Reference
https://www.lukaskawerau.com/local-pyspark-jupyter-mac/

# Using EMR

# Spark Streamming
Spark Streaming is an extension of the core Spark API that enables scalable, high-throughput, fault-tolerant stream processing of live data streams. Data can be ingested from many sources like Kafka, Kinesis, or TCP sockets, and can be processed using complex algorithms expressed with high-level functions like map, reduce, join and window. Finally, processed data can be pushed out to filesystems, databases, and live dashboards.

![spark-kafka](images/spark=kafka.png)

## Reference 
https://spark.apache.org/docs/latest/streaming-programming-guide.html

https://www.rittmanmead.com/blog/2017/01/getting-started-with-spark-streaming-with-python-and-kafka/

https://medium.com/@wfaria_1/kafka-apache-spark-streaming-example-on-aws-free-tier-fcf3c93e15ca
