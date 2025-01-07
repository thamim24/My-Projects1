# app/__init__.py
from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy

# Create SQLAlchemy instance
db = SQLAlchemy()

# Create LoginManager instance
login_manager = LoginManager()
login_manager.login_view = 'auth.login'  # Specify login route
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize LoginManager
    login_manager.init_app(app)
    
    # Import models after initializing db to avoid circular imports
    from app import models
    
    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()

    # Import and register blueprints
    from app import routes
    from app.auth import auth as auth_blueprint
    app.register_blueprint(routes.main)
    app.register_blueprint(auth_blueprint)

    return app