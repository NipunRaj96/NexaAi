import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from PIL import Image

# Load environment variables
load_dotenv()

# Load the image using Pillow
image_path = r"C:\Users\nipun\Downloads\Screenshot_2024-11-07_200624-removebg-preview.png"
image = Image.open(image_path)

# Configure Streamlit page settings
st.set_page_config(
    page_title="NexaAI!",
    page_icon=image,  # Use the image object as the page icon
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    return "assistant" if user_role == "model" else user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("NexaAI - AI Powered Conversations")

# Persistent introduction message for Nexa
def display_nexa_intro():
    intro_text = (
        "Hey there! I'm Nexa, your AI buddy crafted by Nipun, a computer science enthusiast from Galgotias University. "
        "Nipun’s got solid skills in Python and Java, and he's a pro in UI/UX design. Curious to see more? "
        "Check out [Nipun's portfolio](https://nipun.framer.website/)! I’m here, powered by the Gemini 1.5 Pro model, "
        "and ready to bring the answers, ideas, or just some good vibes to whatever you’re working on. Let’s dive in!"
    )
    st.info(intro_text)  # Display as an informational banner

# Show introduction once at the top
display_nexa_intro()

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Input field for user's message
user_prompt = st.chat_input("Ask Nexa...")
if user_prompt:
    # Add user's message to chat and display it
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)
    nexa_response = gemini_response.text

    # Display Nexa's response
    with st.chat_message("assistant"):
        st.markdown(nexa_response)
