from ..data import text as text

class SwdTech:
    NAME_SIZE = 12

    def __init__(self, id, name_data):
        self.id = id
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')

    def name_data(self):
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (self.NAME_SIZE - len(data)))
        return data

    def get_name(self):
        return self.name

    def print(self):
        print(f"{self.id}: {self.name}")
