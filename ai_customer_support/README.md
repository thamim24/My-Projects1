# AI Customer Support Project

## Overview

This project is an AI customer support application built using the Ollama library and Streamlit. The application aims to provide fast and efficient customer support solutions by leveraging Llama 2 models. 

## Features

- Fast response times for customer inquiries.
- User-friendly interface using Streamlit.
- Support for various customer queries.

## Technologies Used

- **Python**: The programming language used for the project.
- **Ollama**: A library for working with AI models, particularly Llama 2.
- **Streamlit**: A framework for building web applications quickly and easily.
- **Torch**: A deep learning framework used in the backend for model processing.
- **Faker**: A library for generating fake data for testing.

## Installation Instructions

Follow the steps below to set up the project on your local machine.

### Prerequisites

- Ensure you have [Anaconda](https://www.anaconda.com/products/distribution) installed.
- Ensure you have Python (preferably version 3.8 or later) installed.
- Ensure you have downloaded and instaalled [Ollama](https://ollama.com/download)

### Step 1: Clone the Repository

1. **Download the ZIP File:**
   Download the project ZIP file from the repository or location where it's hosted.

2. **Extract the ZIP File:**
   Unzip the downloaded file to a directory of your choice.

3. **Navigate to the Project Directory in Anaconda Prompt:**

```bash
cd ai_customer_support
```

### Step 2: Create a Conda Environment

Create a new Conda environment and download the llama 2 model and test in Anaconda Prompt:

```bash
conda create --name ollama python
conda activate --name
ollama pull llama2:latest
ollama run llama2:latest
```

### Step 3: Install Required Packages

Install the required packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

Once the installation is complete, you can run the application using:

```bash
streamlit run llm_app.py
```

## Usage

After running the application, it will be accessible in your web browser at `http://localhost:8501`. You can start interacting with the AI customer support features.


## Acknowledgments

- Thanks to the developers of [Ollama](https://ollama.com/) and [Streamlit](https://streamlit.io/) for their amazing frameworks and tools.
