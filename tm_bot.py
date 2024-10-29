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
#получаем расписание на конкретный день
def get_day_schedule(cur_date:str) -> dict[str, None]:
    with open ('month.json', 'r', encoding='utf-8') as file:
        json_dict = json.load(file)
        return json_dict[cur_date]
#возвращаем список свободных окошек в определённый день
def free_time(schedule: dict[str, None]) -> list[str]:
    return [k for k,v in schedule.items() if v == None]
    

#проверка корректной даты в диапозоне 1 месяц 
def is_correct_date(s:str) -> str:
    try:
        inputed_date = datetime.strptime(s, date_pattern)
        if datetime.now() <= inputed_date <= datetime.now() + timedelta(days=31):
            return 'Correct'
        else:
            return 'Diaposon'
    except:
        return 'Uncorrect'
    
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
    #Прислали дату
    elif t := is_correct_date(message.text):
        cur_date = message.text
        bot.send_message(message.chat.id, t)
        if t == 'Correct':
            if add:
                add = False
                time_list = free_time(get_day_schedule(cur_date)) # получаем список свободного времени в введённое время
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in range(len(time_list)): #создаём кнопки со свободным временем
                    btn = types.KeyboardButton(time_list[i])
                    markup.add(btn)
                bot.send_message(message.chat.id, 'Выберите время', reply_markup=markup)
                #тут мы уже знаем корректную дату и юзер тыкает на определённое время на которое хочет записаться
                #TODO сделать запись по времени с сохранением в JSON
            else:
                pass # просмотр свободных мест
        elif t == 'Diaposon':
            pass
        elif t == 'Uncorrect':
            pass

def date_choise(message): #TODO запрашиваем дату, затем 8 кнопок с временем для записи. Открываем JSON редактируем и сохраняем.
    bot.send_message(message.chat.id, 'Введите дату в формате ДД.ММ.ГГГГ, пример: 13.02.2024')


bot.polling(non_stop=True)