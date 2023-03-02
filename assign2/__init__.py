from flask import Flask 
from flask_sqlalchemy import SQLAlchemy 

import config 

from assign2 import redirector

app = Flask(__name__)
app.config.from_object(config.production_config)
db = SQLAlchemy(app)
from models import *

with app.app_context():
    if app.config["TESTING"]:
        print("Dropping all tables...")
        db.drop_all()
        print("Finished dropping tables")

    print("Creating tables...")
    db.create_all()
    print("Table creation done")

    if app.config["FLASK_ENV"] == "development":
        print("Development environment turned on")
        