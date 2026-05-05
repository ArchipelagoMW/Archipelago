"""This module contains the data class for Memory Address data"""
from dataclasses import dataclass

from worlds.rac3.constants.check_type import CHECKTYPE


@dataclass
class RAC3ADDRESSDATA:
    """Memory Address data"""
    ADDRESS: int
    TYPE: CHECKTYPE
    VALUE: int

    def __init__(self, data: tuple[int, CHECKTYPE, int]):
        self.ADDRESS, self.TYPE, self.VALUE = data
