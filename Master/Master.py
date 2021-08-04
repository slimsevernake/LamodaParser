import asyncio
from logging import Logger
from typing import Optional

import app_logger
from Master.WebhookHandle import *
from Master.ProductChangeEvent import ProductChangeHandler
from Modules.Product import Product

import Parser.parser as parser


class Master:
    product_db: 'list[Product]'
    tags: 'list[str]'

    def __init__(self, logger: 'Logger' = None):
        self.product_db = []
        self.tags = []

        if logger:
            self.logger = logger
        else:
            self.logger = app_logger.get_logger("master")

        self.logger.info("master initiated")

    async def async_process_product_by_sku(self, sku: 'str') -> 'Optional[Product]':
        self.logger.debug(f"SKU to parse: {sku}")

        data = parser.product_by_sku(sku, self.logger)
        # Here code prays to Allah. مجد الله!
        if data:
            await self.handle_product(data)
        # End.
        return data

    async def async_parse_product_by_tag(self, tag: 'str') -> 'Optional[list[Product]]':

        self.logger.debug(f"Tag to parse: {tag}")

        data = parser.search(tag, self.logger)
        if len(data) == 0:
            return None
        loop = asyncio.get_event_loop()
        tasks = []
        for el in data:
            tasks.append(loop.create_task(self.handle_product(el)))
        await asyncio.wait(tasks)
        return data

    async def handle_product(self, product: 'Product') -> None:
        if not self.get_product_by_sku(product.article):
            self.product_db.append(product)

    async def monitor_products(self):
        for cached_product in self.product_db:
            product = parser.product_by_sku(cached_product.article, self.logger)
            await self.check_product_changed(product, cached_product)

    async def check_product_changed(self, product: 'Product', cached_product: 'Product') -> None:
        if product is None:
            if cached_product is not None:
                cached_product.status = cached_product.status
        else:
            if cached_product.get_available_sizes() != product.get_available_sizes():
                ProductChangeHandler.on_size_changed(product)
                cached_product.sizes = product.sizes
            if cached_product.price != product.price:
                ProductChangeHandler.on_price_changed(product, cached_product.price)
                cached_product.price = product.price
            if cached_product.status != product.status:
                ProductChangeHandler.on_status_changed(product)
                cached_product.status = product.status

    # TODO: change to SQL request
    def get_product_by_tag(self, title: 'str') -> 'Optional[list[Product]]':
        products = []
        for product in self.product_db:
            if product.name == title:
                products.append(product)

        if not products:
            return None
        return products

    # TODO: change to SQL request
    def get_product_by_sku(self, sku: 'str') -> 'Optional[Product]':
        for product in self.product_db:
            if product.article == sku:
                return product
        return None
