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


class EntryModel:
    def __init__(self, title, entry, creation_date):
        # new id is generated automatically
        self.id = 0
        self.title = title
        self.entry = entry
        self.creation_date = creation_date


# user model
class UserModel:
    def __init__(self, username, email, password, creation_date):
        self.id = 0
        self.username = username
        self.email = email
        self.password = password
        self.creation_date = creation_date


