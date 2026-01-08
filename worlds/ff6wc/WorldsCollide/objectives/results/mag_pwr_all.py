from ...objectives.results._objective_result import *
from ...objectives.results._add_sub_stat import add_stat_all, sub_stat_all

MAG_PWR_ADDRESS = 0x161d
add_mag_pwr = add_stat_all(MAG_PWR_ADDRESS, "mag_pwr")
sub_mag_pwr = sub_stat_all(MAG_PWR_ADDRESS, "mag_pwr")

class Field(field_result.Result):
    def src(self, count):
        if count < 0:
            return [
                field.LongCall(START_ADDRESS_SNES + sub_mag_pwr, -count),
            ]
        elif count > 0:
            return [
                field.LongCall(START_ADDRESS_SNES + add_mag_pwr, count),
            ]
        return []

class Battle(battle_result.Result):
    def src(self, count):
        if count < 0:
            return [
                asm.LDA(-count, asm.IMM8),
                asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
                asm.JSL(START_ADDRESS_SNES + sub_mag_pwr),
            ]
        elif count > 0:
            return [
                asm.LDA(count, asm.IMM8),
                asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
                asm.JSL(START_ADDRESS_SNES + add_mag_pwr),
            ]
        return []

class Result(ObjectiveResult):
    NAME = "MagPwr All"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
