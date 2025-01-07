# TripAI - AI-Powered Travel Planner

TripAI is a Flask-based web application that helps users plan their trips using AI technology. It generates detailed travel itineraries, provides PDF exports, and manages trip information through a user-friendly interface.

## Features

- User authentication and account management
- AI-powered trip itinerary generation using Groq API
- PDF export of travel itineraries with QR codes
- Currency conversion support
- Detailed day-by-day trip planning
- Secure storage of trip information

## Prerequisites

- Python 3.8 or higher
- PostgreSQL (optional, SQLite is used by default)
- Groq API key for AI functionality

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd tripai
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=sqlite:///tripai.db  # Or your PostgreSQL URL
```

5. Initialize the database:
```bash
python init_db.py
```

## Running the Application

1. Start the development server:
```bash
python run.py
```

2. Access the application at `http://localhost:5000`

## Project Structure

```
tripai/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── pdf_generator.py
│   ├── routes.py
│   └── utils.py
├── instance/
│   └── pdfs/
├── .env
├── init_db.py
├── requirements.txt
└── run.py
```

## Key Components

- `app/__init__.py`: Application factory and initialization
- `app/config.py`: Configuration settings
- `app/models.py`: Database models for User and Trip
- `app/pdf_generator.py`: PDF generation functionality
- `app/routes.py`: Application routes and views
- `app/utils.py`: Utility functions for trip planning

## API Integration

The application uses the Groq API for generating trip itineraries. Ensure you have a valid API key set in your environment variables.

## PDF Generation

The application generates detailed PDF itineraries with:
- Trip overview
- Day-by-day planning
- QR code for digital access
- Custom formatting and sections

## Database Schema

### User Model
- id: Primary key
- username: Unique username
- email: Unique email address
- password_hash: Hashed password
- trips: Relationship to Trip model

### Trip Model
- id: Primary key
- user_id: Foreign key to User
- start_location: Starting point
- destination: Trip destination
- start_date: Trip start date
- end_date: Trip end date
- budget_amount: Trip budget
- budget_currency: Budget currency
- itinerary: Generated trip plan
- created_at: Creation timestamp

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## Security Considerations

- User passwords are hashed using Werkzeug's security functions
- Session management using Flask-Login
- Environment variables for sensitive configuration
- Input validation for trip planning parameters
- Secure file handling for PDF generation


