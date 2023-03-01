import threading
from assign2 import db, Topic_Model, Consumer_Model, Producer_Model, Partition_Model
import uuid, requests
from topic import Topic 
from typing import Dict
from utility_funcs import *

class Redirector():
    #A class that redirects all the messages to the appropriate brokers

    def __init__(self) -> None:
        #We need to handle a single lock
        self._lock = threading.Lock()
        self._metadata: Dict[str, Topic] = {}
        self._ids = [] 


    def sync_with_db(self) -> None: 
        #Sync the in-memory metadata with the database
        self._ids.append(len(Producer_Model.query.all()))
        self._ids.append(len(Consumer_Model.query.all()))

        for topic in Topic_Model.query.all():
            self._metadata[topic.name] = Topic(topic.name)

        for producer in Producer_Model.query.all():
            self._metadata[producer.topic_name].add_producer(producer.id)

        for consumer in Consumer_Model.query.all():
            self._metadata[consumer.topic_name].add_consumer(consumer.id)

        for partition in Partition_Model.query.all():
            self._metadata[partition.topic_name].add_partition(partition.id)


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


    def get_size(self, topic_name: str, consumer_id: str, partition_no = None) -> int:
        #Get the number of remaining messages in the specific partition for the consumer
        if partition_no == None: 
            #Get the remaining number of messages from each partition of the topic
            partition = Partition_Model.query.filter


    def create_partition(self, topic_name: str) -> None:
        #Create a partition in the specific topic 
        if topic_name not in Topic_Model.query.all():
            raise Exception("Topic does not exist")

        
        #Now allocate a broker to the partition 


    def add_consumer(self, topic_name: str) -> int:
        #Add a consumer to a specific topic 
        if not _exists(topic_name):
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
            requests.post(newServerLink, data = _params)

        return consumer_id


    def add_producer(self, topic_name: str) -> int:
        #Add a producer to a specific topic 
        if not _exists(topic_name):
            raise Exception("Topic does not exist")

        with self._lock:
            producer_id = self._ids[0] + 1
            self._ids[0] += 1
            self._metadata[topic_name].add_producer(producer_id)


        db.session.add(Producer_Model(id = producer_id,topic_name = topic_name))
        db.session.commit()

        return producer_id

    
    def add_log(self, topic_name: str, producer_id: int, message: str, partition_no: int = -1):
        #add a log to the specific partition 
        