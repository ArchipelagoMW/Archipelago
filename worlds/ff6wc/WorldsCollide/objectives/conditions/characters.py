from ...objectives.conditions._objective_condition import *
import random

class Condition(ObjectiveCondition):
    NAME = "Characters"
    def __init__(self, min_count, max_count):
        self.count = random.randint(min_count, max_count)
        super().__init__(ConditionType.EventWord, event_word.CHARACTERS_AVAILABLE, self.count)

    def __str__(self):
        return super().__str__(self.count)
