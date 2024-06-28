import os
import django
import asyncio
from threading import Thread
from flask import Flask, request
import requests
from telegram import Update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

app = Flask(__name__)

from src.backend.management.commands.run_telegram_bot import start_bot

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}'

def send_message(chat_id, text):
    url = f'{TELEGRAM_API_URL}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    return response.json()

@app.route('/')
def home():
    return 'Bot is running'

@app.route(f'/telegram-webhook/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    update = Update.de_json(data, start_bot().bot)
    start_bot().dispatcher.process_update(update)
    return '', 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)

def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())

if __name__ == '__main__':
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    bot_thread.join()
    flask_thread.join()