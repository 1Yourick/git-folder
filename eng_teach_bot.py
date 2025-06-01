import telebot
from telebot import types

token = '8066145939:AAElzyCi2vv0VgzREzDXyu3wyzFndxv2oBo'
PASSWORD = '222'

bot = telebot.TeleBot(token)
msg_start_message = 'Hi!\nAll systems work.\nHave a good day'
msg_hello_message = 'Hello dear teacher'
msg_wrong_password = 'Wrong password'
states = {}
students = []


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

@bot.message_handler(commands=['My students 📖'])
def show_students(message):
    pass
#TODO отображение студентов

@bot.message_handler(commands=['Add new student'])
def add_students(message):
    pass
#TODO отображение студентов


bot.polling(non_stop=True, timeout=123)