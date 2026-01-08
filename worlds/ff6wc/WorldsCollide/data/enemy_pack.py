# enemy packs are groups of either 2 or 4 enemy formations
class EnemyPack():
    FORMATION_ID_SIZE = 2

    def __init__(self, id, data):
        self.id = id

        self.formations = []
        self.extra_formations = [] # flags to randomize corresponding formation with the following 3 formations
                                   # this is used to allow 16 possible battles on the floating continent instead of only 4
        for formation_index in range(self.FORMATION_COUNT):
            formation_start = formation_index * self.FORMATION_ID_SIZE
            formation_short = int.from_bytes(data[formation_start : formation_start + self.FORMATION_ID_SIZE], "little")

            self.formations.append(formation_short & 0x7fff)                # 0x7fff is a lot of space for only 575 possible values
            self.extra_formations.append(bool(formation_short & 0x8000))

    def data(self):
        data = [0x00] * self.FORMATION_COUNT * self.FORMATION_ID_SIZE

        for formation_index in range(self.FORMATION_COUNT):
            formation_start = formation_index * self.FORMATION_ID_SIZE
            formation_short = self.formations[formation_index]

            if self.extra_formations[formation_index]:
                formation_short |= 0x8000

            data[formation_start : formation_start + self.FORMATION_ID_SIZE] = formation_short.to_bytes(2, "little")

        return data

    def print(self):
        print(f"{self.id}: ", end = '')
        for x in range(self.FORMATION_COUNT):
            print(f"{self.formations[x]}", end = ', ')
        print()

class EnemyPack2(EnemyPack):
    FORMATION_COUNT = 2

    def __init__(self, id, data):
        super().__init__(id, data)

class EnemyPack4(EnemyPack):
    FORMATION_COUNT = 4

    def __init__(self, id, data):
        super().__init__(id, data)
