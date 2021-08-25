from Modules.Product import Product, ProductStatus
from discord import Embed, Colour
from datetime import datetime
from dataclasses import dataclass

@dataclass
class LamodaProduct(Product):
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