import datetime

import boto3
from flask import request, current_app
from flask_restful import Resource

from db import Ticket


class Entry(Resource):
    def post(self):

        plate = request.args.get("plate")
        parking_lot = request.args.get("parkingLot")

        ticket = Ticket(
            plate=plate,
            parking_lot=parking_lot,
            entry_time=datetime.datetime.now(),
        )

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(current_app.config["MAIN_TABLE_NAME"])
        table.put_item(Item=ticket.serialize())

        return {"ticketId": ticket.ticket_id.hex}, 200, ({"Content-Type": "application/json"})
