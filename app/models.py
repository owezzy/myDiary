from marshmallow import Schema,fields, pre_load
from marshmallow import validate
from  flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()


"""manipulate resources through SQL alchemly sessions """

class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class EntryModel(db.Model, AddUpdateDelete):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    entry = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.TIMESTAMP,
                              server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, title, entry, creation_date):
        # new id is generated automatically
        self.id = 0
        self.title = title
        self.entry = entry
        self.creation_date = creation_date


# Schema
class EntryModelScheme(ma.Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String(required=True, validate=validate.lenght(1))
    entry = fields.String(required=True, validate=validate.length(1))
    creation_date = fields.DateTime()
    url = ma.URLFor('api.entryresource', id='<id>', _external=True)


# user model
class UserModel:
    def __init__(self, username, email, password, creation_date):
        self.id = 0
        self.username = username
        self.email = email
        self.password = password
        self.creation_date = creation_date


