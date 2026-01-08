from ...objectives.results._objective_result import *
from ...constants.items import SHIELDS, EMPTY
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
    NAME = "High Tier Shield"
    def __init__(self):
        import random
        from ...data.items import Items

        good_shields = intersection(Items.GOOD, SHIELDS)
        if len(good_shields) > 0:
            random_item = random.choice(good_shields)
        else:
            random_item = EMPTY
        super().__init__(Field, Battle, random_item)
