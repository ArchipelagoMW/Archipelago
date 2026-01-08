from ...objectives.results._objective_result import *

class Field(field_result.Result):
    def src(self):
        return []

class Battle(battle_result.Result):
    def src(self):
        return []

class Result(ObjectiveResult):
    NAME = "Auto Seizure"
    def __init__(self):
        super().__init__(Field, Battle)
