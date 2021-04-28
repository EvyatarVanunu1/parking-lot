import boto3
from flask import Flask
from flask_restful import Api
from db import create_main_table

from resources.routes import register_routes


def create_app():

    app = Flask(__name__)
    api = Api()
    register_routes(api)
    api.init_app(app)

    app.config["MAIN_TABLE_NAME"] = "Tickets"

    dynamodb = boto3.client("dynamodb")
    with app.app_context():
        create_main_table(dynamodb)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")

