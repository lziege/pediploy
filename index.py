import os
import django
import asyncio
from threading import Thread
from flask import Flask, request
from django.http import JsonResponse
import requests
from telegram import Bot

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

from src.backend.management.commands.run_telegram_bot import start_bot, applicationBuilder

app = Flask(__name__)

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

@app.route('/telegram-webhook/', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')

        if text:
            response_text = f"Recibí tu mensaje: {text}"
            send_message(chat_id, response_text)

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