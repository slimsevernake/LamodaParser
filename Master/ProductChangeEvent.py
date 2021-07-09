from Master.Event import Event, Subscriber
from Modules.Product import Product


class ProductChangeArgs:
    def __init__(self, product: Product, prev_data: str, new_data: str):
        self.product = product
        self.prev_data = prev_data
        self.new_data = new_data

    def __str__(self):
        return "{} ---> {}".format(self.prev_data, self.new_data)


class OnProductChange(Subscriber):
    def __call__(self, args: ProductChangeArgs):

        print("[{}] {} has changed: {}".format(args.product.article, args.product.name, args))


class ProductChangeEvent(Event):
    def invoke(self, args: ProductChangeArgs):
        for sub in self.subscribers:
            sub(args)
