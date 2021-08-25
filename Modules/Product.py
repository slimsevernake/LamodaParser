import copy
import enum
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from discord import Embed, Colour


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

    @staticmethod
    def make_proper_sku(sku):
        return sku.strip().upper()

    def set_sku(self, new_sku):
        self.sku = Product.make_proper_sku(new_sku)

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
        result = Embed(title=f"{self.name}", url=f"{self.link if self.link else ''}", description="Base Product",
                       color=Colour.magenta())
        tstamp = datetime.now().strftime("%H:%M:%S")
        result.set_footer(text=f"SC 2.0 | by 5еХ9оD&Brem -- [{tstamp}]", icon_url=Embed.Empty)
        return result
