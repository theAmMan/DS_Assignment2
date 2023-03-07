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

with app.app_context():
    if app.config["TESTING"]:
        print("Dropping all tables...")
        # db.drop_all()
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
        