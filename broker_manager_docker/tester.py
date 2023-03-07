import requests 

#File to manually test all the endpoints
import requests
serverLink = "http://127.0.0.1:5000"
    
def createTopic(topic):
    newServerLink = serverLink + "/topics"
    _params = {"topic_name" : topic}
    # print(_params)
    output = requests.post(newServerLink, json = _params)
    return output

def listTopics():
    newServerLink = serverLink + "/topics"
    output = requests.get(newServerLink)
    # print(output.json())
    return output.json()

def registerConsumer(topic):
    newServerLink = serverLink + "/consumer/register"
    _params = {"topic_name" : topic}
    output = requests.post(newServerLink, json = _params)
    # print(output.json())
    return output.json()

def registerProducer(topic):
    newServerLink = serverLink + "/producer/register"
    _params = {"topic_name" : topic}
    output = requests.post(newServerLink, json = _params)
    # print(output.json())
    return output.json()

def enqueue(topic, producer_id, message, partition_no=None):
    newServerLink = serverLink + "/producer/produce"
    _params = {"topic_name" : topic, "producer_id": producer_id, "message": message, "partition_no": partition_no}
    output = requests.post(newServerLink, json = _params)
    # print(output.json())
    return output.json()


def dequeue(topic, consumer_id):
    newServerLink = serverLink + "/consumer/consume"
    _params = {"topic_name" : topic, "consumer_id": consumer_id}
    output = requests.get(newServerLink, json = _params)
    # print(output.json())
    return output.json()

def size(topic, consumer_id):
    newServerLink = serverLink + "/size"
    _params = {"topic_name" : topic, "consumer_id": consumer_id}
    output = requests.get(newServerLink, json = _params)
    return output.json()

def getPartitions(topic):
    newServerLink = serverLink + "/topic/count"
    _params = {"topic_name": topic}
    output = requests.get(newServerLink, json = _params)
    return output.json()

def partition(topic, producer_id):
    newServerLink = serverLink + "/topic/partition"
    _params = {"topic_name": topic, "producer_id": producer_id}
    output = requests.post(newServerLink, json = _params)
    return output.json()