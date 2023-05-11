import logging
import re
from typing import List

from bs4 import Tag

from tracker.classes import Raip
from tracker.configs import configure_logging
from tracker.settings import DELAY, RE_DATE, RE_NUMBER, SEARCH_URL, HTMLTag
from tracker.utils import find_tag, make_soup


def get_search_result() -> List[Tag]:
    soup = make_soup(SEARCH_URL, DELAY)
    if soup is None:
        return None
    search_results = find_tag(soup, HTMLTag.UL, class_='search-results')
    return search_results.find_all(HTMLTag.A, class_='search-link')


def get_raip(link: str) -> Raip:
    soup = make_soup(link, DELAY)
    if soup is None:
        return None
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
        href=href.get('href')
    )


def parse_last_raip():
    configure_logging()
    logging.info('Парсер запущен!')
    raips = get_search_result()
    if raips is None:
        return None
    logging.info(f'Получено объектов: {len(raips)}')
    raip_link = raips[0].get('href')
    logging.info(f'Собираю информацию из {raip_link}')
    if raips is None:
        return None
    raip = get_raip(raips[0].get('href'))
    logging.info(f'Найден последний {raip}')
    return raip
