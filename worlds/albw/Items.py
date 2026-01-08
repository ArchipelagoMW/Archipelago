from typing import Dict, List, Optional
from enum import Enum
from BaseClasses import Item, ItemClassification
from .Options import ALBWOptions, LogicMode
from albwrandomizer import PyRandomizable, Item as RItem, Goal, Vane, new_item, new_goal, new_vane

class ALBWItem(Item):
    game = "A Link Between Worlds"

class ItemType(Enum):
    Normal = 0
    Ravio = 1
    Compass = 2
    BigKey = 3
    SmallKey = 4
    Junk = 5
    Prize = 6
    Shop = 7
    Event = 8
    Vane = 9

Normal = ItemType.Normal
Ravio = ItemType.Ravio
Compass = ItemType.Compass
BigKey = ItemType.BigKey
SmallKey = ItemType.SmallKey
Junk = ItemType.Junk
Prize = ItemType.Prize
Shop = ItemType.Shop
Event = ItemType.Event

filler = ItemClassification.filler
useful = ItemClassification.useful
progression = ItemClassification.progression
progression_skip_balancing = ItemClassification.progression_skip_balancing

class ItemData:
    code: Optional[int]
    name: str
    itemtype: ItemType
    classification: ItemClassification
    progress: List[PyRandomizable]
    count: int
    vane: Optional[Vane]

    cur_code: int = 0

    def __init__(
        self,
        code: Optional[int],
        name: str,
        itemtype: ItemType,
        classification: ItemClassification,
        progress: List[PyRandomizable],
        count: int = 1,
        vane: Optional[Vane] = None,
    ):
        self.code = code
        self.name = name
        self.itemtype = itemtype
        self.classification = classification
        self.progress = progress
        self.count = count
        self.vane = vane
    
    def __eq__(self, other: object):
        if not isinstance(other, ItemData):
            return NotImplemented
        return self.name == other.name
    
    def is_dungeon_item(self) -> bool:
        return self.itemtype in [Compass, SmallKey, BigKey]
    
    def is_event(self) -> bool:
        return self.code is None
    
    def get_classification(self, options: ALBWOptions):
        if self == Items.Mail and options.logic_mode in [LogicMode.option_adv_glitched, LogicMode.option_hell]:
            return progression
        return self.classification
    
def goal(name: str, goal: Goal) -> ItemData:
    return ItemData(None, name, ItemType.Event, progression, [new_goal(goal)])

def vane(name: str, vane: Vane) -> ItemData:
    return ItemData(None, name, ItemType.Vane, progression, [new_vane(vane)], vane=vane)

class Items:
    Bow = ItemData(0, "Bow", Ravio, progression, [
        new_item(RItem.Bow01),
        new_item(RItem.Bow02),
    ], 2)
    Boomerang = ItemData(1, "Boomerang", Ravio, progression, [
        new_item(RItem.Boomerang01),
        new_item(RItem.Boomerang02),
    ], 2)
    Hookshot = ItemData(2, "Hookshot", Ravio, progression, [
        new_item(RItem.Hookshot01),
        new_item(RItem.Hookshot02)
    ], 2)
    Bombs = ItemData(3, "Bombs", Ravio, progression, [
        new_item(RItem.Bombs01),
        new_item(RItem.Bombs02),
    ], 2)
    FireRod = ItemData(4, "Fire Rod", Ravio, progression, [
        new_item(RItem.FireRod01),
        new_item(RItem.FireRod02),
    ], 2)
    IceRod = ItemData(5, "Ice Rod", Ravio, progression, [
        new_item(RItem.IceRod01),
        new_item(RItem.IceRod02),
    ], 2)
    Hammer = ItemData(6, "Hammer", Ravio, progression, [
        new_item(RItem.Hammer01),
        new_item(RItem.Hammer02),
    ], 2)
    SandRod = ItemData(7, "Sand Rod", Ravio, progression, [
        new_item(RItem.SandRod01),
        new_item(RItem.SandRod02),
    ], 2)
    TornadoRod = ItemData(8, "Tornado Rod", Ravio, progression, [
        new_item(RItem.TornadoRod01),
        new_item(RItem.TornadoRod02)
    ], 2)
    Bell = ItemData(9, "Bell", Normal, progression, [new_item(RItem.Bell)])
    StaminaScroll = ItemData(10, "Stamina Scroll", Normal, progression, [new_item(RItem.StaminaScroll)])
    BowOfLight = ItemData(11, "Bow of Light", Normal, progression, [new_item(RItem.BowOfLight)])
    Boots = ItemData(12, "Pegasus Boots", Normal, progression, [new_item(RItem.PegasusBoots)])
    Flippers = ItemData(13, "Flippers", Normal, progression, [new_item(RItem.Flippers)])
    Bracelet = ItemData(14, "Progressive Bracelet", Normal, progression, [
        new_item(RItem.RaviosBracelet01),
        new_item(RItem.RaviosBracelet02),
    ], 2)
    HylianShield = ItemData(15, "Hylian Shield", Normal, useful, [new_item(RItem.HylianShield)])
    SmoothGem = ItemData(16, "Smooth Gem", Normal, progression, [new_item(RItem.SmoothGem)])
    # Letter = ItemData(17, "Letter in a Bottle", Normal, progression, [new_item(RItem.LetterInABottle)])
    PremiumMilk = ItemData(18, "Premium Milk", Normal, progression, [new_item(RItem.PremiumMilk)])
    Pouch = ItemData(19, "Pouch", Normal, useful, [new_item(RItem.Pouch)])
    BeeBadge = ItemData(20, "Bee Badge", Normal, filler, [new_item(RItem.BeeBadge)])
    HintGlasses = ItemData(21, "Hint Glasses", Normal, filler, [new_item(RItem.HintGlasses)])
    Charm = ItemData(22, "Charm", Normal, filler, [new_item(RItem.Charm)])
    GreatSpin = ItemData(23, "Great Spin", Normal, progression, [new_item(RItem.GreatSpin)])
    Quake = ItemData(24, "Quake", Normal, progression, [new_item(RItem.Quake)])
    RupeeGreen = ItemData(25, "Green Rupee", Junk, filler, [new_item(RItem.RupeeGreen)], 2)
    RupeeBlue = ItemData(26, "Blue Rupee", Junk, filler, [new_item(RItem.RupeeBlue)], 8)
    RupeeRed = ItemData(27, "Red Rupee", Junk, filler, [new_item(RItem.RupeeRed)], 20)
    RupeePurple = ItemData(28, "Purple Rupee", Normal, filler, [new_item(RItem.RupeePurple01)], 20)
    RupeeSilver = ItemData(29, "Silver Rupee", Normal, filler, [new_item(RItem.RupeeSilver01)], 39)
    RupeeGold = ItemData(30, "Gold Rupee", Normal, filler, [new_item(RItem.RupeeGold01)], 9)
    Maiamai = ItemData(31, "Maiamai", Normal, filler, [new_item(RItem.Maiamai001)], 100)
    MonsterGuts = ItemData(32, "Monster Guts", Junk, filler, [new_item(RItem.MonsterGuts)], 12)
    MonsterHorn = ItemData(33, "Monster Horn", Junk, filler, [new_item(RItem.MonsterHorn)], 3)
    MonsterTail = ItemData(34, "Monster Tail", Junk, filler, [new_item(RItem.MonsterTail)], 4)
    HeartPiece = ItemData(35, "Piece of Heart", Normal, useful, [new_item(RItem.HeartPiece01)], 27)
    HeartContainer = ItemData(36, "Heart Container", Normal, useful, [new_item(RItem.HeartContainer01)], 10)
    Bottle = ItemData(37, "Bottle", Normal, progression, [
        new_item(RItem.Bottle01),
        new_item(RItem.Bottle02),
        new_item(RItem.Bottle03),
        new_item(RItem.Bottle04),
        new_item(RItem.Bottle05),
    ], 4)
    Lamp = ItemData(38, "Lamp", Normal, progression, [
        new_item(RItem.Lamp01),
        new_item(RItem.Lamp02),
    ], 2)
    Sword = ItemData(39, "Progressive Sword", Normal, progression, [
        new_item(RItem.Sword01),
        new_item(RItem.Sword02),
        new_item(RItem.Sword03),
        new_item(RItem.Sword04),
    ], 4)
    Glove = ItemData(40, "Progressive Glove", Normal, progression, [
        new_item(RItem.Glove01),
        new_item(RItem.Glove02),
    ], 2)
    Net = ItemData(41, "Bug Net", Normal, progression, [
        new_item(RItem.Net01),
        new_item(RItem.Net02),
    ], 2)
    Mail = ItemData(42, "Progressive Mail", Normal, useful, [
        new_item(RItem.Mail01),
        new_item(RItem.Mail02),
    ], 2)
    Ore = ItemData(43, "Master Ore", Normal, progression, [
        new_item(RItem.OreYellow),
        new_item(RItem.OreGreen),
        new_item(RItem.OreBlue),
        new_item(RItem.OreRed),
    ], 4)
    KeyHyruleSanctuary = ItemData(44, "Small Key (Hyrule Sanctuary)", SmallKey, progression, [
        new_item(RItem.HyruleSanctuaryKey),
    ])
    KeyLoruleSanctuary = ItemData(45, "Small Key (Lorule Sanctuary)", SmallKey, progression, [
        new_item(RItem.LoruleSanctuaryKey),
    ])
    CompassEastern = ItemData(46, "Compass (Eastern Palace)", Compass, filler, [new_item(RItem.EasternCompass)])
    BigKeyEastern = ItemData(47, "Big Key (Eastern Palace)", BigKey, progression, [
        new_item(RItem.EasternKeyBig),
    ])
    KeyEastern = ItemData(48, "Small Key (Eastern Palace)", SmallKey, progression, [
        new_item(RItem.EasternKeySmall01),
        new_item(RItem.EasternKeySmall02),
    ], 2)
    CompassGales = ItemData(49, "Compass (House of Gales)", Compass, filler, [new_item(RItem.GalesCompass)])
    BigKeyGales = ItemData(50, "Big Key (House of Gales)", BigKey, progression, [
        new_item(RItem.GalesKeyBig),
    ])
    KeyGales = ItemData(51, "Small Key (House of Gales)", SmallKey, progression, [
        new_item(RItem.GalesKeySmall01),
        new_item(RItem.GalesKeySmall02),
        new_item(RItem.GalesKeySmall03),
        new_item(RItem.GalesKeySmall04),
    ], 4)
    CompassHera = ItemData(52, "Compass (Tower of Hera)", Compass, filler, [new_item(RItem.HeraCompass)])
    BigKeyHera = ItemData(53, "Big Key (Tower of Hera)", BigKey, progression, [
        new_item(RItem.HeraKeyBig),
    ])
    KeyHera = ItemData(54, "Small Key (Tower of Hera)", SmallKey, progression, [
        new_item(RItem.HeraKeySmall01),
        new_item(RItem.HeraKeySmall02),
    ], 2)
    CompassDark = ItemData(55, "Compass (Dark Palace)", Compass, filler, [new_item(RItem.DarkCompass)])
    BigKeyDark = ItemData(56, "Big Key (Dark Palace)", BigKey, progression, [
        new_item(RItem.DarkKeyBig),
    ])
    KeyDark = ItemData(57, "Small Key (Dark Palace)", SmallKey, progression, [
        new_item(RItem.DarkKeySmall01),
        new_item(RItem.DarkKeySmall02),
        new_item(RItem.DarkKeySmall03),
        new_item(RItem.DarkKeySmall04),
    ], 4)
    CompassSwamp = ItemData(58, "Compass (Swamp Palace)", Compass, filler, [new_item(RItem.SwampCompass)])
    BigKeySwamp = ItemData(59, "Big Key (Swamp Palace)", BigKey, progression, [
        new_item(RItem.SwampKeyBig),
    ])
    KeySwamp = ItemData(60, "Small Key (Swamp Palace)", SmallKey, progression, [
        new_item(RItem.SwampKeySmall01),
        new_item(RItem.SwampKeySmall02),
        new_item(RItem.SwampKeySmall03),
        new_item(RItem.SwampKeySmall04),
    ], 4)
    CompassSkull = ItemData(61, "Compass (Skull Woods)", Compass, filler, [new_item(RItem.SkullCompass)])
    BigKeySkull = ItemData(62, "Big Key (Skull Woods)", BigKey, progression, [
        new_item(RItem.SkullKeyBig),
    ])
    KeySkull = ItemData(63, "Small Key (Skull Woods)", SmallKey, progression, [
        new_item(RItem.SkullKeySmall01),
        new_item(RItem.SkullKeySmall02),
        new_item(RItem.SkullKeySmall03),
    ], 3)
    CompassThieves = ItemData(64, "Compass (Thieves' Hideout)", Compass, filler, [new_item(RItem.ThievesCompass)])
    BigKeyThieves = ItemData(65, "Big Key (Thieves' Hideout)", BigKey, progression, [
        new_item(RItem.ThievesKeyBig),
    ])
    KeyThieves = ItemData(66, "Small Key (Thieves' Hideout)", SmallKey, progression, [
        new_item(RItem.ThievesKeySmall),
    ])
    CompassIce = ItemData(67, "Compass (Ice Ruins)", Compass, filler, [new_item(RItem.IceCompass)])
    BigKeyIce = ItemData(68, "Big Key (Ice Ruins)", BigKey, progression, [
        new_item(RItem.IceKeyBig),
    ])
    KeyIce = ItemData(69, "Small Key (Ice Ruins)", SmallKey, progression, [
        new_item(RItem.IceKeySmall01),
        new_item(RItem.IceKeySmall02),
        new_item(RItem.IceKeySmall03),
    ], 3)
    CompassDesert = ItemData(70, "Compass (Desert Palace)", Compass, filler, [new_item(RItem.DesertCompass)])
    BigKeyDesert = ItemData(71, "Big Key (Desert Palace)", BigKey, progression, [
        new_item(RItem.DesertKeyBig),
    ])
    KeyDesert = ItemData(72, "Small Key (Desert Palace)", SmallKey, progression, [
        new_item(RItem.DesertKeySmall01),
        new_item(RItem.DesertKeySmall02),
        new_item(RItem.DesertKeySmall03),
        new_item(RItem.DesertKeySmall04),
        new_item(RItem.DesertKeySmall05),
    ], 5)
    CompassTurtle = ItemData(73, "Compass (Turtle Rock)", Compass, filler, [new_item(RItem.TurtleCompass)])
    BigKeyTurtle = ItemData(74, "Big Key (Turtle Rock)", BigKey, progression, [
        new_item(RItem.TurtleKeyBig),
    ])
    KeyTurtle = ItemData(75, "Small Key (Turtle Rock)", SmallKey, progression, [
        new_item(RItem.TurtleKeySmall01),
        new_item(RItem.TurtleKeySmall02),
        new_item(RItem.TurtleKeySmall03),
    ], 3)
    CompassCastle = ItemData(76, "Compass (Lorule Castle)", Compass, filler, [new_item(RItem.LoruleCastleCompass)])
    KeyCastle = ItemData(77, "Small Key (Lorule Castle)", SmallKey, progression, [
        new_item(RItem.LoruleCastleKeySmall01),
        new_item(RItem.LoruleCastleKeySmall02),
        new_item(RItem.LoruleCastleKeySmall03),
        new_item(RItem.LoruleCastleKeySmall04),
        new_item(RItem.LoruleCastleKeySmall05),
    ], 5)
    PendantOfPower = ItemData(None, "Pendant of Power", Prize, progression, [new_item(RItem.PendantOfPower)])
    PendantOfWisdom = ItemData(None, "Pendant of Wisdom", Prize, progression, [new_item(RItem.PendantOfWisdom)])
    PendantOfCourage = ItemData(None, "Pendant of Courage", Prize, progression, [new_item(RItem.PendantOfCourage)])
    Gulley = ItemData(None, "Rescue Gulley", Prize, progression, [new_item(RItem.SageGulley)])
    Oren = ItemData(None, "Rescue Oren", Prize, progression, [new_item(RItem.SageOren)])
    Seres = ItemData(None, "Rescue Seres", Prize, progression, [new_item(RItem.SageSeres)])
    Osfala = ItemData(None, "Rescue Osfala", Prize, progression, [new_item(RItem.SageOsfala)])
    Rosso = ItemData(None, "Rescue Rosso", Prize, progression, [new_item(RItem.SageRosso)])
    Irene = ItemData(None, "Rescue Irene", Prize, progression, [new_item(RItem.SageIrene)])
    Impa = ItemData(None, "Rescue Impa", Prize, progression, [new_item(RItem.SageImpa)])
    ScootFruit = ItemData(None, "Scoot Fruit", Shop, progression, [new_item(RItem.ScootFruit01)])
    FoulFruit = ItemData(None, "Foul Fruit", Shop, filler, [new_item(RItem.FoulFruit01)])
    Shield = ItemData(None, "Shield", Shop, progression, [new_item(RItem.Shield01)])
    GoldBee = ItemData(None, "Gold Bee", Shop, progression, [new_item(RItem.GoldBee01)])
    Bee = ItemData(None, "Bee", Shop, filler, [new_item(RItem.Bee01)])
    Fairy = ItemData(None, "Fairy", Shop, filler, [new_item(RItem.Fairy01)])
    Yuga = goal("Yuga", Goal.Yuga)
    Margomill = goal("Margomill", Goal.Margomill)
    Moldorm = goal("Moldorm", Goal.Moldorm)
    GemesaurKing = goal("Gemesaur King", Goal.GemesaurKing)
    Arrghus = goal("Arrghus", Goal.Arrghus)
    Knucklemaster = goal("Knucklemaster", Goal.Knucklemaster)
    Stalblind = goal("Stalblind", Goal.Stalblind)
    Dharkstare = goal("Dharkstare", Goal.Dharkstare)
    Zaganaga = goal("Zaganaga", Goal.Zaganaga)
    Grinexx = goal("Grinexx", Goal.Grinexx)
    RavioSigns = goal("Ravio Signs", Goal.RavioSigns)
    RavioShopOpen = goal("Ravio Shop Open", Goal.RavioShopOpen)
    OpenSanctuaryDoors = goal("Open Sanctuary Doors", Goal.OpenSanctuaryDoors)
    ShadyGuyTrigger = goal("Shady Guy Trigger", Goal.ShadyGuyTrigger)
    BigBombFlower = goal("Big Bomb Flower", Goal.BigBombFlower)
    StylishWomansHouseOpen = goal("Stylish Woman's House Open", Goal.StylishWomansHouseOpen)
    WomanRoofMaiamai = goal("Woman's Roof Maiamai", Goal.WomanRoofMaiamai)
    SkullEyeRight = goal("Skull Eye Right", Goal.SkullEyeRight)
    SkullEyeLeft = goal("Skull Eye Left", Goal.SkullEyeLeft)
    ThievesB1DoorOpen = goal("Thieves B1 Door Open", Goal.ThievesB1DoorOpen)
    ThievesB2DoorOpen = goal("Thieves B2 Door Open", Goal.ThievesB2DoorOpen)
    ThievesB3WaterDrained = goal("Thieves B3 Water Drained", Goal.ThievesB3WaterDrained)
    TurtleFlipped = goal("Turtle (flipped)", Goal.TurtleFlipped)
    TurtleAttacked = goal("Turtle (attacked)", Goal.TurtleAttacked)
    TurtleWall = goal("Turtle (wall)", Goal.TurtleWall)
    AccessPotionShop = goal("Access Potion Shop", Goal.AccessPotionShop)
    AccessMilkBar = goal("Access Milk Bar", Goal.AccessMilkBar)
    AccessFairyFountain = goal("Access Fairy Fountain", Goal.AccessFairyFountain)
    AccessHyruleBlacksmith = goal("Access Hyrule Blacksmith", Goal.AccessHyruleBlacksmith)
    AccessLoruleCastleField = goal("Access Lorule Castle Field", Goal.AccessLoruleCastleField)
    ClearTreacherousTower = goal("Clear Treacherous Tower", Goal.ClearTreacherousTower)
    BombTrial = goal("Bomb Trial Complete", Goal.LcBombTrial)
    TileTrial = goal("Tile Trial Complete", Goal.LcTileTrial)
    LampTrial = goal("Lamp Trial Complete", Goal.LcLampTrial)
    HookTrial = goal("Hookshot Trial Complete", Goal.LcHookTrial)
    Triforce = goal("Triforce", Goal.Triforce)
    BlacksmithWV = vane("Blacksmith Weather Vane", Vane.BlacksmithWV)
    DarkPalaceWV = vane("Dark Palace Weather Vane", Vane.DarkPalaceWV)
    DeathMountainHyruleWV = vane("Death Mountain (Hyrule) Weather Vane", Vane.DeathMountainHyruleWV)
    DeathMountainLoruleWV = vane("Death Mountain (Lorule) Weather Vane", Vane.DeathMountainLoruleWV)
    DesertPalaceWV = vane("Desert Palace Weather Vane", Vane.DesertPalaceWV)
    EasternPalaceWV = vane("Eastern Palace Weather Vane", Vane.EasternPalaceWV)
    GraveyardWV = vane("Graveyard Weather Vane", Vane.GraveyardWV)
    HouseOfGalesWV = vane("House of Gales Weather Vane", Vane.HouseOfGalesWV)
    IceRuinsWV = vane("Ice Ruins Weather Vane", Vane.IceRuinsWV)
    KakarikoVillageWV = vane("Kakariko Village Weather Vane", Vane.KakarikoVillageWV)
    LoruleCastleWV = vane("Lorule Castle Weather Vane", Vane.LoruleCastleWV)
    MiseryMireWV = vane("Misery Mire Weather Vane", Vane.MiseryMireWV)
    SanctuaryWV = vane("Sanctuary Weather Vane", Vane.SanctuaryWV)
    SkullWoodsWV = vane("Skull Woods Weather Vane", Vane.SkullWoodsWV)
    SwampPalaceWV = vane("Swamp Palace Weather Vane", Vane.SwampPalaceWV)
    ThievesTownWV = vane("Thieves' Town Weather Vane", Vane.ThievesTownWV)
    TowerOfHeraWV = vane("Tower of Hera Weather Vane", Vane.TowerOfHeraWV)
    TreacherousTowerWV = vane("Treacherous Tower Weather Vane", Vane.TreacherousTowerWV)
    TurtleRockWV = vane("Turtle Rock Weather Vane", Vane.TurtleRockWV)
    VacantHouseWV = vane("Vacant House Weather Vane", Vane.VacantHouseWV)
    WitchsHouseWV = vane("Witch's House Weather Vane", Vane.WitchsHouseWV)
    YourHouseWV = vane("Your House Weather Vane", Vane.YourHouseWV)

all_items: List[ItemData] = [item for (name, item) in vars(Items).items() if name[:2] != "__"]
item_table: Dict[str, ItemData] = {item.name: item for item in all_items}
item_code_table: Dict[int, ItemData] = {item.code: item for item in all_items if item.code is not None}
vane_to_item: Dict[Vane, ItemData] = {item.vane: item for item in all_items if item.vane is not None}

hyrule_vanes: List[ItemData] = [
    Items.DeathMountainHyruleWV,
    Items.DesertPalaceWV,
    Items.EasternPalaceWV,
    Items.HouseOfGalesWV,
    Items.KakarikoVillageWV,
    Items.SanctuaryWV,
    Items.TowerOfHeraWV,
    Items.WitchsHouseWV,
    Items.YourHouseWV,
]

lorule_vanes: List[ItemData] = [
    Items.BlacksmithWV,
    Items.DarkPalaceWV,
    Items.DeathMountainLoruleWV,
    Items.GraveyardWV,
    Items.IceRuinsWV,
    Items.LoruleCastleWV,
    Items.MiseryMireWV,
    Items.SkullWoodsWV,
    Items.SwampPalaceWV,
    Items.ThievesTownWV,
    Items.TreacherousTowerWV,
    Items.TurtleRockWV,
    Items.VacantHouseWV,
]

convenient_hyrule_vanes: List[ItemData] = [
    Items.KakarikoVillageWV,
    Items.SanctuaryWV,
    Items.WitchsHouseWV,
    Items.YourHouseWV,
]

convenient_lorule_vanes: List[ItemData] = [
    Items.BlacksmithWV,
    Items.DarkPalaceWV,
    Items.LoruleCastleWV,
    Items.MiseryMireWV,
    Items.SkullWoodsWV,
    Items.ThievesTownWV,
    Items.VacantHouseWV,
]

APItem = new_item(RItem.LetterInABottle)
