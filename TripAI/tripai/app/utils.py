# app/utils.py
import re
from datetime import datetime, timedelta
from forex_python.converter import CurrencyRates
from typing import Dict, List, Tuple, Optional
import json

def calculate_trip_duration(start_date: datetime, end_date: datetime) -> int:
    """Calculate the duration of a trip in days."""
    delta = end_date - start_date
    return delta.days + 1

def format_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """Convert amount from one currency to another using current exchange rates."""
    try:
        c = CurrencyRates()
        converted = c.convert(from_currency, to_currency, amount)
        return round(converted, 2)
    except Exception:
        # Return original amount if conversion fails
        return amount

def generate_trip_prompt(start_location: str, destination: str, start_date: datetime, 
                        end_date: datetime, budget: Dict[str, any]) -> str:
    """Generate an AI prompt for trip planning."""
    duration = calculate_trip_duration(start_date, end_date)
    
    prompt = f"""As a travel expert, create a detailed {duration}-day trip itinerary from {start_location} to {destination}.
The trip starts on {start_date.strftime('%Y-%m-%d')} and ends on {end_date.strftime('%Y-%m-%d')}.
The total budget is {budget['currency']} {budget['amount']}.

Please include:
1. Day-by-day itinerary with specific activities and attractions
2. Recommended accommodations within budget
3. Transportation suggestions between locations
4. Estimated costs for main activities
5. Local cuisine recommendations
6. Cultural customs and etiquette tips
7. Weather considerations for the travel dates
8. Emergency contact numbers and important locations

Format the response in clear sections with Markdown formatting."""

    return prompt

def parse_itinerary(itinerary_text: str) -> Dict[str, any]:
    """Parse the AI-generated itinerary into structured data."""
    sections = {
        'daily_plan': [],
        'accommodations': [],
        'transportation': [],
        'costs': {},
        'recommendations': [],
        'tips': []
    }
    
    current_section = None
    current_day = None
    
    for line in itinerary_text.split('\n'):
        if re.match(r'^#+ ', line):  # Section header
            current_section = line.lstrip('#').strip().lower()
            continue
            
        if re.match(r'^Day \d+:', line):  # Daily itinerary
            current_day = {
                'day': re.match(r'^Day (\d+):', line).group(1),
                'activities': []
            }
            sections['daily_plan'].append(current_day)
            continue
            
        if current_day and line.strip():
            current_day['activities'].append(line.strip())
            
    return sections

def validate_trip_dates(start_date: str, end_date: str) -> Tuple[bool, Optional[str]]:
    """Validate trip dates."""
    try:
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        if start < datetime.now().date():
            return False, "Start date cannot be in the past"
            
        if end < start:
            return False, "End date must be after start date"
            
        if (end - start).days > 30:
            return False, "Trip duration cannot exceed 30 days"
            
        return True, None
    except ValueError:
        return False, "Invalid date format"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    return re.sub(r'[^a-zA-Z0-9._-]', '_', filename)