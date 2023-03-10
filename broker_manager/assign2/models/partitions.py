from assign2 import db 

class Partition(db.Model):
    #Model for each partition
    topic_name = db.Column(
        db.String(256), db.ForeignKey("topic.name"), nullable = False
    )
    partition_number = db.Column(db.Integer) #Partition ID 
    broker = db.Column(
        db.Integer, db.ForeignKey("broker.port"), nullable = False
    ) #which broker is currently servicing this partition
    id = db.Column(db.Integer, primary_key = True)