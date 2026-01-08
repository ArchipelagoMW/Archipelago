from ...objectives.results._objective_result import *
from ...data.item_names import name_id as item_name_id

RESTORATIVES = ["Tonic", "Potion", "X-Potion", "Tincture", "Ether", "X-Ether", "Elixir", "Megalixir", "Fenix Down",
                "Revivify", "Antidote", "Eyedrop", "Soft", "Remedy", "Sleeping Bag", "Tent", "Green Cherry",
                "Echo Screen"]
RESTORATIVE_COUNTS = [10, 10, 5, 10, 10, 5, 3, 1, 10, 5, 2, 2, 2, 3, 10, 3, 2, 2]
RESTORATIVE_IDS = [item_name_id[item_name] for item_name in RESTORATIVES]


class Field(field_result.Result):
    def src(self):
        src = []
        for item_id, count in zip(RESTORATIVE_IDS, RESTORATIVE_COUNTS):
            for _ in range(count):
                src += [
                    field.AddItem(item_id),
                ]
        return src


class Battle(battle_result.Result):
    def src(self):
        src = []
        for item_id, count in zip(RESTORATIVE_IDS, RESTORATIVE_COUNTS):
            for _ in range(count):
                src += [
                    battle_result.AddItem(item_id),
                ]
        return src


class Result(ObjectiveResult):
    NAME = "Restoratives"

    def __init__(self):
        super().__init__(Field, Battle)