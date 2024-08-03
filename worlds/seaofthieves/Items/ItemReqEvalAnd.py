

import typing
from .ItemDetail import ItemDetail

class ItemReqEvalAnd:

    def __init__(self, condition: typing.List[ItemDetail]):
        self.condition: typing.List[ItemDetail] = condition
        self.lambdaFunction = None
        pass

    def evaluate(self, itemsToEvalWith: typing.Set[str]) -> bool:
        for itm_detail in self.condition:
            if (itm_detail.name not in itemsToEvalWith):
                return False
        return True

    def logicToString(self) -> str:
        st = ""
        first = True
        for det in self.condition:
            if not first:
                st += ", "
            else:
                first = False
            st += det.name
        return st
    def addAndLogic(self, item: ItemDetail):
        self.condition.append(item)

    def lamb(self, player):

        def compute(state):

            # if no requirement return true
            if len(self.condition) <= 0:
                return True

            item_names = []
            for item_detail in self.condition:
                item_names.append(item_detail.name)
                # rules.append(lambda state: state.has(item_detail.name, player, item_detail.req_qty))
            return state.has_all(item_names.copy(), player)

        return compute