from typing import Optional

from Master.ProductChangeEvent import ProductChangeEvent, OnProductChange, ProductChangeArgs
from Modules.Product import Product

from Master.Event import MasterResponse
from Master.Event import AbstractResponse

import Parser.parser as parser


class Master:
    product_db: list[Product]
    product_change_event: ProductChangeEvent

    def __init__(self):
        self.product_db = []
        self.product_change_event = ProductChangeEvent()
        self.product_change_event.subscribe(OnProductChange())

    def parse_product_by_tag(self, tag: str) -> Optional[Product]:

        data = parser.search(tag)
        # TODO: add async

        return data

    def is_product_changed(self, product: Product) -> AbstractResponse:
        """
        Check if product has been changed

        :param product: product to check
        :return:
        """
        cached_product = self.get_product_by_sku(product.article)

        if not cached_product:
            return None

        return_event = AbstractResponse()

        if cached_product.status == product.status:
            self.product_change_event.invoke(self, ProductChangeArgs("old_price", "new_price"))
            return_event.append_event(
                MasterResponse("Status of product {} has changed from {} to {}"
                               .format(product.name, cached_product.status, product.status)))

        if cached_product.price != product.price:
            return_event.append_event(
                MasterResponse("Price of product {} has changed from {} to {}"
                               .format(product.name, cached_product.price, product.price)))

        if cached_product.sizes != product.sizes:
            return_event.append_event(
                MasterResponse("Sizes of product {} have changed from {} to {}"
                               .format(product.name, cached_product.sizes, product.sizes)))

        if not return_event.raised:
            return_event.append_event(MasterResponse("Product was not changed"))

        return return_event

    # TODO: change to SQL request
    def get_product_by_tag(self, title: str) -> Optional[list[Product]]:
        products = []
        for product in self.product_db:
            if product.name == title:
                products.append(product)

        if not products:
            return None
        return products

    # TODO: change to SQL request
    def get_product_by_sku(self, sku: str) -> Optional[Product]:
        for product in self.product_db:
            if product.article == sku:
                return product
        return None
