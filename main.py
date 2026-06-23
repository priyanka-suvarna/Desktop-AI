import pyttsx3
import speech_recognition 
import wikipedia
import requests
import os
import plyer 
from bs4 import BeautifulSoup
import datetime
import pyautogui
import random
import speedtest
from Dictapp import openappweb, closeappweb
from tts_config import get_tts_engine

engine = get_tts_engine()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
def takeCommand():
    global input_mode  # Add this at the start of the function to track the mode
    
    if 'input_mode' not in globals():
        input_mode = 'voice'  # Default to voice mode
    
    # Check if we should switch modes based on last command
    if input_mode == 'voice':
        print("Using voice input mode. Say 'text input' to switch to text mode...")
    else:
        print("Using text input mode. Say 'voice input' to switch to voice mode...")
    
    # Handle text mode
    if input_mode == 'text':
        query = input("Enter your command: ").lower()
        print(f"You typed: {query}\n")
        
        # Check for mode switch
        if "voice input" in query:
            input_mode = 'voice'
            speak("voice input mode")
            return takeCommand()  # Recursive call to start voice input
        return query
    
    # Handle voice mode
    r = speech_recognition.Recognizer()
    while True:
        try:
            with speech_recognition.Microphone() as source:
                print("Listening.....")
                r.pause_threshold = 1
                r.energy_threshold = 300
                audio = r.listen(source, timeout=4)
                
                print("Understanding..")
                query = r.recognize_google(audio, language='en-in')
                print(f"You Said: {query}\n")
                
                # Check for mode switch
                if "text input" in query.lower():
                    input_mode = 'text'
                    speak("text input mode")
                    return takeCommand()  # Recursive call to start text input
                return query.lower()
                
        except speech_recognition.WaitTimeoutError:
            print("No voice detected, please try speaking again...")
            continue
            
        except Exception as e:
            print("Could not understand, please try speaking again...")
            continue

def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

if __name__== "__main__":
   while True:
       query = takeCommand().lower()
       if "wake up" in query:
           from GreetMe import greetme
           greetme()

           while True:
               query = takeCommand().lower()
               if "go to sleep" in query:
                   speak("Ok sir , You can call me anytime")
                   break
                
      


#########################################################################################    
               
               elif "hello" in query:
                    speak("Hello sir, how are you ?")
               elif "i am fine" in query:
                    speak("that's great, sir")
               elif "how are you" in query:
                    speak("Perfect, sir")
               elif "thank you" in query:
                    speak("you are welcome, sir")
               elif "introduce yourself" in query:
                    speak("I'm zira, your personal AI assistant, here to help with a wide range of tasks like answering questions, ")     

               elif "pause" in query:
                    pyautogui.press("k")
                    speak("video paused")
               elif "play" in query:
                    pyautogui.press("k")
                    speak("video played")
               elif "mute" in query:
                    pyautogui.press("m")
                    speak("video muted")

               elif "volume up" in query:
                    from keyboard import volumeup
                    speak("Turning volume up,sir")
                    volumeup()
               elif "volume down" in query:
                    from keyboard import volumedown
                    speak("Turning volume down, sir")
                    volumedown()

               elif "open" in query:   #EASY METHOD
                    from Dictapp import openappweb
                    openappweb(query)  

               elif "close" in query:
                    from Dictapp import closeappweb
                    closeappweb(query)

               elif "screenshot" in query:
                     import pyautogui 
                     im = pyautogui.screenshot()
                     im.save("screenshort.jpg")


               elif "take my photo" in query:
                    pyautogui.press("super")
                    pyautogui.typewrite("camera")
                    pyautogui.press("enter")
                    pyautogui.sleep(2)
                    speak("SMILE")
                    pyautogui.press("space")              

               elif "google" in query:
                    from SearchNow import searchGoogle
                    searchGoogle(query)
               elif "youtube" in query:
                    from SearchNow import searchYoutube
                    searchYoutube(query)

               if 'wikipedia' in query:
                    speak('Searching Wikipedia...')
                    query = query.replace("wikipedia", "").strip()
                    query = query.replace("what is","").strip()
                    query = query.replace("tell me about","").strip()
                    if query:
                        try:
                            results = wikipedia.summary(query, sentences=2)
                            speak("According to Wikipedia")
                            print(results)
                            speak(results)
                        except wikipedia.exceptions.PageError:
                            speak("Sorry, I couldn't find any information on that topic.")
                    else:
                        speak("Please specify a topic to search on Wikipedia.")

               elif "internet speed" in query:
                    wifi = speedtest.Speedtest()
                    upload_net = wifi.upload()/1048576         #Megabyte = 1024*1024 Bytes
                    download_net = wifi.download()/1048576
                    print("Wifi Upload Speed is", upload_net)
                    print("Wifi download speed is ",download_net)
                    speak(f"Wifi download speed is {download_net}")
                    speak(f"Wifi Upload speed is {upload_net}")

               elif "calculate" in query:
                    from Calculatenumbers import WolfRamAlpha
                    from Calculatenumbers import Calc
                    query = query.replace("calculate","")
                    query = query.replace("jarvis","")
                    Calc(query)  

               elif "whatsapp" in query:
                         from Whatsapp import sendMessage
                         sendMessage()   

               elif "translate" in query:
                    from Translator import translategl
                    query = query.replace("jarvis","")
                    query = query.replace("translate","")
                    translategl(query)
                                                     
               elif "temperature" in query:
                    search = "temperature is belgaum "
                    url = f"https://www.google.com/search?q={search}" 
                    r = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")
               
               elif "weather" in query:
                    search = "weather in belgaum"
                    url = f"https://www.google.com/search?q={search}"
                    r  = requests.get(url)
                    data = BeautifulSoup(r.text,"html.parser")
                    temp = data.find("div", class_ = "BNeawe").text
                    speak(f"current{search} is {temp}")

               elif "set an alarm" in query:
                    print("input time example:- 10 and 10 and 10")
                    speak("Set the time")
                    a = input("Please tell the time :- ")
                    alarm(a)
                    speak("Done,sir")

               elif "the time" in query:
                    strTime = datetime.datetime.now().strftime("%H:%M")    
                    speak(f"Sir, the time is {strTime}")

               elif "date" in query:
                    strTime = datetime.datetime.now().strftime("%d:%m")    
                    speak(f"Sir, today date is {strTime}")

               elif "good bye" in query:
                    speak("going to sleep, sir,if you have any questions please weak me up, i am ready to help you again, sir")
                    exit()

               elif "remember that" in query:
                    rememberMessage = query.replace("remember that","")
                    rememberMessage = query.replace("jarvis","")
                    speak("You told me to "+rememberMessage)
                    remember = open("Remember.txt","a")
                    remember.write(rememberMessage)
                    remember.close()

               elif "what do you remember" in query:
                    remember = open("Remember.txt","r")
                    speak("You told me to " + remember.read())

               elif "app" in query:
                    query = query.replace("open", "")
                    query = query.replace("app", "")
                    pyautogui.press("super")
                    pyautogui.typewrite(query)
                    pyautogui.sleep(2)
                    pyautogui.press("enter")

               
               elif "shutdown the system" in query:
                    speak("Are You sure you want to shutdown")
                    shutdown = input("Do you wish to shutdown your computer? (yes/no)")
                    if shutdown == "yes":
                         os.system("shutdown /s /t 1")

                    elif shutdown == "no":
                         break
                      
                    speak("ok sir , i will not shutdown")
