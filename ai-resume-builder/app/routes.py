# app/routes.py
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from app.forms import ResumeForm
from app.utils import generate_resume, get_career_advice
from app.ai_helper import score_resume, get_industry_keywords, visualize_career_path
from app.models import Resume, CareerAdvice

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """
    Landing page route.
    Shows different content based on authentication status.
    """
    return render_template('index.html')

@main.route('/resume_builder', methods=['GET', 'POST'])
@login_required
def resume_builder():
    """
    Resume builder route with AI-powered resume generation.
    Requires user authentication.
    """
    form = ResumeForm()
    if form.validate_on_submit():
        try:
            # Prepare resume data
            resume_data = form.data
            generated_resume = generate_resume(resume_data)
            
            # Score the resume
            score, suggestions = score_resume(generated_resume)
            keywords = get_industry_keywords(resume_data['industry'])
            
            # Save resume to database
            new_resume = Resume(
                user_id=current_user.id,
                name=resume_data['name'],
                email=resume_data['email'],
                phone=resume_data['phone'],
                summary=resume_data['summary'],
                experience=resume_data['experience'],
                education=resume_data['education'],
                skills=resume_data['skills'],
                industry=resume_data['industry'],
                resume_score=score,
                suggestions=', '.join(suggestions)
            )
            
            # Add and commit to database
            from app import db
            db.session.add(new_resume)
            db.session.commit()
            
            flash('Resume generated and saved successfully!', 'success')
            
            return render_template(
                'resume_builder.html', 
                form=form, 
                resume=generated_resume, 
                score=score, 
                suggestions=suggestions, 
                keywords=keywords
            )
        
        except Exception as e:
            # Log the error and flash a user-friendly message
            flash(f'An error occurred: {str(e)}', 'error')
            # Optionally log the full error details
            print(f"Resume generation error: {e}")
    
    return render_template('resume_builder.html', form=form)

@main.route('/career_advice', methods=['GET', 'POST'])
@login_required
def career_advice():
    """
    Career advice route with personalized recommendations.
    Requires user authentication.
    """
    skills = request.args.get('skills', '')
    
    if skills:
        try:
            # Generate career advice
            advice = get_career_advice(skills)
            career_path = visualize_career_path(skills)
            
            # Save career advice to database
            new_career_advice = CareerAdvice(
                user_id=current_user.id,
                skills=skills,
                advice=advice,
                career_path=', '.join(career_path)
            )
            
            # Add and commit to database
            from app import db
            db.session.add(new_career_advice)
            db.session.commit()
            
            flash('Career advice generated successfully!', 'success')
            
            return render_template(
                'career_advice.html', 
                advice=advice, 
                career_path=career_path
            )
        
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            print(f"Career advice generation error: {e}")
    
    return render_template('career_advice.html')

@main.route('/dashboard')
@login_required
def dashboard():
    """
    User dashboard to view saved resumes and career advice.
    """
    # Fetch user's resumes
    user_resumes = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.created_at.desc()).all()
    
    # Fetch user's career advice history
    career_advice_history = CareerAdvice.query.filter_by(user_id=current_user.id).order_by(CareerAdvice.created_at.desc()).all()
    
    return render_template(
        'dashboard.html', 
        resumes=user_resumes, 
        career_advice_history=career_advice_history
    )

@main.route('/api/resume_score', methods=['POST'])
@login_required
def api_resume_score():
    """
    API endpoint for scoring a resume.
    Requires user authentication.
    """
    resume_text = request.json['resume']
    score, suggestions = score_resume(resume_text)
    return jsonify({'score': score, 'suggestions': suggestions})

@main.route('/delete_resume/<int:resume_id>', methods=['POST'])
@login_required
def delete_resume(resume_id):
    """
    Delete a specific resume.
    Ensures the resume belongs to the current user.
    """
    from app import db
    resume = Resume.query.get_or_404(resume_id)
    
    # Check if the resume belongs to the current user
    if resume.user_id != current_user.id:
        flash('You are not authorized to delete this resume.', 'error')
        return redirect(url_for('main.dashboard'))
    
    try:
        db.session.delete(resume)
        db.session.commit()
        flash('Resume deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting resume: {str(e)}', 'error')
    
    return redirect(url_for('main.dashboard'))