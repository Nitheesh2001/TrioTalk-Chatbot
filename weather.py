# weather.py

import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Use your API key from the environment variable
weather_api_key = os.getenv("WEATHER_API_KEY")

# Initialize chat history and weather data
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'weather_data' not in st.session_state:
    st.session_state.weather_data = {}

# Function to get weather information
def get_weather(city):
    try:
        complete_api_link = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_api_key}&units=metric"
        api_link = requests.get(complete_api_link)
        api_data = api_link.json()

        if api_link.status_code == 200:
            # Extract weather data
            temp_city = api_data['main']['temp']
            weather_desc = api_data['weather'][0]['description']
            humidity = api_data['main']['humidity']
            wind_speed = api_data['wind']['speed']
            date_time = datetime.now().strftime("%d %b %Y | %I:%M:%S %p")

            # Store weather data for later use
            st.session_state.weather_data = {
                'temp': temp_city,
                'description': weather_desc,
                'humidity': humidity,
                'wind_speed': wind_speed,
                'date_time': date_time
            }

            weather_response = (
                f"**Temperature:** {temp_city:.2f}°C\n"
                f"**Weather Description:** {weather_desc}\n"
                f"**Humidity:** {humidity}%\n"
                f"**Wind Speed:** {wind_speed} m/s\n"
                f"**Date & Time:** {date_time}"
            )
            return weather_response
        else:
            return f"Error: {api_data.get('message', 'Unable to fetch weather data.')}"

    except requests.RequestException as e:
        return f"Request error: {e}"
    except KeyError as e:
        return f"Key error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# Streamlit app interface
def show_weather_page():
    st.title("SkyBuddy")

    # Get user input for city
    user_city = st.text_input("Enter city name for weather:", "")
    if st.button("Get Weather") and user_city:
        with st.spinner("Fetching weather data..."):
            weather_response = get_weather(user_city)
            # Prepend new message to chat history
            st.session_state.chat_history.insert(0, ("You", user_city))
            st.session_state.chat_history.insert(0, ("Bot", weather_response))
            # Display weather response
            st.markdown(f"<div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 10px;'><b style='color: #000000;'>Bot:</b> <span style='color: #000000;'>{weather_response}</span></div>", unsafe_allow_html=True)

    # Chatbot interaction after getting weather
    user_message = st.text_input("Ask me anything about the weather:", "")
    if st.button("Send") and user_message:
        bot_response = generate_response(user_message)
        # Prepend new message to chat history
        st.session_state.chat_history.insert(0, ("You", user_message))
        st.session_state.chat_history.insert(0, ("Bot", bot_response))
        # Display bot response
        st.markdown(f"<div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 10px;'><b style='color: #000000;'>Bot:</b> <span style='color: #000000;'>{bot_response}</span></div>", unsafe_allow_html=True)

# Function to generate chatbot responses based on weather data
def generate_response(user_input):
    # Check if weather data is available
    if not st.session_state.weather_data:
        return "Please provide a city name to get the weather first."

    # Extract data from session state
    temp = st.session_state.weather_data['temp']
    description = st.session_state.weather_data['description']
    humidity = st.session_state.weather_data['humidity']
    wind_speed = st.session_state.weather_data['wind_speed']

    # Simple logic to respond to common questions
    if "temperature" in user_input.lower() and "average" in user_input.lower():
        return f"The current temperature is {temp:.2f}°C. I don't have data for the average temperature."
    elif "temperature" in user_input.lower():
        return f"The current temperature is {temp:.2f}°C."
    elif "weather" in user_input.lower():
        return f"The current weather is {description}."
    elif "humidity" in user_input.lower():
        return f"The humidity is {humidity}%."
    elif "wind" in user_input.lower():
        return f"The wind speed is {wind_speed} m/s."
    elif "thank" in user_input.lower():
        return "You're welcome! Let me know if you need anything else."
    else:
        return "I'm not sure about that. Can you ask something else about the weather?"
