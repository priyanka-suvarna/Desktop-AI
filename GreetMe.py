import pyttsx3
from tts_config import get_tts_engine
import datetime

engine = get_tts_engine()
engine.setProperty("rate",200)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greetme():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning ,sir")
    elif hour >12 and hour<=18:
        speak("Good Afternoon ,sir")

    else:
        speak("Good Evening,sir")

    speak("Please tell me, How can i help you")   
