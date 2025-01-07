# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField
from wtforms.validators import DataRequired, Email, Optional

class ResumeForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired()])
    summary = TextAreaField('About yourself', validators=[DataRequired()])
    
    institute_name = StringField('Institute Name', validators=[DataRequired()])
    
    experience = SelectField('Work Experience', 
        choices=[
            ('fresher', 'Fresher (0-2 years)'), 
            ('2-5years', '2-5 years'), 
            ('5-10years', '5-10 years'), 
            ('10+years', 'More than 10 years')
        ], 
        validators=[DataRequired()])
    
    education = StringField('Highest Qualification', validators=[DataRequired()])
    skills = StringField('What are your skills?', validators=[DataRequired()])
    
    industry = RadioField('Industry', 
        choices=[
            ('tech', 'Technology'), 
            ('finance', 'Finance'), 
            ('healthcare', 'Healthcare'), 
            ('education', 'Education'),
            ('marketing', 'Marketing'),
            ('engineering', 'Engineering'),
            ('consulting', 'Consulting'),
            ('retail', 'Retail'),
            ('hospitality', 'Hospitality')
        ], 
        validators=[DataRequired()])