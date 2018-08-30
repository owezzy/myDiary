from flask import Blueprint, request, jsonify, make_response
from flask_restful import Api, Resource
from models import db, EntryModel,EntryModelScheme
from sqlalchemy.exc import SQLAlchemyError

api_bp = Blueprint('api'__name__)
entry_scheme = EntryModelScheme
api = Api(api_bp)

class EntryResource(Resource):
    def get(self, id):
        entry = EntryModel.query.get_or_404(id)
        result = entry_scheme.dump(entry).data
        return result

    def path(self, id):
        entry = EntryModel.query.get_or_404(id)
        entry_dict = request.get_json(force=True)
        if 'entry' in entry_dict:
            message_message = message_dict['message'] 
            if Message.is_unique(id=id, message=message_message):
                message.message = message_message
            else:
                response = {'error': 'A message with the same message already exists'}
                return response, status.HTTP_400_BAD_REQUEST
        if 'duration' in message_dict:
            message.duration = message_dict['duration']
        if 'printed_times' in message_dict:
            message.printed_times = message_dict['printed_times']
        if 'printed_once' in message_dict:
            message.printed_once = message_dict['printed_once']
        dumped_message, dump_errors = message_schema.dump(message)
        if dump_errors:
            return dump_errors, status.HTTP_400_BAD_REQUEST
        validate_errors = message_schema.validate(dumped_message)
        if validate_errors:
            return validate_errors, status.HTTP_400_BAD_REQUEST
        try:
            message.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"error": str(e)}
                return resp, status.HTTP_400_BAD_REQUEST
        
