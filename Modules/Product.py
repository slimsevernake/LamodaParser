import enum
from discord import Embed, Colour


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

    def to_embed(self):
        result = Embed(title=self.name, url=f"{self.link}", description=f"Описание: {self.brand} | {self.type}",
                       color=Colour.magenta())
        result.set_thumbnail(url="https:"+self.image_link)
        result.add_field(name="Артикул: ", value=str(self.article), inline=False)
        # result.add_field(name="Статус: ", value=str(self.status.name.replace("_", " ")), inline=False)
        result.add_field(name="Цена: ", value=f"{self.price} RUB", inline=False)

        available_sizes = list(filter(lambda x: x["available"], self.sizes))
        if len(available_sizes) > 0:
            result.add_field(name="Размеры: ", value=f"\0", inline=False)
            for size in available_sizes:
                result.add_field(inline=True,
                                 name=f"Российский размер: {size['value']}",
                                 value=f"Размер бренда: {size['brandSize']}")
            '''if len(available_sizes) > 0:
                result.add_field(name="Доступные размеры: ",
                             value="\n".join([size["value"] for size in available_sizes]),
                             inline=False)'''
        return result


class ProductStatus(enum.Enum):
    OUT_OF_STOCK = 0,
    IN_STOCK = 1
