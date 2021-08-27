from bs4 import BeautifulSoup
import requests
import re
import Parser.utils as utils
import copy
from Models.Products import ProductStatus, BasketshopProduct, LamodaProduct


class BaseParser:
    @staticmethod
    def smart_search(pattern, pages=1):
        raise NotImplementedError("Base parser has no realisation for this method!")

    @staticmethod
    def parse_product(url, short_url=False):
        raise NotImplementedError("Base parser has no realisation for this method!")

    @staticmethod
    def product_by_sku(sku):
        raise NotImplementedError("Base parser has no realisation for this method!")


class LamodaParser(BaseParser):
    SEARCH_URL = 'https://www.lamoda.ru/catalogsearch/result/?q={0}&page={1}'.format
    HOME_URL = 'https://www.lamoda.ru{0}'.format
    PRODUCT_URL = 'https://www.lamoda.ru/p/{0}/'.format

    @staticmethod
    def search_skus(tag, pages=1):
        result = []
        for page_num in range(1, pages + 1):
            page = requests.get(LamodaParser.SEARCH_URL(tag, page_num))
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                if "Поиск не дал результатов" in soup.text:
                    return list()
                product_card_list = soup.findAll("div", class_="products-list-item")
                return [utils.get_sku_from_url(card.find("a")["href"]) for card in product_card_list]
            else:
                return result
        return result

    @staticmethod
    def product_by_sku(sku):
        product = LamodaParser.parse_product(LamodaParser.PRODUCT_URL(sku))
        if product is None:
            return LamodaProduct(brand=None,
                                 name=None,
                                 sku=LamodaProduct.make_proper_sku(sku),
                                 image_link=None,
                                 status=ProductStatus.OUT_OF_STOCK,
                                 sizes=list(),
                                 link=LamodaParser.PRODUCT_URL(sku),
                                 price=None)
        else:
            product.set_sku(sku)
        return product

    @staticmethod
    def smart_search(pattern, pages=1):
        result = []
        for page_num in range(1, pages + 1):
            tag = utils.generate_name_from_pattern(pattern)
            page = requests.get(LamodaParser.SEARCH_URL(tag, page_num))
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, "html.parser")
                if "Поиск не дал результатов" in soup.text:
                    return list()
                product_card_list = soup.findAll("div", class_="products-list-item")
                for card in product_card_list:
                    name = card.find("span", class_="products-list-item__type").text.strip()
                    if utils.check_name(name, pattern):
                        parsed = LamodaParser.parse_product(card.find("a")["href"], True)
                        if parsed is not None:
                            result.append(parsed)
            else:
                return result
            return result

    @staticmethod
    def parse_product(url, short_url=False):
        if short_url:
            url = LamodaParser.HOME_URL(url)
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
                pack = re.findall('"sizes":\[[^\]]*\]', page.text)  # replace('"sizes":[', '')
                real_pack = max(pack, key=lambda x: len(x)).replace('"sizes":[', '').replace(']', '')
                p_sizes = utils.parse_sizes(real_pack)
            except:
                p_sizes = list()
            buy_btn = p_grid.find("button")
            is_available = True if buy_btn.text.strip() == "Добавить в корзину" else False
            if is_available:
                p_price_text = p_grid.find_all("span", class_="product-prices__price")[-1].text
                p_price = float(''.join(filter(str.isalnum, p_price_text)))
                p_status = ProductStatus.IN_STOCK
            else:
                p_price = 0
                p_status = ProductStatus.OUT_OF_STOCK
            product = LamodaProduct(brand=p_brand,
                                    name=p_name,
                                    sku=LamodaProduct.make_proper_sku(p_sku),
                                    image_link=p_image,
                                    status=p_status,
                                    sizes=p_sizes,
                                    link=p_link,
                                    price=p_price)
            return product
        except Exception as ex:
            print(ex.__repr__())
            return None


class BasketshopParser(BaseParser):
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
                                     sku=BasketshopProduct.make_proper_sku(sku),
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
        soup = BeautifulSoup(page.text, "html.parser")
        p_name = soup.find("h1", class_="product__title").text
        p_sku = BasketshopProduct.make_proper_sku(BasketshopParser._get_sku_from_name(p_name))
        sizes = dict()
        for p_size_list in soup.find_all("ul", class_="product__sizes-list"):
            sizes[p_size_list["data-size-chart"]] = [x.text for x in
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
                                    sku=BasketshopProduct.make_proper_sku(p_sku),
                                    image_link=p_image,
                                    status=p_status,
                                    sizes=p_sizes,
                                    link=p_link,
                                    price=p_price)
        return product
