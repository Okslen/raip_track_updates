from pathlib import Path

from telegram import ReplyKeyboardMarkup

BASE_DIR = Path(__file__).parent

DT_FORMAT = '%Y-%m-%d_%H-%M-%S'
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
ENCODING = 'utf-8'

DOMAIN = 'https://rk.gov.ru/search'
ORDER_TO_FOUND = '27 ноября 2024 года №2197-р'
DELAY = 5
SLEEP = 740

GREETING = (
    'Привет, {}. Если выйдет новая редакция, я сообщу, актуальная версия:')


# регулярное выражение для поиска даты
RE_DATE = r'\d{2}\.\d{2}\.\d{4}'
# регулярное выражение для поиска номера
RE_NUMBER = r'\d+\-р'


class HTMLTag:
    A = 'a'
    DIV = 'div'
    DL = 'dl'
    H1 = 'h1'
    LI = 'li'
    P = 'p'
    SECTION = 'section'
    SPAN = 'span'
    TABLE = 'table'
    TBODY = 'tbody'
    TD = 'td'
    TR = 'tr'
    UL = 'ul'


class BotConstants:
    BUTTONS = ['/get_raip', '/newcat']
    BUTTON = ReplyKeyboardMarkup([BUTTONS], resize_keyboard=True)
    RESERVE_URL = 'https://api.thedogapi.com/v1/images/search'
    URL = 'https://api.thecatapi.com/v1/images/search'
