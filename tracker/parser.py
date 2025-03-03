from requests import ConnectionError
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import logging
import time

from classes import Raip
from settings import DELAY, DOMAIN, ORDER_TO_FOUND


def get_driver(try_time: time):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())

    for attempt in range(try_time):  # Две попытки запуска
        try:
            driver = webdriver.Chrome(service=service, options=options)
            return driver
        except ConnectionError:
            print(f'Ошибка соединения при запуске WebDriver '
                  f'(попытка {attempt + 1}). Повторный запуск...')
            time.sleep(2)  # Подождать перед повторной попыткой

    raise Exception(f'Не удалось запустить WebDriver, '
                    f'количество попыток: {try_time}')


def search_rk_gov():
    logging.info('Парсер запущен!')
    driver = get_driver(5)
    query = ORDER_TO_FOUND

    try:
        driver.get(DOMAIN)
        time.sleep(DELAY)  # Ждем, пока система защиты загрузит страницу
        # Вводим запрос в поисковую строку
        search_box = driver.find_element(By.NAME, "text")
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)
        time.sleep(5)  # Ждем загрузки результатов
        # Парсим результаты поиска
        try:
            first_search_results = driver.find_element(
                By.CLASS_NAME, "SearchResultsItem")
            title = first_search_results.find_element(
                By.CLASS_NAME, 'SearchResultsItem-Title').text.strip()
            number = first_search_results.find_element(
                By.CLASS_NAME, 'SearchResultsItem-Content').text.strip()
            href = first_search_results.find_element(
                By.CLASS_NAME, 'SearchResultsItem-Title').get_attribute("href")
            pub_date = first_search_results.find_element(
                By.CLASS_NAME, 'SearchResultsItem-Date').text.strip()
        except Exception as e:
            print(f"Ошибка парсинга элемента: {e}")
        return Raip(title, number, pub_date, pub_date, href)
    finally:
        driver.quit()


if __name__ == "__main__":
    raip = search_rk_gov()

    logging.info(raip.title)
    logging.info(raip.number)
    logging.info(raip.pub_date)
    logging.info(raip.href)
