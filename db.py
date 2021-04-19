import datetime
import typing
import uuid

from flask import current_app

if typing.TYPE_CHECKING:
    from boto3.dynamodb import ServiceResource


def create_main_table(dynamodb: "ServiceResource"):
    try:
        dynamodb.create_table(
            TableName=current_app.config['MAIN_TABLE_NAME'],
            KeySchema=[
                {
                    'AttributeName': 'ticket_id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'ticket_id',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1,
            },
        )
    except dynamodb.exception.ResourceInUseException:
        pass


class Ticket():

    def __init__(self):
        self.ticket_id = uuid.uuid4()
        self.parking_lot = None
        self.plate = None
        self.entry_time = None
        self.exit_time = None

    @classmethod
    def deserialize(cls, data):
        properties = [data.get('ticket_id'), data.get('parking_lot'), data.get('plate'),
                      data.get('entry_time'), data.get('exit_time')]
        if cls.validate_str(properties):
            ticket = Ticket()
            ticket.ticket_id = data['ticket_id']
            ticket.parking_lot = data['parking_lot']
            ticket.plate = data['plate']
            ticket.entry_time = datetime.datetime.fromisoformat(data['entry_time'])
            ticket.exit_time = datetime.datetime.fromisoformat(data['exit_time'])
        else:
            return {"error": "invalid fields"}
        return ticket

    @classmethod
    def validate_str(cls, strings):
        for s in strings:
            if isinstance(s, str):
                return True
        return False

    def serialize(self):
        return {'ticket_id': self.ticket_id,
                'parking_lot': self.parking_lot,
                'plate': self.plate,
                'entry_time': self.entry_time.isoformat(),
                'exit_time': self.exit_time.isoformat()}

    def get_price(self):
        time = self.exit_time - self.entry_time
        time = time.seconds / 60
        time = time // 15
        return time * 2.5

