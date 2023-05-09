from bs4 import BeautifulSoup
from requests_html import HTMLSession

from settings import REQUEST_URL


if __name__ == '__main__':
    session = HTMLSession()
    response = session.get(REQUEST_URL)
    response.html.render(sleep=10)
    soup = BeautifulSoup(response.html.html, 'lxml')
    print(soup.prettify())
