import copy

from ..utils import log
from ..utils.utils import randGaussBounds
from ..logic.smbool import SMBool, smboolFalse
from ..logic.smboolmanager import SMBoolManager
from ..logic.helpers import Bosses
from ..graph.graph_utils import getAccessPoint, GraphUtils
from ..rando.Filler import FrontFiller
from ..rando.ItemLocContainer import ItemLocContainer, getLocListStr, ItemLocation, getItemListStr
from ..rando.Restrictions import Restrictions
from ..utils.objectives import Objectives
from ..utils.parameters import infinity
from ..rom.rom_patches import RomPatches

# checks init conditions for the randomizer: processes super fun settings, graph, start location, special restrictions
# the entry point is createItemLocContainer
class RandoSetup(object):
    def __init__(self, graphSettings, locations, services, player, random):
        self.sm = SMBoolManager(player, services.settings.maxDiff)
        self.random = random
        self.settings = services.settings
        self.graphSettings = graphSettings
        self.startAP = graphSettings.startAP
        self.superFun = self.settings.getSuperFun()
        self.container = None
        self.services = services
        self.restrictions = services.restrictions
        self.areaGraph = services.areaGraph
        self.allLocations = locations
        self.locations = self.areaGraph.getAccessibleLocations(locations, self.startAP)
#        print("nLocs Setup: "+str(len(self.locations)))
        # in minimizer we can have some missing boss locs
        bossesItems = [loc.BossItemType for loc in self.locations if loc.isBoss()]
        self.itemManager = self.settings.getItemManager(self.sm, len(self.locations), bossesItems, random)
        self.forbiddenItems = []
        self.restrictedLocs = []
        self.lastRestricted = []
        self.bossesLocs = sorted(['Draygon', 'Kraid', 'Ridley', 'Phantoon', 'Mother Brain'])
        self.suits = ['Varia', 'Gravity']
        # organized by priority
        self.movementItems = ['SpaceJump', 'HiJump', 'SpeedBooster', 'Bomb', 'Grapple', 'SpringBall']
        # organized by priority
        self.combatItems = ['ScrewAttack', 'Plasma', 'Wave', 'Spazer']
        # OMG
        self.bossChecks = {
            'Kraid' : self.sm.enoughStuffsKraid,
            'Phantoon' : self.sm.enoughStuffsPhantoon,
            'Draygon' : self.sm.enoughStuffsDraygon,
            'Ridley' : self.sm.enoughStuffsRidley,
            'Mother Brain': self.sm.enoughStuffsMotherbrain
        }
        self.okay = lambda: SMBool(True, 0)
        exclude = self.settings.getExcludeItems(self.locations)
        # we have to use item manager only once, otherwise pool will change
        self.itemManager.createItemPool(exclude)
        self.basePool = self.itemManager.getItemPool()[:]
        self.log = log.get('RandoSetup')
        if len(locations) != len(self.locations):
            self.log.debug("inaccessible locations :"+getLocListStr([loc for loc in locations if loc not in self.locations]))

    # processes everything and returns an ItemLocContainer, or None if failed (invalid init conditions/settings)
    def createItemLocContainer(self, endDate, vcr=None):
        self.getForbidden()
        self.log.debug("LAST CHECKPOOL")
        if not self.checkPool():
            self.log.debug("createItemLocContainer: last checkPool fail")
            return None
        # reset restricted in locs from previous attempt
        for loc in self.locations:
            loc.restricted = False
        for loc in self.restrictedLocs:
            self.log.debug("createItemLocContainer: loc is restricted: {}".format(loc.Name))
            loc.restricted = True
        
        # checkDoorBeams calls checkPool, so save error messages
        errorMsgsBck = self.errorMsgs[:]
        self.checkDoorBeams()
        self.errorMsgs = errorMsgsBck
        
        self.container = ItemLocContainer(self.sm, self.getItemPool(), self.locations)
        if self.restrictions.isLateMorph():
            self.restrictions.lateMorphInit(self.startAP, self.container, self.services)
            isStdStart = GraphUtils.isStandardStart(self.startAP)
            # ensure we have an area layout that can put morph outside start area
            # TODO::allow for custom start which doesn't require morph early
            if self.graphSettings.areaRando and isStdStart and not self.restrictions.suitsRestrictions and self.restrictions.lateMorphForbiddenArea is None:
                self.container = None
                self.log.debug("createItemLocContainer: checkLateMorph fail")
                return None
        # checkStart needs the container
        if not self.checkStart():
            self.container = None
            self.log.debug("createItemLocContainer: checkStart fail")
            return None
        self.settings.updateSuperFun(self.superFun)
        return self.container

    def getRestrictionsDict(self):
        itemTypes = {item.Type for item in self.container.itemPool if item.Category not in Restrictions.NoCheckCat}
        allAreas = {loc.GraphArea for loc in self.locations}
        items = [self.container.getNextItemInPool(itemType) for itemType in itemTypes]
        restrictionDict = {}
        for area in allAreas:
            restrictionDict[area] = {}
            for itemType in itemTypes:
                restrictionDict[area][itemType] = set()
        for item in items:
            itemType = item.Type
            poss = self.services.possibleLocations(item, self.startAP, self.container)
            for loc in poss:
                restrictionDict[loc.GraphArea][itemType].add(loc.Name)
        if self.restrictions.isEarlyMorph() and GraphUtils.isStandardStart(self.startAP):
            morphLocs = ['Morphing Ball']
            if self.restrictions.split in ['Full', 'Major']:
                dboost = self.sm.knowsCeilingDBoost()
                if dboost.bool == True and dboost.difficulty <= self.settings.maxDiff:
                    morphLocs.append('Energy Tank, Brinstar Ceiling')
            for area, locDict in restrictionDict.items():
                if area == 'Crateria':
                    locDict['Morph'] = set(morphLocs)
                else:
                    locDict['Morph'] = set()
        return restrictionDict

    # fill up unreachable locations with "junk" to maximize the chance of the ROM
    # to be finishable
    def fillRestrictedLocations(self):
        def getPred(itemType, loc):
            return lambda item: (itemType is None or item.Type == itemType) and self.restrictions.canPlaceAtLocation(item, loc, self.container)
        locs = self.restrictedLocs
        self.log.debug("fillRestrictedLocations. locs="+getLocListStr(locs))
        for loc in locs:
            itemLocation = ItemLocation(None, loc)
            if loc.BossItemType is not None:
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred(loc.BossItemType, loc))
            elif self.container.hasItemInPool(getPred('Nothing', loc)):
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('Nothing', loc))
            elif self.container.hasItemInPool(getPred('NoEnergy', loc)):
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('NoEnergy', loc))
            elif self.container.countItems(getPred('Missile', loc)) > 3:
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('Missile', loc))
            elif self.container.countItems(getPred('Super', loc)) > 2:
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('Super', loc))
            elif self.container.countItems(getPred('PowerBomb', loc)) > 1:
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('PowerBomb', loc))
            elif self.container.countItems(getPred('Reserve', loc)) > 1:
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('Reserve', loc))
            elif self.container.countItems(getPred('ETank', loc)) > 3:
                itemLocation.Item = self.container.getNextItemInPoolMatching(getPred('ETank', loc))
            else:
                raise RuntimeError("Cannot fill restricted locations")
            self.log.debug("Fill: {}/{} at {}".format(itemLocation.Item.Type, itemLocation.Item.Class, itemLocation.Location.Name))
            self.container.collect(itemLocation, False)

    def getItemPool(self, forbidden=[]):
        self.itemManager.setItemPool(self.basePool[:]) # reuse base pool to have constant base item set
        return self.itemManager.removeForbiddenItems(self.forbiddenItems + forbidden)

    # if needed, do a simplified "pre-randomization" of a few items to check start AP/area layout validity
    def checkStart(self):
        ap = getAccessPoint(self.startAP)
        if not self.graphSettings.areaRando or ap.Start is None or \
           (('needsPreRando' not in ap.Start or not ap.Start['needsPreRando']) and\
            ('areaMode' not in ap.Start or not ap.Start['areaMode'])):
            return True
        self.log.debug("********* PRE RANDO START")
        container = copy.copy(self.container)
        filler = FrontFiller(self.startAP, self.areaGraph, self.restrictions, container, random=self.random)
        condition = filler.createStepCountCondition(4)
        (isStuck, itemLocations, progItems) = filler.generateItems(condition)
        self.log.debug("********* PRE RANDO END")
        return not isStuck and len(self.services.currentLocations(filler.ap, filler.container)) > 0

    # in door color rando, determine mandatory beams
    def checkDoorBeams(self):
        if self.restrictions.isLateDoors():
            doorBeams = ['Wave','Ice','Spazer','Plasma']
            self.restrictions.mandatoryBeams = [beam for beam in doorBeams if not self.checkPool(forbidden=[beam])]
            self.log.debug("checkDoorBeams. mandatoryBeams="+str(self.restrictions.mandatoryBeams))

    def checkPool(self, forbidden=None):
        self.errorMsgs = []
        self.log.debug("checkPool. forbidden=" + str(forbidden) + ", self.forbiddenItems=" + str(self.forbiddenItems))
        if not self.graphSettings.isMinimizer() and not self.settings.isPlandoRando() and len(self.allLocations) > len(self.locations):
            # invalid graph with looped areas
            msg = "not all areas are connected, but minimizer param is off / not a plando rando"
            self.log.debug("checkPool: {}".format(msg))
            self.errorMsgs.append(msg)
            return False
        ret = True
        if forbidden is not None:
            pool = self.getItemPool(forbidden)
        else:
            pool = self.getItemPool()
        # get restricted locs
        totalAvailLocs = []
        comeBack = {}
        try:
            container = ItemLocContainer(self.sm, pool, self.locations)
        except AssertionError as e:
            # invalid graph altogether
            msg = "AssertionError when creating ItemLocContainer: {}".format(e)
            self.log.debug("checkPool: {}".format(msg))
            self.errorMsgs.append(msg)
            return False
        # restrict item pool in chozo: game should be finishable with chozo items only
        contPool = []
        contPool += [item for item in pool if item in container.itemPool]
        # give us everything and beat every boss to see what we can access
        self.disableBossChecks()
        self.sm.resetItems()
        self.sm.addItems([item.Type for item in contPool]) # will add bosses as well
        self.log.debug('pool={}'.format(getItemListStr(container.itemPool)))
        locs = self.services.currentLocations(self.startAP, container, post=True)
        self.areaGraph.useCache(True)
        for loc in locs:
            ap = loc.accessPoint
            if ap not in comeBack:
                # we chose Golden Four because it is always there.
                # Start APs might not have comeback transitions
                # possible start AP issues are handled in checkStart
                comeBack[ap] = self.areaGraph.canAccess(self.sm, ap, 'Golden Four', self.settings.maxDiff)
            if comeBack[ap]:
                totalAvailLocs.append(loc)
        self.areaGraph.useCache(False)
        self.lastRestricted = [loc for loc in self.locations if loc not in totalAvailLocs]
        self.log.debug("restricted=" + str([loc.Name for loc in self.lastRestricted]))

        # check if objectives are compatible with accessible APs
        startAP = self.areaGraph.accessPoints[self.startAP]
        availAPs = [ap.Name for ap in self.areaGraph.getAvailableAccessPoints(startAP, self.sm, self.settings.maxDiff)]
        self.log.debug("availAPs="+str(availAPs))
        for goal in Objectives.objDict[self.graphSettings.player].activeGoals:
            n, aps = goal.escapeAccessPoints
            if len(aps) == 0:
                continue
            escAPs = [ap for ap in aps if ap in availAPs]
            self.log.debug("escAPs="+str(escAPs))
            if len(escAPs) < n:
                msg = "goal '{}' impossible to complete due to area layout".format(goal.name)
                self.log.debug("checkPool. {}".format(msg))
                self.errorMsgs.append(msg)
                ret = False
                continue
            for ap in escAPs:
                if not self.areaGraph.canAccess(self.sm, ap, "Golden Four", self.settings.maxDiff):
                    msg = "goal '{}' impossible to complete due to area layout".format(goal.name)
                    self.log.debug("checkPool. {}".format(msg))
                    self.errorMsgs.append(msg)
                    ret = False
                    break
        # check if all inter-area APs can reach each other
        if ret:
            interAPs = [ap for ap in self.areaGraph.getAccessibleAccessPoints(self.startAP) if not ap.isInternal() and not ap.isLoop()]
            for startAp in interAPs:
                availAccessPoints = self.areaGraph.getAvailableAccessPoints(startAp, self.sm, self.settings.maxDiff)
                for ap in interAPs:
                    if not ap in availAccessPoints:
                        self.log.debug("checkPool: ap {} non accessible from {}".format(ap.Name, startAp.Name))
                        ret = False
            if not ret:
                msg = "inter-area APs check failed"
                self.log.debug("checkPool. {}".format(msg))
                self.errorMsgs.append(msg)
        # cleanup
        self.sm.resetItems()
        self.restoreBossChecks()
        # check if we can reach/beat all bosses
        if ret:
            # always add G4 to mandatory bosses, even if not required by objectives
            mandatoryBosses = set(Objectives.objDict[self.sm.player].getMandatoryBosses() + Bosses.Golden4())

            for loc in self.lastRestricted:
                if loc.Name in self.bossesLocs:
                    ret = False
                    msg = "unavail Boss: {}".format(loc.Name)
                    self.log.debug("checkPool. {}".format(msg))
            if ret:
                # revive bosses
                self.sm.addItems([item.Type for item in contPool if item.Category != 'Boss'])
                maxDiff = self.settings.maxDiff
                # see if phantoon doesn't block himself, and if we can reach draygon if she's alive
                ret = self.areaGraph.canAccess(self.sm, self.startAP, 'PhantoonRoomIn', maxDiff)\
                      and self.areaGraph.canAccess(self.sm, self.startAP, 'DraygonRoomIn', maxDiff)
                if ret:
                    # see if we can beat bosses with this equipment (infinity as max diff for a "onlyBossesLeft" type check
                    beatableBosses = sorted([loc.BossItemType for loc in self.services.currentLocations(self.startAP, container, diff=infinity) if loc.isBoss()])
                    self.log.debug("checkPool. beatableBosses="+str(beatableBosses))
                    self.log.debug("checkPool. mandatoryBosses: {}".format(mandatoryBosses))
                    ret = mandatoryBosses.issubset(set(beatableBosses)) and Objectives.objDict[self.sm.player].checkLimitObjectives(beatableBosses)
                    if ret:
                        # check that we can then kill mother brain
                        self.sm.addItems(Bosses.Golden4() + Bosses.miniBosses())
                        beatableMotherBrain = [loc.Name for loc in self.services.currentLocations(self.startAP, container, diff=infinity) if loc.Name == 'Mother Brain']
                        ret = len(beatableMotherBrain) > 0
                        self.log.debug("checkPool. beatable Mother Brain={}".format(ret))
                    else:
                        msg = "can't kill all mandatory bosses/minibosses: {}".format(', '.join(list(mandatoryBosses - set(beatableBosses))))
                        self.log.debug("checkPool. {}".format(msg))
                        self.errorMsgs.append(msg)
                else:
                    msg = "locked by Phantoon or Draygon"
                    self.log.debug('checkPool. {}'.format(msg))
                    self.errorMsgs.append(msg)
                self.log.debug('checkPool. boss access sanity check: '+str(ret))

        if self.restrictions.isChozo() or self.restrictions.isScavenger():
            # in chozo or scavenger, we cannot put other items than NoEnergy in the restricted locations,
            # we would be forced to put majors in there, which can make seed generation fail:
            # don't put more restricted major locations than removed major items
            # FIXME something to do there for chozo/ultra sparse, it gives us up to 3 more spots for nothing items
            restrictedLocs = self.restrictedLocs + [loc for loc in self.lastRestricted if loc not in self.restrictedLocs]
            nRestrictedMajor = sum(1 for loc in restrictedLocs if self.restrictions.isLocMajor(loc))
            nNothingMajor = sum(1 for item in pool if self.restrictions.isItemMajor(item) and item.Category == 'Nothing')
            ret &= nRestrictedMajor <= nNothingMajor
            self.log.debug('checkPool. nRestrictedMajor='+str(nRestrictedMajor)+', nNothingMajor='+str(nNothingMajor))
        self.log.debug('checkPool. result: '+str(ret))
        return ret

    def disableBossChecks(self):
        self.sm.enoughStuffsKraid = self.okay
        self.sm.enoughStuffsPhantoon = self.okay
        self.sm.enoughStuffsDraygon = self.okay
        self.sm.enoughStuffsRidley = self.okay
        def mbCheck():
            (possible, energyDiff) = self.sm.mbEtankCheck()
            if possible == True:
                return self.okay()
            return smboolFalse
        self.sm.enoughStuffsMotherbrain = mbCheck

    def restoreBossChecks(self):
        self.sm.enoughStuffsKraid = self.bossChecks['Kraid']
        self.sm.enoughStuffsPhantoon = self.bossChecks['Phantoon']
        self.sm.enoughStuffsDraygon = self.bossChecks['Draygon']
        self.sm.enoughStuffsRidley = self.bossChecks['Ridley']
        self.sm.enoughStuffsMotherbrain = self.bossChecks['Mother Brain']

    def addRestricted(self):
        self.checkPool()
        for r in self.lastRestricted:
            if r not in self.restrictedLocs:
                self.restrictedLocs.append(r)

    def getForbiddenItemsFromList(self, itemList):
        self.log.debug('getForbiddenItemsFromList: ' + str(itemList))
        remove = []
        n = randGaussBounds(self.random, len(itemList))
        for i in range(n):
            idx = self.random.randint(0, len(itemList) - 1)
            item = itemList.pop(idx)
            if item is not None:
                remove.append(item)
        return remove

    def addForbidden(self, removable):
        forb = None
        # it can take several tries if some item combination removal
        # forbids access to more stuff than each individually
        tries = 0
        while forb is None and tries < 100:
            forb = self.getForbiddenItemsFromList(removable[:])
            self.log.debug("addForbidden. forb="+str(forb))
            if self.checkPool(forb) == False:
                forb = None
            tries += 1
        if forb is None:
            # we couldn't find a combination, just pick an item
            firstItem = next((itemType for itemType in removable if itemType is not None), None)
            if firstItem is not None:
                forb = [firstItem]
            else:
                forb = []
        self.forbiddenItems += forb
        self.addRestricted()
        return len(forb)

    def getForbiddenSuits(self):
        self.log.debug("getForbiddenSuits BEGIN. forbidden="+str(self.forbiddenItems)+",ap="+self.startAP)
        removableSuits = [suit for suit in self.suits if self.checkPool([suit])]
        if 'Varia' in removableSuits and self.startAP in ['Bubble Mountain', 'Firefleas Top']:
            # Varia has to be first item there, and checkPool can't detect it
            removableSuits.remove('Varia')
        self.log.debug("getForbiddenSuits removable="+str(removableSuits))
        if len(removableSuits) > 0:
            # remove at least one
            if self.addForbidden(removableSuits) == 0:
                self.forbiddenItems.append(removableSuits.pop())
                self.checkPool()
                self.addRestricted()
        else:
            self.superFun.remove('Suits')
            self.log.debug("Super Fun : Could not remove any suit")
        self.log.debug("getForbiddenSuits END. forbidden="+str(self.forbiddenItems))

    def getForbiddenMovement(self):
        self.log.debug("getForbiddenMovement BEGIN. forbidden="+str(self.forbiddenItems))
        removableMovement = [mvt for mvt in self.movementItems if self.checkPool([mvt])]
        if 'Bomb' in removableMovement and not RomPatches.has(self.sm.player, RomPatches.BombTorizoWake) and Objectives.objDict[self.sm.player].isGoalActive("activate chozo robots"):
            # in this objective, without VARIA tweaks, BT has to wake so give bombs
            removableMovement.remove('Bomb')
        self.log.debug("getForbiddenMovement removable="+str(removableMovement))
        if len(removableMovement) > 0:
            # remove at least the most important
            self.forbiddenItems.append(removableMovement.pop(0))
            self.addForbidden(removableMovement + [None])
        else:
            self.superFun.remove('Movement')
            self.log.debug('Super Fun : Could not remove any movement item')
        self.log.debug("getForbiddenMovement END. forbidden="+str(self.forbiddenItems))

    def getForbiddenCombat(self):
        self.log.debug("getForbiddenCombat BEGIN. forbidden="+str(self.forbiddenItems))
        removableCombat = [cbt for cbt in self.combatItems if self.checkPool([cbt])]
        self.log.debug("getForbiddenCombat removable="+str(removableCombat))
        if len(removableCombat) > 0:
            fake = [] # placeholders to avoid tricking the gaussian into removing too much stuff
            if len(removableCombat) > 0:
                # remove at least one if possible (will be screw or plasma)
                self.forbiddenItems.append(removableCombat.pop(0))
                fake.append(None)
            # if plasma is still available, remove it as well if we can
            if len(removableCombat) > 0 and removableCombat[0] == 'Plasma' and self.checkPool([removableCombat[0]]):
                self.forbiddenItems.append(removableCombat.pop(0))
                fake.append(None)
            self.addForbidden(removableCombat + fake)
        else:
            self.superFun.remove('Combat')
            self.log.debug('Super Fun : Could not remove any combat item')
        self.log.debug("getForbiddenCombat END. forbidden="+str(self.forbiddenItems))

    def getForbidden(self):
        self.forbiddenItems = []
        self.restrictedLocs = []
        self.errorMsgs = []
        if 'Suits' in self.superFun: # impact on movement item
            self.getForbiddenSuits()
        if 'Movement' in self.superFun:
            self.getForbiddenMovement()
        if 'Combat' in self.superFun:
            self.getForbiddenCombat()
        # if no super fun, check that there's no restricted locations (for ultra sparse)
        if len(self.superFun) == 0:
            self.addRestricted()
        self.log.debug("forbiddenItems: {}".format(self.forbiddenItems))
        self.log.debug("restrictedLocs: {}".format([loc.Name for loc in self.restrictedLocs]))
