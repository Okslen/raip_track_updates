import logging
from time import sleep

from tracker.tracker import parse_last_raip


def process_parsing():
    raips = []
    while True:
        last_raip = parse_last_raip()
        if last_raip not in raips:
            logging.info(f'Изменения: {last_raip}')
            raips.append(last_raip)
        sleep(3600)


if __name__ == '__main__':
    process_parsing()
