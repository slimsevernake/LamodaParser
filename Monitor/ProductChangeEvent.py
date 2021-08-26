from Embeds.EmbedGenerator import EmbedGenerator


class ProductChangeHandler:
    @staticmethod
    def on_size_changed(product: 'Product'):
        return EmbedGenerator.sizes_updated_embed(product)

    @staticmethod
    def on_price_changed(product: 'Product', old_price):
        return EmbedGenerator.price_updated_embed(product, old_price)

    @staticmethod
    def on_status_changed(product: 'Product'):
        return EmbedGenerator.status_updated_embed(product)
