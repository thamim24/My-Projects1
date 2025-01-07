# app/routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_user, logout_user, login_required, current_user
from .models import User, Trip, db
from werkzeug.security import generate_password_hash
import os
from datetime import datetime
from .pdf_generator import generate_trip_pdf
from .utils import generate_trip_prompt
import requests
import json

main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)
trip = Blueprint('trip', __name__)

# Main routes
@main.route('/')
def index():
    return render_template('home.html')
# Authentication routes
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.index'))
        
        flash('Please check your login details and try again.')
    return render_template('auth/login.html')

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('auth.register'))

        new_user = User(email=email, username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Updated Trip routes
@trip.route('/plan', methods=['GET', 'POST'])
@login_required
def plan():
    if request.method == 'POST':
        try:
            data = request.get_json()
            
            # Generate the prompt using utility function
            prompt = generate_trip_prompt(
                data['start_location'],
                data['destination'],
                datetime.strptime(data['start_date'], '%Y-%m-%d'),
                datetime.strptime(data['end_date'], '%Y-%m-%d'),
                data['budget']
            )
            
            # Get API key from environment
            api_key = os.getenv('GROQ_API_KEY')
            if not api_key:
                raise ValueError("GROQ_API_KEY environment variable is not set")
            
            # Make direct API request to Groq
            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messages': [
                    {
                        'role': 'system',
                        'content': 'You are an experienced travel planner who creates detailed, personalized travel itineraries.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                'model': 'llama-3.1-70b-versatile',
                'temperature': 0.7,
                'max_tokens': 4096
            }
            
            # Fixed API endpoint URL
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers=headers,
                json=payload,
                timeout=30  # Added timeout
            )
            
            if response.status_code != 200:
                error_message = response.text
                try:
                    error_json = response.json()
                    if 'error' in error_json:
                        error_message = error_json['error'].get('message', error_json['error'])
                except:
                    pass
                raise Exception(f"API request failed: {error_message}")
            
            result = response.json()
            trip_plan = result['choices'][0]['message']['content']
            
            # Save trip to database
            new_trip = Trip(
                user_id=current_user.id,
                start_location=data['start_location'],
                destination=data['destination'],
                start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
                end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
                budget_amount=float(data['budget']['amount']),
                budget_currency=data['budget']['currency'],
                itinerary=trip_plan
            )
            
            db.session.add(new_trip)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'trip_plan': trip_plan,
                'trip_id': new_trip.id
            })
            
        except ValueError as ve:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(ve)
            }), 400
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
            
    return render_template('trip/plan.html')

@trip.route('/trips')
@login_required
def my_trips():
    trips = Trip.query.filter_by(user_id=current_user.id).order_by(Trip.created_at.desc()).all()
    return render_template('trip/trips.html', trips=trips)

@trip.route('/trip/<int:trip_id>/pdf')
@login_required
def download_pdf(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    if trip.user_id != current_user.id:
        return redirect(url_for('main.index'))
    
    try:
        pdf_path = generate_trip_pdf(
            trip.itinerary,
            trip.start_location,
            trip.destination,
            trip.start_date,
            trip.end_date
        )
        
        # Make sure the file exists
        if not os.path.exists(pdf_path):
            flash('Error generating PDF file', 'error')
            return redirect(url_for('trip.my_trips'))
            
        return send_file(
            pdf_path,
            as_attachment=True,
            download_name=os.path.basename(pdf_path)
        )
        
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('trip.my_trips'))