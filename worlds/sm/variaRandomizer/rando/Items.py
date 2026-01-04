from ..utils.utils import randGaussBounds, getRangeDict, chooseFromRange
from ..utils import log
import logging, copy

class Item:
    __slots__ = ( 'Category', 'Class', 'Name', 'Code', 'Type', 'BeamBits', 'ItemBits', 'Id' )

    def __init__(self, Category, Class, Name, Type, Code=None, BeamBits=0, ItemBits=0, Id=None):
        self.Category = Category
        self.Class = Class
        self.Code = Code
        self.Name = Name
        self.Type = Type
        self.BeamBits = BeamBits
        self.ItemBits = ItemBits
        self.Id = Id

    def withClass(self, Class):
        return Item(self.Category, Class, self.Name, self.Type, self.Code, self.BeamBits, self.ItemBits)

    def __eq__(self, other):
        # used to remove an item from a list
        return self.Type == other.Type and self.Class == other.Class

    def __hash__(self):
        # as we define __eq__ we have to also define __hash__ to use items as dictionnary keys
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        return id(self)

    def __repr__(self):
      return "Item({}, {}, {}, {}, {})".format(self.Category,
          self.Class, self.Code, self.Name, self.Type)

    def json(self):
        # as we have slots instead of dict
        return {key : getattr(self, key, None) for key in self.__slots__}

class ItemManager:
    Items = {
        'ETank': Item(
            Category='Energy',
            Class='Major',
            Code=0xfc20,
            Name="Energy Tank",
            Type='ETank',
            Id=0
        ),
        'Missile': Item(
            Category='Ammo',
            Class='Minor',
            Code=0xfc20,
            Name="Missile",
            Type='Missile',
            Id=1
        ),
        'Super': Item(
            Category='Ammo',
            Class='Minor',
            Code=0xfc20,
            Name="Super Missile",
            Type='Super',
            Id=2
        ),
        'PowerBomb': Item(
            Category='Ammo',
            Class='Minor',
            Code=0xfc20,
            Name="Power Bomb",
            Type='PowerBomb',
            Id=3
        ),
        'Bomb': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Bomb",
            Type='Bomb',
            ItemBits=0x1000,
            Id=4
        ),
        'Charge': Item(
            Category='Beam',
            Class='Major',
            Code=0xfc20,
            Name="Charge Beam",
            Type='Charge',
            BeamBits=0x1000,
            Id=5
        ),
        'Ice': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Ice Beam",
            Type='Ice',
            BeamBits=0x2,
            Id=6
        ),
        'HiJump': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Hi-Jump Boots",
            Type='HiJump',
            ItemBits=0x100,
            Id=7
        ),
        'SpeedBooster': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Speed Booster",
            Type='SpeedBooster',
            ItemBits=0x2000,
            Id=8
        ),
        'Wave': Item(
            Category='Beam',
            Class='Major',
            Code=0xfc20,
            Name="Wave Beam",
            Type='Wave',
            BeamBits=0x1,
            Id=9
        ),
        'Spazer': Item(
            Category='Beam',
            Class='Major',
            Code=0xfc20,
            Name="Spazer",
            Type='Spazer',
            BeamBits=0x4,
            Id=10
        ),
        'SpringBall': Item(
            Category='Misc',
            Class='Major',
            Code=0xfc20,
            Name="Spring Ball",
            Type='SpringBall',
            ItemBits=0x2,
            Id=11
        ),
        'Varia': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Varia Suit",
            Type='Varia',
            ItemBits=0x1,
            Id=12
        ),
        'Plasma': Item(
            Category='Beam',
            Class='Major',
            Code=0xfc20,
            Name="Plasma Beam",
            Type='Plasma',
            BeamBits=0x8,
            Id=15
        ),
        'Grapple': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Grappling Beam",
            Type='Grapple',
            ItemBits=0x4000,
            Id=16
        ),
        'Morph': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Morph Ball",
            Type='Morph',
            ItemBits=0x4,
            Id=19
        ),
        'Reserve': Item(
            Category='Energy',
            Class='Major',
            Code=0xfc20,
            Name="Reserve Tank",
            Type='Reserve',
            Id=20
        ),
        'Gravity': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Gravity Suit",
            Type='Gravity',
            ItemBits=0x20,
            Id=13
        ),
        'XRayScope': Item(
            Category='Misc',
            Class='Major',
            Code=0xfc20,
            Name="X-Ray Scope",
            Type='XRayScope',
            ItemBits=0x8000,
            Id=14
        ),
        'SpaceJump': Item(
            Category='Progression',
            Class='Major',
            Code=0xfc20,
            Name="Space Jump",
            Type='SpaceJump',
            ItemBits=0x200,
            Id=17
        ),
        'ScrewAttack': Item(
            Category='Misc',
            Class='Major',
            Code=0xfc20,
            Name="Screw Attack",
            Type='ScrewAttack',
            ItemBits= 0x8,
            Id=18
        ),
        'Nothing': Item(
            Category='Nothing',
            Class='Minor',
            Code=0xbae9, # new nothing plm
            Name="Nothing",
            Type='Nothing',
            Id=22
        ),
        'NoEnergy': Item(
            Category='Nothing',
            Class='Major',
            Code=0xbae9, # see above
            Name="No Energy",
            Type='NoEnergy',
            Id=23
        ),
        'Kraid': Item(
            Category='Boss',
            Class='Boss',
            Name="Kraid",
            Type='Kraid',
        ),
        'Phantoon': Item(
            Category='Boss',
            Class='Boss',
            Name="Phantoon",
            Type='Phantoon',
        ),
        'Draygon': Item(
            Category='Boss',
            Class='Boss',
            Name="Draygon",
            Type='Draygon',
        ),
        'Ridley': Item(
            Category='Boss',
            Class='Boss',
            Name="Ridley",
            Type='Ridley',
        ),
        'MotherBrain': Item(
            Category='Boss',
            Class='Boss',
            Name="Mother Brain",
            Type='MotherBrain',
        ),
        'SporeSpawn': Item(
            Category='MiniBoss',
            Class='Boss',
            Name="Spore Spawn",
            Type='SporeSpawn',
        ),
        'Crocomire': Item(
            Category='MiniBoss',
            Class='Boss',
            Name="Crocomire",
            Type='Crocomire',
        ),
        'Botwoon': Item(
            Category='MiniBoss',
            Class='Boss',
            Name="Botwoon",
            Type='Botwoon',
        ),
        'GoldenTorizo': Item(
            Category='MiniBoss',
            Class='Boss',
            Name="Golden Torizo",
            Type='GoldenTorizo',
        ),
        # used only during escape path check
        'Hyper': Item(
            Category='Beam',
            Class='Major',
            Code=0xffff,
            Name="Hyper Beam",
            Type='Hyper',
        ),
        'ArchipelagoItem': Item(
            Category='ArchipelagoItem',
            Class='Major',
            Code=0xfc20,
            Name="Generic",
            Type='ArchipelagoItem',
            Id=21
        )
    }

    for itemType, item in Items.items():
      if item.Type != itemType:
        raise RuntimeError("Wrong item type for {} (expected {})".format(item, itemType))

    @staticmethod
    def isBeam(item):
        return item.BeamBits != 0

    @staticmethod
    def getItemTypeCode(item, itemVisibility):
        if item.Category == 'Nothing':
            if itemVisibility in ['Visible', 'Chozo']:
                modifier = 0
            elif itemVisibility == 'Hidden':
                modifier = 4
        else:
            if itemVisibility == 'Visible':
                modifier = 0
            elif itemVisibility == 'Chozo':
                modifier = 4
            elif itemVisibility == 'Hidden':
                modifier = 8

        itemCode = item.Code + modifier
        return itemCode

    def __init__(self, majorsSplit, qty, sm, nLocs, bossesItems, maxDiff, random):
        self.qty = qty
        self.sm = sm
        self.majorsSplit = majorsSplit
        self.nLocs = nLocs
        self.bossesItems = bossesItems
        self.maxDiff = maxDiff
        self.majorClass = 'Chozo' if majorsSplit == 'Chozo' else 'Major'
        self.itemPool = []
        self.random = random

    def newItemPool(self, addBosses=True):
        self.itemPool = []
        if addBosses == True:
            # for the bosses
            for boss in self.bossesItems:
                self.addMinor(boss)

    def getItemPool(self):
        return self.itemPool

    def setItemPool(self, pool):
        self.itemPool = pool

    def addItem(self, itemType, itemClass=None):
        self.itemPool.append(ItemManager.getItem(itemType, itemClass))

    def addMinor(self, minorType):
        self.addItem(minorType, 'Minor')

    # remove from pool an item of given type. item type has to be in original Items list.
    def removeItem(self, itemType):
        for idx, item in enumerate(self.itemPool):
            if item.Type == itemType:
                self.itemPool = self.itemPool[0:idx] + self.itemPool[idx+1:]
                return item

    def removeForbiddenItems(self, forbiddenItems):
        # the pool is the one managed by the Randomizer
        for itemType in forbiddenItems:
            self.removeItem(itemType)
            self.addItem('NoEnergy', self.majorClass)
        return self.itemPool

    @staticmethod
    def getItem(itemType, itemClass=None):
        if itemClass is None:
            return copy.copy(ItemManager.Items[itemType])
        else:
            return ItemManager.Items[itemType].withClass(itemClass)

    def createItemPool(self, exclude=None):
        itemPoolGenerator = ItemPoolGenerator.factory(self.majorsSplit, self, self.qty, self.sm, exclude, self.nLocs, self.maxDiff, self.random)
        self.itemPool = itemPoolGenerator.getItemPool()

    @staticmethod
    def getProgTypes():
        return [item for item in ItemManager.Items if ItemManager.Items[item].Category == 'Progression']

    def hasItemInPoolCount(self, itemName, count):
        return len([item for item in self.itemPool if item.Type == itemName]) >= count

class ItemPoolGenerator(object):
    # 100 item locs, 5 bosses, 4 mini bosses
    maxLocs = 109
    nbBosses = 9

    @staticmethod
    def factory(majorsSplit, itemManager, qty, sm, exclude, nLocs, maxDiff, random):
        if majorsSplit == 'Chozo':
            return ItemPoolGeneratorChozo(itemManager, qty, sm, maxDiff, random)
        elif majorsSplit == 'Plando':
            return ItemPoolGeneratorPlando(itemManager, qty, sm, exclude, nLocs, maxDiff, random)
        elif nLocs == ItemPoolGenerator.maxLocs:
            if majorsSplit == "Scavenger":
                return ItemPoolGeneratorScavenger(itemManager, qty, sm, maxDiff, random)
            else:
                return ItemPoolGeneratorMajors(itemManager, qty, sm, maxDiff, random)
        else:
            return ItemPoolGeneratorMinimizer(itemManager, qty, sm, nLocs, maxDiff, random)

    def __init__(self, itemManager, qty, sm, maxDiff, random):
        self.itemManager = itemManager
        self.qty = qty
        self.sm = sm
        self.maxItems = ItemPoolGenerator.maxLocs
        self.maxEnergy = 18 # 14E, 4R
        self.maxDiff = maxDiff
        self.log = log.get('ItemPool')
        self.random = random

    def isUltraSparseNoTanks(self):
        # if low stuff botwoon is not known there is a hard energy req of one tank, even
        # with both suits
        lowStuffBotwoon = self.sm.knowsLowStuffBotwoon()
        return self.random.random() < 0.5 and (lowStuffBotwoon.bool == True and lowStuffBotwoon.difficulty <= self.maxDiff)

    def calcMaxMinors(self):
        pool = self.itemManager.getItemPool()
        energy = [item for item in pool if item.Category == 'Energy']
        if len(energy) == 0:
            self.maxMinors = 0.66*(self.maxItems - ItemPoolGenerator.nbBosses)
        else:
            # if energy has been placed, we can be as accurate as possible
            self.maxMinors = self.maxItems - len(pool) + self.nbMinorsAlready

    def calcMaxAmmo(self):
        self.nbMinorsAlready = 5
        # always add enough minors to pass zebetites (1100 damages) and mother brain 1 (3000 damages)
        # accounting for missile refill. so 15-10, or 10-10 if ice zeb skip is known (Ice is always in item pool)
        zebSkip = self.sm.knowsIceZebSkip()
        if zebSkip.bool == False or zebSkip.difficulty > self.maxDiff:
            self.log.debug("Add missile because ice zeb skip is not known")
            self.itemManager.addMinor('Missile')
            self.nbMinorsAlready += 1
        self.calcMaxMinors()
        self.log.debug("maxMinors: "+str(self.maxMinors))
        self.minorLocations = max(0, self.maxMinors*self.qty['minors']/100.0 - self.nbMinorsAlready)
        self.log.debug("minorLocations: {}".format(self.minorLocations))

    # add ammo given quantity settings
    def addAmmo(self):
        self.calcMaxAmmo()
        # we have to remove the minors already added
        maxItems = min(len(self.itemManager.getItemPool()) + int(self.minorLocations), self.maxItems)
        self.log.debug("maxItems: {}, (self.maxItems={})".format(maxItems, self.maxItems))
        ammoQty = self.qty['ammo']
        if not self.qty['strictMinors']:
            rangeDict = getRangeDict(ammoQty)
            self.log.debug("rangeDict: {}".format(rangeDict))
            while len(self.itemManager.getItemPool()) < maxItems:
                item = chooseFromRange(rangeDict, self.random)
                self.itemManager.addMinor(item)
        else:
            minorsTypes = ['Missile', 'Super', 'PowerBomb']
            totalProps = sum(ammoQty[m] for m in minorsTypes)
            minorsByProp = sorted(minorsTypes, key=lambda m: ammoQty[m])
            totalMinorLocations = self.minorLocations + self.nbMinorsAlready
            self.log.debug("totalMinorLocations: {}".format(totalMinorLocations))
            def ammoCount(ammo):
                return float(len([item for item in self.itemManager.getItemPool() if item.Type == ammo]))
            def targetRatio(ammo):
                return round(float(ammoQty[ammo])/totalProps, 3)
            def cmpRatio(ammo, ratio):
                thisAmmo = ammoCount(ammo)
                thisRatio = round(thisAmmo/totalMinorLocations, 3)
                nextRatio = round((thisAmmo + 1)/totalMinorLocations, 3)
                self.log.debug("{} current, next/target ratio: {}, {}/{}".format(ammo, thisRatio, nextRatio, ratio))
                return abs(nextRatio - ratio) < abs(thisRatio - ratio)
            def fillAmmoType(ammo, checkRatio=True):
                ratio = targetRatio(ammo)
                self.log.debug("{}: target ratio: {}".format(ammo, ratio))
                while len(self.itemManager.getItemPool()) < maxItems and (not checkRatio or cmpRatio(ammo, ratio)):
                    self.log.debug("Add {}".format(ammo))
                    self.itemManager.addMinor(ammo)
            for m in minorsByProp:
                fillAmmoType(m)
            # now that the ratios have been matched as exactly as possible, we distribute the error
            def getError(m, countOffset=0):
                return abs((ammoCount(m)+countOffset)/totalMinorLocations - targetRatio(m))
            while len(self.itemManager.getItemPool()) < maxItems:
                minNextError = 1000
                chosenAmmo = None
                for m in minorsByProp:
                    nextError = getError(m, 1)
                    if nextError < minNextError:
                        minNextError = nextError
                        chosenAmmo = m
                self.itemManager.addMinor(chosenAmmo)
        # fill up the rest with blank items
        for i in range(self.maxItems - maxItems):
            self.itemManager.addMinor('Nothing')

class ItemPoolGeneratorChozo(ItemPoolGenerator):
    def addEnergy(self):
        total = 18
        energyQty = self.qty['energy']
        if energyQty == 'ultra sparse':
            # 0-1, remove reserve tank and two etanks, check if it also remove the last etank
            self.itemManager.removeItem('Reserve')
            self.itemManager.addItem('NoEnergy', 'Chozo')
            self.itemManager.removeItem('ETank')
            self.itemManager.addItem('NoEnergy', 'Chozo')
            self.itemManager.removeItem('ETank')
            self.itemManager.addItem('NoEnergy', 'Chozo')
            if self.isUltraSparseNoTanks():
                # no etank nor reserve
                self.itemManager.removeItem('ETank')
                self.itemManager.addItem('NoEnergy', 'Chozo')
            elif self.random.random() < 0.5:
                # replace only etank with reserve
                self.itemManager.removeItem('ETank')
                self.itemManager.addItem('Reserve', 'Chozo')

            # complete up to 18 energies with nothing item
            alreadyInPool = 4
            for i in range(total - alreadyInPool):
                self.itemManager.addItem('Nothing', 'Minor')
        elif energyQty == 'sparse':
            # 4-6
            # already 3E and 1R
            alreadyInPool = 4
            rest = randGaussBounds(self.random, 2, 5)
            if rest >= 1:
                if self.random.random() < 0.5:
                    self.itemManager.addItem('Reserve', 'Minor')
                else:
                    self.itemManager.addItem('ETank', 'Minor')
            for i in range(rest-1):
                self.itemManager.addItem('ETank', 'Minor')
            # complete up to 18 energies with nothing item
            for i in range(total - alreadyInPool - rest):
                self.itemManager.addItem('Nothing', 'Minor')
        elif energyQty == 'medium':
            # 8-12
            # add up to 3 Reserves or ETanks (cannot add more than 3 reserves)
            for i in range(3):
                if self.random.random() < 0.5:
                    self.itemManager.addItem('Reserve', 'Minor')
                else:
                    self.itemManager.addItem('ETank', 'Minor')
            # 7 already in the pool (3 E, 1 R, + the previous 3)
            alreadyInPool = 7
            rest = 1 + randGaussBounds(self.random, 4, 3.7)
            for i in range(rest):
                self.itemManager.addItem('ETank', 'Minor')
            # fill the rest with NoEnergy
            for i in range(total - alreadyInPool - rest):
                self.itemManager.addItem('Nothing', 'Minor')
        else:
            # add the vanilla 3 reserves and 13 Etanks
            for i in range(3):
                self.itemManager.addItem('Reserve', 'Minor')
            for i in range(11):
                self.itemManager.addItem('ETank', 'Minor')

    def getItemPool(self):
        self.itemManager.newItemPool()
        # 25 locs: 16 majors, 3 etanks, 1 reserve, 2 missile, 2 supers, 1 pb
        for itemType in ['ETank', 'ETank', 'ETank', 'Reserve', 'Missile', 'Missile', 'Super', 'Super', 'PowerBomb', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
            self.itemManager.addItem(itemType, 'Chozo')

        self.addEnergy()
        self.addAmmo()

        return self.itemManager.getItemPool()

class ItemPoolGeneratorMajors(ItemPoolGenerator):
    def __init__(self, itemManager, qty, sm, maxDiff, random):
        super(ItemPoolGeneratorMajors, self).__init__(itemManager, qty, sm, maxDiff, random)
        self.sparseRest = 1 + randGaussBounds(self.random,2, 5)
        self.mediumRest = 3 + randGaussBounds(self.random, 4, 3.7)
        self.ultraSparseNoTanks = self.isUltraSparseNoTanks()

    def addNoEnergy(self):
        self.itemManager.addItem('NoEnergy')

    def addEnergy(self):
        total = self.maxEnergy
        alreadyInPool = 2
        def getE(toAdd):
            nonlocal total, alreadyInPool
            d = total - alreadyInPool - toAdd
            if d < 0:
                toAdd += d
            return toAdd
        energyQty = self.qty['energy']
        if energyQty == 'ultra sparse':
            # 0-1, add up to one energy (etank or reserve)
            self.itemManager.removeItem('Reserve')
            self.itemManager.removeItem('ETank')
            self.addNoEnergy()
            if self.ultraSparseNoTanks:
                # no energy at all
                self.addNoEnergy()
            else:
                if self.random.random() < 0.5:
                    self.itemManager.addItem('ETank')
                else:
                    self.itemManager.addItem('Reserve')

            # complete with nothing item
            for i in range(total - alreadyInPool):
                self.addNoEnergy()

        elif energyQty == 'sparse':
            # 4-6
            if self.random.random() < 0.5:
                self.itemManager.addItem('Reserve')
            else:
                self.itemManager.addItem('ETank')
            # 3 in the pool (1 E, 1 R + the previous one)
            alreadyInPool = 3
            rest = self.sparseRest
            for i in range(rest):
                self.itemManager.addItem('ETank')
            # complete with nothing item
            for i in range(total - alreadyInPool - rest):
                self.addNoEnergy()

        elif energyQty == 'medium':
            # 8-12
            # add up to 3 Reserves or ETanks (cannot add more than 3 reserves)
            alreadyInPool = 2
            n = getE(3)
            for i in range(n):
                if self.random.random() < 0.5:
                    self.itemManager.addItem('Reserve')
                else:
                    self.itemManager.addItem('ETank')
            alreadyInPool += n
            rest = getE(self.mediumRest)
            for i in range(rest):
                self.itemManager.addItem('ETank')
            # fill the rest with NoEnergy
            for i in range(total - alreadyInPool - rest):
                self.addNoEnergy()
        else:
            nE = getE(13)
            alreadyInPool += nE
            nR = getE(3)
            alreadyInPool += nR
            for i in range(nR):
                self.itemManager.addItem('Reserve')
            for i in range(nE):
                self.itemManager.addItem('ETank')
            for i in range(total - alreadyInPool):
                self.addNoEnergy()

    def getItemPool(self):
        self.itemManager.newItemPool()

        for itemType in ['ETank', 'Reserve', 'Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
            self.itemManager.addItem(itemType, 'Major')
        for itemType in ['Missile', 'Missile', 'Super', 'Super', 'PowerBomb']:
            self.itemManager.addItem(itemType, 'Minor')

        self.addEnergy()
        self.addAmmo()

        return self.itemManager.getItemPool()

class ItemPoolGeneratorScavenger(ItemPoolGeneratorMajors):
    def __init__(self, itemManager, qty, sm, maxDiff, random):
        super(ItemPoolGeneratorScavenger, self).__init__(itemManager, qty, sm, maxDiff, random)

    def addNoEnergy(self):
        self.itemManager.addItem('Nothing')

class ItemPoolGeneratorMinimizer(ItemPoolGeneratorMajors):
    def __init__(self, itemManager, qty, sm, nLocs, maxDiff, random):
        super(ItemPoolGeneratorMinimizer, self).__init__(itemManager, qty, sm, maxDiff, random)
        self.maxItems = nLocs
        self.calcMaxAmmo()
        nMajors = len([itemName for itemName,item in ItemManager.Items.items() if item.Class == 'Major' and item.Category != 'Energy'])
        energyQty = self.qty['energy']
        if energyQty == 'medium':
            if nLocs < 40:
                self.maxEnergy = 5
            elif nLocs < 55:
                self.maxEnergy = 6
            else:
                self.maxEnergy = 5 + self.mediumRest
        elif energyQty == 'vanilla':
            if nLocs < 40:
                self.maxEnergy = 6
            elif nLocs < 55:
                self.maxEnergy = 8
            else:
                self.maxEnergy = 8 + int(float(nLocs - 55)/50.0 * 8)
            self.log.debug("maxEnergy: "+str(self.maxEnergy))
            # remove bosses and minimal minors
            maxItems = self.maxItems - (self.nbMinorsAlready + len(self.itemManager.bossesItems))
            self.maxEnergy = int(max(self.maxEnergy, maxItems - nMajors - self.minorLocations))
            if self.maxEnergy > 18:
                self.maxEnergy = 18
        elif energyQty == 'ultra sparse':
            self.maxEnergy = 0 if self.ultraSparseNoTanks else 1
        elif energyQty == 'sparse':
            self.maxEnergy = 3 + self.sparseRest
        self.log.debug("maxEnergy: "+str(self.maxEnergy))

class ItemPoolGeneratorPlando(ItemPoolGenerator):
    def __init__(self, itemManager, qty, sm, exclude, nLocs, maxDiff, random):
        super(ItemPoolGeneratorPlando, self).__init__(itemManager, qty, sm, maxDiff, random)
        # in exclude dict:
        #   in alreadyPlacedItems:
        #     dict of 'itemType: count' of items already added in the plando.
        #     also a 'total: count' with the total number of items already added in the plando.
        #   in forbiddenItems: list of item forbidden in the pool
        self.exclude = exclude
        self.maxItems = nLocs
        self.log.debug("maxItems: {}".format(self.maxItems))
        self.log.debug("exclude: {}".format(self.exclude))

    def getItemPool(self):
        exceptionMessage = "Too many items already placed by the plando or not enough available locations:"
        self.itemManager.newItemPool(addBosses=False)

        # add the already placed items by the plando
        for item, count in self.exclude['alreadyPlacedItems'].items():
            if item == 'total':
                continue
            itemClass = 'Major'
            if item in ['Missile', 'Super', 'PowerBomb', 'Kraid', 'Phantoon', 'Draygon', 'Ridley', 'MotherBrain', 'SporeSpawn', 'Crocomire', 'Botwoon', 'GoldenTorizo']:
                itemClass = 'Minor'
            for i in range(count):
                self.itemManager.addItem(item, itemClass)

        remain = self.maxItems - self.exclude['alreadyPlacedItems']['total']
        self.log.debug("Plando: remain start: {}".format(remain))
        if remain > 0:
            # add missing bosses
            for boss in self.itemManager.bossesItems:
                if self.exclude['alreadyPlacedItems'][boss] == 0:
                    self.itemManager.addItem(boss, 'Minor')
                    self.exclude['alreadyPlacedItems'][boss] = 1
                    remain -= 1

            self.log.debug("Plando: remain after bosses: {}".format(remain))
            if remain < 0:
                raise Exception("{} can't add the remaining bosses".format(exceptionMessage))

            # add missing majors
            majors = []
            for itemType in ['Bomb', 'Charge', 'Ice', 'HiJump', 'SpeedBooster', 'Wave', 'Spazer', 'SpringBall', 'Varia', 'Plasma', 'Grapple', 'Morph', 'Gravity', 'XRayScope', 'SpaceJump', 'ScrewAttack']:
                if self.exclude['alreadyPlacedItems'][itemType] == 0 and itemType not in self.exclude['forbiddenItems']:
                    self.itemManager.addItem(itemType, 'Major')
                    self.exclude['alreadyPlacedItems'][itemType] = 1
                    majors.append(itemType)
                    remain -= 1

            self.log.debug("Plando: remain after majors: {}".format(remain))
            if remain < 0:
                raise Exception("{} can't add the remaining majors: {}".format(exceptionMessage, ', '.join(majors)))

            # add minimum minors to finish the game
            for (itemType, minimum) in [('Missile', 3), ('Super', 2), ('PowerBomb', 1)]:
                while self.exclude['alreadyPlacedItems'][itemType] < minimum and itemType not in self.exclude['forbiddenItems']:
                    self.itemManager.addItem(itemType, 'Minor')
                    self.exclude['alreadyPlacedItems'][itemType] += 1
                    remain -= 1

            self.log.debug("Plando: remain after minimum minors: {}".format(remain))
            if remain < 0:
                raise Exception("{} can't add the minimum minors to finish the game".format(exceptionMessage))

            # add energy
            energyQty = self.qty['energy']
            limits = {
                "sparse": [('ETank', 4), ('Reserve', 1)],
                "medium": [('ETank', 8), ('Reserve', 2)],
                "vanilla": [('ETank', 14), ('Reserve', 4)]
            }
            for (itemType, minimum) in limits[energyQty]:
                while self.exclude['alreadyPlacedItems'][itemType] < minimum and itemType not in self.exclude['forbiddenItems']:
                    self.itemManager.addItem(itemType, 'Major')
                    self.exclude['alreadyPlacedItems'][itemType] += 1
                    remain -= 1

            self.log.debug("Plando: remain after energy: {}".format(remain))
            if remain < 0:
                raise Exception("{} can't add energy".format(exceptionMessage))

            # add ammo
            nbMinorsAlready = self.exclude['alreadyPlacedItems']['Missile'] + self.exclude['alreadyPlacedItems']['Super'] + self.exclude['alreadyPlacedItems']['PowerBomb']
            minorLocations = max(0, 0.66*self.qty['minors'] - nbMinorsAlready)
            maxItems = len(self.itemManager.getItemPool()) + int(minorLocations)
            ammoQty = {itemType: qty for itemType, qty in self.qty['ammo'].items() if itemType not in self.exclude['forbiddenItems']}
            if ammoQty:
                rangeDict = getRangeDict(ammoQty)
                while len(self.itemManager.getItemPool()) < maxItems and remain > 0:
                    item = chooseFromRange(rangeDict, self.random)
                    self.itemManager.addMinor(item)
                    remain -= 1

            self.log.debug("Plando: remain after ammo: {}".format(remain))

            # add nothing
            while remain > 0:
                self.itemManager.addMinor('Nothing')
                remain -= 1

            self.log.debug("Plando: remain after nothing: {}".format(remain))

        return self.itemManager.getItemPool()
