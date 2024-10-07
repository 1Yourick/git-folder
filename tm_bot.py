import telebot
from telebot import types
import datetime
import locale
#для перевода дней недели
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

token = '7762712132:AAGzzk_k5eOp_FDPn0B9ZJaUZoH7seo6pn8'
bot = telebot.TeleBot(token)

START_MESSAGE = '''Text. Bot description.
Hello, I`m bot. I will help you to do something'''

#Стартовое сообщение
@bot.message_handler(commands=['start', 'help'])
def main(message):
   
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("key1")
    btn2 = types.KeyboardButton("key2")
    btn3 = types.KeyboardButton("key3")
    markup.add(btn1)
    markup.add(btn2)
    markup.add(btn3)
    
    bot.send_message(message.chat.id, START_MESSAGE, reply_markup=markup)

@bot.message_handler(commands=['key1'])
def button_message(message):
    bot.send_message(message.chat.id, 'hi 1')
@bot.message_handler(commands=['key2'])
def button_message(message):
    bot.send_message(message.chat.id, 'hi 2')
@bot.message_handler(commands=['key3'])
def button_message(message):
    bot.send_message(message.chat.id, 'hi 3')

week_list = list()
for i in range(8):
    week_list.append((datetime.date.today() + datetime.timedelta(days=i)).strftime('%d.%m.%Y %A'))

bot.polling(non_stop=True)