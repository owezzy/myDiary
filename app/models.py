from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_load, ValidationError, validates_schema
from passlib.hash import pbkdf2_sha256 as sha256

db = SQLAlchemy()
ma = Marshmallow()
"""manipulate resources through SQL alchemly sessions """


class AddUpdateDelete:
    @staticmethod
    def add(resource):
        db.session.add(resource)
        return db.session.commit()

    @staticmethod
    def update():
        return db.session.commit()

    @staticmethod
    def delete(resource):
        db.session.delete(resource)
        return db.session.commit()


# Diary entry
class EntryModel(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    content = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False)

    def __init__(self, title, content):
        # new id is generated automatically
        self.title = title
        self.content = content

    @classmethod
    def is_unique(cls, id):
        existing_entry = cls.query.filter_by(id=id).first()
        if existing_entry is None:
            return True
        else:
            if existing_entry.id == id:
                return True
            else:
                return False


# custom validation
@validates_schema(pass_original=True)
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


# Schema
class EntryModelScheme(ma.ModelSchema):
    id = fields.Int(dump_only=True)
    title = fields.String(required=True, validate=must_not_be_blank)
    content = fields.String(required=True, validate=must_not_be_blank)
    creation_date = fields.DateTime(dump_only=True)
    url = ma.URLFor('api.entryresource', id='<id>', _external=True)

    @pre_load
    def process_entry(self, data):
        entry = data.get('entry')
        if entry:
            entry_dict = entry
        else:
            entry_dict = {}
        data['entry'] = entry_dict
        return data


# user model
class UserModel(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(140), nullable=False)
    password = db.Column(db.String(70), nullable=False)
    creation_date = db.Column(
        db.TIMESTAMP,
        server_default=db.func.current_timestamp(),
        nullable=False)

    def __init__(self, username, email, password):
        # new id is generated automatically
        self.username = username
        self.email = email
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class UserModelSchema(ma.ModelSchema):
    id = fields.Int(dump_only=True)
    username = fields.String(required=True, validate=must_not_be_blank)
    email = fields.Email(required=True, validate=must_not_be_blank)
    password = fields.String(required=True, validate=must_not_be_blank)
    creation_date = fields.DateTime(dump_only=True)


class RevokedTokenModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def add(self):
        db.session.add(self)
        return db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)


class RevokedTokenModelSchema(ma.ModelSchema):
    id = fields.Int(dump_only=True)
    jti = fields.String(required=True)
