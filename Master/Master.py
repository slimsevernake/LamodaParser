import asyncio
from typing import Optional

from Bot import WebhookHandle
from Master.ProductChangeEvent import ProductChangeEvent, OnProductChange, ProductChangeArgs
from Modules.Product import Product

import Parser.parser as parser


class Master:
    product_db: list[Product]
    product_change_event: ProductChangeEvent
    tags: list[str]

    def __init__(self):
        self.product_db = []
        self.tags = []
        self.product_change_event = ProductChangeEvent()
        self.product_change_event.subscribe(OnProductChange())

    def parse_product_by_tag(self, tag: str) -> Optional[list[Product]]:
        return asyncio.run(self.async_parse_product_by_tag(tag))

    async def async_parse_product_by_tag(self, tag: str) -> Optional[list[Product]]:
        data = parser.search(tag)
        loop = asyncio.get_event_loop()
        tasks = []
        for el in data:
            tasks.append(loop.create_task(self.handle_product(el)))
        await asyncio.wait(tasks)
        return data

    async def handle_product(self, product: Product) -> None:
        if not self.get_product_by_sku(product.article):
            self.product_db.append(product)

    def monitor_products(self):
        for cached_product in self.product_db:
            product = self.parse_product_by_sku(cached_product.article)
            if not product:
                # product has disappeared
                self.product_change_event.invoke(ProductChangeArgs(cached_product, "product exists", "product was removed"))
            self.check_product_changed(product, cached_product)
        # for tag in self.tags:
        #     data = self.parse_product_by_tag(tag)
        #     for product in data:
        #         cached_product = self.get_product_by_sku(product.article)
        #         if not cached_product:

        # for cached_product in self.product_db:
        #    product = self.parse_product_by_sku(cached_product.article)

    def check_product_changed(self, product: Product, cached_product: Product) -> None:
        if cached_product.price != product.price:
            WebhookHandle.send_embed(product.to_embed())
            # self.product_change_event.invoke(ProductChangeArgs(product, "old_price", "new_price"))

        if cached_product.sizes != product.sizes:
            pass
            #self.product_change_event.invoke(ProductChangeArgs(product, "old_sizes", "new_sizes"))

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

