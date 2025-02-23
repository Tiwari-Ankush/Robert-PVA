from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import shutil
from gtts import gTTS
import pygame
import os
import subprocess

app = Flask(__name__)

recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def getNews():
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=43abcf1d1e264b599fd666e0ab849b24')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if articles:
                first_news = articles[0]["title"]
                print(f"News: {first_news}")
                speak(first_news)
                return first_news  # Return the news headline
            else:
                print("No news found.")
                speak("Sorry, I couldn't find any news.")
                return "No news found."
        else:
            print("Error fetching news.")
            speak("Sorry, I couldn't fetch the news.")
            return "Error fetching news."
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while getting news.")
        return "An error occurred while getting news."

def system_command(action):
    commands = {
        "shutdown": "shutdown /s /t 1",
        "restart": "shutdown /r /t 1",
        "lock": "rundll32.exe user32.dll,LockWorkStation",
        "sleep": "rundll32.exe powrprof.dll,SetSuspendState 0,1,0"
    }
    if action in commands:
        speak(f"{action}ing your PC")
        os.system(commands[action])
        return f"{action}ing your PC"
    else:
        speak("Invalid system command")
        return "Invalid system command"

def get_weather(city="Pune"):
    API_KEY = "03d680695d72f619fd55f8f6bc4e465b"
    # url = f"https://api.openweathermap.org/data/2.5/weather?q={city},IN&appid={API_KEY}&units=metric"
    url = f"https://api.openweathermap.org/data/2.5/weather?q=India,In&appid={API_KEY}"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        weather = response["weather"][0]["description"]
        # speak(f"The temperature in {city} is {temp} degrees with {weather}")
        return f"Todays weather is {weather}"
    else:
        speak("Sorry, I couldn't fetch the weather")
        return "Sorry, I couldn't fetch the weather"

def openSoftware(software):
    try:
        if software == "word":
            subprocess.run(["start", "winword"], shell=True)
        elif software == "notepad":
            subprocess.run(["notepad"], shell=True)
        elif software == "chrome":
            subprocess.run(["start", "chrome"], shell=True)
        elif software == "edge":
            subprocess.run(["start", "msedge"], shell=True)
        elif software == "ms store":
            subprocess.run(["start", "ms-windows-store:"], shell=True)
        else:
            speak("Software not recognized or not installed")
            return "Software not recognized or not installed"
    except Exception as e:
        speak("Sorry, I couldn't open the software")
        print(e)
        return "Sorry, I couldn't open the software"

def take_notes(text):
    notes_path = "notes.txt"
    with open(notes_path, "a") as f:
        f.write(text + "\n")
    os.system("notepad.exe notes.txt")
    speak("Note saved and opened")
    return "Note saved and opened"

def set_volume(level):
    os.system(f"nircmd.exe setsysvolume {level * 65535 // 100}")
    speak(f"Volume set to {level} percent")
    return f"Volume set to {level} percent"

def set_brightness(level):
    os.system(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
    speak(f"Brightness set to {level} percent")
    return f"Brightness set to {level} percent"

def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}")
    return f"Here are the search results for {query}"

def file_management(action, path, destination=None):
    if action == "create":
        with open(path, "w") as f:
            f.write("This is a new file")
        speak("File created successfully")
        return "File created successfully"
    elif action == "delete":
        os.remove(path)
        speak("File deleted successfully")
        return "File deleted successfully"
    elif action == "move":
        shutil.move(path, destination)
        speak("File moved successfully")
        return "File moved successfully"
    else:
        speak("Invalid file action")
        return "Invalid file action"

def processCommand(command):
    c = command.lower()
    if "open google" in c:
        webbrowser.open("https://google.com")
        return "Opening Google..."
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
        return "Opening Facebook..."
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube..."
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
        return "Opening LinkedIn..."
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song, "")
        if link:
            webbrowser.open(link)
            return f"Playing {song}..."
        else:
            return "Song not found in the library."
    elif "breaking news" in c:
        return getNews()
    elif c.startswith("open"):
        software = c.split("open")[-1].strip()
        return openSoftware(software)
    elif "shutdown" in c:
        return system_command("shutdown")
    elif "restart" in c:
        return system_command("restart")
    elif "lock" in c:
        return system_command("lock")
    elif "sleep" in c:
        return system_command("sleep")
    elif "weather" in c:
        return get_weather("Pune")
    elif "take notes" in c:
        return take_notes("Hello Ankush, have a good day")
    elif "set volume" in c:
        level = int(c.split(" ")[-1].replace("%", ""))
        return set_volume(level)
    elif "set brightness" in c:
        level = int(c.split(" ")[-1].replace("%", ""))
        return set_brightness(level)
    elif "search for" in c:
        query = c.replace("search for", "").strip()
        return google_search(query)
    elif "create file" in c:
        return file_management("create", "example.txt")
    elif "delete file" in c:
        return file_management("delete", "example.txt")
    elif "move file" in c:
        return file_management("move", "example.txt", "C:/DestinationFolder")
    else:
        return "I am sorry, I do not understand that command."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    command = data.get('command')
    if not command:
        return jsonify({"status": "error", "message": "No command provided"})
    
    response = processCommand(command)
    return jsonify({"status": "success", "message": response})

if __name__ == "__main__":
    app.run(debug=True)