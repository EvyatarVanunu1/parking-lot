import datetime
import typing
import uuid

import pytz
from flask import current_app

if typing.TYPE_CHECKING:
    from boto3.dynamodb import ServiceResource


def create_main_table(dynamodb: "ServiceResource"):
    try:
        dynamodb.create_table(
            TableName=current_app.config["MAIN_TABLE_NAME"],
            KeySchema=[
                {"AttributeName": "ticket_id", "KeyType": "HASH"},
            ],
            AttributeDefinitions=[
                {"AttributeName": "ticket_id", "AttributeType": "S"},
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1,
            },
        )
    except dynamodb.exception.ResourceInUseException:
        pass


class Ticket:
    def __init__(
        self,
        parking_lot: str,
        plate: str,
        entry_time: datetime.datetime,
        exit_time: typing.Optional[datetime.datetime] = None,
        ticket_id: typing.Optional[uuid.UUID] = None,
    ):
        self.parking_lot = parking_lot
        self.plate = plate
        self.entry_time = entry_time.replace(tzinfo=pytz.UTC)
        self.exit_time = exit_time.replace(tzinfo=pytz.UTC) if exit_time else None
        self.ticket_id = uuid.uuid4() if not ticket_id else ticket_id

    @classmethod
    def deserialize(cls, data):
        properties = [
            data.get("ticket_id"),
            data.get("parking_lot"),
            data.get("plate"),
            data.get("entry_time"),
        ]

        is_valid = all(map(cls.validate_str, properties)) and cls.validate_str(data.get("exit_time"), is_optional=True)

        if is_valid:
            exit_time = data.get("exit_time")
            return Ticket(
                ticket_id=uuid.UUID(data["ticket_id"]),
                parking_lot=data["parking_lot"],
                plate=data["plate"],
                entry_time=datetime.datetime.fromisoformat(data["entry_time"]),
                exit_time=datetime.datetime.fromisoformat(exit_time) if exit_time else None,
            )
        else:
            raise ValueError("invalid fields")

    @classmethod
    def validate_str(cls, value, is_optional=False):
        return (isinstance(value, str) and value) or (value is None and is_optional)

    def serialize(self):
        return {
            "ticket_id": self.ticket_id.hex,
            "parking_lot": self.parking_lot,
            "plate": self.plate,
            "entry_time": self.entry_time.isoformat(),
            "exit_time": self.exit_time.isoformat() if self.exit_time else None,
        }

    def get_total_time(self):
        if not self.exit_time:
            raise RuntimeError("exit is not set")

        return (self.exit_time - self.entry_time).seconds // 60 + 1

    def get_price(self):
        if not self.exit_time:
            raise RuntimeError("exit is not set")

        time = self.get_total_time()
        time = time // 15
        return time * 2.5
