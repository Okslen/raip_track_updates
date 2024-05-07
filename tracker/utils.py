import logging
from time import sleep
from typing import Optional, Union

from bs4 import BeautifulSoup, Tag
from requests import RequestException, Response
from requests_html import HTMLSession

from settings import DELAY, ENCODING
from exceptions import ParserFindTagException


def get_response(url: str, sleep_time: Optional[int]) -> Union[Response, None]:
    session = HTMLSession()
    try:
        response: Response = session.get(url)
    except RequestException:
        # logging.error(f'Возникла ошибка при загрузке {url}',
        #              exc_info=True, stack_info=True)
        logging.error(f'Неудачный запрос, попробую секунд через {DELAY}')
        sleep(DELAY)
        get_response(url, sleep_time)
        return None
    if sleep_time:
        response.html.render(sleep=sleep_time)
    return response


def find_tag(soup: BeautifulSoup, tag: str, **attrs: str) -> Tag:
    searched_tag = soup.find(tag, **attrs)
    if searched_tag is None:
        error_message = f'Не найден тег {tag} {None}'
        # logging.error(error_message, stack_info=True)
        raise ParserFindTagException(error_message)
    return searched_tag


def make_soup(response: Response) -> BeautifulSoup:
    response.encoding = ENCODING
    return BeautifulSoup(response.html.html, 'lxml')
