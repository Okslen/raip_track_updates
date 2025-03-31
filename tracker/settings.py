from pathlib import Path

from telegram import ReplyKeyboardMarkup

BASE_DIR = Path(__file__).parent

DT_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
ENCODING = 'utf-8'

DOMAIN = 'https://rk.gov.ru/search'
ORDER_TO_FOUND = '27 ноября 2024 года №2197-р'
DELAY = 10
SLEEP = 740

GREETING = (
    'Привет, {}. Если выйдет новая редакция, я сообщу, актуальная версия:')

IMAGE_ERROR = 'Не удалось скачать картинку'


class BotConstants:
    BUTTONS = ['/get_raip', '/newcat']
    BUTTON = ReplyKeyboardMarkup([BUTTONS], resize_keyboard=True)
    RESERVE_URL = 'https://api.thedogapi.com/v1/images/search'
    URL = 'https://api.thecatapi.com/v1/images/search'
