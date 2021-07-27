from typing import Optional

from WebhookHandle import *
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

    def parse_product_by_sku(self, sku: str) -> Optional[Product]:
        return parser.product_by_sku(sku)

    async def async_parse_product_by_tag(self, tag: str) -> Optional[list[Product]]:
        # DEBUG
        print(f"tag to parse: {tag}")

        data = parser.search(tag)
        if len(data) == 0:
            return None
        loop = asyncio.get_event_loop()
        tasks = []
        for el in data:
            tasks.append(loop.create_task(self.handle_product(el)))
        await asyncio.wait(tasks)
        return data

    async def handle_product(self, product: Product) -> None:
        if not self.get_product_by_sku(product.article):
            self.product_db.append(product)

    async def monitor_products(self):
        for cached_product in self.product_db:
            product = self.parse_product_by_sku(cached_product.article)
            await self.check_product_changed(product, cached_product)

    async def check_product_changed(self, product: Product, cached_product: Product) -> None:
        if not product:
            # product has disappeared
            await self.product_change_event.invoke(
                ProductChangeArgs(cached_product, "status", "product exists", "product was removed"))
            return

        if cached_product.price != product.price:
            await self.product_change_event.invoke(ProductChangeArgs(product, "price", cached_product.price, product.price))

        if cached_product.sizes != product.sizes:
            pass
            # self.product_change_event.invoke(ProductChangeArgs(product, "sizes", cached_product.sizes, product.sizes))

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
