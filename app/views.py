from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from models import db, EntryModel, EntryModelScheme
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


api_bp = Blueprint('api', __name__)
entry_schema = EntryModelScheme()
entries_schema = EntryModelScheme(many=True)
api = Api(api_bp)


class EntryResource(Resource):

    @staticmethod
    def get(id):
        try:
            entry = EntryModel.query.get_or_404(id)
        except IntegrityError:
            return jsonify({'message': 'Entry does not exists!'})
        result = entry_schema.dump(entry).data
        return result

    def put(self, id):
        entry = EntryModel.query.get_or_404(id)
        entry_dict = request.get_json(force=True)
        if 'entry' in entry_dict:
            entry_entry = entry_dict['entry']
            if EntryModel.is_unique(entry=entry_entry):
                entry.entry = id
            else:
                response = {'error': 'No Changes made to the Entry'}
                return response, 400
        if 'title' in entry_dict:
            entry.title = entry_dict['title']
        if 'content' in entry_dict:
            entry.content = entry_dict['content']
        dumped_entry, dump_errors = entry_schema.dump(entry)
        if dump_errors:
            return dump_errors, 400
        validate_errors = entry_schema.validate(dumped_entry)
        if validate_errors:
            return validate_errors, 400
        try:
            entry.update()
            return self.get(id)
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": str(e)})
            return resp, 400

    @staticmethod
    def delete(id):
        entry = EntryModel.query.get_or_404(id)
        try:
            delete = entry.delete(entry)
            response = {'message': delete}
            return response, 204
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": e})
            return resp, 401


class EntryListResource(Resource):

    @staticmethod
    def get():
        entries = EntryModel.query.all()
        result = entries_schema.dump(entries, many=True)
        return result

    @staticmethod
    def post():
        request_dict = request.get_json(force=True)
        if not request_dict:
            response = {'message': 'no input data provided'}
            return response, 400
            # Validate and deserialize input
        errors = entry_schema.validate(request_dict)
        if errors:
            return errors, 400
        if not EntryModel.is_unique(id=0):
            response = {'error': 'An entry with the same id already exists!'}
            return response, 400
        try:
            # create a new Entry
            entry = EntryModel(
                title=request_dict['title'],
                content=request_dict['content'],
            )
            entry.add(entry)
            query = EntryModel.query.get_or_404(entry.id)
            result = entry_schema.dump(query).data
            resp = {
                'message': 'Created new Diary entry',
                'entry': result}
            return resp, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            res = {'error': e}
            return res, 400


api.add_resource(EntryResource, '/entries/<int:id>')
api.add_resource(EntryListResource, '/entries/')
