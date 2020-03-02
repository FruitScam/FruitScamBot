import telebot
from telebot import *
import csv
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

'''
	Дорогой программист, если ты читаешь это,
	да прибудет с тобой Бог, ибо кроме меня, 
	только он знает, как работает этот код, удачи.
'''
bot = telebot.TeleBot("1046202079:AAHvG98Gv-oj_8nVJMQwAkUXvrcgVY3X7QA")
name = ''
surname = ''
age = ''
logs_path = "logs.csv"
t=''

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '🍒Выбери нужное действие с помощью кнопок ниже',reply_markup=keyboard1())

@bot.message_handler(content_types=['text'])
def start(message):
	if message.text == '✅Добавить✅':
		bot.send_message(message.from_user.id, "🔗Ссылка🔗",reply_markup=keyboard3())
		bot.register_next_step_handler(message, get_link)#каскадный вызов функций
	elif message.text == '🔎Поиск🔎':
		bot.send_message(message.chat.id,"🔗Ссылка🔗",reply_markup=keyboard3())###################################################################################################################################################################################################################################################################################################################################################################################################################################
		bot.register_next_step_handler(message,search)
	else:
		bot.send_message(message.from_user.id, 'Выбери нужное действие с помощью кнопок ниже',reply_markup=keyboard1())

def get_link(message):
	global t
	if message.text == '❌Отмена❌':
		t=''
		bot.send_message(message.from_user.id,'❌Ввод отменён❌',reply_markup=keyboard1())
		return None
	t+=message.text+'\n'
	bot.send_message(message.from_user.id, '📍Площадка📍',reply_markup=keyboard2())
	bot.register_next_step_handler(message, get_platform)

def get_platform(message):
	global t
	if message.text == '❌Отмена❌':
		t=''
		bot.send_message(message.from_user.id,'❌Ввод отменён❌',reply_markup=keyboard1())
		return None
	t+=message.text+'\n'
	bot.send_message(message.from_user.id,'❗Причина❗',reply_markup=keyboard3())
	bot.register_next_step_handler(message, get_status)

def get_status(message):
	global t
	if message.text == '❌Отмена❌':
		t=''
		bot.send_message(message.from_user.id,'❌Ввод отменён❌',reply_markup=keyboard1())
		return None
	t+=message.text
	logs_data = [t.split("\n")]
	csv_writer(logs_path,logs_data)
	bot.send_message(message.chat.id,"✅Запись добавлена✅",reply_markup=keyboard1())
	t=''

def search(message):
	#global t
	global logs_path
	t=message.text
	res=[]
	res=csv_reader(logs_path,t)
	if(res!=""):
		print('Вывод: ')
		for sub in res:
			print(*sub)
			st=""
			for i in sub: 
				st+=i+'\n'
			bot.send_message(message.chat.id,st, disable_web_page_preview=True)
		bot.send_message(message.chat.id,"🔎Результатов: "+str(len(res)),reply_markup=keyboard1())	

def csv_writer(path,data):
	with open(path, "a", newline='') as csv_file:
		writer = csv.writer(csv_file, delimiter='~')
		for line in data:
				writer.writerow(line)

def csv_reader(path,obj):
	with open(path, "r", newline='') as csv_file:
		reader = csv.reader(csv_file, delimiter='~')
		j=0
		ress=[]
		for row in reader:
			if (row[0]==obj):
				ress.insert(j,row)
				j+=1
	print(ress)
	return ress


def keyboard1():#клавиатура
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	btn1 = types.KeyboardButton('✅Добавить✅')
	btn2 = types.KeyboardButton('🔎Поиск🔎')
	markup.row(btn1, btn2)
	return markup

def keyboard2():#клавиатура
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	btn1 = types.KeyboardButton('Юла')
	btn2 = types.KeyboardButton('Авито')
	btn3 = types.KeyboardButton('❌Отмена❌')
	markup.row(btn1, btn2).add(btn3)
	return markup

def keyboard3():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
	btn1 = types.KeyboardButton('❌Отмена❌')
	markup.row(btn1)
	return markup

if __name__ == '__main__':
	bot.polling(none_stop=True)
