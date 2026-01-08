from ...objectives.results._objective_result import *
from ...objectives.results._apply_characters_party import ApplyToParty

def _set_hp_one():
    current_hp_start = 0x1609

    src = ApplyToParty([
        asm.A16(),
        asm.LDA(0x0001, asm.IMM16),
        asm.STA(current_hp_start, asm.ABS_Y),
        asm.A8(),
    ])
    src += [
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, "fallen one set hp one")
    return space.start_address
set_hp_one = _set_hp_one()

class Field(field_result.Result):
    def src(self):
        return [
            field.LongCall(START_ADDRESS_SNES + set_hp_one),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            asm.JSL(START_ADDRESS_SNES + set_hp_one),
        ]

class Result(ObjectiveResult):
    NAME = "Fallen One"
    def __init__(self):
        super().__init__(Field, Battle)
