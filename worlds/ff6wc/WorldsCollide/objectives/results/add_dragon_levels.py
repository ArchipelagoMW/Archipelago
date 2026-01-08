from ...objectives.results._objective_result import *

class Field(field_result.Result):
    def src(self, levels):
        return []

class Battle(battle_result.Result):
    def src(self, levels):
        return []

class Result(ObjectiveResult):
    NAME = "Add Dragon Levels"
    def __init__(self, min_levels, max_levels):
        self.levels = random.randint(min_levels, max_levels)
        super().__init__(Field, Battle, self.levels)
