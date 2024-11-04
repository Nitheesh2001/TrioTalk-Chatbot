# weather.py

import streamlit as st
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

# Use your API key from the environment variable
weather_api_key = os.getenv("WEATHER_API_KEY")

# Initialize chat history and weather data if not already set
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

# Function to extract city name from user input using simple keyword matching
def extract_city(user_input):
    # Regular expression to capture place names following 'in' or 'at'
    match = re.search(r"\b(?:in|at)\s+(\w+)", user_input, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        # If no keyword-based match, assume input as direct city name
        return user_input.strip()

# Streamlit app interface
def show_weather_page():
    st.title("SkyBuddy")

    # Get user input for city
    user_city_input = st.text_input("Enter city name or type your request:", "")
    if st.button("Get Weather") and user_city_input:
        city_name = extract_city(user_city_input)
        if city_name:
            with st.spinner("Fetching weather data..."):
                weather_response = get_weather(city_name)
                # Prepend new message to chat history
                st.session_state.chat_history.insert(0, ("You", user_city_input))
                st.session_state.chat_history.insert(0, ("Bot", weather_response))
                # Display weather response
                st.markdown(
                    f"<div style='background-color: #d4edda; border-radius: 10px; padding: 10px; margin-bottom: 10px;'>"
                    f"<b style='color: #000000;'>Bot:</b> <span style='color: #000000;'>{weather_response}</span></div>",
                    unsafe_allow_html=True
                )
        else:
            st.error("Please enter a valid city or place name.")

# Call the weather page function
if __name__ == "__main__":
    show_weather_page()
