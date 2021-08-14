import app_logger
import Parser.parser as parser
from logging import Logger
from typing import Dict, List
from Modules.Product import Product
import manifests.test_manifest as manifest


class Monitor:
    product_db: 'Dict[str, Product]'  # SKU:str -> Product object with same SKU.
    tags: 'List[str]'
    logger: 'Logger'

    def __init__(self, manifest, logger: 'Logger' = None):
        self.product_db = {}
        self.tags = []
        self.manifest = manifest
        '''if logger:
            self.logger = logger
        else:
            self.logger = app_logger.get_logger("master")'''

    def run(self):
        for product_tag in self.manifest.products_to_monitor:
            products_found = Monitor.search(product_tag)
            for product in products_found:
                if product.sku not in self.product_db:
                    self.product_db[product.sku] = product
                else:
                    # Invoke checks.
                    pass

    # TODO: Method invokes checks.
    @staticmethod
    def check_differences():
        pass

    @staticmethod
    def search(tag: str) -> List:
        stype, stag = Monitor.get_context(tag)
        if stype is None:
            return []
        else:
            if stype == "SKU":
                return [parser.product_by_sku(stag)]
            elif stype == "EXTENDED":
                return parser.smart_search(stag)
            else:
                return parser.search(tag)

    @staticmethod
    def get_context(tag):
        splitted = tag.split(": ")
        if len(splitted) > 1:
            return splitted[0], splitted[1]
        else:
            return None, None


monitor = Monitor(manifest)
