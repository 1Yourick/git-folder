import telebot
from telebot import types
from datetime import date, timedelta, datetime
import json
import locale
#для перевода дней недели
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
date_pattern = "%d.%m.%Y"

token = '7762712132:AAGzzk_k5eOp_FDPn0B9ZJaUZoH7seo6pn8'
bot = telebot.TeleBot(token)

START_MESSAGE = '''Text. Bot description.
Hello, I`m bot. I will help you to do something'''

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
    if message.text == 'Свободные окошки':
        bot.send_message(message.chat.id, 'Мест НЕТ !')  
    elif message.text == 'Записаться на процедуру':
        bot.send_message(message.chat.id, 'Окей, записываемся на процедуру')
        bot.send_message(message.chat.id, f'Сегодня {date.today().strftime("%d.%m.%Y %A")}')
        date_choise(message)

def date_choise(message): #TODO запрашиваем дату, затем 8 кнопок с временем для записи. Открываем JSON редактируем и сохраняем.
    bot.send_message(message.chat.id, 'Введите дату в формате ДД.ММ.ГГГГ, пример: 13.02.2024')




#Создание JSON файла с расписанием на месяц. Словарь[дата][время] = none
day_shedule = {'9:00':None, '10:30':None, '12:00':None, '13:30':None, '15:00':None, '16:30':None, '18:00':None, '19:30':None} #расписание на день
month_shedule = {}
now = datetime.now()
for d in range(30):
    month_shedule[(now + timedelta(days=d)).strftime(date_pattern)] = day_shedule.copy()

with open ('month.json', 'w', encoding='utf-8') as file:
    json.dump(month_shedule, file)
#Конец создания json




bot.polling(non_stop=True)