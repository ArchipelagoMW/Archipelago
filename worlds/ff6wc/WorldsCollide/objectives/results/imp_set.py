from ...objectives.results._objective_result import *
from ...data.item_names import name_id as item_name_id

IMP_ITEMS = ["Imp Halberd", "TortoiseShld", "Titanium", "Imp's Armor"]
IMP_ITEM_IDS = [item_name_id[item_name] for item_name in IMP_ITEMS]

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in IMP_ITEM_IDS:
            src += [
                field.AddItem(item_id)
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in IMP_ITEM_IDS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Imp Set"
    def __init__(self):
        super().__init__(Field, Battle)
