from ..utils import log
from ..utils.utils import getRangeDict, chooseFromRange
from ..rando.ItemLocContainer import ItemLocation

# helper object to choose item/loc
class Choice(object):
    def __init__(self, restrictions):
        self.restrictions = restrictions
        self.settings = restrictions.settings
        self.log = log.get("Choice")

    # args are return from RandoServices.getPossiblePlacements
    # return itemLoc dict, or None if no possible choice
    def chooseItemLoc(self, itemLocDict, isProg):
        return None

    def getItemList(self, itemLocDict):
        return sorted([item for item in itemLocDict.keys()], key=lambda item: item.Type)

    def getLocList(self, itemLocDict, item):
        return sorted(itemLocDict[item], key=lambda loc: loc.Name)

# simple random choice, that chooses an item first, then a locatio to put it in
class ItemThenLocChoice(Choice):
    def __init__(self, restrictions, random):
        super(ItemThenLocChoice, self).__init__(restrictions)
        self.random = random

    def chooseItemLoc(self, itemLocDict, isProg):
        itemList = self.getItemList(itemLocDict)
        item = self.chooseItem(itemList, isProg)
        if item is None:
            return None
        locList = self.getLocList(itemLocDict, item)
        loc = self.chooseLocation(locList, item, isProg)
        if loc is None:
            return None
        return ItemLocation(item, loc)

    def chooseItem(self, itemList, isProg):
        if len(itemList) == 0:
            return None
        if isProg:
            return self.chooseItemProg(itemList)
        else:
            return self.chooseItemRandom(itemList)

    def chooseItemProg(self, itemList):
        return self.chooseItemRandom(itemList)

    def chooseItemRandom(self, itemList):
        return self.random.choice(itemList)

    def chooseLocation(self, locList, item, isProg):
        if len(locList) == 0:
            return None
        if isProg:
            return self.chooseLocationProg(locList, item)
        else:
            return self.chooseLocationRandom(locList)

    def chooseLocationProg(self, locList, item):
        return self.chooseLocationRandom(locList)

    def chooseLocationRandom(self, locList):
        return self.random.choice(locList)

# Choice specialization for prog speed based filler
class ItemThenLocChoiceProgSpeed(ItemThenLocChoice):
    def __init__(self, restrictions, progSpeedParams, distanceProp, services, random):
        super(ItemThenLocChoiceProgSpeed, self).__init__(restrictions, random)
        self.progSpeedParams = progSpeedParams
        self.distanceProp = distanceProp
        self.services = services
        self.chooseItemFuncs = {
            'Random' : self.chooseItemRandom,
            'MinProgression' : self.chooseItemMinProgression,
            'MaxProgression' : self.chooseItemMaxProgression
        }
        self.chooseLocFuncs = {
            'Random' : self.chooseLocationRandom,
            'MinDiff' : self.chooseLocationMinDiff,
            'MaxDiff' : self.chooseLocationMaxDiff
        }

    def currentLocations(self, item=None):
        return self.services.currentLocations(self.ap, self.container, item=item)

    def processLateDoors(self, itemLocDict, ap, container):
        doorBeams = self.restrictions.mandatoryBeams
        def canOpenExtendedDoors(item):
            return item.Category == 'Ammo' or item.Type in doorBeams
        # exclude door items from itemLocDict
        noDoorsLocDict = {item:locList for item,locList in itemLocDict.items() if not canOpenExtendedDoors(item) or container.sm.haveItem(item.Type)}
        if len(noDoorsLocDict) > 0:
            self.log.debug('processLateDoors. no doors')
            itemLocDict.clear()
            itemLocDict.update(noDoorsLocDict)

    def chooseItemLoc(self, itemLocDict, isProg, progressionItemLocs, ap, container):
        # if late morph, redo the late morph check if morph is the
        # only possibility since we can rollback
        canRollback = len(container.currentItems) > 0
        if self.restrictions.isLateMorph() and canRollback and len(itemLocDict) == 1:
            item, locList = list(itemLocDict.items())[0]
            if item.Type == 'Morph':
                morphLocs = self.restrictions.lateMorphCheck(container, locList, self.random)
                if morphLocs is not None:
                    itemLocDict[item] = morphLocs
                else:
                    return None
        # if a boss is available, choose it right away
        for item,locs in itemLocDict.items():
            if item.Category == 'Boss':
                assert len(locs) == 1 and locs[0].Name == item.Name
                return ItemLocation(item, locs[0])
        # late doors check for random door colors
        if self.restrictions.isLateDoors() and self.random.random() < self.lateDoorsProb:
            self.processLateDoors(itemLocDict, ap, container)
        self.progressionItemLocs = progressionItemLocs
        self.ap = ap
        self.container = container
        return super(ItemThenLocChoiceProgSpeed, self).chooseItemLoc(itemLocDict, isProg)

    def determineParameters(self, progSpeed=None, progDiff=None):
        self.chooseLocRanges = getRangeDict(self.getChooseLocs(progDiff))
        self.chooseItemRanges = getRangeDict(self.getChooseItems(progSpeed))
        self.spreadProb = self.progSpeedParams.getSpreadFactor(progSpeed)
        self.lateDoorsProb = self.progSpeedParams.getLateDoorsProb(progSpeed)

    def getChooseLocs(self, progDiff=None):
        if progDiff is None:
            progDiff = self.settings.progDiff
        return self.progSpeedParams.getChooseLocDict(progDiff)

    def getChooseItems(self, progSpeed):
        if progSpeed is None:
            progSpeed = self.settings.progSpeed
        return self.progSpeedParams.getChooseItemDict(progSpeed)

    def chooseItemProg(self, itemList):
        ret = self.getChooseFunc(self.chooseItemRanges, self.chooseItemFuncs)(itemList)
        self.log.debug('chooseItemProg. ret='+ret.Type)
        return ret

    def chooseLocationProg(self, locs, item):
        locs = self.getLocsSpreadProgression(locs)
        self.random.shuffle(locs)
        ret = self.getChooseFunc(self.chooseLocRanges, self.chooseLocFuncs)(locs)
        self.log.debug('chooseLocationProg. ret='+ret.Name)
        return ret

    # get choose function from a weighted dict
    def getChooseFunc(self, rangeDict, funcDict):
        v = chooseFromRange(rangeDict, self.random)

        return funcDict[v]

    def chooseItemMinProgression(self, items):
        minNewLocs = 1000
        ret = None

        for item in items:
            newLocs = len(self.currentLocations(item))
            if newLocs < minNewLocs:
                minNewLocs = newLocs
                ret = item
        return ret

    def chooseItemMaxProgression(self, items):
        maxNewLocs = 0
        ret = None

        for item in items:
            newLocs = len(self.currentLocations(item))
            if newLocs > maxNewLocs:
                maxNewLocs = newLocs
                ret = item
        return ret


    def chooseLocationMaxDiff(self, availableLocations):
        self.log.debug("MAX")
        self.log.debug("chooseLocationMaxDiff: {}".format([(l.Name, l.difficulty) for l in availableLocations]))
        return max(availableLocations, key=lambda loc:loc.difficulty.difficulty)

    def chooseLocationMinDiff(self, availableLocations):
        self.log.debug("MIN")
        self.log.debug("chooseLocationMinDiff: {}".format([(l.Name, l.difficulty) for l in availableLocations]))
        return min(availableLocations, key=lambda loc:loc.difficulty.difficulty)

    def areaDistance(self, loc, otherLocs):
        areas = [getattr(l, self.distanceProp) for l in otherLocs]
        cnt = areas.count(getattr(loc, self.distanceProp))
        d = None
        if cnt == 0:
            d = 2
        else:
            d = 1.0/cnt
        return d

    def getLocsSpreadProgression(self, availableLocations):
        split = self.restrictions.split
        cond = lambda item: ((split == 'Full' and item.Class == 'Major') or split == item.Class) and item.Category != "Energy"
        progLocs = [il.Location for il in self.progressionItemLocs if cond(il.Item)]
        distances = [self.areaDistance(loc, progLocs) for loc in availableLocations]
        maxDist = max(distances)
        locs = []
        for i in range(len(availableLocations)):
            loc = availableLocations[i]
            d = distances[i]
            if d == maxDist or self.random.random() >= self.spreadProb:
                locs.append(loc)
        return locs
