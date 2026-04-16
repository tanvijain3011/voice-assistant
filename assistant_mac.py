import pyttsx3
import requests
import speech_recognition as sr
import datetime
import time
import os
import os.path
import sys
import cv2
import random
from requests import get
import wikipedia
import webbrowser
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pyjokes
import pyautogui
import PyPDF2
import operator
from bs4 import BeautifulSoup
from wikipedia import search as wikipedia_search
from pywikihow import search_wikihow

# Initialize TTS engine (macOS uses nsss, not sapi5)
engine = pyttsx3.init()


# --- Speak function ---
def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()


# --- Wish user ---
def wishMe():
    hour = int(datetime.datetime.now().hour)
    tt = time.strftime("%I:%M %p")
    if 0 <= hour < 12:
        speak(f"Good Morning Sir, it's {tt}")
    elif 12 <= hour < 18:
        speak(f"Good Afternoon Sir, it's {tt}")
    else:
        speak(f"Good Evening Sir, it's {tt}")
    speak("I am Coffee Sir. Tell me how may I help you")


# --- Send email ---
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    # Replace with your Gmail and password (or app password)
    server.login("mangaguy432@gmail.com", "kingofpirates")
    server.sendmail("tanvij3011@gmail.com", to, content)
    server.close()


# --- Get news (TechCrunch) ---
def news():
    main_url = 'https://newsapi.org/v2/top-headlines?sources=techcrunch&apiKey=e44a5ef8ff6848158b21b486eb54f72f'
    mainpage = requests.get(main_url).json()
    articles = mainpage["articles"]
    head = [ar["title"] for ar in articles]
    day = ["first", "second", "third", "fourth", "fifth", "sixth"]
    for i in range(min(len(day), len(head))):
        speak(f"Today's {day[i]} news is: {head[i]}")


# --- Read PDF ---
def pdf_reader():
    # Change path as per macOS
    pdfname = "/Users/utkarshjain/Desktop/Console-Assist-App-main/Jarvis Console/cooking- research paper.pdf"
    if not os.path.exists(pdfname):
        speak("PDF file not found")
        return
    book = open(pdfname, 'rb')
    pdfReader = PyPDF2.PdfReader(book)  # Note: newer PyPDF2 uses PdfReader
    pages = len(pdfReader.pages)
    speak(f"Total pages in this book are {pages}")
    speak("Sir which page do you want me to read")
    pg = int(input("Enter the page number: ")) - 1  # 0‑based
    page = pdfReader.pages[pg]
    text = page.extract_text()
    speak(text)
    book.close()


# --- Voice input ---
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=3, phrase_time_limit=5)
        except Exception as e:
            print(e)
            return "none"

    try:
        print('Recognizing...')
        query = r.recognize_google(audio, language='en-in')
        print(f"User Said: {query}")
    except Exception as e:
        speak("Say that again please")
        return "none"
    return query.lower()


# --- Main assistant logic ---
def taskExecution():
    wishMe()
    while True:
        query = takecommand()

        # General commands
        if 'hello' in query:
            speak("Oh, hello sir")
        elif 'how are you' in query:
            speak("I am fine sir, and what about you")
        elif 'good' in query:
            speak("That's great to hear from you")
        elif 'not' in query:
            speak("Well, there are some consequences")

        elif "quit" in query or "goodbye" in query or "sleep" in query:
            speak("Ok sir, call me when you want")
            sys.exit()

        elif "thanks" in query or "thank you" in query:
            speak("No problem sir")


        # System functions
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'alarm' in query:
            speak("At what time. For example, set alarm to 5:30 a.m.")
            tt = takecommand()
            tt = tt.replace("to", "")
            tt = tt.replace(".", "")
            tt = tt.upper()
            # Example: you need to have MyAlarm.py compatible with macOS
            import MyAlarm
            MyAlarm.alarm(tt)

        elif 'play music' in query:
            # Replace with your macOS music folder
            music_dir = "/Users/utkarshjain/Desktop/Console-Assist-App-main/Jarvis Console"
            if os.path.exists(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    rd = random.choice(songs)
                    os.system(f"open \"{os.path.join(music_dir, rd)}\"")
                else:
                    speak("No songs in folder")
            else:
                speak("Music folder not found")

        elif 'screenshot' in query:
            speak("Sir, please tell me a name for this screenshot")
            name1 = takecommand()
            speak("Ok sir, taking screenshot")
            time.sleep(5)
            img = pyautogui.screenshot()
            img.save(f"{name1}.jpg")
            speak("Sir, screenshot has been taken")

        elif 'switch window' in query:
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            time.sleep(2)
            pyautogui.keyUp("alt")

        # elif 'volume up' in query or 'increase volume' in query:
        #     # No direct key on macOS; you can use AppleScript (optional)
        #     speak("Volume control not implemented on macOS yet")

        # elif 'volume down' in query or 'decrease volume' in query:
        #     speak("Volume control not implemented on macOS yet")

        # elif 'mute' in query or 'quiet' in query:
        #     speak("Volume control not implemented on macOS yet")

        elif 'ip address' in query:
            ip = get('https://api.ipify.org').text
            speak(f"Your IP address is {ip}")

        elif 'restart system' in query:
            speak("Restarting")
            os.system("osascript -e 'tell app \"System Events\" to restart'")

        elif 'shut down system' in query:
            speak("Sir, do you really want to shut down the system?")
            ans = takecommand()
            if 'yes' in ans:
                speak("Shutting down")
                os.system("osascript -e 'tell app \"System Events\" to shut down'")
            else:
                speak("Ok sir, not shutting down")


        # Application controls (macOS using `open -a`)
        elif 'open notepad' in query:
            os.system("open -a 'TextEdit'")
            speak("Opening text editor")

        elif 'open safari' in query:
            os.system("open -a 'Safari'")
            speak("Opening Safari")

        elif 'open zoom' in query:
            os.system("open -a 'zoom'")
            speak("Opening Zoom")

        elif 'open code' in query:
            os.system("open -a 'Visual Studio Code'")
            speak("Opening VS Code")

        elif 'open telegram' in query:
            os.system("open -a 'Telegram'")
            speak("Opening Telegram")

        elif 'open whatsapp' in query:
            os.system("open -a 'Whatsapp'")
            speak("Opening Whatsapp")

        # Other Office apps (if installed; adjust as needed)
        elif 'open calender' in query:
            os.system("open -a 'Calender")
            speak("Opening Calender")

        elif 'open powerpoint' in query:
            os.system("open -a 'Microsoft PowerPoint'")
            speak("Opening PowerPoint")

        elif 'open excel' in query:
            os.system("open -a 'Microsoft Excel'")
            speak("Opening Excel")

        elif 'open onenote' in query:
            os.system("open -a 'Microsoft OneNote'")
            speak("Opening OneNote")

        elif 'open outlook' in query:
            os.system("open -a 'Microsoft Outlook'")
            speak("Opening Outlook")

        elif 'open terminal' in query:
            os.system("open -a 'Terminal'")
            speak("Starting terminal")

        elif 'close terminal' in query:
            speak("Closing terminal")
            os.system("osascript -e 'tell app \"Terminal\" to quit'")


        # Folders (macOS paths)
        elif 'open videos' in query:
            os.system("open /Users/yourusername/Lucky\\ Self")

        # elif 'open lucky' in query:
        #     os.system("open /Users/yourusername/Lucky")

        # elif 'open coding' in query:
        #     os.system("open /Users/yourusername/Lucky\\ Self/Coding")


        # Internet
        elif 'open google' in query:
            webbrowser.open("https://www.google.com")

        elif 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")

        elif 'open facebook' in query:
            webbrowser.open("https://www.facebook.com")

        elif 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")

        elif 'profile on instagram' in query:
            speak("Sir, please enter the username.")
            name = input("Enter the username here: ")
            webbrowser.open(f"https://www.instagram.com/{name}")
            speak(f"Sir, here is the profile of the user {name}")
            time.sleep(5)

        elif 'search on google' in query:
            speak("Sir, what should I search on Google?")
            cm = takecommand()
            webbrowser.open(f"https://www.google.com/search?q={cm}")

        elif 'email to utkarsh' in query:
            speak("Sir, what should I say?")
            query = takecommand()
            if 'send a file' in query:
                email = "your_email@gmail.com"
                password = "your_password"
                send_to_email = "lucky_email@gmail.com"
                speak("Ok sir, what is the subject for this email?")
                subject = takecommand()
                speak("And sir, what's the message?")
                message = takecommand()
                speak("Sir, please enter path of the file you want to send")
                file_location = input("Please enter the location of file here: ")

                speak("Please wait sir, I am sending email")
                msg = MIMEMultipart()
                msg['From'] = email
                msg['To'] = send_to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                filename = os.path.basename(file_location)
                with open(file_location, "rb") as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {filename}")
                msg.attach(part)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                text = msg.as_string()
                server.sendmail(email, send_to_email, text)
                server.quit()
                speak('Email has been sent to utkarsh')

            else:
                email = "your_email@gmail.com"
                password = "your_password"
                send_to_email = "lucky_email@gmail.com"
                message = query

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(email, password)
                server.sendmail(email, send_to_email, message)
                server.quit()
                speak('Email has been sent to lucky')


        # Wikipedia
        elif "wikipedia" in query:
            speak("Searching...")
            query = query.replace("wikipedia", "")
            try:
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                speak(results)
            except Exception as e:
                speak("Could not find that on Wikipedia")

        # How‑to from WikiHow
        elif 'how to' in query:
            speak("Searching")
            how = query.replace("Coffee", "")
            max_results = 1
            how_to = search_wikihow(how, max_results)
            if how_to:
                speak(how_to[0].summary)
            else:
                speak("Could not find a how‑to for that")

        # Internet speed
        elif 'internet speed' in query:
            import speedtest
            st = speedtest.Speedtest()
            dl = st.download()
            up = st.upload()
            speak("Wait")
            speak(f"Sir, downloading speed is {dl} bits per second and uploading is {up} bits per second")

        # News
        elif 'news' in query:
            speak("Please wait sir, fetching the latest news")
            news()

        # Location (IP‑based)
        elif 'where am i' in query or 'where are we' in query or 'ip' in query:
            speak("Wait sir, let me check")
            try:
                ipAdd = requests.get('https://api.ipify.org').text
                print(ipAdd)
                url = f'https://get.geojs.io/v1/ip/geo/{ipAdd}.json'
                geo_requests = requests.get(url)
                geo_data = geo_requests.json()
                city = geo_data.get('city', 'Unknown')
                country = geo_data.get('country', 'Unknown')
                speak(f"Sir, I am not sure, but I think we are in {city} city in {country}")
            except Exception as e:
                speak("Sorry sir, I am not able to access the location")

        # Temperature (Google page scraping)
        elif 'temperature' in query:
            search = "temperature in Jaipur"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp_elem = data.find("div", class_="BNeawe")
            if temp_elem:
                temp = temp_elem.text
                speak(f"Current {search} is {temp}")
            else:
                speak("Could not get temperature")


        # Outer applications
        elif 'open camera' in query:
            speak("Opening camera")
            cap = cv2.VideoCapture(0)
            while True:
                ret, img = cap.read()
                cv2.imshow('Webcam', img)
                k = cv2.waitKey(50)
                if k == 27:  # ESC key
                    break
            cap.release()
            cv2.destroyAllWindows()

        elif 'read pdf' in query:
            pdf_reader()

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            speak(joke)


# Main entry
if __name__ == "__main__":
    taskExecution()