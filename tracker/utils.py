import datetime
import logging
from pathlib import Path
from typing import Optional, Union

from bs4 import BeautifulSoup, Tag
from requests import RequestException, Response
from requests_html import HTMLSession

from tracker.settings import BASE_DIR, DT_FORMAT, ENCODING
from tracker.exceptions import ParserFindTagException


def get_response(url: str, sleep: Optional[int]) -> Union[Response, None]:
    session = HTMLSession()
    try:
        response = session.get(url)
        if sleep:
            response.html.render(sleep=10)
        return response
    except RequestException:
        logging.error(f'Возникла ошибка при загрузке {url}',
                      exc_info=True, stack_info=True)
        return None


def find_tag(soup: BeautifulSoup, tag: str, **attrs: str) -> Tag:
    searched_tag = soup.find(tag, **attrs)
    if searched_tag is None:
        error_message = f'Не найден тег {tag} {None}'
        logging.error(error_message, stack_info=True)
        raise ParserFindTagException(error_message)
    return searched_tag


def make_soup(
    url: str, sleep: Optional[int] = None
) -> Union[BeautifulSoup, None]:
    response = get_response(url, sleep)
    if response is None:
        return None
    response.encoding = ENCODING
    return BeautifulSoup(response.html.html, 'lxml')


def get_filepath() -> Union[str, Path]:
    filename = f'''raip_{
        datetime.datetime.now().strftime(DT_FORMAT)
        }.sqlite'''
    downloads_dir = Path(BASE_DIR, 'downloads')
    downloads_dir.mkdir(exist_ok=True)
    logging.info(f'Информация сохраняется в {filename}')
    return Path(downloads_dir, filename)
