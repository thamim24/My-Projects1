import streamlit as st
import sys
import os
from dotenv import load_dotenv

def load_css():
    try:
        css_file_path = os.path.join(os.path.dirname(__file__), 'styles.css')
        with open(css_file_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Custom CSS file not found. Using default styling.")

# Call the function to load CSS
load_css()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'models')))
from llama_summarizer import LLaMASummarizer

# Load environment variables from .env file
load_dotenv()

# Load GroqCloud API key
api_key = os.environ.get('GROQ_API_KEY')
if not api_key:
    st.error("Please set the GROQ_API_KEY in your .env file or environment variables")
    st.stop()

# Initialize the summarizer
summarizer = LLaMASummarizer(api_key)

# Sidebar for navigation
page = st.sidebar.radio("Go to", ["Home", "About"])

if page == "Home":
    st.title("Automated News Article Summarizer using Llama 3.1")

    # User input
    input_type = st.radio("Choose input type:", ["URL", "Text"])

    if input_type == "URL":
        article_url = st.text_input("Enter the news article URL:")
    else:
        article_text = st.text_area("Paste your news article here:", height=200)

    max_length = st.slider("Summary length (words)", 50, 200, 100)
    include_sentiment = st.checkbox("Include sentiment analysis", value=True)
    include_entities = st.checkbox("Extract key entities", value=True)
    include_topic = st.checkbox("Classify topic", value=True)

    if st.button("Summarize"):
        if (input_type == "URL" and article_url) or (input_type == "Text" and article_text):
            with st.spinner("Generating summary and analysis..."):
                if input_type == "URL":
                    result = summarizer.summarize_from_url(
                        article_url,
                        max_length=max_length,
                        sentiment=include_sentiment,
                        entities=include_entities,
                        topic=include_topic
                    )
                else:
                    result = summarizer.summarize(
                        article_text,
                        max_length=max_length,
                        sentiment=include_sentiment,
                        entities=include_entities,
                        topic=include_topic
                    )
                
                # Store result in session state
                st.session_state.summary_result = result
                st.session_state.translation_result = None  # Clear previous translation

        else:
            st.warning("Please enter a URL or article text to summarize.")

    # Display summary result if it exists
    if 'summary_result' in st.session_state:
        st.subheader("Summary and Analysis")
        st.write(st.session_state.summary_result)

    # Translation feature
    st.subheader("Translation")
    text_to_translate = st.text_area("Enter text to translate:")
    target_language = st.selectbox("Target language", ["French", "Tamil", "German", "Chinese", "Hindi"])

    if st.button("Translate"):
        if text_to_translate:
            with st.spinner("Translating..."):
                translated_text = summarizer.translate(text_to_translate, target_language)
                st.session_state.translation_result = translated_text  # Store translation in session state
        else:
            st.warning("Please enter text to translate.")

    # Display translation result if it exists
    if 'translation_result' in st.session_state:
        st.write("Translated text:")
        st.write(st.session_state.translation_result)

elif page == "About":
    st.title("About Automated News Article Summarizer")
    st.write("""
    The Automated News Article Summarizer is an innovative tool designed to help users quickly digest large volumes of news content. By leveraging the power of LLaMA 3.1, a state-of-the-art language model, our application provides concise and accurate summaries of news articles.

    **Key Features**:
    - Summarization of articles from URLs or pasted text
    - Customizable summary length
    - Sentiment analysis
    - Key entity extraction
    - Topic classification
    - Multi-language translation support

    **Our goal** is to enhance media consumption efficiency and improve information retention for readers in today's fast-paced information age.

    For more information or support, please contact our team at support@newsummarizer.com.
    """)

    st.subheader("How It Works")
    st.write("""
    1. **Input**: Users provide a news article URL or paste the article text directly.
    2. **Processing**: Our LLaMA-based model analyzes the content, extracting key information.
    3. **Summarization**: A concise summary is generated based on the most important points.
    4. **Analysis**: Optional sentiment analysis, entity extraction, and topic classification are performed.
    5. **Output**: The summary and analysis results are presented to the user.
    6. **Translation**: Users can translate the summary or any text into multiple languages.
    """)

    st.subheader("Privacy & Data Usage")
    st.write("""
    We respect your privacy. No personal data or article content is stored on our servers. All processing is done in real-time and discarded after the summary is generated.

    **Why Choose Our Summarizer**:
    - **Efficiency**: Get quick insights without reading entire articles.
    - **Comprehensive Analysis**: Understand the sentiment, topics, and key entities involved.
    - **Multi-language Translation**: Access content in the language of your choice.
    """)
