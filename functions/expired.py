#  Set expired flag one day before item date is reached

import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import *
from dateutil.relativedelta import *


functions_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(functions_dir, os.pardir))
database_file = f"sqlite:///{(os.path.join(parent_dir, 'foodyea.db'))}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    date = db.Column(db.DateTime)
    expired = db.Column(db.Integer)

    def __repr__(self):
        return f"Item: {self.title} Expiry Date: {self.date} Expired Flag: {self.expired}"


def expired():
    #today = datetime.today()
    yesterday = datetime.today() + relativedelta(days=-1)
    all_items = Item.query.all()
    for items in all_items:
        if items.date <= yesterday:
            if items.expired == 0:
                items.expired=1
                db.session.commit()
        
# expired()
