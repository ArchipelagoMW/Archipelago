from ...objectives.conditions._objective_condition import *
from ...constants.objectives.condition_bits import boss_bit
from ...data.bosses import name_formation, name_pack

class Condition(ObjectiveCondition):
    NAME = "Boss"
    def __init__(self, boss):
        self.boss = boss
        self.boss_name = boss_bit[self.boss].name
        self.boss_formation = name_formation[self.boss_name]
        self.boss_pack = name_pack[self.boss_name]
        super().__init__(ConditionType.BattleBit, boss_bit[self.boss].bit)

    def __str__(self):
        return super().__str__(self.boss)