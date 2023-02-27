
# user-defined class to implement queue for the distributed task
class distQueue:
 
  # Initialisation
  def __init__(self):
    # Store all registered producers, in a Dict
    # {'topic1':[1,2],'topic2':[1,3],'topic3':[]}
    self.reg_prod = {}
    # Store all registered consumers
    # {'topic1':[1,2,3],'topic2':[2,3],'topic3':[1]}
    self.reg_cons = {}
    # Store all topics in a list
    self.topics = []
    # Main queue containing all messages
    # {'topic':[(pid,message,viewed_by)]}
    # pid : producer_id
    # message : Log message to be added to the queue
    # viewed_by = list of all consumers who have viewed this message
    self.queue = {}
    # Consumers are numbered sequentially from 1
    self.cid = 1
    # Producers are numbered sequentially from 1
    self.pid = 1
  
  # Create Topic functionality
  def createTopic(self,name):
    ret_dict = {}
    # Check whether the topic already exists
    if name in self.topics:
      ret_dict['status'] = "failure"
      ret_dict["message"] = "Error: Topic "+name+" creation failed"
      return ret_dict
    # Check topic name validity
    if(name == ''):
      ret_dict['status'] = "failure"
      ret_dict["message"] = "Error: Topic name cannot be blank"
      return ret_dict
    # Add the topic to the list of the topics, and to the queue
    self.topics.append(name)
    self.queue[name] = []
    # Create a list for the topic for Producers and Consumers
    self.reg_prod[name]=[]
    self.reg_cons[name]=[]
    ret_dict['status'] = "sucess"
    ret_dict["message"] = "Topic "+name+" succesfully created"
    return ret_dict 
  
  # Return all topics in the queue
  def listTopics(self):
    ret_dict = {}
    # Return the list of topics
    if self.topics:
      ret_dict["topics"] = self.topics
      return ret_dict
    # If no topics are present in the queue
    ret_dict["message"] = "Error: No topics are present"
    return ret_dict
  
  # Register Consumer
  def registerConsumer(self,topic):
    ret_dict = {}
    if topic in self.topics:
      self.reg_cons[topic].append(self.cid)
      ret_dict["consumer_id"] = self.cid
      self.cid+=1
      return ret_dict
    # If the topic is not present in the queue
    ret_dict["message"] = "Error: Topic does not exist"
    return ret_dict
  
  # Register Producer
  def registerProducer(self,topic):
    ret_dict = {}
    # CHeck if topic is valid
    if topic == '':
      ret_dict["message"] = "Error: Topic name cannot be blank"
      return ret_dict
    # If the topic is not present in the queue
    if topic not in self.topics:
      # Add the topic to the list of the topics, and to the queue
      self.topics.append(topic)
      self.queue[topic] = []
      # Create a list for the topic for Producers and Consumers
      self.reg_prod[topic]=[]
      self.reg_cons[topic]=[]
    
    self.reg_prod[topic].append(self.pid)
    ret_dict["producer_id"] = self.pid
    self.pid+=1
    return ret_dict
    
  # Enqueue
  def enqueue(self,topic, pid, message):
    ret_dict = {}
    # Check if the topic is present
    if topic not in self.topics:
      ret_dict["message"] = "Error: Invalid topic"
      return ret_dict
    # Check if the producer is subscribed to this topic
    if pid not in self.reg_prod[topic]:
      # print(pid)
      # print(self.reg_prod[topic])
      ret_dict["message"] = "Error: Invalid producer"
      return ret_dict
    # Add the message to the queue
    self.queue[topic].append((pid,message,[]))
  
  # Dequeue
  def dequeue(self,topic,cid):
    ret_dict = {}
    # Check if the topic is present
    if topic not in self.topics:
      ret_dict["message"] = "Error: Invalid topic"
      return ret_dict
    # Check if the consumer is subscribed to this topic
    if cid not in self.reg_cons[topic]:
      ret_dict["message"] = "Error: Invalid consumer"
      return ret_dict
    # Return the first mesage that has not yet been sent to this consumer
    n = len(self.queue[topic])
    message = ''
    for i in range(0,n,1):
      if cid not in self.queue[topic][i][2]:
        self.queue[topic][i][2].append(cid)
        self.queue[topic][i][2].sort()
        message = self.queue[topic][i][1]
        # Design decision : We keep track of all previous messages and do not remove them from the database
        # # If the message has been seen by all consumers the message is removed from the queue
        # if(self.queue[topic][i][2]==self.reg_cons[topic]):
        #   self.queue[topic].pop(i)
        break
    # All available messages has already been sent to this consumer
    if message == '':
      ret_dict["message"] = "No log message in queue for this request"
      return ret_dict
    ret_dict["message"] = message
    return ret_dict
  
  # Get the size of the queue for this topic and consumer
  def size(self,topic,cid):
    ret_dict = {}
    # print(self.topics)
    # print(topic)
    # Check if the topic exists
    if topic not in self.topics:
      ret_dict["message"] = "Error: Invalid topic"
      return ret_dict
    # Check if this consumer is subscribed to this topic
    if cid not in self.reg_cons[topic]:
      ret_dict["message"] = "Error: Invalid consumer"
      return ret_dict
    # Count all messages in this topic not yet viewed by the consumer
    count = 0
    for i in self.queue[topic]:
      if cid not in i[2]:
        count+=1
    ret_dict["size"] = count
    return ret_dict