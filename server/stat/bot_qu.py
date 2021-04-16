import io
import sys
import time
from json import load
import telebot
import subprocess
from os import listdir, path
from os.path import isfile, join


PATH_DATAFILE = 'data'
file_conf = open('tbot_conf.json', 'r')
conf = load(file_conf)
bot = telebot.TeleBot(conf.get('token'))


@bot.message_handler(commands=['start'])
def command_help(message):
    run = "python3 qu.py &"
    sub = subprocess.Popen(run, shell=True, stdout=subprocess.PIPE)
    sub_return = sub.stdout.read()
    bot.reply_to(message, f"Script is running.\n{sub_return}")


@bot.message_handler(commands=['stop'])
def command_help(message):
    pid = int(message.text.split(' ', maxsplit=1)[1])
    stop = f"kill {pid}"
    bot.reply_to(message, f"Script is stopping.\n{stop}")


@bot.message_handler(commands=['show'])
def command_help(message):
    files = '\n'.join([f for f in listdir(PATH_DATAFILE) if isfile(join(PATH_DATAFILE, f)) and 'xlsx' in f])
    bot.reply_to(message, f"Files\n{files}")


@bot.message_handler(commands=['file'])
def command_help(message):
    user_want = message.text.split(' ', maxsplit=1)[1]

    path_to_file = '/'.join([path.dirname(sys.argv[0]), PATH_DATAFILE, user_want])

    try:
        with open(path_to_file, "rb") as misc:
            doc = io.BytesIO(misc.read())
            doc.name = user_want
        bot.send_document(message.chat.id, doc, reply_to_message_id=message.message_id)
    except Exception:
        bot.send_message(message.chat.id, f"Not found\n{path_to_file}")


bot.polling()


while True:
    time.sleep(5)
