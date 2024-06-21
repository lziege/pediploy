from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update
import os
from src.backend.management.commands.run_telegram_bot import applicationBuilder

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.json, bot)
        applicationBuilder.process_update(update)
    return JsonResponse({"status": "ok"})

def index(request):
    return HttpResponse("¡Hola desde la aplicación Django en Vercel!")