"""
Coffee Voice Assistant - Flask Backend

Run:
    python server.py

Then open:
    http://127.0.0.1:5000
"""


import os
import random
import subprocess
import webbrowser
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS


# ENVIRONMENT VARIABLES
load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")


# FLASK
app = Flask(__name__)

CORS(app)


# CHROME
def open_chrome(url):
    """
    Open a URL specifically in Google Chrome on Windows.
    If Chrome cannot be found, use the default browser.
    """

    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ),
    ]

    for chrome_path in chrome_paths:

        if os.path.exists(chrome_path):

            try:

                subprocess.Popen(
                    [chrome_path, url]
                )

                return True

            except Exception as e:

                print("Chrome error:", e)

    # Fallback
    try:

        webbrowser.open(url)

        return True

    except Exception as e:

        print("Browser error:", e)

        return False


# OPEN WEBSITE / APP
def h_open_app(text):
    text = text.lower().strip()

    # Remove common words so:
    # "open gmail", "open gmail app", "please open gmail" all become easier to match.
    cleaned = text

    for word in ["please", "open", "start", "launch", "app", "website"]:
        cleaned = cleaned.replace(word, " ")

    cleaned = " ".join(cleaned.split())

    websites = {
        "gmail": "https://mail.google.com/",
        "whatsapp": "https://web.whatsapp.com/",
        "youtube": "https://www.youtube.com/",
        "google": "https://www.google.com/",
        "github": "https://github.com/",
        "instagram": "https://www.instagram.com/",
        "facebook": "https://www.facebook.com/",
        "linkedin": "https://www.linkedin.com/",
        "chatgpt": "https://chatgpt.com/",
        "spotify": "https://open.spotify.com/",
        "netflix": "https://www.netflix.com/",
        "amazon": "https://www.amazon.in/",
        "flipkart": "https://www.flipkart.com/",
        "drive": "https://drive.google.com/",
        "google drive": "https://drive.google.com/",
        "maps": "https://maps.google.com/",
        "google maps": "https://maps.google.com/",
    }

    print("OPEN COMMAND:", text)
    print("CLEANED APP NAME:", cleaned)

    # Chrome itself
    if cleaned in ["chrome", "google chrome"]:
        open_chrome("https://www.google.com/")
        return "Opening Google Chrome."

    # Exact match
    if cleaned in websites:
        url = websites[cleaned]

        if open_chrome(url):
            return f"Opening {cleaned} in Chrome."

        return f"I couldn't open {cleaned}."

    # Partial match
    for name, url in websites.items():
        if name in cleaned:
            if open_chrome(url):
                return f"Opening {name} in Chrome."

            return f"I couldn't open {name}."

    return f"I don't know the app {cleaned}."

   

# Open Chrome

def open_chrome(url):
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ),
    ]

    for chrome_path in chrome_paths:
        if os.path.exists(chrome_path):
            try:
                subprocess.Popen([chrome_path, url])
                return True

            except Exception as e:
                print("CHROME ERROR:", e)

    # If Chrome path wasn't found, use default browser
    try:
        webbrowser.open(url)
        return True

    except Exception as e:
        print("BROWSER ERROR:", e)
        return False



# TIME
def h_time():

    current_time = datetime.now().strftime("%I:%M %p")

    return f"The current time is {current_time}."


# DATE
def h_date():

    current_date = datetime.now().strftime(
        "%A, %d %B %Y"
    )

    return f"Today is {current_date}."



# GREETING
def h_greeting():

    hour = datetime.now().hour

    if hour < 12:

        greeting = "Good morning"

    elif hour < 17:

        greeting = "Good afternoon"

    else:

        greeting = "Good evening"

    return (
        f"{greeting}. "
        "I am Coffee. How may I help you?"
    )



# JOKE
def h_joke():

    jokes = [
        (
            "Why do programmers prefer dark mode? "
            "Because light attracts bugs."
        ),

        (
            "Why was the computer cold? "
            "Because it left its Windows open."
        ),

        (
            "Why did the developer go broke? "
            "Because he used up all his cache."
        ),

        (
            "Why do Java developers wear glasses? "
            "Because they can't C sharp."
        ),

        (
            "There are only 10 types of people in the world. "
            "Those who understand binary and those who don't."
        ),
    ]

    return random.choice(jokes)



# NEWS
def h_news():

    # Read directly from environment.
    # This avoids your previous NEWS_API_KEY local-variable error.

    news_api_key = os.getenv("NEWS_API_KEY")

    if not news_api_key:

        return (
            "News API key is missing. "
            "Please add NEWS_API_KEY to your .env file."
        )

    url = "https://newsapi.org/v2/top-headlines"

    params = {
        "country": "us",
        "pageSize": 5,
        "apiKey": news_api_key,
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        # NewsAPI can return an error as JSON
        if data.get("status") == "error":

            print(
                "NewsAPI error:",
                data.get("message")
            )

            return (
                "NewsAPI returned an error: "
                + data.get(
                    "message",
                    "Unknown error."
                )
            )

        articles = data.get(
            "articles",
            []
        )

        if not articles:

            return (
                "I couldn't find any latest news."
            )

        headlines = []

        for article in articles[:5]:

            title = article.get("title")

            if title:

                headlines.append(title)

        if not headlines:

            return (
                "I couldn't find any latest news."
            )

        return (
            "Here are the latest headlines. "
            + ". ".join(headlines)
        )

    except requests.RequestException as e:

        print(
            "NEWS ERROR:",
            e
        )

        return (
            "Sorry, I couldn't fetch the latest news."
        )



# WEATHER
def h_weather(text):

    weather_api_key = os.getenv(
        "WEATHER_API_KEY"
    )

    if not weather_api_key:

        return (
            "Weather API is not configured yet. "
            "Add WEATHER_API_KEY to the .env file."
        )

    text = text.lower()

    # Default city
    city = "Jaipur"

    if "weather in " in text:

        city = text.split(
            "weather in ",
            1
        )[1].strip()

    elif "weather for " in text:

        city = text.split(
            "weather for ",
            1
        )[1].strip()

    url = (
        "https://api.openweathermap.org/"
        "data/2.5/weather"
    )

    params = {
        "q": city,
        "appid": weather_api_key,
        "units": "metric",
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        temperature = data[
            "main"
        ]["temp"]

        feels_like = data[
            "main"
        ]["feels_like"]

        description = data[
            "weather"
        ][0]["description"]

        city_name = data.get(
            "name",
            city
        )

        return (
            f"The weather in {city_name} is "
            f"{description}. "
            f"The temperature is "
            f"{temperature} degrees Celsius "
            f"and it feels like "
            f"{feels_like} degrees Celsius."
        )

    except requests.RequestException as e:

        print(
            "WEATHER ERROR:",
            e
        )

        return (
            "Sorry, I couldn't fetch "
            "the weather."
        )

    except (KeyError, IndexError):

        return (
            "I couldn't understand the "
            "weather information."
        )


# WIKIPEDIA
def h_wikipedia(text):

    query = text.lower()

    # Remove command words

    query = query.replace(
        "wikipedia",
        ""
    )

    query = query.replace(
        "search",
        ""
    )

    query = query.replace(
        "who is",
        ""
    )

    query = query.replace(
        "what is",
        ""
    )

    query = query.strip()

    if not query:

        return (
            "Please tell me what you want "
            "to search on Wikipedia."
        )

    encoded_query = requests.utils.quote(
        query
    )

    url = (
        "https://en.wikipedia.org/"
        "api/rest_v1/page/summary/"
        + encoded_query
    )

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent":
                "CoffeeVoiceAssistant/1.0"
            }
        )

        if response.status_code != 200:

            return (
                f"I couldn't find Wikipedia "
                f"information about {query}."
            )

        data = response.json()

        extract = data.get(
            "extract",
            ""
        )

        if not extract:

            return (
                f"I couldn't find information "
                f"about {query}."
            )

        # Keep answer short
        sentences = extract.split(". ")

        answer = ". ".join(
            sentences[:3]
        )

        if not answer.endswith("."):

            answer += "."

        return answer

    except requests.RequestException as e:

        print(
            "WIKIPEDIA ERROR:",
            e
        )

        return (
            "Sorry, I couldn't connect "
            "to Wikipedia."
        )



# GOOGLE SEARCH
def h_google_search(text):

    query = text.lower().strip()

    remove_words = [
        "search google for",
        "google search for",
        "google search",
        "search for",
        "search",
        "google",
    ]

    for words in remove_words:

        if query.startswith(words):

            query = query[
                len(words):
            ].strip()

            break

    if not query:

        return (
            "What would you like me "
            "to search for?"
        )

    encoded_query = requests.utils.quote(
        query
    )

    url = (
        "https://www.google.com/search?q="
        + encoded_query
    )

    open_chrome(url)

    return (
        f"Searching Google for {query}."
    )


# VOLUME
def h_volume(text):

    text = text.lower()

    # Basic Windows volume control using keyboard media keys via PowerShell / WScript.

    if "volume up" in text:

        try:

            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    (
                        "$obj = New-Object -ComObject WScript.Shell; "
                        "$obj.SendKeys([char]175)"
                    )
                ],
                check=False
            )

            return "Volume increased."

        except Exception as e:

            print(
                "VOLUME ERROR:",
                e
            )

            return (
                "I couldn't increase the volume."
            )

    if "volume down" in text:

        try:

            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    (
                        "$obj = New-Object -ComObject WScript.Shell; "
                        "$obj.SendKeys([char]174)"
                    )
                ],
                check=False
            )

            return "Volume decreased."

        except Exception as e:

            print(
                "VOLUME ERROR:",
                e
            )

            return (
                "I couldn't decrease the volume."
            )

    if (
        "mute" in text
        or "unmute" in text
    ):

        try:

            subprocess.run(
                [
                    "powershell",
                    "-Command",
                    (
                        "$obj = New-Object -ComObject WScript.Shell; "
                        "$obj.SendKeys([char]173)"
                    )
                ],
                check=False
            )

            return "Toggling mute."

        except Exception as e:

            print(
                "VOLUME ERROR:",
                e
            )

            return (
                "I couldn't change the mute setting."
            )

    return (
        "Say volume up, volume down, or mute."
    )


# MAIN COMMAND HANDLER
def handle_command(text):

    if not text:

        return "I didn't hear anything."

    text = text.lower().strip()

    print(
        "Received command:",
        text
    )

    try:
        # OPEN

        if text.startswith("open "):

            return h_open_app(text)


        # NEWS

        if (
            text == "news"
            or "latest news" in text
            or "headlines" in text
        ):

            return h_news()

        
        # WEATHER

        if "weather" in text:

            return h_weather(text)

        
        # TIME

        if (
            text == "time"
            or "what time" in text
            or "what's the time" in text
            or "current time" in text
        ):
    
            return h_time()

        # DATE
            
        if (
            text == "date"
            or "today's date" in text
            or "todays date" in text
            or "what is the date" in text
            or "what day is it" in text
        ):

            return h_date()

        
        # JOKE
    
        if "joke" in text:

            return h_joke()

        
        # WIKIPEDIA
    
        if (
            "wikipedia" in text
            or text.startswith("who is ")
        ):

            return h_wikipedia(text)

        
        # GOOGLE SEARCH

        if (
            text.startswith("search ")
            or text.startswith("google ")
        ):

            return h_google_search(text)

        
        # VOLUME

        if (
            "volume" in text
            or "mute" in text
        ):

            return h_volume(text)


        # GREETING

        if text in [
            "hello",
            "hi",
            "hey",
            "hello coffee",
            "hi coffee",
            "hey coffee",
        ]:

            return h_greeting()

       
        # THANKS
         
        if (
            "thank you" in text
            or text == "thanks"
        ):

            return (
                "You're welcome."
            )

        
        # UNKNOWN

        return (
            "I don't understand that command yet. "
            "Try asking for time, weather, latest news, "
            "a joke, Wikipedia, Google search, "
            "or ask me to open a website."
        )


    except Exception as e:

        print(
            "COMMAND ERROR:",
            e
        )

        return (
            "Something went wrong: "
            + str(e)
        )



# API - HEALTH CHECK

@app.route(
    "/api/health",
    methods=["GET"]
)
def health():

    return jsonify(
        {
            "ok": True,
            "status": "online",
            "assistant": "Coffee",
            "news_api": bool(
                os.getenv(
                    "NEWS_API_KEY"
                )
            ),
            "weather_api": bool(
                os.getenv(
                    "WEATHER_API_KEY"
                )
            ),
        }
    )



# API - COMMAND

@app.route(
    "/api/command",
    methods=["POST"]
)
def command():

    try:

        data = request.get_json(
            silent=True
        ) or {}

        # Support several frontend field names
        text = (
            data.get("text")
            or data.get("command")
            or data.get("message")
            or ""
        )

        text = str(text).strip()

        if not text:

            return jsonify(
                {
                    "ok": False,
                    "reply":
                    "Please enter a command."
                }
            ), 400

        reply = handle_command(
            text
        )

        return jsonify(
            {
                "ok": True,
                "reply": reply,
                "response": reply,
            }
        )

    except Exception as e:

        print(
            "API ERROR:",
            e
        )

        return jsonify(
            {
                "ok": False,
                "reply":
                "Something went wrong: "
                + str(e)
            }
        ), 500



# OPTIONAL ROOT ROUTE

@app.route(
    "/",
    methods=["GET"]
)
def home():

    return jsonify(
        {
            "message":
            "Coffee Assistant server is running.",
            "health":
            "/api/health",
            "command":
            "/api/command"
        }
    )



# START FLASK SERVER

if __name__ == "__main__":

    print()
    print("=" * 55)
    print("COFFEE ASSISTANT SERVER")
    print("=" * 55)

    print(
        "News API:",
        "Loaded"
        if NEWS_API_KEY
        else "Missing"
    )

    print(
        "Weather API:",
        "Loaded"
        if WEATHER_API_KEY
        else "Missing"
    )

    print(
        "Server: http://127.0.0.1:5000"
    )

    print("=" * 55)
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )