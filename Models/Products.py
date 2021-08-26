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
class BaseProduct:
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
        self.sku = BaseProduct.make_proper_sku(new_sku)

    @staticmethod
    def get_copy(product: 'Product'):
        return BaseProduct(brand=product.brand,
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


@dataclass
class LamodaProduct(BaseProduct):
    def __str__(self):
        return f"{self.brand} | " \
               f"{self.name} | " \
               f"Price: {self.price} | " \
               f"Status: {self.status} | " \
               f"SKU: {self.sku} | " \
               f"Link: {self.link} | " \
               f"Image: {self.image_link} | " \
               f"Sizes: {' '.join([size.get('size', -1) for size in self.sizes])}"

    def to_embed(self):
        result = Embed(title=f"{self.name} | {self.brand}", url=f"{self.link}", description="",
                       color=Colour.magenta())
        if self.image_link:
            result.set_thumbnail(url=self.image_link)
        result.add_field(name="Артикул: ", value=str(self.sku), inline=False)
        result.add_field(name="Статус: ", value=self.status.name.replace("_", " "), inline=False)
        tstamp = datetime.now().strftime("%H:%M:%S")
        result.set_footer(text=f"SC 2.0 | by 5еХ9оD&Brem -- [{tstamp}]", icon_url=Embed.Empty)
        if self.status == ProductStatus.IN_STOCK:
            result.add_field(name="Цена: ", value=f"{self.price} RUB", inline=False)
        if not self.sizes:
            return result
        else:
            if len(self.sizes) > 0:
                result.add_field(name="Размеры: ", value="\0", inline=False)
                for size in self.sizes:
                    result.add_field(inline=True,
                                     name=f"Российский размер: {size['size']}",
                                     value=f"Размер бренда: {size['brand_size']}")
        return result


@dataclass
class BasketshopProduct(BaseProduct):
    def __str__(self):
        return f"{self.name} | " \
               f"Price: {self.price} | " \
               f"Status: {self.status} | " \
               f"SKU: {self.sku} | " \
               f"Link: {self.link} | " \
               f"Image: {self.image_link} | " \
               f"Sizes UK/RUS: {' '.join(self.sizes)}"

    def to_embed(self):
        result = Embed(title=f"{self.name}", url=f"{self.link}", description="",
                       color=Colour.orange())
        if self.image_link:
            result.set_thumbnail(url=self.image_link)
        result.add_field(name="Артикул: ", value=str(self.sku), inline=False)
        result.add_field(name="Статус: ", value=self.status.name.replace("_", " "), inline=False)
        tstamp = datetime.now().strftime("%H:%M:%S")
        result.set_footer(text=f"SC 2.0 | by 5еХ9оD&Brem -- [{tstamp}]", icon_url=Embed.Empty)
        if self.status == ProductStatus.IN_STOCK:
            result.add_field(name="Цена: ", value=f"{self.price} RUB", inline=False)
        if not self.sizes:
            return result
        else:
            if len(self.sizes) > 0:
                result.add_field(name="Размеры: ", value="\0", inline=False)
                for size in self.sizes:
                    result.add_field(inline=True,
                                     name=f"UK: {size.split('/')[0]}",
                                     value=f"RUS: {size.split('/')[1]}")
        return result
