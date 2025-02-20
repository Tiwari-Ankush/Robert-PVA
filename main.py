import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import shutil
# from openai import OpenAI
from gtts import gTTS
import pygame
import os
import subprocess


recognizer = sr.Recognizer()
engine = pyttsx3.init() 
# newsapi = "<Your Key Here>"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

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
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# def aiProcess(command):
#     client = OpenAI(api_key="<Your Key Here>",
#     )

#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
#         {"role": "user", "content": command}
#     ]
#     )

#     return completion.choices[0].message.content


NEWS_API_KEY = "43abcf1d1e264b599fd666e0ab849b24"  # Replace with your NewsAPI key https://newsapi.org
def getNews():
    # url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    # url = f"https://newsapi.org/v2/everything?q=tesla&from=2025-01-20&sortBy=publishedAt&apiKey=43abcf1d1e264b599fd666e0ab849b24"
    url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=43abcf1d1e264b599fd666e0ab849b24')
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get("articles", [])

            if articles:
                # Fetch the first news headline
                first_news = articles[0]["title"]
                print(f"News: {first_news}")
                speak(first_news)  # Robert will speak the headline
            else:
                print("No news found.")
                speak("Sorry, I couldn't find any news.")
        else:
            print("Error fetching news.")
            speak("Sorry, I couldn't fetch the news.")
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while getting news.")




# NEWS_API_KEY = '43abcf1d1e264b599fd666e0ab849b24'  # Replace with your NewsAPI key https://newsapi.org
# def getNews(category="general"):
#     url = f"https://newsapi.org/v2/top-headlines?country=in&category={category}&apiKey={NEWS_API_KEY}"
    
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             data = response.json()
#             articles = data.get("articles", [])

#             if articles:
#                 # Fetch the first news headline
#                 first_news = articles[0]["title"]
#                 print(f"{category.capitalize()} News: {first_news}")
#                 speak(first_news)  # Robert will speak the headline
#             else:
#                 print(f"No {category} news found.")
#                 speak(f"Sorry, I couldn't find any {category} news.")
#         else:
#             print("Error fetching news.")
#             speak("Sorry, I couldn't fetch the news.")
#     except Exception as e:
#         print(f"Error: {e}")
#         speak("An error occurred while getting news.")



# 1️⃣ System Commands
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
    else:
        speak("Invalid system command")

# 2️⃣ Weather Report
def get_weather(city="Pune"):
    API_KEY = "your_openweathermap_api_key"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        weather = response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degrees with {weather}")
    else:
        speak("Sorry, I couldn't fetch the weather")

# 3️⃣ Open Software

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
    except Exception as e:
        speak("Sorry, I couldn't open the software")
        print(e)


# 4️⃣ Taking notes

def take_notes(text):
    notes_path = "notes.txt"
    with open(notes_path, "a") as f:
        f.write(text + "\n")
    os.system("notepad.exe notes.txt")
    speak("Note saved and opened")

# 4️⃣ Control System Volume & Brightness
def set_volume(level):
    os.system(f"nircmd.exe setsysvolume {level * 65535 // 100}")
    speak(f"Volume set to {level} percent")

def set_brightness(level):
    os.system(f"powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})")
    speak(f"Brightness set to {level} percent")

# 5️⃣ Google Search Integration
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Here are the search results for {query}")

# 6️⃣ File Management
def file_management(action, path, destination=None):
    if action == "create":
        with open(path, "w") as f:
            f.write("This is a new file")
        speak("File created successfully")
    elif action == "delete":
        os.remove(path)
        speak("File deleted successfully")
    elif action == "move":
        shutil.move(path, destination)
        speak("File moved successfully")
    else:
        speak("Invalid file action")


def processCommand(command):
    c=command.lower()
    command =command.lower()
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


    elif "breaking news" in c.lower():
            getNews()  # Fetch and speak news

    # # News Categories
    # elif "breaking news" in c.lower():
    #     getNews("general")  # General news

    # elif "sports news" in c.lower():
    #     getNews("sports")  # Sports news

    # elif "technology news" in c.lower():
    #     getNews("technology")  # Tech news

    # elif "business news" in c.lower():
    #     getNews("business")  # Business news

    # elif "entertainment news" in c.lower():
    #     getNews("entertainment")  # Entertainment news

    # elif "health news" in c.lower():
    #     getNews("health")  # Health news

    # elif "science news" in c.lower():
    #     getNews("science")  # Science news

    # elif "news" in c.lower():
    #     r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
    #     if r.status_code == 200:
    #         # Parse the JSON response
    #         data = r.json()
            
    #         # Extract the articles
    #         articles = data.get('articles', [])
            
    #         # Print the headlines
    #         for article in articles:
    #             speak(article['title'])

    elif c.lower().startswith("open"):
            software = c.lower().split("open")[-1].strip()
            openSoftware(software)

    elif "shutdown" in command:
        system_command("shutdown")
    elif "restart" in command:
        system_command("restart")
    elif "lock" in command:
        system_command("lock")
    elif "sleep" in command:
        system_command("sleep")
    elif "weather" in command:
        get_weather("Pune")
    elif "take notes" in command:
        take_notes("Hello Ankush, have a good day")
    elif "set volume" in command:
        level = int(command.split(" ")[-1].replace("%", ""))
        set_volume(level)
    elif "set brightness" in command:
        level = int(command.split(" ")[-1].replace("%", ""))
        set_brightness(level)
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        google_search(query)
    elif "create file" in command:
        file_management("create", "example.txt")
    elif "delete file" in command:
        file_management("delete", "example.txt")
    elif "move file" in command:
        file_management("move", "example.txt", "C:/DestinationFolder")
    else:
        # # Let OpenAI handle the request
        # output = aiProcess(c)
        # speak(output) 
        speak("I am sorry, I do not understand that command")


# 9️⃣ Voice Command Processing
def process_command(command):
    command = command.lower()
    if "shutdown" in command:
        system_command("shutdown")
    elif "restart" in command:
        system_command("restart")
    elif "lock" in command:
        system_command("lock")
    elif "sleep" in command:
        system_command("sleep")
    elif "weather" in command:
        get_weather("Pune")
    elif "take notes" in command:
        take_notes("Hello Ankush, have a good day")
    elif "set volume" in command:
        level = int(command.split(" ")[-1].replace("%", ""))
        set_volume(level)
    elif "set brightness" in command:
        level = int(command.split(" ")[-1].replace("%", ""))
        set_brightness(level)
    elif "search for" in command:
        query = command.replace("search for", "").strip()
        google_search(query)
    elif "create file" in command:
        file_management("create", "example.txt")
    elif "delete file" in command:
        file_management("delete", "example.txt")
    elif "move file" in command:
        file_management("move", "example.txt", "C:/DestinationFolder")
    elif "breaking news" in command:
        getNews()
    else:
        speak("I do not understand that command")


if __name__ == "__main__":
    speak("Initializing Robert...")
    print("Robert is ready")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            print(word.lower())
            if(word.lower() == "robert"):
                speak("Ya, I am here")
                # Listen for command
                with sr.Microphone() as source:
                    print("Robert is listening...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))


