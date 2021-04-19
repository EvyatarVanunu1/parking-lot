import typing

from flask import current_app

if typing.TYPE_CHECKING:
    from boto3.dynamodb import ServiceResource


def create_main_table(dynamodb: "ServiceResource"):
    try:
        dynamodb.create_table(
            TableName=current_app.config['MAIN_TABLE_NAME'],
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
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




