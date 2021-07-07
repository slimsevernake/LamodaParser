import enum


class Product:
    def __init__(self, brand="", name="", article="", type="", image_link="", status=None, sizes=None, link="",
                 price=0):
        self.brand = brand
        self.name = name
        self.article = article
        self.type = type
        self.image_link = image_link
        self.status = ProductStatus.IN_STOCK if status is None else ProductStatus.OUT_OF_STOCK
        self.sizes = sizes
        self.link = link
        self.price = price

    def __str__(self):
        return f"{self.brand}\n" \
               f"{self.name} | {self.type}\n" \
               f"Price: {self.price}\n" \
               f"Status: {self.status}\n" \
               f"SKU: {self.article}\n" \
               f"Link: {self.link}\n" \
               f"Image: {self.image_link}\n" \
               f"Sizes: {' '.join([size.get('value', -1) for size in self.sizes])}\n"


class ProductStatus(enum.Enum):
    OUT_OF_STOCK = 0,
    IN_STOCK = 1
