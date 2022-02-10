import sqlite3

import telebot
import time

TOKEN = '5250676031:AAH5cZ7YFzDdgyBS8ijK0l9AD1FKEVVTbrg'
bot = telebot.TeleBot(TOKEN)
conn = sqlite3.connect('hse_curator.db', check_same_thread=False)
cursor = conn.cursor()
name = ''
age = ''

# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#     if message.text == "Привет":
#         bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")
#     elif message.text == "/help":
#         bot.send_message(message.from_user.id, "Напиши привет")
#     else:
#         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if  message.text == "/reg":
        cursor.execute('SELECT tg_username FROM users WHERE tg_username=?', [str(message.from_user.username)])
        if cursor.fetchone():
            bot.send_message(message.from_user.id, "Ты уже зареган!")
        else:
            bot.send_message(message.from_user.id, "Введи свое имя:")
            bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Напиши /reg")

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.from_user.id, "Сколько те лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    global age
    age = int(message.text)
    bot.send_message(message.from_user.id, "Привет," + name + " Тебе " + str(age) + " лет \nТы зареган!")
    reg_to_db(message)

def reg_to_db(message):

    cursor.execute('INSERT INTO users (tg_username, person_name, points, answered_questions_id) VALUES (?, ?, ?, ?)', (str(message.from_user.username), name, 0, -1))
    conn.commit()


bot.polling(none_stop=True, interval=0)
