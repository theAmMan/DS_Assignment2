import requests 

#File to manually test all the endpoints
import requests
serverLink = "http://127.0.0.1:8000"
    
def createTopic(topic, id):
    newServerLink = serverLink + "/topics"
    _params = {"topic_name" : topic, "partition_no": id}
    # print(_params)
    output = requests.post(newServerLink, data = _params, json = _params)
    return output

def listTopics():
    newServerLink = serverLink + "/topics"
    output = requests.get(newServerLink)
    # print(output.json())
    return output.json()

def registerConsumer(topic):
    newServerLink = serverLink + "/consumer/register"
    _params = {"topic_name" : topic}
    output = requests.post(newServerLink, json = _params, data = _params)
    # print(output.json())
    return output.json()

def registerProducer(topic):
    newServerLink = serverLink + "/producer/register"
    _params = {"topic_name" : topic}
    output = requests.post(newServerLink, json = _params, data = _params)
    # print(output.json())
    return output.json()

def enqueue(topic, producer_id, message, partition_no):
    newServerLink = serverLink + "/producer/produce"
    _params = {"topic_name" : topic, "producer_id": producer_id, "message": message, "partition_no": partition_no}
    output = requests.post(newServerLink, json = _params, data = _params)
    # print(output.json())
    return output.json()

def dequeue(topic, consumer_id, id):
    newServerLink = serverLink + "/consumer/consume"
    _params = {"topic_name" : topic, "consumer_id": consumer_id, "partition_no": id}
    output = requests.get(newServerLink, json = _params, params = _params)
    # print(output.json())
    return output.json()

def size(topic, consumer_id, id):
    newServerLink = serverLink + "/size"
    _params = {"topic_name" : topic, "consumer_id": consumer_id, "partition_no": id}
    output = requests.get(newServerLink, json = _params, params = _params)
    return output.json()

def topic_size(topic, consumer_id):
    #Total size of messages in a specific topic
    newServerLink = serverLink + "/size"
    _params = {"topic_name": topic, "consumer_id": consumer_id}
    output = requests.get(newServerLink, json = _params, params = _params)
    return output.json()

def partition(topic, producer_id):
    newServerLink = serverLink + "/partition"
    _params = {"topic_name": topic, "producer_id": producer_id}
    output = requests.post(newServerLink, json = _params, data = _params)
    return output.json()

def probe(topic, consumer_id, id):
    #Test probe endpoint
    newServerLink = serverLink + "/consumer/probe"
    _params = {"topic_name" : topic, "consumer_id": consumer_id, "partition_no": id}
    output = requests.get(newServerLink, json = _params, params = _params)
    # print(output.json())
    return output.json()