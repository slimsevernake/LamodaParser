from bs4 import BeautifulSoup
import requests

URL = 'https://www.lamoda.ru/catalogsearch/result/?q={0}'.format


def search(tag):
    result = []
    page = requests.get(URL(tag))
    if page.status_code != '200':
        soup = BeautifulSoup(page.text, "html.parser")
        if "Поиск не дал результатов" in soup.text:
            return list()
        product_card_list = soup.findAll("div", class_="products-list-item")
        for card in product_card_list:
            print(card.a[0].href)
        # soup.find_all("a", text="Elsie")
    else:
        raise ConnectionError("Нет подключения к сайту!")
    return result


def parse(div_block):
    pass


search("jordan")