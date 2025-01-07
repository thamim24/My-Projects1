# app/models.py
from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin, db.Model):
    """
    User model for authentication
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Optional: Add relationships to other models
    resumes = db.relationship('Resume', backref='user', lazy=True)
    career_advice = db.relationship('CareerAdvice', backref='user', lazy=True)

class Resume(db.Model):
    """
    Represents a resume in the system.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add this line
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    summary = db.Column(db.Text)
    experience = db.Column(db.Text)
    education = db.Column(db.Text)
    skills = db.Column(db.Text)
    industry = db.Column(db.String(50))
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resume_score = db.Column(db.Integer)
    suggestions = db.Column(db.Text)
    
class CareerAdvice(db.Model):
    """
    Logs career advice and career path recommendations.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Add this line
    skills = db.Column(db.Text, nullable=False)
    advice = db.Column(db.Text)
    career_path = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)