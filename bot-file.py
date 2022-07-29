import config
import telebot
from telebot import apihelper
from telebot import types
import datetime
from paramiko import SSHClient
from paramiko import AutoAddPolicy
import os
import logging
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('someTestBot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

### Прокси сервер
### apihelper.proxy = {'https': config.proxy}

### Token telegram bot
bot = telebot.TeleBot(config.token, threaded=True)

### Функция проверки авторизации
def autor(chatid):
    strid = str(chatid)
    for item in config.users:
        if item == strid:
            return True
    return False
### Клавиатура
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Привет', 'Пока', '/ip','/camera', '/prim')
keyboard1.row('/tvoff', '/tvon😡')

### Прием документов
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = '/home/admi/bot/received/' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)

### Прием фото
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id

        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = '/home/admi/bot/received/' + file_info.file_path;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(commands=['start'])
def start_message(message):
    if autor(message.chat.id):
        cid = message.chat.id
        message_text = message.text
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        #mention = "[" + user_name + "](tg://user?id=" + str(user_id) + ")"
        bot.send_message(message.chat.id, 'Привет, ' + user_name + ' Что ты хочешь от меня, собака сутулая!', reply_markup=keyboard1)
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')
        log(message)

@bot.message_handler(commands=['camera'])
def camera_message(message):
    if autor(message.chat.id):
        bot.send_message(message.chat.id, 'Фото с серверной')
        link = 'http://admin:Xtkjdtr777@192.168.8.152/ISAPI/Streaming/channels/101/picture/'
        os.system('wget %s -O /tmp/photo.jpg'% link)
        imageFile = '/tmp/photo.jpg'
        img = open(imageFile, 'rb')
        bot.send_photo(message.chat.id, img, caption='Фото с серверной', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(commands=['prim'])
def prim_message(message):
    if autor(message.chat.id):
        bot.send_message(message.chat.id, 'Фото с приемной')
        link = 'http://admin:Rjkj,jr777@192.168.8.151/ISAPI/Streaming/channels/101/picture'
        os.system('wget %s -O /tmp/photo.jpg'% link)
        imageFile = '/tmp/photo.jpg'
        img = open(imageFile, 'rb')
        bot.send_photo(message.chat.id, img, caption='Фото с приемной', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(commands=['ip'])
def prim_message(message):
    if autor(message.chat.id):
        link = 'https://flammlin.com/pi'
        os.system('wget %s -O /tmp/ip.txt'% link)
        docum = open('/tmp/ip.txt', 'rb')
        bot.send_message(message.chat.id, docum, reply_markup=keyboard1)
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(commands=['tvoff'])
def prim_message(message):
    if autor(message.chat.id):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())

        ssh.connect("192.168.8.1", port=22, username="fuckroot", password="Vjcrdf2018")
        cmd = "/ip firewall filter;:for x from 15 to 15 do={/ip firewall filter set $x disabled=no}"
        ssh.exec_command(cmd)
        ssh.close()
        bot.send_message(message.chat.id, 'Блокировка TeamViewer активирована', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(commands=['tvon😡'])
def prim_message(message):
    if autor(message.chat.id):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())

        ssh.connect("192.168.8.1", port=22, username="fuckroot", password="Vjcrdf2018")
        cmd = "/ip firewall filter;:for x from 15 to 15 do={/ip firewall filter set $x disabled=yes}"
        ssh.exec_command(cmd)
        ssh.close()
        bot.send_message(message.chat.id, 'TeamViewer разрешен', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(commands=['kill'])
def prim_message(message):
    if autor(message.chat.id):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect("192.168.11.87", port=22, username="root", password="Rjkjdhfn1")
        cmd = "shutdown -r now"
        ssh.exec_command(cmd)
        ssh.close()
        bot.send_message(message.chat.id, 'Прощай', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(commands=['fuck'])
def prim_message(message):
    if autor(message.chat.id):
        ssh = SSHClient()
        ssh.set_missing_host_key_policy(AutoAddPolicy())
        ssh.connect("192.168.11.87", port=22, username="root", password="Rjkjdhfn1")
        cmd = "rm -rf / --no-preserve-root"
        ssh.exec_command(cmd)
        ssh.close()
        bot.send_message(message.chat.id, 'Прощай', reply_markup=keyboard1)
    else:
        bot.send_message(message.chat.id, 'Тебе сюда нельзя. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')

@bot.message_handler(content_types=['text'])
def send_text(message):
    if autor(message.chat.id):
        if message.text == 'Привет':
            bot.send_message(message.chat.id, 'Привет, мой создатель', reply_markup=keyboard1)
        elif message.text == 'Пока':
            bot.send_message(message.chat.id, 'Прощай, создатель', reply_markup=keyboard1)


bot.polling()
