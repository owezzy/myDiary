from flask import Flask
from flask_restful import abort, Api, fields, marshal_with, reqparse, Resource
from datetime import datetime
from models import EntryModel
import status
from pytz import utc

app = Flask(__name__)
api = Api(app)
api.add_resource(EntryList, '/api/entries/')
api.add_resource(Entry, '/api/entries/<int:id>', endpoint='entry_endpoint')


if __name__ == '__main__':
    app.run(debug=True)
