class Incrementer:
    def __init__(self, starting_int: int):
        self.index = starting_int

    def next(self) -> int:
        current = self.index
        self.index += 1
        return current
