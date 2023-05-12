import logging
import re
from typing import List

from bs4 import Tag

from classes import Raip
from configs import configure_logging
from settings import DOMAIN, RE_DATE, RE_NUMBER, SEARCH_URL, HTMLTag
from utils import find_tag, make_soup


def get_search_result(delay: int) -> List[Tag]:
    soup = make_soup(SEARCH_URL, delay)
    search_results = find_tag(soup, HTMLTag.UL, class_='search-results')
    return search_results.find_all(HTMLTag.A, class_='search-link')


def get_raip(link: str, delay: int) -> Raip:
    soup = make_soup(link, delay)
    print(soup.prettify())
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


def parse_last_raip(delay: int):
    configure_logging()
    logging.info('Парсер запущен!')
    raips = get_search_result(delay)
    logging.info(f'Получено объектов: {len(raips)}')
    raip_link = raips[0].get('href')
    logging.info(f'Собираю информацию из {raip_link}')
    raip = get_raip(raips[0].get('href'), delay)
    logging.info(f'Найден последний {raip}')
    return raip


if __name__ == '__main__':
    parse_last_raip(0)
