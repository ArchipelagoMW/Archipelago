from ...objectives.results._objective_result import *
from ...data import event_bit as event_bit

class Field(field_result.Result):
    def src(self):
        return [
            field.SetEventBit(event_bit.UNLOCKED_FINAL_KEFKA),
        ]

class Battle(battle_result.Result):
    def src(self):
        return [
            battle_result.SetBit(event_bit.address(event_bit.UNLOCKED_FINAL_KEFKA), event_bit.UNLOCKED_FINAL_KEFKA),
        ]

class Result(ObjectiveResult):
    NAME = "Unlock Final Kefka"
    def __init__(self):
        super().__init__(Field, Battle)
