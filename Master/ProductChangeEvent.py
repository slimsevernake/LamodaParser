from Master.Event import Event, Subscriber


class ProductChangeArgs:
    def __init__(self, prev_data: str, new_data: str):
        self.prev_data = prev_data
        self.new_data = new_data

    def __str__(self):
        return "{} ---> {}".format(self.prev_data, self.new_data)


class OnProductChange(Subscriber):
    def __call__(self, sender: object, args: ProductChangeArgs):
        print("{} sent data: {}".format(sender, args))


class ProductChangeEvent(Event):
    def invoke(self, sender: object, args: ProductChangeArgs):
        super().invoke(sender, args)