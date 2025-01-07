# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-hard-to-guess-secret-key'
    # Other existing configurations
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY') or 'your-groq-api-key'
    
    # SQLAlchemy Configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///resume_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False