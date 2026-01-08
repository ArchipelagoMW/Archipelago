from ...objectives.results._objective_result import *
from ...data.item_names import name_id as item_name_id

class Field(field_result.Result):
    def src(self, lance):
        return [
            field.AddItem(item_name_id["DragoonBoots"]),
            field.AddItem(item_name_id["Dragon Horn"]),
            field.AddItem(item_name_id[lance]),
        ]

class Battle(battle_result.Result):
    def src(self, lance):
        return [
            battle_result.AddItem(item_name_id["DragoonBoots"]),
            battle_result.AddItem(item_name_id["Dragon Horn"]),
            battle_result.AddItem(item_name_id[lance]),
        ]

class Result(ObjectiveResult):
    NAME = "Dragoon"
    def __init__(self):
        import random
        lances = ["Partisan", "Pearl Lance", "Aura Lance"]
        lance = random.choice(lances)

        super().__init__(Field, Battle, lance)
