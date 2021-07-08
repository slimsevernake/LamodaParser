import enum


class EventCode(enum.Enum):
    OK = 1,
    ERROR = 2


class Subscriber:
    def __call__(self, *args, **kwargs):
        pass


class Event:
    subscribers: list[Subscriber]

    def __init__(self):
        self.subscribers = []

    def subscribe(self, sub: Subscriber):
        self.subscribers.append(sub)

    def unsubscribe(self, sub: Subscriber):
        self.subscribers.remove(sub)

    def invoke(self, *args, **arguments):
        pass

