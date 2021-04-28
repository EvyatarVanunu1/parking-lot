from flask_restful import Api

from .entry import Entry
from .exit import Exit


def register_routes(api: Api):
    api.add_resource(Exit, "/exit")
    api.add_resource(Entry, "/entry")
