from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, pre_load, ValidationError, validates_schema

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
class UserModel:
    def __init__(self, username, email, password, creation_date):
        self.id = 0
        self.username = username
        self.email = email
        self.password = password
        self.creation_date = creation_date
