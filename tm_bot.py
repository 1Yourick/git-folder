import telebot
from telebot import types
from datetime import date, timedelta, datetime
import json
import locale
#для перевода дней недели
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
date_pattern = "%d.%m.%Y"
add = False #переменная записи на процедууру. True если хотят записаться
token = '7762712132:AAGzzk_k5eOp_FDPn0B9ZJaUZoH7seo6pn8'
bot = telebot.TeleBot(token)

START_MESSAGE = '''Text. Bot description.
Hello, I`m bot. I will help you to do something'''

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
def is_correct_time(message):
    pass
    
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
    if message.text == 'Свободные окошки':
        add = False
        bot.send_message(message.chat.id, 'Мест НЕТ !')  
    elif message.text == 'Записаться на процедуру':
        add = True
        bot.send_message(message.chat.id, 'Окей, записываемся на процедуру')
        bot.send_message(message.chat.id, f'Сегодня {date.today().strftime("%d.%m.%Y %A")}')
        date_choise(message)
    elif is_correct_date(message.text):
        time_choise(message)
    elif is_correct_time:
        pass #TODO запись в JSON


def date_choise(message):
    near_dates = get_schedule(day=False)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    print(near_dates)
    for i in range(len(near_dates)):
        btn = types.KeyboardButton(near_dates[i])
        markup.add(btn)
    bot.send_message(message.chat.id, 'Введите дату в формате ДД.ММ.ГГГГ, пример: 13.02.2024\nИли выбирете дату из списка', reply_markup=markup)

def time_choise(message):
    cur_date = message.text
    time_list = free_time(get_schedule(cur_date)) # получаем список свободного времени в введённое время
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for i in range(len(time_list)): #создаём кнопки со свободным временем
        btn = types.KeyboardButton(time_list[i])
        markup.add(btn)
    bot.send_message(message.chat.id, 'Выберите время', reply_markup=markup)


bot.polling(non_stop=True)