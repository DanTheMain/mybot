import logging
from datetime import datetime

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import settings
import ephem

logging.basicConfig(filename='bot.log', level=logging.INFO)
PROXY = {'proxy_url': settings.PROXY_URL, 
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 
                                  'password': settings.PROXY_PASSWORD}}

def greet_user(update, context):
    print('Вызван /start')
    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')

def talk_to_me(update, context):
    user_text = update.message.text 
    print(user_text)
    update.message.reply_text(user_text)

def print_constallation(update, context):
    planet_name = update.message.text.split()[1]
    date = datetime.date(datetime.now())
    constellation = 'not supported'
    if planet_name.lower() == 'mars':
        constellation = ephem.constellation(ephem.Mars(date))
    elif planet_name.lower() == 'mercury':
        constellation = ephem.constellation(ephem.Mercury(date))
    elif planet_name.lower() == 'venus':
        constellation = ephem.constellation(ephem.Venus(date))
    elif planet_name.lower() == 'jupiter':
        constellation = ephem.constellation(ephem.Jupiter(date))
    elif planet_name.lower() == 'saturn':
        constellation = ephem.constellation(ephem.Saturn(date))
    elif planet_name.lower() == 'uranus':
        constellation = ephem.constellation(ephem.Uranus(date))
    elif planet_name.lower() == 'neptune':
        constellation = ephem.constellation(ephem.Neptune(date))
    update.message.reply_text(f"Planet: {planet_name.capitalize()}, date: {date}, constellation: {constellation}")

def main():

    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", print_constallation))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")


    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()