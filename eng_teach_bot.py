import telebot
from telebot import types
import json

token = '8066145939:AAElzyCi2vv0VgzREzDXyu3wyzFndxv2oBo'
PASSWORD = '222'

bot = telebot.TeleBot(token)
msg_start_message = 'Hi!\nAll systems work.\nHave a good day'
msg_hello_message = 'Hello dear teacher'
msg_wrong_password = 'Wrong password'
states = {}
students = []
path = 'git folder/students.json'


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
    bot.send_message(message.chat.id, msg_start_message)
    bot.send_message(message.chat.id, 'Please, enter password')
#authorization
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "auth" or states.get(message.chat.id) == None, content_types=['text'])
def authorization(message):
    print(message.text)
    if message.text == PASSWORD:
        states[message.chat.id] = 'auth_done'
        first_buttons(message)
    else:
        bot.send_message(message.chat.id, msg_wrong_password)


#send buttons
def first_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("My students 📖")
    btn2 = types.KeyboardButton("Add new student")
    markup.add(btn1)
    markup.add(btn2)

    bot.send_message(message.chat.id,text = msg_hello_message, reply_markup=markup)

# two func for show students
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "student list", content_types=['text'])
def show_students(message):
    json_dict = open_json()
    if message.text == 'Add lesson':
        pass
    elif message.text == 'Remove lesson':
        pass
    elif message.text not in json_dict.keys():
        states[message.chat.id] = 'auth_done'
        bot.send_message(message.chat.id, 'Student not found')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        #TODO вывод сообщения с информацией об уроках.
        INFO_TEXT = f'''Здесь будет иинформация об уроках(словарях)'''
        btn1 = types.KeyboardButton('Add lesson')
        btn2 = types.KeyboardButton('Remove lesson')
        markup.add(btn1)
        markup.add(btn2)
        bot.send_message(message.chat.id, INFO_TEXT, reply_markup=markup)

    
@bot.message_handler(func=lambda message: message.text == 'My students 📖', content_types=['text'])
def show_students(message):
    states[message.chat.id] = 'student list'
    #show buttons with students
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    json_dict = open_json()
    for user in json_dict:
        btn = types.KeyboardButton(user)
        markup.add(btn)
    bot.send_message(message.chat.id, 'Students list:', reply_markup=markup)

# two func for add students
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "add student", content_types=['text'])
def add_students(message):
    #add new student in json
    json_file = open_json()
    json_file[message.text] = dict()
    save_json(json_file)

    bot.send_message(message.chat.id, f'Student {message.text} added in students list')
    states[message.chat.id] = 'auth_done'
@bot.message_handler(func=lambda message: message.text == 'Add new student', content_types=['text'])
def add_students(message):
    states[message.chat.id] = 'add student' 
    bot.send_message(message.chat.id, 'Write student name\nExample: Michael Jackson')

bot.polling(non_stop=True, timeout=123)