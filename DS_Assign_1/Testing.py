from myQueueClass import *
from fileinput import filename
import threading
import time
from random import randint

q = myQueue("http://127.0.0.1:8000")

q.createTopic("T-1")
# print(q.registerProducer("T-1")["producer_id"])
# x = q.registerConsumer("T-1")["consumer_id"]
# print(q.dequeue("T-1", x)["message"])
q.createTopic("T-2")
q.createTopic("T-3")

producers = {}
producers["P1"] = {}
producers["P2"] = {}
producers["P3"] = {}
producers["P4"] = {}
producers["P5"] = {}

producers["P1"]["T-1"] = q.registerProducer("T-1")["producer_id"]
producers["P1"]["T-2"] = q.registerProducer("T-2")["producer_id"]
producers["P1"]["T-3"] = q.registerProducer("T-3")["producer_id"]

producers["P2"]["T-1"] = q.registerProducer("T-1")["producer_id"]
producers["P2"]["T-3"] = q.registerProducer("T-3")["producer_id"]

producers["P3"]["T-1"] = q.registerProducer("T-1")["producer_id"]

producers["P4"]["T-2"] = q.registerProducer("T-2")["producer_id"]

producers["P5"]["T-2"] = q.registerProducer("T-2")["producer_id"]


consumers = {}
consumers["C1"] = {}
consumers["C2"] = {}
consumers["C3"] = {}

consumers["C1"]["T-1"] = q.registerConsumer("T-1")["consumer_id"]
consumers["C1"]["T-2"] = q.registerConsumer("T-2")["consumer_id"]
consumers["C1"]["T-3"] = q.registerConsumer("T-3")["consumer_id"]

consumers["C2"]["T-1"] = q.registerConsumer("T-1")["consumer_id"]
consumers["C2"]["T-3"] = q.registerConsumer("T-3")["consumer_id"]

consumers["C3"]["T-1"] = q.registerConsumer("T-1")["consumer_id"]

consumers["C3"]["T-3"] = q.registerConsumer("T-3")["consumer_id"]



def consumer_func(q, consumer_id, topics : list, id_dict : dict):
    file_name = "../test_asgn1/consumer_" + str(consumer_id) + ".txt"
    log_file = open(file_name,"w")
    
    while True:
        for topic in topics:
            time.sleep(1)
            log = q.dequeue(topic, id_dict[topic])["message"]
            if log is not None:
                log_file.write(log)

def producer_func(q, producer_id, id_dict : dict):
    file_name = "../test_asgn1/producer_" + str(producer_id) + ".txt"
    log_file = open(file_name, "r")

    for log in log_file:
        sleep_time = randint(20,60) / 60
        time.sleep(sleep_time*2)
        topic = log.split()[3]
        q.enqueue(topic, id_dict[topic], log)



t1 = threading.Thread(target=producer_func, args=(q, 1,producers["P1"]))
t2 = threading.Thread(target=producer_func, args=(q, 2,producers["P2"]))
t3 = threading.Thread(target=producer_func, args=(q, 3,producers["P3"]))
t4 = threading.Thread(target=producer_func, args=(q, 4,producers["P4"]))
t5 = threading.Thread(target=producer_func, args=(q, 5,producers["P5"]))


t6 = threading.Thread(target=consumer_func, args=(q, 1,['T-1', 'T-2', 'T-3'], consumers["C1"]))
t7 = threading.Thread(target=consumer_func, args=(q, 2,['T-1', 'T-3'], consumers["C2"]))
t8 = threading.Thread(target=consumer_func, args=(q, 3,['T-1', 'T-3'], consumers["C3"]))

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()
t6.start()
t7.start()
t8.start()


t1.join()
t2.join()
t3.join()
t4.join()
t5.join()
t6.join()
t7.join()
t8.join()
<<<<<<< HEAD

# q.registerConsumer("T-1")
# q.registerProducer("T-2")
# q.registerProducer("T-3")
# q.enqueue("Message 1", 5, "Enjoy2!")
# q.enqueue("Message 1", 5, "Enjoy3!")
# # q.dequeue("Message 1", 9)

# q.size("Message 1", 9)

# t1 = threading.Thread(target=producer_func, args=(1,['T-1', 'T-2', 'T-3']))
# t2 = threading.Thread(target=producer_func, args=(2,['T-1', 'T-3']))
# t3 = threading.Thread(target=producer_func, args=(3,['T-1']))
# t4 = threading.Thread(target=producer_func, args=(4,['T-2']))
# t5 = threading.Thread(target=producer_func, args=(5,['T-1', 'T-2', 'T-3']))


# t6 = threading.Thread(target=consumer_func, args=(1,['T-1', 'T-2', 'T-3']))
# t7 = threading.Thread(target=consumer_func, args=(2,['T-1', 'T-3']))
# t8 = threading.Thread(target=consumer_func, args=(3,['T-1', 'T-2', 'T-3']))
=======
>>>>>>> b383b5baf820a158602257d487fd4cbb685964c7
