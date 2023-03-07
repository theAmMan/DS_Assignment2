from assign2 import db
from sqlalchemy.sql import func
import datetime
from sqlalchemy import Column, Integer, DateTime

class Broker(db.Model):
    #Model to store Broker details on broker manager
    # id = db.Column(db.Integer, primary_key = True, index = True)
    port = db.Column(db.Integer, primary_key = True) #The port on which the broker is currently operating on
    database_name = db.Column(db.String(64))
    heartbeat = db.Column(db.DateTime(timezone=True), server_default=db.func.now())