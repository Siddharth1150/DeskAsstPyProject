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
import pywhatkit
import re
import logging
from dotenv import load_dotenv
from AppOpener import open
import pywhatkit as pwk
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import requests
from plyer import notification



# Load environment variables from .env file
load_dotenv()


# Initialize the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(text):
    print(f"NOVA : {text}")  # Debugging statement
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


# first_prompt = True

# def get_input():
#     global first_prompt
#     if first_prompt:
#         speak("can I assist you using voice command or text input sir....")
#         choice = input("USER : ")
#         first_prompt = False 

#          # Set the flag to False after the first prompt

#         if choice and 'text' in choice:
#             speak("Please enter your command: ")
#             command = input("USER : ")
#             return command.lower()
#         else:
#             return takeCommand()
#     else:
#         # If it's not the first prompt, just take voice input directly
#         return takeCommand()

def get_input():
    speak("can I assist you using voice command or text input sir....")
    choice = input("USER : ").lower()

    if 'text' in choice:
        speak("Please enter your command... ")
        return input("USER : ").lower()
    elif 'voice' in choice:
        speak("please enter your command...")
        return takeCommand()
    else:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return get_input()

# def get_input():
#     speak("Would you like to use voice command or text input, sir?")
#     choice = input("USER : ")

#     if choice and 'enter text' in choice:
#         speak("Please enter your command.... ")
#         command = input("USER : ")
#         return command.lower()
#     else:
#         return takeCommand()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("NOVA : Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("NOVA : Working On...") 
        query = r.recognize_google(audio, language='en-in')
        print(f"USER SAID : {query}")
    except Exception:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return None
    return query.lower()


pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
def valid_mail(pattern, receiver_mail):
    return re.match(pattern, receiver_mail) is not None



def send_mail(sender_mail, sender_password, receiver_mail, msg):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(sender_mail, sender_password)
        server.sendmail(sender_mail, receiver_mail, msg)
        server.close()
        speak("Email sent successfully")
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        speak("Sorry, I couldn't send the email.")

def send_whatsapp_message(phone_number, message, hour, minute):

# Validate phone number format
    if not phone_number.startswith('+') or not phone_number[1:].isdigit():
        speak("Invalid phone number. Please enter a valid phone number.")
        print("Invalid phone number format. Please include the country code and ensure it contains only digits.")
    else:
        try:
        # Send the message at the specified time
            pwk.sendwhatmsg(phone_number, message, hour, minute, wait_time=20)
            speak("Message sent successfully!")
            print("Message sent successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")




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

def whatsapp_msgs(recipient_number, msg, time):
    try:
        recipient_number = "+91" + recipient_number
        # Ensure the time format is correct
        # pywhatkit.sendwhatmsg requires the time in the format (hour, minute)
        # Extract hours and minutes from the provided time
        time_parts = time.split(':')
        if len(time_parts) != 2:
            speak("Invalid time format. Please provide time in HH:MM format.")
            return
        
        hour, minute = map(int, time_parts)
        
        if not (0 <= hour < 24 and 0 <= minute < 60):
            speak("Invalid time. Please provide time in valid 24-hour format.")
            return
        
        pywhatkit.sendwhatmsg(recipient_number, msg, hour, minute, 5)
        speak("Message sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I am not able to send the message at the moment.")

def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    speak("Volume set to that required level...")

def set_brightness(level):
    sbc.set_brightness(level)
    speak("brightness set to that required percentage...")


def get_weather_data(city, api_key):
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def show_notification(temp, desc):
    notification.notify(
        title="Weather Update",
        message=f"Current Temperature: {temp}°C\nCondition: {desc}",
        timeout=10
    )


def speak_weather_update(temp, desc):
    engine = pyttsx3.init()
    weather_update = f"The current temperature is {temp} degrees Celsius with {desc}."
    engine.say(weather_update)
    engine.runAndWait()




if __name__ == "__main__":
    wishMe()
    running = True
    while running:
        query = get_input()
        if query:
            if 'open' in query:
                if 'cam' in query:
                    speak("Opening iV cam.....")
                    os.system('"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\e2eSoft iVCam\iVCam.lnk"')
                elif 'code' in query:
                    speak("Opening Visual Studio Code...")
                    os.system("code")
                elif 'youtube' in query:
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

            elif 'hello nova' in query:
                speak("Hi SIR ! Long time to see you how's going everything....")
                
            elif 'play a song' in query: 
                speak('Which song would you like to listen to?')
                song_name = input("USER : ")
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

            elif 'send whatsapp message' in query:
                speak("Enter the recipient's phone number (with country code): ")
                phone_number = input("RECIPIENT CONTACT: ")
                speak("Enter the message you want to send: ")
                message = input("MESSAGE: ")
                speak("can you tell me the time may be hours....")
                hour = int(input("HOURS(24-hour format): "))
                speak("can you tell me the time may be minutes....")
                minute = int(input("MINUTES: "))
                send_whatsapp_message(phone_number, message, hour, minute)


            elif 'send an email' in query:
                speak("what should i send???")
                msg=input("MESSAGE : ")
                sender_mail="siddharthsingh1150@gmail.com"
                sender_password="oavw barp qmuv ghjx"
                speak("To whom you want to send???,sir....")
                receiver_mail=input("ADDRESS : ")
                valid_mail(pattern,receiver_mail)
                if valid_mail(pattern, receiver_mail):
                    send_mail(sender_mail, sender_password, receiver_mail, msg)
                else:
                    speak("Invalid Gmail address. Please try again.")

            elif 'change system volume' in query:
                speak('What would you like to set the volume to?')
                level = float(input("Enter volume level (0-100): "))
                set_volume(level)

            elif 'change system brightness' in query:
                speak('What would you like to set the brightness to?')
                level = int(input("Enter brightness level (0-100): "))
                set_brightness(level)

            
            elif 'show weather updates' in query:
                city="kanpur"
                api_key = os.getenv('WEATHER_API_KEY')
                weather_data = get_weather_data(city, api_key)
                if weather_data:
                    try:
                        temp = weather_data['current']['temp_c']
                        desc = weather_data['current']['condition']['text']
                        show_notification(temp, desc)
                        speak_weather_update(temp, desc)
                    except KeyError as e:
                        print(f"KeyError: {e} - The API response structure might have changed.")
                else:
                    print("Failed to retrieve weather data. Please check the city name and API key.")

            elif 'shut down my system' in query:
                speak('Shutting down your laptop...')
                speak('Bye sir hope we will meet again....')
                os.system('shutdown /s /f /t 0')

            elif 'restart my system' in query:
                speak('restarting down your laptop...')
                speak('Bye sir hope we will meet again....')
                os.system('shutdown /r')

            elif 'exit' in query:
                speak('Goodbye! Have a great day.')
                running = False
