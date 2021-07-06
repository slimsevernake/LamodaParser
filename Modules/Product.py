import enum


class Product:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.article = ""
        self.type = ""
        self.image = ""
        self.status = None
        self.available_sizes = list()
        self.link = ""
        pass


class ProductStatus(enum.Enum):
    OUT_OF_STOCK = 0,
    IN_STOCK = 1
