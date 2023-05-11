import logging
import os
import requests
from time import sleep

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Bot
from telegram.ext import CommandHandler, Updater

from tracker.classes import Raip
from tracker.tracker import parse_last_raip

load_dotenv()
TOKEN = os.getenv('TOKEN')
secret_token = os.getenv('TOKEN')
bot = Bot(secret_token)
URL = 'https://api.thecatapi.com/v1/images/search'

hash = {
    'last_raip': Raip('', '', '', '', ''),
    'users_id': set()
}


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    if response.status_code == 200:
        response = response.json()
        random_cat = response[0].get('url')
        return random_cat


# def new_cat(update, context):
#     chat = update.effective_chat
#     context.bot.send_photo(chat.id, get_new_image())


def get_raip(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/get_raip']], resize_keyboard=True)
    context.bot.send_message(
        chat.id, hash['last_raip'].href, reply_markup=button)


def wake_up(update, context):
    chat = update.effective_chat
    hash['users_id'].add(chat.id)
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/get_raip']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=(
            'Привет, {}. Вот действующая редакция РАИП '.format(name)
            + hash['last_raip'].href
        ),
        reply_markup=button
    )


if __name__ == '__main__':
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    # updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('get_raip', get_raip))
    updater.start_polling()
    updater.idle()
    while True:
        last_raip = parse_last_raip()
        if last_raip != hash.get('last_raip'):
            logging.info(f'Изменения: {last_raip}')
            hash['last_raip'] = last_raip
            for user_id in hash['users_id']:
                bot.send_message(user_id, last_raip.href)
        sleep(60)
