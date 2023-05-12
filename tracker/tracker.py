import logging
import re
from requests import Response
from typing import List, Optional

from bs4 import Tag

from classes import Raip
from configs import configure_logging
from exceptions import ParserFindTagException
from settings import DOMAIN, RE_DATE, RE_NUMBER, SEARCH_URL, HTMLTag
from utils import find_tag, get_response, make_soup


def get_search_result(response: Response) -> List[Tag]:
    soup = make_soup(response)
    search_results = find_tag(soup, HTMLTag.UL, class_='search-results')
    return search_results.find_all(HTMLTag.A, class_='search-link')


def get_raip(response: Response) -> Raip:
    soup = make_soup(response)
    info = find_tag(soup, HTMLTag.DIV, class_='info')
    number = find_tag(info, HTMLTag.P)
    accept_date = number.find_next_sibling()
    pub_date = accept_date.find_next_sibling()
    href = find_tag(info, HTMLTag.A, class_='doc-name__link')
    return Raip(
        title=find_tag(info, HTMLTag.DIV, class_='info__title').text,
        number=re.search(RE_NUMBER, number.text).group(),
        accept_date=re.search(RE_DATE, accept_date.text).group(),
        pub_date=re.search(RE_DATE, pub_date.text).group(),
        href=DOMAIN + href.get('href')
    )


def parse_last_raip(delay: int) -> Optional[Raip]:
    configure_logging()
    logging.info('Парсер запущен!')
    response = get_response(SEARCH_URL, delay)
    if response is None:
        return None
    try:
        raips = get_search_result(response)
    except ParserFindTagException:
        return None
    logging.info(f'Получено объектов: {len(raips)}')
    raip_link = raips[0].get('href')
    logging.info(f'Собираю информацию из {raip_link}')
    response = get_response(raips[0].get('href'), delay)
    if response is None:
        return None
    try:
        raip = get_raip(response)
    except ParserFindTagException:
        return None
    logging.info(f'Последний {raip}')
    return raip
