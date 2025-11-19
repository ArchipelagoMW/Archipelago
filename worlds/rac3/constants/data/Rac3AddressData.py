from dataclasses import dataclass

from constants.Rac3CheckType import CHECKTYPE


@dataclass
class RAC3ADDRESSDATA:
    ADDRESS: int
    TYPE: CHECKTYPE
    VALUE: int

    def __init__(self, data: tuple[int, CHECKTYPE, int]):
        self.ADDRESS, self.TYPE, self.VALUE = data
