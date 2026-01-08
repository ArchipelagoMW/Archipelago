from ..data import text as text

class Dance:
    def __init__(self, id, data, name_data):
        self.id = id
        self.dances = data
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')

    def data(self):
        return self.dances

    def name_data(self):
        from ..data.dances import Dances
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Dances.NAME_SIZE - len(data)))
        return data

    def get_name(self):
        return self.name

    def print(self):
        print(f"{self.id} {self.get_name()} {self.dances}")
