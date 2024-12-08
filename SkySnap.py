import streamlit as st
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
import threading
import time

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
        st.success(f"Email sent to {receiver_email} successfully!")
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

# Format Weather Report
def format_weather_report(location, weather_data):
    sunrise = datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S')
    sunset = datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S')
    wind_speed = round(weather_data['wind']['speed'] * 3.6, 2)
    description = weather_data['weather'][0]['description']

    return f"""
    Weather in {location}:
    Current Temperature: {weather_data['main']['temp']}°C
    Feels Like: {weather_data['main']['feels_like']}°C
    Description: {description}
    Sunrise: {sunrise}
    Sunset: {sunset}
    Wind Speed: {wind_speed} kph
    Lifestyle Tips: {"Carry an umbrella!" if "rain" in description.lower() else "Enjoy your day!"}
    """

# Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Schedule Daily Email
def schedule_daily_email(receiver_email, location, time, weather_api_key, lat, lng):
    def send_daily_weather():
        weather_data = get_weather(weather_api_key, lat, lng)
        if weather_data:
            weather_report = format_weather_report(location, weather_data)
            send_email(receiver_email, f"Daily Weather Update for {location}", weather_report)

    scheduler.add_job(
        send_daily_weather,
        'cron',
        hour=time.hour,
        minute=time.minute,
        id=f"daily_email_{receiver_email}",
        replace_existing=True
    )

# Start Rain Alert Monitoring
def start_rain_alert_monitoring(receiver_email, location, weather_api_key, lat, lng):
    def monitor_rain():
        while True:
            weather_data = get_weather(weather_api_key, lat, lng)
            if weather_data and "rain" in weather_data['weather'][0]['description'].lower():
                weather_report = format_weather_report(location, weather_data)
                send_email(receiver_email, f"Rain Alert for {location}", weather_report)
                time.sleep(3600)  # Wait 1 hour before checking again
            else:
                time.sleep(3600)  # Wait 1 hour before re-checking

    threading.Thread(target=monitor_rain, daemon=True).start()

# Main App
st.image("C:/Users/Praveen/OneDrive/Pictures/76818-forecasting-material-rain-shower-weather-icon.png", width=400)
st.title("SkySnap")
st.caption("SkySnap is your personalized weather assistant, providing real-time weather information and forecasts.")

# User Registration
email_time = st.sidebar.time_input("Select time for daily updates", value=datetime(2024, 1, 1, 8, 0).time())
st.sidebar.title("User Registration")
user_name = st.sidebar.text_input("Enter your name")
user_email = st.sidebar.text_input("Enter your email")
dob = st.sidebar.date_input("Enter your Date of Birth")
photo = st.sidebar.file_uploader("Upload your photo")
preference = st.sidebar.radio("How would you like to receive updates?", ["Daily Updates", "Rain Alerts"])

if st.sidebar.button("Register"):
    if user_name and user_email and preference:
        location = st.text_input("Enter a location in India:")
        if location:
            coords = get_coordinates(geocode_api_key, location)
            if coords:
                lat, lng = coords
                st.success(f"Welcome, {user_name}! You will receive {preference.lower()} at {user_email}.")

                if preference == "Daily Updates":
                    schedule_daily_email(user_email, location, email_time, weather_api_key, lat, lng)
                    st.info(f"Your daily updates are scheduled for {email_time.strftime('%H:%M')}.")

                elif preference == "Rain Alerts":
                    start_rain_alert_monitoring(user_email, location, weather_api_key, lat, lng)
                    st.info("Rain alerts monitoring has been activated. You'll be notified if it rains.")
            else:
                st.error("Could not retrieve location coordinates. Please try again.")
        else:
            st.error("Please enter a valid location to complete registration.")
    else:
        st.error("Please fill in all fields to complete your registration.")

