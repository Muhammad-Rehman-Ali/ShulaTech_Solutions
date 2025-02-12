import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests

# OpenWeatherMap API key
API_KEY = "112a21bb6f903d4ead1d19f6fd278a74"

# Function to fetch real-time weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    # API URL for current weather
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        messagebox.showerror("Error", "City not found! Please enter a valid city name.")
        return

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]

    weather_info = f" Temperature: {temp}°C\n Humidity: {humidity}%\n Condition: {weather.capitalize()}"
    weather_label.config(text=weather_info)

    # Fetch and display 7-day forecast using the free API
    get_forecast(city)

# Function to fetch 7-day forecast
def get_forecast(city):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    data = response.json()

    if data.get("cod") != "200":
        messagebox.showerror("Error", "Unable to fetch forecast data.")
        return

    forecast_data = ""
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    daily_temps = {}

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]  # Extract date
        temp = entry["main"]["temp"]
        condition = entry["weather"][0]["description"]

        if date not in daily_temps:
            daily_temps[date] = (temp, condition)

    # Format forecast for display
    for i, (date, (temp, condition)) in enumerate(daily_temps.items()):
        forecast_data += f"{days[i % 7]}: {temp}°C, {condition.capitalize()}\n"

    forecast_label.config(text=forecast_data)

# GUI Setup
# Initialize the main window
root = tk.Tk()
root.title("Weather App")
root.geometry("400x560")
root.configure(bg="#2C3E50")
root.iconbitmap('Weather favicon.ico')

try:
    icon = Image.open("weather_icon.png")
    icon = icon.resize((100, 100), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon)
    icon_label = tk.Label(root, image=icon_photo, bg="#2C3E50")
    icon_label.pack(pady=10)
except Exception as e:
    print(f"Error loading icon: {e}")

# Title Label
tk.Label(root, text="Weather Forecast", font=("Arial", 20, "bold"), bg="#2C3E50", fg="white").pack(pady=10)

# City Input Field
city_entry = tk.Entry(root, font=("Arial", 14), bg="white", fg="black", relief="solid", bd=2, width=25)
city_entry.pack(pady=5)

# Search Button
tk.Button(root, text="Get Weather", font=("Arial", 14, "bold"), bg="#3498DB", fg="white", relief="raised", bd=3,
          padx=10, pady=5, command=get_weather).pack(pady=10)

# Weather Details
weather_label = tk.Label(root, text="", font=("Arial", 14), bg="#2C3E50", fg="white", justify="left", padx=10, pady=5)
weather_label.pack(pady=10)

# Forecast Title
tk.Label(root, text="7-Day Forecast", font=("Arial", 16, "bold"), bg="#2C3E50", fg="#F39C12").pack(pady=5)

# Forecast Data
forecast_label = tk.Label(root, text="", font=("Arial", 12), bg="#2C3E50", fg="white", justify="left", padx=10, pady=5)
forecast_label.pack(pady=5)


root.mainloop()