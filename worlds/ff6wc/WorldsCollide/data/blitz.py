from ..data import text as text

class Blitz:
    LEVEL_SIZE = 1

    def __init__(self, id, level):
        self.id = id
        self.level = level

    def print(self):
        print(f"{self.id}: {self.level}")
