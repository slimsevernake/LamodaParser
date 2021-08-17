from discord import Embed

import app_logger
import Parser.parser as parser
from logging import Logger
from typing import Dict, List
from Modules import Product
from .ProductChangeEvent import ProductChangeHandler
from .WebhookHandle import async_send_embed


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
        self.embed_queue = []

    async def run(self):
        for product_tag in self.manifest:
            self.logger.debug(product_tag)
            products_found = Monitor.search(product_tag)
            for product in products_found:
                cached_product = self.product_db.get(product.sku, None)
                if cached_product:
                    if self.check_differences(cached_product, product):
                        self.product_db[product.sku] = product
                else:
                    self.product_db[product.sku] = product
                    await async_send_embed(product.to_embed())
        for embed in self.embed_queue:
            self.logger.info('sending embeds')
            await async_send_embed(embed)
        self.embed_queue.clear()

    def check_differences(self, old_product: 'Product', new_product: 'Product') -> 'bool':
        check = False
        if old_product.status != new_product.status:
            self.embed_queue.append(ProductChangeHandler.on_status_changed(new_product))
            return True
        if old_product.price != new_product.price:
            check = True
            self.embed_queue.append(ProductChangeHandler.on_price_changed(new_product, old_product.price))
        if old_product.sizes != new_product.sizes:
            check = True
            self.embed_queue.append(ProductChangeHandler.on_size_changed(new_product))
        return check

    @staticmethod
    def search(tag: str) -> List:
        stype, stag = Monitor.get_context(tag)

        if stype:
            if stype == "SKU":
                return [parser.product_by_sku(stag)]
            elif stype == "EXTENDED":
                return parser.smart_search(stag)
            else:
                return parser.search(tag)
        else:
            return []

    @staticmethod
    def get_context(tag):
        splitted = tag.split(": ")
        if len(splitted) > 1:
            return splitted[0], splitted[1]
        else:
            return None, None
