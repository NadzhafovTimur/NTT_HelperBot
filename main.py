import telebot
import os
from dotenv import load_dotenv
from handlers.birthdays import register_birthday_handlers
from handlers.start import register_start_handlers


load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

register_start_handlers(bot)
register_birthday_handlers(bot)

bot.infinity_polling()