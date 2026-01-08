from ...objectives.results._objective_result import *
from ...constants.items import ARMORS, EMPTY
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
    NAME = "High Tier Armor"
    def __init__(self):
        import random
        from ...data.items import Items

        # filter down to just armors (or empty)
        good_armors = intersection(Items.GOOD, ARMORS)
        if len(good_armors) > 0:
            random_item = random.choice(good_armors)
        else:
            random_item = EMPTY
        super().__init__(Field, Battle, random_item)
