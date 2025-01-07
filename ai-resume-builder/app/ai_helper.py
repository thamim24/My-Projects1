# app/ai_helper.py
import os
import requests
from config import Config

def createGroq(config):
    """
    Create a Groq API client configuration.
    """
    return {
        'baseURL': config.get('baseURL', 'https://api.groq.com/openai/v1'),
        'apiKey': config.get('apiKey', Config.GROQ_API_KEY)
    }

def generateText(params):
    """
    Generate text using Groq API.
    
    :param params: Dictionary containing model, prompt, and other generation parameters
    :return: Dictionary with generated text
    """
    model = params.get('model', {})
    prompt = params.get('prompt', '')
    
    headers = {
        'Authorization': f'Bearer {model.get("apiKey", Config.GROQ_API_KEY)}',
        'Content-Type': 'application/json'
    }
    
    payload = {
        'model': model.get('model', 'llama-3.1-70b-versatile'),
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ],
        'max_tokens': 500,
        'temperature': 0.7
    }
    
    try:
        response = requests.post(
            f"{model.get('baseURL', 'https://api.groq.com/openai/v1')}/chat/completions", 
            headers=headers, 
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        return {
            'text': result['choices'][0]['message']['content'].strip()
        }
    except requests.RequestException as e:
        print(f"Error generating text: {e}")
        return {'text': 'Unable to generate text due to API error.'}

def generate_resume_ai(resume_data):
    """
    Generate a professional resume using AI.
    """
    prompt = f"Generate a professional resume based on the following information. do not use asterik symbol:\n\n{resume_data}"
    response = generateText({
        'model': createGroq({
            'model': 'llama-3.1-70b-versatile',
            'apiKey': Config.GROQ_API_KEY
        }),
        'prompt': prompt,
    })
    return response['text']

def get_career_advice_ai(skills):
    """
    Provide career advice based on skills.
    """
    prompt = f"Provide career advice for someone with the following skills. do not use asterik symbol:\n\n{skills}"
    response = generateText({
        'model': createGroq({
            'model': 'llama-3.1-70b-versatile',
            'apiKey': Config.GROQ_API_KEY
        }),
        'prompt': prompt,
    })
    return response['text']

def score_resume(resume_text):
    """
    Score a resume and provide improvement suggestions.
    
    :param resume_text: Text content of the resume
    :return: Tuple of (score, suggestions)
    """
    prompt = f"""Analyze the following resume and provide:
1. A numerical score from 0-100 
2. 3-5 specific, actionable improvement suggestions
3. Format the response exactly as:
Score: [numeric score]
Suggestions:
1. [First suggestion]
2. [Second suggestion]
3. [Third suggestion]

Resume:
{resume_text}"""

    response = generateText({
        'model': createGroq({
            'model': 'llama-3.1-70b-versatile',
            'apiKey': Config.GROQ_API_KEY
        }),
        'prompt': prompt,
    })

    # Enhanced parsing of the response
    try:
        # Split the response into lines
        lines = response['text'].strip().split('\n')
        
        # Debug print to understand the AI's response
        print("AI Response:", lines)
        
        # More robust score extraction
        score_candidates = [line for line in lines if line.lower().startswith('score:')]
        if score_candidates:
            score_line = score_candidates[0].replace('Score:', '').strip()
            score = int(score_line)
        else:
            # Fallback method to extract first numeric value
            score_match = [int(word) for word in lines[0].split() if word.isdigit()]
            score = score_match[0] if score_match else 50
        
        # Extract suggestions
        suggestions = [
            line.strip() for line in lines 
            if line.strip() and 
            not line.lower().startswith(('score:', 'suggestions:')) and 
            not line[0].isdigit()
        ][:5]
        
        # Validate score and suggestions
        score = max(0, min(score, 100))  # Ensure score is between 0-100
        
        # Fallback if no suggestions found
        if not suggestions:
            suggestions = [
                "Ensure your resume includes a clear professional summary",
                "Quantify your achievements with specific metrics",
                "Tailor your resume to the specific job description",
                "Use industry-specific keywords",
                "Proofread for grammar and formatting consistency"
            ]
        
        return score, suggestions
    
    except Exception as e:
        print(f"Comprehensive error parsing resume score: {e}")
        return 50, [
            "Ensure your resume includes a clear professional summary",
            "Quantify your achievements with specific metrics",
            "Tailor your resume to the specific job description",
            "Use industry-specific keywords",
            "Proofread for grammar and formatting consistency"
        ]

def get_industry_keywords(industry):
    """
    Get important keywords for a specific industry.
    """
    prompt = f"Provide important keywords for the {industry} industry in the context of resume writing. Do not use asterisks or numbers for listing. Directly list the keywords and their content without additional phrases like 'Here is a list of...'. Avoid leaving blank line spaces between the listed points; they should follow one after another without gaps. there should be only one keyword for each point"

    response = generateText({
        'model': createGroq({
            'model': 'llama-3.1-70b-versatile',
            'apiKey': Config.GROQ_API_KEY
        }),
        'prompt': prompt,
    })
    return response['text'].split('\n')

def visualize_career_path(skills):
    """
    Suggest a potential career path based on skills.
    """
    prompt = f"Based on the following skills, suggest a potential career path with 5 steps. do not use asterik symbol:\n\n{skills}"
    response = generateText({
        'model': createGroq({
            'model': 'llama-3.1-70b-versatile',
            'apiKey': Config.GROQ_API_KEY
        }),
        'prompt': prompt,
    })
    return response['text'].split('\n')