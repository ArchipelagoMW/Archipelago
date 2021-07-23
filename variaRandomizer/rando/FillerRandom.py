
import random, sys, copy, logging, time

from rando.Filler import Filler, FrontFiller
from rando.Choice import ItemThenLocChoice
from rando.MiniSolver import MiniSolver
from rando.ItemLocContainer import ContainerSoftBackup, ItemLocation
from rando.RandoServices import ComebackCheckType
from solver.randoSolver import RandoSolver
from utils.parameters import infinity
from logic.helpers import diffValue2txt
from logic.logic import Logic

# simple, uses mini solver only
class FillerRandom(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate=infinity, diffSteps=0):
        super(FillerRandom, self).__init__(startAP, graph, restrictions, container, endDate)
        self.miniSolver = MiniSolver(startAP, graph, restrictions)
        self.diffSteps = diffSteps
        self.beatableBackup = None
        self.nFrontFillSteps = 0
        self.stepIncr = 1

    def initFiller(self):
        super(FillerRandom, self).initFiller()
        self.log.debug("initFiller. maxDiff="+str(self.settings.maxDiff))
        self.createBaseLists()

    def createBaseLists(self):
        self.baseContainer = ContainerSoftBackup(self.container)
        self.helpContainer = ContainerSoftBackup(self.container)

    def createHelpingBaseLists(self):
        self.helpContainer = ContainerSoftBackup(self.container)

    def resetContainer(self):
        self.baseContainer.restore(self.container, resetSM=True)

    def resetHelpingContainer(self):
        self.helpContainer.restore(self.container, resetSM=False)

    def isBeatable(self, maxDiff=None):
        return self.miniSolver.isBeatable(self.container.itemLocations, maxDiff=maxDiff)

    def getLocations(self, item):
        return [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc, self.container)]

    # implemented in the speedrun version
    def getHelp(self):
        pass

    def step(self):
        # here a step is not an item collection but a whole fill attempt
        date = time.process_time()
        while not self.container.isPoolEmpty() and date <= self.endDate:
            item = random.choice(self.container.itemPool)
            locs = self.getLocations(item)
            if not locs:
                self.log.debug("FillerRandom: constraint collision during step {} for item {}/{}".format(self.nSteps, item.Type, item.Class))
                self.resetHelpingContainer()
                date = time.process_time()
                continue
            loc = random.choice(locs)
            itemLoc = ItemLocation(item, loc)
            self.container.collect(itemLoc, pickup=False)
        date = time.process_time()
        if date > self.endDate:
            return False
        # pool is exhausted, use mini solver to see if it is beatable
        if self.isBeatable():
            sys.stdout.write('o')
            sys.stdout.flush()
        else:
            if self.diffSteps > 0 and self.settings.maxDiff < infinity:
                if self.nSteps < self.diffSteps:
                    couldBeBeatable = self.isBeatable(maxDiff=infinity)
                    if couldBeBeatable:
                        difficulty = max([il.Location.difficulty.difficulty for il in self.container.itemLocations])
                        if self.beatableBackup is None or difficulty < self.beatableBackup[1]:
                            self.beatableBackup = (self.container.itemLocations, difficulty)
                elif self.beatableBackup is not None:
                    self.container.itemLocations = self.beatableBackup[0]
                    difficulty = self.beatableBackup[1]
                    self.errorMsg += "Could not find a solution compatible with max difficulty. Estimated seed difficulty: "+diffValue2txt(difficulty)
                    sys.stdout.write('O')
                    sys.stdout.flush()
                    return True
                else:
                    return False
            # reset container to force a retry
            self.resetHelpingContainer()
            if (self.nSteps + 1) % 100 == 0:
                sys.stdout.write('x')
                sys.stdout.flush()

            # help speedrun filler
            self.getHelp()

        return True

# no logic random fill with one item placement per step. intended for incremental filling,
# so does not copy initial container before filling.
class FillerRandomItems(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate, steps=0):
        super(FillerRandomItems, self).__init__(startAP, graph, restrictions, container, endDate)
        self.steps = steps

    def initContainer(self):
        self.container = self.baseContainer

    def generateItems(self, condition=None, vcr=None):
        if condition is None and self.steps > 0:
            condition = self.createStepCountCondition(self.steps)
        return super(FillerRandomItems, self).generateItems(condition, vcr)

    def step(self):
        item = random.choice(self.container.itemPool)
        locs = [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocation(item, loc, self.container)]
        loc = random.choice(locs)
        itemLoc = ItemLocation(item, loc)
        self.container.collect(itemLoc, pickup=False)
        sys.stdout.write('.')
        sys.stdout.flush()
        return True

class FrontFillerNoCopy(FrontFiller):
    def __init__(self, startAP, graph, restrictions, container, endDate):
        super(FrontFillerNoCopy, self).__init__(startAP, graph, restrictions, container, endDate)

    def initContainer(self):
        self.container = self.baseContainer

class FrontFillerKickstart(FrontFiller):
    def __init__(self, startAP, graph, restrictions, emptyContainer):
        super(FrontFillerKickstart, self).__init__(startAP, graph, restrictions, emptyContainer)

    def initContainer(self):
        self.container = self.baseContainer

    # if during a step no item is a progression item, check all two items pairs instead of just one item
    def step(self, onlyBossCheck=False):
        self.cache.reset()
        (itemLocDict, isProg) = self.services.getPossiblePlacements(self.ap, self.container, ComebackCheckType.NoCheck)
        if isProg == True:
            self.log.debug("FrontFillerKickstart: found prog item")
            return super(FrontFillerKickstart, self).step(onlyBossCheck)

        self.cache.reset()
        pair = self.services.findStartupProgItemPair(self.ap, self.container)
        if pair == None:
            # no pair found or prog item found
            return False
        itemLoc1, itemLoc2 = pair
        self.collect(itemLoc1)
        self.collect(itemLoc2)
        # we've collected two items, increase the number of steps
        self.nSteps += 1

        return True

# actual random filler will real solver on top of mini
class FillerRandomSpeedrun(FillerRandom):
    def __init__(self, graphSettings, graph, restrictions, container, endDate=infinity, diffSteps=0):
        super(FillerRandomSpeedrun, self).__init__(graphSettings.startAP, graph, restrictions, container, endDate)
        self.nFrontFillSteps = Logic.LocationsHelper.getRandomFillHelp(graphSettings.startAP)
        # based on runtime limit, help the random fill with up to three front fill steps
        limit_s = endDate - time.process_time()
        self.runtimeSteps = [limit_s/4, limit_s/2, limit_s*3/4, sys.maxsize]

    def initFiller(self):
        super(FillerRandomSpeedrun, self).initFiller()
        self.restrictions.precomputeRestrictions(self.container)
        self.progressionItemLocs = []

    # depending on the start location help the randomfill with a little bit of frontfill.
    # also if the randomfill can't find a solution, help him too with a little bit of frontfill.
    def createBaseLists(self, updateBase=True):
        if self.nFrontFillSteps > 0:
            if updateBase == False:
                super(FillerRandomSpeedrun, self).resetContainer()
            filler = FrontFillerKickstart(self.startAP, self.graph, self.restrictions, self.container)
            condition = filler.createStepCountCondition(self.nFrontFillSteps)
            (isStuck, itemLocations, progItems) = filler.generateItems(condition)
            self.log.debug(self.container.dump())
        if updateBase == True:
            # our container is updated, we can create base lists
            super(FillerRandomSpeedrun, self).createBaseLists()
            # reset help steps to zero
            self.nFrontFillSteps = 0
        else:
            super(FillerRandomSpeedrun, self).createHelpingBaseLists()

    def getLocations(self, item):
        return [loc for loc in self.container.unusedLocations if self.restrictions.canPlaceAtLocationFast(item.Type, loc.Name, self.container)]

    def isBeatable(self, maxDiff=None):
        miniOk = self.miniSolver.isBeatable(self.container.itemLocations, maxDiff=maxDiff)
        if miniOk == False:
            return False
        sys.stdout.write('s')
        if maxDiff is None:
            maxDiff = self.settings.maxDiff
        minDiff = self.settings.minDiff
        graphLocations = self.container.getLocsForSolver()
        split = self.restrictions.split if self.restrictions.split != 'Scavenger' else 'Full'
        solver = RandoSolver(split, self.startAP, self.graph, graphLocations, self.vcr)
        diff = solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if diff < minDiff: # minDiff is 0 if unspecified: that covers "unsolvable" (-1)
            sys.stdout.write('X')
            sys.stdout.flush()

            # remove vcr data
            if self.vcr is not None:
                self.vcr.empty()

            return False
        now = time.process_time()
        sys.stdout.write('S({}/{}ms)'.format(self.nSteps+1, int((now-self.startDate)*1000)))
        sys.stdout.flush()

        # order item locations with the order used by the solver
        self.orderItemLocations(solver)

        return True

    def getProgressionItemLocations(self):
        return self.progressionItemLocs

    def orderItemLocations(self, solver):
        orderedItemLocations = []
        # keep only first minors
        firstMinors = {"Missile": False, "Super": False, "PowerBomb": False}
        for loc in solver.visitedLocations:
            if loc.itemName in ["ETank", "Reserve"]:
                continue
            if loc.itemName in firstMinors:
                if firstMinors[loc.itemName] == True:
                    continue
                else:
                    firstMinors[loc.itemName] = True
            itemLoc = self.container.getItemLoc(loc)
            orderedItemLocations.append(itemLoc)
        self.progressionItemLocs = orderedItemLocations

    def getHelp(self):
        if time.process_time() > self.runtimeSteps[self.nFrontFillSteps]:
            # store the step for debug purpose
            sys.stdout.write('n({})'.format(self.nSteps))
            sys.stdout.flush()
            # help the random fill with a bit of frontfill
            self.nFrontFillSteps += self.stepIncr
            self.createBaseLists(updateBase=False)
