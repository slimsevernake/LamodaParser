from discord import Colour, Embed

from Master.utils import get_field_index_by_name
from WebhookHandle import send_embed
from Master.Event import Event, Subscriber
from Modules.Product import Product


class ProductChangeArgs:
    def __init__(self, product: Product, field: str, prev_data: any, new_data: any):
        self.field = field
        self.product = product
        self.prev_data = prev_data
        self.new_data = new_data

    def __str__(self):
        return "{} ---> {}".format(self.prev_data, self.new_data)


class OnProductChange(Subscriber):
    def __call__(self, args: ProductChangeArgs):
        data = args.product.to_embed()
        data.description = "Изменение в товаре\n" + data.description
        data.colour = Colour.blue()

        if args.field == "price":
            self.update(data, args, "Цена: ")
        elif args.field == "sizes":
            for size in args.prev_data:
                if size not in args.new_data:
                    field_index = get_field_index_by_name(data, size.name)
                    if field_index == -1:
                        continue
                    data.insert_field_at(field_index, name="~~{}~~".format(size.name), value="~~{}~~".format(size.value))
        send_embed(data)

    def update(self, embed: Embed, args, name: str):
        field_index = get_field_index_by_name(embed, name)
        if field_index == -1:
            return None
        embed.insert_field_at(field_index, name=name, value="~~{}~~ -> {}".format(args.prev_data, args.new_data),
                              inline=False)
        embed.remove_field(field_index + 1)


class ProductChangeEvent(Event):
    def invoke(self, args: ProductChangeArgs):
        for sub in self.subscribers:
            sub(args)
