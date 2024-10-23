# app.py

import streamlit as st
import chit_chat
import qna
import chat_history  # Import the chat history module
import weather  # Import the weather module

# Set up the home page configuration
st.set_page_config(page_title="TrioTalk", layout="wide")

# Sidebar navigation options as a selectbox (scrollable)
st.sidebar.title("Navigation")
options = st.sidebar.selectbox("Select a page", ("Home", "Chit-Chat", "Q&A", "Weather", "Chat History"))  # Added Weather

# Function to show the home page with intro
def show_home_page():
    st.title("Welcome to **TrioTalk**!")
    
    st.markdown(
        """
        TrioTalk is your all-in-one conversational AI platform, designed to assist you with a variety of tasks. 
        Whether you want to have a casual conversation, seek answers to your questions, or check the latest weather updates, 
        TrioTalk has you covered!

        ### Choose from the following options:
        - **Chit-Chat**: Engage in light-hearted conversations with **ChitChat Buddy**.
        - **Q&A**: Get reliable answers with **QueryMaster**.
        - **Weather**: Stay updated on the latest weather conditions with **SkyBuddy**.

        Select an option from the left sidebar to get started!
        """
    )

# Introductions for the chatbots
def show_chatbot_intros():
    st.subheader("Meet Our Chatbots")
    st.markdown(
        """
        ### 🤖 ChitChat Buddy
        ChitChat Buddy is your friendly conversational companion! 
        Whether you're feeling chatty or just want to pass the time, 
        this chatbot is here to engage you in fun and light-hearted discussions.

        ### ❓ QueryMaster
        QueryMaster is your go-to assistant for all your questions!
        Ask anything from general knowledge to specific queries, 
        and get informative answers quickly and efficiently.

        ### ☁️ SkyBuddy
        SkyBuddy is your personal weather assistant!
        With accurate and up-to-date weather information, 
        it helps you plan your day, whether it’s sunny, rainy, or anything in between.
        """
    )

# Display the appropriate page based on sidebar selection
if options == "Home":
    show_home_page()
    show_chatbot_intros()  # Display chatbot introductions
elif options == "Chit-Chat":
    chit_chat.show_chit_chat_page()
elif options == "Q&A":
    qna.show_qa_page()
elif options == "Weather":  # Display weather page
    weather.show_weather_page()  # Call the weather page function
elif options == "Chat History":  # Display chat history page
    chat_history.show_chat_history_page()
