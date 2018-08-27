from marshmallow import Schema,fields, pre_load
from marshmallow import validate
import psycopg2
from flask_marshmallow import Marshmallow

pgdb = psycopg2
ma = Marshmallow

# connect to database
conn = pgdb.connect("dbname=diary user=owen")

# open cursor to perform db operation
cur = conn.cursor()


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


