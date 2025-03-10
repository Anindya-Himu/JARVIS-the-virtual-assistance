import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI 
from gtts import gTTS
import pygame
import os
# pip install pocketphinx
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "88630ed240e841f9be01dd1a00074566"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load("temp.mp3")  # Replace with the path to your MP3 file

    # Play the music
    pygame.mixer.music.play()

    # Keep the program running while the music plays
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def AIprocess(command):
    client = OpenAI(api_key="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") 

    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
        {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa & Google Cloud. Give short responses please"},
        {"role": "user", "content": command}
      ]
    )

    return completion.choices[0].message.content
def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
        # parse the JSON response
           data = r.json()
        # Extract the articles
           articles = data.get('articles',[])
        # Print the headlines
           for article in articles:
            speak(article['title'])
    else:
        # Let OpenAI handle the request
        output = AIprocess(c)
        speak(output)

            
if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        # Listen for the wake word "Jarvis"
        # Obtain audio from the microphone
        r = sr.Recognizer()
        print("Recognizing....")
        try:
           with sr.Microphone() as source:
               print("Listening....")
               audio = r.listen(source, timeout=4, phrase_time_limit=2)
           word = r.recognize_google(audio)
           if(word.lower() == "jarvis"):
               speak("Yes,Jarvis is speaking.How can I assist you?")
               # Listen for command
               with sr.Microphone() as source:
                    print("Jarvis activated")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))