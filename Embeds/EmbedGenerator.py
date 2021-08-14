from Modules.Product import Product


class EmbedGenerator:
    @staticmethod
    def price_updated_embed(product: 'Product', old_price: float):
        product_embed = product.to_embed()
        product_embed.description = "Цена товара изменилась: " + "~~{}~~ -> {}".format(old_price, product.price)
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

