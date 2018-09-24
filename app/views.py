from flask import Blueprint, request, jsonify,render_template
from flask_restful import Api, Resource
from models import db, EntryModel, EntryModelScheme, UserModel, UserModelSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError


api_bp = Blueprint('api', __name__)
entry_schema = EntryModelScheme()
entries_schema = EntryModelScheme(many=True)
user_schema = UserModelSchema()
users_schema = UserModelSchema(many=True)
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
    def get(self):
        entries = EntryModel.query.all()
        result = entries_schema.dump(entries, many=True)
        return result

    def post(self):
        request_dict = request.get_json(force=True)
        # Validate and deserialize input
        errors = entry_schema.validate(request_dict)
        if errors:
            return errors, 400
        if not UserModel.is_unique(id=0):
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


class UserRegistration(Resource):

    def post(self):
        request_dict = request.get_json(force=True)
        errors = user_schema.validate(request_dict)
        if errors:
            return errors, 400
        if UserModel.find_by_username(request_dict['username']):
            return {'error': 'username {} already registered!'.format(request_dict['username'])}, 400
        try:
            # create a new User
            user = UserModel(
                username=request_dict['username'],
                email=request_dict['email'],
                password=UserModel.generate_hash(request_dict['password'])
            )
            user.add(user)
            access_token = create_access_token(identity=request_dict['username'])
            refresh_token = create_refresh_token(identity=request_dict['username'])
            query = UserModel.query.get_or_404(user.id)
            result = user_schema.dump(query).data
            return {'created new diary User': result['username'],
                    'access_token': access_token,
                    'refresh_token': refresh_token}, 201
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': e}, 400


class UserLogin(Resource):
    def post(self):
        request_dict = request.get_json()
        current_user = UserModel.find_by_username(request_dict['username'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(request_dict['username'])}

        if UserModel.verify_hash(request_dict['password'], current_user.password):
            access_token = create_access_token(identity=request_dict['username'])
            refresh_token = create_refresh_token(identity=request_dict['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        else:
            return {'message': 'Password does not match the username'}


class UserLogoutAccess(Resource):
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Access token has been revoked'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': e}, 400


class UserLogoutRefresh(Resource):
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {'message': 'Refresh token has been revoked'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'error': e}, 400


class TokenRefresh(Resource):
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}


# for testing purposes
class AllUsers(Resource):
    def get(self):
        users = UserModel.query.all()
        result = users_schema.dump(users, many=True)
        return result

    def delete(self):
        user = UserModel.query.all()
        try:
            delete = user.delete()
            db.session.commit()
            response = {'message': delete}
            return response, 204
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error": e})
            return resp, 401


api.add_resource(EntryResource, '/entries/<int:id>')
api.add_resource(EntryListResource, '/entries/')
