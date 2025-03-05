import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import requests
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# OpenWeatherMap API key
API_KEY = "112a21bb6f903d4ead1d19f6fd278a74"

# Paths to icons
ICON_PATH = "D:/Git and Github/ShulaTech_Solutions/Project 1-Weather App/weather_icon.png"
FAVICON_PATH = "D:/Git and Github/ShulaTech_Solutions/Project 1-Weather App/Weather favicon.ico"

# Colors
BG_COLOR = "#1E1E2F"
TEXT_COLOR = "#EAEAEA"
BUTTON_COLOR = "#007ACC"
ACCENT_COLOR = "#4CAF50"


# Function to fetch real-time weather data
def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showerror("Error", "Please enter a city name!")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        messagebox.showerror("Error", "City not found! Please enter a valid city name.")
        return

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    weather = data["weather"][0]["description"]

    weather_info = f"Temperature: {temp}°C\nHumidity: {humidity}%\nCondition: {weather.capitalize()}"
    weather_label.config(text=weather_info)

    get_forecast(city)


# Function to fetch and display 7-day forecast with Matplotlib
def get_forecast(city):
    forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)
    data = response.json()

    if data.get("cod") != "200":
        messagebox.showerror("Error", "Unable to fetch forecast data.")
        return

    daily_temps = {}
    daily_labels = []

    for entry in data["list"]:
        date = entry["dt_txt"].split(" ")[0]
        temp = entry["main"]["temp"]

        if date not in daily_temps:
            daily_temps[date] = temp
            daily_labels.append(date)

        if len(daily_temps) == 7:
            break

    plot_forecast(daily_labels, list(daily_temps.values()))


# Function to plot the forecast
def plot_forecast(dates, temps):
    for widget in forecast_frame.winfo_children():
        widget.destroy()

    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    ax.plot(dates, temps, marker='o', linestyle='-', color=ACCENT_COLOR, linewidth=2)
    ax.set_title("7-Day Temperature Forecast", fontsize=14, color=TEXT_COLOR, pad=15)
    ax.set_xlabel("Date", fontsize=12, color=TEXT_COLOR)
    ax.set_ylabel("Temperature (°C)", fontsize=12, color=TEXT_COLOR)
    ax.tick_params(axis='x', rotation=45, labelcolor=TEXT_COLOR)
    ax.tick_params(axis='y', labelcolor=TEXT_COLOR)
    fig.patch.set_facecolor(BG_COLOR)
    ax.set_facecolor("#2A2A3D")

    chart = FigureCanvasTkAgg(fig, master=forecast_frame)
    chart.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    chart.draw()


# GUI Setup
root = tk.Tk()
root.title("Weather App")
root.geometry("900x500")
root.configure(bg=BG_COLOR)
root.iconbitmap(FAVICON_PATH)

# Layout frames
main_frame = tk.Frame(root, bg=BG_COLOR)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

left_frame = tk.Frame(main_frame, bg=BG_COLOR)
left_frame.pack(side="left", padx=20, fill="y")

right_frame = tk.Frame(main_frame, bg=BG_COLOR)
right_frame.pack(side="right", padx=20, fill="both", expand=True)

# Weather Icon
try:
    icon_img = Image.open(ICON_PATH).resize((80, 80), Image.LANCZOS)
    icon_photo = ImageTk.PhotoImage(icon_img)
    tk.Label(left_frame, image=icon_photo, bg=BG_COLOR).pack(pady=5)
except Exception as e:
    print(f"Error loading icon: {e}")

# Title
tk.Label(left_frame, text="Weather Forecast", font=("Arial", 22, "bold"), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=15)

# City Entry
city_entry = tk.Entry(left_frame, font=("Arial", 16), width=25, relief="solid", bd=2)
city_entry.pack(pady=10)

# Get Weather Button
tk.Button(left_frame, text="Get Weather", font=("Arial", 14, "bold"), bg=BUTTON_COLOR, fg="white",
          relief="raised", bd=3, padx=10, pady=5, command=get_weather).pack(pady=15)

# Weather Details
weather_label = tk.Label(left_frame, text="", font=("Arial", 14), bg=BG_COLOR, fg=TEXT_COLOR, justify="left")
weather_label.pack(pady=10)

# Forecast Frame for Matplotlib chart
forecast_frame = tk.Frame(right_frame, bg=BG_COLOR)
forecast_frame.pack(fill="both", expand=True)

root.mainloop()