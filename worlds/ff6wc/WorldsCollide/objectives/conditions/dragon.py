from ...objectives.conditions._objective_condition import *
from ...constants.objectives.condition_bits import dragon_bit
from ...data.bosses import name_formation, name_pack

class Condition(ObjectiveCondition):
    NAME = "Dragon"
    def __init__(self, dragon):
        self.dragon = dragon
        self.dragon_name = dragon_bit[self.dragon].name
        self.dragon_formation = name_formation[self.dragon_name]
        self.dragon_pack = name_pack[self.dragon_name]
        super().__init__(ConditionType.BattleBit, dragon_bit[self.dragon].bit)

    def __str__(self):
        return super().__str__(self.dragon)

