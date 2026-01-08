from ...objectives.results._objective_result import *
from ...data.item_names import name_id as item_name_id

TOOLS = ["Air Anchor", "AutoCrossbow", "Bio Blaster", "Chain Saw", "Debilitator", "Drill", "Flash", "NoiseBlaster"]
TOOL_IDS = [item_name_id[item_name] for item_name in TOOLS]

class Field(field_result.Result):
    def src(self):
        src = []
        for item_id in TOOL_IDS:
            src += [
                field.AddItem(item_id),
            ]
        return src

class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id in TOOL_IDS:
            src += [
                battle_result.AddItem(item_id),
            ]
        return src

class Result(ObjectiveResult):
    NAME = "Tools"
    def __init__(self):
        super().__init__(Field, Battle)
