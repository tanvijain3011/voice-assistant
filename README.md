# Coffee – voice assistant (web frontend + Flask backend)

## Setup
    python -m venv venv && source venv/bin/activate
    pip install -r requirements.txt
    cp .env.example .env      # add keys you need
    python server.py

Open http://127.0.0.1:5000 in Chrome or Safari (mic works on localhost).

## Layout
    server.py        Flask API: POST /api/command, GET /api/health
    static/          index.html, style.css, app.js

Alarm, timer, website opening, Google search and calculator run in the browser.
Everything else (weather, news, Wikipedia, opening Mac apps, volume, screenshots, email, PDF, power) goes to the server.
Restart/shutdown ask for a spoken "yes" first. The server only listens on 127.0.0.1.