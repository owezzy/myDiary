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
            entry_entry = entry_dict['entry'] 
            if EntryModel.is_unique(id=id, entry=entry_entry):
                entry.entry = entry_entry
            else:
                response = {'error': 'An entry with the same entry already exists'}
                return response,HTTP_400_BAD_REQUEST
        if 'title' in entry_dict:
            entry.title = entry_dict['title']
        dumped_entry, dump_errors = entry_schema.dump(message)
        if dump_errors:
            return dump_errors,HTTP_400_BAD_REQUEST
        validate_errors = entry_schema.validate(dumped_message)
        if validate_errors:
            return validate_errors, HTTP_400_BAD_REQUEST
        try:
            entry.update()
            return self.get(id)
        except SQLAlchemyError as e:
                db.session.rollback()
                resp = {"error": str(e)}
                return resp,HTTP_400_BAD_REQUEST

    def delete(self, id):
        entry = EntryModel.query.get_or_404(id)
        try:
            delete = entry.delete(entry)
            response = make_response()
            return response, HTTP_204_NO_CONTENT
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e) })
            return resp, HTTP_401_UNAUTHORIZED


class EntryListResource(Resource):
    def get(self):
        entry = EntryModel.query.all()
        result = entry_scheme.dump(entry, many=True).data
        return result

    def post(self):
        request_dict = request.get_json()
        if not request_dict:
            response = {'message':'no input data provided'}
            return response, HTTP_400_BAD_REQUEST
        errors = entry_scheme.validate(request_dict)
        if errors:
            if errors:
                return errors, status.HTTP_400_BAD_REQUEST
            try:
                # create a new Entry
                entry = EntryModel(
                    entry=request_dict['entry'],
                    title=request_dict['title'],)
                    entry.add(entry)
                    query = EntryModel.query.get(enrty.id)
                    result = entry_schema.dump(query).data
                    return result, HTTP_201_CREATED
            except SQLAlchemyError as e:
                db.session.rollback()
                resp = jsonify({"error": str(e)})
                return resp, HTTP_400_BAD_REQUEST
            
api.add_resource(EntryResource, '/entries/<int:id>')
api.add_resource(EntryListResource, '/entries/')
