from dataclasses import dataclass

from worlds.rac3.constants.check_type import CHECKTYPE


@dataclass
class RAC3ADDRESSDATA:
    ADDRESS: int
    TYPE: CHECKTYPE
    VALUE: int

    def __init__(self, data: tuple[int, CHECKTYPE, int]):
        self.ADDRESS, self.TYPE, self.VALUE = data
