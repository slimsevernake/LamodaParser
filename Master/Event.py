import enum


class EventCode(enum.Enum):
    OK = 1,
    ERROR = 2


class AbstractResponse:
    pass


class AbstractResponse:
    message: str
    raised: bool
    code: EventCode
    inner_event: AbstractResponse

    def __init__(self):
        self.raised = False

    def append_event(self, event: AbstractResponse):
        if not self.raised:
            self.message = event.message
            self.code = event.code
            self.inner_event = event.inner_event
            self.raised = True
        else:
            temp_event = self.inner_event
            self.inner_event = event
            self.inner_event.inner_event = temp_event

    def read_event_stack(self):
        return self.inner_event


class MasterResponse(AbstractResponse):

    def __init__(self, message: str, code: EventCode = EventCode.OK):
        super().__init__()
        self.raised = True
        self.message = message
        self.code = code
