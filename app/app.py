from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime

from models import EntryModel
from pytz import utc


# object to hold user's actions on the api resources

class EntryManager:
    # initialize last_id to 0

    last_id = 0

    # initialize an empty dictionary to hold user input

    def __init__(self):
        self.entries = {}

    # add user entry to list

    def insert_entry(self, entry):
        self.__class__.last_id += 1
        entry.id = self.__class__.last_id
        self.entries[self.__class__.last_id] = entry

    # user request for a single entry from entries list

    def get_entry(self, id):
        return self.entries[id]

    # user delete a single entry

    def delete_entry(self, id):
        return self.entries.pop(id)


""" template for a single entry"""
entry_fields = {
    'id': fields.Integer,
    'uri': fields.Url('entry_endpoint'),
    'title': fields.String,
    'entry': fields.String,
    'creation_date': fields.DateTime
}

"""initialized entry manager object"""
entry_manager = EntryManager()

# entry object to define entries


class Entry(Resource):

    # check entry id if already in dictionary
    def abort_if_entry_doesnt_exist(self, id):
        if id not in entry_manager.entries:
            abort(404, entry="Entry {0} doesn't exist".format(id))

    # capture user input for entry

    @marshal_with(entry_fields)
    def get(self, id):
        self.abort_if_entry_doesnt_exist(id)
        return entry_manager.get_entry(id)

    # delete user entry from list

    def delete(self, id):
        self.abort_if_entry_doesnt_exist(id)
        entry_manager.delete_entry(id)

    # edit and update user entry record"""

    @marshal_with(entry_fields)
    def put(self, id):
        self.abort_if_entry_doesnt_exist(id)
        entry = entry_manager.get_entry(id)
        parser = reqparse.RequestParser()
        parser.add_argument('entry', type=str)
        args = parser.parse_args()
        if 'entry' in args:
            entry.entry = args['entry']
        return entry


# object that holds the user entries
class EntryList(Resource):

    # get a list of all entries

    @marshal_with(entry_fields)
    def get(self):
        return [v for v in entry_manager.entries.values()]

    # add a single entry to the list

    @marshal_with(entry_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('entry', type=str, required=True, help='Entry cannot be blank')
        args = parser.parse_args()
        entry = EntryModel(
            entry=args['entry'],
            creation_date=datetime.now(utc))
        entry_manager.insert_entry(entry)
        return entry, 201


# flask web server declaration

app = Flask(__name__)
api = Api(app)
api.add_resource(EntryList, '/api/v1/entries')
api.add_resource(Entry, '/api/v1/entries/<int:id>', endpoint='entry_endpoint')

if __name__ == '__main__':
    app.run(debug=True)
