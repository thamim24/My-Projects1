# AI-Powered Resume Builder & Career Guidance Platform

## Project Overview

This is a Flask-based web application that leverages AI to help users generate professional resumes, receive resume scoring, and get personalized career advice. The platform uses advanced language models to provide intelligent recommendations and guidance for job seekers.

## Key Features

- User Authentication (Register/Login)
- AI-Powered Resume Generation
- Resume Score and Improvement Suggestions
- Personalized Career Advice
- Career Path Visualization
- User Dashboard for Tracking Resumes and Advice

## Technology Stack

- Backend: Flask
- Database: SQLAlchemy
- Authentication: Flask-Login
- AI Integration: Groq API
- Frontend: Flask Templates, WTForms
- Language Model: Llama 3.1 70B Versatile

## Prerequisites

- Python 3.8+
- pip (Python Package Manager)
- A Groq API Key

## Installation Steps

1. Extract the Project Zip File
```bash
# Unzip the project file
unzip ai-resume-builder.zip
cd ai-resume-builder
```

2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Configure Environment Variables
Create a `config.py` file in the project root with the following:
```python
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    GROQ_API_KEY = 'your_groq_api_key'
```

5. Initialize the Database
```bash
flask db upgrade  # If using Flask-Migrate
# Or
python run.py  # Creates the database via db.create_all()
```

6. Run the Application
```bash
python run.py
```

## Environment Setup Notes

- Ensure you have a Groq API key
- Set the `GROQ_API_KEY` in your `config.py` -> `.env`
- The application uses SQLite by default; modify `SQLALCHEMY_DATABASE_URI` for other databases

## Security Recommendations

- Use a strong, unique `SECRET_KEY`
- Never commit API keys or sensitive information to version control
- Use environment variables in production

## Contributions

Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

## License

[Specify your license, e.g., MIT License]

## Disclaimer

This is an AI-assisted platform. Resume and career advice should be reviewed and personalized by the user.
