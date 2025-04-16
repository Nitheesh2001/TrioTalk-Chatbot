# qna.py

import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Gemini API with the provided API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get chat responses
model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(message):
    # Construct a structured prompt for the Gemini model
    structured_prompt = f"You are an intelligent assistant named QueryMaster. Respond to the following question: {message}"
    response = chat.send_message(structured_prompt, stream=True)
    return response

def show_qa_page():
    st.subheader("Ask Your Questions to QueryMaster")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # User input for questions
    input_text = st.text_input("Input: ", key="input_qa")
    submit_qa = st.button("Ask the question")

    if submit_qa and input_text:
        # Get the response from the Gemini model for Q&A
        response = get_gemini_response(input_text)

        # Collect the bot's response
        response_text = ""
        for chunk in response:
            response_text += chunk.text  # Collect the bot's response

        # Add user query and bot's response to chat history in the correct order
        st.session_state['chat_history'].append(("You", input_text))  # User input first
        st.session_state['chat_history'].append(("Bot", response_text))  # Then bot response

        # Display the latest user input and bot response prominently
        st.markdown(
            f"""
            <div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                <b style='color: #000000;'>You:</b> <span style='color: #000000;'>{input_text}</span>
            </div>
            <div style='background-color: #f8d7da; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>
                <b style='color: #000000;'>Bot:</b> <span style='color: #000000;'>{response_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Display chat history
    if st.session_state['chat_history']:
        st.markdown("<hr>", unsafe_allow_html=True)
        for sender, message in st.session_state['chat_history']:
            if sender == "You":
                st.markdown(
                    f"<div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 5px;'><b style='color: #000000;'>You:</b> <span style='color: #000000;'>{message}</span></div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color: #f8d7da; border-radius: 10px; padding: 10px; margin-bottom: 5px;'><b style='color: #000000;'>Bot:</b> <span style='color: #000000;'>{message}</span></div>",
                    unsafe_allow_html=True
                )
