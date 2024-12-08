import streamlit as st
import requests
from datetime import datetime

st.image("C:/Users/Praveen/OneDrive/Pictures/76818-forecasting-material-rain-shower-weather-icon.png",width=400)
st.title("SKySnap")
st.caption(" Sky Snap is weather assistant provides up-to-date weather information at your fingertips. With a user-friendly interface Sky Snap delivers real-time weather conditions and detailed forecasts for any location in India")
st.sidebar.title("Create your Profile ")
st.sidebar.text_input("Enter your name")
st.sidebar.date_input("Enter ur Date of Birth")
st.sidebar.file_uploader(" Drop your photo to create a profile  ")
st.sidebar.select_slider(" Rate the application", ["Bad" , " Good" , " Excellent"])
st.sidebar.button("submit")
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

def get_forecast(api_key, lat, lng):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = f"{base_url}lat={lat}&lon={lng}&appid={api_key}&units=metric"

    response = requests.get(complete_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error retrieving forecast data. Please try again.")
        return None

def get_lifestyle_tips(weather_description):
    tips = {
        'clear sky': "It's a beautiful day! Enjoy outdoor activities.",
        'few clouds': "A nice day for a walk or a picnic.",
        'scattered clouds': "Might be a bit cloudy, but still great for outdoor plans!",
        'broken clouds': "Consider carrying a light jacket.",
        'shower rain': "Don't forget your umbrella!",
        'rain': "Stay dry and enjoy a cozy day inside.",
        'thunderstorm': "Stay safe indoors until the storm passes.",
        'snow': "Bundle up and enjoy the winter wonderland!",
        'mist': "Drive carefully and keep an eye on visibility."
    }
    return tips.get(weather_description.lower(), "No specific tips available.")

def display_weather(current_weather):
    st.header(f"Weather in {current_weather['location']}")
    st.subheader(f"Current Temperature: {current_weather['temp']}°C")
    st.write(f"Feels Like: {current_weather['feels_like']}°C")
    st.write(f"Description: {current_weather['description']}")
    st.write(f"Sunrise: {current_weather['sunrise']}")
    st.write(f"Sunset: {current_weather['sunset']}")
    st.write(f"Wind Speed: {current_weather['wind_speed']} kph")
    st.write(f"Lifestyle Tips: {current_weather['tips']}")

def display_forecast(forecast_data):
    st.header("5-Day Forecast")
    for day in forecast_data:
        st.write(f"{day['date']}: {day['temp']}°C, {day['description']}")

def main():
    weather_api_key = "18102c3a12c5ac5cecf4b5216f95cbf2" 
    geocode_api_key = "894a11aadc014e3aa5c8efeb2de6102f"

    location = st.text_input("Enter a location in India:")

    if location:
        coords = get_coordinates(geocode_api_key, location)
        if coords:
            lat, lng = coords

            weather_data = get_weather(weather_api_key, lat, lng)
            if weather_data:
                current_weather = {
                    'location': location,
                    'temp':weather_data['main']['temp'],
                    'feels_like': weather_data['main']['feels_like'],
                    'description': weather_data['weather'][0]['description'],
                    'sunrise': datetime.fromtimestamp(weather_data['sys']['sunrise']).strftime('%H:%M:%S'),
                    'sunset': datetime.fromtimestamp(weather_data['sys']['sunset']).strftime('%H:%M:%S'),
                    'wind_speed': round(weather_data['wind']['speed'] * 3.6, 2),  
                    'tips': get_lifestyle_tips(weather_data['weather'][0]['description'])
                }

                display_weather(current_weather)

                show_forecast = st.checkbox("Show 5-day Forecast")
                if show_forecast:
                    forecast_data = get_forecast(weather_api_key, lat, lng)
                    if forecast_data:
                        forecast_list = []
                        for entry in forecast_data['list'][::8]:  
                            date = datetime.fromtimestamp(entry['dt']).strftime('%Y-%m-%d')
                            temp = entry['main']['temp']
                            description = entry['weather'][0]['description']
                            forecast_list.append({'date': date, 'temp': temp, 'description': description})

                        display_forecast(forecast_list)

if __name__ == "__main__":
    main()


import smtplib
from email.mime.text import MIMEText

# Email sender and receiver details
sender_email = "skysnapalert@gmail.com"
receiver_email = "kalyansagar7008@gmail.com"
password = "qudl wqwk vdei aled"

# Email content
subject = "Work Done"
body = ""

# Create the MIMEText object
message = MIMEText(body, "plain")
message["Subject"] = subject
message["From"] = sender_email
message["To"] = receiver_email

# Connect to the SMTP server and send the email
try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()  # Secure the connection
        server.login(sender_email, password)  # Login to your email account
        server.sendmail(sender_email, receiver_email, message.as_string())  # Send the email
        print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email: {e}")

