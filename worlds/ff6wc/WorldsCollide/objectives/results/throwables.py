from ...objectives.results._objective_result import *
from ...data.item_names import name_id as item_name_id

THROWABLES = ["Shuriken", "Ninja Star", "Tack Star", "Fire Skean", "Water Edge", "Bolt Edge", "Inviz Edge",
              "Shadow Edge"]
THROWABLE_COUNTS = [20, 10, 5, 10, 10, 10, 5, 5]
THROWABLE_IDS = [item_name_id[item_name] for item_name in THROWABLES]


class Field(field_result.Result):
    def src(self):
        src = []
        for item_id, count in zip(THROWABLE_IDS, THROWABLE_COUNTS):
            for _ in range(count):
                src += [
                    field.AddItem(item_id),
                ]
        return src


class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id, count in zip(THROWABLE_IDS, THROWABLE_COUNTS):
            for _ in range(count):
                src += [
                    battle_result.AddItem(item_id),
                ]
        return src


class Result(ObjectiveResult):
    NAME = "Throwables"

    def __init__(self):
        super().__init__(Field, Battle)