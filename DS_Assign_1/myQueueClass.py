import requests
class myQueue:
    serverLink = ""
    def __init__(self, _serverlink):
        self.serverLink = _serverlink
    
    def createTopic(self, topic):
        newServerLink = self.serverLink + "/topics"
        _params = {"topic_name" : topic}
        output = requests.post(newServerLink, data = _params)
        # print(output.json())
        return output
    
    def listTopics(self):
        newServerLink = self.serverLink + "/topics"
        output = requests.get(newServerLink)
        # print(output.json())
        return output.json()

    def registerConsumer(self, topic):
        newServerLink = self.serverLink + "/consumer/register"
        _params = {"topic_name" : topic}
        output = requests.post(newServerLink, data = _params)
        # print(output.json())
        return output.json()

    def registerProducer(self, topic):
        newServerLink = self.serverLink + "/producer/register"
        _params = {"topic_name" : topic}
        output = requests.post(newServerLink, data = _params)
        # print(output.json())
        return output.json()

    def enqueue(self, topic, producer_id, message):
        newServerLink = self.serverLink + "/producer/produce"
        _params = {"topic_name" : topic, "producer_id": producer_id, "message": message}
        output = requests.post(newServerLink, data = _params)
        # print(output.json())
        return output.json()


    def dequeue(self, topic, consumer_id):
        newServerLink = self.serverLink + "/consumer/consume"
        _params = {"topic_name" : topic, "consumer_id": consumer_id}
        output = requests.get(newServerLink, params = _params)
        # print(output.json())
        return output.json()


    def size(self, topic, consumer_id):
        newServerLink = self.serverLink + "/size"
        _params = {"topic_name" : topic, "consumer_id": consumer_id}
        output = requests.get(newServerLink, params = _params)
        # print(output.json())
        return output.json()