from ...objectives.results._objective_result import *

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
    NAME = "High Tier Item"
    def __init__(self):
        import random
        from ...data.items import Items

        random_item = random.choice(Items.GOOD)
        super().__init__(Field, Battle, random_item)
