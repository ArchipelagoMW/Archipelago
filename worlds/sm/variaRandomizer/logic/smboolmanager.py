# object to handle the smbools and optimize them

from ..logic.cache import Cache
from ..logic.smbool import SMBool, smboolFalse
from ..logic.helpers import Bosses
from ..logic.logic import Logic
from ..utils.doorsmanager import DoorsManager
from ..utils.objectives import Objectives
from ..utils.parameters import Knows, isKnows
import logging
import sys

class SMBoolManager(object):
    items = ['ETank', 'Missile', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Reserve', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack', 'Nothing', 'NoEnergy', 'MotherBrain', 'Hyper', 'Gunship'] + Bosses.Golden4() + Bosses.miniBosses()
    countItems = ['Missile', 'Super', 'PowerBomb', 'ETank', 'Reserve']

    percentItems = ['Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']
    def __init__(self, player=0, maxDiff=sys.maxsize, onlyBossLeft = False):
        self._items = { }
        self._counts = { }

        self.player = player
        self.maxDiff = maxDiff
        self.onlyBossLeft = onlyBossLeft

        # cache related
        #self.cacheKey = 0
        #self.computeItemsPositions()
        Cache.reset()
        Logic.factory('vanilla')
        self.helpers = Logic.HelpersGraph(self)
        self.doorsManager = DoorsManager()
        self.objectives = Objectives.objDict[player] if player in Objectives.objDict.keys() else Objectives(player)
        self.createFacadeFunctions()
        self.createKnowsFunctions(player)
        self.resetItems()

    def computeItemsPositions(self):
        # compute index in cache key for each items
        self.itemsPositions = {}
        maxBitsForCountItem = 7 # 128 values with 7 bits
        for (i, item) in enumerate(self.countItems):
            pos = i*maxBitsForCountItem
            bitMask = (2<<(maxBitsForCountItem-1))-1
            bitMask = bitMask << pos
            self.itemsPositions[item] = (pos, bitMask)
        for (i, item) in enumerate(self.items, (i+1)*maxBitsForCountItem+1):
            if item in self.countItems:
                continue
            self.itemsPositions[item] = (i, 1<<i)

    def computeNewCacheKey(self, item, value):
        # generate an unique integer for each items combinations which is use as key in the cache.
        if item in ['Nothing', 'NoEnergy']:
            return
        (pos, bitMask) = self.itemsPositions[item]
#        print("--------------------- {} {} ----------------------------".format(item, value))
#        print("old:  "+format(self.cacheKey, '#067b'))
        self.cacheKey = (self.cacheKey & (~bitMask)) | (value<<pos)
#        print("new:  "+format(self.cacheKey, '#067b'))
#        self.printItemsInKey(self.cacheKey)

    def printItemsInKey(self, key):
        # for debug purpose
        print("key:  "+format(key, '#067b'))
        msg = ""
        for (item, (pos, bitMask)) in self.itemsPositions.items():
            value = (key & bitMask) >> pos
            if value != 0:
                msg += " {}: {}".format(item, value)
        print("items:{}".format(msg))

    def isEmpty(self):
        for item in self.items:
            if self.haveItem(item):
                return False
        for item in self.countItems:
            if self.itemCount(item) > 0:
                return False
        return True

    def getItems(self):
        # get a dict of collected items and how many (to be displayed on the solver spoiler)
        itemsDict = {}
        for item in self.items:
            itemsDict[item] = 1 if self._items[item] == True else 0
        for item in self.countItems:
            itemsDict[item] = self._counts[item]
        return itemsDict

    def withItem(self, item, func):
        addAndRemoveItem = self.isCountItem(item) or not self.haveItem(item)
        if addAndRemoveItem:
            self.addItem(item)
        ret = func(self)
        if addAndRemoveItem:
            self.removeItem(item)
        return ret

    def resetItems(self):
        self._items = { item : smboolFalse for item in self.items }
        self._counts = { item : 0 for item in self.countItems }

        #self.cacheKey = 0
        #Cache.update(self.cacheKey)

    def addItem(self, item):
        # a new item is available
        self._items[item] = SMBool(True, items=[item])
        if self.isCountItem(item):
            count = self._counts[item] + 1
            self._counts[item] = count
            #self.computeNewCacheKey(item, count)
        #else:
            #self.computeNewCacheKey(item, 1)

        #Cache.update(self.cacheKey)

    def addItems(self, items):
        if len(items) == 0:
            return
        for item in items:
            self._items[item] = SMBool(True, items=[item])
            if self.isCountItem(item):
                count = self._counts[item] + 1
                self._counts[item] = count
                #self.computeNewCacheKey(item, count)
            #else:
                #self.computeNewCacheKey(item, 1)

        #Cache.update(self.cacheKey)

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if self.isCountItem(item):
            count = self._counts[item] - 1
            self._counts[item] = count
            if count == 0:
                self._items[item] = smboolFalse
            #self.computeNewCacheKey(item, count)
        else:
            self._items[item] = smboolFalse
            #self.computeNewCacheKey(item, 0)

        #Cache.update(self.cacheKey)

    def createFacadeFunctions(self):
        for fun in dir(self.helpers):
            if fun != 'smbm' and fun[0:2] != '__':
                setattr(self, fun, getattr(self.helpers, fun))

    def traverse(self, doorName):
        return self.doorsManager.traverse(self, doorName)
    
    def canPassG4(self):
        return self.objectives.canClearGoals(self, 'Golden Four')

    def hasItemsPercent(self, percent, totalItemsCount=None):
        if totalItemsCount is None:
            totalItemsCount = self.objectives.getTotalItemsCount()
        currentItemsCount = self.getCollectedItemsCount()
        return SMBool(100*(currentItemsCount/totalItemsCount) >= percent)

    def getCollectedItemsCount(self):
        return (len([item for item in self._items if self.haveItem(item) and item in self.percentItems])
                + sum([self.itemCount(item) for item in self._items if self.isCountItem(item)]))

    def createKnowsFunctions(self, player):
        # for each knows we have a function knowsKnows (ex: knowsAlcatrazEscape()) which
        # take no parameter
        for knows in Knows.__dict__:
            if isKnows(knows):
                self._createKnowsFunction(knows, player)

    def _setKnowsFunction(self, knows, k):
        setattr(self, 'knows'+knows, lambda: SMBool(k.bool, k.difficulty,
                                                    knows=[knows]))

    def _createKnowsFunction(self, knows, player):
        if player in Knows.knowsDict and knows in Knows.knowsDict[player].__dict__:
            self._setKnowsFunction(knows, Knows.knowsDict[player].__dict__[knows])
        else:
            self._setKnowsFunction(knows, Knows.__dict__[knows])

    def changeKnows(self, knows, newVal):
        if isKnows(knows):
            self._setKnowsFunction(knows, newVal)
            #Cache.reset()
        else:
            raise ValueError("Invalid knows "+str(knows))

    def restoreKnows(self, knows):
        if isKnows(knows):
            self._createKnowsFunction(knows)
            #Cache.reset()
        else:
            raise ValueError("Invalid knows "+str(knows))
        
    def isCountItem(self, item):
        return item in self.countItems

    def itemCount(self, item):
        # return integer
        #self.state.item_count(item, self.player)
        return self._counts[item]

    def haveItem(self, item):
        #return self.state.has(item, self.player)
        return self._items[item]
    
    def haveItems(self, items):
        for item in items:
            if not self.haveItem(item):
                return smboolFalse
        return SMBool(True)

    wand = staticmethod(SMBool.wand)
    wandmax = staticmethod(SMBool.wandmax)
    wor = staticmethod(SMBool.wor)
    wnot = staticmethod(SMBool.wnot)

    def itemCountOk(self, item, count, difficulty=0):
        if self.itemCount(item) >= count:
            if item in ['ETank', 'Reserve']:
                item = str(count)+'-'+item
            return SMBool(True, difficulty, items = [item])
        else:
            return smboolFalse

    def energyReserveCountOk(self, count, difficulty=0):
        if self.energyReserveCount() >= count:
            nEtank = self.itemCount('ETank')
            if nEtank > count:
                nEtank = int(count)
            items = str(nEtank)+'-ETank'
            nReserve = self.itemCount('Reserve')
            if nEtank < count:
                nReserve = int(count) - nEtank
                items += ' - '+str(nReserve)+'-Reserve'
            return SMBool(True, difficulty, items = [items])
        else:
            return smboolFalse

class SMBoolManagerPlando(SMBoolManager):
    def __init__(self):
        super(SMBoolManagerPlando, self).__init__()

    def addItem(self, item):
        # a new item is available
        already = self.haveItem(item)
        isCount = self.isCountItem(item)
        if isCount or not already:
            self._items[item] = SMBool(True, items=[item])
        else:
            # handle duplicate major items (plandos)
            self._items['dup_'+item] = True
        if isCount:
            count = self._counts[item] + 1
            self._counts[item] = count
            #self.computeNewCacheKey(item, count)
        #else:
            #self.computeNewCacheKey(item, 1)

        #Cache.update(self.cacheKey)

    def removeItem(self, item):
        # randomizer removed an item (or the item was added to test a post available)
        if self.isCountItem(item):
            count = self._counts[item] - 1
            self._counts[item] = count
            if count == 0:
                self._items[item] = smboolFalse
            #self.computeNewCacheKey(item, count)
        else:
            dup = 'dup_'+item
            if self._items.get(dup, None) is None:
                self._items[item] = smboolFalse
                #self.computeNewCacheKey(item, 0)
            else:
                del self._items[dup]
                #self.computeNewCacheKey(item, 1)

        #Cache.update(self.cacheKey)
