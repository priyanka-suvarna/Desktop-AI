import os
import webbrowser
import pyautogui

def openappweb(query):
    query = query.lower()
    
    # Common apps and websites
    apps = {
        # Websites
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "gmail": "https://mail.google.com",
        "facebook": "https://www.facebook.com",
        "instagram": "https://www.instagram.com",

        
        # Desktop apps
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "camera": "camera.exe",
        "powerpoint": "powerpoint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "settings": "control.exe",
        "power toys": "powertoys.exe",
        "calander": "calender.exe",
        "cmd": "cmd.exe",
        "control panel": "control.exe",
        "terminal": "wt.exe",
        "store": "ms-windows-store://",
        "task manager": "taskmgr.exe",
        "vs code": "code.exe",
        "whatsapp ":"https://web.whatsapp.com",
        "file explorer": "explorer.exe",
        "telegram": "https://web.telegram.org",

        

        
    }
    
    # Check if app exists in our dictionary
    for app, path in apps.items():
        if app in query:
            # If it's a website (starts with http)
            if path.startswith('http'):
                webbrowser.open(path)
            # If it's a desktop app
            else:
                os.startfile(path)
            return f"Opening {app}"
    
    return "Application not found!"

def closeappweb(query):
    query = query.lower()
    
    # Common desktop apps
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "camera": "camera.exe",
        "powerpoint": "powerpoint.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "word": "winword.exe",
        "excel": "excel.exe",
        "powerpoint": "powerpnt.exe",
        "settings": "control.exe",
        "powertoys": "powertoys.exe",
        "calander": "calender.exe",
        "cmd": "cmd.exe",
        "control panel": "control.exe",
        "terminal": "wt.exe",
        "store": "ms-windows-store://",
        "task manager": "taskmgr.exe",
        "vs code": "code.exe",
        "whatsapp ":"https://web.whatsapp.com",
        "file explorer": "explorer.exe",
        "telegram": "https://web.telegram.org",

        
    }
    
    # Close browser tab if chrome is mentioned
    if "chrome" in query:
        pyautogui.hotkey("ctrl", "w")
        return "Closing current tab"
    
    # Close desktop app
    for app, process in apps.items():
        if app in query:
            os.system(f"taskkill /f /im {process}")
            return f"Closing {app}"
    
    return "Application not found!"