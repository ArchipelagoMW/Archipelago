import sys
from collections import defaultdict
from ..rando.Items import ItemManager
from ..utils.utils import getRangeDict, chooseFromRange
from ..rando.ItemLocContainer import ItemLocation

# Holder for settings and a few utility functions related to them
# (especially for plando/rando).
# Holds settings not related to graph layout.
class RandoSettings(object):
    def __init__(self, maxDiff, progSpeed, progDiff, qty, restrictions,
                 superFun, runtimeLimit_s, PlandoOptions, minDiff):
        self.progSpeed = progSpeed.lower()
        self.progDiff = progDiff.lower()
        self.maxDiff = maxDiff
        self.qty = qty
        self.restrictions = restrictions
        self.superFun = superFun
        self.runtimeLimit_s = runtimeLimit_s
        if self.runtimeLimit_s <= 0:
            self.runtimeLimit_s = sys.maxsize
        self.PlandoOptions = PlandoOptions
        self.minDiff = minDiff

    def getSuperFun(self):
        return self.superFun[:]

    def updateSuperFun(self, superFun):
        self.superFun = superFun[:]

    def isPlandoRando(self):
        return self.PlandoOptions is not None

    def getItemManager(self, smbm, nLocs, bossesItems, random):
        if not self.isPlandoRando():
            return ItemManager(self.restrictions['MajorMinor'], self.qty, smbm, nLocs, bossesItems, self.maxDiff, random)
        else:
            return ItemManager('Plando', self.qty, smbm, nLocs, bossesItems, self.maxDiff, random)

    def getExcludeItems(self, locations):
        if not self.isPlandoRando():
            return None
        exclude = {'alreadyPlacedItems': defaultdict(int), 'forbiddenItems': []}
        # locsItems is a dict {'loc name': 'item type'}
        for locName,itemType in self.PlandoOptions["locsItems"].items():
            if not any(loc.Name == locName for loc in locations):
                continue
            exclude['alreadyPlacedItems'][itemType] += 1
            exclude['alreadyPlacedItems']['total'] += 1

        exclude['forbiddenItems'] = self.PlandoOptions['forbiddenItems']

        return exclude

    def collectAlreadyPlacedItemLocations(self, container):
        if not self.isPlandoRando():
            return
        for locName,itemType in self.PlandoOptions["locsItems"].items():
            if not any(loc.Name == locName for loc in container.unusedLocations):
                continue
            item = container.getNextItemInPool(itemType)
            assert item is not None, "Invalid plando item pool"
            location = container.getLocs(lambda loc: loc.Name == locName)[0]
            itemLoc = ItemLocation(item, location)
            container.collect(itemLoc, pickup=False)

# Holds settings and utiliy functions related to graph layout
class GraphSettings(object):
    def __init__(self, player, startAP, areaRando, lightAreaRando,
                 bossRando, escapeRando, minimizerN, dotFile,
                 doorsColorsRando, allowGreyDoors, tourian,
                 plandoRandoTransitions):
        self.player = player
        self.startAP = startAP
        self.areaRando = areaRando
        self.lightAreaRando = lightAreaRando
        self.bossRando = bossRando
        self.escapeRando = escapeRando
        self.minimizerN = minimizerN
        self.dotFile = dotFile
        self.doorsColorsRando = doorsColorsRando
        self.allowGreyDoors = allowGreyDoors
        self.tourian = tourian
        self.plandoRandoTransitions = plandoRandoTransitions

    def isMinimizer(self):
        return self.minimizerN is not None

# algo settings depending on prog speed (slowest to fastest+variable,
# other "speeds" are actually different algorithms)
class ProgSpeedParameters(object):
    def __init__(self, restrictions, nLocs):
        self.restrictions = restrictions
        self.nLocs = nLocs

    def getVariableSpeed(self, random):
        ranges = getRangeDict({
            'slowest':7,
            'slow':20,
            'medium':35,
            'fast':27,
            'fastest':11
        })
        return chooseFromRange(ranges, random)

    def getMinorHelpProb(self, progSpeed):
        if self.restrictions.split != 'Major':
            return 0
        if progSpeed == 'slowest':
            return 0.16
        elif progSpeed == 'slow':
            return 0.33
        elif progSpeed == 'medium':
            return 0.5
        return 1

    def getLateDoorsProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 1
        elif progSpeed == 'slow':
            return 0.8
        elif progSpeed == 'medium':
            return 0.66
        elif progSpeed == 'fast':
            return 0.5
        elif progSpeed == 'fastest':
            return 0.33
        return 0
    
    # chozo/slowest can make seed generation fail often, not much
    # of a gameplay difference between slow/slowest in Chozo anyway,
    # so we merge slow and slowest for some params
    def isSlow(self, progSpeed):
        return progSpeed == "slow" or (progSpeed == "slowest" and self.restrictions.split == "Chozo")

    def getItemLimit(self, progSpeed, random):
        itemLimit = self.nLocs
        if self.isSlow(progSpeed):
            itemLimit = int(self.nLocs*0.209) # 21 for 105
        elif progSpeed == 'medium':
            itemLimit = int(self.nLocs*0.095) # 9 for 105
        elif progSpeed == 'fast':
            itemLimit = int(self.nLocs*0.057) # 5 for 105
        elif progSpeed == 'fastest':
            itemLimit = int(self.nLocs*0.019) # 1 for 105
        minLimit = itemLimit - int(itemLimit/5)
        maxLimit = itemLimit + int(itemLimit/5)
        if minLimit == maxLimit:
            itemLimit = minLimit
        else:
            itemLimit = random.randint(minLimit, maxLimit)
        return itemLimit

    def getLocLimit(self, progSpeed):
        locLimit = -1
        if self.isSlow(progSpeed):
            locLimit = 1
        elif progSpeed == 'medium':
            locLimit = 2
        elif progSpeed == 'fast':
            locLimit = 3
        elif progSpeed == 'fastest':
            locLimit = 4
        return locLimit

    def getProgressionItemTypes(self, progSpeed):
        progTypes = ItemManager.getProgTypes()
        if self.restrictions.isLateDoors():
            progTypes += ['Wave','Spazer','Plasma']
        progTypes.append('Charge')
        if progSpeed == 'slowest' and self.restrictions.split != "Chozo":
            return progTypes
        else:
            progTypes.remove('HiJump')
            progTypes.remove('Charge')
        if self.isSlow(progSpeed):
            return progTypes
        else:
            progTypes.remove('Bomb')
            progTypes.remove('Grapple')
        if progSpeed == 'medium':
            return progTypes
        else:
            if not self.restrictions.isLateDoors():
                progTypes.remove('Ice')
            progTypes.remove('SpaceJump')
        if progSpeed == 'fast':
            return progTypes
        else:
            progTypes.remove('SpeedBooster')
        if progSpeed == 'fastest':
            return progTypes # only morph, varia, gravity
        raise RuntimeError("Unknown prog speed " + progSpeed)

    def getPossibleSoftlockProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 1
        if progSpeed == 'slow':
            return 0.66
        if progSpeed == 'medium':
            return 0.33
        if progSpeed == 'fast':
            return 0.1
        if progSpeed == 'fastest':
            return 0
        raise RuntimeError("Unknown prog speed " + progSpeed)

    def getChooseLocDict(self, progDiff):
        if progDiff == 'normal':
            return {
                'Random' : 1,
                'MinDiff' : 0,
                'MaxDiff' : 0
            }
        elif progDiff == 'easier':
            return {
                'Random' : 2,
                'MinDiff' : 1,
                'MaxDiff' : 0
            }
        elif progDiff == 'harder':
            return {
                'Random' : 2,
                'MinDiff' : 0,
                'MaxDiff' : 1
            }

    def getChooseItemDict(self, progSpeed):
        if progSpeed == 'slowest':
            return {
                'MinProgression' : 1,
                'Random' : 2,
                'MaxProgression' : 0
            }
        elif progSpeed == 'slow':
            return {
                'MinProgression' : 25,
                'Random' : 75,
                'MaxProgression' : 0
            }
        elif progSpeed == 'medium':
            return {
                'MinProgression' : 0,
                'Random' : 1,
                'MaxProgression' : 0
            }
        elif progSpeed == 'fast':
            return {
                'MinProgression' : 0,
                'Random' : 85,
                'MaxProgression' : 15
            }
        elif progSpeed == 'fastest':
            return {
                'MinProgression' : 0,
                'Random' : 2,
                'MaxProgression' : 1
            }

    def getSpreadFactor(self, progSpeed):
        if progSpeed == 'slowest':
            return 0.9
        elif progSpeed == 'slow':
            return 0.7
        elif progSpeed == 'medium':
            return 0.4
        elif progSpeed == 'fast':
            return 0.1
        return 0

    def getChozoSecondPhaseRestrictionProb(self, progSpeed):
        if progSpeed == 'slowest':
            return 0
        if progSpeed == 'slow':
            return 0.16
        if progSpeed == 'medium':
            return 0.5
        if progSpeed == 'fast':
            return 0.9
        return 1
