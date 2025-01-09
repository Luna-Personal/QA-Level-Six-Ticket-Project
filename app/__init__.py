# Importing packages
from flask import Flask
from flask import SQLAlchemy
from flask import Bcrypt
from flask import LoginManager
from flask import Migrate
from config import Config


# Setting up Variables
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
migrate = Migrate()


# Creating a function to create and configure the Flask App
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main
    app.register_blueprint(main)

    return app

