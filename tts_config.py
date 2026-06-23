import platform
import pyttsx3

def get_tts_engine():
    """Initialize TTS engine based on OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        engine = pyttsx3.init("nsss")
    elif system == "Windows":
        engine = pyttsx3.init("sapi5")
    else:  # Linux
        engine = pyttsx3.init("espeak")
    
    voices = engine.getProperty("voices")
    if voices:
        engine.setProperty("voice", voices[0].id)
    engine.setProperty("rate", 174)
    
    return engine
