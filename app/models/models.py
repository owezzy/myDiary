
class EntryModel:
    def __init__(self, title, entry, creation_date):
        # new id is generated automatically
        self.id = 0
        self.title = title
        self.entry = entry
        self.creation_date = creation_date


# user model
class UserModel:
    def __init__(self, username, email, password):
        self.id = 0
        self.username = username
        self.email = email
        self.password = password
