import logging
import os
from time import sleep

import requests
from configs import configure_logging
from dotenv import load_dotenv
from outputs import file_output, get_last_raip, get_users, save_raip
from settings import DELAY, GREETING, SLEEP, BotConstants
from telegram import Bot
from telegram.ext import CommandHandler, Updater

from tracker import parse_last_raip

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(TOKEN)

cache = {}


def get_new_image():
    try:
        response = requests.get(BotConstants.URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        response = requests.get(BotConstants.RESERVE_URL)
    if response.status_code == 200:
        response = response.json()
        random_cat = response[0].get('url')
        return random_cat


def new_cat(update, context):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image())
    logging.info(
        f'Отправлена фотка пользователю: {update.message.chat.first_name}')


def get_raip(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, cache['last_raip'].href)
    logging.info(
        f'Отправлен документ пользователю: {update.message.chat.first_name}')


def wake_up(update, context):
    chat = update.effective_chat
    cache['users_id'].add(chat.id)
    file_output([tuple(cache['users_id'])], 'users')
    name = update.message.chat.first_name
    button = BotConstants.BUTTON

    context.bot.send_message(
        chat_id=chat.id,
        text=(GREETING.format(name) + cache['last_raip'].href),
        reply_markup=button
    )


if __name__ == '__main__':
    configure_logging()
    updater = Updater(token=TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('get_raip', get_raip))
    updater.start_polling()
    cache['last_raip'] = get_last_raip()
    cache['users_id'] = get_users()
    logging.info(f'Данные в кеше: {cache}')
    while True:
        last_raip = parse_last_raip(delay=DELAY)
        if last_raip is None:
            logging.error(f'Неудачный запрос, попробую секунд через {DELAY}')
        elif last_raip != cache.get('last_raip'):
            logging.info(f'Изменения: {last_raip}')
            cache['last_raip'] = last_raip
            save_raip(last_raip)
            for user_id in cache['users_id']:
                bot.send_message(
                    user_id, f'Что-то изменилось {last_raip.href}')
        sleep(SLEEP)
