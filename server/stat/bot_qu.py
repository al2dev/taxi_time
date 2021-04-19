import io
import sys
import time
from json import load
import telebot
import subprocess
import platform
from os import listdir, path, system
from os.path import isfile, join


# Name files
TCONF_FILE = 'tbot_conf.json'


# Paths
ABS_MODULE_PATH = path.abspath('')
ABS_DATA_STORAGE_PATH = path.abspath('data')
ABS_TCONF_FILE_PATH = '\\'.join([ABS_MODULE_PATH, TCONF_FILE]) if platform.system() == 'Windows' else '/'.join([ABS_MODULE_PATH, TCONF_FILE])

file_conf = open(ABS_TCONF_FILE_PATH, 'r')
conf = load(file_conf)


bot = telebot.TeleBot(conf.get('token'))


@bot.message_handler(commands=['start'])
def command_help(message):
    get_pid = "pgrep python3"
    run = "(python3 qu.py &)"

    sub_pid = subprocess.Popen(get_pid, shell=True, stdout=subprocess.PIPE)
    before_pid = sub_pid.stdout.read()

    system(run)

    sub_pid = subprocess.Popen(get_pid, shell=True, stdout=subprocess.PIPE)
    after_pid = sub_pid.stdout.read()

    bot.reply_to(message, f"Script is running.\n{after_pid}\n{before_pid}")


@bot.message_handler(commands=['stop'])
def command_help(message):
    pid = int(message.text.split(' ', maxsplit=1)[1])
    stop = f"kill {pid}"
    bot.reply_to(message, f"Script is stopping.\n{stop}")


@bot.message_handler(commands=['show'])
def command_help(message):
    files = '\n'.join([f for f in listdir(ABS_DATA_STORAGE_PATH) if isfile(join(ABS_DATA_STORAGE_PATH, f)) and 'xlsx' in f])
    bot.reply_to(message, f"Files\n{files}")


@bot.message_handler(commands=['file'])
def command_help(message):
    user_want = message.text.split(' ', maxsplit=1)[1]

    path_to_file = '/'.join([path.dirname(sys.argv[0]), ABS_DATA_STORAGE_PATH, user_want])

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
