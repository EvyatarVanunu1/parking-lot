import boto3
from flask import Flask
from db import create_main_table


def create_app():

    app = Flask(__name__)
    app.config["MAIN_TABLE_NAME"] = "Tickets"

    dynamodb = boto3.resource("dynamodb")
    with app.app_context():
        create_main_table(dynamodb)

    return app
