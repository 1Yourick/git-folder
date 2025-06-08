import telebot
from telebot import types
import json
import random

token = '7189188824:AAFoIRw2UHNxM3eThMslpy7dNhaT4SvthAc'
path = 'git folder/students.json'
bot = telebot.TeleBot(token)
MSG_START = 'Рады приветствовать!'

states = dict()
current_student = ''
current_lesson = ''
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
    states[message.chat.id] = 'choise lesson'

#show lesson topic
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "choise lesson" , content_types=['text'])
def choise_lesson(message):
    global current_lesson
    json_dict = open_json()
    # pressed button back or testing
    if message.text == 'Testing 📕':
        states[message.chat.id] = 'testing'
        testing_1(message)
    elif message.text == 'Back 🔙':
        states[message.chat.id] = 'auth_done'
        first_buttons(message)
    #entered correct lesson
    elif message.text in json_dict[current_student]['lessons']:
        text = ''
        current_lesson = message.text
        for en, ru in json_dict[current_student]['lessons'][current_lesson]['dict'].items():
            text += en + ' - ' + ru + '\n'
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_back = types.KeyboardButton('Back 🔙')
        btn_testing = types.KeyboardButton('Testing 📕')
        markup.add(btn_back)
        markup.add(btn_testing)

        msg = bot.send_message(message.chat.id, '📖' + message.text  + ':\n\n' + text, reply_markup=markup)
        ids_messages_volabulary.append(msg.id)
    else:
        #entered uncorrect lesson
        bot.send_message(message.chat.id, 'We can`t find this lesson. Choise from list.')
        show_lessons(message)

#start testing
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "testing", content_types=['text'])
def testing_1(message):
    #first start this func
    if message.text == 'Testing 📕':
        json_dict = open_json()
        pairs = list(json_dict[current_student]['lessons'][current_lesson]['dict'].items())
        #delete messages with words
        bot.delete_messages(message.chat.id, ids_messages_volabulary)
        ids_messages_volabulary.clear()
        random.shuffle(pairs)
        pair = pairs.pop()
        states[message.chat.id]='testing2'
        bot.send_message(message.chat.id, 'Now I will send you words, you must send me a translation of these words')
        bot.send_message(message.chat.id, pair[0])
        testing_2(message, pairs, pair, lang='0' )

@bot.message_handler(func=lambda message: states.get(message.chat.id) == "testing2", content_types=['text'])
def testing_2(message, pairs, pair, lang):
    if lang == '0':
        if pair[1].lower() == message.text():
            pass #correct answer
        else:
            bot.send_message(message.chat.id, 'Wrong answer')
    if lang == '1':
        if pair[0].lower() == message.text():
            pass #correct answer
        else:
            bot.send_message(message.chat.id, 'Wrong answer')

#TODO доделать тесты, у еня голова уже не думает

        
bot.polling(non_stop=True, timeout=123) 