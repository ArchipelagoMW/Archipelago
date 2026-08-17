from enum import Enum
import re
import copy
from typing import List

from .Config import Config, SMLogic

class ItemType(Enum):
    Nothing = 0
    MapHC = 0x7F
    MapEP = 0x7D
    MapDP = 0x7C
    MapTH = 0x75
    MapPD = 0x79
    MapSP = 0x7A
    MapSW = 0x77
    MapTT = 0x74
    MapIP = 0x76
    MapMM = 0x78
    MapTR = 0x73
    MapGT = 0x72

    CompassEP = 0x8D
    CompassDP = 0x8C
    CompassTH = 0x85
    CompassPD = 0x89
    CompassSP = 0x8A
    CompassSW = 0x87
    CompassTT = 0x84
    CompassIP = 0x86
    CompassMM = 0x88
    CompassTR = 0x83
    CompassGT = 0x82

    BigKeyEP = 0x9D
    BigKeyDP = 0x9C
    BigKeyTH = 0x95
    BigKeyPD = 0x99
    BigKeySP = 0x9A
    BigKeySW = 0x97
    BigKeyTT = 0x94
    BigKeyIP = 0x96
    BigKeyMM = 0x98
    BigKeyTR = 0x93
    BigKeyGT = 0x92       
    
    KeyHC = 0xA0
    KeyCT = 0xA4
    KeyDP = 0xA3
    KeyTH = 0xAA
    KeyPD = 0xA6
    KeySP = 0xA5
    KeySW = 0xA8
    KeyTT = 0xAB
    KeyIP = 0xA9
    KeyMM = 0xA7
    KeyTR = 0xAC
    KeyGT = 0xAD

    Key = 0x24
    Compass = 0x25
    BigKey = 0x32
    Map = 0x33

    Something = 0x6B

    ProgressiveTunic = 0x60
    ProgressiveShield = 0x5F
    ProgressiveSword = 0x5E
    Bow = 0x0B
    SilverArrows = 0x58
    BlueBoomerang = 0x0C
    RedBoomerang = 0x2A
    Hookshot = 0x0A
    Mushroom = 0x29
    Powder = 0x0D
    Firerod = 0x07
    Icerod = 0x08
    Bombos = 0x0f
    Ether = 0x10
    Quake = 0x11
    Lamp = 0x12
    Hammer = 0x09
    Shovel = 0x13
    Flute = 0x14
    Bugnet = 0x21
    Book = 0x1D
    Bottle = 0x16
    Somaria = 0x15
    Byrna = 0x18
    Cape = 0x19
    Mirror = 0x1A
    Boots = 0x4B
    ProgressiveGlove = 0x61
    Flippers = 0x1E
    MoonPearl = 0x1F
    HalfMagic = 0x4E
    HeartPiece = 0x17
    HeartContainer = 0x3E
    HeartContainerRefill = 0x3F
    ThreeBombs = 0x28
    Arrow = 0x43
    TenArrows = 0x44
    OneRupee = 0x34
    FiveRupees = 0x35
    TwentyRupees = 0x36
    TwentyRupees2 = 0x47
    FiftyRupees = 0x41
    OneHundredRupees = 0x40
    ThreeHundredRupees = 0x46
    BombUpgrade5 = 0x51
    BombUpgrade10 = 0x52
    ArrowUpgrade5 = 0x53
    ArrowUpgrade10 = 0x54

    CardCrateriaL1 = 0xD0
    CardCrateriaL2 = 0xD1
    CardCrateriaBoss = 0xD2
    CardBrinstarL1 = 0xD3
    CardBrinstarL2 = 0xD4
    CardBrinstarBoss = 0xD5
    CardNorfairL1 = 0xD6
    CardNorfairL2 = 0xD7
    CardNorfairBoss = 0xD8
    CardMaridiaL1 = 0xD9
    CardMaridiaL2 = 0xDA
    CardMaridiaBoss = 0xDB
    CardWreckedShipL1 = 0xDC
    CardWreckedShipBoss = 0xDD
    CardLowerNorfairL1 = 0xDE
    CardLowerNorfairBoss = 0xDF

    SmMapBrinstar = 0xCA
    SmMapWreckedShip = 0xCB
    SmMapMaridia = 0xCC
    SmMapLowerNorfair = 0xCD

    Missile = 0xC2
    Super = 0xC3
    PowerBomb = 0xC4
    Grapple = 0xB0
    XRay = 0xB1
    ETank = 0xC0
    ReserveTank = 0xC1
    Charge = 0xBB
    Ice = 0xBC
    Wave = 0xBD
    Spazer = 0xBE
    Plasma = 0xBF
    Varia = 0xB2
    Gravity = 0xB6
    Morph = 0xB4
    Bombs = 0xB9
    SpringBall = 0xB3
    ScrewAttack = 0xB5
    HiJump = 0xB7
    SpaceJump = 0xB8
    SpeedBooster = 0xBA

    BottleWithRedPotion = 0x2B
    BottleWithGreenPotion = 0x2C
    BottleWithBluePotion = 0x2D
    BottleWithFairy = 0x3D
    BottleWithBee = 0x3C
    BottleWithGoldBee = 0x48
    RedContent = 0x2E
    GreenContent = 0x2F
    BlueContent = 0x30
    BeeContent = 0x0E

class Item:
    Name: str
    Type: ItemType
    Progression: bool

    dungeon = re.compile("^(BigKey|Key|Map|Compass)")
    bigKey = re.compile("^BigKey")
    key = re.compile("^Key")
    map = re.compile("^Map")
    compass = re.compile("^Compass")
    keycard = re.compile("^Card")
    smMap = re.compile("^SmMap")

    def IsNameDungeonItem(item_name): return Item.dungeon.match(item_name)
    def IsDungeonItem(self): return self.dungeon.match(self.Type.name)
    def IsBigKey(self): return self.bigKey.match(self.Type.name)
    def IsKey(self): return self.key.match(self.Type.name)
    def IsMap(self): return self.map.match(self.Type.name)
    def IsCompass(self): return self.compass.match(self.Type.name)
    def IsKeycard(self): return self.keycard.match(self.Type.name)
    def IsSmMap(self): return self.smMap.match(self.Type.name)

    def Is(self, type: ItemType, world):
        return self.Type == type and self.World == world

    def IsNot(self, type: ItemType, world):
        return not self.Is(type, world)

    def __init__(self, itemType: ItemType, world = None):
        self.Type = itemType
        self.World = world
        self.Progression = False
        #self.Name = itemType.GetDescription()

    @staticmethod
    def Nothing(world):
        return Item(ItemType.Nothing, world)

    @staticmethod
    def AddRange(itemPool, count, item):
        for i in range(count):
            itemPool.append(copy.copy(item))

    @staticmethod
    def CreateProgressionPool(world):
        itemPool = [
            Item(ItemType.ProgressiveShield),
            Item(ItemType.ProgressiveShield),
            Item(ItemType.ProgressiveShield),
            Item(ItemType.ProgressiveSword),
            Item(ItemType.ProgressiveSword),
            Item(ItemType.Bow),
            Item(ItemType.Hookshot),
            Item(ItemType.Mushroom),
            Item(ItemType.Powder),
            Item(ItemType.Firerod),
            Item(ItemType.Icerod),
            Item(ItemType.Bombos),
            Item(ItemType.Ether),
            Item(ItemType.Quake),
            Item(ItemType.Lamp),
            Item(ItemType.Hammer),
            Item(ItemType.Shovel),
            Item(ItemType.Flute),
            Item(ItemType.Bugnet),
            Item(ItemType.Book),
            Item(ItemType.Bottle),
            Item(ItemType.Somaria),
            Item(ItemType.Byrna),
            Item(ItemType.Cape),
            Item(ItemType.Mirror),
            Item(ItemType.Boots),
            Item(ItemType.ProgressiveGlove),
            Item(ItemType.ProgressiveGlove),
            Item(ItemType.Flippers),
            Item(ItemType.MoonPearl),
            Item(ItemType.HalfMagic),

            Item(ItemType.Grapple),
            Item(ItemType.Charge),
            Item(ItemType.Ice),
            Item(ItemType.Wave),
            Item(ItemType.Plasma),
            Item(ItemType.Varia),
            Item(ItemType.Gravity),
            Item(ItemType.Morph),
            Item(ItemType.Bombs),
            Item(ItemType.SpringBall),
            Item(ItemType.ScrewAttack),
            Item(ItemType.HiJump),
            Item(ItemType.SpaceJump),
            Item(ItemType.SpeedBooster),

            Item(ItemType.Missile),
            Item(ItemType.Super),
            Item(ItemType.PowerBomb),
            Item(ItemType.PowerBomb),
            Item(ItemType.ETank),
            Item(ItemType.ETank),
            Item(ItemType.ETank),
            Item(ItemType.ETank),
            Item(ItemType.ETank),

            Item(ItemType.ReserveTank),
            Item(ItemType.ReserveTank),
            Item(ItemType.ReserveTank),
            Item(ItemType.ReserveTank),
        ]

        for item in itemPool:
            item.Progression = True
            item.World = world
        return itemPool

    @staticmethod
    def CreateNicePool(world):
        itemPool = [
            Item(ItemType.ProgressiveTunic),
            Item(ItemType.ProgressiveTunic),
            Item(ItemType.ProgressiveSword),
            Item(ItemType.ProgressiveSword),
            Item(ItemType.SilverArrows),
            Item(ItemType.BlueBoomerang),
            Item(ItemType.RedBoomerang),
            Item(ItemType.Bottle),
            Item(ItemType.Bottle),
            Item(ItemType.Bottle),
            Item(ItemType.HeartContainerRefill),

            Item(ItemType.Spazer),
            Item(ItemType.XRay),
        ]

        Item.AddRange(itemPool, 10, Item(ItemType.HeartContainer, world))

        for item in itemPool:
            item.World = world
        return itemPool

    @staticmethod
    def CreateJunkPool(world):
        itemPool = [
            Item(ItemType.Arrow),
            Item(ItemType.OneHundredRupees)
        ]

        Item.AddRange(itemPool, 24, Item(ItemType.HeartPiece))
        Item.AddRange(itemPool, 8, Item(ItemType.TenArrows))
        Item.AddRange(itemPool, 13, Item(ItemType.ThreeBombs))
        Item.AddRange(itemPool, 4, Item(ItemType.ArrowUpgrade5))
        Item.AddRange(itemPool, 4, Item(ItemType.BombUpgrade5))
        Item.AddRange(itemPool, 2, Item(ItemType.OneRupee))
        Item.AddRange(itemPool, 4, Item(ItemType.FiveRupees))
        Item.AddRange(itemPool, 21 if world.Config.Keysanity else 28, Item(ItemType.TwentyRupees))
        Item.AddRange(itemPool, 7, Item(ItemType.FiftyRupees))
        Item.AddRange(itemPool, 5, Item(ItemType.ThreeHundredRupees))

        Item.AddRange(itemPool, 9, Item(ItemType.ETank))
        Item.AddRange(itemPool, 39, Item(ItemType.Missile))
        Item.AddRange(itemPool, 15, Item(ItemType.Super))
        Item.AddRange(itemPool, 8, Item(ItemType.PowerBomb))

        for item in itemPool:
            item.World = world

        return itemPool

    # The order of the dungeon pool is significant
    @staticmethod
    def CreateDungeonPool(world):
        itemPool = [Item(ItemType.BigKeyGT)]
        Item.AddRange(itemPool, 4, Item(ItemType.KeyGT))
        if (not world.Config.Keysanity):
            itemPool += [
                Item(ItemType.MapGT),
                Item(ItemType.CompassGT),
                ]
        itemPool += [
            Item(ItemType.BigKeyEP),
            Item(ItemType.BigKeyDP),
            Item(ItemType.BigKeyTH),
            Item(ItemType.BigKeyPD),
            Item(ItemType.BigKeySP),
            Item(ItemType.BigKeySW),
            Item(ItemType.BigKeyTT),
            Item(ItemType.BigKeyIP),
            Item(ItemType.BigKeyMM),
            Item(ItemType.BigKeyTR),
        ]

        Item.AddRange(itemPool, 1, Item(ItemType.KeyHC))
        Item.AddRange(itemPool, 2, Item(ItemType.KeyCT))
        Item.AddRange(itemPool, 1, Item(ItemType.KeyDP))
        Item.AddRange(itemPool, 1, Item(ItemType.KeyTH))
        Item.AddRange(itemPool, 6, Item(ItemType.KeyPD))
        Item.AddRange(itemPool, 1, Item(ItemType.KeySP))
        Item.AddRange(itemPool, 3, Item(ItemType.KeySW))
        Item.AddRange(itemPool, 1, Item(ItemType.KeyTT))
        Item.AddRange(itemPool, 2, Item(ItemType.KeyIP))
        Item.AddRange(itemPool, 3, Item(ItemType.KeyMM))
        Item.AddRange(itemPool, 4, Item(ItemType.KeyTR))

        itemPool += [
            Item(ItemType.MapEP),
            Item(ItemType.MapDP),
            Item(ItemType.MapTH),
            Item(ItemType.MapPD),
            Item(ItemType.MapSP),
            Item(ItemType.MapSW),
            Item(ItemType.MapTT),
            Item(ItemType.MapIP),
            Item(ItemType.MapMM),
            Item(ItemType.MapTR),
        ]
        if (not world.Config.Keysanity):
            itemPool += [
                Item(ItemType.MapHC),
                Item(ItemType.CompassEP),
                Item(ItemType.CompassDP),
                Item(ItemType.CompassTH),
                Item(ItemType.CompassPD),
                Item(ItemType.CompassSP),
                Item(ItemType.CompassSW),
                Item(ItemType.CompassTT),
                Item(ItemType.CompassIP),
                Item(ItemType.CompassMM),
                Item(ItemType.CompassTR),
            ]

        for item in itemPool:
            item.World = world

        return itemPool

    @staticmethod
    def CreateKeycards(world):
        itemPool =  [
            Item(ItemType.CardCrateriaL1, world),
            Item(ItemType.CardCrateriaL2, world),
            Item(ItemType.CardCrateriaBoss, world),
            Item(ItemType.CardBrinstarL1, world),
            Item(ItemType.CardBrinstarL2, world),
            Item(ItemType.CardBrinstarBoss, world),
            Item(ItemType.CardNorfairL1, world),
            Item(ItemType.CardNorfairL2, world),
            Item(ItemType.CardNorfairBoss, world),
            Item(ItemType.CardMaridiaL1, world),
            Item(ItemType.CardMaridiaL2, world),
            Item(ItemType.CardMaridiaBoss, world),
            Item(ItemType.CardWreckedShipL1, world),
            Item(ItemType.CardWreckedShipBoss, world),
            Item(ItemType.CardLowerNorfairL1, world),
            Item(ItemType.CardLowerNorfairBoss, world),
        ]

        for item in itemPool:
            item.World = world

        return itemPool

    @staticmethod
    def CreateSmMaps(world):
        itemPool =  [
            Item(ItemType.SmMapBrinstar, world),
            Item(ItemType.SmMapWreckedShip, world),
            Item(ItemType.SmMapMaridia, world),
            Item(ItemType.SmMapLowerNorfair, world)
        ]

        for item in itemPool:
            item.World = world

        return itemPool

    @staticmethod
    def Get(items, itemType:ItemType):
        item = next((i for i in items if i.Type == itemType), None)
        if (item == None):
            raise Exception(f"Could not find an item of type {itemType}")
        return item

    @staticmethod
    def Get(items, itemType:ItemType, world):
        item = next((i for i in items if i.Is(itemType, world)), None)
        if (item == None):
            raise Exception(f"Could not find an item of type {itemType} in world {world.Id}")
        return item

class Progression:
    BigKeyEP: bool
    BigKeyDP: bool
    BigKeyTH: bool
    BigKeyPD: bool
    BigKeySP: bool
    BigKeySW: bool
    BigKeyTT: bool
    BigKeyIP: bool
    BigKeyMM: bool
    BigKeyTR: bool
    BigKeyGT: bool
    KeyHC: bool
    KeyDP: bool
    KeyTH: bool
    KeySP: bool
    KeyTT: bool
    KeyCT: bool
    KeyPD: bool
    KeySW: bool
    KeyIP: bool
    KeyMM: bool
    KeyTR: bool
    KeyGT: bool
    CardCrateriaL1: bool
    CardCrateriaL2: bool
    CardCrateriaBoss: bool
    CardBrinstarL1: bool
    CardBrinstarL2: bool
    CardBrinstarBoss: bool
    CardNorfairL1: bool
    CardNorfairL2: bool
    CardNorfairBoss: bool
    CardMaridiaL1: bool
    CardMaridiaL2: bool
    CardMaridiaBoss: bool
    CardWreckedShipL1: bool
    CardWreckedShipBoss: bool
    CardLowerNorfairL1: bool
    CardLowerNorfairBoss: bool
    def CanBlockLasers(self): return self.shield >= 3
    Sword: bool
    MasterSword: bool
    Bow: bool
    Hookshot: bool
    Mushroom: bool
    Powder: bool
    Firerod: bool
    Icerod: bool
    Bombos: bool
    Ether: bool
    Quake: bool
    Lamp: bool
    Hammer: bool
    Shovel: bool
    Flute: bool
    Book: bool
    Bottle: bool
    Somaria: bool
    Byrna: bool
    Cape: bool
    Mirror: bool
    Boots: bool
    Glove: bool
    Mitt: bool
    Flippers: bool
    MoonPearl: bool
    HalfMagic: bool
    Grapple: bool
    Charge: bool
    Ice: bool
    Wave: bool
    Plasma: bool
    Varia: bool
    Gravity: bool
    Morph: bool
    Bombs: bool
    SpringBall: bool
    ScrewAttack: bool
    HiJump: bool
    SpaceJump: bool
    SpeedBooster: bool
    Missile: bool
    Super: bool
    PowerBomb: bool
    TwoPowerBombs: bool
    ETank: int
    ReserveTank: int

    shield: int

    itemMapping = [
        ItemType.BigKeyEP,
        ItemType.BigKeyDP,
        ItemType.BigKeyTH,
        ItemType.BigKeyPD,
        ItemType.BigKeySP,
        ItemType.BigKeySW,
        ItemType.BigKeyTT,
        ItemType.BigKeyIP,
        ItemType.BigKeyMM,
        ItemType.BigKeyTR,
        ItemType.BigKeyGT,
        ItemType.KeyHC,
        ItemType.KeyDP,
        ItemType.KeyTH,
        ItemType.KeySP,
        ItemType.KeyTT,
        ItemType.CardCrateriaL1,
        ItemType.CardCrateriaL2,
        ItemType.CardCrateriaBoss,
        ItemType.CardBrinstarL1,
        ItemType.CardBrinstarL2,
        ItemType.CardBrinstarBoss,
        ItemType.CardNorfairL1,
        ItemType.CardNorfairL2,
        ItemType.CardNorfairBoss,
        ItemType.CardMaridiaL1,
        ItemType.CardMaridiaL2,
        ItemType.CardMaridiaBoss,
        ItemType.CardWreckedShipL1,
        ItemType.CardWreckedShipBoss,
        ItemType.CardLowerNorfairL1,
        ItemType.CardLowerNorfairBoss,
        ItemType.Bow,
        ItemType.Hookshot,
        ItemType.Mushroom,
        ItemType.Powder,
        ItemType.Firerod,
        ItemType.Icerod,
        ItemType.Bombos,
        ItemType.Ether,
        ItemType.Quake,
        ItemType.Lamp,
        ItemType.Hammer,
        ItemType.Shovel,
        ItemType.Flute,
        ItemType.Book,
        ItemType.Bottle,
        ItemType.Somaria,
        ItemType.Byrna,
        ItemType.Cape,
        ItemType.Mirror,
        ItemType.Boots,
        ItemType.Flippers,
        ItemType.MoonPearl,
        ItemType.HalfMagic,
        ItemType.Grapple,
        ItemType.Charge,
        ItemType.Ice,
        ItemType.Wave,
        ItemType.Plasma,
        ItemType.Varia,
        ItemType.Gravity,
        ItemType.Morph,
        ItemType.Bombs,
        ItemType.SpringBall,
        ItemType.ScrewAttack,
        ItemType.HiJump,
        ItemType.SpaceJump,
        ItemType.SpeedBooster,
        ItemType.Missile,
        ItemType.Super,
    ]

    def __init__(self, items):
        for item in Progression.itemMapping:
            setattr(self, item.name, False)
        self.KeyCT = 0
        self.KeyPD = 0
        self.KeySW = 0
        self.KeyIP = 0
        self.KeyMM = 0
        self.KeyTR = 0
        self.KeyGT = 0
        self.ETank = 0
        self.ReserveTank = 0
        self.shield = 0
        self.MasterSword = False
        self.Sword = False
        self.Mitt = False
        self.Glove = False
        self.TwoPowerBombs = False
        self.PowerBomb = False
        self.Add(items)

    def Add(self, items:List[Item]):
        for item in items:
            found = item.Type in Progression.itemMapping
            if found:
                setattr(self, item.Type.name, True)
                continue

            if (item.Type == ItemType.KeyCT):
                self.KeyCT += 1
            elif (item.Type == ItemType.KeyPD):
                self.KeyPD += 1
            elif (item.Type == ItemType.KeySW):
                self.KeySW += 1
            elif (item.Type == ItemType.KeyIP):
                self.KeyIP += 1
            elif (item.Type == ItemType.KeyMM):
                self.KeyMM += 1
            elif (item.Type == ItemType.KeyTR):
                self.KeyTR += 1
            elif (item.Type == ItemType.KeyGT):
                self.KeyGT += 1
            elif (item.Type == ItemType.ETank):
                self.ETank += 1
            elif (item.Type == ItemType.ReserveTank):
                self.ReserveTank += 1
            elif (item.Type == ItemType.KeyPD):
                self.shield += 1
            elif (item.Type == ItemType.ProgressiveSword):
                self.MasterSword = self.Sword
                self.Sword = True
            elif (item.Type == ItemType.ProgressiveGlove):
                self.Mitt = self.Glove
                self.Glove = True
            elif (item.Type == ItemType.PowerBomb):
                self.TwoPowerBombs = self.PowerBomb
                self.PowerBomb = True     

    def Remove(self, items:List[Item]):
        for item in items:
            found = item.Type in Progression.itemMapping
            if found:
                setattr(self, item.Type.name, False)
                continue

            if (item.Type == ItemType.KeyCT):
                self.KeyCT -= 1
            elif (item.Type == ItemType.KeyPD):
                self.KeyPD -= 1
            elif (item.Type == ItemType.KeySW):
                self.KeySW -= 1
            elif (item.Type == ItemType.KeyIP):
                self.KeyIP -= 1
            elif (item.Type == ItemType.KeyMM):
                self.KeyMM -= 1
            elif (item.Type == ItemType.KeyTR):
                self.KeyTR -= 1
            elif (item.Type == ItemType.KeyGT):
                self.KeyGT -= 1
            elif (item.Type == ItemType.ETank):
                self.ETank -= 1
            elif (item.Type == ItemType.ReserveTank):
                self.ReserveTank -= 1
            elif (item.Type == ItemType.KeyPD):
                self.shield -= 1
            elif (item.Type == ItemType.ProgressiveSword):
                self.Sword = self.MasterSword
                self.MasterSword = False
            elif (item.Type == ItemType.ProgressiveGlove):
                self.Glove = self.Mitt
                self.Mitt = False
            elif (item.Type == ItemType.PowerBomb):
                self.PowerBomb = self.TwoPowerBombs
                self.TwoPowerBombs = False           

    def CanLiftLight(self): return self.Glove

    def CanLiftHeavy(self): return self.Mitt

    def CanLightTorches(self): return self.Firerod or self.Lamp

    def CanMeltFreezors(self): return self.Firerod or self.Bombos and self.Sword

    def CanExtendMagic(self, bars:int = 2): return (2 if self.HalfMagic else 1) * (2 if self.Bottle else 1) >= bars

    def CanKillManyEnemies(self):
        return self.Sword or self.Hammer or self.Bow or self.Firerod or \
                self.Somaria or self.Byrna and self.CanExtendMagic()

    def CanAccessDeathMountainPortal(self):
        return (self.CanDestroyBombWalls() or self.SpeedBooster) and self.Super and self.Morph
        

    def CanAccessDarkWorldPortal(self, config: Config):
        if (config.SMLogic == SMLogic.Normal):
            return self.CardMaridiaL1 and self.CardMaridiaL2 and self.CanUsePowerBombs() and self.Super and self.Gravity and self.SpeedBooster
        else:
            return self.CardMaridiaL1 and self.CardMaridiaL2 and self.CanUsePowerBombs() and self.Super and \
                (self.Charge or self.Super and self.Missile) and \
                (self.Gravity or self.HiJump and self.Ice and self.Grapple) and \
                (self.Ice or self.Gravity and self.SpeedBooster)


    def CanAccessMiseryMirePortal(self, config: Config):
        if (config.SMLogic == SMLogic.Normal):
            return (self.CardNorfairL2 or (self.SpeedBooster and self.Wave)) and self.Varia and self.Super and self.Gravity and self.SpaceJump and self.CanUsePowerBombs()
        else:
            return (self.CardNorfairL2 or self.SpeedBooster) and self.Varia and self.Super and \
                    (self.CanFly() or self.HiJump or self.SpeedBooster or self.CanSpringBallJump() or self.Ice) \
                    and (self.Gravity or self.HiJump) and self.CanUsePowerBombs() 

    def CanIbj(self):
            return self.Morph and self.Bombs

    def CanFly(self):
            return self.SpaceJump or self.CanIbj()

    def CanUsePowerBombs(self):
            return self.Morph and self.PowerBomb

    def CanPassBombPassages(self):
            return self.Morph and (self.Bombs or self.PowerBomb)

    def CanDestroyBombWalls(self):
            return self.CanPassBombPassages() or self.ScrewAttack

    def CanSpringBallJump(self):
            return self.Morph and self.SpringBall

    def CanHellRun(self):
            return self.Varia or self.HasEnergyReserves(5)

    def HasEnergyReserves(self, amount: int):
            return (self.ETank + self.ReserveTank) >= amount

    def CanOpenRedDoors(self):
            return self.Missile or self.Super

    def CanAccessNorfairUpperPortal(self):
            return self.Flute or self.CanLiftLight() and self.Lamp

    def CanAccessNorfairLowerPortal(self):
            return self.Flute and self.CanLiftHeavy()

    def CanAccessMaridiaPortal(self, world):
        from .Region import RewardType
        if (world.Config.SMLogic == SMLogic.Normal):
            return self.MoonPearl and self.Flippers and \
                    self.Gravity and self.Morph and \
                    (world.CanAcquire(self, RewardType.Agahnim) or self.Hammer and self.CanLiftLight() or self.CanLiftHeavy())
        else:
            return self.MoonPearl and self.Flippers and \
                    (self.CanSpringBallJump() or self.HiJump or self.Gravity) and self.Morph and \
                    (world.CanAcquire(self, RewardType.Agahnim) or self.Hammer and self.CanLiftLight() or self.CanLiftHeavy())

# Start of AP integration
items_start_id = 84000

lookup_id_to_name = { items_start_id + enum.value : enum.name for enum in ItemType }
lookup_name_to_id = { item_name : item_id for item_id, item_name in lookup_id_to_name.items() }