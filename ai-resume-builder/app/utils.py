# app/utils.py
from app.ai_helper import generate_resume_ai, get_career_advice_ai

def generate_resume(resume_data):
    # Prepare the resume data for AI processing
    ai_input = f"""
    Name: {resume_data['name']}
    Email: {resume_data['email']}
    Phone: {resume_data['phone']}
    Summary: {resume_data['summary']}
    Institute Name: {resume_data['institute_name']}
    Experience: {resume_data['experience']}
    Education: {resume_data['education']}
    Skills: {resume_data['skills']}
    Industry: {resume_data['industry']}
    """
    return generate_resume_ai(ai_input)

def get_career_advice(skills):
    return get_career_advice_ai(skills)