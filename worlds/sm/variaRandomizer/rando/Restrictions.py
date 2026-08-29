import copy
from ..utils import log
from ..graph.graph_utils import getAccessPoint
from ..rando.ItemLocContainer import getLocListStr

# Holds settings related to item placement restrictions.
# canPlaceAtLocation is the main entry point here
class Restrictions(object):
    def __init__(self, settings):
        self.log = log.get('Restrictions')
        self.settings = settings
        # Item split : Major, Chozo, Full, Scavenger
        self.split = settings.restrictions['MajorMinor']
        self.suitsRestrictions = settings.restrictions['Suits']
        self.scavLocs = None
        self.scavIsVanilla = False
        self.restrictionDictChecker = None
        if self.split == 'Scavenger':
            self.scavIsVanilla = settings.restrictions['ScavengerParams']['vanillaItems']
        # checker function chain used by canPlaceAtLocation
        self.checkers = self.getCheckers()
        self.static = {}
        self.dynamic = {}
        # only useful in door color rando
        self.mandatoryBeams = []

    def disable(self):
        self.split = "Full"
        self.suitsRestrictions = False
        self.checkers = []

    def setScavengerLocs(self, scavLocs):
        self.scavLocs = scavLocs
        self.log.debug("scavLocs="+getLocListStr(scavLocs))
        self.scavItemTypes = [loc.VanillaItemType for loc in scavLocs]

    def isEarlyMorph(self):
        return self.settings.restrictions['Morph'] == 'early'

    def isLateMorph(self):
        return self.settings.restrictions['Morph'] == 'late'

    def isLateDoors(self):
        return self.settings.restrictions['doors'] == 'late'

    def isChozo(self):
        return self.split == 'Chozo'

    def isScavenger(self):
        return self.split == "Scavenger"

    def lateMorphInit(self, ap, emptyContainer, services):
        assert self.isLateMorph()
        morph = emptyContainer.getNextItemInPool('Morph')
        assert morph is not None
        locs = services.possibleLocations(morph, ap, emptyContainer, bossesKilled=False)
        self.lateMorphLimit = len(locs)
        self.log.debug('lateMorphInit. {} locs: {}'.format(self.lateMorphLimit, getLocListStr(locs)))
        areas = {}
        for loc in locs:
            areas[loc.GraphArea] = areas.get(loc.GraphArea, 0) + 1
        self.log.debug('lateMorphLimit. areas: {}'.format(areas))
        if len(areas) > 1:
            self.lateMorphForbiddenArea = getAccessPoint(ap).GraphArea
            self.log.debug('lateMorphLimit. forbid start area: {}'.format(self.lateMorphForbiddenArea))
        else:
            self.lateMorphForbiddenArea = None

    NoCheckCat = set(['Energy', 'Nothing', 'Boss'])

    def setPlacementRestrictions(self, restrictionDict):
        self.log.debug("set placement restrictions")
        self.log.debug(restrictionDict)
        if self.restrictionDictChecker is not None:
            self.checkers.remove(self.restrictionDictChecker)
            self.restrictionDictChecker = None
        if restrictionDict is None:
            return
        self.restrictionDictChecker = lambda item, loc, cont: item.Category in Restrictions.NoCheckCat\
                                   or (item.Category == 'Ammo' and cont.hasUnrestrictedLocWithItemType(item.Type))\
                                   or loc.Name in restrictionDict[loc.GraphArea][item.Type]
        self.checkers.append(self.restrictionDictChecker)

    def isLocMajor(self, loc):
        return (not loc.isBoss() and self.split == "Full") or loc.isClass(self.split)

    def isLocMinor(self, loc):
        return not loc.isBoss() and (self.split == "Full" or not loc.isClass(self.split))

    def isItemMajor(self, item):
        if self.split == "Full":
            return True
        elif self.split == 'Scavenger':
            return not self.isItemMinor(item) or item.Type == "Ridley"
        else:
            return item.Class == self.split

    def isItemMinor(self, item):
        if self.split == "Full":
            return True
        elif self.split == 'Scavenger':
            return item.Class != "Major" or item.Category == "Energy"
        else:
            return item.Class == "Minor"

    def isItemLocMatching(self, item, loc):
        if self.split == "Full":
            return True
        if loc.isClass(self.split):
            return item.Class == self.split
        else:
            return item.Class == "Minor"

    # return True if we can keep morph as a possibility
    def lateMorphCheck(self, container, possibleLocs, random):
        # the closer we get to the limit the higher the chances of allowing morph
        proba = random.randint(0, self.lateMorphLimit)
        if self.split == 'Full':
            nbItems = len(container.currentItems)
        else:
            nbItems = len([item for item in container.currentItems if self.split == item.Class])
        if proba > nbItems:
            return None
        if self.lateMorphForbiddenArea is not None:
            morphLocs = [loc for loc in possibleLocs if loc.GraphArea != self.lateMorphForbiddenArea]
            forbidden = len(morphLocs) == 0
            possibleLocs = morphLocs if not forbidden else None
        return possibleLocs

    def isSuit(self, item):
        return item.Type == 'Varia' or item.Type == 'Gravity'
    
    def getCheckers(self):
        checkers = []
        self.log.debug("add bosses restriction")
        checkers.append(lambda item, loc, cont: (item.Category not in ['Boss', 'MiniBoss'] and not loc.isBoss()) or (item.Category in ['Boss', 'MiniBoss'] and item.Type == loc.BossItemType))
        if self.split != 'Full':
            if self.split != 'Scavenger':
                self.log.debug("add majorsSplit restriction")
                checkers.append(lambda item, loc, cont: self.isItemLocMatching(item, loc))
            else:
                self.log.debug("add scavenger restriction")
                baseScavCheck = lambda item, loc: ((loc.VanillaItemType is None and self.isItemMinor(item))
                                                or (loc.VanillaItemType is not None and self.isItemMajor(item)))
                vanillaScavCheck = lambda item, loc: (self.scavLocs is None
                                                  or (loc not in self.scavLocs and item.Type not in self.scavItemTypes)
                                                  or (item.Type == loc.VanillaItemType and loc in self.scavLocs))
                nonVanillaScavCheck = lambda item, loc: (self.scavLocs is None
                                                      or loc not in self.scavLocs
                                                      or (loc in self.scavLocs and item.Category != 'Nothing'))
                if self.scavIsVanilla:
                    checkers.append(lambda item, loc, cont: baseScavCheck(item, loc) and vanillaScavCheck(item, loc))
                else:
                    checkers.append(lambda item, loc, cont: baseScavCheck(item, loc) and nonVanillaScavCheck(item, loc))
        if self.suitsRestrictions:
            self.log.debug("add suits restriction")
            checkers.append(lambda item, loc, cont: not self.isSuit(item) or loc.GraphArea != 'Crateria')
        return checkers

    # return bool telling whether we can place a given item at a given location
    def canPlaceAtLocation(self, item, location, container):
        ret = True
        for chk in self.checkers:
            ret = ret and chk(item, location, container)
            if not ret:
                break

        return ret

    ### Below : faster implementation tailored for random fill

    def precomputeRestrictions(self, container):
        # precompute the values for canPlaceAtLocation. only for random filler.
        # dict (loc name, item type) -> bool
        items = container.getDistinctItems()
        for item in items:
            for location in container.unusedLocations:
                self.static[(location.Name, item.Type)] = self.canPlaceAtLocation(item, location, container)

        container.unrestrictedItems = set(['Super', 'PowerBomb'])
        for item in items:
            if item.Type not in ['Super', 'PowerBomb']:
                continue
            for location in container.unusedLocations:
                self.dynamic[(location.Name, item.Type)] = self.canPlaceAtLocation(item, location, container)
        container.unrestrictedItems = set()

    def canPlaceAtLocationFast(self, itemType, locName, container):
        if itemType in ['Super', 'PowerBomb'] and container.hasUnrestrictedLocWithItemType(itemType):
            return self.dynamic.get((locName, itemType))
        else:
            return self.static.get((locName, itemType))
