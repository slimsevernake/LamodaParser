from discord import Embed
import app_logger
from Parser.Parsers import BasketshopParser as Parser
from logging import Logger
from typing import Dict, List
from Models.Products import BasketshopProduct as Product
from Monitor.ProductChangeEvent import ProductChangeHandler
from Monitor.WebhookHandle import async_send_embed


class Monitor:
    product_db: 'Dict[str, Product]'  # SKU:str -> Product object with same SKU.
    tags: 'List[str]'
    logger: 'Logger'
    embed_queue: 'List[Embed]'

    def __init__(self, manifest, logger: 'Logger' = None):
        self.product_db = {}
        self.tags = []
        self.manifest = manifest
        self.logger = logger if logger else app_logger.get_logger("monitor")

    async def run(self):
        for product_tag in self.manifest:
            self.logger.debug(product_tag)
            products_found = Monitor.search(product_tag)
            for product in products_found:
                cached_product = self.product_db.get(product.sku, None)
                if cached_product:
                    await Monitor.process_differences(cached_product, product)
                    self.product_db[product.sku] = product
                else:
                    self.product_db[product.sku] = product
                    await async_send_embed(product.to_embed())

    @staticmethod
    async def process_differences(old_product: 'Product', new_product: 'Product') -> 'bool':
        check = False
        if old_product.status != new_product.status:
            await async_send_embed(ProductChangeHandler.on_status_changed(new_product))
            return True
        if old_product.price != new_product.price:
            check = True
            await async_send_embed(ProductChangeHandler.on_price_changed(new_product, old_product.price))
        if old_product.sizes != new_product.sizes:
            check = True
            await async_send_embed(ProductChangeHandler.on_size_changed(new_product))
        return check

    @staticmethod
    def search(tag: str) -> List:
        stype, stag = Monitor.get_context(tag)

        if stype:
            if stype == "SKU":
                return [Parser.product_by_sku(stag)]
            elif stype == "EXTENDED":
                return Parser.smart_search(stag)
        else:
            return []

    @staticmethod
    def get_context(tag):
        splitted = tag.split(": ")
        if len(splitted) > 1:
            return splitted[0], splitted[1]
        else:
            return None, None
