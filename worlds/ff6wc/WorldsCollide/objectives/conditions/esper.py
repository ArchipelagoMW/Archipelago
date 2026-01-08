from ...objectives.conditions._objective_condition import *

class Condition(ObjectiveCondition):
    NAME = "Esper"
    def __init__(self, esper):
        self.esper = esper
        super().__init__(ConditionType.Esper, self.esper)

    def __str__(self):
        return super().__str__(self.esper)
