import logging
from typing import Optional, Union

from bs4 import BeautifulSoup, Tag
from requests import RequestException, Response
from requests_html import HTMLSession

from settings import ENCODING
from exceptions import ParserFindTagException


def get_response(url: str, sleep: Optional[int]) -> Union[Response, None]:
    session = HTMLSession()
    try:
        response = session.get(url)
    except RequestException:
        # logging.error(f'Возникла ошибка при загрузке {url}',
        #              exc_info=True, stack_info=True)
        return None
    if sleep:
        response.html.render(sleep=sleep)
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
