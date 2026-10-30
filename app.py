
import os
import time
from dotenv import load_dotenv
import speech_recognition as sr
from gtts import gTTS
import pygame
import requests

load_dotenv()
api_key = os.getenv("api_key")

def VoiceToText():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... Speak now!")
        try:
            # Calibrate for room noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            voice = recognizer.listen(source)
            print("Processing voice...")
            text = recognizer.recognize_google(voice)
            return text.lower()
        except:
            return None

def text_to_voice(text):
    pygame.mixer.init()
    # lang='en' for standard English output
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("welcome.mp3")
    pygame.mixer.music.load("welcome.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.music.unload()

def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    data = requests.get(url).json()
    if str(data.get("cod")) != "200":
        return None
    description = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]
    return f"The weather in {city} is {description}. The temperature is {temp} degrees Celsius and humidity is {humidity} percent."


# Main Execution
city = VoiceToText()
print("City:", city)

if city:
    weather_text = get_weather(city)
    if weather_text is None:
        weather_text = "Sorry, city not found."
    
    print("Weather Info:", weather_text)
    text_to_voice(weather_text)
else:
    print("Could not capture your voice. Please run again.")