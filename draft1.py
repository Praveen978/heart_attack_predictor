import streamlit as st
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# Email Configuration
SENDER_EMAIL = "skysnapalert@gmail.com"
PASSWORD = "qudl wqwk vdei aled"

# Functions to send email
def send_email(receiver_email, subject, body):
    try:
        message = MIMEText(body, "plain")
        message["Subject"] = subject
        message["From"] = SENDER_EMAIL
        message["To"] = receiver_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()  # Secure the connection
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, message.as_string())
        st.success("Email sent successfully!")
    except Exception as e:
        st.error(f"Failed to send email: {e}")

# Weather API Functions
def get_coordinates(api_key, location):
    base_url = "https://api.opencagedata.com/geocode/v1/json"
    complete_url = f"{base_url}?q={location},India&key={api_key}"
    response = requests.get(complete_url)
    data = response.json()
    if response.status_code == 200 and data['results']:
        lat = data['results'][0]['geometry']['lat']
        lng = data['results'][0]['geometry']['lng']
        return lat, lng
    else:
        st.error("Error retrieving coordinates. Please try again.")
        return None

def get_weather(api_key, lat, lng):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}lat={lat}&lon={lng}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error retrieving weather data. Please try again.")
        return None

# Display Weather Details
def display_weather(current_weather):
    st.header(f"Weather in {current_weather['location']}")
    st.subheader(f"Current Temperature: {current_weather['temp']}°C")
    st.write(f"Feels Like: {current_weather['feels_like']}°C")
    st.write(f"Description: {current_weather['description']}")
    st.write(f"Sunrise: {current_weather['sunrise']}")
    st.write(f"Sunset: {current_weather['sunset']}")
    st.write(f"Wind Speed: {current_weather['wind_speed']} kph")
    st.write(f"Lifestyle Tips: {current_weather['tips']}")
    return f"""
    Weather in {current_weather['location']}:
    Current Temperature: {current_weather['temp']}°C
    Feels Like: {current_weather['feels_like']}°C
    Description: {current_weather['description']}
    Sunrise: {current_weather['sunrise']}
    Sunset: {current_weather['sunset']}
    Wind Speed: {current_weather['wind_speed']} kph
    Lifestyle Tips: {current_weather['tips']}
    """

# Main App
st.image("C:/Users/Praveen/OneDrive/Pictures/76818-forecasting-material-rain-shower-weather-icon.png", width=400)
st.title("SkySnap")
st.caption("SkySnap is a weather assistant providing up-to-date weather information at your fingertips. Deliver real-time conditions and detailed forecasts for any location in India.")

# Sidebar
st.sidebar.title("User Options")
receiver_email = st.sidebar.text_input("Enter email to receive weather updates")
location = st.text_input("Enter a location in India:")

# Weather API Keys
weather_api_key = "18102c3a12c5ac5cecf4b5216f95cbf2"
geocode_api_key = "894a11aadc014e3aa5c8efeb2de6102f"

if location:
    coords = get_coordinates(geocode_api_key, location)
    if coords:
        lat, lng = coords
        weather_data = get_weather(weather_api_key, lat, lng)
        if weather_data:
            current_weather = {
                'location': location,
                'temp': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'description': weather_data['weather'][0]['description'],
                'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S'),
                'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S'),
                'wind_speed': round(weather_data['wind']['speed'] * 3.6, 2),
                'tips': "Enjoy your day!"  # Simple tip
            }

            weather_report = display_weather(current_weather)

            # Email the weather details if email is provided
            if receiver_email:
                if st.button("Send Weather Report via Email"):
                    send_email(receiver_email, f"Weather Update for {location}", weather_report)
