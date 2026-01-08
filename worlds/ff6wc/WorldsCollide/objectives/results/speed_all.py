from ...objectives.results._objective_result import *
from ...objectives.results._add_sub_stat import add_stat_all, sub_stat_all

SPEED_ADDRESS = 0x161b
add_speed = add_stat_all(SPEED_ADDRESS, "speed")
sub_speed = sub_stat_all(SPEED_ADDRESS, "speed")

class Field(field_result.Result):
    def src(self, count):
        if count < 0:
            return [
                field.LongCall(START_ADDRESS_SNES + sub_speed, -count),
            ]
        elif count > 0:
            return [
                field.LongCall(START_ADDRESS_SNES + add_speed, count),
            ]
        return []

class Battle(battle_result.Result):
    def src(self, count):
        if count < 0:
            return [
                asm.LDA(-count, asm.IMM8),
                asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
                asm.JSL(START_ADDRESS_SNES + sub_speed),
            ]
        elif count > 0:
            return [
                asm.LDA(count, asm.IMM8),
                asm.STA(field.LongCall.ARG_ADDRESS, asm.DIR),
                asm.JSL(START_ADDRESS_SNES + add_speed),
            ]
        return []

class Result(ObjectiveResult):
    NAME = "Speed All"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(Field, Battle, self.count)
