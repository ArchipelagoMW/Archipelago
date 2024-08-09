from ..Regions.RegionDetails import RegionDetails
from ..Items.ItemReqEvalOr import ItemReqEvalOr


class ConnectionDetails:

    def __init__(self, start: RegionDetails, end: RegionDetails, itemLogic: ItemReqEvalOr):
        self.start: RegionDetails = start
        self.end: RegionDetails = end
        self.itemLogic: ItemReqEvalOr = itemLogic
        self.lambdaFunction = None
        self.car = 2

    def name(self):
        return "{} -> {}".format(self.start, self.end)

    def lamb(self, player):
        def compute(state):
            return self.itemLogic.lamb(player)(state)

        return compute

        # self.lambdaFunction = self.itemLogic.getLambda(player)
