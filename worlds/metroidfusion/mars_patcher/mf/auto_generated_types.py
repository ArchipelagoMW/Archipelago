# This file is generated. Manual changes will be lost
# fmt: off
# ruff: noqa
# mypy: disable-error-code="misc"
from __future__ import annotations

import typing_extensions as typ


# Definitions
Seed: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 2147483647']
Typeu4: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 15']
Typeu5: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 31']
Typeu8: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 255']
Typeu10: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 1023']
Areaid: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 6']
Areaidkey = typ.Literal[
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6'
]
Minimapidkey = typ.Literal[
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '10'
]
Sectorid: typ.TypeAlias = typ.Annotated[int, '1 <= value <= 6']
Shortcutsectorlist: typ.TypeAlias = typ.Annotated[list[Sectorid], 'len() == 6']
Huerotation: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 360']
Validsources = typ.Literal[
    'MainDeckData',
    'Arachnus',
    'ChargeCoreX',
    'Level1',
    'TroData',
    'Zazabi',
    'Serris',
    'Level2',
    'PyrData',
    'MegaX',
    'Level3',
    'ArcData1',
    'WideCoreX',
    'ArcData2',
    'Yakuza',
    'Nettori',
    'Nightmare',
    'Level4',
    'AqaData',
    'WaveCoreX',
    'Ridley',
    'Boiler',
    'Animals',
    'AuxiliaryPower'
]
Validitems = typ.Literal[
    'None',
    'Level0',
    'Missiles',
    'MorphBall',
    'ChargeBeam',
    'Level1',
    'Bombs',
    'HiJump',
    'SpeedBooster',
    'Level2',
    'SuperMissiles',
    'VariaSuit',
    'Level3',
    'IceMissiles',
    'WideBeam',
    'PowerBombs',
    'SpaceJump',
    'PlasmaBeam',
    'GravitySuit',
    'Level4',
    'DiffusionMissiles',
    'WaveBeam',
    'ScrewAttack',
    'IceBeam',
    'MissileTank',
    'EnergyTank',
    'PowerBombTank',
    'IceTrap',
    'InfantMetroid'
]
Validitemsprites = typ.Literal[
    'Empty',
    'Missiles',
    'Level0',
    'MorphBall',
    'ChargeBeam',
    'Level1',
    'Bombs',
    'HiJump',
    'SpeedBooster',
    'Level2',
    'SuperMissiles',
    'VariaSuit',
    'Level3',
    'IceMissiles',
    'WideBeam',
    'PowerBombs',
    'SpaceJump',
    'PlasmaBeam',
    'GravitySuit',
    'Level4',
    'DiffusionMissiles',
    'WaveBeam',
    'ScrewAttack',
    'IceBeam',
    'MissileTank',
    'EnergyTank',
    'PowerBombTank',
    'Anonymous',
    'ShinyMissileTank',
    'ShinyPowerBombTank',
    'InfantMetroid'
]
Validabilities = typ.Literal[
    'Missiles',
    'MorphBall',
    'ChargeBeam',
    'Bombs',
    'HiJump',
    'SpeedBooster',
    'SuperMissiles',
    'VariaSuit',
    'IceMissiles',
    'WideBeam',
    'PowerBombs',
    'SpaceJump',
    'PlasmaBeam',
    'GravitySuit',
    'DiffusionMissiles',
    'WaveBeam',
    'ScrewAttack',
    'IceBeam'
]
Validelevatortops = typ.Literal[
    'OperationsDeckTop',
    'MainHubToSector1',
    'MainHubToSector2',
    'MainHubToSector3',
    'MainHubToSector4',
    'MainHubToSector5',
    'MainHubToSector6',
    'MainHubTop',
    'HabitationDeckTop',
    'Sector1ToRestrictedLab'
]
Validelevatorbottoms = typ.Literal[
    'OperationsDeckBottom',
    'MainHubBottom',
    'RestrictedLabToSector1',
    'HabitationDeckBottom',
    'Sector1ToMainHub',
    'Sector2ToMainHub',
    'Sector3ToMainHub',
    'Sector4ToMainHub',
    'Sector5ToMainHub',
    'Sector6ToMainHub'
]
Validlanguages = typ.Literal[
    'JapaneseKanji',
    'JapaneseHiragana',
    'English',
    'German',
    'French',
    'Italian',
    'Spanish'
]
Messagelanguages: typ.TypeAlias = dict[Validlanguages, str]

class Itemmessages(typ.TypedDict, total=False):
    Kind: typ.Required[Itemmessageskind]
    Languages: Messagelanguages
    Centered: bool = True
    MessageID: typ.Annotated[int, '0 <= value <= 56']
    """The Message ID, will display one of the predefined messages in the ROM"""

Itemmessageskind = typ.Literal[
    'CustomMessage',
    'MessageID'
]
Jingle = typ.Literal[
    'Minor',
    'Major'
]

class BlocklayerItem(typ.TypedDict, total=False):
    X: Typeu8
    """The X position in the room that should get edited."""

    Y: Typeu8
    """The Y position in the room that should get edited."""

    Value: Typeu10
    """The value that should be used to edit the room. For backgrounds, this is calculated via `((Row-1) * ColumnsInTileset) + (Column-1)`."""

Blocklayer: typ.TypeAlias = typ.Annotated[list[BlocklayerItem], 'Unique items']
Hintlocks = typ.Literal[
    'OPEN',
    'LOCKED',
    'GREY',
    'BLUE',
    'GREEN',
    'YELLOW',
    'RED'
]

# Schema entries

class MarsschemamfLocationsMajorlocationsItem(typ.TypedDict):
    Source: Validsources
    """Valid major locations."""

    Item: Validitems
    """Valid items for shuffling."""

    ItemMessages: typ.NotRequired[Itemmessages]
    Jingle: Jingle

class MarsschemamfLocationsMinorlocationsItem(typ.TypedDict):
    Area: Areaid
    """The area ID where this item is located."""

    Room: Typeu8
    """The room ID where this item is located."""

    BlockX: Typeu8
    """The X-coordinate in the room where this item is located."""

    BlockY: Typeu8
    """The Y-coordinate in the room where this item is located."""

    Item: Validitems
    """Valid items for shuffling."""

    ItemSprite: typ.NotRequired[Validitemsprites]
    """Valid graphics for minor location items."""

    ItemMessages: typ.NotRequired[Itemmessages]
    Jingle: Jingle

class MarsschemamfLocations(typ.TypedDict):
    """Specifies how the item locations in the game should be changed."""

    MajorLocations: typ.Annotated[list[MarsschemamfLocationsMajorlocationsItem], 'len() == 23', 'Unique items']
    """Specifies how the major item locations should be changed. A major item location is a location where an item is obtained by defeating a boss or interacting with a device."""

    MinorLocations: typ.Annotated[list[MarsschemamfLocationsMinorlocationsItem], 'len() == 103', 'Unique items']
    """Specifies how the minor item locations should be changed. A minor item location is a location where an item is obtained by touching a tank block."""


class MarsschemamfStartinglocation(typ.TypedDict):
    """The location the player should spawn at the start of the game."""

    Area: Areaid
    """The area ID of the starting location."""

    Room: Typeu8
    """The room ID of the starting location."""

    BlockX: Typeu8
    """The X-coordinate in the room where the player should spawn. If the room contains a save station, then this value will not be taken into consideration."""

    BlockY: Typeu8
    """The Y-coordinate in the room where the player should spawn. If the room contains a save station, then this value will not be taken into consideration."""

MarsschemamfStartingitemsSecuritylevelsItem = typ.Literal[
    0,
    1,
    2,
    3,
    4
]

class MarsschemamfStartingitems(typ.TypedDict, total=False):
    Energy: typ.Annotated[int, '1 <= value <= 2099'] = 99
    """How much energy the player should start with on a new save file."""

    Missiles: typ.Annotated[int, '0 <= value <= 999'] = 10
    """How many missiles the player should start with on a new save file (the amount unlocked by collecting missile data)."""

    PowerBombs: typ.Annotated[int, '0 <= value <= 99'] = 10
    """How many power bombs the player should start with on a new save file (the amount unlocked by collecting power bomb data)."""

    Abilities: typ.Annotated[list[Validabilities], 'Unique items'] = []
    """Which abilities the player should start with on a new save file."""

    SecurityLevels: typ.Annotated[list[MarsschemamfStartingitemsSecuritylevelsItem], 'Unique items'] = [0]
    """Which security levels will be unlocked from the start."""

    DownloadedMaps: typ.Annotated[list[Areaid], 'Unique items'] = []
    """Which area maps will be downloaded from the start."""


class MarsschemamfTankincrements(typ.TypedDict):
    """How much ammo/health tanks provide when collected."""

    MissileTank: typ.Annotated[int, '-1000 <= value <= 1000'] = 5
    """How much ammo missile tanks provide when collected."""

    EnergyTank: typ.Annotated[int, '-2100 <= value <= 2100'] = 100
    """How much health energy tanks provide when collected."""

    PowerBombTank: typ.Annotated[int, '-100 <= value <= 100'] = 2
    """How much ammo power bomb tanks provide when collected."""

    MissileData: typ.NotRequired[typ.Annotated[int, '0 <= value <= 1000']] = 10
    """How much ammo Missile Launcher Data provides when collected."""

    PowerBombData: typ.NotRequired[typ.Annotated[int, '0 <= value <= 100']] = 10
    """How much ammo Power Bomb Data provides when collected."""


class MarsschemamfElevatorconnections(typ.TypedDict):
    """Defines the elevator that each elevator connects to."""

    ElevatorTops: typ.Annotated[dict[Validelevatortops, Validelevatorbottoms], 'len() >= 10']
    """Defines the bottom elevator that each top elevator connects to."""

    ElevatorBottoms: typ.Annotated[dict[Validelevatorbottoms, Validelevatortops], 'len() >= 10']
    """Defines the top elevator that each bottom elevator connects to."""


class MarsschemamfSectorshortcuts(typ.TypedDict):
    """Defines the sector that each sector shortcut connects to."""

    LeftAreas: Shortcutsectorlist
    """Destination areas on the left side of sectors."""

    RightAreas: Shortcutsectorlist
    """Destination areas on the right side of sectors"""

MarsschemamfDoorlocksItemLocktype = typ.Literal[
    'Open',
    'Level0',
    'Level1',
    'Level2',
    'Level3',
    'Level4',
    'Locked'
]

class MarsschemamfDoorlocksItem(typ.TypedDict):
    Area: Areaid
    """The area ID where this door is located."""

    Door: Typeu8
    """The door ID of this door."""

    LockType: MarsschemamfDoorlocksItemLocktype
    """The type of cover on the hatch."""

MarsschemamfPalettesRandomizeKey = typ.Literal[
    'Tilesets',
    'Enemies',
    'Samus',
    'Beams'
]

@typ.final
class MarsschemamfPalettesRandomize(typ.TypedDict, total=False):
    """The range to use for rotating palette hues."""

    HueMin: Huerotation = None
    """The minimum value to use for rotating palette hues. If not specified, the patcher will randomly generate one."""

    HueMax: Huerotation = None
    """The maximum value to use for rotating palette hues. If not specified, the patcher will randomly generate one."""


MarsschemamfPalettesColorspace = typ.Literal[
    'HSV',
    'Oklab'
]

@typ.final
class MarsschemamfPalettes(typ.TypedDict, total=False):
    """Properties for randomized in-game palettes."""

    Seed: Seed = None
    """A number used to initialize the random number generator for palettes. If not specified, the patcher will randomly generate one."""

    Randomize: typ.Required[dict[MarsschemamfPalettesRandomizeKey, MarsschemamfPalettesRandomize]]
    """What kind of palettes should be randomized."""

    ColorSpace: MarsschemamfPalettesColorspace = 'Oklab'
    """The color space to use for rotating palette hues."""

    Symmetric: bool = True
    """Randomly rotates hues in the positive or negative direction true."""


class MarsschemamfNavigationtextNavigationterminals(typ.TypedDict, total=False):
    """Assigns each navigation room a specific text."""

    MainDeckWest: str
    """Specifies what text should appear at the west Navigation Terminal in Main Deck."""

    MainDeckEast: str
    """Specifies what text should appear at the east Navigation Terminal in Main Deck."""

    OperationsDeck: str
    """Specifies what text should appear at the Navigation Terminal in Operations Deck."""

    Sector1Entrance: str
    """Specifies what text should appear at the Navigation Terminal in Sector 1."""

    Sector2Entrance: str
    """Specifies what text should appear at the Navigation Terminal in Sector 2."""

    Sector3Entrance: str
    """Specifies what text should appear at the Navigation Terminal in Sector 3."""

    Sector4Entrance: str
    """Specifies what text should appear at the Navigation Terminal in Sector 4."""

    Sector5Entrance: str
    """Specifies what text should appear at the Navigation Terminal in Sector 5."""

    Sector6Entrance: str
    """Specifies what text should appear at the Navigation Terminal in Sector 6."""

    AuxiliaryPower: str
    """Specifies what text should appear at the Navigation Terminal near the Auxiliary Power Station."""

    RestrictedLabs: str
    """Specifies what text should appear at the Navigation Terminal in the Restricted Labs."""


class MarsschemamfNavigationtextShiptext(typ.TypedDict, total=False):
    """Assigns the ship specific text."""

    InitialText: str
    """Specifies what text should appear at the initial ship communication."""

    ConfirmText: str
    """Specifies what text should appear at the ship after confirming 'No' on subsequent ship communications."""


@typ.final
class MarsschemamfNavigationtext(typ.TypedDict, total=False):
    """Specifies text for a specific language."""

    NavigationTerminals: MarsschemamfNavigationtextNavigationterminals
    """Assigns each navigation room a specific text."""

    ShipText: MarsschemamfNavigationtextShiptext
    """Assigns the ship specific text."""



class MarsschemamfTitletextItem(typ.TypedDict, total=False):
    Text: typ.Annotated[str, '/^[ -~]{0,30}$/']
    """The ASCII text for this line"""

    LineNum: typ.Annotated[int, '0 <= value <= 14']
MarsschemamfCreditstextItemLinetype = typ.Literal[
    'Blank',
    'Blue',
    'Red',
    'White1',
    'White2'
]

class MarsschemamfCreditstextItem(typ.TypedDict, total=False):
    LineType: typ.Required[MarsschemamfCreditstextItemLinetype]
    """The color and line height of the text (or blank)."""

    Text: typ.Annotated[str, '/^[ -~]{0,34}$/']
    """The ASCII text for this line."""

    BlankLines: Typeu8 = 0
    """Inserts the provided number of blank lines after the text line."""

    Centered: bool = True
    """Centers the text horizontally when true."""

MarsschemamfNavstationlocksKey = typ.Literal[
    'MainDeckWest',
    'MainDeckEast',
    'OperationsDeck',
    'RestrictedLabs',
    'AuxiliaryPower',
    'Sector1Entrance',
    'Sector2Entrance',
    'Sector3Entrance',
    'Sector4Entrance',
    'Sector5Entrance',
    'Sector6Entrance'
]


@typ.final
class MarsschemamfLeveledits(typ.TypedDict, total=False):
    """Specifies the Room ID."""

    BG1: Blocklayer
    """The BG1 layer that should be edited."""

    BG2: Blocklayer
    """The BG2 layer that should be edited."""

    Clipdata: Blocklayer
    """The Clipdata layer that should be edited."""




class MarsschemamfMinimapeditsItem(typ.TypedDict, total=False):
    X: Typeu5
    """The X position in the minimap that should get edited."""

    Y: Typeu5
    """The Y position in the minimap that should get edited."""

    Tile: Typeu10
    """The tile value that should be used to edit the minimap."""

    Palette: Typeu4
    """The palette row to use for the tile."""

    HFlip: bool = False
    """Whether the tile should be horizontally flipped or not."""

    VFlip: bool = False
    """Whether the tile should be vertically flipped or not."""



class MarsschemamfRoomnamesItem(typ.TypedDict):
    Area: Areaid
    """The area ID where this room is located."""

    Room: Typeu8 = 3
    """The room ID."""

    Name: typ.Annotated[str, 'len() <= 112']
    """Specifies what text should appear for this room. Two lines are available, with an absolute maximum of 56 characters per line, if all characters used are small. Text will auto-wrap if the next word doesn't fit on the line. If the text is too long, it will be truncated.  Use 
 to force a line break. If not provided, will display 'Unknown Room'."""


class Marsschemamf(typ.TypedDict, total=False):
    """
    Metroid Fusion patching schema
    
    A json schema describing the input for patching Metroid Fusion via mars_patcher.
    """

    SeedHash: typ.Required[typ.Annotated[str, '/^[0-9A-Z]{8}$/']]
    """A seed hash that will be displayed on the file select screen."""

    Locations: typ.Required[MarsschemamfLocations]
    """Specifies how the item locations in the game should be changed."""

    RequiredMetroidCount: typ.Required[typ.Annotated[int, '0 <= value <= 20']]
    """The number of infant Metroids that must be collected to beat the game."""

    StartingLocation: MarsschemamfStartinglocation
    """The location the player should spawn at the start of the game."""

    StartingItems: MarsschemamfStartingitems = None
    TankIncrements: MarsschemamfTankincrements = None
    """How much ammo/health tanks provide when collected."""

    ElevatorConnections: MarsschemamfElevatorconnections
    """Defines the elevator that each elevator connects to."""

    SectorShortcuts: MarsschemamfSectorshortcuts
    """Defines the sector that each sector shortcut connects to."""

    DoorLocks: list[MarsschemamfDoorlocksItem]
    """List of all lockable doors and their lock type."""

    Palettes: MarsschemamfPalettes = None
    """Properties for randomized in-game palettes."""

    NavigationText: dict[Validlanguages, MarsschemamfNavigationtext] = None
    """Specifies text to be displayed at navigation rooms and the ship."""

    TitleText: list[MarsschemamfTitletextItem] = None
    """Lines of ascii text to write to the title screen."""

    CreditsText: list[MarsschemamfCreditstextItem]
    """Lines of text to insert into the credits."""

    NavStationLocks: dict[MarsschemamfNavstationlocksKey, Hintlocks]
    """Sets the required Security Levels for accessing Navigation Terminals."""

    DisableDemos: bool = False
    """Disables title screen demos when true."""

    SkipDoorTransitions: bool = False
    """Makes all door transitions instant when true."""

    StereoDefault: bool = True
    """Forces stereo sound by default when true."""

    DisableMusic: bool = False
    """Disables all music tracks when true."""

    DisableSoundEffects: bool = False
    """Disables all sound effects when true."""

    MissileLimit: Typeu8 = 3
    """Changes how many missiles can be on-screen at a time. The vanilla game has it set to 2, the randomizer changes it to 3 by default. Zero Mission uses 4."""

    UnexploredMap: bool = False
    """When enabled, starts you with a map where all unexplored items and non-visited tiles have a gray background. This is different from the downloaded map stations where there, the full tile is gray."""

    PowerBombsWithoutBombs: bool = False
    """When enabled, lets you use Power Bombs without needing to collect Bomb Data."""

    AccessibilityPatches: bool = False
    """Whether to apply patches for better accessibility."""

    LevelEdits: dict[Areaidkey, dict[str, MarsschemamfLeveledits]]
    """Specifies room edits that should be done. These will be applied last."""

    MinimapEdits: dict[Minimapidkey, list[MarsschemamfMinimapeditsItem]]
    """Specifies minimap edits that should be done."""

    HideDoorsOnMinimap: bool = False
    """When enabled, hides doors on the minimap. This is automatically enabled when the 'DoorLocks' field is provided."""

    RoomNames: typ.Annotated[list[MarsschemamfRoomnamesItem], 'Unique items']
    """Specifies a name to be displayed when the A Button is pressed on the pause menu."""

    RevealHiddenTiles: bool = False
    """When enabled, reveals normally hidden blocks that are breakable by upgrades. Hidden pickup tanks are not revealed regardless of this setting."""

MarsSchemaMF: typ.TypeAlias = Marsschemamf
