class Rage():
    def __init__(self, id, attack_data):
        self.id = id

        self.attack1 = attack_data[0]
        self.attack2 = attack_data[1]

    def attack_data(self):
        from ..data.rages import Rages
        data = [0x00] * Rages.ATTACKS_DATA_SIZE

        data[0] = self.attack1
        data[1] = self.attack2

        return data

    def print(self):
        print(f"{self.id} {self.attack1} {self.attack2}")
