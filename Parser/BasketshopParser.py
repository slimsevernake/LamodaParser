from bs4 import BeautifulSoup
import requests
from Modules.Product import Product, ProductStatus
from Modules.BasketshopProduct import BasketshopProduct
import Parser.utils as utils
from .Parser import Parser

class BasketshopParser(Parser):
    SEARCH_URL = 'https://www.basketshop.ru/catalog/search/?&s[q]={0}&p={1}'.format
    HOME_URL = "https://www.basketshop.ru{0}".format

    @staticmethod
    def product_by_sku(sku):
        try:
            page = requests.get(BasketshopParser.SEARCH_URL(sku, 1))
            soup = BeautifulSoup(page.text, "html.parser")
            link = BasketshopParser.HOME_URL(soup.find("a", class_="product-card__name")["href"])
            return BasketshopParser.parse_product(link)
        except:
            return BasketshopProduct(brand=None,
                                     name=None,
                                     sku=Product.make_proper_sku(sku),
                                     image_link=None,
                                     status=ProductStatus.OUT_OF_STOCK,
                                     sizes=list(),
                                     link="",
                                     price=None)

    @staticmethod
    def smart_search(pattern, pages=2):
        result = []
        for page_num in range(1, pages + 1):
            tag = utils.generate_name_from_pattern(pattern)
            page = requests.get(BasketshopParser.SEARCH_URL(tag, page_num))
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                products_in_page = soup.find_all("a", class_="product-card__name")
                for card in products_in_page:
                    name = card.find("span").text.strip()
                    link = BasketshopParser.HOME_URL(card["href"])
                    if utils.check_name(name, pattern):
                        parsed = BasketshopParser.parse_product(link)
                        if parsed:
                            result.append(parsed)
            else:
                return result
            return result

    @staticmethod
    def _get_sku_from_name(name):
        return name[name.rfind("(") + 1:name.rfind(")")]

    @staticmethod
    def parse_product(url):
        page = requests.get(url)
        try:
            soup = BeautifulSoup(page.text, "html.parser")
            p_name = soup.find("h1", class_="product__title").text
            p_sku = BasketshopProduct.make_proper_sku(BasketshopParser._get_sku_from_name(p_name))
            sizes = dict()
            for p_size_list in soup.find_all("ul", class_="product__sizes-list"):
                sizes[p_size_list["data-size-chart"]] = [x["data-size"] for x in
                                                         p_size_list.find_all("button", class_="product__sizes-button")]
            p_sizes = list(map('/'.join, zip(sizes['UK'], sizes['RUS'])))
            p_status = ProductStatus.IN_STOCK if len(p_sizes) != 0 else ProductStatus.OUT_OF_STOCK
            p_image = soup.find("div", class_="product__gallery-slider-slide-cell js-zoom").find("img")["src"]
            p_link = url
            if p_status == ProductStatus.IN_STOCK:
                price = soup.find("div", class_="product__price-value").text
                p_price = float(''.join(filter(str.isdigit, price)))
            else:
                p_price = 0.0
            product = BasketshopProduct(brand="",
                                        name=p_name,
                                        sku=Product.make_proper_sku(p_sku),
                                        image_link=p_image,
                                        status=p_status,
                                        sizes=p_sizes,
                                        link=p_link,
                                        price=p_price)
            return product
        except Exception as ex:
            print(ex.__repr__())
            return None

