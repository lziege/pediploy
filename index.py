import os
import django
import asyncio
from threading import Thread
from flask import Flask
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'src.settings')
django.setup()

from src.backend.management.commands.run_telegram_bot import start_bot, applicationBuilder

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

app = Flask(__name__)

@app.route('/')
def home():
    return 'Bot is running'

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.json, bot)
        applicationBuilder.process_update(update)
    return JsonResponse({"status": "ok"})

def index(request):
    return HttpResponse("¡Hola desde la aplicación Django en Vercel!")

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