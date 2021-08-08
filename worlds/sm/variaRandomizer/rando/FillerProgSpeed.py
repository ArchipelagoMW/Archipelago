
import copy, random, sys

from rando.Filler import Filler
from rando.FillerRandom import FillerRandom, FillerRandomItems
from rando.Choice import ItemThenLocChoiceProgSpeed, ItemThenLocChoice
from rando.RandoServices import ComebackCheckType
from rando.Items import ItemManager
from rando.ItemLocContainer import ItemLocContainer, getLocListStr, getItemListStr, getItemLocationsStr, getItemLocStr
from rando.RandoSettings import ProgSpeedParameters
from utils.parameters import infinity
from graph.graph_utils import GraphUtils, getAccessPoint

# algo state used for rollbacks
class FillerState(object):
    def __init__(self, filler):
        self.container = copy.copy(filler.container)
        self.ap = filler.ap
        self.states = filler.states[:]
        self.progressionItemLocs = filler.progressionItemLocs[:]
        self.progressionStatesIndices = filler.progressionStatesIndices[:]

    def apply(self, filler):
        filler.container = copy.copy(self.container)
        filler.ap = self.ap
        filler.states = self.states[:]
        filler.progressionItemLocs = self.progressionItemLocs[:]
        filler.progressionStatesIndices = self.progressionStatesIndices[:]
        filler.cache.reset()

    def __eq__(self, rhs):
        if rhs is None:
            return False
        eq = self.ap == rhs.ap
        eq &= self.progressionStatesIndices == rhs.progressionStatesIndices
        eq &= self.container == rhs.container
        return eq

# complex filler based on progression speed settings.  will alternate
# non progression phases and progression phases. can get stuck and
# rollback.  duration of each phases, item pool restrictions and
# choices are based on progression speed (see ProgSpeedParameters)
class FillerProgSpeed(Filler):
    def __init__(self, graphSettings, areaGraph, restrictions, container, endDate):
        super(FillerProgSpeed, self).__init__(graphSettings.startAP, areaGraph, restrictions, container, endDate)
        distanceProp = 'GraphArea' if graphSettings.areaRando else 'Area'
        self.stdStart = GraphUtils.isStandardStart(self.startAP)
        self.progSpeedParams = ProgSpeedParameters(self.restrictions, len(container.unusedLocations))
        self.choice = ItemThenLocChoiceProgSpeed(restrictions, self.progSpeedParams, distanceProp, self.services)

    def initFiller(self):
        super(FillerProgSpeed, self).initFiller()
        self.states = []
        self.progressionItemLocs = []
        self.progressionStatesIndices = []
        self.rollbackItemsTried = {}
        self.lastFallbackStates = []
        self.initState = FillerState(self)

    def determineParameters(self):
        speed = self.settings.progSpeed
        if speed == 'variable':
            speed = self.progSpeedParams.getVariableSpeed()
        self.currentProgSpeed = speed
        self.choice.determineParameters(speed)
        self.minorHelpProb = self.progSpeedParams.getMinorHelpProb(speed)
        self.itemLimit = self.progSpeedParams.getItemLimit(speed) if not self.isEarlyGame() else 0
        self.locLimit = self.progSpeedParams.getLocLimit(speed)
        self.possibleSoftlockProb = self.progSpeedParams.getPossibleSoftlockProb(speed)
        self.progressionItemTypes = self.progSpeedParams.getProgressionItemTypes(speed)
        if self.restrictions.isEarlyMorph() and 'Morph' in self.progressionItemTypes:
            self.progressionItemTypes.remove('Morph')
        collectedAmmo = self.container.getCollectedItems(lambda item: item.Category == 'Ammo')
        collectedAmmoTypes = set([item.Type for item in collectedAmmo])
        ammos = ['Missile', 'Super', 'PowerBomb']
        if 'Super' in collectedAmmoTypes:
            ammos.remove('Missile')
        self.progressionItemTypes += [ammoType for ammoType in ammos if ammoType not in collectedAmmoTypes]

    def chooseItemLoc(self, itemLocDict, possibleProg):
        return self.choice.chooseItemLoc(itemLocDict, possibleProg, self.progressionItemLocs, self.ap, self.container)

    # during random fill at the end put suits first while there's still available locations which don't fall under the suits restriction
    def chooseItemLocNoLogic(self, itemLocDict):
        if self.settings.restrictions['Suits'] == True and self.container.hasItemInPool(lambda item: item.Type in ['Varia', 'Gravity']):
            itemLocDict = {key: value for key, value in itemLocDict.items() if key.Type in ['Varia', 'Gravity']}
        # pure random choice instead of prog-speed specific
        return ItemThenLocChoice.chooseItemLoc(self.choice, itemLocDict, False)

    def currentLocations(self, item=None):
        return self.services.currentLocations(self.ap, self.container, item=item)

    def getComebackCheck(self):
        if self.isEarlyGame() or self.services.can100percent(self.ap, self.container):
            return ComebackCheckType.NoCheck
        if random.random() >= self.possibleSoftlockProb:
            return ComebackCheckType.ComebackWithoutItem
        return ComebackCheckType.JustComeback

    # from current accessible locations and an item pool, generate an item/loc dict.
    # return item/loc, or None if stuck
    def generateItem(self, comeback=ComebackCheckType.Undefined):
        comebackCheck = comeback if comeback != ComebackCheckType.Undefined else self.getComebackCheck()
        itemLocDict, possibleProg = self.services.getPossiblePlacements(self.ap, self.container, comebackCheck)
        if self.isEarlyGame() and possibleProg == True:
            # cheat a little bit if non-standard start: place early
            # progression away from crateria/blue brin if possible
            startAp = getAccessPoint(self.startAP)
            if startAp.GraphArea != "Crateria":
                newItemLocDict = {}
                for w, locs in itemLocDict.items():
                    filtered = [loc for loc in locs if loc.GraphArea != 'Crateria']
                    if len(filtered) > 0:
                        newItemLocDict[w] = filtered
                if len(newItemLocDict) > 0:
                    itemLocDict = newItemLocDict
        itemLoc = self.chooseItemLoc(itemLocDict, possibleProg)
        self.log.debug("generateItem. itemLoc="+"None" if itemLoc is None else getItemLocStr(itemLoc))
        return itemLoc

    def getCurrentState(self):
        return self.states[-1] if len(self.states) > 0 else self.initState

    def appendCurrentState(self):
        curState = FillerState(self)
        self.states.append(curState)
        curState.states.append(curState)

    # collect specialization that stores progression and state
    def collect(self, itemLoc):
        isProg = self.services.isProgression(itemLoc.Item, self.ap, self.container)
        super(FillerProgSpeed, self).collect(itemLoc)
        if isProg:
            n = len(self.states)
            self.log.debug("prog indice="+str(n))
            self.progressionStatesIndices.append(n)
            self.progressionItemLocs.append(itemLoc)
        self.appendCurrentState()
        self.cache.reset()

    def isProgItem(self, item):
        if item.Type in self.progressionItemTypes:
            return True
        return self.services.isProgression(item, self.ap, self.container)

    def isEarlyGame(self):
        return len(self.progressionStatesIndices) <= 2 if self.stdStart else len(self.progressionStatesIndices) <= 3

    # check if remaining locations pool is conform to rando settings when filling up
    # with non-progression items
    def checkLocPool(self):
        sm = self.container.sm
 #       self.log.debug("checkLocPool {}".format([it.Name for it in self.itemPool]))
        if self.locLimit <= 0:
            return True
        progItems = self.container.getItems(self.isProgItem)
        self.log.debug("checkLocPool. progItems {}".format([it.Name for it in progItems]))
 #       self.log.debug("curItems {}".format([it.Name for it in self.currentItems]))
        if len(progItems) == 0:
            return True
        isMinorProg = any(self.restrictions.isItemMinor(item) for item in progItems)
        isMajorProg = any(self.restrictions.isItemMajor(item) for item in progItems)
        accessibleLocations = []
#        self.log.debug("unusedLocs: {}".format([loc.Name for loc in self.unusedLocations]))
        locs = self.currentLocations()
        for loc in locs:
            majAvail = self.restrictions.isLocMajor(loc)
            minAvail = self.restrictions.isLocMinor(loc)
            if ((isMajorProg and majAvail) or (isMinorProg and minAvail)) \
               and self.services.locPostAvailable(sm, loc, None):
                accessibleLocations.append(loc)
        self.log.debug("accesLoc {}".format([loc.Name for loc in accessibleLocations]))
        if len(accessibleLocations) <= self.locLimit:
            sys.stdout.write('|')
            sys.stdout.flush()
            return False
        # check that there is room left in all main areas
        room = {'Brinstar' : 0, 'Norfair' : 0, 'WreckedShip' : 0, 'LowerNorfair' : 0, 'Maridia' : 0 }
        if not self.stdStart:
            room['Crateria'] = 0
        for loc in self.container.unusedLocations:
            majAvail = self.restrictions.isLocMajor(loc)
            minAvail = self.restrictions.isLocMinor(loc)
            if loc.Area in room and ((isMajorProg and majAvail) or (isMinorProg and minAvail)):
                room[loc.Area] += 1
        for r in room.values():
            if r > 0 and r <= self.locLimit:
                sys.stdout.write('|')
                sys.stdout.flush()
                return False
        return True

    def addEnergyAsNonProg(self):
        collectedEnergy = self.container.getCollectedItems(lambda item: item.Category == 'Energy')
        return self.restrictions.split == 'Chozo' or (len(collectedEnergy) <= 2 and self.settings.progSpeed != 'slowest')

    def nonProgItemCheck(self, item):
        return (item.Category == 'Energy' and self.addEnergyAsNonProg()) or (not self.stdStart and item.Category == 'Ammo') or (self.restrictions.isEarlyMorph() and item.Type == 'Morph') or not self.isProgItem(item)

    def getNonProgItemPoolRestriction(self):
        return self.nonProgItemCheck

    def pickHelpfulMinor(self, item):
        self.helpfulMinorPicked = not self.container.sm.haveItem(item.Type).bool
        if self.helpfulMinorPicked:
            self.log.debug('pickHelpfulMinor. pick '+item.Type)
        return self.helpfulMinorPicked

    def getNonProgItemPoolRestrictionStart(self):
        self.helpfulMinorPicked = random.random() >= self.minorHelpProb
        self.log.debug('getNonProgItemPoolRestrictionStart. helpfulMinorPicked='+str(self.helpfulMinorPicked))
        return lambda item: (item.Category == 'Ammo' and not self.helpfulMinorPicked and self.pickHelpfulMinor(item)) or self.nonProgItemCheck(item)

    # return True if stuck, False if not
    def fillNonProgressionItems(self):
        if self.itemLimit <= 0:
            return False
        poolRestriction = self.getNonProgItemPoolRestrictionStart()
        self.container.restrictItemPool(poolRestriction)
        if self.container.isPoolEmpty():
            self.container.unrestrictItemPool()
            return False
        itemLocation = None
        nItems = 0
        locPoolOk = True
        self.log.debug("NON-PROG")
        while not self.container.isPoolEmpty() and nItems < self.itemLimit and locPoolOk:
            itemLocation = self.generateItem()
            if itemLocation is not None:
                nItems += 1
                self.log.debug("fillNonProgressionItems: {} at {}".format(itemLocation.Item.Name, itemLocation.Location.Name))
                # doing this first is actually important, as state is saved in collect
                self.container.unrestrictItemPool()
                self.collect(itemLocation)
                locPoolOk = self.checkLocPool()
                poolRestriction = self.getNonProgItemPoolRestriction()
                self.container.restrictItemPool(poolRestriction)
            else:
                break
        self.container.unrestrictItemPool()
        return itemLocation is None

    def generateItemFromStandardPool(self):
        self.log.debug('generateItemFromStandardPool')
        itemLoc = self.generateItem()
        if itemLoc is not None and self.currentProgSpeed in ['medium', 'slow', 'slowest'] and\
           not self.isEarlyGame() and not self.services.can100percent(self.ap, self.container):
            itemLocWithout = self.generateItem(ComebackCheckType.ComebackWithoutItem)
            if itemLocWithout is None:
                # the *only* available locations are locs we couldn't come back from without the item,
                # consider ourselves stuck (mitigates 'supers at spospo' syndrome)
                return None
        return itemLoc

    def getItemFromStandardPool(self):
        itemLoc = self.generateItemFromStandardPool()
        isStuck = itemLoc is None
        if not isStuck:
            sys.stdout.write('-')
            sys.stdout.flush()
            self.collect(itemLoc)
        return isStuck

    def initRollbackPoints(self):
        minRollbackPoint = 0
        maxRollbackPoint = len(self.states)
        if len(self.progressionStatesIndices) > 0:
            minRollbackPoint = self.progressionStatesIndices[-1]
        self.log.debug('initRollbackPoints: min=' + str(minRollbackPoint) + ", max=" + str(maxRollbackPoint))
        return minRollbackPoint, maxRollbackPoint

    def initRollback(self):
        self.log.debug('initRollback: progressionStatesIndices 1=' + str(self.progressionStatesIndices))
        if len(self.progressionStatesIndices) > 0 and self.progressionStatesIndices[-1] == len(self.states) - 1:
            # the state we are about to remove was a progression state
            self.progressionStatesIndices.pop()
        if len(self.states) > 0:
            self.states.pop() # remove current state, it's the one we're stuck in
        self.log.debug('initRollback: progressionStatesIndices 2=' + str(self.progressionStatesIndices))

    def getSituationId(self):
        progItems = str(sorted([il.Item.Type for il in self.progressionItemLocs]))
        position = str(sorted([ap.Name for ap in self.services.currentAccessPoints(self.ap, self.container)]))
        return progItems+'/'+position

    def hasTried(self, itemLoc):
        if self.isEarlyGame():
            return False
        itemType = itemLoc.Item.Type
        situation = self.getSituationId()
        ret = False
        if situation in self.rollbackItemsTried:
            ret = itemType in self.rollbackItemsTried[situation]
            if ret:
                self.log.debug('has tried ' + itemType + ' in situation ' + situation)
        return ret

    def updateRollbackItemsTried(self, itemLoc):
        itemType = itemLoc.Item.Type
        situation = self.getSituationId()
        if situation not in self.rollbackItemsTried:
            self.rollbackItemsTried[situation] = []
        self.log.debug('adding ' + itemType + ' to situation ' + situation)
        self.rollbackItemsTried[situation].append(itemType)

    def getFallbackState(self):
        self.log.debug("getFallbackState")
        curState = self.getCurrentState()
        fallbackState = self.states[-2] if len(self.states) > 1 else self.initState
        if (len(self.lastFallbackStates) > 0 and curState == self.lastFallbackStates[-1]):
            self.log.debug("getFallbackState. rewind fallback")
            return fallbackState
        # n = sum(1 for state in self.lastFallbackStates if state == fallbackState)
        # if n >= 3:
        #     self.log.debug("getFallbackState. kickstart needed")
        #     self.lastFallbackStates = None
        #     return None
        return curState

    # goes back in the previous states to find one where
    # we can put a progression item
    def rollback(self):
        nItemsAtStart = len(self.container.currentItems)
        nStatesAtStart = len(self.states)
        self.log.debug("rollback BEGIN: nItems={}, nStates={}".format(nItemsAtStart, nStatesAtStart))
        ret = None
        self.initRollback()
        if len(self.states) == 0:
            self.initState.apply(self)
            self.log.debug("rollback END initState apply, nCurLocs="+str(len(self.currentLocations())))
            if self.vcr != None:
                self.vcr.addRollback(nStatesAtStart)
            sys.stdout.write('<'*nStatesAtStart)
            sys.stdout.flush()
            return None
        # to stay consistent in case no solution is found as states list was popped in init
        fallbackState = self.getFallbackState()
        # if fallbackState is None: # kickstart needed
        #     return None
        self.lastFallbackStates.append(fallbackState)
        i = 0
        possibleStates = []
        self.log.debug('rollback. nStates='+str(len(self.states)))
        while i >= 0 and len(possibleStates) == 0:
            states = self.states[:] + [fallbackState]
            minRollbackPoint, maxRollbackPoint = self.initRollbackPoints()
            i = maxRollbackPoint
            while i >= minRollbackPoint:
                state = states[i]
                state.apply(self)
                self.log.debug('rollback. state applied. Container=\n'+self.container.dump())
                itemLoc = self.generateItemFromStandardPool()
                if itemLoc is not None and not self.hasTried(itemLoc) and self.services.isProgression(itemLoc.Item, self.ap, self.container):
                    possibleStates.append((state, itemLoc))
                i -= 1
            # nothing, let's rollback further a progression item
            if len(possibleStates) == 0 and i >= 0:
                if len(self.progressionStatesIndices) > 0:
                    sys.stdout.write('!')
                    sys.stdout.flush()
                    self.progressionStatesIndices.pop()
                else:
                    break
        if len(possibleStates) > 0:
            (state, itemLoc) = random.choice(possibleStates)
            self.updateRollbackItemsTried(itemLoc)
            state.apply(self)
            ret = itemLoc
            if self.vcr != None:
                nRoll = nItemsAtStart - len(self.container.currentItems)
                if nRoll > 0:
                    self.vcr.addRollback(nRoll)
        else:
            self.log.debug('fallbackState apply')
            fallbackState.apply(self)
            if self.vcr != None:
                self.vcr.addRollback(1)
        sys.stdout.write('<'*(nStatesAtStart - len(self.states)))
        sys.stdout.flush()
        self.log.debug("rollback END: {}".format(len(self.container.currentItems)))
        return ret

    # def kickStart(self):
    #     self.initState.apply(self)
    #     self.lastFallbackStates = []
    #     pairItemLocDict = self.services.getStartupProgItemsPairs(self.ap, self.container)
    #     if pairItemLocDict == None:
    #         # no pair found
    #         self.log.debug("kickStart KO")
    #         return False
    #     self.collectPair(pairItemLocDict)
    #     self.log.debug("kickStart OK")
    #     return True

    def step(self, onlyBossCheck=False):
        self.cache.reset()
        if self.services.can100percent(self.ap, self.container) and self.settings.progSpeed not in ['slowest', 'slow']:
            (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
            itemLoc = self.chooseItemLocNoLogic(itemLocDict)
            if itemLoc is None:
                self.restrictions.disable()
                self.cache.reset()
                self.errorMsg = "Restrictions disabled"
                (itemLocDict, isProg) = self.services.getPossiblePlacementsNoLogic(self.container)
                itemLoc = self.chooseItemLocNoLogic(itemLocDict)
            assert itemLoc is not None
            self.ap = self.services.collect(self.ap, self.container, itemLoc)
            return True
        self.determineParameters()
        # fill up with non-progression stuff
        isStuck = self.fillNonProgressionItems()
        if not self.container.isPoolEmpty():
            isStuck = self.getItemFromStandardPool()
            if isStuck:
                if onlyBossCheck == False and self.services.onlyBossesLeft(self.ap, self.container):
                    self.settings.maxDiff = infinity
                    return self.step(onlyBossCheck=True)
                if onlyBossCheck == True:
                    # we're stuck even after bumping diff.
                    # it was a onlyBossesLeft false positive, restore max diff
                    self.settings.maxDiff = self.maxDiff
                # check that we're actually stuck
                itemLoc = None
                if not self.services.can100percent(self.ap, self.container):
                    # stuck, rollback to make progress if we can't access everything yet
                    itemLoc = self.rollback()
                    # if itemLoc is None and self.lastFallbackStates is None:
                    #     # kickstart needed
                    #     return self.kickStart()
                if itemLoc is not None:
                    self.collect(itemLoc)
                    isStuck = False
                else:
                    isStuck = self.getItemFromStandardPool()
#        self.log.debug("step end. itemLocations="+getItemLocationsStr(self.container.itemLocations))
        return not isStuck

    def getProgressionItemLocations(self):
        return self.progressionItemLocs


class FillerRandomNoCopy(FillerRandom):
    def __init__(self, startAP, graph, restrictions, container, endDate, diffSteps=0):
        super(FillerRandomNoCopy, self).__init__(startAP, graph, restrictions, container, endDate, diffSteps)

    def initContainer(self):
        self.container = self.baseContainer

# progression speed based filler to use for 2nd phase Chozo split. has
# more and more chance to preserve "intended" Chozo progression as
# speed slows.
class FillerProgSpeedChozoSecondPhase(Filler):
    def __init__(self, startAP, graph, restrictions, container, endDate):
        super(FillerProgSpeedChozoSecondPhase, self).__init__(startAP, graph, restrictions, container, endDate)
        self.firstPhaseItemLocs = container.itemLocations
        self.progSpeedParams = ProgSpeedParameters(self.restrictions, len(container.unusedLocations))

    def initContainer(self):
        self.container = self.baseContainer

    def initFiller(self):
        super(FillerProgSpeedChozoSecondPhase, self).initFiller()
        self.conditions = [
            ('Missile', lambda sm: sm.canOpenRedDoors()),
            ('Super', lambda sm: sm.canOpenGreenDoors()),
            ('PowerBomb', lambda sm: sm.canOpenYellowDoors())
        ]
        self.container.resetCollected()
        self.firstPhaseContainer = ItemLocContainer(self.container.sm,
                                                    [il.Item for il in self.firstPhaseItemLocs],
                                                    [il.Location for il in self.firstPhaseItemLocs])
        self.firstPhaseIndex = 0

    def nextMetCondition(self):
        for cond in self.conditions:
            diff = cond[1](self.container.sm)
            if diff.bool == True and diff.difficulty <= self.settings.maxDiff:
                return cond
        return None

    def currentLocations(self):
        curLocs = self.services.currentLocations(self.ap, self.container)
        return self.services.getPlacementLocs(self.ap, self.container, ComebackCheckType.JustComeback, None, curLocs)

    def determineParameters(self):
        speed = self.settings.progSpeed
        if speed == 'variable':
            speed = self.progSpeedParams.getVariableSpeed()
        self.restrictedItemProba = self.progSpeedParams.getChozoSecondPhaseRestrictionProb(speed)

    def step(self):
        if len(self.conditions) > 1:
            self.determineParameters()
            curLocs = []
            while self.firstPhaseIndex < len(self.firstPhaseItemLocs):
                self.cache.reset()
                newCurLocs = [loc for loc in self.currentLocations() if loc not in curLocs]
                curLocs += newCurLocs
                cond = self.nextMetCondition()
                if cond is not None:
                    self.log.debug('step. cond item='+cond[0])
                    self.conditions.remove(cond)
                    break
                itemLoc = self.firstPhaseItemLocs[self.firstPhaseIndex]
                self.collect(itemLoc, container=self.firstPhaseContainer)
                self.firstPhaseIndex += 1
            self.log.debug('step. curLocs='+getLocListStr(curLocs))
            restrictedItemTypes = [cond[0] for cond in self.conditions]
            self.log.debug('step. restrictedItemTypes='+str(restrictedItemTypes))
            basePool = self.container.itemPool[:]
            itemPool = []
            self.log.debug('step. basePool: {}'.format(getItemListStr(basePool)))
            while len(itemPool) < len(curLocs):
                item = random.choice(basePool)
                if item.Type not in restrictedItemTypes or\
                   random.random() < self.restrictedItemProba or\
                   self.restrictedItemProba == 0 and not any(item for item in basePool if item.Type not in restrictedItemTypes):
                    itemPool.append(item)
                    basePool.remove(item)
            self.log.debug('step. itemPool='+getItemListStr(itemPool))
            cont = ItemLocContainer(self.container.sm, itemPool, curLocs)
            self.container.transferCollected(cont)
            filler = FillerRandomItems(self.ap, self.graph, self.restrictions, cont, self.endDate)
            (stuck, itemLocs, prog) = filler.generateItems()
            if stuck:
                if len(filler.errorMsg) > 0:
                    self.errorMsg += '\n'+filler.errorMsg
                return False
            for itemLoc in itemLocs:
                if itemLoc.Location in self.container.unusedLocations:
                    self.log.debug("step. POST COLLECT "+itemLoc.Item.Type+" at "+itemLoc.Location.Name)
                    self.container.collect(itemLoc)
        else:
            # merge collected of 1st phase and 2nd phase so far for seed to be solvable by random fill
            self.container.itemLocations += self.firstPhaseItemLocs
            self.log.debug("step. LAST FILL. cont: "+self.container.dump())
            filler = FillerRandomNoCopy(self.startAP, self.graph, self.restrictions, self.container, self.endDate, diffSteps=100)
            (stuck, itemLocs, prog) = filler.generateItems()
            if len(filler.errorMsg) > 0:
                self.errorMsg += '\n'+filler.errorMsg
            if stuck:
                return False
        return True
