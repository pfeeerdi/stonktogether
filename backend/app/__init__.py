from flask import Flask
from app.config import Config, TestConfig
from flask_bcrypt import Bcrypt
from flask_cors import CORS
#from app.create_db import create_db

#db = SQLAlchemy()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # bcrypt.init_app(app)
    # db.init_app(app)
    # with app.app_context():
    #     from app.model import User
    #     try:
    #         db.create_all()
    #     except:
    #         create_db()
    #         db.create_all()
    #     print("DB connected")
    #     if User.query.first() is None:
    #         from app.generate import generate
    #         generate()

    from app.controller import blueprint as api
    app.register_blueprint(api, url_prefix="")

    CORS(app, support_credentials=False)
    return app