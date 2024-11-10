
# AI Zodiac Sign Analysis & Name Generation with Llama 2 App

🔮 **AI Zodiac Sign Analysis & Name Generation with Llama 2 App** combines astrology, name generation, and sentiment analysis to provide a unique and insightful experience. This application uses AI to generate zodiac-related insights and analyze textual descriptions.

## Features

- **Zodiac Sign Identification**: Determine your zodiac sign based on your date of birth.
- **Sentiment Analysis**: Analyze the sentiment of zodiac descriptions using TextBlob and VADER sentiment analysis.
- **Name Generation**: Generate unique names based on the qualities of your zodiac sign using LLaMA 2.
- **Comprehensive Zodiac Information Board**: Explore detailed descriptions, positives, and negatives of each zodiac sign.

## Technologies Used

- **Streamlit**: For building the web application interface.
- **Pandas**: For data manipulation and analysis.
- **TextBlob**: For natural language processing and sentiment analysis.
- **VADER**: For sentiment analysis of individual words.
- **Altair**: For data visualization.
- **Ollama**: For integrating LLaMA 2 model for name generation and zodiac descriptions.

## Installation

1. **Download and Extract the Zip File**: Ensure you have the project zip file and extract its contents to your local directory.

2. **Navigate to the Project Directory**:

   ```bash
   cd AI_Zodiac_Sign_Analysis_&_Name_Generation_with_Llama_2
   ```

3. **Create a Conda Environment**: Create a new Conda environment and download the LLaMA 2 model:

   ```bash
   conda create --name python
   conda activate --name
   ollama pull llama2:7b
   ollama run llama2:7b
   ```

4. **Install the Required Packages**: Navigate to the project directory and run the following command:

   ```bash
   pip install -r requirements.txt
   ```

5. **Zodiac Data File**: The project includes a `zodiac_data.csv` file in the root directory, which contains the necessary zodiac descriptions and characteristics.

## Running the Application

To run the Streamlit application, use the following command in your terminal:

```bash
streamlit run app.py
```

## Running the Jupyter Notebook

To run the `zodiac_analysis_app.ipynb` notebook:

1. **Install Jupyter Notebook** (if not already installed):

   ```bash
   pip install notebook
   ```

2. **Launch Jupyter Notebook**:

   ```bash
   jupyter notebook
   ```

3. **Open the Notebook**: In the Jupyter interface, navigate to the project directory and open `zodiac_analysis_app.ipynb`.

4. **Run the Cells**: Execute each cell in the notebook sequentially to perform zodiac analysis, generate names, and analyze sentiments.

## Usage Instructions

1. Open the application in your web browser.
2. Enter your date of birth and select your gender.
3. Click on "Generate Zodiac Sign" to find your zodiac sign.
4. Use the buttons to generate a name based on your zodiac sign and to perform sentiment analysis on the zodiac description.

## About

This app aims to provide users with a deeper understanding of astrology through AI-powered insights. The integration of LLaMA 2 allows for unique name generation and description generation based on traditional astrological concepts.

## Acknowledgements

- Special thanks to the creators of the libraries and models used in this application.