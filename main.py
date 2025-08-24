import speech_recognition as sr
import speech_recognition as sr
import pyttsx3
import webbrowser
import musiclibrary
import requests
import os
import pygame
from gtts import gTTS
import threading
from googleapiclient.discovery import build  #for google api
import pywhatkit as kit
import spotipy
from spotipy.oauth2 import SpotifyOAuth


r = sr.Recognizer()
engine = pyttsx3.init('sapi5')
newsapi = "ee513c6bf36f4313b13941d98142fd30"
    

# 👇 Google API setup
API_KEY = "AIzaSyA7AFqujn1LhAEzrM86jnxXXzgXPc3h6as"   # put your key here
CSE_ID = "c2df58d429fce41b8"     # put your custom search engine ID here

def google_search(query):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=query, cx=CSE_ID).execute()
    if "items" in res:
        first_result = res["items"][0]
        return f"{first_result['title']} - {first_result['snippet']}"
    else:
        return "Sorry, I could not find anything."
    

# Global flag for stopping
stop_flag = False   #globally run for stop comaand
    

    
def speak_old(text):
    engine.say(text)
    engine.runAndWait()
    
def speak(text):     
    global stop_flag
    stop_flag = False   # reset each time

# this is better than the old method as it is more clear and has better quality (lower part)

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing     
    while pygame.mixer.music.get_busy():         
        if stop_flag:   # if stop requested
            pygame.mixer.music.stop()
            break
        pygame.time.Clock().tick(10)      

    pygame.mixer.music.unload()     
    os.remove("temp.mp3")  

def stop():
    global stop_flag
    stop_flag = True
    try:
        pygame.mixer.music.stop()
    except:
        pass

# this is much more better than th epyttsx3 method as it is more clear and has better quality (upper part)
    
def processCommand(c):
    print(c)
    if "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        speak("Opening youtube")
        webbrowser.open("https://youtube.com")
    elif "open instagram" in c.lower():
        speak("Opening instagram")
        webbrowser.open("https://instagram.com")
    elif "open linkedin" in c.lower():
        speak("Opening linkdin")
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play", "").strip()

        # Case 1: If "spotify" in command → open Spotify search
        if "spotify" in song:
            song = song.replace("on spotify", "").strip()
            speak(f"Playing {song} on Spotify")
            webbrowser.open(f"https://open.spotify.com/search/{song}")

        # Case 2: If "jiosaavn" in command → open JioSaavn search
        elif "jio" in song or "saavn" in song:
            song = song.replace("on jiosaavn", "").strip()
            speak(f"Playing {song} on JioSaavn")
            webbrowser.open(f"https://www.jiosaavn.com/search/{song}")

            # Case 1: If "youtube" is in the command → play on YouTube
        if "youtube" in song:
            song = song.replace("on youtube", "").strip()
            speak(f"Playing {song} on YouTube")
            kit.playonyt(song)


            # Case 2: Otherwise, search on YouTube
        else:
            speak(f"Playing {song} on YouTube since I couldn't find it locally")
            kit.playonyt(song)
    
    # elif c.lower().startswith("play"):
    #     song = c.lower().split(" ")[1]
    #     link = musiclibrary.music[song]
    #     speak(f"Playing {song}")
    #     webbrowser.open(link)
    
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")

        if r.status_code == 200:
            # parse the json response
            data = r.json()
            # extract the articles
            articles = data.get("articles", [])
            # print the headlines
            for article in articles:
                if stop_flag:   # check stop before speaking
                    break
                speak(article['title']) 
                  
    # 👇 NEW: Google API query
    elif "what is" in c.lower() or "who is" in c.lower():
        result = google_search(c)
        speak(result)

    elif "stop" in c.lower():
        stop()
        speak("Okay, stopping.") 
        
    else:
        # if nothing else matched, do a Google search
        result = google_search(c)
        speak(result)

        

# Background listener to catch "stop" anytime
def stop_listener():
    global stop_flag
    while True:
        try:
            with sr.Microphone() as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                command = r.recognize_google(audio).lower()
                if "stop" in command:
                    stop_flag = True
                    pygame.mixer.music.stop()
                    print("🛑 Stop command detected!")
        except:
            pass

# Start the stop listener in background
threading.Thread(target=stop_listener, daemon=True).start()        

        
        
if __name__ == "__main__":
    speak(" Initializing jarvis...........")
    while True:
 
        r = sr.Recognizer()
        print("Recognizing...")
# # recognize speech using youtube
# # listen for the wake word jarvis
# # obtain audio from the microphone

        try:
            with sr.Microphone() as source: 
                print("Listening for the wake word 'jarvis'...")
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            word = r.recognize_google(audio)
            if (word.lower() == "jarvis"):
                speak("yaa ! how can i help you sir ")
                
                # listen for commomd
                with sr.Microphone() as source: 
                    print("jarvis activated")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                
                    processCommand(command)
                
        except Exception as e:
            # print("Sorry, I did not understand that.")
            print("Error; {0}".format(e))