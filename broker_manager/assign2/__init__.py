from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

import config 

app = Flask(__name__)
app.config.from_object(config.production_config)
db = SQLAlchemy(app)
from .models import *

from assign2.redirector import *

redirector = Redirector()

from assign2 import views

# import the threading module
import threading
import time

def healthCheck():
		# print(str(self.thread_name) +" "+ str(self.thread_ID));
        while True:
            # print("Hi")
            try:
                with app.app_context():
                    redirector.healthCheck()
            except Exception as e :
                print(e)
            time.sleep(15)

with app.app_context():
    if app.config["TESTING"]:
        print("Dropping all tables...")
        db.drop_all()
        print("Finished dropping tables")

    print("Creating tables...")
    db.create_all()
    print("Table creation done")

    #Initialize the in-memory data structures 
    print("Initializing the in-memory datastructures from the database...")
    redirector.sync_with_db()
    print("Initialization done")

    if app.config["FLASK_ENV"] == "development":
        print("Development environment turned on")
        
    # thread1 = thread("HealthCheck", 1000)
    thread1 = threading.Thread(target=healthCheck, daemon=True)
    thread1.start()

    # thread1.join()
    
    # print("Exit")
