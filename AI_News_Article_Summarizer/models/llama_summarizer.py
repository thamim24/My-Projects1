# models/llama_summarizer.py
import groq
import requests
from bs4 import BeautifulSoup

class LLaMASummarizer:
    def __init__(self, api_key):
        self.client = groq.Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"

    def fetch_article(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # Break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # Drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error fetching article: {e}")
            return None

    def summarize(self, text, max_length=150, language="english", sentiment=True, entities=True, topic=True):
        prompt = f"""Summarize the following text in about {max_length} words:

        {text}

        Then, provide an analysis of the summary:
        {"- Overall sentiment" if sentiment else ""}
        {"- Key entities (people, organizations, locations) mentioned" if entities else ""}
        {"- Topic classification" if topic else ""}

        Summary and Analysis:"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_length + 200,  # Additional tokens for analysis
            temperature=0.7,
        )

        return response.choices[0].message.content

    def summarize_from_url(self, url, max_length=150, language="english", sentiment=True, entities=True, topic=True):
        article_text = self.fetch_article(url)
        if article_text:
            return self.summarize(article_text, max_length, language, sentiment, entities, topic)
        else:
            return "Failed to fetch article content."

    def translate(self, text, target_language):
        prompt = f"Translate the following text to {target_language}: {text}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.3,
        )

        return response.choices[0].message.content