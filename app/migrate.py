from flask_restful import Manager
from flask_migrate import Migrate, MigrateCommand
from models import db
from run import app

migrate = Migrate(app, db)
manager = Manger(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
