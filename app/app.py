from flask import Flask
from flask_jwt_extended import JWTManager



def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    jwt = JWTManager(app)

    from models import db
    db.init_app(app)

    from views import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
