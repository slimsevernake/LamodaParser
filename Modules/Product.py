import enum


class Product:
    def __init__(self):
        self.brand = ""
        self.name = ""
        self.article = ""
        self.type = ""
        self.image = ""
        self.status = None
        self.sizes = None
        self.link = ""
        self.price = 0


class ProductStatus(enum.Enum):
    OUT_OF_STOCK = 0,
    IN_STOCK = 1
