from dataclasses import dataclass


@dataclass
class RAC3ADDRESSDATA:
    ADDRESS: int
    TYPE: int
    VALUE: int

    def __init__(self, data: tuple[int, int, int]):
        self.ADDRESS, self.TYPE, self.VALUE = data
