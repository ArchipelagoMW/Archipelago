from ..data.ability_data import AbilityData
from ..data import text as text

class Lore(AbilityData):
    def __init__(self, id, name_data, ability_data, desc_data):
        super().__init__(id, ability_data)

        self.id = id
        self.name = text.get_string(name_data, text.TEXT2).rstrip('\0')
        self.desc = text.get_string(desc_data, text.TEXT2).rstrip('\0')

    def name_data(self):
        from ..data.lores import Lores
        data = text.get_bytes(self.name, text.TEXT2)
        data.extend([0xff] * (Lores.NAME_SIZE - len(data)))
        return data

    def desc_data(self):
        from ..data.lores import Lores
        data = text.get_bytes(self.desc, text.TEXT2)
        return data

    def get_name(self):
        return self.name.strip('\0')

    def get_desc(self):
        return self.desc.strip('\0')

    def print(self):
        print(f"{self.id} {self.get_name()}")
