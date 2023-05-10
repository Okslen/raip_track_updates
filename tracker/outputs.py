import csv
import datetime as dt
import logging
from argparse import Namespace
from typing import List, Tuple

from classes import Raip
from settings import BASE_DIR, DT_FORMAT, ENCODING


def file_output(
    results: List[Tuple[str, ...]], cli_args: Namespace
) -> None:
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DT_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding=ENCODING) as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами сохранен: {file_path}')
