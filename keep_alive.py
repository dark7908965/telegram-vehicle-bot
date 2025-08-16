from flask import Flask
from threading import Thread
import requests
import time
import os

app = Flask('')

@app.route('/')
def home():
    return "🤖 Telegram Bot is running! ✅"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# Auto-ping to keep alive
def ping_self():
    while True:
        try:
            # Replace with your repl URL
            repl_url = os.getenv('REPLIT_URL', 'https://your-repl.replit.dev')
            requests.get(repl_url)
            print("🔄 Keep alive ping sent")
        except:
            pass
        time.sleep(300)  # Ping every 5 minutes

def start_ping():
    t = Thread(target=ping_self)
    t.daemon = True
    t.start()
