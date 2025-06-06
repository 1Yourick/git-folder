import telebot
from telebot import types
import json

token = '8066145939:AAElzyCi2vv0VgzREzDXyu3wyzFndxv2oBo'
PASSWORD = '222'

bot = telebot.TeleBot(token)
msg_start_message = 'Hi!\nAll systems work.\nHave a good day'
msg_hello_message = 'Hello 👋'
msg_wrong_password = 'Wrong password'
states = {}
students = []
path = 'git folder/students.json'
current_student = None
current_lesson = None
EXAMPLE_ADD ='''Write list of words like on example:
Word - Translate
Car - Машина
Elephant - Слон'''

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
def show_students_actions(message):
    global current_student
    current_student = message.text
    json_dict = open_json()
    
    if message.text not in json_dict.keys():
        states[message.chat.id] = 'auth_done'
        bot.send_message(message.chat.id, 'Student not found')
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # вывод сообщения с информацией об уроках.
        INFO_TEXT = ''
        if len(json_dict[current_student]['lessons']) > 0:
            for lesson in json_dict[current_student]['lessons']:
                INFO_TEXT += " 🟣 " + lesson + '\n'
                attempts = len(json_dict[current_student]['lessons'][lesson]['result'])
                if attempts > 0:
                    best_result = max(json_dict[current_student]['lessons'][lesson]['result'])
                else:
                    best_result = '⛔ No data'
                INFO_TEXT += '   Best result: ' + str(best_result) + '% 💯 ' + '\n'
                INFO_TEXT += '   Number of attempts: ' + str(attempts) + '\n'
                INFO_TEXT += '\n'
        else:
            INFO_TEXT = 'Student doesn`t have a lessons'
        btn1 = types.KeyboardButton('Add lesson')
        btn2 = types.KeyboardButton('Lessons list')
        btn3 = types.KeyboardButton('Back 🔙')
        markup.add(btn1)
        markup.add(btn2)
        markup.add(btn3)
        bot.send_message(message.chat.id, INFO_TEXT, reply_markup=markup)
        states[message.chat.id] = 'student action'
    
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
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "add student" and message.text != 'Add new student', content_types=['text'])
def add_students(message):
    #add new student in json
    json_file = open_json()
    json_file[message.text] = dict()
    json_file[message.text].setdefault('lessons', dict())
    save_json(json_file)

    bot.send_message(message.chat.id, f'Student {message.text} added in students list')
    states[message.chat.id] = 'auth_done'
@bot.message_handler(func=lambda message: message.text == 'Add new student', content_types=['text'])
def add_students(message):
    states[message.chat.id] = 'add student' 
    bot.send_message(message.chat.id, 'Write student name\nExample: Michael Jackson')

#action processing
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "student action", content_types=['text'])
def students_action(message):
    if message.text == 'Add lesson':
        bot.send_message(message.chat.id, 'Write lesson name\nExample: Tourism')
        states[message.chat.id] = 'create_lesson'
    elif message.text == 'Lessons list':
        json_dict = open_json()
        markup = types.ReplyKeyboardMarkup(resize_keyboard= True)
        if len(json_dict[current_student]['lessons'].keys()) == 0:
            bot.send_message(message.chat.id, 'Lessons list is empty')
            show_students(message)
            return
        for lesson in json_dict[current_student]['lessons'].keys():
            btn = types.KeyboardButton(lesson)
            markup.add(btn)
        bot.send_message(message.chat.id, 'Lessons list', reply_markup=markup)
        states[message.chat.id] = 'choice lesson'
    elif message.text == 'Back 🔙':
        states[message.chat.id] = 'auth_done'
        first_buttons(message)
#func for create new lesson and add lesson name
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "create_lesson", content_types=['text'])
def create_new_lesson(message):
    global current_lesson
    json_dict = open_json()
    current_lesson = message.text
    json_dict[current_student]['lessons'].setdefault(current_lesson, dict())
    json_dict[current_student]['lessons'][current_lesson].setdefault('result', list())
    json_dict[current_student]['lessons'][current_lesson].setdefault('dict', dict())
    save_json(json_dict)
    bot.send_message(message.chat.id, EXAMPLE_ADD)
    states[message.chat.id] = 'add words'

#func for adding new words in current lesson
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "add words", content_types=['text'])
def add_new_words(message):
    pairs = message.text.split('\n')
    json_dict = open_json()
    for pair in pairs:
        en,ru = pair.split('-')
        json_dict[current_student]['lessons'][current_lesson]['dict'].setdefault(en.strip(), ru.strip())
    save_json(json_dict)
    bot.send_message(message.chat.id, "New words sucsesfully added!")
    #TODO проверка на тире. Разные Тире.
    states[message.chat.id] = 'auth_done'
    first_buttons(message)

#func with action in lesson
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "choice lesson", content_types=['text'])
def lesson_actions(message):
    global current_lesson

    json_dict = open_json()
    if message.text not in json_dict[current_student]['lessons']:
        bot.send_message(message.chat.id, 'Lesson not found')
        states[message.chat.id] = 'auth_done'
        first_buttons(message)

        return
    else:
        current_lesson = message.text

    text = ''
    for en, ru in json_dict[current_student]['lessons'][current_lesson]['dict'].items():
        text += en + ' - ' + ru + '\n'

    #if lesson without words
    if len(text) == 0:
        text = 'Lesson is empty'
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Back')
    btn2 = types.KeyboardButton('Remove lesson ❌')
    markup.add(btn1)
    markup.add(btn2)
    bot.send_message(message.chat.id, text,reply_markup=markup)
    states[message.chat.id] = 'lesson actions'

#func with action in lesson
@bot.message_handler(func=lambda message: states.get(message.chat.id) == "lesson actions", content_types=['text'])
def lesson_actions(message):
    if message.text == 'Remove lesson ❌':
        json_dict = open_json()
        del json_dict[current_student]['lessons'][current_lesson]
        save_json(json_dict)
        bot.send_message(message.chat.id, 'Lesson succesfully removed')
    
    states[message.chat.id] = 'auth_done'
    first_buttons(message) 

bot.polling(non_stop=True, timeout=123)