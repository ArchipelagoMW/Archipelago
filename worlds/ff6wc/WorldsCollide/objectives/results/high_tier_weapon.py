from ...objectives.results._objective_result import *
from ...constants.items import WEAPONS, EMPTY
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
    NAME = "High Tier Weapon"
    def __init__(self):
        import random
        from ...data.items import Items

        good_weapons = intersection(Items.GOOD, WEAPONS)
        if len(good_weapons) > 0:
            random_item = random.choice(good_weapons)
        else:
            random_item = EMPTY
        super().__init__(Field, Battle, random_item)
