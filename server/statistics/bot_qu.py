import telebot
import time
import os

TOKEN = '<token_string>'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def command_help(message):
    pid = os.system("(python3 qu.py &)")
    bot.reply_to(message, "Script is running. PID ", pid)


@bot.message_handler(commands=['stop'])
def command_help(message):
    pid = os.system(f"kill {message}")
    bot.reply_to(message, "Script is stopping. ", message)


bot.polling()


while True: # Don't let the main Thread end.
    pass
