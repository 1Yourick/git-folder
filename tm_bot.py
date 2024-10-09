import telebot
from telebot import types
from datetime import date, timedelta, time
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
  

bot.polling(non_stop=True)