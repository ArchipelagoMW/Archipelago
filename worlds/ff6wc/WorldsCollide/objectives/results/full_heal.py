from ...objectives.results._objective_result import *
from ...objectives.results._apply_characters_party import ApplyToParty

def _full_heal():
    current_hp_start = 0x1609
    max_hp_start = 0x160b
    current_mp_start = 0x160d
    max_mp_start = 0x160f
    max_hp_mp_mask = 0x3fff

    character_status_start = 0x1614
    magitek_vanish_mask = 0x18 # remove all status effects except magitek and vanish

    src = ApplyToParty([
        asm.A16(),

        asm.LDA(max_hp_start, asm.ABS_Y),               # a = hp boost/max hp
        asm.AND(max_hp_mp_mask, asm.IMM16),             # a = max hp
        asm.STA(current_hp_start, asm.ABS_Y),           # current hp = max hp

        asm.LDA(max_mp_start, asm.ABS_Y),               # a = mp boost/max mp
        asm.AND(max_hp_mp_mask, asm.IMM16),             # a = max mp
        asm.STA(current_mp_start, asm.ABS_Y),           # current mp = max mp

        asm.A8(),

        asm.LDA(character_status_start, asm.ABS_Y),     # a = character's current status effect bits
        asm.AND(magitek_vanish_mask, asm.IMM8),         # remove every status except magitek/vanish
        asm.STA(character_status_start, asm.ABS_Y),     # save status effects
    ])
    src += [
        asm.RTL(),
    ]

    space = Write(Bank.F0, src, "full heal")
    return space.start_address
full_heal = _full_heal()

class Field(field_result.Result):
    def src(self):
        return [
            field.LongCall(START_ADDRESS_SNES + full_heal),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            asm.JSL(START_ADDRESS_SNES + full_heal),
        ]

class Result(ObjectiveResult):
    NAME = "Full Heal"
    def __init__(self):
        super().__init__(Field, Battle)
