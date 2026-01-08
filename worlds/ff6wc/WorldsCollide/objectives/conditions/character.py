from ...objectives.conditions._objective_condition import *

class Condition(ObjectiveCondition):
    NAME = "Character"
    def __init__(self, character):
        self.character = character
        super().__init__(ConditionType.Character, self.character)

    def __str__(self):
        return super().__str__(self.character)
