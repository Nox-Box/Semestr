import logging
 
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
 
from pyowm import OWM
from pyowm.utils.config import get_default_config
 
def main() -> None:
    updater = Updater("1757924540:AAGWOXn0qJYYqenJ7MNNyDNVTqjPj0JUfio")
    dispatcher = updater.dispatcher
 
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
 
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_message))
 
    updater.start_polling()
    updater.idle()
 

config_dict = get_default_config()  # Инициализация get_default_config()
config_dict['language'] = 'ru'  # Установка языка
 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)
 
 
def weather(place):  # Функция с выводом погоды
    owm = OWM('d13683afdd6a88eb0ba7d3caacb33707')  #  Ключ с сайта open weather map
    mgr = owm.weather_manager()  # Инициализация owm.weather_manager()
    observation = mgr.weather_at_place(place)
    # Инициализация mgr.weather_at_place() И передача в качестве параметра туда страну и город
 
    w = observation.weather
 
    status = w.detailed_status  # Узнаём статус погоды в городе и записываем в переменную status
    w.wind()  # Узнаем скорость ветра
    humidity = w.humidity  # Узнаём Влажность и записываем её в переменную humidity
    temp = w.temperature('celsius')['temp']  # Узнаём температуру в градусах по цельсию и записываем в переменную temp
 
    return ("В городе " + str(place) + " сейчас " + str(status) +  # Выводим город и статус погоды в нём
            "\nТемпература " + str(
                round(temp)) + " градусов по цельсию" +  # Выводим температуру с округлением в ближайшую сторону
            "\nВлажность составляет " + str(humidity) + "%" +  # Выводим влажность в виде строки
            "\nСкорость ветра " + str(w.wind()['speed']) + " метров в секунду")  # Узнаём и выводим скорость ветра
 
 
def start(update: Update, _: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Если ты хочешь узнать погоду в какому нибудь городе, напиши мне название города'
    )
 
 
def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Если ты хочешь узнать погоду в своём городе напиши мне свой город!\nК примеру: Харьков")
 
 
def check_message(update: Update, _: CallbackContext) -> None:
    text = update.message.text
    print('Пользователь написал', text)
    try:
        update.message.reply_text(weather(text))
    except Exception as e:
        print(e)
        update.message.reply_text("Я вас не понял, если вам нужна помощь введите команду /help")
 
 
if __name__ == '__main__':
    main()