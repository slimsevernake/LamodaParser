from discord import Color
from Models.Products import BasketshopProduct as Product


class EmbedGenerator:
    @staticmethod
    def prepare_embed(product):
        product_embed = product.to_embed()
        product_embed.color = Color.red()
        return product_embed

    @staticmethod
    def price_updated_embed(product: 'Product', old_price: float):
        product_embed = EmbedGenerator.prepare_embed(product)
        product_embed.description = "_**Цена товара изменилась: ~~{}~~ RUB -> {} RUB!**_".format(old_price, product.price)
        return product_embed

    @staticmethod
    def status_updated_embed(product: 'Product'):
        product_embed = EmbedGenerator.prepare_embed(product)
        product_embed.description = "_**Статус товара изменился!**_"
        return product_embed

    @staticmethod
    def sizes_updated_embed(product: 'Product'):
        product_embed = EmbedGenerator.prepare_embed(product)
        product_embed.description = "_**Изменились доступные размеры!**_"
        return product_embed
