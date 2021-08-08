import app_logger
import Parser.parser as parser

from utils import *
from logging import Logger
from typing import Dict, List
from Modules.Product import Product


class Monitor:
    product_db: 'Dict[str, Product]'
    tags: 'List[str]'
    logger: 'Logger'

    def __init__(self, manifest, logger: 'Logger' = None):
        self.product_db = {}
        self.tags = []
        self.manifest = manifest

        if logger:
            self.logger = logger
        else:
            self.logger = app_logger.get_logger("master")

    def monitor_cycle(self) -> 'None':
        for product_tag in self.manifest.products_to_monitor:
            # if product_tag is category:
            #       TODO
            # else product_tag is sku:

            # maybe create parser.async_product_by_sku ??
            parsed_product = parser.product_by_sku(SKU(product_tag), self.logger)
            if parsed_product:
                if parsed_product in self.product_db:
                    # invoke checks
                    pass
                else:
                    self.product_db[parsed_product.article] = parsed_product
