from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Bot, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, Application
import os

from backend.constants import ALL_COMMANDS

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TELEGRAM_BOT_TOKEN)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        update = Update.de_json(request.json, bot)
        application.process_update(update)
    return JsonResponse({"status": "ok"})

def start(update, context):
    update.message.reply_text('Hello!')

async def post_init(application: Application) -> None:
    await application.bot.set_my_commands(ALL_COMMANDS)

application = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).post_init(post_init).build()
application.add_handler(CommandHandler("start", start))