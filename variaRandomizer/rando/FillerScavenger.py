import random, sys, copy, logging, time

from rando.Filler import Filler
from rando.ItemLocContainer import getLocListStr
from solver.randoSolver import RandoSolver
from utils.parameters import easy, medium, hard, harder, hardcore, mania, infinity


class ScavengerSolver(RandoSolver):
    def __init__(self, startAP, areaGraph, locations, scavLocs, maxDiff, progDiff, vcr):
        super(ScavengerSolver, self).__init__("Full", startAP, areaGraph, locations, vcr)
        self.remainingScavLocs = scavLocs
        self.maxDiff = maxDiff
        self.progDiff = progDiff
        self.threshold = self.getThreshold()
        self.visited = []
        self.scavOrder = []

    def getThreshold(self):
        if self.maxDiff >= mania:
            return harder
        else:
            return hard

    def pickupScav(self, nextScav):
        self.scavOrder.append(nextScav)
        self.remainingScavLocs.remove(nextScav)
        self.log.debug("pickupScav: {}".format(nextScav.Name))

    def chooseNextScavLoc(self, scavAvailable):
        def getHarder(th):
            if th <= easy:
                th = 0
            harder = [loc for loc in scavAvailable if loc.difficulty.difficulty >= th]
            if len(harder) > 1:
                return harder
            else:
                return getHarder(th/1.5)
        def getEasier(th):
            easier = [loc for loc in scavAvailable if loc.difficulty.difficulty < th]
            if len(easier) > 1:
                return easier
            else:
                return getEasier(th*1.5)
        if self.progDiff == "harder" and len(scavAvailable) > 1:
            harder = getHarder(self.threshold)
            return random.choice(harder)
        elif self.progDiff == "easier" and len(scavAvailable) > 1:
            easier = getEasier(self.threshold)
            return random.choice(easier)
        else:
            return random.choice(scavAvailable)

    def nextDecision(self, majorsAvailable, minorsAvailable, hasEnoughMinors, diffThreshold):
        # since solver split is forced to Full, majorsAvailable=minorsAvailable
        # we don't care about hasEnoughMinors, we're gonna pick enough anyway
        # we can ignore diffThreshold as well, we have self.maxDiff
        scavAvailable = [loc for loc in majorsAvailable if loc in self.remainingScavLocs and loc.difficulty.difficulty <= self.maxDiff and loc.comeBack == True]
        minorsAvailable = [loc for loc in majorsAvailable if loc not in self.remainingScavLocs and loc.difficulty.difficulty <= self.maxDiff and loc.comeBack == True]
        ret = None
        if len(minorsAvailable) > 0:
            nextMinor = random.choice(minorsAvailable)
            ret = self.collectMajor(nextMinor)
        elif len(scavAvailable) > 0:
            self.log.debug("scavAvailable: "+getLocListStr(scavAvailable))
            nextScav = self.chooseNextScavLoc(scavAvailable)
            self.pickupScav(nextScav)
            ret = self.collectMajor(nextScav)
        else:
            # fallback to base solver behaviour to handle comeback etc
            ret = super(ScavengerSolver, self).nextDecision(majorsAvailable, majorsAvailable, hasEnoughMinors, diffThreshold) # not a typo, the args are the same, and we overwrote minorsAvailable
            if ret is not None and ret in self.remainingScavLocs:
                self.pickupScav(ret)
        if ret is not None:
            self.visited.append(ret)
        return ret

    def cancelLastItems(self, count):
        # remove locs from scavOrder
        a=len(self.visitedLocations)-count
        for loc in self.visitedLocations[a:]:
            if loc in self.scavOrder:
                self.scavOrder.remove(loc)
                self.remainingScavLocs.append(loc)
                self.log.debug("cancel scav loc: {}".format(loc.Name))
            if loc in self.visited:
                self.visited.remove(loc)

        # call base func
        super(ScavengerSolver, self).cancelLastItems(count)

class FillerScavenger(Filler):
    def __init__(self, startAP, graph, restrictions, fullContainer, endDate=infinity):
        super(FillerScavenger, self).__init__(startAP, graph, restrictions, fullContainer, endDate)
        self.remainingScavLocs = restrictions.scavLocs[:]
        self.log.debug("FillerScavenger ctor. scavLocs="+getLocListStr(self.remainingScavLocs))

    def initContainer(self):
        self.container = self.baseContainer
        self.log.debug("FillerScavenger. container="+self.container.dump())

    def initFiller(self):
        super(FillerScavenger, self).initFiller()
        locs = self.container.getLocsForSolver()
        if self.vcr is not None:
            self.vcr.reinit('scav')
        self.solver = ScavengerSolver(self.startAP, self.graph, locs, self.remainingScavLocs, self.maxDiff, self.settings.progDiff, self.vcr)

    def itemPoolCondition(self):
        return len(self.remainingScavLocs) > 0

    def step(self):
        self.solver.solveRom()
        self.container.cleanLocsAfterSolver()
        if self.itemPoolCondition():
            return False
        # reorder item/locs in container to follow pickup order
        def indexInVisited(itemLoc):
            ret = len(self.solver.visited)
            try:
                ret = self.solver.visited.index(itemLoc.Location)
            except ValueError:
                pass
            return ret
        self.container.itemLocations.sort(key=indexInVisited)
        return True

    def getProgressionItemLocations(self):
        self.log.debug("Final Scavenger list: {}".format(getLocListStr(self.solver.scavOrder)))
        return [self.container.getItemLoc(loc) for loc in self.solver.scavOrder]
