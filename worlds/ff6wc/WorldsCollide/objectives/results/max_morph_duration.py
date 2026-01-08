from ...objectives.results._objective_result import *

def _max_morph_duration():
    morph_duration_address = 0x1cf6

    src = [
        asm.LDA(0xff, asm.IMM8),
        asm.STA(morph_duration_address, asm.ABS),
        asm.RTL(),
    ]
    space = Write(Bank.F0, src, "max morph duration")
    return space.start_address
max_morph_duration = _max_morph_duration()

class Field(field_result.Result):
    def src(self):
        return [
            field.LongCall(START_ADDRESS_SNES + max_morph_duration),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            asm.JSL(START_ADDRESS_SNES + max_morph_duration),
        ]

class Result(ObjectiveResult):
    NAME = "Max Morph Duration"
    def __init__(self):
        super().__init__(Field, Battle)
