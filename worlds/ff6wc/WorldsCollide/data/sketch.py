class Sketch():
    def __init__(self, id, attack_data):
        self.id = id

        self.rare = attack_data[0]
        self.common = attack_data[1]

    def attack_data(self):
        from ..data.sketches import Sketches
        data = [0x00] * Sketches.ATTACKS_DATA_SIZE

        data[0] = self.rare
        data[1] = self.common

        return data

    def print(self):
        print(f"{self.id} {self.rare} {self.common}")
