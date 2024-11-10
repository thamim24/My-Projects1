# Automated News Article Summarizer using LLaMA 3.1
.
# Project Description: 
   In today's information age, the sheer volume of news content poses a challenge for users to stay informed without investing significant time. This project aims to address this issue by developing an Automated Content Summarizer for News Articles. The solution leverages LLaMA, a powerful language model, to automatically generate concise and coherent summaries from lengthy news articles. By integrating advanced natural language processing capabilities, the tool will enhance media consumption efficiency and improve information retention for readers.

# How LLaMA is Utilized in the Project: 
   LLaMA, like other open large language models (LLMs), will serve as the core engine for text summarization within the project. Specifically, LLaMA's capabilities in understanding and synthesizing complex textual information will be harnessed to extract the most significant information from news articles. Through fine-tuning and adapting LLaMA's pre-trained model, the system will be optimized to generate accurate and contextually relevant summaries tailored to various news topics and styles. This approach ensures that the automated summaries maintain high quality and readability, enhancing the overall user experience.

## Installation

1. **Download or Clone the Repository:**

   Download the project files as a ZIP folder or clone the repository using Git.

2. **Extract the Files:**

   If you downloaded the ZIP folder, extract it to your desired location.

3. **Navigate to the Project Directory:**

   Open a terminal or command prompt and navigate to the project directory.

   ```bash
   cd AI_News_Article_Summarizer
   ```

4. **Create a Virtual Environment (Optional but Recommended):**

   It's a good practice to create a virtual environment to manage your project's dependencies.

   ```bash
   python -m venv venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

5. **Install Requirements:**

   Install the required packages using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Updating Groq Cloud API Key

To use the Groq Cloud LLaMA 3.1 70B Versatile model, you need to set your API key as an environment variable:

1. **Obtain your Groq API key** from the Groq Cloud platform.

2. **Set the API key as an environment variable:**

   - On Windows:
     ```bash
     set GROQ_API_KEY=your_api_key_here
     ```

   - On macOS/Linux:
     ```bash
     export GROQ_API_KEY=your_api_key_here
     ```

## Usage

1. **Run the Application:**

   Start the Streamlit application with the following command:

   ```bash
   streamlit run app/streamlit_app.py
   ```

2. **Open Your Web Browser:**

   After running the command, a new browser window should open. If it doesn't, navigate to `http://localhost:8502` in your web browser.



## Requirements

Make sure to install the following Python packages:

```plaintext
groq
streamlit==1.31.0
python-dotenv==1.0.0
requests==2.31.0
beautifulsoup4==4.12.2
ipywidgets

```

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

---

Feel free to modify any part of this README to better suit your project's specifics or your preferences!