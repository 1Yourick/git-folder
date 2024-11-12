import telebot
from telebot import types
from datetime import date, timedelta, datetime
import json
import locale
#для перевода дней недели
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
date_pattern = "%d.%m.%Y"
add = False #переменная записи на процедууру. True если хотят записаться
inputed_datetime = []# переменная для хранения даты и времени на которое хотят записаться
token = '7762712132:AAGzzk_k5eOp_FDPn0B9ZJaUZoH7seo6pn8'
bot = telebot.TeleBot(token)

START_MESSAGE = '''Спасибо, что пользуетесь нашим сервисом'''

#получаем расписание на конкретный день если day = true или список ближайших дат
def get_schedule(cur_date:str = None, day = True):
    with open ('month.json', 'r', encoding='utf-8') as file:
        json_dict = json.load(file)
        if day:
            return json_dict[cur_date]
        else:
            return list(json_dict.keys())
#возвращаем список свободных окошек в определённый день
def free_time(schedule: dict[str, None]) -> list[str]:
    return [k for k,v in schedule.items() if v == None]
    

#проверка корректной даты в диапозоне 1 месяц 
def is_correct_date(s:str) -> str:
    try:
        inputed_date = datetime.strptime(s, date_pattern)
        if datetime.now() <= inputed_date <= datetime.now() + timedelta(days=31):
            return True
        else:
            return False
    except:
        return False
#Проверка корректного времени
def is_correct_time(time):
    return True if  time in ['9:00', '10:30', '12:00', '13:30', '15:00', '16:30', '18:00', '19:30'] else False

    
#Стартовое сообщение
@bot.message_handler(commands=['start', 'help'])
def main(message):
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Свободные окошки")
    btn2 = types.KeyboardButton("Записаться на процедуру")
    markup.add(btn1)
    markup.add(btn2)

    
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=markup)

# Выбор функции после нажатия на кнопки
@bot.message_handler(content_types=['text'])
def get_message(message):
    global add
    global inputed_datetime
    if message.text == 'Свободные окошки':
        add = False
        bot.send_message(message.chat.id, 'Скоро') 
        print(message) 
    elif message.text == 'Записаться на процедуру':
        add = True
        inputed_datetime.clear()
        bot.send_message(message.chat.id, f'Сегодня {date.today().strftime("%d.%m.%Y %A")}')
        date_choise(message)
    elif message.text == 'Спасибо' or message.text == 'В начало':
        main(message)

    elif is_correct_date(message.text):
        inputed_datetime.append(message.text)
        time_choise(message)
    elif is_correct_time(message.text):
        inputed_datetime.append(message.text)
        if new_record_in_json(inputed_datetime, message):
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('Спасибо')
            markup.add(btn)
            bot.send_message(message.chat.id, f'Вы записаны на процедуру {inputed_datetime[0]} в {inputed_datetime[1]}. Не опаздывайте.', reply_markup=markup)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton('В начало')
            markup.add(btn)
            bot.send_message(message.chat.id, 'Что-то пошло не так. Проверьте введённые данные и попробуйте ещё раз.', reply_markup=markup)
        


def date_choise(message):
    near_dates = get_schedule(day=False)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(near_dates)):
        btn = types.KeyboardButton(near_dates[i])
        markup.add(btn)
    bot.send_message(message.chat.id, 'Пожалуйста, выбирете дату для записи из списка', reply_markup=markup)

def time_choise(message):
    cur_date = message.text
    time_list = free_time(get_schedule(cur_date)) # получаем список свободного времени в введённое время
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(time_list)): #создаём кнопки со свободным временем
        btn = types.KeyboardButton(time_list[i])
        markup.add(btn)
    bot.send_message(message.chat.id, 'Выберите время', reply_markup=markup)

def new_record_in_json(inputed_datetime, message):   # запись в JSON на дату и время
    if len(inputed_datetime) != 2:
        return False
    with open ('month.json', 'r', encoding='utf-8') as file: #открыли старый JSON
        json_dict = json.load(file)
        dt, tm = inputed_datetime[0], inputed_datetime[1]#введённые дата и время

        f_name = message.from_user.first_name
        l_name = message.from_user.last_name
        id = message.from_user.id
        username =message.from_user.username 
        
        
        json_dict[dt][tm] = [f_name, l_name, username, id] #изменили словарь из JSON, на нужную дату добавили имя фамилию, юзернэйм, ид
    with open ('month.json', 'w', encoding='utf-8') as file:#сохранили новый словарь в JSON
        json.dump(json_dict, file, ensure_ascii=False)
    return True

bot.polling(non_stop=True)