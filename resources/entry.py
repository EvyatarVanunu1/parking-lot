import datetime

import boto3
from flask import request, current_app
from flask_restful import Resource

from db import Ticket


class Entry(Resource):
    def post(self):

        data = dict(
            plate=request.args.get("plate"),
            parking_lot=request.args.get("parkingLot"),
            entry_time=datetime.datetime.utcnow().isoformat(),
        )

        ticket = Ticket.deserialize(data=data)

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(current_app.config["MAIN_TABLE_NAME"])
        table.put_item(Item=ticket.serialize())

        return {"ticketId": ticket.ticket_id.hex}, 200, ({"Content-Type": "application/json"})
