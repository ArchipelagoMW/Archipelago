from ..utils.parameters import infinity
import copy

class Location:
    graph_slots = (
        'distance', 'accessPoint', 'difficulty', 'path',
        'pathDifficulty', 'locDifficulty' )
    
    rando_slots = (
        'restricted', )

    solver_slots = (
        'itemName', 'comeBack', 'areaWeight' )

    __slots__ = graph_slots + rando_slots + solver_slots

    def __init__(
            self, distance=None, accessPoint=None,
            difficulty=None, path=None, pathDifficulty=None,
            locDifficulty=None, restricted=None, itemName=None,
            itemType=None, comeBack=None, areaWeight=None):
        self.distance = distance
        self.accessPoint = accessPoint
        self.difficulty = difficulty
        self.path = path
        self.pathDifficulty = pathDifficulty
        self.locDifficulty = locDifficulty
        self.restricted = restricted
        self.itemName = itemName
        self.itemType = itemType
        self.comeBack = comeBack
        self.areaWeight = areaWeight

    def isMajor(self):
        return self._isMajor

    def isChozo(self):
        return self._isChozo

    def isMinor(self):
        return self._isMinor

    def isBoss(self):
        return self._isBoss

    def isScavenger(self):
        return self._isScavenger

    def isClass(self, _class):
        return _class in self.Class

    def setClass(self, _class):
        self.Class = _class
        self._isChozo = 'Chozo' in _class
        self._isMajor = 'Major' in _class
        self._isMinor = 'Minor' in _class
        self._isBoss = 'Boss' in _class
        self._isScavenger = 'Scavenger' in _class

    def evalPostAvailable(self, smbm):
        if self.difficulty.bool == True and self.PostAvailable is not None:
            addAndRemoveItem = smbm.isCountItem(self.itemName) or not smbm.haveItem(self.itemName)
            if addAndRemoveItem:
                smbm.addItem(self.itemName)
            postAvailable = self.PostAvailable(smbm)
            if addAndRemoveItem:
                smbm.removeItem(self.itemName)

            self.difficulty = self.difficulty & postAvailable
            if self.locDifficulty is not None:
                self.locDifficulty = self.locDifficulty & postAvailable

    def evalComeBack(self, smbm, areaGraph, ap):
        if self.difficulty.bool == True:
            # check if we can come back to given ap from the location
            self.comeBack = areaGraph.canAccess(smbm, self.accessPoint, ap, infinity, self.itemName)

    def json(self):
        # to return after plando rando
        ret = {'Name': self.Name, 'accessPoint': self.accessPoint}
        if self.difficulty is not None:
            ret['difficulty'] = self.difficulty.json()
        return ret

    def __repr__(self):
        return "Location({}: {})".format(self.Name,
            '. '.join(
                (repr(getattr(self, slot)) for slot in Location.__slots__ if getattr(self, slot) is not None)))

    def __copy__(self):
        d = self.difficulty
        difficulty = copy.copy(d) if d is not None else None
        ret = type(self)(
            self.distance, self.accessPoint, difficulty, self.path,
            self.pathDifficulty, self.locDifficulty, self.restricted,
            self.itemName, self.itemType, self.comeBack,
            self.areaWeight)
        ret.AccessFrom = self.AccessFrom
        ret.Available = self.Available
        ret.PostAvailable = self.PostAvailable
        ret.setClass(self.Class)

        return ret

    def __eq__(self, other):
        return self.Name == other.Name

def define_location(
        Area, GraphArea, SolveArea, Name, Class, CanHidden, Address, Id,
        Visibility, Room, VanillaItemType=None, BossItemType=None, AccessFrom=None, Available=None, PostAvailable=None, HUD=None):
    name = Name.replace(' ', '').replace(',', '') + 'Location'
    subclass = type(name, (Location,), {
        'Area': Area,
        'GraphArea': GraphArea,
        'SolveArea': SolveArea,
        'Name': Name,
        'Class': Class,
        'CanHidden': CanHidden,
        'Address': Address,
        'Id': Id,
        'Visibility': Visibility,
        'Room': Room,
        'VanillaItemType': VanillaItemType,
        'BossItemType': BossItemType,
        'HUD': HUD,
        'AccessFrom': AccessFrom,
        'Available': Available,
        'PostAvailable': PostAvailable,
        '_isMajor': 'Major' in Class,
        '_isChozo': 'Chozo' in Class,
        '_isMinor': 'Minor' in Class,
        '_isBoss': 'Boss' in Class,
        '_isScavenger': 'Scavenger' in Class
    })
    return subclass()

# all the items locations with the prerequisites to access them
locationsDict = {
###### MAJORS
    "Energy Tank, Gauntlet":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Gauntlet",
    Name="Energy Tank, Gauntlet",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x78264,
    Id=0x5,
    Visibility="Visible",
    Room='Gauntlet Energy Tank Room',
),
    "Bomb":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Bombs",
    Name="Bomb",
    Address=0x78404,
    Id=0x7,
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Visibility="Chozo",
    Room='Bomb Torizo Room',
    VanillaItemType='Bomb',
    HUD=1,
),
    "Energy Tank, Terminator":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Terminator",
    Name="Energy Tank, Terminator",
    Class=["Major"],
    CanHidden=False,
    Address=0x78432,
    Id=0x8,
    Visibility="Visible",
    Room='Terminator Room',
),
    "Reserve Tank, Brinstar":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Reserve Tank, Brinstar",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x7852C,
    Id=0x11,
    Visibility="Chozo",
    Room='Brinstar Reserve Tank Room',
),
    "Charge Beam":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Charge Beam",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78614,
    Id=0x17,
    Visibility="Chozo",
    Room='Big Pink',
    VanillaItemType='Charge',
    HUD=2,
),
    "Morphing Ball":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Morphing Ball",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x786DE,
    Id=0x1a,
    Visibility="Visible",
    Room='Morph Ball Room',
    VanillaItemType='Morph',
    HUD=0,
),
    "Energy Tank, Brinstar Ceiling":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Energy Tank, Brinstar Ceiling",
    Class=["Major"],
    CanHidden=False,
    Address=0x7879E,
    Id=0x1d,
    Visibility="Hidden",
    Room='Blue Brinstar Energy Tank Room',
),
    "Energy Tank, Etecoons":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Energy Tank, Etecoons",
    Class=["Major"],
    CanHidden=True,
    Address=0x787C2,
    Id=0x1e,
    Visibility="Visible",
    Room='Etecoon Energy Tank Room',
),
    "Energy Tank, Waterway":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Energy Tank, Waterway",
    Class=["Major"],
    CanHidden=True,
    Address=0x787FA,
    Id=0x21,
    Visibility="Visible",
    Room='Waterway Energy Tank Room',
),
    "Energy Tank, Brinstar Gate":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Energy Tank, Brinstar Gate",
    Class=["Major"],
    CanHidden=True,
    Address=0x78824,
    Id=0x23,
    Visibility="Visible",
    Room='Hopper Energy Tank Room',
),
    "X-Ray Scope":
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar",
    Name="X-Ray Scope",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78876,
    Id=0x26,
    Visibility="Chozo",
    Room='X-Ray Scope Room',
    VanillaItemType='XRayScope',
    HUD=10,
),
    "Spazer":
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar",
    Name="Spazer",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x7896E,
    Id=0x2a,
    Visibility="Chozo",
    Room='Spazer Room',
    VanillaItemType='Spazer',
    HUD=3,
),
    "Energy Tank, Kraid":
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid",
    Name="Energy Tank, Kraid",
    Class=["Major"],
    CanHidden=False,
    Address=0x7899C,
    Id=0x2b,
    Visibility="Hidden",
    Room='Warehouse Energy Tank Room',
),
    "Kraid":
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid Boss",
    Name="Kraid",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B055,
    Id=None,
    Visibility="Hidden",
    Room='Kraid Room',
    BossItemType="Kraid"
),
    "Varia Suit":
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid Boss",
    Name="Varia Suit",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78ACA,
    Id=0x30,
    Visibility="Chozo",
    Room='Varia Suit Room',
    VanillaItemType='Varia',
    HUD=4,
),
    "Ice Beam":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Ice",
    Name="Ice Beam",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78B24,
    Id=0x32,
    Visibility="Chozo",
    Room='Ice Beam Room',
    VanillaItemType='Ice',
    HUD=6,
),
    "Energy Tank, Crocomire":
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Energy Tank, Crocomire",
    Class=["Major"],
    CanHidden=True,
    Address=0x78BA4,
    Id=0x34,
    Visibility="Visible",
    Room="Crocomire's Room",
),
    "Hi-Jump Boots":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Hi-Jump Boots",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78BAC,
    Id=0x35,
    Visibility="Chozo",
    Room='Hi Jump Boots Room',
    VanillaItemType='HiJump',
    HUD=5,
),
    "Grapple Beam":
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Grapple Beam",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78C36,
    Id=0x3c,
    Visibility="Chozo",
    Room='Grapple Beam Room',
    VanillaItemType='Grapple',
    HUD=9,
),
    "Reserve Tank, Norfair":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Reserve",
    Name="Reserve Tank, Norfair",
    Class=["Major"],
    CanHidden=False,
    Address=0x78C3E,
    Id=0x3d,
    Visibility="Chozo",
    Room='Norfair Reserve Tank Room',
),
    "Speed Booster":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Speed",
    Name="Speed Booster",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78C82,
    Id=0x42,
    Visibility="Chozo",
    Room='Speed Booster Room',
    VanillaItemType='SpeedBooster',
    HUD=7,
),
    "Wave Beam":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Wave",
    Name="Wave Beam",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x78CCA,
    Id=0x44,
    Visibility="Chozo",
    Room='Wave Beam Room',
    VanillaItemType='Wave',
    HUD=8,
),
    "Ridley":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Ridley Boss",
    Name="Ridley",
    Class=["Boss", "Scavenger"],
    CanHidden=False,
    Address=0xB055B056,
    Id=0xaa,
    Visibility="Hidden",
    Room="Ridley's Room",
    VanillaItemType="Ridley",
    BossItemType="Ridley",
    HUD=16
),
    "Energy Tank, Ridley":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Ridley Boss",
    Name="Energy Tank, Ridley",
    Class=["Major", "Chozo"],
    CanHidden=False,
    Address=0x79108,
    Id=0x4e,
    Visibility="Hidden",
    Room='Ridley Tank Room',
),
    "Screw Attack":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Screw Attack",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x79110,
    Id=0x4f,
    Visibility="Chozo",
    Room='Screw Attack Room',
    VanillaItemType='ScrewAttack',
    HUD=15,
),
    "Energy Tank, Firefleas":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Energy Tank, Firefleas",
    Class=["Major"],
    CanHidden=True,
    Address=0x79184,
    Id=0x50,
    Visibility="Visible",
    Room='Lower Norfair Fireflea Room',
),
    "Reserve Tank, Wrecked Ship":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Gravity",
    Name="Reserve Tank, Wrecked Ship",
    Class=["Major"],
    CanHidden=False,
    Address=0x7C2E9,
    Id=0x81,
    Visibility="Chozo",
    Room='Bowling Alley',
),
    "Energy Tank, Wrecked Ship":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Back",
    Name="Energy Tank, Wrecked Ship",
    Class=["Major", "Chozo"],
    CanHidden=True,
    Address=0x7C337,
    Id=0x84,
    Visibility="Visible",
    Room='Wrecked Ship Energy Tank Room',
),
    "Phantoon":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="Phantoon Boss",
    Name="Phantoon",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B057,
    Id=None,
    Visibility="Hidden",
    Room="Phantoon's Room",
    BossItemType="Phantoon"
),
    "Right Super, Wrecked Ship":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Main",
    Name="Right Super, Wrecked Ship",
    Class=["Major", "Chozo"],
    CanHidden=True,
    Address=0x7C365,
    Id=0x86,
    Visibility="Visible",
    Room='Wrecked Ship East Super Room',
),
    "Gravity Suit":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Gravity",
    Name="Gravity Suit",
    Class=["Major", "Scavenger"],
    CanHidden=False,
    Address=0x7C36D,
    Id=0x87,
    Visibility="Chozo",
    Room='Gravity Suit Room',
    VanillaItemType='Gravity',
    HUD=11,
),
    "Energy Tank, Mama turtle":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Energy Tank, Mama turtle",
    Class=["Major"],
    CanHidden=True,
    Address=0x7C47D,
    Id=0x8a,
    Visibility="Visible",
    Room='Mama Turtle Room',
),
    "Plasma Beam":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Forgotten Highway",
    Name="Plasma Beam",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x7C559,
    Id=0x8f,
    Visibility="Chozo",
    Room='Plasma Room',
    VanillaItemType='Plasma',
    HUD=14,
),
    "Reserve Tank, Maridia":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Left Sandpit",
    Name="Reserve Tank, Maridia",
    Class=["Major"],
    CanHidden=False,
    Address=0x7C5E3,
    Id=0x91,
    Visibility="Chozo",
    Room='West Sand Hole',
),
    "Spring Ball":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Sandpits",
    Name="Spring Ball",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x7C6E5,
    Id=0x96,
    Visibility="Chozo",
    Room='Spring Ball Room',
    VanillaItemType='SpringBall',
    HUD=13,
),
    "Energy Tank, Botwoon":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Top",
    Name="Energy Tank, Botwoon",
    Class=["Major"],
    CanHidden=True,
    Address=0x7C755,
    Id=0x98,
    Visibility="Visible",
    Room='Botwoon Energy Tank Room',
),
    "Draygon":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Draygon Boss",
    Name="Draygon",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B058,
    Id=None,
    Visibility="Hidden",
    Room="Draygon's Room",
    BossItemType="Draygon"
),
    "Space Jump":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Draygon Boss",
    Name="Space Jump",
    Class=["Major", "Chozo", "Scavenger"],
    CanHidden=False,
    Address=0x7C7A7,
    Id=0x9a,
    Visibility="Chozo",
    Room='Space Jump Room',
    VanillaItemType='SpaceJump',
    HUD=12,
),
    "Mother Brain":
define_location(
    Area="Tourian",
    GraphArea="Tourian",
    SolveArea="Tourian",
    Name="Mother Brain",
    Class=["Boss"],
    Address=0xB055B059,
    Id=None,
    Visibility="Hidden",
    CanHidden=False,
    Room='Mother Brain Room',
    BossItemType="MotherBrain"
),
    "Spore Spawn":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Spore Spawn",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B055,
    Id=None,
    Visibility="Hidden",
    Room='Spore Spawn Room',
    BossItemType="SporeSpawn"
),
    "Botwoon":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Top",
    Name="Botwoon",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B055,
    Id=None,
    Visibility="Hidden",
    Room="Botwoon's Room",
    BossItemType="Botwoon"
),
    "Crocomire":
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Crocomire",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B055,
    Id=None,
    Visibility="Hidden",
    Room="Crocomire's Room",
    BossItemType="Crocomire"
),
    "Golden Torizo":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Golden Torizo",
    Class=["Boss"],
    CanHidden=False,
    Address=0xB055B055,
    Id=None,
    Visibility="Hidden",
    Room="Golden Torizo's Room",
    BossItemType="GoldenTorizo"
),
###### MINORS
    "Power Bomb (Crateria surface)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Power Bomb (Crateria surface)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x781CC,
    Id=0x0,
    Visibility="Visible",
    Room='Crateria Power Bomb Room',
),
    "Missile (outside Wrecked Ship bottom)":
define_location(
    Area="Crateria",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Bottom",
    Name="Missile (outside Wrecked Ship bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x781E8,
    Id=0x1,
    Visibility="Visible",
    Room='West Ocean',
),
    "Missile (outside Wrecked Ship top)":
define_location(
    Area="Crateria",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Top",
    Name="Missile (outside Wrecked Ship top)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x781EE,
    Id=0x2,
    Visibility="Hidden",
    Room='West Ocean',
),
    "Missile (outside Wrecked Ship middle)":
define_location(
    Area="Crateria",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Top",
    Name="Missile (outside Wrecked Ship middle)",
    CanHidden=True,
    Class=["Minor"],
    Address=0x781F4,
    Id=0x3,
    Visibility="Visible",
    Room='West Ocean',
),
    "Missile (Crateria moat)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Missile (Crateria moat)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78248,
    Id=0x4,
    Visibility="Visible",
    Room='The Moat',
),
    "Missile (Crateria bottom)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Missile (Crateria bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x783EE,
    Id=0x6,
    Visibility="Visible",
    Room='Pit Room',
),
    "Missile (Crateria gauntlet right)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Gauntlet",
    Name="Missile (Crateria gauntlet right)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78464,
    Id=0x9,
    Visibility="Visible",
    Room='Green Pirates Shaft',
),
    "Missile (Crateria gauntlet left)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Gauntlet",
    Name="Missile (Crateria gauntlet left)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7846A,
    Id=0xa,
    Visibility="Visible",
    Room='Green Pirates Shaft',
),
    "Super Missile (Crateria)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Super Missile (Crateria)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78478,
    Id=0xb,
    Visibility="Visible",
    Room='Crateria Super Room',
),
    "Missile (Crateria middle)":
define_location(
    Area="Crateria",
    GraphArea="Crateria",
    SolveArea="Crateria Landing Site",
    Name="Missile (Crateria middle)",
    Class=["Minor", "Chozo"],
    CanHidden=True,
    Address=0x78486,
    Id=0xc,
    Visibility="Visible",
    Room='The Final Missile',
),
    "Power Bomb (green Brinstar bottom)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Power Bomb (green Brinstar bottom)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x784AC,
    Id=0xd,
    Visibility="Chozo",
    Room='Green Brinstar Main Shaft',
),
    "Super Missile (pink Brinstar)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Super Missile (pink Brinstar)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x784E4,
    Id=0xe,
    Visibility="Chozo",
    Room='Spore Spawn Super Room',
),
    "Missile (green Brinstar below super missile)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Missile (green Brinstar below super missile)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78518,
    Id=0xf,
    Visibility="Visible",
    Room='Early Supers Room',
),
    "Super Missile (green Brinstar top)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Super Missile (green Brinstar top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7851E,
    Id=0x10,
    Visibility="Visible",
    Room='Early Supers Room',
),
    "Missile (green Brinstar behind missile)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Missile (green Brinstar behind missile)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78532,
    Id=0x12,
    Visibility="Hidden",
    Room='Brinstar Reserve Tank Room',
),
    "Missile (green Brinstar behind reserve tank)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar Reserve",
    Name="Missile (green Brinstar behind reserve tank)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78538,
    Id=0x13,
    Visibility="Visible",
    Room='Brinstar Reserve Tank Room',
),
    "Missile (pink Brinstar top)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Missile (pink Brinstar top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78608,
    Id=0x15,
    Visibility="Visible",
    Room='Big Pink',
),
    "Missile (pink Brinstar bottom)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Missile (pink Brinstar bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7860E,
    Id=0x16,
    Visibility="Visible",
    Room='Big Pink',
),
    "Power Bomb (pink Brinstar)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Pink Brinstar",
    Name="Power Bomb (pink Brinstar)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7865C,
    Id=0x18,
    Visibility="Visible",
    Room='Pink Brinstar Power Bomb Room',
),
    "Missile (green Brinstar pipe)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Brinstar Hills",
    Name="Missile (green Brinstar pipe)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78676,
    Id=0x19,
    Visibility="Visible",
    Room='Green Hill Zone',
),
    "Power Bomb (blue Brinstar)":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Power Bomb (blue Brinstar)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7874C,
    Id=0x1b,
    Visibility="Visible",
    Room='Morph Ball Room',
),
    "Missile (blue Brinstar middle)":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar middle)",
    Address=0x78798,
    Id=0x1c,
    Class=["Minor"],
    CanHidden=True,
    Visibility="Visible",
    Room='Blue Brinstar Energy Tank Room',
),
    "Super Missile (green Brinstar bottom)":
define_location(
    Area="Brinstar",
    GraphArea="GreenPinkBrinstar",
    SolveArea="Green Brinstar",
    Name="Super Missile (green Brinstar bottom)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x787D0,
    Id=0x1f,
    Visibility="Visible",
    Room='Etecoon Super Room',
),
    "Missile (blue Brinstar bottom)":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar bottom)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x78802,
    Id=0x22,
    Visibility="Chozo",
    Room='First Missile Room',
),
    "Missile (blue Brinstar top)":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78836,
    Id=0x24,
    Visibility="Visible",
    Room='Billy Mays Room',
),
    "Missile (blue Brinstar behind missile)":
define_location(
    Area="Brinstar",
    GraphArea="Crateria",
    SolveArea="Blue Brinstar",
    Name="Missile (blue Brinstar behind missile)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7883C,
    Id=0x25,
    Visibility="Hidden",
    Room='Billy Mays Room',
),
    "Power Bomb (red Brinstar sidehopper room)":
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar Top",
    Name="Power Bomb (red Brinstar sidehopper room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x788CA,
    Id=0x27,
    Visibility="Visible",
    Room='Beta Power Bomb Room',
),
    "Power Bomb (red Brinstar spike room)":
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar Top",
    Name="Power Bomb (red Brinstar spike room)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x7890E,
    Id=0x28,
    Visibility="Chozo",
    Room='Alpha Power Bomb Room',
),
    "Missile (red Brinstar spike room)":
define_location(
    Area="Brinstar",
    GraphArea="RedBrinstar",
    SolveArea="Red Brinstar Top",
    Name="Missile (red Brinstar spike room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78914,
    Id=0x29,
    Visibility="Visible",
    Room='Alpha Power Bomb Room',
),
    "Missile (Kraid)":
define_location(
    Area="Brinstar",
    GraphArea="Kraid",
    SolveArea="Kraid",
    Name="Missile (Kraid)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x789EC,
    Id=0x2c,
    Visibility="Hidden",
    Room='Warehouse Keyhunter Room',
),
    "Missile (lava room)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Missile (lava room)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78AE4,
    Id=0x31,
    Visibility="Hidden",
    Room='Cathedral',
),
    "Missile (below Ice Beam)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Ice",
    Name="Missile (below Ice Beam)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78B46,
    Id=0x33,
    Visibility="Hidden",
    Room='Crumble Shaft',
),
    "Missile (above Crocomire)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Grapple Escape",
    Name="Missile (above Crocomire)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78BC0,
    Id=0x36,
    Visibility="Visible",
    Room='Crocomire Escape',
),
    "Missile (Hi-Jump Boots)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Missile (Hi-Jump Boots)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78BE6,
    Id=0x37,
    Visibility="Visible",
    Room='Hi Jump Energy Tank Room',
),
    "Energy Tank (Hi-Jump Boots)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Norfair Entrance",
    Name="Energy Tank (Hi-Jump Boots)",
    CanHidden=True,
    Class=["Minor"],
    Address=0x78BEC,
    Id=0x38,
    Visibility="Visible",
    Room='Hi Jump Energy Tank Room',
),
    "Power Bomb (Crocomire)":
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Power Bomb (Crocomire)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C04,
    Id=0x39,
    Visibility="Visible",
    Room='Post Crocomire Power Bomb Room',
),
    "Missile (below Crocomire)":
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Missile (below Crocomire)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C14,
    Id=0x3a,
    Visibility="Visible",
    Room='Post Crocomire Missile Room',
),
    "Missile (Grapple Beam)":
define_location(
    Area="Norfair",
    GraphArea="Crocomire",
    SolveArea="Crocomire",
    Name="Missile (Grapple Beam)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C2A,
    Id=0x3b,
    Visibility="Visible",
    Room='Post Crocomire Jump Room',
),
    "Missile (Norfair Reserve Tank)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Reserve",
    Name="Missile (Norfair Reserve Tank)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78C44,
    Id=0x3e,
    Visibility="Hidden",
    Room='Norfair Reserve Tank Room',
),
    "Missile (bubble Norfair green door)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Reserve",
    Name="Missile (bubble Norfair green door)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C52,
    Id=0x3f,
    Visibility="Visible",
    Room='Green Bubbles Missile Room',
),
    "Missile (bubble Norfair)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Bottom",
    Name="Missile (bubble Norfair)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78C66,
    Id=0x40,
    Visibility="Visible",
    Room='Bubble Mountain',
),
    "Missile (Speed Booster)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Speed",
    Name="Missile (Speed Booster)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78C74,
    Id=0x41,
    Visibility="Hidden",
    Room='Speed Booster Hall',
),
    "Missile (Wave Beam)":
define_location(
    Area="Norfair",
    GraphArea="Norfair",
    SolveArea="Bubble Norfair Wave",
    Name="Missile (Wave Beam)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78CBC,
    Id=0x43,
    Visibility="Visible",
    Room='Double Chamber',
),
    "Missile (Gold Torizo)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Missile (Gold Torizo)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78E6E,
    Id=0x46,
    Visibility="Visible",
    Room="Golden Torizo's Room",
),
    "Super Missile (Gold Torizo)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Screw Attack",
    Name="Super Missile (Gold Torizo)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78E74,
    Id=0x47,
    Visibility="Hidden",
    Room="Golden Torizo's Room",
),
    "Missile (Mickey Mouse room)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair Before Amphitheater",
    Name="Missile (Mickey Mouse room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78F30,
    Id=0x49,
    Visibility="Visible",
    Room='Mickey Mouse Room',
),
    "Missile (lower Norfair above fire flea room)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Missile (lower Norfair above fire flea room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x78FCA,
    Id=0x4a,
    Visibility="Visible",
    Room='Lower Norfair Spring Ball Maze Room',
),
    "Power Bomb (lower Norfair above fire flea room)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Power Bomb (lower Norfair above fire flea room)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x78FD2,
    Id=0x4b,
    Visibility="Visible",
    Room='Lower Norfair Escape Power Bomb Room',
),
    "Power Bomb (Power Bombs of shame)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Power Bomb (Power Bombs of shame)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x790C0,
    Id=0x4c,
    Visibility="Visible",
    Room='Wasteland',
),
    "Missile (lower Norfair near Wave Beam)":
define_location(
    Area="LowerNorfair",
    GraphArea="LowerNorfair",
    SolveArea="Lower Norfair After Amphitheater",
    Name="Missile (lower Norfair near Wave Beam)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x79100,
    Id=0x4d,
    Visibility="Visible",
    Room="Three Muskateers' Room",
),
    "Missile (Wrecked Ship middle)":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Main",
    Name="Missile (Wrecked Ship middle)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C265,
    Id=0x80,
    Visibility="Visible",
    Room='Wrecked Ship Main Shaft',
),
    "Missile (Gravity Suit)":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Gravity",
    Name="Missile (Gravity Suit)",
    Class=["Minor", "Chozo"],
    CanHidden=False,
    Address=0x7C2EF,
    Id=0x82,
    Visibility="Visible",
    Room='Bowling Alley',
),
    "Missile (Wrecked Ship top)":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Top",
    Name="Missile (Wrecked Ship top)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C319,
    Id=0x83,
    Visibility="Visible",
    Room='Wrecked Ship East Missile Room',
),
    "Super Missile (Wrecked Ship left)":
define_location(
    Area="WreckedShip",
    GraphArea="WreckedShip",
    SolveArea="WreckedShip Main",
    Name="Super Missile (Wrecked Ship left)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C357,
    Id=0x85,
    Visibility="Visible",
    Room='Wrecked Ship West Super Room',
),
    "Missile (green Maridia shinespark)":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Missile (green Maridia shinespark)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7C437,
    Id=0x88,
    Visibility="Visible",
    Room='Main Street',
),
    "Super Missile (green Maridia)":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Super Missile (green Maridia)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C43D,
    Id=0x89,
    Visibility="Visible",
    Room='Main Street',
),
    "Missile (green Maridia tatori)":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Green",
    Name="Missile (green Maridia tatori)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7C483,
    Id=0x8b,
    Visibility="Hidden",
    Room='Mama Turtle Room',
),
    "Super Missile (yellow Maridia)":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Super Missile (yellow Maridia)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C4AF,
    Id=0x8c,
    Visibility="Visible",
    Room='Watering Hole',
),
    "Missile (yellow Maridia super missile)":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Missile (yellow Maridia super missile)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C4B5,
    Id=0x8d,
    Visibility="Visible",
    Room='Watering Hole',
),
    "Missile (yellow Maridia false wall)":
define_location(
    Area="Maridia",
    GraphArea="WestMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Missile (yellow Maridia false wall)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C533,
    Id=0x8e,
    Visibility="Visible",
    Room='Pseudo Plasma Spark Room',
),
    "Missile (left Maridia sand pit room)":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Left Sandpit",
    Name="Missile (left Maridia sand pit room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C5DD,
    Id=0x90,
    Visibility="Visible",
    Room='West Sand Hole',
),
    "Missile (right Maridia sand pit room)":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Right Sandpit",
    Name="Missile (right Maridia sand pit room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C5EB,
    Id=0x92,
    Visibility="Visible",
    Room='East Sand Hole',
),
    "Power Bomb (right Maridia sand pit room)":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Right Sandpit",
    Name="Power Bomb (right Maridia sand pit room)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C5F1,
    Id=0x93,
    Visibility="Visible",
    Room='East Sand Hole',
),
    "Missile (pink Maridia)":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Missile (pink Maridia)",
    Address=0x7C603,
    Id=0x94,
    Class=["Minor"],
    CanHidden=True,
    Visibility="Visible",
    Room='Aqueduct',
),
    "Super Missile (pink Maridia)":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Bottom",
    Name="Super Missile (pink Maridia)",
    Class=["Minor"],
    CanHidden=True,
    Address=0x7C609,
    Id=0x95,
    Visibility="Visible",
    Room='Aqueduct',
),
    "Missile (Draygon)":
define_location(
    Area="Maridia",
    GraphArea="EastMaridia",
    SolveArea="Maridia Pink Top",
    Name="Missile (Draygon)",
    Class=["Minor"],
    CanHidden=False,
    Address=0x7C74D,
    Id=0x97,
    Visibility="Hidden",
    Room='The Precious Room',
)
}
