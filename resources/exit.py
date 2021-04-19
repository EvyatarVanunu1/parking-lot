import datetime

import boto3
import pytz
from flask import request, current_app
from flask_restful import Resource

from db import Ticket


class Exit(Resource):
    def post(self):

        ticket_id = request.args.get("ticketId")
        if not ticket_id:
            return {"msg": "invalid ticket id"}

        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table(current_app.config["MAIN_TABLE_NAME"])

        response = table.get_item(Key={"ticket_id": ticket_id})

        if not response.get("Item"):
            return {"msg": "ticketId not found"}

        ticket = Ticket.deserialize(data=response.get("Item"))
        ticket.exit_time = datetime.datetime.now(tz=pytz.utc)
        return (
            {
                "plate": ticket.plate,
                "parkingLot": ticket.parking_lot,
                "totalParkingTime": ticket.get_total_time(),
                "charge": ticket.get_price(),
            },
            200,
            ({"Content-Type": "application/json"}),
        )
