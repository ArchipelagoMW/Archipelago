from enum import Enum, Flag, auto
from typing import TYPE_CHECKING, NamedTuple, Optional

from BaseClasses import Location, Region

if TYPE_CHECKING:
    from .randomizers.Dungeons import Dungeon


class TWWFlag(Flag):
    """
    This class represents flags used for categorizing game locations.
    Flags are used to group locations by their specific gameplay or logic attributes.
    """

    ALWAYS = auto()
    DUNGEON = auto()
    TNGL_CT = auto()
    DG_SCRT = auto()
    PZL_CVE = auto()
    CBT_CVE = auto()
    SAVAGE = auto()
    GRT_FRY = auto()
    SHRT_SQ = auto()
    LONG_SQ = auto()
    SPOILS = auto()
    MINIGME = auto()
    SPLOOSH = auto()
    FREE_GF = auto()
    MAILBOX = auto()
    PLTFRMS = auto()
    SUBMRIN = auto()
    EYE_RFS = auto()
    BG_OCTO = auto()
    TRI_CHT = auto()
    TRE_CHT = auto()
    XPENSVE = auto()
    ISLND_P = auto()
    MISCELL = auto()
    BOSS = auto()
    OTHER = auto()


class TWWLocationType(Enum):
    """
    This class defines constants for various types of locations in The Wind Waker.
    """

    CHART = auto()
    BOCTO = auto()
    CHEST = auto()
    SWTCH = auto()
    PCKUP = auto()
    EVENT = auto()
    SPECL = auto()


class TWWLocationData(NamedTuple):
    """
    This class represents the data for a location in The Wind Waker.

    :param code: The unique code identifier for the location.
    :param flags: The flags that categorize the location.
    :param region: The name of the region where the location resides.
    :param stage_id: The ID of the stage where the location resides.
    :param type: The type of the location.
    :param bit: The bit in memory that is associated with the location. This is combined with other location data to
    determine where in memory to determine whether the location has been checked. If the location is a special type,
    this bit is ignored.
    :param address: For certain location types, this variable contains the address of the byte with the check bit for
    that location. Defaults to `None`.
    """

    code: Optional[int]
    flags: TWWFlag
    region: str
    stage_id: int
    type: TWWLocationType
    bit: int
    address: Optional[int] = None


class TWWLocation(Location):
    """
    This class represents a location in The Wind Waker.

    :param player: The ID of the player whose world the location is in.
    :param name: The name of the location.
    :param parent: The location's parent region.
    :param data: The data associated with this location.
    """

    game: str = "The Wind Waker"
    dungeon: Optional["Dungeon"] = None

    def __init__(self, player: int, name: str, parent: Region, data: TWWLocationData):
        address = None if data.code is None else TWWLocation.get_apid(data.code)
        super().__init__(player, name, address=address, parent=parent)

        self.code = data.code
        self.flags = data.flags
        self.region = data.region
        self.stage_id = data.stage_id
        self.type = data.type
        self.bit = data.bit
        self.address = self.address

    @staticmethod
    def get_apid(code: int) -> int:
        """
        Compute the Archipelago ID for the given location code.

        :param code: The unique code for the location.
        :return: The computed Archipelago ID.
        """
        base_id: int = 2326528
        return base_id + code


DUNGEON_NAMES = [
    "Dragon Roost Cavern",
    "Forbidden Woods",
    "Tower of the Gods",
    "Forsaken Fortress",
    "Earth Temple",
    "Wind Temple",
]

LOCATION_TABLE: dict[str, TWWLocationData] = {
    # Outset Island
    "Outset Island - Underneath Link's House": TWWLocationData(
        0, TWWFlag.MISCELL, "The Great Sea", 0xB, TWWLocationType.CHEST, 5
    ),
    "Outset Island - Mesa the Grasscutter's House": TWWLocationData(
        1, TWWFlag.MISCELL, "The Great Sea", 0xB, TWWLocationType.CHEST, 4
    ),
    "Outset Island - Orca - Give 10 Knight's Crests": TWWLocationData(
        2, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 5, 0x803C5237
    ),
    # "Outset Island - Orca - Hit 500 Times": TWWLocationData(
    #     3, TWWFlag.OTHER, "The Great Sea"
    # ),
    "Outset Island - Great Fairy": TWWLocationData(
        4, TWWFlag.GRT_FRY, "The Great Sea", 0xC, TWWLocationType.EVENT, 4, 0x803C525C
    ),
    "Outset Island - Jabun's Cave": TWWLocationData(
        5, TWWFlag.ISLND_P, "The Great Sea", 0xB, TWWLocationType.CHEST, 6
    ),
    "Outset Island - Dig up Black Soil": TWWLocationData(
        6, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.PCKUP, 2
    ),
    "Outset Island - Savage Labyrinth - Floor 30": TWWLocationData(
        7, TWWFlag.SAVAGE, "Savage Labyrinth", 0xD, TWWLocationType.CHEST, 11
    ),
    "Outset Island - Savage Labyrinth - Floor 50": TWWLocationData(
        8, TWWFlag.SAVAGE, "Savage Labyrinth", 0xD, TWWLocationType.CHEST, 12
    ),

    # Windfall Island
    "Windfall Island - Jail - Tingle - First Gift": TWWLocationData(
        9, TWWFlag.FREE_GF, "The Great Sea", 0xB, TWWLocationType.SWTCH, 53
    ),
    "Windfall Island - Jail - Tingle - Second Gift": TWWLocationData(
        10, TWWFlag.FREE_GF, "The Great Sea", 0xB, TWWLocationType.SWTCH, 54
    ),
    "Windfall Island - Jail - Maze Chest": TWWLocationData(
        11, TWWFlag.ISLND_P, "The Great Sea", 0xB, TWWLocationType.CHEST, 0
    ),
    "Windfall Island - Chu Jelly Juice Shop - Give 15 Green Chu Jelly": TWWLocationData(
        12, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 2, 0x803C5239
    ),
    "Windfall Island - Chu Jelly Juice Shop - Give 15 Blue Chu Jelly": TWWLocationData(
        13, TWWFlag.SPOILS | TWWFlag.LONG_SQ, "The Great Sea", 0xB, TWWLocationType.EVENT, 1, 0x803C5239
    ),
    "Windfall Island - Ivan - Catch Killer Bees": TWWLocationData(
        14, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 6, 0x803C523F
    ),
    "Windfall Island - Mrs. Marie - Catch Killer Bees": TWWLocationData(
        15, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.EVENT, 7, 0x803C524B
    ),
    "Windfall Island - Mrs. Marie - Give 1 Joy Pendant": TWWLocationData(
        16, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C52EC
    ),
    "Windfall Island - Mrs. Marie - Give 21 Joy Pendants": TWWLocationData(
        17, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 3, 0x803C5248
    ),
    "Windfall Island - Mrs. Marie - Give 40 Joy Pendants": TWWLocationData(
        18, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 2, 0x803C5248
    ),
    "Windfall Island - Lenzo's House - Left Chest": TWWLocationData(
        19, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.CHEST, 1
    ),
    "Windfall Island - Lenzo's House - Right Chest": TWWLocationData(
        20, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.CHEST, 2
    ),
    "Windfall Island - Lenzo's House - Become Lenzo's Assistant": TWWLocationData(
        21, TWWFlag.LONG_SQ, "The Great Sea", 0xB, TWWLocationType.SPECL, 0, 0x803C52F0
    ),
    "Windfall Island - Lenzo's House - Bring Forest Firefly": TWWLocationData(
        22, TWWFlag.LONG_SQ, "The Great Sea", 0xB, TWWLocationType.EVENT, 5, 0x803C5295
    ),
    "Windfall Island - House of Wealth Chest": TWWLocationData(
        23, TWWFlag.MISCELL, "The Great Sea", 0xB, TWWLocationType.CHEST, 3
    ),
    "Windfall Island - Maggie's Father - Give 20 Skull Necklaces": TWWLocationData(
        24, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 4, 0x803C52F1
    ),
    "Windfall Island - Maggie - Free Item": TWWLocationData(
        25, TWWFlag.FREE_GF, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C5296
    ),
    "Windfall Island - Maggie - Delivery Reward": TWWLocationData(
        # TODO: Where is the flag for this location. Using a temporary workaround for now.
        26, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.SPECL, 0
    ),
    "Windfall Island - Cafe Bar - Postman": TWWLocationData(
        27, TWWFlag.SHRT_SQ, "The Great Sea", 0xB, TWWLocationType.EVENT, 1, 0x803C5296
    ),
    "Windfall Island - Kreeb - Light Up Lighthouse": TWWLocationData(
        28, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 5, 0x803C5247
    ),
    "Windfall Island - Transparent Chest": TWWLocationData(
        29, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.CHEST, 10
    ),
    "Windfall Island - Tott - Teach Rhythm": TWWLocationData(
        30, TWWFlag.FREE_GF, "The Great Sea", 0x0, TWWLocationType.EVENT, 6, 0x803C5238
    ),
    "Windfall Island - Pirate Ship": TWWLocationData(
        31, TWWFlag.MINIGME, "The Great Sea", 0xD, TWWLocationType.CHEST, 5
    ),
    "Windfall Island - 5 Rupee Auction": TWWLocationData(
        32, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea", 0xB, TWWLocationType.EVENT, 7, 0x803C523C
    ),
    "Windfall Island - 40 Rupee Auction": TWWLocationData(
        33, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C523B
    ),
    "Windfall Island - 60 Rupee Auction": TWWLocationData(
        34, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea", 0xB, TWWLocationType.EVENT, 6, 0x803C523C
    ),
    "Windfall Island - 80 Rupee Auction": TWWLocationData(
        35, TWWFlag.XPENSVE | TWWFlag.MINIGME, "The Great Sea", 0xB, TWWLocationType.EVENT, 5, 0x803C523C
    ),
    "Windfall Island - Zunari - Stock Exotic Flower in Zunari's Shop": TWWLocationData(
        36, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 6, 0x803C5295
    ),
    "Windfall Island - Sam - Decorate the Town": TWWLocationData(
        37, TWWFlag.LONG_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 4, 0x803C5247
    ),
    # "Windfall Island - Kane - Place Shop Guru Statue on Gate": TWWLocationData(
    #     38, TWWFlag.OTHER, "The Great Sea", 0x0, TWWLocationType.EVENT, 4, 0x803C5250
    # ),
    # "Windfall Island - Kane - Place Postman Statue on Gate": TWWLocationData(
    #     39, TWWFlag.OTHER, "The Great Sea", 0x0, TWWLocationType.EVENT, 3, 0x803C5250
    # ),
    # "Windfall Island - Kane - Place Six Flags on Gate": TWWLocationData(
    #     40, TWWFlag.OTHER, "The Great Sea", 0x0, TWWLocationType.EVENT, 2, 0x803C5250
    # ),
    # "Windfall Island - Kane - Place Six Idols on Gate": TWWLocationData(
    #     41, TWWFlag.OTHER, "The Great Sea", 0x0, TWWLocationType.EVENT, 1, 0x803C5250
    # ),
    "Windfall Island - Mila - Follow the Thief": TWWLocationData(
        42, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 3, 0x803C523A
    ),
    "Windfall Island - Battlesquid - First Prize": TWWLocationData(
        43, TWWFlag.SPLOOSH, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C532A
    ),
    "Windfall Island - Battlesquid - Second Prize": TWWLocationData(
        44, TWWFlag.SPLOOSH, "The Great Sea", 0xB, TWWLocationType.EVENT, 1, 0x803C532A
    ),
    "Windfall Island - Battlesquid - Under 20 Shots Prize": TWWLocationData(
        45, TWWFlag.SPLOOSH, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C532B
    ),
    "Windfall Island - Pompie and Vera - Secret Meeting Photo": TWWLocationData(
        46, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 2, 0x803C5295
    ),
    "Windfall Island - Kamo - Full Moon Photo": TWWLocationData(
        47, TWWFlag.LONG_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 4, 0x803C5295
    ),
    "Windfall Island - Minenco - Miss Windfall Photo": TWWLocationData(
        48, TWWFlag.SHRT_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 3, 0x803C5295
    ),
    "Windfall Island - Linda and Anton": TWWLocationData(
        49, TWWFlag.LONG_SQ, "The Great Sea", 0xB, TWWLocationType.EVENT, 7, 0x803C524E
    ),

    # Dragon Roost Island
    "Dragon Roost Island - Wind Shrine": TWWLocationData(
        50, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.EVENT, 3, 0x803C5253
    ),
    "Dragon Roost Island - Rito Aerie - Give Hoskit 20 Golden Feathers": TWWLocationData(
        51, TWWFlag.SPOILS, "The Great Sea", 0xB, TWWLocationType.EVENT, 7, 0x803C524D
    ),
    "Dragon Roost Island - Chest on Top of Boulder": TWWLocationData(
        52, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 8
    ),
    "Dragon Roost Island - Fly Across Platforms Around Island": TWWLocationData(
        53, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 9
    ),
    "Dragon Roost Island - Rito Aerie - Mail Sorting": TWWLocationData(
        54, TWWFlag.MINIGME, "The Great Sea", 0xB, TWWLocationType.EVENT, 0, 0x803C5253
    ),
    "Dragon Roost Island - Secret Cave": TWWLocationData(
        55, TWWFlag.CBT_CVE, "Dragon Roost Island Secret Cave", 0xD, TWWLocationType.CHEST, 0
    ),

    # Dragon Roost Cavern
    "Dragon Roost Cavern - First Room": TWWLocationData(
        56, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 0
    ),
    "Dragon Roost Cavern - Alcove With Water Jugs": TWWLocationData(
        57, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 2
    ),
    "Dragon Roost Cavern - Water Jug on Upper Shelf": TWWLocationData(
        58, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 1
    ),
    "Dragon Roost Cavern - Boarded Up Chest": TWWLocationData(
        59, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 1
    ),
    "Dragon Roost Cavern - Chest Across Lava Pit": TWWLocationData(
        60, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 13
    ),
    "Dragon Roost Cavern - Rat Room": TWWLocationData(
        61, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 14
    ),
    "Dragon Roost Cavern - Rat Room Boarded Up Chest": TWWLocationData(
        62, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 3
    ),
    "Dragon Roost Cavern - Bird's Nest": TWWLocationData(
        63, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 3
    ),
    "Dragon Roost Cavern - Dark Room": TWWLocationData(
        64, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 4
    ),
    "Dragon Roost Cavern - Tingle Chest in Hub Room": TWWLocationData(
        65, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 16
    ),
    "Dragon Roost Cavern - Pot on Upper Shelf in Pot Room": TWWLocationData(
        66, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 0
    ),
    "Dragon Roost Cavern - Pot Room Chest": TWWLocationData(
        67, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 6
    ),
    "Dragon Roost Cavern - Miniboss": TWWLocationData(
        68, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 17
    ),
    "Dragon Roost Cavern - Under Rope Bridge": TWWLocationData(
        69, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 7
    ),
    "Dragon Roost Cavern - Tingle Statue Chest": TWWLocationData(
        70, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 15
    ),
    "Dragon Roost Cavern - Big Key Chest": TWWLocationData(
        71, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 12
    ),
    "Dragon Roost Cavern - Boss Stairs Right Chest": TWWLocationData(
        72, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 11
    ),
    "Dragon Roost Cavern - Boss Stairs Left Chest": TWWLocationData(
        73, TWWFlag.DUNGEON, "Dragon Roost Cavern", 0x3, TWWLocationType.CHEST, 10
    ),
    "Dragon Roost Cavern - Boss Stairs Right Pot": TWWLocationData(
        74, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Dragon Roost Cavern", 0x3, TWWLocationType.PCKUP, 6
    ),
    "Dragon Roost Cavern - Gohma Heart Container": TWWLocationData(
        75, TWWFlag.DUNGEON | TWWFlag.BOSS, "Gohma Boss Arena", 0x3, TWWLocationType.PCKUP, 21
    ),

    # Forest Haven
    "Forest Haven - On Tree Branch": TWWLocationData(
        76, TWWFlag.ISLND_P, "The Great Sea", 0xB, TWWLocationType.PCKUP, 2
    ),
    "Forest Haven - Small Island Chest": TWWLocationData(
        77, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 7
    ),

    # Forbidden Woods
    "Forbidden Woods - First Room": TWWLocationData(
        78, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 0
    ),
    "Forbidden Woods - Inside Hollow Tree's Mouth": TWWLocationData(
        79, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 1
    ),
    "Forbidden Woods - Climb to Top Using Boko Baba Bulbs": TWWLocationData(
        80, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 2
    ),
    "Forbidden Woods - Pot High Above Hollow Tree": TWWLocationData(
        81, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Forbidden Woods", 0x4, TWWLocationType.PCKUP, 1
    ),
    "Forbidden Woods - Hole in Tree": TWWLocationData(
        82, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 6
    ),
    "Forbidden Woods - Morth Pit": TWWLocationData(
        83, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 8
    ),
    "Forbidden Woods - Vine Maze Left Chest": TWWLocationData(
        84, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 7
    ),
    "Forbidden Woods - Vine Maze Right Chest": TWWLocationData(
        85, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 5
    ),
    "Forbidden Woods - Highest Pot in Vine Maze": TWWLocationData(
        86, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Forbidden Woods", 0x4, TWWLocationType.PCKUP, 22
    ),
    "Forbidden Woods - Tall Room Before Miniboss": TWWLocationData(
        87, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 12
    ),
    "Forbidden Woods - Mothula Miniboss Room": TWWLocationData(
        88, TWWFlag.DUNGEON, "Forbidden Woods Miniboss Arena", 0x4, TWWLocationType.CHEST, 10
    ),
    "Forbidden Woods - Past Seeds Hanging by Vines": TWWLocationData(
        89, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 3
    ),
    "Forbidden Woods - Chest Across Red Hanging Flower": TWWLocationData(
        90, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 11
    ),
    "Forbidden Woods - Tingle Statue Chest": TWWLocationData(
        91, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 15
    ),
    "Forbidden Woods - Chest in Locked Tree Trunk": TWWLocationData(
        92, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 9
    ),
    "Forbidden Woods - Big Key Chest": TWWLocationData(
        93, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 4
    ),
    "Forbidden Woods - Double Mothula Room": TWWLocationData(
        94, TWWFlag.DUNGEON, "Forbidden Woods", 0x4, TWWLocationType.CHEST, 14
    ),
    "Forbidden Woods - Kalle Demos Heart Container": TWWLocationData(
        95, TWWFlag.DUNGEON | TWWFlag.BOSS, "Kalle Demos Boss Arena", 0x4, TWWLocationType.PCKUP, 21
    ),

    # Greatfish Isle
    "Greatfish Isle - Hidden Chest": TWWLocationData(
        96, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 6
    ),

    # Tower of the Gods
    "Tower of the Gods - Chest Behind Bombable Walls": TWWLocationData(
        97, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 2
    ),
    "Tower of the Gods - Pot Behind Bombable Walls": TWWLocationData(
        98, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Tower of the Gods", 0x5, TWWLocationType.PCKUP, 0
    ),
    "Tower of the Gods - Hop Across Floating Boxes": TWWLocationData(
        99, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 1
    ),
    "Tower of the Gods - Light Two Torches": TWWLocationData(
        100, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 10
    ),
    "Tower of the Gods - Skulls Room Chest": TWWLocationData(
        101, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 3
    ),
    "Tower of the Gods - Shoot Eye Above Skulls Room Chest": TWWLocationData(
        102, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 9
    ),
    "Tower of the Gods - Tingle Statue Chest": TWWLocationData(
        103, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 15
    ),
    "Tower of the Gods - First Chest Guarded by Armos Knights": TWWLocationData(
        104, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 6
    ),
    "Tower of the Gods - Stone Tablet": TWWLocationData(
        105, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.EVENT, 4, 0x803C5251
    ),
    "Tower of the Gods - Darknut Miniboss Room": TWWLocationData(
        106, TWWFlag.DUNGEON, "Tower of the Gods Miniboss Arena", 0x5, TWWLocationType.CHEST, 5
    ),
    "Tower of the Gods - Second Chest Guarded by Armos Knights": TWWLocationData(
        107, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 8
    ),
    "Tower of the Gods - Floating Platforms Room": TWWLocationData(
        108, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 4
    ),
    "Tower of the Gods - Top of Floating Platforms Room": TWWLocationData(
        109, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 11
    ),
    "Tower of the Gods - Eastern Pot in Big Key Chest Room": TWWLocationData(
        110, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Tower of the Gods", 0x5, TWWLocationType.PCKUP, 1
    ),
    "Tower of the Gods - Big Key Chest": TWWLocationData(
        111, TWWFlag.DUNGEON, "Tower of the Gods", 0x5, TWWLocationType.CHEST, 0
    ),
    "Tower of the Gods - Gohdan Heart Container": TWWLocationData(
        112, TWWFlag.DUNGEON | TWWFlag.BOSS, "Gohdan Boss Arena", 0x5, TWWLocationType.PCKUP, 21
    ),

    # Hyrule
    "Hyrule - Master Sword Chamber": TWWLocationData(
        113, TWWFlag.DUNGEON, "Master Sword Chamber", 0x9, TWWLocationType.CHEST, 0
    ),

    # Forsaken Fortress
    "Forsaken Fortress - Phantom Ganon": TWWLocationData(
        114, TWWFlag.DUNGEON, "The Great Sea", 0x0, TWWLocationType.CHEST, 16
    ),
    "Forsaken Fortress - Chest Outside Upper Jail Cell": TWWLocationData(
        115, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 0
    ),
    "Forsaken Fortress - Chest Inside Lower Jail Cell": TWWLocationData(
        116, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 3
    ),
    "Forsaken Fortress - Chest Guarded By Bokoblin": TWWLocationData(
        117, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 2
    ),
    "Forsaken Fortress - Chest on Bed": TWWLocationData(
        118, TWWFlag.DUNGEON, "The Great Sea", 0x2, TWWLocationType.CHEST, 1
    ),
    "Forsaken Fortress - Helmaroc King Heart Container": TWWLocationData(
        119, TWWFlag.DUNGEON | TWWFlag.BOSS, "Helmaroc King Boss Arena", 0x2, TWWLocationType.PCKUP, 21
    ),

    # Mother and Child Isles
    "Mother and Child Isles - Inside Mother Isle": TWWLocationData(
        120, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.CHEST, 28
    ),

    # Fire Mountain
    "Fire Mountain - Cave - Chest": TWWLocationData(
        121, TWWFlag.PZL_CVE | TWWFlag.CBT_CVE, "Fire Mountain Secret Cave", 0xC, TWWLocationType.CHEST, 0
    ),
    "Fire Mountain - Lookout Platform Chest": TWWLocationData(
        122, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 1
    ),
    "Fire Mountain - Lookout Platform - Destroy the Cannons": TWWLocationData(
        123, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 0
    ),
    "Fire Mountain - Big Octo": TWWLocationData(
        124, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51F0
    ),

    # Ice Ring Isle
    "Ice Ring Isle - Frozen Chest": TWWLocationData(
        125, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 18
    ),
    "Ice Ring Isle - Cave - Chest": TWWLocationData(
        126, TWWFlag.PZL_CVE, "Ice Ring Isle Secret Cave", 0xC, TWWLocationType.CHEST, 1
    ),
    "Ice Ring Isle - Inner Cave - Chest": TWWLocationData(
        127, TWWFlag.PZL_CVE | TWWFlag.CBT_CVE, "Ice Ring Isle Inner Cave", 0xC, TWWLocationType.CHEST, 21
    ),

    # Headstone Island
    "Headstone Island - Top of the Island": TWWLocationData(
        128, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.PCKUP, 8
    ),
    "Headstone Island - Submarine": TWWLocationData(
        129, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 4
    ),

    # Earth Temple
    "Earth Temple - Transparent Chest In Warp Pot Room": TWWLocationData(
        130, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 0
    ),
    "Earth Temple - Behind Curtain In Warp Pot Room": TWWLocationData(
        131, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Earth Temple", 0x6, TWWLocationType.PCKUP, 0
    ),
    "Earth Temple - Transparent Chest in First Crypt": TWWLocationData(
        132, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 1
    ),
    "Earth Temple - Chest Behind Destructible Walls": TWWLocationData(
        133, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 12
    ),
    "Earth Temple - Chest In Three Blocks Room": TWWLocationData(
        134, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 2
    ),
    "Earth Temple - Chest Behind Statues": TWWLocationData(
        135, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 3
    ),
    "Earth Temple - Casket in Second Crypt": TWWLocationData(
        136, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.PCKUP, 14
    ),
    "Earth Temple - Stalfos Miniboss Room": TWWLocationData(
        137, TWWFlag.DUNGEON, "Earth Temple Miniboss Arena", 0x6, TWWLocationType.CHEST, 7
    ),
    "Earth Temple - Tingle Statue Chest": TWWLocationData(
        138, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 15
    ),
    "Earth Temple - End of Foggy Room With Floormasters": TWWLocationData(
        139, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 4
    ),
    "Earth Temple - Kill All Floormasters in Foggy Room": TWWLocationData(
        140, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 11
    ),
    "Earth Temple - Behind Curtain Next to Hammer Button": TWWLocationData(
        141, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Earth Temple", 0x6, TWWLocationType.PCKUP, 1
    ),
    "Earth Temple - Chest in Third Crypt": TWWLocationData(
        142, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 5
    ),
    "Earth Temple - Many Mirrors Room Right Chest": TWWLocationData(
        143, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 9
    ),
    "Earth Temple - Many Mirrors Room Left Chest": TWWLocationData(
        144, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 10
    ),
    "Earth Temple - Stalfos Crypt Room": TWWLocationData(
        145, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 14
    ),
    "Earth Temple - Big Key Chest": TWWLocationData(
        146, TWWFlag.DUNGEON, "Earth Temple", 0x6, TWWLocationType.CHEST, 6
    ),
    "Earth Temple - Jalhalla Heart Container": TWWLocationData(
        147, TWWFlag.DUNGEON | TWWFlag.BOSS, "Jalhalla Boss Arena", 0x6, TWWLocationType.PCKUP, 21
    ),

    # Wind Temple
    "Wind Temple - Chest Between Two Dirt Patches": TWWLocationData(
        148, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 0
    ),
    "Wind Temple - Behind Stone Head in Hidden Upper Room": TWWLocationData(
        149, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Wind Temple", 0x7, TWWLocationType.PCKUP, 0
    ),
    "Wind Temple - Tingle Statue Chest": TWWLocationData(
        150, TWWFlag.TNGL_CT | TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 15
    ),
    "Wind Temple - Chest Behind Stone Head": TWWLocationData(
        151, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 3
    ),
    "Wind Temple - Chest in Left Alcove": TWWLocationData(
        152, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 7
    ),
    "Wind Temple - Big Key Chest": TWWLocationData(
        153, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 8
    ),
    "Wind Temple - Chest In Many Cyclones Room": TWWLocationData(
        154, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 11
    ),
    "Wind Temple - Behind Stone Head in Many Cyclones Room": TWWLocationData(
        155, TWWFlag.DUNGEON | TWWFlag.DG_SCRT, "Wind Temple", 0x7, TWWLocationType.PCKUP, 1
    ),
    "Wind Temple - Chest In Middle Of Hub Room": TWWLocationData(
        156, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 13
    ),
    "Wind Temple - Spike Wall Room - First Chest": TWWLocationData(
        157, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 9
    ),
    "Wind Temple - Spike Wall Room - Destroy All Cracked Floors": TWWLocationData(
        158, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 10
    ),
    "Wind Temple - Wizzrobe Miniboss Room": TWWLocationData(
        159, TWWFlag.DUNGEON, "Wind Temple Miniboss Arena", 0x7, TWWLocationType.CHEST, 5
    ),
    "Wind Temple - Chest at Top of Hub Room": TWWLocationData(
        160, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 2
    ),
    "Wind Temple - Chest Behind Seven Armos": TWWLocationData(
        161, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 4
    ),
    "Wind Temple - Kill All Enemies in Tall Basement Room": TWWLocationData(
        162, TWWFlag.DUNGEON, "Wind Temple", 0x7, TWWLocationType.CHEST, 12
    ),
    "Wind Temple - Molgera Heart Container": TWWLocationData(
        163, TWWFlag.DUNGEON | TWWFlag.BOSS, "Molgera Boss Arena", 0x7, TWWLocationType.PCKUP, 21
    ),

    # Ganon's Tower
    "Ganon's Tower - Maze Chest": TWWLocationData(
        164, TWWFlag.DUNGEON, "The Great Sea", 0x8, TWWLocationType.CHEST, 0
    ),

    # Mailbox
    "Mailbox - Letter from Hoskit's Girlfriend": TWWLocationData(
        165, TWWFlag.MAILBOX | TWWFlag.SPOILS, "The Great Sea", 0x0, TWWLocationType.SPECL, 0, 0x803C52DA
    ),
    "Mailbox - Letter from Baito's Mother": TWWLocationData(
        166, TWWFlag.MAILBOX, "The Great Sea", 0x0, TWWLocationType.SPECL, 0, 0x803C52D8
    ),
    "Mailbox - Letter from Baito": TWWLocationData(
        167, TWWFlag.MAILBOX | TWWFlag.DUNGEON, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52A8
    ),
    "Mailbox - Letter from Komali's Father": TWWLocationData(
        168, TWWFlag.MAILBOX, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52E1
    ),
    "Mailbox - Letter Advertising Bombs in Beedle's Shop": TWWLocationData(
        169, TWWFlag.MAILBOX, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52A9
    ),
    "Mailbox - Letter Advertising Rock Spire Shop Ship": TWWLocationData(
        170, TWWFlag.MAILBOX, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52A6
    ),
    # "Mailbox - Beedle's Silver Membership Reward": TWWLocationData(
    #     171, TWWFlag.OTHER, "The Great Sea"
    # ),
    # "Mailbox - Beedle's Gold Membership Reward": TWWLocationData(
    #     172, TWWFlag.OTHER, "The Great Sea"
    # ),
    "Mailbox - Letter from Orca": TWWLocationData(
        173, TWWFlag.MAILBOX | TWWFlag.DUNGEON, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52A7
    ),
    "Mailbox - Letter from Grandma": TWWLocationData(
        174, TWWFlag.MAILBOX, "The Great Sea", 0x0, TWWLocationType.SPECL, 0, 0x803C52C9
    ),
    "Mailbox - Letter from Aryll": TWWLocationData(
        175, TWWFlag.MAILBOX | TWWFlag.DUNGEON, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52B7
    ),
    "Mailbox - Letter from Tingle": TWWLocationData(
        176,
        TWWFlag.MAILBOX | TWWFlag.DUNGEON | TWWFlag.XPENSVE, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52DE
    ),

    # The Great Sea
    "The Great Sea - Beedle's Shop Ship - 20 Rupee Item": TWWLocationData(
        177, TWWFlag.MISCELL, "The Great Sea",  0xA, TWWLocationType.EVENT, 1, 0x803C5295
    ),
    "The Great Sea - Salvage Corp Gift": TWWLocationData(
        178, TWWFlag.FREE_GF, "The Great Sea", 0x0, TWWLocationType.EVENT, 7, 0x803C5295
    ),
    "The Great Sea - Cyclos": TWWLocationData(
        179, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.EVENT, 4, 0x803C5253
    ),
    "The Great Sea - Goron Trading Reward": TWWLocationData(
        180, TWWFlag.LONG_SQ | TWWFlag.XPENSVE, "The Great Sea", 0x0, TWWLocationType.EVENT, 2, 0x803C526A
    ),
    "The Great Sea - Withered Trees": TWWLocationData(
        181, TWWFlag.LONG_SQ, "The Great Sea", 0x0, TWWLocationType.EVENT, 5, 0x803C525A
    ),
    "The Great Sea - Ghost Ship": TWWLocationData(
        182, TWWFlag.MISCELL, "The Great Sea", 0xA, TWWLocationType.CHEST, 23
    ),

    # Private Oasis
    "Private Oasis - Chest at Top of Waterfall": TWWLocationData(
        183, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 19
    ),
    "Private Oasis - Cabana Labyrinth - Lower Floor Chest": TWWLocationData(
        184, TWWFlag.PZL_CVE, "Cabana Labyrinth", 0xC, TWWLocationType.CHEST, 22
    ),
    "Private Oasis - Cabana Labyrinth - Upper Floor Chest": TWWLocationData(
        185, TWWFlag.PZL_CVE, "Cabana Labyrinth", 0xC, TWWLocationType.CHEST, 17
    ),
    "Private Oasis - Big Octo": TWWLocationData(
        186, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C520A
    ),

    # Spectacle Island
    "Spectacle Island - Barrel Shooting - First Prize": TWWLocationData(
        187, TWWFlag.MINIGME, "The Great Sea", 0x0, TWWLocationType.EVENT, 0, 0x803C52E3
    ),
    "Spectacle Island - Barrel Shooting - Second Prize": TWWLocationData(
        188, TWWFlag.MINIGME, "The Great Sea", 0x0, TWWLocationType.EVENT, 1, 0x803C52E3
    ),

    # Needle Rock Isle
    "Needle Rock Isle - Chest": TWWLocationData(
        189, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 3
    ),
    "Needle Rock Isle - Cave": TWWLocationData(
        190, TWWFlag.PZL_CVE, "Needle Rock Isle Secret Cave", 0xD, TWWLocationType.CHEST, 9
    ),
    "Needle Rock Isle - Golden Gunboat": TWWLocationData(
        191, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 2, 0x803C5202
    ),

    # Angular Isles
    "Angular Isles - Peak": TWWLocationData(
        192, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 0
    ),
    "Angular Isles - Cave": TWWLocationData(
        193, TWWFlag.PZL_CVE, "Angular Isles Secret Cave", 0xD, TWWLocationType.CHEST, 6
    ),

    # Boating Course
    "Boating Course - Raft": TWWLocationData(
        194, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 21
    ),
    "Boating Course - Cave": TWWLocationData(
        195, TWWFlag.PZL_CVE | TWWFlag.CBT_CVE, "Boating Course Secret Cave", 0xD, TWWLocationType.CHEST, 15
    ),

    # Stone Watcher Island
    "Stone Watcher Island - Cave": TWWLocationData(
        196, TWWFlag.CBT_CVE, "Stone Watcher Island Secret Cave", 0xC, TWWLocationType.CHEST, 10
    ),
    "Stone Watcher Island - Lookout Platform Chest": TWWLocationData(
        197, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 18
    ),
    "Stone Watcher Island - Lookout Platform - Destroy the Cannons": TWWLocationData(
        198, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 20
    ),

    # Islet of Steel
    "Islet of Steel - Interior": TWWLocationData(
        199, TWWFlag.MISCELL, "The Great Sea", 0xC, TWWLocationType.CHEST, 4
    ),
    "Islet of Steel - Lookout Platform - Defeat the Enemies": TWWLocationData(
        200, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 16
    ),

    # Overlook Island
    "Overlook Island - Cave": TWWLocationData(
        201, TWWFlag.CBT_CVE, "Overlook Island Secret Cave", 0xC, TWWLocationType.CHEST, 11
    ),

    # Bird's Peak Rock
    "Bird's Peak Rock - Cave": TWWLocationData(
        202, TWWFlag.PZL_CVE, "Bird's Peak Rock Secret Cave", 0xC, TWWLocationType.CHEST, 16
    ),

    # Pawprint Isle
    "Pawprint Isle - Chuchu Cave - Chest": TWWLocationData(
        203, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 26
    ),
    "Pawprint Isle - Chuchu Cave - Behind Left Boulder": TWWLocationData(
        204, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 24
    ),
    "Pawprint Isle - Chuchu Cave - Behind Right Boulder": TWWLocationData(
        205, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 25
    ),
    "Pawprint Isle - Chuchu Cave - Scale the Wall": TWWLocationData(
        206, TWWFlag.PZL_CVE, "Pawprint Isle Chuchu Cave", 0xC, TWWLocationType.CHEST, 2
    ),
    "Pawprint Isle - Wizzrobe Cave": TWWLocationData(
        207, TWWFlag.CBT_CVE, "Pawprint Isle Wizzrobe Cave", 0xD, TWWLocationType.CHEST, 2
    ),
    "Pawprint Isle - Lookout Platform - Defeat the Enemies": TWWLocationData(
        208, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 5
    ),

    # Thorned Fairy Island
    "Thorned Fairy Island - Great Fairy": TWWLocationData(
        209, TWWFlag.GRT_FRY, "Thorned Fairy Fountain", 0xC, TWWLocationType.EVENT, 0, 0x803C525C
    ),
    "Thorned Fairy Island - Northeastern Lookout Platform - Destroy the Cannons": TWWLocationData(
        210, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 14
    ),
    "Thorned Fairy Island - Southwestern Lookout Platform - Defeat the Enemies": TWWLocationData(
        211, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 15
    ),

    # Eastern Fairy Island
    "Eastern Fairy Island - Great Fairy": TWWLocationData(
        212, TWWFlag.GRT_FRY, "Eastern Fairy Fountain", 0xC, TWWLocationType.EVENT, 3, 0x803C525C
    ),
    "Eastern Fairy Island - Lookout Platform - Defeat the Cannons and Enemies": TWWLocationData(
        213, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 10
    ),

    # Western Fairy Island
    "Western Fairy Island - Great Fairy": TWWLocationData(
        214, TWWFlag.GRT_FRY, "Western Fairy Fountain", 0xC, TWWLocationType.EVENT, 1, 0x803C525C
    ),
    "Western Fairy Island - Lookout Platform": TWWLocationData(
        215, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 6
    ),

    # Southern Fairy Island
    "Southern Fairy Island - Great Fairy": TWWLocationData(
        216, TWWFlag.GRT_FRY, "Southern Fairy Fountain", 0xC, TWWLocationType.EVENT, 2, 0x803C525C
    ),
    "Southern Fairy Island - Lookout Platform - Destroy the Northwest Cannons": TWWLocationData(
        217, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 23
    ),
    "Southern Fairy Island - Lookout Platform - Destroy the Southeast Cannons": TWWLocationData(
        218, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 17
    ),

    # Northern Fairy Island
    "Northern Fairy Island - Great Fairy": TWWLocationData(
        219, TWWFlag.GRT_FRY, "Northern Fairy Fountain", 0xC, TWWLocationType.EVENT, 5, 0x803C525C
    ),
    "Northern Fairy Island - Submarine": TWWLocationData(
        220, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 6
    ),

    # Tingle Island
    "Tingle Island - Ankle - Reward for All Tingle Statues": TWWLocationData(
        221, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.SPECL, 0
    ),
    "Tingle Island - Big Octo": TWWLocationData(
        222, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51EA
    ),

    # Diamond Steppe Island
    "Diamond Steppe Island - Warp Maze Cave - First Chest": TWWLocationData(
        223, TWWFlag.PZL_CVE, "Diamond Steppe Island Warp Maze Cave", 0xC, TWWLocationType.CHEST, 23
    ),
    "Diamond Steppe Island - Warp Maze Cave - Second Chest": TWWLocationData(
        224, TWWFlag.PZL_CVE, "Diamond Steppe Island Warp Maze Cave", 0xC, TWWLocationType.CHEST, 3
    ),
    "Diamond Steppe Island - Big Octo": TWWLocationData(
        225, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C5210
    ),

    # Bomb Island
    "Bomb Island - Cave": TWWLocationData(
        226, TWWFlag.PZL_CVE, "Bomb Island Secret Cave", 0xC, TWWLocationType.CHEST, 5
    ),
    "Bomb Island - Lookout Platform - Defeat the Enemies": TWWLocationData(
        227, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 3
    ),
    "Bomb Island - Submarine": TWWLocationData(
        228, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 2
    ),

    # Rock Spire Isle
    "Rock Spire Isle - Cave": TWWLocationData(
        229, TWWFlag.CBT_CVE, "Rock Spire Isle Secret Cave", 0xC, TWWLocationType.CHEST, 8
    ),
    "Rock Spire Isle - Beedle's Special Shop Ship - 500 Rupee Item": TWWLocationData(
        230, TWWFlag.XPENSVE, "The Great Sea", 0xA, TWWLocationType.EVENT, 5, 0x803C524C
    ),
    "Rock Spire Isle - Beedle's Special Shop Ship - 950 Rupee Item": TWWLocationData(
        231, TWWFlag.XPENSVE, "The Great Sea", 0xA, TWWLocationType.EVENT, 4, 0x803C524C
    ),
    "Rock Spire Isle - Beedle's Special Shop Ship - 900 Rupee Item": TWWLocationData(
        232, TWWFlag.XPENSVE, "The Great Sea", 0xA, TWWLocationType.EVENT, 3, 0x803C524C
    ),
    "Rock Spire Isle - Western Lookout Platform - Destroy the Cannons": TWWLocationData(
        233, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 23
    ),
    "Rock Spire Isle - Eastern Lookout Platform - Destroy the Cannons": TWWLocationData(
        234, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 24
    ),
    "Rock Spire Isle - Center Lookout Platform": TWWLocationData(
        235, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 25
    ),
    "Rock Spire Isle - Southeast Gunboat": TWWLocationData(
        236, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51E8
    ),

    # Shark Island
    "Shark Island - Cave": TWWLocationData(
        237, TWWFlag.CBT_CVE, "Shark Island Secret Cave", 0xD, TWWLocationType.CHEST, 22
    ),

    # Cliff Plateau Isles
    "Cliff Plateau Isles - Cave": TWWLocationData(
        238, TWWFlag.PZL_CVE, "Cliff Plateau Isles Secret Cave", 0xC, TWWLocationType.CHEST, 7
    ),
    "Cliff Plateau Isles - Highest Isle": TWWLocationData(
        239, TWWFlag.PZL_CVE, "Cliff Plateau Isles Inner Cave", 0x0, TWWLocationType.CHEST, 1
    ),
    "Cliff Plateau Isles - Lookout Platform": TWWLocationData(
        240, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 19
    ),

    # Crescent Moon Island
    "Crescent Moon Island - Chest": TWWLocationData(
        241, TWWFlag.MISCELL, "The Great Sea", 0x0, TWWLocationType.CHEST, 4
    ),
    "Crescent Moon Island - Submarine": TWWLocationData(
        242, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 7
    ),

    # Horseshoe Island
    "Horseshoe Island - Play Golf": TWWLocationData(
        243, TWWFlag.ISLND_P, "The Great Sea", 0x0, TWWLocationType.CHEST, 5
    ),
    "Horseshoe Island - Cave": TWWLocationData(
        244, TWWFlag.CBT_CVE, "Horseshoe Island Secret Cave", 0xD, TWWLocationType.CHEST, 1
    ),
    "Horseshoe Island - Northwestern Lookout Platform": TWWLocationData(
        245, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 26
    ),
    "Horseshoe Island - Southeastern Lookout Platform": TWWLocationData(
        246, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 27
    ),

    # Flight Control Platform
    "Flight Control Platform - Bird-Man Contest - First Prize": TWWLocationData(
        247, TWWFlag.MINIGME, "The Great Sea", 0x0, TWWLocationType.EVENT, 6, 0x803C5257
    ),
    "Flight Control Platform - Submarine": TWWLocationData(
        248, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 3
    ),

    # Star Island
    "Star Island - Cave": TWWLocationData(
        249, TWWFlag.CBT_CVE, "Star Island Secret Cave", 0xC, TWWLocationType.CHEST, 6
    ),
    "Star Island - Lookout Platform": TWWLocationData(
        250, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 4
    ),

    # Star Belt Archipelago
    "Star Belt Archipelago - Lookout Platform": TWWLocationData(
        251, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 11
    ),

    # Five-Star Isles
    "Five-Star Isles - Lookout Platform - Destroy the Cannons": TWWLocationData(
        252, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 2
    ),
    "Five-Star Isles - Raft": TWWLocationData(
        253, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 2
    ),
    "Five-Star Isles - Submarine": TWWLocationData(
        254, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 1
    ),

    # Seven-Star Isles
    "Seven-Star Isles - Center Lookout Platform": TWWLocationData(
        255, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 8
    ),
    "Seven-Star Isles - Northern Lookout Platform": TWWLocationData(
        256, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 7
    ),
    "Seven-Star Isles - Southern Lookout Platform": TWWLocationData(
        257, TWWFlag.PLTFRMS, "The Great Sea", 0x0, TWWLocationType.CHEST, 22
    ),
    "Seven-Star Isles - Big Octo": TWWLocationData(
        258, TWWFlag.BG_OCTO, "The Great Sea", 0x0, TWWLocationType.BOCTO, 0, 0x803C51D4
    ),

    # Cyclops Reef
    "Cyclops Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        259, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 11
    ),
    "Cyclops Reef - Lookout Platform - Defeat the Enemies": TWWLocationData(
        260, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 12
    ),

    # Two-Eye Reef
    "Two-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        261, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 13
    ),
    "Two-Eye Reef - Lookout Platform": TWWLocationData(
        262, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 21
    ),
    "Two-Eye Reef - Big Octo Great Fairy": TWWLocationData(
        263, TWWFlag.BG_OCTO | TWWFlag.GRT_FRY, "The Great Sea", 0x0, TWWLocationType.SWTCH, 52
    ),

    # Three-Eye Reef
    "Three-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        264, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 12
    ),

    # Four-Eye Reef
    "Four-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        265, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 14
    ),

    # Five-Eye Reef
    "Five-Eye Reef - Destroy the Cannons": TWWLocationData(
        266, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 15
    ),
    "Five-Eye Reef - Lookout Platform": TWWLocationData(
        267, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 20
    ),

    # Six-Eye Reef
    "Six-Eye Reef - Destroy the Cannons and Gunboats": TWWLocationData(
        268, TWWFlag.EYE_RFS, "The Great Sea", 0x0, TWWLocationType.CHEST, 17
    ),
    "Six-Eye Reef - Lookout Platform - Destroy the Cannons": TWWLocationData(
        269, TWWFlag.PLTFRMS, "The Great Sea", 0x1, TWWLocationType.CHEST, 13
    ),
    "Six-Eye Reef - Submarine": TWWLocationData(
        270, TWWFlag.SUBMRIN, "The Great Sea", 0xA, TWWLocationType.CHEST, 0
    ),

    # Sunken Treasure
    "Forsaken Fortress Sector - Sunken Treasure": TWWLocationData(
        271, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 8
    ),
    "Star Island - Sunken Treasure": TWWLocationData(
        272, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 18
    ),
    "Northern Fairy Island - Sunken Treasure": TWWLocationData(
        273, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 51
    ),
    "Gale Isle - Sunken Treasure": TWWLocationData(
        274, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 33
    ),
    "Crescent Moon Island - Sunken Treasure": TWWLocationData(
        275, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 40
    ),
    "Seven-Star Isles - Sunken Treasure": TWWLocationData(
        276, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 38
    ),
    "Overlook Island - Sunken Treasure": TWWLocationData(
        277, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 15
    ),
    "Four-Eye Reef - Sunken Treasure": TWWLocationData(
        278, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 12
    ),
    "Mother and Child Isles - Sunken Treasure": TWWLocationData(
        279, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 56
    ),
    "Spectacle Island - Sunken Treasure": TWWLocationData(
        280, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 5
    ),
    "Windfall Island - Sunken Treasure": TWWLocationData(
        281, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 58
    ),
    "Pawprint Isle - Sunken Treasure": TWWLocationData(
        282, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 42
    ),
    "Dragon Roost Island - Sunken Treasure": TWWLocationData(
        283, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 50
    ),
    "Flight Control Platform - Sunken Treasure": TWWLocationData(
        284, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 13
    ),
    "Western Fairy Island - Sunken Treasure": TWWLocationData(
        285, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 10
    ),
    "Rock Spire Isle - Sunken Treasure": TWWLocationData(
        286, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 48
    ),
    "Tingle Island - Sunken Treasure": TWWLocationData(
        287, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 0
    ),
    "Northern Triangle Island - Sunken Treasure": TWWLocationData(
        288, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 11
    ),
    "Eastern Fairy Island - Sunken Treasure": TWWLocationData(
        289, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 62
    ),
    "Fire Mountain - Sunken Treasure": TWWLocationData(
        290, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 9
    ),
    "Star Belt Archipelago - Sunken Treasure": TWWLocationData(
        291, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 17
    ),
    "Three-Eye Reef - Sunken Treasure": TWWLocationData(
        292, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 49
    ),
    "Greatfish Isle - Sunken Treasure": TWWLocationData(
        293, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 32
    ),
    "Cyclops Reef - Sunken Treasure": TWWLocationData(
        294, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 16
    ),
    "Six-Eye Reef - Sunken Treasure": TWWLocationData(
        295, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 52
    ),
    "Tower of the Gods Sector - Sunken Treasure": TWWLocationData(
        296, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 1
    ),
    "Eastern Triangle Island - Sunken Treasure": TWWLocationData(
        297, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 57
    ),
    "Thorned Fairy Island - Sunken Treasure": TWWLocationData(
        298, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 44
    ),
    "Needle Rock Isle - Sunken Treasure": TWWLocationData(
        299, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 60
    ),
    "Islet of Steel - Sunken Treasure": TWWLocationData(
        300, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 54
    ),
    "Stone Watcher Island - Sunken Treasure": TWWLocationData(
        301, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 34
    ),
    "Southern Triangle Island - Sunken Treasure": TWWLocationData(
        302, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 37
    ),
    "Private Oasis - Sunken Treasure": TWWLocationData(
        303, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 55
    ),
    "Bomb Island - Sunken Treasure": TWWLocationData(
        304, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 43
    ),
    "Bird's Peak Rock - Sunken Treasure": TWWLocationData(
        305, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 6
    ),
    "Diamond Steppe Island - Sunken Treasure": TWWLocationData(
        306, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 45
    ),
    "Five-Eye Reef - Sunken Treasure": TWWLocationData(
        307, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 53
    ),
    "Shark Island - Sunken Treasure": TWWLocationData(
        308, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 59
    ),
    "Southern Fairy Island - Sunken Treasure": TWWLocationData(
        309, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 61
    ),
    "Ice Ring Isle - Sunken Treasure": TWWLocationData(
        310, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 7
    ),
    "Forest Haven - Sunken Treasure": TWWLocationData(
        311, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 46
    ),
    "Cliff Plateau Isles - Sunken Treasure": TWWLocationData(
        312, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 36
    ),
    "Horseshoe Island - Sunken Treasure": TWWLocationData(
        313, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 4
    ),
    "Outset Island - Sunken Treasure": TWWLocationData(
        314, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 35
    ),
    "Headstone Island - Sunken Treasure": TWWLocationData(
        315, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 63
    ),
    "Two-Eye Reef - Sunken Treasure": TWWLocationData(
        316, TWWFlag.TRI_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 39
    ),
    "Angular Isles - Sunken Treasure": TWWLocationData(
        317, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 41
    ),
    "Boating Course - Sunken Treasure": TWWLocationData(
        318, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 14
    ),
    "Five-Star Isles - Sunken Treasure": TWWLocationData(
        319, TWWFlag.TRE_CHT, "The Great Sea", 0x0, TWWLocationType.CHART, 47
    ),

    # Defeat Ganondorf
    "Defeat Ganondorf": TWWLocationData(
        None, TWWFlag.ALWAYS, "The Great Sea", 0x8, TWWLocationType.SWTCH, 64
    ),
}


ISLAND_NAME_TO_SALVAGE_BIT: dict[str, int] = {
    "Forsaken Fortress Sector": 8,
    "Star Island": 18,
    "Northern Fairy Island": 51,
    "Gale Isle": 33,
    "Crescent Moon Island": 40,
    "Seven-Star Isles": 38,
    "Overlook Island": 15,
    "Four-Eye Reef": 12,
    "Mother and Child Isles": 56,
    "Spectacle Island": 5,
    "Windfall Island": 58,
    "Pawprint Isle": 42,
    "Dragon Roost Island": 50,
    "Flight Control Platform": 13,
    "Western Fairy Island": 10,
    "Rock Spire Isle": 48,
    "Tingle Island": 0,
    "Northern Triangle Island": 11,
    "Eastern Fairy Island": 62,
    "Fire Mountain": 9,
    "Star Belt Archipelago": 17,
    "Three-Eye Reef": 49,
    "Greatfish Isle": 32,
    "Cyclops Reef": 16,
    "Six-Eye Reef": 52,
    "Tower of the Gods Sector": 1,
    "Eastern Triangle Island": 57,
    "Thorned Fairy Island": 44,
    "Needle Rock Isle": 60,
    "Islet of Steel": 54,
    "Stone Watcher Island": 34,
    "Southern Triangle Island": 37,
    "Private Oasis": 55,
    "Bomb Island": 43,
    "Bird's Peak Rock": 6,
    "Diamond Steppe Island": 45,
    "Five-Eye Reef": 53,
    "Shark Island": 59,
    "Southern Fairy Island": 61,
    "Ice Ring Isle": 7,
    "Forest Haven": 46,
    "Cliff Plateau Isles": 36,
    "Horseshoe Island": 4,
    "Outset Island": 35,
    "Headstone Island": 63,
    "Two-Eye Reef": 39,
    "Angular Isles": 41,
    "Boating Course": 14,
    "Five-Star Isles": 47,
}


def split_location_name_by_zone(location_name: str) -> tuple[str, str]:
    """
    Split a location name into its zone name and specific name.

    :param location_name: The full name of the location.
    :return: A tuple containing the zone and specific name.
    """
    if " - " in location_name:
        zone_name, specific_location_name = location_name.split(" - ", 1)
    else:
        zone_name = specific_location_name = location_name

    return zone_name, specific_location_name
