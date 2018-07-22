from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import EntryModel
import status
from pytz import utc


class EntryManager:
    last_id = 0

    def __init__(self):
        self.entries = {}

    def insert_entry(self, entry):
        self.__class__ .last_id += 1
        entry.id = self.__class__.last_id
        self.entries[self.__class__.last_id] = entry

    def get_entry(self, id):
        return self.entries[id]

    def delete_entry(self, id):
        return self.entries[id]


entry_fields = {
    'id': fields.Integer,
    'uri': fields.Url('entry_endpoint'),
    'entry': fields.String,
    'creation_date': fields.DateTime
}
entry_manager = EntryManager()

# entry collection declaration


class Entry(Resource):
    def abort_if_entry_doesnt_exist(self, id):
        if id not in entry_manager.entries:
            abort(
                status.HTTP_404_NOT_FOUND,
                entry="Entry {0} doesn't exist".format(id))

    @marshal_with(entry_fields)
    def get(self, id):
        self.abort_if_entry_doesnt_exist(id)
        return entry_manager.get_entry(id)

    def get(self, id):
        self.abort_if_entry_doesnt_exist(id)
        entry_manager.delete_entry(id

    @marshal_with(entry_fields)
    def patch(self, id):
        self.abort_if_entry_doesnt_exist(id)
        entry = entry_manager.get_entry(id)
        parser = reqparse.RequestParser()
        parser.add_argument('entry', type=str)
        args = parser.parse_args()
        if 'entry' in args:
            entry.entry = args['entry']
        return entry

class EntryList(Resource):
    @marshal_with(entry_fields)
    def get(self):
        return [v for v in entry_manager.entries.values()]

    @marshal_with(entry_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('entry', type=str, required=True, help='Entry cannot be blank')
        args = parser.parse_args()
        entry = EntryModel(
            entry=args['entry'],
            creation_date=datetime.now(utc))
        entry_manager.insert_entry(entry)
        return entry, status.HTTP_201_CREATED



app = Flask(__name__)
api = Api(app)
api.add_resource(EntryList, '/api/entries/')
api.add_resource(Entry, '/api/entries/<int:id>', endpoint='entry_endpoint')


if __name__ == '__main__':
    app.run(debug=True)
