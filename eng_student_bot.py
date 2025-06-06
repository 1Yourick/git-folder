import telebot
from telebot import types
import json

token = '7189188824:AAFoIRw2UHNxM3eThMslpy7dNhaT4SvthAc'
path = 'git folder/students.json'
bot = telebot.TeleBot(token)
MSG_START = 'Рады приветствовать!'

states = dict()
current_student = ''
ids_messages_volabulary = []

def open_json(path = 'git folder/students.json'):
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_json(json_dict, path = 'git folder/students.json'):
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(json_dict,file, ensure_ascii=False)

#First message
@bot.message_handler(commands=['start', 'help'])
def main(message):
    states[message.chat.id] = 'auth'
    bot.send_message(message.chat.id, MSG_START)
    bot.send_message(message.chat.id, 'Please, enter your name as a teacher recorded you in a journal')
#authorization
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "auth" or states.get(message.chat.id) == None, content_types=['text'])
def authorization(message):
    global current_student
    print(message.text)
    json_dict = open_json()
    if message.text in json_dict:
        states[message.chat.id] = 'auth_done'
        bot.send_message(message.chat.id, 'Hi, ' + message.text)
        
        current_student = message.text
        first_buttons(message)
    else:
        bot.send_message(message.chat.id, "Sorry we can`t find student with this name.\nPlease, contact the teacher.")

@bot.message_handler(func=lambda message: states.get(message.chat.id) == "auth done" or states.get(message.chat.id) == None, content_types=['text'])
def first_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('My lessons 📚')
    msg_text = 'TODO msg with information about new lessons'
    markup.add(btn1)
    bot.send_message(message.chat.id, msg_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "My lessons 📚", content_types=['text'])
def show_lessons(message):
    json_dict = open_json()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lesson in json_dict[current_student]['lessons']:
        btn = types.KeyboardButton(lesson)
        markup.add(btn)
    bot.send_message(message.chat.id, 'Your lessons: ', reply_markup=markup)


bot.polling(non_stop=True, timeout=123) 