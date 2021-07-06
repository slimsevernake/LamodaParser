from bs4 import BeautifulSoup
import requests
import re
import json

SEARCH_URL = 'https://www.lamoda.ru/catalogsearch/result/?q={0}&page={1}'.format
HOME_URL = 'https://www.lamoda.ru{0}'.format


def search(tag, pages=10):
    result = []
    for page_num in range(1, pages+1):
        page = requests.get(SEARCH_URL(tag, page_num))
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            if "Поиск не дал результатов" in soup.text:
                return list()
            product_card_list = soup.findAll("div", class_="products-list-item")
            for card in product_card_list:
                parsed = parse_product(card.find("a")["href"])
                if parsed is not None:
                    result.append(parsed)
        else:
            raise ConnectionError("Нет подключения к сайту!")
            pass
        return result


def parse_product(short_url):
    page = requests.get(HOME_URL(short_url))
    if page.status_code == 200:
        soup = BeautifulSoup(page.text, "html.parser")
        p_grid = soup.find("div", class_="grid__product")

        p_brand = p_grid.find("h1", class_="product-title__brand-name")["title"]
        p_name = p_grid.find("h1", class_="product-title__brand-name").find("span").text

        p_price_text = p_grid.find_all("span", class_="product-prices__price")[-1].text
        p_price = float(''.join(filter(str.isalnum, p_price_text)))

        try:
            p_image = p_grid.find("img", class_="x-product-gallery__image x-product-gallery__image_first")['src']
        except TypeError:
            p_image = p_grid.find("img", class_="x-product-gallery__image x-product-gallery__image_single")['src']

        p_article = short_url.replace("https://", "").split("/")[2]

        p_type = p_grid.find("x-product-title")["product-name"]
        p_sizes = []
        sizes = p_grid.find("script", attrs={"data-module": "statistics"}).decode().replace("\n", "").replace(" ", "")
        expressed = re.search('"sizes":\[[^]]*', sizes)[0].replace('"sizes":[', '')
        ''' Доделать парс размеров'''
        ''' Доделать парс статуса'''

        p_link = HOME_URL(short_url)

    else:
        return None


search("zig dynamica")