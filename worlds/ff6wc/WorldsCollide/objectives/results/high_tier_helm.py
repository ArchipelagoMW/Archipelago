from ...objectives.results._objective_result import *
from ...constants.items import HELMETS, EMPTY
from ...ff6wcutils.intersection import intersection

class Field(field_result.Result):
    def src(self, item_id):
        return [
            field.AddItem(item_id),
        ]

class Battle(battle_result.Result):
    def src(self, item_id):
        return [
            battle_result.AddItem(item_id),
        ]

class Result(ObjectiveResult):
    NAME = "High Tier Helm"
    def __init__(self):
        import random
        from ...data.items import Items

        good_helms = intersection(Items.GOOD, HELMETS)
        if len(good_helms) > 0:
            random_item = random.choice(good_helms)
        else:
            random_item = EMPTY
        super().__init__(Field, Battle, random_item)
