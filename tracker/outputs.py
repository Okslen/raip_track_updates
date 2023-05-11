import csv
import logging
from typing import List, Tuple

from classes import Raip
from settings import BASE_DIR, ENCODING


def get_file_path(filename: str):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    file_name = f'{filename}.csv'
    return results_dir / file_name


def file_output(results: List[Tuple[str, ...]], filename: str) -> None:
    file_path = get_file_path(filename)
    with open(file_path, 'w', encoding=ENCODING) as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами сохранен: {file_path}')


def save_raip(raip: Raip) -> List[Tuple[str, ...]]:
    attrs = ('title', 'number', 'accept_date', 'pub_date', 'href')
    return file_output([tuple(getattr(raip, attr) for attr in attrs)], 'last')


def read_file(filename: str):
    file_path = get_file_path(filename)
    with open(file_path, 'r', encoding=ENCODING) as f:
        reader = csv.reader(f, dialect='unix')
        results = [tuple(row) for row in reader]
        logging.info(f'Загружены данные из файла {filename}: {results}')
        return results


def get_last_raip():
    attrs = ('title', 'number', 'accept_date', 'pub_date', 'href')
    raip = Raip(*['']*5)
    for row in read_file('last'):
        for attr, value in zip(attrs, row):
            setattr(raip, attr, value)
    return raip


def get_users():
    result = read_file('users')
    return set(result[0])
