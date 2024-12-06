

import typing
from .ItemReqEvalAnd import ItemReqEvalAnd
from .ItemDetail import ItemDetail

class ItemReqEvalOr:

    def __init__(self, conditions: typing.List[ItemReqEvalAnd]):
        self.conditions = conditions
        self.lambdaFunction = None

    def evaluate(self, itemsToEvalWith: typing.Set[str]) -> bool:
        if len(self.conditions) == 0:
            return True
        for c in self.conditions:
            if c.evaluate(itemsToEvalWith):
                return True
        return False

    def logicToString(self) -> str:
        st = ""
        first = True
        for andLgc in self.conditions:
            if not first:
                st += " or ("
            else:
                st += "("
                first = False
            st += andLgc.logicToString()
            st += ")"
        return st


    def addAndLogic(self, detail: ItemDetail):
        for andLgc in self.conditions:
            andLgc.addAndLogic(detail)

    def lamb(self, player: int):

        def compute(state):

            # return true if there is no logic
            if len(self.conditions) <= 0:
                return True

            # we need to look and check if any is true, then return true
            for and_condition in self.conditions:
                if and_condition.lamb(player)(state):
                    return True

            # if there were no possible conditions that worked, return false
            return False

        return compute