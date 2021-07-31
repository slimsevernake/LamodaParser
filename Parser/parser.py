from bs4 import BeautifulSoup
import requests
import re
import Parser.utils as utils
from Modules.Product import Product, ProductStatus
import datetime

SEARCH_URL = 'https://www.lamoda.ru/catalogsearch/result/?q={0}&page={1}'.format
HOME_URL = 'https://www.lamoda.ru{0}'.format
PRODUCT_URL = 'https://www.lamoda.ru/p/{0}/'.format


def search(tag, pages=3):
    result = []
    for page_num in range(1, pages + 1):
        page = requests.get(SEARCH_URL(tag, page_num))
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "lxml")
            if "Поиск не дал результатов" in soup.text:
                return list()
            product_card_list = soup.findAll("div", class_="products-list-item")
            for card in product_card_list:
                parsed = parse_product(card.find("a")["href"], short_url=True)
                if parsed is not None:
                    result.append(parsed)
        else:
            raise ConnectionError("Нет подключения к сайту!")
        return result


def parse_product(url, short_url=False):
    if short_url:
        url = HOME_URL(url)
    page = requests.get(url)
    if page.status_code == 200:
        try:
            soup = BeautifulSoup(page.text, "lxml")
            p_grid = soup.find("div", class_="grid__product")
            p_brand = p_grid.find("h1", class_="product-title__brand-name")["title"]
            p_name = p_grid.find("h1", class_="product-title__brand-name").find("span").text
            try:
                p_image = p_grid.find("img", class_="x-product-gallery__image x-product-gallery__image_first")['src']
            except TypeError:
                p_image = p_grid.find("img", class_="x-product-gallery__image x-product-gallery__image_single")['src']

            p_link = url

            p_article = url.replace("https://", "").split("/")[2]

            p_type = p_grid.find("x-product-title")["product-name"]

            sizes = p_grid.find("script", attrs={"data-module": "statistics"}).decode().replace("\n", "").replace(" ",
                                                                                                                  "")
            pack = re.search('"sizes":\[[^]]*', sizes)[0].replace('"sizes":[', '')
            p_sizes = utils.parse_sizes(pack)

            is_available = p_grid.find("button", text="Добавить в корзину")
            if is_available is not None:
                p_price_text = p_grid.find_all("span", class_="product-prices__price")[-1].text
                p_price = float(''.join(filter(str.isalnum, p_price_text)))
                p_status = ProductStatus.IN_STOCK
            else:
                p_price = 0
                p_status = ProductStatus.OUT_OF_STOCK

            product = Product(brand=p_brand,
                              name=p_name,
                              article=p_article,
                              type=p_type,
                              image_link=p_image,
                              status=p_status,
                              sizes=p_sizes,
                              link=p_link,
                              price=p_price)
            print(f"{datetime.datetime.now()} | {product}".replace("\n", "    "))
            return product
        except Exception as ex:
            print(ex)
            return None
    else:
        return None


def product_by_sku(sku):
    try:
        product = parse_product(PRODUCT_URL(sku))
        product.article = sku
        return product
    except Exception as ex:
        print(ex)
        return None
