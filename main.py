#тг-бот
from pyowm import OWM
from datetime import datetime, date, time
import pyowm
import telebot
import forecast
import timestamps
from pyowm.utils import config
from pyowm.utils import timestamps

owm = OWM('e5f5c146af2a039f2c1a46d2986aa25b')
bot = telebot.TeleBot("1137909786:AAGI3jdc46-AIl1TcKqftksey6znyq8lU-o")

@bot.message_handler(commands = ['start'])
def welcome(message):
	sticker = open('welcome.webp', 'rb')
	bot.send_sticker(message.chat.id, sticker)

	bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот, который поможет тебе узнать текущую погоду или посмотреть прогноз погоды!🤓".format(message.from_user, bot.get_me()),
		parse_mode = 'html')
	bot.send_message(message.chat.id, "Для того, чтобы ознакомиться с возможностями бота - введите /help и сразу узнаете, на что он способен!😉")

@bot.message_handler(commands = ['help'])
def help(message):
	answer = "Данный бот содержит функционал: " + "\n"
	answer += "/start - команда начала работы с ботом" + "\n"
	answer += "/help - описание функционала и всех поддерживаемых команд" + "\n"
	answer += "/current - команда, демонстрирующая текущую погоду" + "\n"
	answer += "/forecast - команда, демонстрирующая прогноз погоды" + "\n"
	answer += "/sun - команда, демонстрирующая время восхода и захода солнца"

	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands = ['current'])
def current(message):
	cur = bot.send_message(message.chat.id, "Введите название города, в котором хотите узнать текущую погоду: ")
	bot.register_next_step_handler(cur, send_weather)

def send_weather(message):
	mgr = owm.weather_manager()
	observation = mgr.weather_at_place(message.text)
	w = observation.weather
	status = w.status
	temp = w.temperature('celsius')["temp"]
	deg = w.wind()["deg"]
	speed = w.wind()["speed"]
	hum = w.humidity
	sunrise_unix = w.sunrise_time(timeformat='date')

	if deg < 45 or deg > 315:
		wind = "северный"
	if deg > 45 and deg < 135:
		wind = "восточный"
	if deg > 135 and deg < 225:
		wind = "южный"
	if deg > 225 and deg < 315:
		wind = "западный"

	if status == "Clouds":
		status = "Облачно"
		sti_clouds = open('clouds.tgs', 'rb')
		bot.send_sticker(message.chat.id, sti_clouds)
	elif status == "Rain":
		status = "Дождь"
		sti_rain = open('rain.tgs', 'rb')
		bot.send_sticker(message.chat.id, sti_rain)
	elif status == "Mist":
		status = "Туман"
		sti_mist = open('mist.webp', 'rb')
		bot.send_sticker(message.chat.id, sti_mist)
	elif status == "Fog":
		status = "Туман"
		sti_mist = open('mist.webp', 'rb')
		bot.send_sticker(message.chat.id, sti_mist)

	if status == "Clear" and temp > 30:
		status = "Ясно"
		sti_clear = open('clear.tgs', 'rb')
		bot.send_sticker(message.chat.id, sti_clear)
	elif status == "Clear" and temp < 30:
		status = "Ясно"
		sti_clear = open('clear_less30.tgs', 'rb')
		bot.send_sticker(message.chat.id, sti_clear)

	answer = "В городе " + message.text  + " сейчас " + str(temp) + " градусов! " + "\n"
	answer += status + "\n"
	answer += "Ветер - " + wind + " со скоростью " + str(speed) + " м/с!" + "\n"
	answer += "Влажность - " + str(hum) + "%" + "\n"
	
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands = ['forecast'])
def forecast(message):
	forecast = bot.send_message(message.chat.id, "Введите название города, в котором хотите посмотреть прогноз погоды: ")
	bot.register_next_step_handler(forecast, send_forecast)

def send_forecast(message):
	mgr = owm.weather_manager()
	forecaster = mgr.forecast_at_place(message.text, '3h')
	start = forecaster.when_starts('date')
	end = forecaster.when_ends('date')
	tomorrow = timestamps.tomorrow()                                   
	rain = forecaster.will_be_rainy_at(tomorrow)   
	snow = forecaster.will_have_snow() 
	fog = forecaster.will_have_fog()
	cold = forecaster.most_cold()
	rainy = forecaster.most_rainy()

	if rain == False:
		rain = "Нет"
	else: 
		rain = "Да"

	if rainy == None:
		rainy = "Не будет"
	else:
		rainy = "Будет"

	if snow == False:
		snow = "Нет"
	else: 
		snow = "Да"

	if fog == False:
		fog = "Нет"
	else: 
		fog = "Да"

	answer = "Будет ли завтра дождь?: " + str(rain) + "\n"
	answer += "Прогноз на ближайшие 5 дней!" + "\n"
	answer += "Начало периода: " + str(start) + "\n" + "Конец периода: " + str(end) + "\n"
	answer += "Дождь: " + str(rainy) + "\n" + "Снег: " + str(snow) + "\n" + "Туман: " + str(fog) + "\n"
	
	sti_forecast = open('forecast.webp', 'rb')
	bot.send_sticker(message.chat.id, sti_forecast)
	bot.send_message(message.chat.id, answer)

@bot.message_handler(commands = ['sun'])
def sun_city(message):
	sun = bot.send_message(message.chat.id, "Введите название города, где хотите узнать время восхода и захода солнца: ")
	bot.register_next_step_handler(sun, send_suntime)

def send_suntime(message):
	mgr = owm.weather_manager()
	suntime = mgr.weather_at_place(message.text)
	w = suntime.weather
	sunrise_date = w.sunrise_time(timeformat ='date')
	sunset_date = w.sunset_time(timeformat ='date')

	answer = "Время восхода солнца в городе " + str(message.text) + ":" + "\n" + str(sunrise_date) + "\n"
	answer += "Время захода солнца в городе " + str(message.text) + ":" + "\n" + str(sunset_date) + "\n"

	sti_sun = open('sun.tgs', 'rb')
	bot.send_sticker(message.chat.id, sti_sun)
	bot.send_message(message.chat.id, answer)

@bot.message_handler(content_types = ['text'])
def wrong_command(message):
	answer = "Команда введена не правильно, либо не существует! " + "\n" + "Введите /help и узнайте возможности бота."
	bot.send_message(message.chat.id, answer)

bot.polling( none_stop = True)