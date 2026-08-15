import telebot
import os
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands = ["start", "help"])
def send_welkome(message):
    bot.reply_to(message, """
Привет я твой персональный помощник я помогу тебе чем смогу
""")

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()