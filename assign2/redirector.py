import threading
from assign2 import db, Topic_Model, Consumer_Model, Producer_Model, Partition_Model, Broker_Model
import uuid, requests
from topic import Topic 
from typing import Dict, List
from utility_funcs import *

MAX_SIZE = 10

class Redirector():
    #A class that redirects all the messages to the appropriate brokers

    def __init__(self) -> None:
        #We need to handle a single lock
        self._lock = threading.Lock()
        self._metadata: Dict[str, Topic] = {}
        self._broker: Dict[int, int] = {}
        self._ids = []
        self._sync_with_db()


    def _sync_with_db(self) -> None: 
        #Sync the in-memory metadata with the database
        self._ids.append(len(Producer_Model.query.all()))
        self._ids.append(len(Consumer_Model.query.all()))
        self._ids.append(len(Broker_Model.query.all()))

        for topic in Topic_Model.query.all():
            self._metadata[topic.name] = Topic(topic.name)

        for producer in Producer_Model.query.all():
            self._metadata[producer.topic_name].add_producer(producer.id)

        for consumer in Consumer_Model.query.all():
            self._metadata[consumer.topic_name].add_consumer(consumer.id)

        for partition in Partition_Model.query.all():
            self._metadata[partition.topic_name].add_partition(partition.id)
            if partition.broker not in self._broker.keys():
                self._broker[partition.broker] = 1
            else:  
                self._broker[partition.broker] += 1


    def _exists(self, topic_name: str, partition_no = None) -> bool:
        #Check whether the topic exists or not
        with self._lock: 
            if topic_name not in self._metadata:
                return False 
            
            elif partition_no != None and partition_no not in self._metadata[topic_name].partitions:
                return False 
            
            return True


    def add_topic(self, topic_name: str) -> None:
        #Add the topic
        with self._lock:
            if topic_name in self._metadata:
                raise Exception("Topic already exists")

            self._metadata[topic_name] = Topic(topic_name)

        db.session.add(Topic_Model(name = topic_name, partition_count = 1))
        db.commit()

        #Create a first partition for the topic 
        self.create_partition(topic_name)

    def get_topics(self) -> List[str]:
        # List all topics
        with self._lock:
            return list(self._metadata.keys())

    def get_size(self, topic_name: str, consumer_id: str, partition_no = None) -> int:
        #Get the number of remaining messages in the specific partition for the consumer
        if topic_name not in self._metadata:
            raise Exception("Topic does not exists")
        if consumer_id not in self._metadata[topic_name].consumers:
            raise Exception("Consumer not registered with this topic")
        if partition_no == None: 
            #Get the remaining number of messages from each partition of the topic
            size = 0
            for partition in Partition_Model.query.filter_by(topic_name = topic_name).all():
                newLink = get_link(partition.broker.port) + "/size"
                _params = {"topic_name" : topic_name, "consumer_id" : consumer_id}
                size = size + requests.get(newLink, data = _params)
            return size
        # Feature implemented : Support for multiple partitions in a broker for the same topic
        partition = Partition_Model.query.filter_by(topic_name = topic_name, partition_number = partition_no).first()
        newLink = get_link(partition.broker.port) + "/size"
        # _params = {"topic_name" : topic_name, "consumer_id" : consumer_id}
        _params = {"topic_name" : topic_name, "consumer_id" : consumer_id, "partition_number" : partition_no}
        return requests.get(newLink, data = _params)



    def create_partition(self, topic_name: str) -> None:
        #Create a partition in the specific topic 
        if topic_name not in Topic_Model.query.all():
            raise Exception("Topic does not exist")
        with self._lock:
            # partition_id starts at 1, and is sequential
            partition_id = len(Partition_Model.query.filter_by(topic_name = topic_name).all()) + 1
            self._metadata[topic_name].add_partition(partition_id)
            #Now allocate a broker to the partition 
            broker_number = 0
            broker_size = MAX_SIZE # This needs to be set
            for broker_id in self._broker.keys():
                if self._broker[broker_id] < broker_size:
                    broker_size = self._broker[broker_id]
                    broker_number = broker_id
            if broker_size == MAX_SIZE :
                broker_number = self.add_broker()


        db.session.add(Partition_Model(topic_name = topic_name, partition_number = partition_id, broker = broker_number))
        db.session.commit()


    def add_consumer(self, topic_name: str) -> int:
        #Add a consumer to a specific topic 
        if not self._exists(topic_name):
            raise Exception("Topic does not exist")

        with self._lock:
            consumer_id = self._ids[1] + 1
            self._ids[1] += 1
            self._metadata[topic_name].add_consumer(consumer_id)

        db.session.add(Consumer_Model(id = consumer_id, topic_name = topic_name))
        db.session.commit()

        #Now let the other brokers subscribed to this specific topic know about the new consumer
        for partition in Partition_Model.query.filter_by(topic_name = topic_name).all():
            #Inform the broker about the new consumer
            newLink = get_link(partition.broker.port) + "/consumer/register"
            _params = {"topic_name" : topic_name}
            requests.post(newLink, data = _params)

        return consumer_id


    def add_producer(self, topic_name: str) -> int:
        #Add a producer to a specific topic 
        if not self._exists(topic_name):
            raise Exception("Topic does not exist")

        with self._lock:
            producer_id = self._ids[0] + 1
            self._ids[0] += 1
            self._metadata[topic_name].add_producer(producer_id)


        db.session.add(Producer_Model(id = producer_id,topic_name = topic_name))
        db.session.commit()

        return producer_id

    
    def add_log(self, topic_name: str, producer_id: int, message: str, partition_no: int = -1) -> None:
        #add a log to the specific partition 
        if partition_no == -1:
            if not self._exists(topic_name):
                raise Exception("Topic does not exist")

            if producer_id not in self._metadata[topic_name].producers:
                raise Exception("Producer is not subscribed to the topic")
            
            partition_no = self._metadata[topic_name].current_round_robin_index
            self._metadata[topic_name].update_round_robin()

        if not self._exists(topic_name, partition_no):
            raise Exception("Topic or the Partition does not exist")

        #Now send the add request to the appropriate broker 
        partition = Partition_Model.query.filter_by(topic_name = topic_name, partition_number = partition_no).first()
        newLink = get_link(partition.broker.port) + "/producer/produce" #Link for publishing to the specific partition of a particular topic 
        # _params = {"topic_name" : topic_name} #Complete this part as well
        _params = {"topic_name" : topic_name, "partition_number" : partition_no}
        requests.post(newLink, data = _params)


    def get_log(self, topic_name: str, consumer_id: int):
        #Can return None or the message depending on if the queue is full or not
        if not self._exists(topic_name):
            raise Exception("Topic does not exist")

        if consumer_id not in self._metadata[topic_name].consumers:
            raise Exception("Consumer is not subscribed to the topic")
        
        log_msg = {}

        for partition in Partition_Model.query.filter_by(topic_name = topic_name).all():
            newLink = get_link(partition.broker.port) + "/consumer/probe"
            _params = {"topic_name" : topic_name, "consumer_id" : consumer_id}
            msg = requests.get(newLink, data = _params)
            if msg['status'] == 'success':
                log_msg[partition] = msg

        if len(log_msg) == 0:
            return None

        # FIX These Params
        partition_no = -1
        min_time = 1e9
        for partition in log_msg.keys():
            if log_msg[partition]['created'] < min_time :
                min_time = log_msg[partition]['created']
                partition_no = partition

        newLink = get_link(partition_no.broker.port) + "/consumer/consume"
        _params = {"topic_name" : topic_name, "consumer_id" : consumer_id}
        return requests.get(newLink, data = _params)['message']
        


    def add_broker(self):
        # Add new broker 
        with self._lock:
            broker_id = self._ids[2] + 1
            self._ids[2] += 1
            self._broker[broker_id] = 0

        # FIX THIS
        db.session.add(Broker_Model(id = broker_id, port = 5432+broker_id))
        db.session.commit()

        return broker_id


    def remove_broker(self):
        # Remove existing broker