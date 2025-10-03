
import copy, time
from ..utils import log
from ..logic.cache import RequestCache
from ..rando.RandoServices import RandoServices
from ..rando.Choice import ItemThenLocChoice
from ..rando.RandoServices import ComebackCheckType
from ..rando.ItemLocContainer import ItemLocation, getItemLocationsStr
from ..utils.parameters import infinity
from ..logic.helpers import diffValue2txt
from ..graph.graph_utils import GraphUtils

# base class for fillers. a filler responsibility is to fill a given
# ItemLocContainer while a certain condition is fulfilled (usually
# item pool is not empty).
# entry point is generateItems
class Filler(object):
    def __init__(self, startAP, graph, restrictions, emptyContainer, endDate=infinity, *, random):
        self.startAP = startAP
        self.cache = RequestCache()
        self.graph = graph
        self.services = RandoServices(graph, restrictions, self.cache, random=random)
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.endDate = endDate
        self.baseContainer = emptyContainer
        self.maxDiff = self.settings.maxDiff
        self.log = log.get('Filler')

    # reinit algo state
    def initFiller(self):
        self.ap = self.startAP
        self.initContainer()
        self.nSteps = 0
        self.errorMsg = ""
        self.settings.maxDiff = self.maxDiff
        self.startDate = time.process_time()

    # sets up container initial state
    def initContainer(self):
        self.container = copy.copy(self.baseContainer)

    # default continuation condition: item pool is not empty
    def itemPoolCondition(self):
        return not self.container.isPoolEmpty()

    # factory for step count condition
    def createStepCountCondition(self, n):
        return lambda: self.nSteps < n

    # calls step while condition is fulfilled and we did not hit runtime limit
    # condition: continuation condition
    # vcr: debug VCR object
    # shall return (stuck, itemLoc dict list, progression itemLoc dict list)
    def generateItems(self, condition=None, vcr=None):
        self.vcr = vcr
        self.initFiller()
        if condition is None:
            condition = self.itemPoolCondition
        isStuck = False
        date = self.startDate
        while condition() and not isStuck and date <= self.endDate:
            isStuck = not self.step()
            if not isStuck:
                self.nSteps += 1
            date = time.process_time()
        if condition() or date > self.endDate:
            isStuck = True
            if date > self.endDate:
                self.errorMsg = "Exceeded time limit of "+str(self.settings.runtimeLimit_s) +" seconds"
            else:
                self.errorMsg = "STUCK !\n"+self.container.dump()
        else:
            # check if some locations are above max diff and add relevant message
            locs = self.container.getUsedLocs(lambda loc: loc.difficulty.difficulty > self.maxDiff)
            aboveMaxDiffStr = '[ ' + ' ; '.join([loc.Name + ': ' + diffValue2txt(loc.difficulty.difficulty) for loc in locs]) + ' ]'
            if aboveMaxDiffStr != '[  ]':
                self.errorMsg += "\nMaximum difficulty could not be applied everywhere. Affected locations: {}".format(aboveMaxDiffStr)
            isStuck = False

        if self.vcr != None:
            self.vcr.dump()
        return isStuck, self.container.itemLocations, self.getProgressionItemLocations()

    # helper method to collect in item/location with logic. updates self.ap and VCR
    def collect(self, itemLoc, container=None, pickup=True):
        containerArg = container
        if container is None:
            container = self.container
        location = itemLoc.Location
        item = itemLoc.Item
        pickup &= location.restricted is None or location.restricted == False
        self.ap = self.services.collect(self.ap, container, itemLoc, pickup=pickup)
        self.log.debug("AP="+self.ap)
        if self.vcr is not None and containerArg is None:
            self.vcr.addLocation(location.Name, item.Type)

    # called by generateItems at the end to knows which particulier
    # item/locations were progression, if the info is available
    def getProgressionItemLocations(self):
        return []

    # performs a fill step. can be multiple item/locations placement,
    # not necessarily just one.
    # return True if ok, False if stuck
    def step(self):
        pass

# very simple front fill algorithm with no rollback and no "softlock checks" (== dessy algorithm)
class FrontFiller(Filler):
    def __init__(self, startAP, graph, restrictions, emptyContainer, endDate=infinity, *, random):
        super(FrontFiller, self).__init__(startAP, graph, restrictions, emptyContainer, endDate, random=random)
        self.choice = ItemThenLocChoice(restrictions, random)
        self.stdStart = GraphUtils.isStandardStart(self.startAP)

    def isEarlyGame(self):
        n = 2 if self.stdStart else 3
        return len(self.container.currentItems) <= n

    # one item/loc per step
    def step(self, onlyBossCheck=False):
        self.cache.reset()
        if not self.services.can100percent(self.ap, self.container):
            comebackCheck = ComebackCheckType.ComebackWithoutItem if not self.isEarlyGame() else ComebackCheckType.NoCheck
            (itemLocDict, isProg) = self.services.getPossiblePlacements(self.ap, self.container, comebackCheck)
        else:
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
        itemLoc = self.choice.chooseItemLoc(itemLocDict, isProg)
        if itemLoc is None:
            if onlyBossCheck == False and self.services.onlyBossesLeft(self.ap, self.container):
                self.settings.maxDiff = infinity
                return self.step(onlyBossCheck=True)
            return False
        self.collect(itemLoc)
        return True
