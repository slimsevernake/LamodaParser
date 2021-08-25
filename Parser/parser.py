class Parser:
    @staticmethod
    def smart_search(pattern, pages=1):
        raise NotImplementedError("Base parser has no realisation for this method!")

    @staticmethod
    def parse_product(url, short_url=False):
        raise NotImplementedError("Base parser has no realisation for this method!")

    @staticmethod
    def product_by_sku(sku):
        raise NotImplementedError("Base parser has no realisation for this method!")


