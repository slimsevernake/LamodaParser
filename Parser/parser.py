from logging import Logger
from bs4 import BeautifulSoup
import requests
import re
import Parser.utils as utils
from Modules.Product import Product, ProductStatus

SEARCH_URL = 'https://www.lamoda.ru/catalogsearch/result/?q={0}&page={1}'.format
HOME_URL = 'https://www.lamoda.ru{0}'.format
PRODUCT_URL = 'https://www.lamoda.ru/p/{0}/'.format


def smart_search(pattern, pages=1):
    result = []
    for page_num in range(1, pages + 1):
        tag = utils.generate_name_from_pattern(pattern)
        page = requests.get(SEARCH_URL(tag, page_num))
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            if "Поиск не дал результатов" in soup.text:
                return list()
            product_card_list = soup.findAll("div", class_="products-list-item")
            for card in product_card_list:
                name = card.find("span", class_="products-list-item__type").text.strip()
                if utils.check_name(name, pattern):
                    parsed = parse_product(card.find("a")["href"], True)
                    # print(parsed)
                    if parsed is not None:
                        result.append(parsed)
        else:
            return result
        return result


def search_skus(tag, pages=1):
    result = []
    for page_num in range(1, pages + 1):
        page = requests.get(SEARCH_URL(tag, page_num))
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, "html.parser")
            if "Поиск не дал результатов" in soup.text:
                return list()
            product_card_list = soup.findAll("div", class_="products-list-item")
            return [utils.get_sku_from_url(card.find("a")["href"]) for card in product_card_list]
        else:
            return result
    return result


def search(tag, logger: 'Logger', pages=1):
    result = []
    skus = search_skus(tag, pages)
    for sku in skus:
        parsed = product_by_sku(sku)
        if parsed is not None:
            result.append(parsed)
    return result


def parse_product(url, short_url=False):
    if short_url:
        url = HOME_URL(url)
    page = requests.get(url)
    try:
        soup = BeautifulSoup(page.text, "html.parser")
        p_grid = soup.find("div", class_="grid__product")
        p_link = url
        p_sku = url.replace("https://", "").split("/")[2]
        brand_name = p_grid.find("h1", class_="product-title__brand-name")
        p_brand = brand_name["title"]
        p_name = brand_name.find("span").text
        try:
            p_image = p_grid.find("img", class_="x-product-gallery__image x-product-gallery__image_first")['src']
        except TypeError:
            p_image = p_grid.find("img", class_="x-product-gallery__image x-product-gallery__image_single")['src']
        p_image = "https:" + p_image
        try:
            sizes = p_grid.find("script", attrs={"data-module": "statistics"}).decode().replace("\n", "").replace(" ", "")
            pack = re.search('"sizes":\[[^]]*', sizes)[0].replace('"sizes":[', '')
            p_sizes = utils.parse_sizes(pack)
        except AttributeError:
            p_sizes = list()
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
                          sku=Product.make_proper_sku(p_sku),
                          image_link=p_image,
                          status=p_status,
                          sizes=p_sizes,
                          link=p_link,
                          price=p_price)
        # logger.debug(f"{product}")
        return product
    except Exception as ex:
        print(ex.__repr__())
        return None


# Return Product with certain sku instead of None.
def product_by_sku(sku):
    product = parse_product(PRODUCT_URL(sku))
    if product is None:
        return Product(brand=None,
                       name=None,
                       sku=Product.make_proper_sku(sku),
                       image_link=None,
                       status=ProductStatus.OUT_OF_STOCK,
                       sizes=list(),
                       link=PRODUCT_URL(sku),
                       price=None)
    else:
        product.set_sku(sku)
    return product
