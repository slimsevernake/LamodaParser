from Master.WebhookHandle import async_send_embed
from Master.Event import Event, Subscriber
from Modules.Product import Product
from Embeds.EmbedGenerator import EmbedGenerator


class ProductChangeArgs:
    def __init__(self, product: 'Product', field: str, prev_data: 'any', new_data: 'any'):
        self.field = field
        self.product = product
        self.prev_data = prev_data
        self.new_data = new_data

    def __str__(self):
        return "{} ---> {}".format(self.prev_data, self.new_data)


class OnProductChange(Subscriber):
    async def __call__(self, args: 'ProductChangeArgs'):
        embed = None
        if args.field == "status":
            embed = EmbedGenerator.status_updated_embed(args)
        elif args.field == "price":
            embed = EmbedGenerator.price_updated_embed(args)
        elif args.field == "size":
            embed = EmbedGenerator.sizes_updated_embed(args)
        if embed is not None:
            await async_send_embed(embed)


class ProductChangeEvent(Event):
    async def invoke(self, args: 'ProductChangeArgs'):
        for sub in self.subscribers:
            await sub(args)
