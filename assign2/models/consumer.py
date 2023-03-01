from assign2 import db 

class Consumer(db.Model):
    #Consumer class
    __tablename__ = "consumer"
    id = db.Column(db.Integer, primary_key = True, index = True)
    topic_name = db.Column(
        db.String(256), db.ForeignKey("topic.name"), nullable = False
    )