

class EventCallCondition:
    def __init__(self, flag=None, value=None):
        self.flag = flag
        self.value = value

class EventCallCase:
    def __init__(self):
        self.conditions = []
        self.event = None

    def add_condition(self, flag, value):
        self.conditions.append( EventCallCondition(flag, value) )

    def encode(self):
        encoding = []
        for condition in self.conditions:
            if condition.value:
                encoding.append(0xFE)
            encoding.append(condition.flag)

        encoding.append(0xFF)
        encoding.append(self.event)

        return encoding


class EventCall:
    def __init__(self):
        self.cases = []
        self.parameters = []

    def encode(self):
        encoding = []
        for case in self.cases:
            encoding.extend(case.encode())
        encoding.extend(self.parameters)
        return encoding

    def contains_event(self, event):
        for case in self.cases:
            if case.event == event:
                return True

        return False


def decode(byte_list):
    if not byte_list:
        return None

    call = EventCall()
    data = list(byte_list)

    while 0xFF in data:
        case = EventCallCase()
        condition_bytes = data[:data.index(0xFF)]
        data = data[len(condition_bytes) + 1:]
        while condition_bytes:
            b = condition_bytes.pop(0)
            if b == 0xFE:
                b = condition_bytes.pop(0)
                case.add_condition(b, True)
            else:
                case.add_condition(b, False)

        if not data:
            # missing last event code?
            break

        case.event = data.pop(0)
        call.cases.append(case)

    call.parameters.extend(data)
    return call
