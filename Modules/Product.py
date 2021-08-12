import enum
from dataclasses import dataclass
from typing import Optional
from discord import Embed, Colour
import copy


class ProductStatus(enum.Enum):
    OUT_OF_STOCK = 0,
    IN_STOCK = 1


@dataclass
class Product:
    brand: Optional[str]
    name: Optional[str]
    sku: Optional[str]
    image_link: Optional[str]
    status: Optional[ProductStatus]
    sizes: Optional[list]
    link: Optional[str]
    price: Optional[float]

    def __str__(self):
        return f"{self.brand} | " \
               f"{self.name} | " \
               f"Price: {self.price} | " \
               f"Status: {self.status} | " \
               f"SKU: {self.sku} | " \
               f"Link: {self.link} | " \
               f"Image: {self.image_link} | " \
               f"Sizes: {' '.join([size.get('value', -1) for size in self.sizes])}"

    def set_sku(self, new_sku):
        self.sku = new_sku.upper()

    @staticmethod
    def get_copy(product: 'Product'):
        return Product(brand=product.brand,
                       name=product.name,
                       sku=product.sku,
                       image_link=product.image_link,
                       status=product.status,
                       sizes=copy.deepcopy(product.sizes),
                       link=product.link,
                       price=product.price)

    def to_embed(self):
        print("EMBEDDED!")
        result = Embed(title=self.name, url=f"{self.link}", description=f"Описание: {self.brand}",
                       color=Colour.magenta())
        result.set_thumbnail(url=self.image_link)
        result.add_field(name="Артикул: ", value=str(self.sku), inline=False)
        result.add_field(name="Статус: ", value=self.status.name.replace("_", " "), inline=False)
        if self.status == ProductStatus.IN_STOCK:
            result.add_field(name="Цена: ", value=f"{self.price} RUB", inline=False)
        if not self.sizes:
            return result
        else:
            if len(self.sizes) > 0:
                result.add_field(name="Размеры: ", value=f"\0", inline=False)
                for size in self.sizes:
                    result.add_field(inline=True,
                                     name=f"Российский размер: {size['value']}",
                                     value=f"Размер бренда: {size['brandSize']}")
        return result
