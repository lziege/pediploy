import os
import django
from threading import Thread
from flask import Flask, request
from telegram import Update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

app = Flask(__name__)

from src.backend.management.commands.run_telegram_bot import start_bot

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

application = start_bot()

@app.route('/')
def home():
    return 'Bot is running'

@app.route(f'/telegram-webhook/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def telegram_webhook():
    data = request.get_json()
    update = Update.de_json(data, application.bot)
    application.update_queue.put(update)
    return '', 200

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    flask_thread.join()