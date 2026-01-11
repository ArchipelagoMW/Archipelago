
from ..Subclasses import PHTransition, EntranceGroups, OPPOSITE_ENTRANCE_GROUPS






ENTRANCE_DATA = {
    # "Name": {
    #   "return_name": str. what to call the vanilla connecting entrance that generates automatically
    #   "entrance": tuple[int, int, int], stage room entrance. If you come from entrance
    #   "exit": tuple[int, int, int], stage room entrance. What the vanilla game sends you on entering
    #   "entrance_region": str. logic region that the entrance is in
    #   "exit_region": str. logic region it leads to in
    #   "coords": tuple[int, int, int]. x, y, z. Where to place link on a continuous transition. y value is also used
    #       to differentiate transitions at different heights
    #   "extra_data": dict[str: int]. additional coordinate data for continuous boundaries, like "x_max" etc.
    #   "type": EntranceGroup. Entrance group entrance type (house, cave, sea etc)
    #   "direction": EntranceGroup. Entrance group direction
    #   "two_way": bool=True. generates a reciprocal entrance, also used for ER generation
    # }

    "Mercay SW Oshus' House": {
        "return_name": "Oshus' Exit",
        "entrance": (0xB, 0, 2),
        "exit": (0xB, 0xA, 1),
        "entrance_region": "mercay sw",
        "exit_region": "mercay oshus",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "two_way": True,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW Apricot's House": {
        "return_name": "Apricot's Exit",
        "entrance": (0xB, 0x0, 3),
        "exit": (0xB, 0xB, 1),
        "entrance_region": "mercay sw",
        "exit_region": "mercay apricot",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "two_way": True,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW Barrel Cave": {
        "return_name": "Sword Cave Exit",
        "entrance": (0xB, 0x0, 4),
        "exit": (0xB, 0x13, 1),
        "entrance_region": "mercay sw",
        "exit_region": "mercay sword cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW North": {
        "return_name": "Mercay NW South",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-164000, -164, 16000),  # The coord that doesn't matter doesn't matter. Y level diferentiates exit
        "entrance_region": "mercay sw",
        "exit_region": "mercay nw chus",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW East": {
        "return_name": "Mercay SE West",
        "entrance": (0xB, 0x0, 0xFD),
        "exit": (0xB, 0x3, 0xFE),
        "coords": (4780, -164, 53300),
        "entrance_region": "mercay sw bridge",
        "exit_region": "mercay se",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Milk Bar": {
        "return_name": "Milk Bar Exit",
        "entrance": (0xB, 0x3, 0x3),
        "exit": (0xB, 0xC, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay milk bar",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Shipyard": {
        "return_name": "Shipyard Exit",
        "entrance": (0xB, 0x3, 0x4),
        "exit": (0xB, 0xD, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay shipyard",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Tuzi's House": {
        "return_name": "Tuzi's Exit",
        "entrance": (0xB, 0x3, 0x5),
        "exit": (0xB, 0xE, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay tuzi",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Treasure Teller": {
        "return_name": "Treasure Teller's Exit",
        "entrance": (0xB, 0x3, 0x6),
        "exit": (0xB, 0xF, 0x0),
        "entrance_region": "mercay se",
        "exit_region": "mercay treasure teller",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Shop": {
        "return_name": "Mercay Shop Exit",
        "entrance": (0xB, 0x3, 0x7),
        "exit": (0xB, 0x11, 0x1),
        "entrance_region": "mercay se",
        "exit_region": "mercay shop",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE North": {
        "return_name": "Mercay NE South",
        "entrance_region": "mercay se",
        "exit_region": "mercay ne",
        "entrance": (0xB, 0x3, 0xFC),
        "exit": (0xB, 0x2, 0xFB),
        "coords": (131000, -164, -4815),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE West": {
        "return_name": "Mercay NW East",
        "entrance_region": "mercay ne",
        "exit_region": "mercay nw temple",
        "entrance": (0xB, 0x2, 0xFE),
        "exit": (0xB, 0x1, 0xFD),
        "coords": (-4815, 9666, -60000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NW Temple Cave": {
        "return_name": "Mercay Geozard Cave North Exit",
        "entrance_region": "mercay nw temple",
        "exit_region": "mercay geozard cave north",
        "entrance": (0xB, 0x1, 0x3),
        "exit": (0xB, 0x10, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE Ledge Cave": {
        "return_name": "Mercay Geozard Cave South Exit",
        "entrance_region": "mercay ne ledge",
        "exit_region": "mercay geozard cave south",
        "entrance": (0xB, 0x2, 0x1),
        "exit": (0xB, 0x10, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Ledge North": {
        "return_name": "Mercay NE Ledge South",
        "entrance_region": "mercay se ledge",
        "exit_region": "mercay ne ledge",
        "entrance": (0xB, 0x3, 0xFC),
        "exit": (0xB, 0x2, 0xFB),
        "coords": (110000, 9666, -4815),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE Hidden Cave": {
        "return_name": "Freedle Tunnel West",
        "entrance_region": "mercay ne",
        "exit_region": "mercay freedle tunnel",
        "entrance": (0xB, 0x2, 0x2),
        "exit": (0xB, 0x12, 0x3),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE Freedle Island Cave": {
        "return_name": "Freedle Tunnel East",
        "entrance_region": "mercay freedle island",
        "exit_region": "mercay freedle tunnel",
        "entrance": (0xB, 0x2, 0x3),
        "exit": (0xB, 0x12, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Cave": {
        "return_name": "Mountain Passage Upper Exit",
        "entrance_region": "mercay se",
        "exit_region": "mercay passage 4",
        "entrance": (0xB, 0x3, 0x1),
        "exit": (0x27, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mountain Passage Lower Staircase": {
        "return_name": "Mountain Passage Upper Staircase",
        "entrance_region": "mercay passage 2 exit",
        "exit_region": "mercay passage 3",
        "entrance": (0x27, 0x0, 0x2),
        "exit": (0x27, 0x1, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NW Bamboo Cave": {
        "return_name": "Mountain Passage Lower Exit",
        "entrance_region": "mercay nw bamboo",
        "exit_region": "mercay passage 1",
        "entrance": (0xB, 0x1, 0x1),
        "exit": (0x27, 0x0, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },

    # =========== TotOK ==============
    "Mercay NW Enter Temple": {
        "return_name": "TotOK Lobby Exit",
        "entrance": (0xB, 0x1, 0x2),
        "exit": (0x26, 0x00, 0x1),
        "entrance_region": "mercay nw temple",
        "exit_region": "totok",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    # ========== Cannon ==========
    "Cannon Workshop East": {
        "return_name": "Cannon Eddo Exit",
        "entrance_region": "cannon outside eddo",
        "exit_region": "cannon eddo",
        "entrance": (0x13, 0x0, 0x4),
        "exit": (0x13, 0xB, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Cannon Workshop West": {
        "return_name": "Fuzo's Exit",
        "entrance_region": "cannon island",
        "exit_region": "cannon fuzo",
        "entrance": (0x13, 0x0, 0x3),
        "exit": (0x13, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Fuzo's Interior Door": {
        "return_name": "Eddo's Interior Door",
        "entrance_region": "cannon fuzo",
        "exit_region": "cannon eddo",
        "entrance": (0x13, 0xA, 0x1),
        "exit": (0x13, 0xB, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Cannon Bee Cave": {
        "return_name": "Cannon Cave Exit",
        "entrance_region": "cannon island",
        "exit_region": "cannon cave south",
        "entrance": (0x13, 0x0, 0x1),
        "exit": (0x28, 0x0, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Cannon Bomb Garden Cave": {
        "return_name": "Cannon Cave Staircase",
        "entrance_region": "cannon bomb garden",
        "exit_region": "cannon cave north",
        "entrance": (0x13, 0x0, 0x2),
        "exit": (0x28, 0x0, 0x1),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.CANNON
    },
#
#     # =========== Ember Island ================
    "Ember Port House": {
        "return_name": "Ember Port House Exit",
        "entrance": (0xD, 0x0, 0x2),
        "exit": (0xD, 0xB, 0x0),
        "entrance_region": "ember port",
        "exit_region": "ember port house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "Ember Astrid's House": {
        "return_name": "Astrid's Exit",
        "entrance": (0xD, 0x0, 0x1),
        "exit": (0xD, 0xA, 0x0),
        "entrance_region": "ember port",
        "exit_region": "ember astrid",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "Astrid's Stairs": {
        "return_name": "Astrid's Basement Stairs",
        "entrance": (0xD, 0xA, 0x1),
        "exit": (0xD, 0x14, 0x0),
        "entrance_region": "ember astrid",
        "exit_region": "ember astrid basement",
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.EMBER
    },
    "Ember Kayo's House": {
        "return_name": "Kayo's Exit",
        "entrance": (0xD, 0x0, 0x3),
        "exit": (0xD, 0xC, 0x0),
        "entrance_region": "ember port",
        "exit_region": "ember kayo",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "Ember West Coast South": {
        "return_name": "Ember East Coast South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, -164, 80000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember port",
        "exit_region": "ember coast east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Coast North": {
        "return_name": "Ember East Coast North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, -164, -85000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember coast north",
        "exit_region": "ember coast east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Climb North": {
        "return_name": "Ember East Climb North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 4751, -65000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember port",
        "exit_region": "ember climb east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Climb South": {
        "return_name": "Ember East Climb South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 4751, 50000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember climb west",
        "exit_region": "ember coast east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Heights North": {
        "return_name": "Ember East Heights North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 9666, -50000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember climb west",
        "exit_region": "ember outside tof",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Heights South": {
        "return_name": "Ember East Heights South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 9666, 25000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember summit west",
        "exit_region": "ember outside tof",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Summit North": {
        "return_name": "Ember East Summit North",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 14582, -35000),
        "extra_data": {"z_max": 0},
        "entrance_region": "ember summit west",
        "exit_region": "ember summit north",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },
    "Ember West Summit South": {
        "return_name": "Ember East Summit South",
        "entrance": (0xD, 0x0, 0xFD),
        "exit": (0xD, 0x1, 0xFE),
        "coords": (-4500, 14582, 8000),
        "extra_data": {"z_min": 0},
        "entrance_region": "ember summit west",
        "exit_region": "ember summit east",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },

    # ========== Temple of Fire ============
    "Ember Enter Temple": {
        "return_name": "ToF Exit",
        "entrance": (0xD, 0x1, 0x0),
        "exit": (0x1C, 0x0, 0x0),
        "entrance_region": "ember outside tof",
        "exit_region": "tof 1f",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
        },
    "ToF Enter Boss": {
        "return_name": "Blaaz Exit",
        "entrance": (0x1C, 0x3, 0x1),
        "exit": (0x2B, 0x0, 0x0),
        "entrance_region": "tof before blaaz",
        "exit_region": "tof blaaz",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "ToF Blaaz Warp": {
        "entrance": (0x2B, 0x0, 0x0),
        "exit": (0xD, 0x1, 0x1),
        "entrance_region": "tof blaaz",
        "exit_region": "ember outside tof",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.EMBER
    },
# ========== Molida ============
    "Molida Port House": {
        "return_name": "Molida Port House Exit",
        "entrance": (0xC, 0x0, 0x4),
        "exit": (0xC, 0xC, 0x1),
        "entrance_region": "molida island",
        "exit_region": "molida port house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cave Geozard Cave": {
        "return_name": "Octo Cave East",
        "entrance_region": "molida cave post geozard",
        "exit_region": "molida cave octos",
        "entrance": (0xC, 0xA, 0x6),
        "exit": (0xC, 0xF, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cave Back Cave": {
        "return_name": "Octo Cave West",
        "entrance_region": "molida cave back",
        "exit_region": "molida cave octos",
        "entrance": (0xC, 0xA, 0x7),
        "exit": (0xC, 0xF, 0x3),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cave Bomb Cave": {
        "return_name": "Shovel Cave Exit",
        "entrance_region": "molida cave back",
        "exit_region": "molida shovel cave",
        "entrance": (0xC, 0xA, 0x5),
        "exit": (0xC, 0xF, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cave Staircase": {
        "return_name": "Molida Cliff Staircase",
        "entrance_region": "molida cave back",
        "exit_region": "molida cliff north",
        "entrance": (0xC, 0xA, 0x1),
        "exit": (0xC, 0x1, 0x1),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cliff North": {
        "return_name": "Molida Cliff South",
        "entrance_region": "molida cliff south",
        "exit_region": "molida cliff north",
        "entrance": (0xC, 0x0, 0xFC),
        "exit": (0xC, 0x1, 0xFB),
        "coords": (80000, 4751, -4815),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Romanos' House": {
        "return_name": "Romanos' Exit",
        "entrance_region": "molida island",
        "exit_region": "molida romaros",
        "entrance": (0xC, 0x0, 0x3),
        "exit": (0xC, 0xB, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Shop": {
        "return_name": "Molida Shop Exit",
        "entrance_region": "molida island",
        "exit_region": "molida shop",
        "entrance": (0xC, 0x0, 0x6),
        "exit": (0xC, 0xE, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Potato's House": {
        "return_name": "Potato's Exit",
        "entrance_region": "molida island",
        "exit_region": "molida potato house",
        "entrance": (0xC, 0x0, 0x5),
        "exit": (0xC, 0xD, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cave": {
        "return_name": "Molida Cave Exit",
        "entrance_region": "molida island",
        "exit_region": "molida cave",
        "entrance": (0xC, 0x0, 0x2),
        "exit": (0xC, 0xA, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida Cave Sun Staircase": {
        "return_name": "Molida North Staircase",
        "entrance_region": "molida cave sun door",
        "exit_region": "molida north",
        "entrance": (0xC, 0xA, 0x4),
        "exit": (0xC, 0x1, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Dig Hole": {
        "reverse_name": "Molida Cave South Drop",
        "two_way": False,
        "entrance_region": "molida island",
        "exit_region": "molida cave upper",
        "entrance": (0xC, 0x0, 0x0),
        "exit": (0xC, 0xA, 0x3),
        "type": EntranceGroups.HOLES,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida North Dig Hole": {
        "reverse_name": "Molida Cave Chest Drop",
        "two_way": False,
        "entrance_region": "molida north",
        "exit_region": "molida cave drop",
        "entrance": (0xC, 0x1, 0x2),
        "exit": (0xC, 0xA, 0x8),
        "type": EntranceGroups.HOLES,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MOLIDA
    },

    # ========== Temple of Courage ============
    "Molida Enter Temple": {
        "return_name": "ToC Exit",
        "entrance": (0xC, 0x1, 0x3),
        "exit": (0x1E, 0x0, 0x0),
        "entrance_region": "toc gates",
        "exit_region": "toc",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "ToC Enter Boss": {
        "return_name": "Crayk Exit",
        "entrance": (0x1E, 0x3, 0x3),
        "exit": (0x2C, 0x0, 0x2),
        "entrance_region": "toc before boss",
        "exit_region": "toc crayk",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "ToC Crayk Warp": {
        "entrance": (0x2C, 0x0, 0x0),
        "exit": (0xC, 0x1, 0x4),
        "entrance_region": "toc crayk",
        "exit_region": "toc gates",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.MOLIDA
    },

    # Spirit
    "Spirit Island Cave": {
        "return_name": "Spirit Cave Exit",
        "entrance_region": "spirit island",
        "exit_region": "spirit cave",
        "entrance": (0x17, 0x0, 0x1),
        "exit": (0x17, 0x1, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.SPIRIT
    },
    # ========== Gust ============

    "Fake temp": {
        "return_name": "Temp Fake",
        "entrance": (0x40, 0x1, 0x0),
        "exit": (0x40, 0x0, 0x0),
        "entrance_region": "nope",
        "exit_region": "epon",
        "type": EntranceGroups.NONE,
        "direction": EntranceGroups.NONE,
        },
    "Gust SW Coast North": {
        "return_name": "Gust NW Coast South",
        "entrance_region": "gust west ledge",
        "exit_region": "gust nw",
        "entrance": (0xE, 0x0, 0xFC),
        "exit": (0xE, 0x1, 0xFB),
        "coords": (-76000, 9666, -8192),
        "extra_data": {"x_max": -67000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GUST
    },
    "Gust SW Inland North": {
        "return_name": "Gust NW Inland South",
        "entrance_region": "gust west",
        "exit_region": "gust above temple",
        "entrance": (0xE, 0x0, 0xFC),
        "exit": (0xE, 0x1, 0xFB),
        "coords": (-48500, 9666, -8192),
        "extra_data": {"x_min": -56000,
                       "x_max": -40000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GUST
    },
    "Gust South Above Temple North": {
        "return_name": "Gust North Above Temple South",
        "entrance_region": "gust cliffs",
        "exit_region": "gust above temple",
        "entrance": (0xE, 0x0, 0xFC),
        "exit": (0xE, 0x1, 0xFB),
        "coords": (-17000, 9666, -8192),
        "extra_data": {"x_min": -25000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GUST
    },
    "Gust South Temple Road North": {
        "return_name": "Gust North Temple Road South",
        "entrance_region": "gust cliffs",
        "exit_region": "gust temple road",
        "entrance": (0xE, 0x0, 0xFC),
        "exit": (0xE, 0x1, 0xFB),
        "coords": (4452, 4751, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GUST
    },
    "Gust Cave East": {
        "return_name": "Miniblin Cave East",
        "entrance_region": "gust cliffs",
        "exit_region": "gust cave",
        "entrance": (0xE, 0x0, 0x4),
        "exit": (0xE, 0xB, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },
    "Gust Cave West": {
        "return_name": "Miniblin Cave West",
        "entrance_region": "gust south",
        "exit_region": "gust cave",
        "entrance": (0xE, 0x0, 0x3),
        "exit": (0xE, 0xB, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },
    "Gust Secret Cave": {
        "return_name": "Gust Hideout Exit",
        "entrance_region": "gust south",
        "exit_region": "gust hideout",
        "entrance": (0xE, 0x0, 0x2),
        "exit": (0xE, 0xA, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },


        # ========== Temple of Wind ============
    "Gust Enter Temple": {
        "return_name": "ToW Exit",
        "entrance": (0xE, 0x1, 0x0),
        "exit": (0x1D, 0x0, 0x0),
        "entrance_region": "gust outside temple",
        "exit_region": "tow",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
        },
    "ToW Enter Boss": {
        "return_name": "Cyclok Exit",
        "entrance": (0x1D, 0x4, 0x1),
        "exit": (0x2A, 0x0, 0x1),
        "entrance_region": "tow before boss",
        "exit_region": "tow cyclok",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },
    "ToW Cyclok Warp": {
        "entrance": (0x2A, 0x0, 0x0),
        "exit": (0xE, 0x1, 0x0),
        "entrance_region": "tow cyclok",
        "exit_region": "gust outside temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.GUST
    },
    # Bannan
    "Bannan Hut": {
        "return_name": "Wayfarer's Exit",
        "entrance_region": "bannan",
        "exit_region": "bannan wayfarer",
        "entrance": (0x14, 0x0, 0x2),
        "exit": (0x14, 0x1, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.BANNAN
    },
    "Bannan Wayfarer Cave": {
        "return_name": "Bannan Cave West Exit",
        "entrance_region": "bannan",
        "exit_region": "bannan cave west",
        "entrance": (0x14, 0x0, 0x5),
        "exit": (0x14, 0xA, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.BANNAN
    },
    "Bannan Salvatore Cave": {
        "return_name": "Bannan Cave East Exit",
        "entrance_region": "bannan east",
        "exit_region": "bannan cave east",
        "entrance": (0x14, 0x0, 0x4),
        "exit": (0x14, 0xA, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.BANNAN
    },
    # ===== Zauz =====
    "Zauz' House": {
        "return_name": "Zauz' Exit",
        "entrance_region": "zauz",
        "exit_region": "zauz house",
        "entrance": (0x16, 0x0, 0x2),
        "exit": (0x16, 0xA, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.ZAUZ
    },
    # ===== Uncharted =====
    "Uncharted Cave": {
        "return_name": "Uncharted Cave Exit",
        "entrance_region": "uncharted outside cave",
        "exit_region": "uncharted cave",
        "entrance": (0x1A, 0x0, 0x2),
        "exit": (0x1A, 0xA, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.UNCHARTED
    },
    "Uncharted Cave Inner Cave": {
        "return_name": "Golden Chief Exit",
        "entrance_region": "uncharted cave",
        "exit_region": "uncharted inner cave",
        "entrance": (0x1A, 0xA, 0x2),
        "exit": (0x1A, 0xB, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.UNCHARTED
    },

    # ========== Goron ============
    "Goron SW Port House": {
        "return_name": "Goron Port House Exit",
        "entrance": (0x10, 0x2, 0x1),
        "exit": (0x10, 0xB, 0x0),
        "entrance_region": "goron sw",
        "exit_region": "goron port house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SE Mountain House": {
        "return_name": "Goron Mountain House Exit",
        "entrance_region": "goron se",
        "exit_region": "goron mountain house",
        "entrance": (0x10, 0x3, 0x2),
        "exit": (0x10, 0xF, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Chu House": {
        "return_name": "Goron Chu House Exit",
        "entrance_region": "goron sw",
        "exit_region": "goron chu house",
        "entrance": (0x10, 0x2, 0x3),
        "exit": (0x10, 0xD, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Rock House": {
        "return_name": "Goron Rock House Exit",
        "entrance_region": "goron sw",
        "exit_region": "goron rock house",
        "entrance": (0x10, 0x2, 0x2),
        "exit": (0x10, 0xC, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Shop": {
        "return_name": "Goron Shop Exit",
        "entrance_region": "goron sw",
        "exit_region": "goron shop",
        "entrance": (0x10, 0x2, 0x4),
        "exit": (0x10, 0x14, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW North": {
        "return_name": "Goron NW South",
        "entrance_region": "goron sw",
        "exit_region": "goron shortcut",
        "entrance": (0x10, 0x2, 0xFC),
        "exit": (0x10, 0x0, 0xFB),
        "coords": (-140000, 9666, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GORON
    },
    "Goron SE Coast House": {
        "return_name": "Goron Coast House Exit",
        "entrance_region": "goron se",
        "exit_region": "goron se house",
        "entrance": (0x10, 0x3, 0x1),
        "exit": (0x10, 0xE, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SE Chief House": {
        "return_name": "Goron Chief House Exit",
        "entrance_region": "goron se",
        "exit_region": "goron chief house",
        "entrance": (0x10, 0x3, 0x0),
        "exit": (0x10, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Coast East": {
        "return_name": "Goron SE Coast West",
        "entrance_region": "goron sw",
        "exit_region": "goron se",
        "entrance": (0x10, 0x2, 0xFD),
        "exit": (0x10, 0x3, 0xFE),
        "coords": (-8000, 4751, 70000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron SW Mountains East": {
        "return_name": "Goron SE Mountains West",
        "entrance_region": "goron chu ledge",
        "exit_region": "goron se",
        "entrance": (0x10, 0x2, 0xFD),
        "exit": (0x10, 0x3, 0xFE),
        "coords": (-8000, 9666, 22500),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron SE North": {
        "return_name": "Goron NE South",
        "entrance_region": "goron se",
        "exit_region": "goron ne",
        "entrance": (0x10, 0x3, 0xFC),
        "exit": (0x10, 0x1, 0xFB),
        "coords": (148000, 4751, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GORON
    },
    "Goron South Dead End": {
        "return_name": "Goron NE Mountain West",
        "entrance_region": "goron maze south dead end",
        "exit_region": "goron maze south",
        "entrance": (0x10, 0x0, 0xFD),
        "exit": (0x10, 0x1, 0xFE),
        "coords": (-8000, 4751, -60000),
        "extra_data": {"z_min": -65000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron North Dead End": {
        "return_name": "Goron NE Middle West",
        "entrance_region": "goron maze north dead end",
        "exit_region": "goron maze north",
        "entrance": (0x10, 0x0, 0xFD),
        "exit": (0x10, 0x1, 0xFE),
        "coords": (-8000, 4751, -102000),
        "extra_data": {"z_max": -95000, "z_min": -105000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron NW Coast East": {
        "return_name": "Goron NE Coast West",
        "entrance_region": "goron like like",
        "exit_region": "goron maze nw",
        "entrance": (0x10, 0x0, 0xFD),
        "exit": (0x10, 0x1, 0xFE),
        "coords": (-8000, 4751, -122000),
        "extra_data": {"z_max": -110000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron NW Middle East": {
        "return_name": "Goron Spikes Dead End",
        "entrance_region": "goron like like",
        "exit_region": "goron maze spikes",
        "entrance": (0x10, 0x0, 0xFD),
        "exit": (0x10, 0x1, 0xFE),
        "coords": (-8000, 4751, -82000),
        "extra_data": {"z_max": -75000, "z_min": -85000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },

    # ========== Goron Temple ============
    "Goron Enter Temple": {
        "return_name": "GT Exit",
        "entrance": (0x10, 0x0, 0x0),
        "exit": (0x20, 0x0, 0x0),
        "entrance_region": "goron outside temple",
        "exit_region": "gt",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "GT Enter Boss": {
        "return_name": "Dongo Exit",
        "entrance": (0x20, 0x4, 0x1),
        "exit": (0x2E, 0x0, 0x0),
        "entrance_region": "gt before dongo",
        "exit_region": "gt dongo",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "GT Dongo Warp": {
        "entrance": (0x20, 0xA, 0x0),
        "exit": (0x10, 0x0, 0x1),
        "entrance_region": "gt dongo",
        "exit_region": "goron outside temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.GORON
    },
    # ========== Frost ============
    "Frost SW Smart House": {
        "return_name": "Smart Anouki's Exit",
        "entrance": (0xF, 0x0, 0x2),
        "exit": (0xF, 0xB, 0x0),
        "entrance_region": "frost",
        "exit_region": "frost smart house",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW Chief House": {
        "return_name": "Anouki Chief's Exit",
        "entrance_region": "frost",
        "exit_region": "frost chief house",
        "entrance": (0xF, 0x0, 0x1),
        "exit": (0xF, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW Sensitive House": {
        "return_name": "Sensitive Anouki's Exit",
        "entrance_region": "frost",
        "exit_region": "frost sensitive house",
        "entrance": (0xF, 0x0, 0x3),
        "exit": (0xF, 0xC, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW North": {
        "return_name": "Frost NW South",
        "entrance_region": "frost",
        "exit_region": "frost estate",
        "entrance": (0xF, 0x0, 0xFC),
        "exit": (0xF, 0x2, 0xFB),
        "coords": (-120000, -164, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    "Frost NW Dobo's House": {
        "return_name": "Dobo's Exit",
        "entrance_region": "frost estate",
        "exit_region": "frost dobo",
        "entrance": (0xF, 0x2, 0x1),
        "exit": (0xF, 0xD, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Kumu's House": {
        "return_name": "Kumu's Exit",
        "entrance_region": "frost estate",
        "exit_region": "frost kumu",
        "entrance": (0xF, 0x2, 0x2),
        "exit": (0xF, 0xE, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Fofo's House": {
        "return_name": "Fofo's Exit",
        "entrance_region": "frost estate",
        "exit_region": "frost fofo",
        "entrance": (0xF, 0x2, 0x3),
        "exit": (0xF, 0xF, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Mazo's House": {
        "return_name": "Mazo's Exit",
        "entrance_region": "frost estate",
        "exit_region": "frost mazo",
        "entrance": (0xF, 0x2, 0x6),
        "exit": (0xF, 0x12, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Aroo's House": {
        "return_name": "Aroo's Exit",
        "entrance_region": "frost estate",
        "exit_region": "frost aroo",
        "entrance": (0xF, 0x2, 0x5),
        "exit": (0xF, 0x11, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Gumo's House": {
        "return_name": "Gumo's Exit",
        "entrance_region": "frost estate",
        "exit_region": "frost gumo",
        "entrance": (0xF, 0x2, 0x4),
        "exit": (0xF, 0x10, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW Cave": {
        "return_name": "Frost Cave West Exit",
        "entrance_region": "frost",
        "exit_region": "frost cave",
        "entrance": (0xF, 0x0, 0x4),
        "exit": (0xF, 0x13, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SE Cave": {
        "return_name": "Frost Cave East Exit",
        "entrance_region": "frost field",
        "exit_region": "frost cave",
        "entrance": (0xF, 0x3, 0x0),
        "exit": (0xF, 0x13, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost Field Upper NE": {
        "return_name": "Frost Above Temple SE",
        "entrance_region": "frost field upper se",
        "exit_region": "frost above temple east",
        "entrance": (0xF, 0x3, 0xFC),
        "exit": (0xF, 0x1, 0xFB),
        "coords": (202000, 14582, -8192),
        "extra_data": {"x_min": 185000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    "Frost Field Upper NW": {
        "return_name": "Frost Above Temple SW",
        "entrance_region": "frost field upper north",
        "exit_region": "frost above temple west",
        "entrance": (0xF, 0x3, 0xFC),
        "exit": (0xF, 0x1, 0xFB),
        "coords": (166000, 14582, -8192),
        "extra_data": {"x_max": 185000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    "Frost Field Lower North": {
        "return_name": "Frost NE Lower South",
        "entrance_region": "frost field exit",
        "exit_region": "frost outside arena",
        "entrance": (0xF, 0x3, 0xFC),
        "exit": (0xF, 0x1, 0xFB),
        "coords": (185000, -164, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    # ========== Temple of Ice ============
    "Frost Enter Temple": {
        "return_name": "ToI Exit",
        "entrance": (0xF, 0x1, 0x0),
        "exit": (0x1F, 0x0, 0x0),
        "entrance_region": "frost outside temple",
        "exit_region": "toi",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "ToI Gleeok Warp": {
        "entrance": (0x1f, 0x6, 0x0),
        "exit": (0xF, 0x1, 0x1),
        "entrance_region": "toi gleeok",
        "exit_region": "frost outside temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.FROST
    },
    "ToI 1F Right Staircase": {
        "return_name": "ToI 2F Right Descent",
        "entrance": (0x1f, 0x0, 0x1),
        "exit": (0x1F, 0x3, 0x3),
        "entrance_region": "toi 1f ascent",
        "exit_region": "toi 2f right",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 2F Right Ascent": {
        "return_name": "ToI 3F Right Staircase",
        "entrance": (0x1f, 0x3, 0x2),
        "exit": (0x1F, 0x1, 0x1),
        "entrance_region": "toi 2f right",
        "exit_region": "toi 3f right",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 3F Key Door Staircase": {
        "return_name": "ToI 2F Arena Staircase",
        "entrance": (0x1f, 0x2, 0x2),
        "exit": (0x1F, 0x3, 0x1),
        "entrance_region": "toi 3f key door",
        "exit_region": "toi 2f arena",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 2F Left Descent": {
        "return_name": "ToI 1F Beetle Staircase",
        "entrance": (0x1f, 0x3, 0x0),
        "exit": (0x1F, 0x0, 0x2),
        "entrance_region": "toi 2f left",
        "exit_region": "toi 1f beetles",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 1F Descent": {
        "return_name": "ToI B1 Ascent",
        "entrance": (0x1f, 0x0, 0x3),
        "exit": (0x1F, 0x2, 0x1),
        "entrance_region": "toi 1f descent",
        "exit_region": "toi b1 ascent",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI B1 Descent": {
        "return_name": "ToI B2 Staircase",
        "entrance": (0x1f, 0x2, 0x2),
        "exit": (0x1F, 0x5, 0x0),
        "entrance_region": "toi b1 boss door",
        "exit_region": "toi b2",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI B1 Blue Warp": {
        "return_name": "ToI 1F Blue Warp",
        "entrance": (0x1f, 0x2, 0x7),
        "exit": (0x1F, 0x0, 0x4),
        "entrance_region": "toi b1 before boss",
        "exit_region": "toi blue warp",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI Enter Boss": {
        "return_name": "Gleeok Exit",
        "entrance": (0x1f, 0x2, 0x3),
        "exit": (0x2D, 0x0, 0x0),
        "entrance_region": "toi b1 before boss",
        "exit_region": "gleeok",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },

# ======= Dead=========
    "IotD Port Cave": {
        "return_name": "IotD Cave East Exit",
        "entrance_region": "iotd port",
        "exit_region": "iotd cave",
        "entrance": (0x15, 0x0, 0x6),
        "exit": (0x15, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "Aquanine Cave Secret Cave": {
        "return_name": "Rupoor Cave Exit",
        "entrance_region": "iotd cave",
        "exit_region": "iotd rupoor",
        "entrance": (0x15, 0x1, 0x3),
        "exit": (0x15, 0x2, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "IotD Like Like Cave": {
        "return_name": "Aquanine Cave West",
        "entrance_region": "iotd",
        "exit_region": "iotd cave",
        "entrance": (0x15, 0x0, 0x8),
        "exit": (0x15, 0x1, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "Boulder Tunnel Cave": {
        "return_name": "IotD Rupee Cave Exit",
        "entrance_region": "iotd tunnel",
        "exit_region": "iotd tunnel cave",
        "entrance": (0x15, 0x3, 0x3),
        "exit": (0x15, 0x4, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "IotD Face Staircase": {
        "return_name": "Boulder Tunnel Staircase",
        "entrance_region": "iotd face",
        "exit_region": "iotd tunnel",
        "entrance": (0x15, 0x0, 0x5),
        "exit": (0x15, 0x3, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.DEAD
    },
    "IotD Pyramid": {
        "return_name": "Brant's Exit",
        "entrance_region": "iotd",
        "exit_region": "iotd temple",
        "entrance": (0x15, 0x0, 0x3),
        "exit": (0x15, 0x5, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "IotD Crown Staircase": {
        "return_name": "Brant's Chamber Staircase",
        "entrance_region": "iotd crown",
        "exit_region": "iotd temple",
        "entrance": (0x15, 0x0, 0x4),
        "exit": (0x15, 0xA, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.DEAD
    },
    "IotD Dig Hole": {
        "reverse_name": "IotD Tunnel Drop",
        "entrance_region": "iotd",
        "exit_region": "iotd tunnel",
        "entrance": (0x15, 0x0, 0x0),
        "exit": (0x15, 0x3, 0x1),
        "type": EntranceGroups.HOLES,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.DEAD
    },
    "Brant's Maze 1": {
        "entrance_region": "iotd temple",
        "exit_region": "iotd brant maze",
        "entrance": (0x15, 0x5, 0x2),
        "exit": (0x15, 0x6, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "never_shuffle": True,  # Doesn't do anything, isn't needed yet
        "island": EntranceGroups.DEAD
    },
    "Brant's Maze Exit": {
        "entrance_region": "iotd brant maze",
        "exit_region": "iotd brant chamber",
        "entrance": (0x15, 0xA, 0x1),
        "exit": (0x15, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "never_shuffle": True,  # Doesn't do anything, isn't needed yet
        "island": EntranceGroups.DEAD
    },
    # ========== Ruins ============
    "Ruins SW Upper Maze North": {
        "return_name": "Ruins NW One-Way Ledge South",
        "entrance_region": "ruins sw maze upper",
        "exit_region": "ruins nw maze upper exit",
        "entrance": (0x11, 0x0, 0xFC),
        "exit": (0x11, 0x1, 0xFB),
        "coords": (-174425, 4751, -4815),
        "extra_data": {"x_max": -70000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Lower Maze Exit North": {
        "return_name": "Ruins NW One-Way Ledge SW",
        "entrance_region": "ruins sw maze lower exit",
        "exit_region": "ruins nw maze lower exit",
        "entrance": (0x11, 0x0, 0xFC),
        "exit": (0x11, 0x1, 0xFB),
        "coords": (-194200, 9666, -4815),
        "extra_data": {"x_max": -150000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Across Bridge East": {
        "return_name": "Ruins NE Doylan Bridge One-Way West",
        "entrance_region": "ruins nw across bridge",
        "exit_region": "ruins ne enter upper",
        "entrance": (0x11, 0x1, 0xFD),
        "exit": (0x11, 0x2, 0xFE),
        "coords": (4784, 9666, -62640),
        "extra_data": {"z_min": -110000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Upper One-Way East": {
        "return_name": "Ruins NE Doylan's Bridge NW",
        "entrance_region": "ruins nw return",
        "exit_region": "ruins ne doylan bridge",
        "entrance": (0x11, 0x1, 0xFD),
        "exit": (0x11, 0x2, 0xFE),
        "coords": (4784, 9666, -150700),
        "extra_data": {"z_max": -110000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Port Cliff North": {
        "return_name": "Ruins NW Port Cliff South",
        "entrance_region": "ruins sw port cliff",
        "exit_region": "ruins nw port cliff",
        "entrance": (0x11, 0x0, 0xFC),
        "exit": (0x11, 0x1, 0xFB),
        "coords": (-46050, 4751, -4815),
        "extra_data": {"x_min": -70000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW East": {
        "return_name": "Ruins SE West",
        "entrance_region": "ruins sw port cliff",
        "exit_region": "ruins se return bridge west",
        "entrance": (0x11, 0x0, 0xFD),
        "exit": (0x11, 0x3, 0xFE),
        "coords": (4784, 9666, 51500),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Port Cave": {
        "return_name": "Ruins Geozard Cave East",
        "entrance": (0x11, 0x0, 0x2),
        "exit": (0x11, 0xA, 0x1),
        "entrance_region": "ruins port",
        "exit_region": "ruins geozard cave east",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
"Ruins SW Cliff Cave": {
        "return_name": "Ruins Geozard Cave West",
        "entrance_region": "ruins sw maze upper",
        "exit_region": "ruins geozard cave west",
        "entrance": (0x11, 0x0, 0x3),
        "exit": (0x11, 0xA, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Maze Lower North": {
        "return_name": "Ruins NW Lower Maze Chest South",
        "entrance_region": "ruins sw maze lower",
        "exit_region": "ruins nw maze lower chest",
        "entrance": (0x12, 0x0, 0xFC),
        "exit": (0x12, 0x1, 0xFB),
        "coords": (-63750, -164, -4815),
        "extra_data": {"conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Pyramid": {
        "return_name": "Bremeur's Exit",
        "entrance_region": "ruins nw boulders",
        "exit_region": "bremeur",
        "entrance": (0x11, 0x1, 0x1),
        "exit": (0x24, 0x0, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Cave": {
        "return_name": "Ruins Rupee Cave Exit",
        "entrance_region": "ruins nw across bridge",
        "exit_region": "ruins rupee cave",
        "entrance": (0x12, 0x1, 0x2),
        "exit": (0x12, 0xB, 0x1),
        "extra_data": {"conditional": ["ruins_water"]},
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins NE Small Pyramid": {
        "return_name": "Doylan's Exit",
        "entrance_region": "ruins ne doylan bridge",
        "exit_region": "doylan temple",
        "entrance": (0x11, 0x2, 0x1),
        "exit": (0x22, 0x0, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Doylan's Staircase": {
        "return_name": "Doylan's Chamber Exit",
        "entrance_region": "doylan temple",
        "exit_region": "doylan chamber",
        "entrance": (0x22, 0x0, 0x2),
        "exit": (0x22, 0x1, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE Coast North": {
        "return_name": "Ruins NE Coast South",
        "entrance_region": "ruins se coast",
        "exit_region": "ruins ne behind temple",
        "entrance": (0x12, 0x3, 0xFC),
        "exit": (0x12, 0x2, 0xFB),
        "coords": (213590, -164, 4784),
        "extra_data": {"x_min": 144990,
                       "conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Alcove East": {
        "return_name": "Ruins NE Lower Bay West",
        "entrance_region": "ruins nw alcove",
        "exit_region": "ruins ne lower",
        "entrance": (0x12, 0x1, 0xFD),
        "exit": (0x12, 0x2, 0xFE),
        "coords": (8192, -164, -43675),
        "extra_data": {"z_min": -80000,
                       "conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Lower East": {
        "return_name": "Ruins NE Lower Boulders West",
        "entrance_region": "ruins nw lower",
        "exit_region": "ruins ne lower",
        "entrance": (0x12, 0x1, 0xFD),
        "exit": (0x12, 0x2, 0xFE),
        "coords": (4784, -164, -120000),
        "extra_data": {"z_max": -80000,
                       "conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE Bay North": {
        "return_name": "Ruins NE South",
        "entrance_region": "ruins se lower",
        "exit_region": "ruins ne lower",
        "entrance": (0x12, 0x3, 0xFC),
        "exit": (0x12, 0x2, 0xFB),
        "coords": (13000, -164, 4784),
        "extra_data": {"x_max": 70000,
                       "conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE Boulder North": {
        "return_name": "Ruins NE Secret Chest South",
        "entrance_region": "ruins se lower",
        "exit_region": "ruins ne secret chest",
        "entrance": (0x12, 0x3, 0xFC),
        "exit": (0x12, 0x2, 0xFB),
        "coords": (100700, -164, 4784),
        "extra_data": {"x_min": 70000,
                       "x_max": 101000,
                       "conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE Pyramid": {
        "return_name": "Max's Exit",
        "entrance_region": "ruins se outside max",
        "exit_region": "max",
        "entrance": (0x12, 0x3, 0x1),
        "exit": (0x23, 0x0, 0x1),
        "extra_data": {"conditional": ["ruins_water"]},
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE King's Road North": {
        "return_name": "Ruins NE King's Road South",
        "entrance_region": "ruins se path to temple",
        "exit_region": "ruins ne geozards",
        "entrance": (0x12, 0x3, 0xFC),
        "exit": (0x12, 0x2, 0xFB),
        "coords": (123000, -164, 4784),
        "extra_data": {"x_max": 140000,
                       "x_min": 101000,
                       "conditional": ["ruins_water"]},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.RUINS
    },

    # ========== Mutoh's Temple ============
    "Ruins Enter Temple": {
        "return_name": "MT Exit",
        "entrance": (0x12, 0x2, 0x2),
        "exit": (0x21, 0x0, 0x1),
        "entrance_region": "ruins ne outside temple",
        "exit_region": "mutoh",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "MT Enter Boss": {
        "return_name": "Eox Exit",
        "entrance": (0x21, 0x5, 0x2),
        "exit": (0x2F, 0x0, 0x1),
        "entrance_region": "mutoh before eox",
        "exit_region": "mutoh eox",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "MT Eox Warp": {
        "entrance": (0x21, 0x6, 0x0),
        "exit": (0x12, 0x2, 0x2),
        "entrance_region": "mutoh eox",
        "exit_region": "ruins ne outside temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.RUINS
    },
#
#     # ============= SW Ocean ==================
#
    "Ocean SW Mercay": {
        "return_name": "Mercay SE Boat",
        "entrance": (0x0, 0x0, 0x2),
        "exit": (0xB, 0x3, 0x2),
        "entrance_region": "mercay boat",
        "exit_region": "mercay se",
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.MERCAY,
    },
    "Ocean SW Cannon": {
        "return_name": "Cannon Boat",
        "entrance_region": "cannon boat",
        "exit_region": "cannon island",
        "entrance": (0x0, 0x0, 0x4),
        "exit": (0x13, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.CANNON,
    },
    "Ocean SW Ember": {
        "return_name": "Ember Boat",
        "entrance_region": "ember boat",
        "exit_region": "ember port",
        "entrance": (0x0, 0x0, 0x3),
        "exit": (0xD, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.EMBER,
    },
    "Ocean SW Molida": {
        "return_name": "Molida Boat",
        "entrance_region": "molida boat",
        "exit_region": "molida island",
        "entrance": (0x0, 0x0, 0x1),
        "exit": (0xC, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.MOLIDA,
    },
    "Ocean SW Spirit": {
        "return_name": "Spirit Boat",
        "entrance_region": "spirit boat",
        "exit_region": "spirit island",
        "entrance": (0x0, 0x0, 0x5),
        "exit": (0x17, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.SPIRIT,
    },

    # ============= NW Ocean ==================

    "Ocean NW Gust": {
        "return_name": "Gust Boat",
        "entrance_region": "gust boat",
        "exit_region": "gust south",
        "entrance": (0x0, 0x1, 0x0),
        "exit": (0xE, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.GUST,
    },
    "Ocean NW Bannan": {
        "return_name": "Bannan Boat",
        "entrance_region": "bannan boat",
        "exit_region": "bannan",
        "entrance": (0x0, 0x1, 0x3),
        "exit": (0x14, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.BANNAN,
    },
    "Ocean NW Zauz": {
        "return_name": "Zauz Boat",
        "entrance_region": "zauz boat",
        "exit_region": "zauz",
        "entrance": (0x0, 0x1, 0x4),
        "exit": (0x16, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.ZAUZ,
    },
    "Ocean NW Uncharted": {
        "return_name": "Uncharted Boat",
        "entrance_region": "uncharted boat",
        "exit_region": "uncharted",
        "entrance": (0x0, 0x1, 0x7),
        "exit": (0x1A, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.UNCHARTED,
    },

    # ========== Ghost Ship ==========
    "Board Ghost Ship": {
        "return_name": "GS Exit",
        "entrance": (0, 0x1, 0xFA),
        "exit": (0x29, 0x3, 0x0),
        "extra_data": {"ship_exit": 5},
        "entrance_region": "nw ocean",
        "exit_region": "ghost ship deck",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST
    },
    "Ghost Ship 1F Descend": {
        "return_name": "Ghost Ship B1 Ascend",
        "entrance": (0x29, 0x3, 0x1),
        "exit": (0x29, 0x0, 0x1),
        "entrance_region": "ghost ship deck",
        "exit_region": "ghost ship",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST
    },
    "Finish Ghost Ship": {
        "entrance": (0x4, 0x0, 0x0),
        "exit": (0x0, 0x1, 0x5),
        "entrance_region": "ghost ship tetra",
        "exit_region": "nw ocean",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST,
        "two_way": False,
    },
    "Ghost Ship Cubus Sisters Reunion": {
        "return_name": "Cubus Sisters Blue Warp",
        "entrance": (0x29, 0x0, 0x3),
        "exit": (0x30, 0x0, 0x1),
        "entrance_region": "ghost ship b3",
        "exit_region": "ghost ship cubus",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST,
    },

    # ============= SE Ocean ==================

    "Ocean SE Goron": {
        "return_name": "Goron Boat",
        "entrance_region": "goron boat",
        "exit_region": "goron sw",
        "entrance": (0x0, 0x2, 0x2),
        "exit": (0x10, 0x2, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.GORON,
    },
    "Ocean SE Harrow": {
        "return_name": "Harrow Boat",
        "entrance_region": "harrow boat",
        "exit_region": "harrow",
        "entrance": (0x0, 0x2, 0x4),
        "exit": (0x18, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.NONE,
    },
    "Ocean SE Dee Ess": {
        "return_name": "Dee Ess Boat",
        "entrance_region": "ds boat",
        "exit_region": "ds",
        "entrance": (0x0, 0x2, 0x5),
        "exit": (0x1B, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.NONE,
    },
    "Ocean SE Frost": {
        "return_name": "Frost Boat",
        "entrance_region": "frost boat",
        "exit_region": "frost",
        "entrance": (0x0, 0x2, 0x3),
        "exit": (0xF, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.FROST,
    },

    # ============= NE Ocean ==================

    "Ocean NE IotD": {
        "return_name": "IotD Boat",
        "entrance_region": "dead boat",
        "exit_region": "iotd port",
        "entrance": (0x0, 0x3, 0x1),
        "exit": (0x15, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.DEAD,
    },
    "Ocean NE Ruins": {
        "return_name": "Ruins Boat",
        "entrance_region": "ruins boat",
        "exit_region": "ruins port",
        "entrance": (0x0, 0x3, 0x2),
        "exit": (0x11, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.RUINS,
    },
    "Ocean NE Maze": {
        "return_name": "Maze Boat",
        "entrance_region": "maze boat",
        "exit_region": "maze",
        "entrance": (0x0, 0x3, 0x3),
        "exit": (0x19, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.NONE,
    },
    # Don't move until future versions ~
    # TotOK shortcuts
    "TotOK B3.5 Blue Warp": {
        "return_name": "TotOK B3.5 Warp Exit",
        "entrance_region": "totok b35",
        "exit_region": "totok",
        "entrance": (0x25, 0x4, 0x3),
        "exit": (0x26, 0x0, 0x3),
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
        "two_way": False
    },
    "TotOK B6.5 Yellow Warp": {
        "return_name": "TotOK Lobby Yellow Warp",
        "entrance_region": "totok midway",
        "exit_region": "totok",
        "entrance": (0x25, 0x9, 0x2),
        "exit": (0x26, 0x0, 0x6),
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
    },
    "TotOK B9.5 Blue Warp": {
        "return_name": "TotOK 9.5 Warp Exit",
        "entrance_region": "totok b10",
        "exit_region": "totok",
        "entrance": (0x25, 0xD, 0x2),
        "exit": (0x26, 0x0, 0x3),
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
        "two_way": False
    },
    "TotOK B9.5 Descend": {
        "return_name": "TotOK B10 Cave",
        "entrance_region": "totok b95",
        "exit_region": "totok b10",
        "entrance": (0x25, 0xD, 0x1),
        "exit": (0x25, 0xE, 0x0),
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
    },
    "TotOK CC Room Warp": {
        "return_name": "TotOK CC Warp Reverse",
        "entrance_region": "totok b6 crest",
        "exit_region": "totok",
        "entrance": (0x25, 0x8, 0x1),
        "exit": (0x26, 0x0, 0x3),
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
    },
    "TotOK B6 Exit CC Room": {
        "return_name": "TotOK B6 Red Door Hourglass",
        "entrance_region": "totok b6 crest",
        "exit_region": "totok b6",
        "entrance": (0x25, 0x8, 0x0),
        "exit": (0x25, 0x7, 0x1),
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.MERCAY,
    },
    # ==== Mercay OOB =====
    "Mercay SW OOB North Upper": {
        "return_name": "Mercay NW OOB South Upper",
        "entrance_region": "mercay sw oob high",
        "exit_region": "mercay nw oob high",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-85000, 14582, -5000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True,
                       "x_max": -30000,},
    },
    "Mercay SW OOB North Waterfall": {
        "return_name": "Mercay NW OOB South Waterfall",
        "entrance_region": "mercay sw oob east",
        "exit_region": "mercay nw oob high",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-14000, 14582, -5000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True,
                       "x_min": -30000, },
    },
    "Mercay SW OOB East": {
        "return_name": "Mercay SE OOB West",
        "entrance_region": "mercay sw oob east",
        "exit_region": "mercay se oob",
        "entrance": (0xB, 0x0, 0xFD),
        "exit": (0xB, 0x3, 0xFE),
        "coords": (5000, 14582, 25000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True},
    },
    "Mercay NW OOB East": {
        "return_name": "Mercay NE OOB West",
        "entrance_region": "mercay nw oob high",
        "exit_region": "mercay ne oob",
        "entrance": (0xB, 0x1, 0xFD),
        "exit": (0xB, 0x2, 0xFE),
        "coords": (5000, 14582, -8000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True},
    },
    "Mercay SE OOB North": {
        "return_name": "Mercay NE OOB South",
        "entrance_region": "mercay se oob",
        "exit_region": "mercay ne oob",
        "entrance": (0xB, 0x3, 0xFC),
        "exit": (0xB, 0x2, 0xFB),
        "coords": (10000, 14582, -5000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True},
    },
    "Mercay SW OOB North Lower": {
        "return_name": "Mercay NW OOB South Lower",
        "entrance_region": "mercay sw oob low",
        "exit_region": "mercay nw oob low",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-140000, 4751, -5000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True},
    },
}




ENTRANCES: dict[str, "PHTransition"] = PHTransition.from_data(ENTRANCE_DATA)
counter = {}
i = 0
entrance_id_to_region = {d.id: d.entrance_region for d in ENTRANCES.values()}

# print({key: value for key, value in counter.items() if value != 1})



if __name__ == "__main__":
    sorted_entrances = sorted(ENTRANCES, key=lambda x: (ENTRANCES[x].island, ENTRANCES[x].category_group, ENTRANCES[x].direction, ENTRANCES[x].name))
    for name in sorted_entrances:
        if not "Unnamed" in name:
            print(name)


    # for name, data in ENTRANCES.items():
    #     print(f"{name}:", "{")
    #     for k, v in data.items():
    #         print(f"\t{k}: {v}")
    #     print("},")
