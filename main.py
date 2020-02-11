import os

from datetime import *

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = f"sqlite:///{(os.path.join(project_dir, 'foodyea.db'))}"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Item(db.Model):  # SQLAlchemy creates a table called Items
    # creates the columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    expired = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"Item: {self.title} Expiry Date: {self.date}"


@app.route("/", methods=["GET", "POST"])
def home():
    all_items = None
    if request.form:
        try:
            date_converted = datetime.strptime(request.form.get("date"), "%d/%m/%Y")
            item = Item(title=request.form.get("title"),
                        date=date_converted)
            if len(item.title) == 0:
                print('Please enter a title')
            elif len(request.form.get("date")) != 10:
                print("Wrong date format")
            else:
                db.session.add(item)
                db.session.commit()
        except Exception as err:
            db.session.rollback()
            print("Failed to add item.")
            print(err)


    all_items = Item.query.order_by(Item.date.asc()).all()
    return render_template("home.html", all_items=all_items)  # Updates the page and displays all items in db


@app.route("/delete", methods=["POST"])
def delete():
    id = request.form.get("id")
    item = Item.query.filter_by(id=id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect("/")  # Updates the page    

if __name__ == "__main__":
    db.create_all()
    app.run(host='localhost', port=5000,debug=True)
