from Master.WebhookHandle import async_send_embed
from Modules.Product import Product
from Embeds.EmbedGenerator import EmbedGenerator


class ProductChangeHandler:
    @staticmethod
    async def on_size_changed(product: 'Product'):
        embed = EmbedGenerator.sizes_updated_embed(product)
        await async_send_embed(embed)

    @staticmethod
    async def on_price_changed(product: 'Product', old_price):
        embed = EmbedGenerator.status_updated_embed(product, old_price)
        await async_send_embed(embed)

    @staticmethod
    async def on_status_changed(product: 'Product'):
        embed = EmbedGenerator.status_updated_embed(product)
        await async_send_embed(embed)

