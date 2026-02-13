# This file is generated. Manual changes will be lost
# fmt: off
# ruff: noqa
# mypy: disable-error-code="misc"
from __future__ import annotations

import typing_extensions as typ


# Definitions
Seed: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 2147483647']
TypeU4: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 15']
TypeU5: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 31']
TypeU8: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 255']
TypeU10: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 1023']
AreaId: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 6']
AreaIdKey = typ.Literal[
    '0',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6'
]
MinimapIdKey = typ.Literal[
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
HueRotation: typ.TypeAlias = typ.Annotated[int, '0 <= value <= 360']
ValidSources = typ.Literal[
    'LONG_BEAM',
    'CHARGE_BEAM',
    'ICE_BEAM',
    'WAVE_BEAM',
    'PLASMA_BEAM',
    'BOMBS',
    'VARIA_SUIT',
    'GRAVITY_SUIT',
    'MORPH_BALL',
    'SPEED_BOOSTER',
    'HI_JUMP',
    'SCREW_ATTACK',
    'SPACE_JUMP',
    'POWER_GRIP',
    'FULLY_POWERED',
    'ZIPLINES'
]
ValidItems = typ.Literal[
    'NONE',
    'ENERGY_TANK',
    'MISSILE_TANK',
    'SUPER_MISSILE_TANK',
    'POWER_BOMB_TANK',
    'LONG_BEAM',
    'CHARGE_BEAM',
    'ICE_BEAM',
    'WAVE_BEAM',
    'PLASMA_BEAM',
    'BOMBS',
    'VARIA_SUIT',
    'GRAVITY_SUIT',
    'MORPH_BALL',
    'SPEED_BOOSTER',
    'HI_JUMP',
    'SCREW_ATTACK',
    'SPACE_JUMP',
    'POWER_GRIP',
    'FULLY_POWERED',
    'ZIPLINES',
    'ICE_TRAP'
]
ValidItemSprites = typ.Literal[
    'DEFAULT',
    'EMPTY',
    'ENERGY_TANK',
    'MISSILE_TANK',
    'SUPER_MISSILE_TANK',
    'POWER_BOMB_TANK',
    'LONG_BEAM',
    'CHARGE_BEAM',
    'ICE_BEAM',
    'WAVE_BEAM',
    'PLASMA_BEAM',
    'BOMBS',
    'VARIA_SUIT',
    'GRAVITY_SUIT',
    'MORPH_BALL',
    'SPEED_BOOSTER',
    'HI_JUMP',
    'SCREW_ATTACK',
    'SPACE_JUMP',
    'POWER_GRIP',
    'FULLY_POWERED',
    'ZIPLINES',
    'ANONYMOUS',
    'SHINY_MISSILE_TANK',
    'SHINY_POWER_BOMB_TANK'
]
ValidAbilities = typ.Literal[
    'LONG_BEAM',
    'CHARGE_BEAM',
    'ICE_BEAM',
    'WAVE_BEAM',
    'PLASMA_BEAM',
    'BOMBS',
    'VARIA_SUIT',
    'GRAVITY_SUIT',
    'MORPH_BALL',
    'SPEED_BOOSTER',
    'HI_JUMP',
    'SCREW_ATTACK',
    'SPACE_JUMP',
    'POWER_GRIP'
]
ValidElevatorTops = typ.Literal[
    'BRINSTAR_TO_KRAID',
    'BRINSTAR_TO_NORFAIR',
    'BRINSTAR_TO_TOURIAN',
    'NORFAIR_TO_RIDLEY',
    'CRATERIA_TO_TOURIAN'
]
ValidElevatorBottoms = typ.Literal[
    'KRAID_TO_BRINSTAR',
    'NORFAIR_TO_BRINSTAR',
    'TOURIAN_TO_BRINSTAR',
    'RIDLEY_TO_NORFAIR',
    'TOURIAN_TO_CRATERIA'
]
ValidLanguages = typ.Literal[
    'JAPANESE_KANJI',
    'JAPANESE_HIRAGANA',
    'ENGLISH',
    'GERMAN',
    'FRENCH',
    'ITALIAN',
    'SPANISH'
]
MessageLanguages: typ.TypeAlias = dict[ValidLanguages, str]

class ItemMessages(typ.TypedDict, total=False):
    kind: typ.Required[ItemMessagesKind]
    languages: MessageLanguages
    centered: bool = True
    message_id: typ.Annotated[int, '0 <= value <= 56']
    """The Message ID, will display one of the predefined messages in the ROM"""

ItemMessagesKind = typ.Literal[
    'CUSTOM_MESSAGE',
    'MESSAGE_ID'
]
Jingle = typ.Literal[
    'DEFAULT',
    'MINOR',
    'MAJOR',
    'UNKNOWN',
    'FULLY_POWERED'
]
HintLocations = typ.Literal[
    'NONE',
    'LONG_BEAM',
    'BOMBS',
    'ICE_BEAM',
    'SPEED_BOOSTER',
    'HIGH_JUMP',
    'VARIA_SUIT',
    'WAVE_BEAM',
    'SCREW_ATTACK'
]

class BlockLayerItem(typ.TypedDict, total=False):
    x: TypeU8
    """The X position in the room that should get edited."""

    y: TypeU8
    """The Y position in the room that should get edited."""

    value: TypeU10
    """The value that should be used to edit the room. For backgrounds, this is calculated via `((Row-1) * ColumnsInTileset) + (Column-1)`."""

BlockLayer: typ.TypeAlias = typ.Annotated[list[BlockLayerItem], 'Unique items']

# Schema entries

class MarsschemazmLocationsMajorLocationsItem(typ.TypedDict):
    source: ValidSources
    """Valid major locations."""

    item: ValidItems
    """Valid items for shuffling."""

    item_messages: typ.NotRequired[ItemMessages]
    jingle: Jingle

class MarsschemazmLocationsMinorLocationsItem(typ.TypedDict):
    area: AreaId
    """The area ID where this item is located."""

    room: TypeU8
    """The room ID where this item is located."""

    block_x: TypeU8
    """The X-coordinate in the room where this item is located."""

    block_y: TypeU8
    """The Y-coordinate in the room where this item is located."""

    item: ValidItems
    """Valid items for shuffling."""

    item_sprite: typ.NotRequired[ValidItemSprites]
    """Valid graphics for item tanks/sprites."""

    item_messages: typ.NotRequired[ItemMessages]
    jingle: Jingle
    hinted_by: typ.NotRequired[HintLocations]
    """The hint location (Chozo statue) that hints to this item's location ('None' if not hinted by anything)."""


class MarsschemazmLocations(typ.TypedDict):
    """Specifies how the item locations in the game should be changed."""

    major_locations: typ.Annotated[list[MarsschemazmLocationsMajorLocationsItem], 'len() == 16', 'Unique items']
    """Specifies how the major item locations should be changed. A major item location is a location where an item is obtained from a sprite or interacting with a device."""

    minor_locations: typ.Annotated[list[MarsschemazmLocationsMinorLocationsItem], 'len() == 100', 'Unique items']
    """Specifies how the minor item locations should be changed. A minor item location is a location where an item is obtained by touching a tank block. _tank clipdata is required at each location, the patcher does not modify any clipdata for minor locations."""


class MarsschemazmStartingLocation(typ.TypedDict):
    """The location the player should spawn at the start of the game."""

    area: AreaId
    """The area ID of the starting location."""

    room: TypeU8
    """The room ID of the starting location."""

    block_x: TypeU8
    """The X-coordinate in the room where the player should spawn. If the room contains a save station, then this value will not be taken into consideration."""

    block_y: TypeU8
    """The Y-coordinate in the room where the player should spawn. If the room contains a save station, then this value will not be taken into consideration."""

MarsschemazmStartingItemsSuitType = typ.Literal[
    'SUITLESS',
    'NORMAL',
    'FULLY_POWERED'
]

class MarsschemazmStartingItems(typ.TypedDict, total=False):
    energy: typ.Annotated[int, '1 <= value <= 1299'] = 99
    """How much energy the player should start with on a new save file."""

    missiles: typ.Annotated[int, '0 <= value <= 999'] = 0
    """How many missiles the player should start with on a new save file."""

    super_missiles: typ.Annotated[int, '0 <= value <= 99'] = 0
    """How many missiles the player should start with on a new save file."""

    power_bombs: typ.Annotated[int, '0 <= value <= 99'] = 0
    """How many power bombs the player should start with on a new save file."""

    abilities: typ.Annotated[list[ValidAbilities], 'Unique items'] = []
    """Which abilities the player should start with on a new save file."""

    downloaded_maps: typ.Annotated[list[AreaId], 'Unique items'] = []
    """Which area maps will be downloaded from the start."""

    suit_type: MarsschemazmStartingItemsSuitType = 'normal'
    """Which suit type the player should start with."""

    ziplines_activated: bool = False
    """Whether the ziplines should be activated from the start."""


class MarsschemazmTankIncrements(typ.TypedDict):
    """How much ammo/health tanks provide when collected."""

    energy_tank: typ.Annotated[int, '-1300 <= value <= 1300'] = 100
    """How much health energy tanks provide when collected."""

    missile_tank: typ.Annotated[int, '-1000 <= value <= 1000'] = 5
    """How much ammo missile tanks provide when collected."""

    super_missile_tank: typ.Annotated[int, '-100 <= value <= 100'] = 2
    """How much ammo super missile tanks provide when collected."""

    power_bomb_tank: typ.Annotated[int, '-100 <= value <= 100'] = 2
    """How much ammo power bomb tanks provide when collected."""


class MarsschemazmElevatorConnections(typ.TypedDict):
    """Defines the elevator that each elevator connects to."""

    elevator_tops: typ.Annotated[dict[ValidElevatorTops, ValidElevatorBottoms], 'len() >= 10']
    """Defines the bottom elevator that each top elevator connects to."""

    elevator_bottoms: typ.Annotated[dict[ValidElevatorBottoms, ValidElevatorTops], 'len() >= 10']
    """Defines the top elevator that each bottom elevator connects to."""

MarsschemazmDoorLocksItemLockType = typ.Literal[
    'OPEN',
    'NORMAL',
    'MISSILE',
    'SUPER_MISSILE',
    'POWER_BOMB',
    'LOCKED'
]

class MarsschemazmDoorLocksItem(typ.TypedDict):
    area: AreaId
    """The area ID where this door is located."""

    door: TypeU8
    """The door ID of this door."""

    lock_type: MarsschemazmDoorLocksItemLockType
    """The type of cover on the hatch."""

MarsschemazmPalettesRandomizeKey = typ.Literal[
    'tilesets',
    'enemies',
    'samus',
    'beams'
]

@typ.final
class MarsschemazmPalettesRandomize(typ.TypedDict, total=False):
    """The range to use for rotating palette hues."""

    hue_min: HueRotation = None
    """The minimum value to use for rotating palette hues. If not specified, the patcher will randomly generate one."""

    hue_max: HueRotation = None
    """The maximum value to use for rotating palette hues. If not specified, the patcher will randomly generate one."""


MarsschemazmPalettesColorSpace = typ.Literal[
    'HSV',
    'OKLAB'
]

@typ.final
class MarsschemazmPalettes(typ.TypedDict, total=False):
    """Properties for randomized in-game palettes."""

    seed: Seed = None
    """A number used to initialize the random number generator for palettes. If not specified, the patcher will randomly generate one."""

    randomize: typ.Required[dict[MarsschemazmPalettesRandomizeKey, MarsschemazmPalettesRandomize]]
    """What kind of palettes should be randomized."""

    color_space: MarsschemazmPalettesColorSpace = 'OKLAB'
    """The color space to use for rotating palette hues."""

    symmetric: bool = True
    """Randomly rotates hues in the positive or negative direction true."""


class MarsschemazmTitleTextItem(typ.TypedDict, total=False):
    text: typ.Annotated[str, '/^[ -~]{0,30}$/']
    """The ASCII text for this line"""

    line_num: typ.Annotated[int, '0 <= value <= 14']
MarsschemazmCreditsTextItemLineType = typ.Literal[
    'BLANK',
    'BLUE',
    'RED',
    'WHITE1',
    'WHITE2'
]

class MarsschemazmCreditsTextItem(typ.TypedDict, total=False):
    line_type: typ.Required[MarsschemazmCreditsTextItemLineType]
    """The color and line height of the text (or blank)."""

    text: typ.Annotated[str, '/^[ -~]{0,34}$/']
    """The ASCII text for this line."""

    blank_lines: TypeU8 = 0
    """Inserts the provided number of blank lines after the text line."""

    centered: bool = True
    """Centers the text horizontally when true."""


@typ.final
class MarsschemazmLevelEdits(typ.TypedDict, total=False):
    """Specifies the Room ID."""

    bg1: BlockLayer
    """The BG1 layer that should be edited."""

    bg2: BlockLayer
    """The BG2 layer that should be edited."""

    clipdata: BlockLayer
    """The Clipdata layer that should be edited."""




class MarsschemazmMinimapEditsItem(typ.TypedDict, total=False):
    x: TypeU5
    """The X position in the minimap that should get edited."""

    y: TypeU5
    """The Y position in the minimap that should get edited."""

    tile: TypeU10
    """The tile value that should be used to edit the minimap."""

    palette: TypeU4
    """The palette row to use for the tile."""

    h_flip: bool = False
    """Whether the tile should be horizontally flipped or not."""

    v_flip: bool = False
    """Whether the tile should be vertically flipped or not."""



class MarsschemazmRoomNamesItem(typ.TypedDict):
    area: AreaId
    """The area ID where this room is located."""

    room: TypeU8 = 0
    """The room ID."""

    name: typ.Annotated[str, 'len() <= 112']
    """Specifies what text should appear for this room. Two lines are available, with an absolute maximum of 56 characters per line, if all characters used are small. Text will auto-wrap if the next word doesn't fit on the line. If the text is too long, it will be truncated.  Use 
 to force a line break. If not provided, will display 'Unknown Room'."""


class Marsschemazm(typ.TypedDict, total=False):
    """
    Metroid Zero Mission patching schema
    
    A json schema describing the input for patching Metroid Zero Mission via mars_patcher.
    """

    seed_hash: typ.Required[typ.Annotated[str, '/^[0-9A-Z]{8}$/']]
    """A seed hash that will be displayed on the file select screen."""

    locations: typ.Required[MarsschemazmLocations]
    """Specifies how the item locations in the game should be changed."""

    starting_location: MarsschemazmStartingLocation
    """The location the player should spawn at the start of the game."""

    starting_items: MarsschemazmStartingItems = None
    tank_increments: MarsschemazmTankIncrements = None
    """How much ammo/health tanks provide when collected."""

    elevator_connections: MarsschemazmElevatorConnections
    """Defines the elevator that each elevator connects to."""

    door_locks: list[MarsschemazmDoorLocksItem]
    """List of all lockable doors and their lock type."""

    palettes: MarsschemazmPalettes = None
    """Properties for randomized in-game palettes."""

    intro_text: dict[ValidLanguages, str] = None
    """Specifies what text should appear during the new game intro."""

    title_text: list[MarsschemazmTitleTextItem] = None
    """Lines of ascii text to write to the title screen."""

    credits_text: list[MarsschemazmCreditsTextItem]
    """Lines of text to insert into the credits."""

    disable_demos: bool = False
    """Disables title screen demos when true."""

    skip_door_transitions: bool = False
    """Makes all door transitions instant when true."""

    stereo_default: bool = True
    """Forces stereo sound by default when true."""

    disable_music: bool = False
    """Disables all music tracks when true."""

    disable_sound_effects: bool = False
    """Disables all sound effects when true."""

    unexplored_map: bool = False
    """When enabled, starts you with a map where all unexplored items and non-visited tiles have a gray background. This is different from the downloaded map stations where there, the full tile is gray."""

    accessibility_patches: bool = False
    """Whether to apply patches for better accessibility."""

    level_edits: dict[AreaIdKey, dict[str, MarsschemazmLevelEdits]]
    """Specifies room edits that should be done. These will be applied last."""

    minimap_edits: dict[MinimapIdKey, list[MarsschemazmMinimapEditsItem]]
    """Specifies minimap edits that should be done."""

    hide_doors_on_minimap: bool = False
    """When enabled, hides doors on the minimap. This is automatically enabled when the 'DoorLocks' field is provided."""

    room_names: typ.Annotated[list[MarsschemazmRoomNamesItem], 'Unique items']
    """Specifies a name to be displayed when the A Button is pressed on the pause menu."""

    reveal_hidden_tiles: bool = False
    """When enabled, reveals normally hidden blocks that are breakable by upgrades. Hidden pickup tanks are not revealed regardless of this setting."""

MarsSchemaZM: typ.TypeAlias = Marsschemazm
