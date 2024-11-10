import streamlit as st
import pandas as pd
from datetime import datetime
from textblob import TextBlob
import altair as alt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import requests
import random
import names
import ollama

# Load zodiac data
@st.cache_data
def load_zodiac_data():
    return pd.read_csv('zodiac_data.csv')

# Find zodiac sign
def find_zodiac(month, day):
    zodiac_signs = {
        'december': ('Sagittarius', 'Capricorn', 22),
        'january': ('Capricorn', 'Aquarius', 20),
        'february': ('Aquarius', 'Pisces', 19),
        'march': ('Pisces', 'Aries', 21),
        'april': ('Aries', 'Taurus', 20),
        'may': ('Taurus', 'Gemini', 21),
        'june': ('Gemini', 'Cancer', 21),
        'july': ('Cancer', 'Leo', 23),
        'august': ('Leo', 'Virgo', 23),
        'september': ('Virgo', 'Libra', 23),
        'october': ('Libra', 'Scorpio', 23),
        'november': ('Scorpio', 'Sagittarius', 22) 
    } 

    
    sign1, sign2, split_day = zodiac_signs.get(month.lower(), (None, None, None))
    return sign1 if day < split_day else sign2

# Generate name using LLaMA 2
def generate_name(zodiac_sign, gender):
    prompt = f"Generate a unique {gender} name that embodies the qualities of the {zodiac_sign} zodiac sign."
    response = ollama.generate(model='llama2:7b', prompt=prompt)
    return response['response'].strip()

# Ollama integration (for generating zodiac descriptions)
def generate_with_ollama(prompt, model="llama2"):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()["response"]
    else:
        return f"Error: {response.status_code}"

# Sentiment Analysis Functions
def convert_to_df(sentiment):
    sentiment_dict = {'polarity': sentiment.polarity, 'subjectivity': sentiment.subjectivity}
    sentiment_df = pd.DataFrame(sentiment_dict.items(), columns=['metric', 'value'])
    return sentiment_df

def analyze_token_sentiment(docx):
    analyzer = SentimentIntensityAnalyzer()
    pos_list = []
    neg_list = []
    neu_list = []
    for word in docx.split():
        res = analyzer.polarity_scores(word)['compound']
        if res > 0.1:
            pos_list.append(word)
        elif res <= -0.1:
            neg_list.append(word)
        else:
            neu_list.append(word)
    result = {'positives': pos_list, 'negatives': neg_list, 'neutral': neu_list}
    return result

# Cache the results for name generation based on zodiac sign and gender
@st.cache_data
def cached_generate_name(zodiac_sign, gender):
    return generate_name(zodiac_sign, gender)

def main():
    st.set_page_config(page_title="AI Zodiac Sign Analysis & Name Generation with Llama 2", page_icon="🔮", layout="wide")
    st.title("🔮AI Zodiac Sign Analysis & Name Generation with Llama 2")

    menu = ["Home", "Summary Report", "Zodiac Board", "About"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        home_page()
    elif choice == "Summary Report":
        summary_report_page()
    elif choice == "Zodiac Board":
        zodiac_board_page()
    else:
        about_page()

def home_page():
    st.header("📅 Enter Your Date of Birth and Gender")
    dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.now())
    gender = st.radio("Gender", ["Male", "Female", "Non-binary"])

    # Initialize session state variables
    if 'zodiac_sign' not in st.session_state:
        st.session_state.zodiac_sign = None
    if 'name' not in st.session_state:
        st.session_state.name = None
    if 'description' not in st.session_state:
        st.session_state.description = None
    if 'sentiment' not in st.session_state:
        st.session_state.sentiment = None
    if 'zdf' not in st.session_state:
        st.session_state.zdf = None
    # Initialize dob and gender in session state
    st.session_state.dob = dob
    st.session_state.gender = gender

    # Generate Zodiac Sign
    if st.button("Generate Zodiac Sign"):
        zodiac_sign = find_zodiac(dob.strftime("%B"), dob.day)
        st.session_state.zodiac_sign = zodiac_sign
        st.success(f"🌟 Your Zodiac Sign: {zodiac_sign}")

    # Generate Name
    if st.button("Generate Name"):
        if st.session_state.zodiac_sign:
            with st.spinner("Generating name with Llama 2..."):
                name = cached_generate_name(st.session_state.zodiac_sign, gender)
                st.session_state.name = name
            st.success(f"Generated Name: {name}")
        else:
            st.warning("Please generate your zodiac sign first.")

    # Load Zodiac Data and Perform Sentiment Analysis
    if st.button("Perform Sentiment Analysis"):
        zodiac_df = load_zodiac_data()
        st.session_state.zdf = zodiac_df[zodiac_df['horoscope'] == st.session_state.zodiac_sign.title()]  # Update zdf based on zodiac sign

        if not st.session_state.zdf.empty:
            st.session_state.description = st.session_state.zdf.iloc[0].description
            st.write(st.session_state.description)

            sentiment = TextBlob(st.session_state.description).sentiment
            st.session_state.sentiment = sentiment
            
            st.subheader("Sentiment Analysis of Zodiac Description")
            col1, col2 = st.columns(2)
            with col1:
                st.info("Results")
                result_df = convert_to_df(sentiment)
                chart = alt.Chart(result_df).mark_bar().encode(
                    x='metric',
                    y='value',
                    color='metric'
                ).properties(width=300, height=200)
                st.altair_chart(chart, use_container_width=True)
                
                if sentiment.polarity > 0:
                    st.markdown("Sentiment: Positive 😊")
                elif sentiment.polarity < 0:
                    st.markdown("Sentiment: Negative 😞")
                else:
                    st.markdown("Sentiment: Neutral 😐")

            with col2:
                st.info("Token Sentiment")
                token_sentiments = analyze_token_sentiment(st.session_state.description)
                st.write("Positive words:", ", ".join(token_sentiments['positives']))
                st.write("Negative words:", ", ".join(token_sentiments['negatives']))
                st.write("Neutral words:", ", ".join(token_sentiments['neutral']))

def summary_report_page():
    st.subheader("Summary Report")

    # Check if required information is in session state
    if 'name' in st.session_state and 'zodiac_sign' in st.session_state and 'zdf' in st.session_state and st.session_state.zdf is not None and not st.session_state.zdf.empty:
        # Retrieve data from session state
        dob = st.session_state.dob  # Now dob is properly initialized
        gender = st.session_state.gender  # Now gender is properly initialized

        # Display the summary report
        st.header("Summary Report")
        st.write(f"Date of Birth: {dob.strftime('%B %d, %Y')}")
        st.write(f"Gender: {gender}")
        st.write(f"Zodiac Sign: {st.session_state.zodiac_sign}")
        st.write(f"Zodiac Alias: {st.session_state.zdf.iloc[0].aliasname}")
        st.write(f"Generated Name (Llama 2): {st.session_state.name}")
    else:
        st.warning("Please make sure you have filled out all necessary information on the home page.")


def zodiac_board_page():
    st.subheader("Zodiac Board")
    df = load_zodiac_data()
    st.dataframe(df)
    
    selected_zodiac = st.selectbox("Select a Zodiac Sign for more details", df['horoscope'].unique())
    
    if selected_zodiac:
        zodiac_info = df[df['horoscope'] == selected_zodiac].iloc[0]
        st.subheader(f"{selected_zodiac} - {zodiac_info['aliasname']}")
        st.write(zodiac_info['description'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("Positives:")
            st.write(", ".join(zodiac_info['positives'].split(',')))
        with col2:
            st.write("Negatives:")
            st.write(", ".join(zodiac_info['negatives'].split(',')))

def about_page():
    st.subheader("About This App")
    st.write(""" 
    This Enhanced Zodiac Analysis App combines astrology, name generation, and sentiment analysis to provide a unique and insightful experience. 
    
    Features include:
    - Zodiac sign identification based on birth date
    - Sentiment analysis of zodiac descriptions
    - Name generation based on zodiac sign
    - Comprehensive zodiac information board
    
    The app uses Llama 2 via Ollama for generating descriptions and explanations, providing a touch of AI-powered insight to traditional astrological concepts.
    """)

if __name__ == '__main__':
    main()
