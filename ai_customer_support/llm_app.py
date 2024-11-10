import streamlit as st
import ollama
import torch
import json
from faker import Faker
from datetime import datetime, timedelta
import random
import os

# Set page configuration (must be the first Streamlit command)
st.set_page_config(page_title="AI-Based Customer Support for Small Businesses", page_icon="🏪", layout="wide")

# Define internal CSS styles
css = """
<style>
/* General Styles */
body {
    font-family: 'Roboto', sans-serif;
    background-color: #f7f7f7;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 600;
    color: #333;
}

button {
    background-color: #007bff;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    font-size: 16px;
    transition: background-color 0.3s;
}

button:hover {
    background-color: #0056b3;
}

/* Chatbox Styles */
.st-chat {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

.st-chat-message {
    background-color: #e9ecef;
    border-radius: 15px;
    padding: 12px 20px;
    margin-bottom: 10px;
    display: inline-block;
    max-width: 80%;
}

.st-chat-message.user {
    background-color: #007bff;
    color: white;
    float: right;
}

.st-chat-message.assistant {
    background-color: #f8f9fa;
    color: #333;
}

/* Sidebar Styles */
.st-sidebar {
    background-color: #ffffff;
    box-shadow: 0 0 15px rgba(0, 0, 0, 0.05);
    padding: 20px;
    border-radius: 8px;
}

.st-sidebar h2 {
    color: #007bff;
    font-size: 22px;
}

.st-sidebar p {
    font-size: 16px;
    color: #666;
}

/* Input Box */
.st-chat-input input {
    border: 2px solid #007bff;
    border-radius: 8px;
    padding: 10px;
    font-size: 16px;
    width: 100%;
}

.st-chat-input button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 16px;
}

/* Header */
header {
    text-align: center;
    margin-bottom: 20px;
}

header h1 {
    color: #007bff;
    font-size: 36px;
    font-weight: 700;
}

header h1 span {
    color: #ff9800;
}

/* Reset button */
.st-button {
    margin-top: 10px;
}

.st-button button {
    background-color: #ff4b4b;
    color: white;
    border-radius: 8px;
    padding: 8px 16px;
    font-size: 14px;
}

.st-button button:hover {
    background-color: #c42c2c;
}

</style>
"""

# Load and apply the internal CSS
st.markdown(css, unsafe_allow_html=True)

# The rest of your code continues here
st.title("🤖 AI-Based Customer Support for Small Businesses")

# Load business-specific data
@st.cache_data
def load_business_data():
    fake = Faker()
    
    # Generate products
    products = []
    categories = ["Electronics", "Home & Garden", "Fashion", "Books", "Sports & Outdoors"]
    for _ in range(20):
        category = random.choice(categories)
        product_name = f"{fake.word().capitalize()} {fake.random_element(['Pro', 'Ultra', 'Lite', 'Max', 'Elite'])}"
        products.append({
            "name": product_name,
            "category": category,
            "price": round(random.uniform(9.99, 199.99), 2),
            "description": fake.sentence(),
            "sku": fake.ean(length=8),
            "in_stock": random.choice([True, False])
        })
    
    # Generate FAQs
    faqs = [
        {"question": "What are your business hours?", "answer": "We're open Monday to Friday, 9 AM to 6 PM, and Saturday 10 AM to 4 PM."},
        {"question": "Do you offer refunds?", "answer": "Yes, we offer refunds within 30 days of purchase for unused items in original condition."},
        {"question": "How can I track my order?", "answer": "You can track your order by logging into your account or using the tracking number sent to your email."},
        {"question": "Do you ship internationally?", "answer": "Yes, we ship to most countries. International shipping rates apply."},
        {"question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and Apple Pay."},
        {"question": "How long does shipping usually take?", "answer": "Domestic shipping typically takes 3-5 business days. International shipping can take 7-14 business days."},
        {"question": "Do you offer gift wrapping?", "answer": "Yes, we offer gift wrapping for a small additional fee. You can select this option at checkout."},
        {"question": "What is your return policy?", "answer": "You can return items within 30 days of purchase. Items must be unused and in original packaging."},
        {"question": "Do you have a physical store?", "answer": "Yes, we have a flagship store located at 123 Main St, Anytown, USA. You can also shop online."},
        {"question": "How can I contact customer support?", "answer": "You can reach our customer support team via email at support@ourbusiness.com or by phone at 1-800-123-4567."}
    ]
    
    # Generate booking slots for the next 7 days
    booking_slots = []
    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        for hour in range(9, 18):  # 9 AM to 5 PM
            if random.random() > 0.3:  # 70% chance of slot being available
                slot = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                booking_slots.append(slot.strftime("%Y-%m-%d %I:%M %p"))
    
    # Generate services
    services = [
        {"name": "Basic Consultation", "duration": "30 minutes", "price": 50},
        {"name": "Advanced Troubleshooting", "duration": "1 hour", "price": 100},
        {"name": "Custom Solution Design", "duration": "2 hours", "price": 200},
        {"name": "Emergency Support", "duration": "Varies", "price": "150/hour"},
        {"name": "Software Installation", "duration": "1 hour", "price": 75},
    ]
    
    return {
        "products": products,
        "faqs": faqs,
        "booking_slots": booking_slots,
        "services": services
    }

business_data = load_business_data()

# Initialize session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "model" not in st.session_state:
    st.session_state["model"] = ""

# Model selection
models = [model["name"] for model in ollama.list()["models"] if "llama" in model["name"].lower()]
st.session_state["model"] = st.selectbox("Choose your LLaMA model", models)

def model_res_generator(prompt):
    # Use a separate thread to handle long-running tasks for non-blocking UI
    if torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    # Prepare the system message with business context
    system_message = f"""You are an AI assistant for a small business. Use the following information to assist customers:
    Products: {json.dumps(business_data['products'])}
    FAQs: {json.dumps(business_data['faqs'])}
    Available Booking Slots: {json.dumps(business_data['booking_slots'])}
    
    Provide helpful, concise responses. For bookings, confirm available slots. For product inquiries, give accurate information."""

    messages = [
        {"role": "system", "content": system_message},
        *st.session_state["messages"],
        {"role": "user", "content": prompt}
    ]

    # Stream response
    try:
        stream = ollama.chat(
            model=st.session_state["model"],
            messages=messages,
            stream=True,
        )
        response = ""
        for chunk in stream:
            response += chunk["message"]["content"]
            yield response
    except Exception as e:
        yield f"Error: {str(e)}"  # Handle any errors gracefully


# Sidebar for business info
with st.sidebar:
    st.header("Business Information")
    st.write("Welcome to our AI-powered customer support!")
    st.write("We can help you with:")
    st.write("- Product information")
    st.write("- Booking appointments")
    st.write("- Answering common questions")
    st.write("- And more!")

# Main chat interface
st.header("Chat with our AI Support")

# Display chat messages from history on app rerun
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I assist you today?"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for chunk in model_res_generator(prompt):
            full_response = chunk  # Show the entire chunk at once for faster perception
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    st.session_state["messages"].append({"role": "assistant", "content": full_response})

# Reset conversation button
if st.button("Start New Conversation"):
    st.session_state["messages"] = []
    st.experimental_rerun()
