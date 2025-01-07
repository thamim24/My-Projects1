# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def init_db(app):
    """Initialize the database and create all tables."""
    with app.app_context():
        db.create_all()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from .routes import main, auth, trip
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(trip)

    # Initialize database
    init_db(app)

    return app