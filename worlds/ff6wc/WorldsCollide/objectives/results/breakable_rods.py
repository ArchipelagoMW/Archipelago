from ...objectives.results._objective_result import *
from ...constants.items import BREAKABLE_RODS

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in BREAKABLE_RODS:
            src += [
                field.AddItem(item_id),
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in BREAKABLE_RODS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Breakable Rods"
    def __init__(self):
        super().__init__(Field, Battle)
