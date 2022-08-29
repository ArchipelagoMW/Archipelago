class TextArchive:
    address: int = 0x000000
    size: int = 0

    scripts = []

    def __init__(self, address, size):
        self.address = address
        self.size = size

class Script:
    index: int = 0

    commands = []

    def __init__(self, index):
        self.index = index


class Command:
    command: str = ""
    parameters = []

    def __init__(self, command):
        self.command = command


class Parameter:
    key: str = ""
    value: str = ""

    def __init__(self, key, value):
        self.key = key
        self.value = value


class TextBlock:
    lines = []

    def __init__(self, lines):
        self.lines = lines


