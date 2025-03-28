import streamlit as st
import speech_recognition as sr
import webbrowser
import datetime
import wikipedia
import pyttsx3

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            return "Timeout: No speech detected."
        except sr.UnknownValueError:
            return "Could not understand the audio."
        except sr.RequestError:
            return "Could not request results. Check your internet connection."

def speak(audio):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    engine.runAndWait()

def tell_day():
    day_dict = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
                4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    day_of_week = day_dict[datetime.datetime.today().weekday()]
    return f"The day is {day_of_week}."

def tell_time():
    now = datetime.datetime.now()
    return f"The time is {now.strftime('%I:%M %p')}."

def process_command(command):
    command = command.lower()
    if "open google" in command:
        webbrowser.open("https://www.google.com")
        return "Opening Google."
    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        return "Opening YouTube."
    elif "which day it is" in command:
        return tell_day()
    elif "tell me the time" in command:
        return tell_time()
    elif "from wikipedia" in command:
        speak("Checking Wikipedia.")
        query = command.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia: {result}"
    elif "tell me your name" in command:
        return "I am Jarvis, your virtual assistant."
    elif "bye" in command:
        return "Goodbye!"
    return "Command not recognized."

st.title("Voice Assistant with Streamlit")
st.write("Click the button below and speak your command.")

if st.button("Start Listening"):
    user_command = recognize_speech()
    st.write("**You said:**", user_command)
    response = process_command(user_command)
    st.write("**Response:**", response)
    speak(response)
