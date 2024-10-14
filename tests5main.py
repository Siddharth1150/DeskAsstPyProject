import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yt_dlp
import json

# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"Cortana: {text}")  # Debugging statement
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your virtual assistant. How can I help you today?")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Working On...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
    except Exception:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    return query.lower()


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('siddharthsingh1150@gmail.com', 'oavw barp qmuv ghjx')
    server.sendmail('siddharthsingh1150@gmail.com', to, content)
    server.close()

def play_song_on_youtube(song_name):
    ydl_opts = {
        'format': 'best',
        'noplaylist': True,
        'quiet': True,
        'default_search': 'ytsearch1',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(song_name, download=False)
        video_url = result['entries'][0]['webpage_url']
        webbrowser.open(video_url)
        speak(f'Playing {result["entries"][0]["title"]}')

if __name__ == "__main__":
    wishMe()
    running = True
    while running:
        query = takeCommand()
        if query:
            if 'open' in query:
                if 'youtube' in query:
                    speak("Opening YouTube...")
                    webbrowser.open("https://www.youtube.com")
                elif 'wikipedia' in query:
                    speak("Opening Wikipedia...")
                    webbrowser.open("https://www.wikipedia.com")
                elif 'google' in query:
                    speak("Opening Google...")
                    webbrowser.open("https://www.google.com")
                # Add more commands here
                elif 'open erp portal' in query:
                    speak("Opening erp portal...")
                    webbrowser.open("https://erp.psit.ac.in/Student/")

            elif 'play a song' in query: 
                speak('Which song would you like to listen to?')
                song_name = takeCommand()
                if song_name:
                    play_song_on_youtube(song_name)

            elif 'wikipedia' in query:
                speak('Searching Wikipedia...')
                query = query.replace('wikipedia', '')
                try:
                    results = wikipedia.summary(query, sentences=2)
                    speak("According to Wikipedia")
                    speak(results)
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any results.")
                except Exception as e:
                    speak("An error occurred while searching Wikipedia.")

            elif 'play music' in query:
                music_dir = 'D:\\songs'
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                    speak("Playing your music.")
                else:
                    speak("No songs found in the directory.")

            elif 'can you please tell me time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"The time is {strTime}")

            elif 'open code' in query:
                codePath = "C:\\Users\\siddh\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Visual Studio Code"
                os.startfile(codePath)
                speak("Opening Visual Studio Code.")

            elif 'send an email to me' in query:
                try:
                    speak("What should I say?")
                    content = takeCommand()
                    to = "siddharthsingh1150@gmail.com"    
                    sendEmail(to, content)
                    speak("Email has been sent!")
                    
                except Exception as e:
                    print(e)
                    speak("Sorry my friend . I am not able to send this email")
                    

            elif 'exit' in query:
                speak('Goodbye! Have a great day.')
                running = False
