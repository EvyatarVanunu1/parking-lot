import boto3
from flask import request, current_app
from flask_restful import Resource


class Entry(Resource):
    def post(self):

        plate = request.args.get("plate")
        parking_lot = request.args.get("parkingLot")

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("Tickets")

        # insert item to table

        return {"ticketId": ""}, 200, ({"Content-Type": "application/json"})


class Exit(Resource):
    def post(self):
        pass