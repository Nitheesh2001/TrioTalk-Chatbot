# chit_chat.py

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API with the provided API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get chat responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(message):
    response = chat.send_message(message, stream=True)
    return response

def show_chit_chat_page():
    st.subheader("Chit-Chat with ChitChat Buddy")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # User input for chit-chat
    user_input = st.text_input("You: ", key="input")
    submit = st.button("Send")

    if submit and user_input:
        # Get the response from the Gemini model for chit-chat
        response = get_gemini_response(user_input)

        # Add user input to session state chat history
        st.session_state['chat_history'].append(("You", user_input))

        # Collect the bot's response
        response_text = ""
        for chunk in response:
            response_text += chunk.text  # Collect the bot's response
        
        # Add bot's response to chat history
        st.session_state['chat_history'].append(("Bot", response_text))

        # Display the latest user input and bot response prominently
        st.markdown(
            f"""
            <div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                <b style='color: #000000;'>You:</b> <span style='color: #000000;'>{user_input}</span>
            </div>
            <div style='background-color: #f8d7da; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                <b style='color: #000000;'>Bot:</b> <span style='color: #000000;'>{response_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
