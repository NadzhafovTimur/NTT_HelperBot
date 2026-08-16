import telebot
import schedule
import os
import threading
import time

from dotenv import load_dotenv
from handlers.birthdays import register_birthday_handlers, check_and_notify_birthdays
from handlers.start import register_start_handlers


load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

def run_scheduler():
    schedule.every().day.at("00:00").do(check_and_notify_birthdays, bot)
    schedule.every().day.at("23:00").do(check_and_notify_birthdays, bot)
    while True:
        schedule.run_pending()
        time.sleep(30)
scheduler_thread = threading.Thread(target = run_scheduler, daemon = True)
scheduler_thread.start()

register_start_handlers(bot)
register_birthday_handlers(bot)

bot.infinity_polling()