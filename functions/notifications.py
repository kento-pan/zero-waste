#  Send notification mail for products with expired flag

import os
import smtplib
import ssl

import config_mail
import expired

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


functions_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(functions_dir, os.pardir))
database_file = f"sqlite:///{(os.path.join(parent_dir, 'mydatabse.db'))}"

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
        return f"ID: {self.id} Item: {self.title} Expiry Date: {self.date} Expired Flag: {self.expired}"


expired.expired()
expired_products = []


def notification(expired_products):
    all_items = Item.query.all()
    for items in all_items:
        if items.expired == 1:
            expired_products.append(items.title)
    return expired_products


notification(expired_products)

expired_products_string = " ".join(expired_products)

recipe_link_single = ""
recipe_link_multi = ""


def recipe_single(expired_products, recipe_link_single):
    for i in expired_products:
        recipe_link_single += f"<a href='https://www.google.com/search?q=Recipes+with+{i}'>Recipes with {i}</a><br>" + '\n'
    return recipe_link_single


recipe_link_single = recipe_single(expired_products, recipe_link_single)


def recipe_multi(expired_products, recipe_link_multi):
    if len(expired_products) > 1:
        recipe_link_multi = "<a href=https://www.google.com/search?q=Recipes+with+" + "+".join(expired_products) + ">Recipes including all of these</a><br>"

    return recipe_link_multi


recipe_link_multi = recipe_multi(expired_products, recipe_link_multi)


def mail(expired_products):
    send_to_multi = ", ".join(config_mail.send_to)
    message = MIMEMultipart("alternative")
    message["Subject"] = "Oh snap - Some of your food is expiring!"
    message["From"] = config_mail.send_from
    message["To"] = send_to_multi

    # Create the plain-text and HTML version of mail
    text = f"""\
    This is just a friendly reminder.
    The following items are about to expire:
    {expired_products}
    You better start thinking about some recipes!"""

    if len(expired_products) > 1:
        html = f"""\
        <html>
            <body>
                <p>Hi,<br>
                    <br>
                    This is just a friendly reminder.<br>
                    <br>
                    The following items are about to expire:<br>
                    {expired_products_string}
                    <br>
                    <br>
                    Need some inspiration for a recipe? Check this out:<br><br>""" + recipe_link_single + recipe_link_multi + """\
                    <br>
                    Bon Appétit!
                </p>
            </body>
        </html>
        """
    else:
        html = f"""\
        <html>
            <body>
                <p>Hi,<br>
                    <br>
                    This is just a friendly reminder.<br>
                    <br>
                    The following item is about to expire:<br>
                    {expired_products_string}
                    <br>
                    <br>
                    Need some inspiration for a recipe? Check this out:<br><br>""" + recipe_link_single + """\
                    <br>
                    Bon Appétit!
                </p>
            </body>
        </html>
        """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
	
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
   
    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(config_mail.host, config_mail.port, context=context) as server:
        server.login(config_mail.send_from, config_mail.password)
        server.sendmail(
            config_mail.send_from, config_mail.send_to, message.as_string()
        )


mail(expired_products)
