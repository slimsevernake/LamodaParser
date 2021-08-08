from discord import Embed
from Master.ProductChangeEvent import *
from Modules.Product import Product, ProductStatus


class EmbedGenerator:
    @staticmethod
    def update_embed_field(embed: 'Embed', value: str, name: 'str'):
        field_index = EmbedGenerator.get_field_index_by_name(embed, name)
        if field_index == -1:
            return None
        embed.insert_field_at(field_index,
                              name=name,
                              value=value,
                              inline=False)
        embed.remove_field(field_index + 1)

    @staticmethod
    def get_field_index_by_name(embed: Embed, name: str) -> int:
        for field_index in range(len(embed.fields)):
            if embed.fields[field_index].name == name:
                return field_index
        return -1

    @staticmethod
    def price_updated_embed(product: 'Product', old_price: float):
        product_embed = product.to_embed()
        product_embed.description = "Цена товара изменилась: " + product_embed.description
        if product.status != ProductStatus.OUT_OF_STOCK:
            EmbedGenerator.update_embed_field(embed=product_embed,
                                              value="~~{}~~ -> {}".format(old_price, product.price),
                                              name="Цена: ")
        return product_embed

    @staticmethod
    def status_updated_embed(product: 'Product'):
        product_embed = product.to_embed()
        product_embed.description = "Статус товара изменился: " + product_embed.description
        return product_embed

    @staticmethod
    def sizes_updated_embed(product: 'Product'):
        product_embed = product.to_embed()
        product_embed.description = "Количество доступных размеров изменилось: " + product_embed.description
        return product_embed

