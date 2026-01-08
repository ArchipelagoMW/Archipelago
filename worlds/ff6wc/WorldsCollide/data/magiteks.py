from ..data.magitek import Magitek
from ..data.ability_data import AbilityData
from ..data.structures import DataArray

from ..memory.space import Bank, Reserve, Allocate, Write

class Magiteks:
    MAGITEK_COUNT = 8
    FIRE_BEAM, BOLT_BEAM, ICE_BEAM, BIO_BLAST, HEAL_FORCE, CONFUSER, X_FER, TEKMISSILE = range(MAGITEK_COUNT)

    NAMES_START = 0x26f9ad 
    NAMES_END = 0x26f9fc
    NAME_SIZE = 10

    ABILITY_DATA_START = 0x0471ea
    ABILITY_DATA_END = 0x047259

    def __init__(self, rom, args):
        self.rom = rom
        self.args = args

        self.name_data = DataArray(self.rom, self.NAMES_START, self.NAMES_END, self.NAME_SIZE)
        self.ability_data = DataArray(self.rom, self.ABILITY_DATA_START, self.ABILITY_DATA_END, AbilityData.DATA_SIZE)

        self.magiteks = []
        for magitek_index in range(len(self.ability_data)):
            magitek = Magitek(magitek_index, self.name_data[magitek_index], self.ability_data[magitek_index])
            self.magiteks.append(magitek)

    def fix_reflectable_beams(self):
        # Set the Fire/Bolt/Ice beams to ignore reflect to avoid graphical glitches
        self.magiteks[self.FIRE_BEAM].flags2 = 0x22
        self.magiteks[self.BOLT_BEAM].flags2 = 0x22
        self.magiteks[self.ICE_BEAM].flags2 = 0x22

    def mod(self):
        self.fix_reflectable_beams()
        pass

    def write(self):
        if self.args.spoiler_log:
            self.log()

        for magitek_index, magitek in enumerate(self.magiteks):
            self.name_data[magitek_index] = magitek.name_data()
            self.ability_data[magitek_index] = magitek.ability_data()

        self.name_data.write()
        self.ability_data.write()

    def log(self):
        pass

    def print(self):
        for magitek in self.magiteks:
            magitek.print()
