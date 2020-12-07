import logging
from datetime import datetime
import re

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

def count_words(update, context):
    user_text = update.message.text.replace('/wordcount', '')
    user_text_cleaned = re.sub('[!?-_,.:;\'"/\[\]{}|@#$%^&*()=+<>~`]', ' ', user_text)
    user_text_stripped = re.sub(' +',' ',user_text_cleaned).strip()
    reply = 0
    if not user_text_stripped:
        reply = "Введите фразу из хотя бы одного слова!"
    elif user_text_stripped.replace(' ', '').isnumeric():
        reply = f"{user_text} - не фраза!"
    else:
        reply = len(user_text_stripped.split(' '))
    print(f'Word count for {user_text} is {reply}')
    update.message.reply_text(reply)


def main():

    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", print_constallation))
    dp.add_handler(CommandHandler("wordcount", count_words))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()