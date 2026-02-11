
if __name__ == "__main__":
    from worlds.tloz_ph.Subclasses import PHTransition, EntranceGroups
else:
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
        "entrance_region": "Mercay SW",
        "exit_region": "Oshus' House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "two_way": True,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW Apricot's House": {
        "return_name": "Apricot's Exit",
        "entrance": (0xB, 0x0, 3),
        "exit": (0xB, 0xB, 1),
        "entrance_region": "Mercay SW",
        "exit_region": "Apricot's House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "two_way": True,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW Barrel Cave": {
        "return_name": "Sword Cave Exit",
        "entrance": (0xB, 0x0, 4),
        "exit": (0xB, 0x13, 1),
        "entrance_region": "Mercay SW",
        "exit_region": "Sword Cave",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW North": {
        "return_name": "Mercay NW South",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-164000, -164, 16000),  # The coord that doesn't matter doesn't matter. Y level diferentiates exit
        "entrance_region": "Mercay SW",
        "exit_region": "Mercay NW Chus",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SW East": {
        "return_name": "Mercay SE West",
        "entrance": (0xB, 0x0, 0xFD),
        "exit": (0xB, 0x3, 0xFE),
        "coords": (4780, -164, 53300),
        "entrance_region": "Mercay SW Bridge",
        "exit_region": "Mercay SE",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Milk Bar": {
        "return_name": "Milk Bar Exit",
        "entrance": (0xB, 0x3, 0x3),
        "exit": (0xB, 0xC, 0x0),
        "entrance_region": "Mercay SE",
        "exit_region": "Milk Bar",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Shipyard": {
        "return_name": "Shipyard Exit",
        "entrance": (0xB, 0x3, 0x4),
        "exit": (0xB, 0xD, 0x0),
        "entrance_region": "Mercay SE Shipyard",
        "exit_region": "Shipyard",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Tuzi's House": {
        "return_name": "Tuzi's Exit",
        "entrance": (0xB, 0x3, 0x5),
        "exit": (0xB, 0xE, 0x0),
        "entrance_region": "Mercay SE",
        "exit_region": "Tuzi's House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Treasure Teller": {
        "return_name": "Treasure Teller's Exit",
        "entrance": (0xB, 0x3, 0x6),
        "exit": (0xB, 0xF, 0x0),
        "entrance_region": "Mercay SE Treasure Teller",
        "exit_region": "Treasure Teller",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Shop": {
        "return_name": "Mercay Shop Exit",
        "entrance": (0xB, 0x3, 0x7),
        "exit": (0xB, 0x11, 0x1),
        "entrance_region": "Mercay SE",
        "exit_region": "Mercay Shop",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE North": {
        "return_name": "Mercay NE South",
        "entrance_region": "Mercay SE",
        "exit_region": "Mercay NE",
        "entrance": (0xB, 0x3, 0xFC),
        "exit": (0xB, 0x2, 0xFB),
        "coords": (131000, -164, -4815),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE West": {
        "return_name": "Mercay NW East",
        "entrance_region": "Mercay NE",
        "exit_region": "Mercay NW Temple",
        "entrance": (0xB, 0x2, 0xFE),
        "exit": (0xB, 0x1, 0xFD),
        "coords": (-4815, 9666, -60000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.LEFT,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NW Temple Cave": {
        "return_name": "Eye Bridge Cave North Exit",
        "entrance_region": "Mercay NW Temple",
        "exit_region": "Eye Bridge Cave North",
        "entrance": (0xB, 0x1, 0x3),
        "exit": (0xB, 0x10, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE Ledge Cave": {
        "return_name": "Eye Bridge Cave South Exit",
        "entrance_region": "Mercay NE Ledge",
        "exit_region": "Eye Bridge Cave South",
        "entrance": (0xB, 0x2, 0x1),
        "exit": (0xB, 0x10, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Ledge North": {
        "return_name": "Mercay NE Ledge South",
        "entrance_region": "Mercay SE Ledge",
        "exit_region": "Mercay NE Ledge",
        "entrance": (0xB, 0x3, 0xFC),
        "exit": (0xB, 0x2, 0xFB),
        "coords": (110000, 9666, -4815),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE Hidden Cave": {
        "return_name": "Long Bridge Cave West",
        "entrance_region": "Mercay NE",
        "exit_region": "Long Bridge Cave",
        "entrance": (0xB, 0x2, 0x2),
        "exit": (0xB, 0x12, 0x3),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NE Freedle Island Cave": {
        "return_name": "Long Bridge Cave East",
        "entrance_region": "Mercay NW Freedle Island",
        "exit_region": "Long Bridge Cave",
        "entrance": (0xB, 0x2, 0x3),
        "exit": (0xB, 0x12, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mercay SE Cave": {
        "return_name": "Mountain Passage 2F Exit",
        "entrance_region": "Mercay SE",
        "exit_region": "Mountain Passage 4",
        "entrance": (0xB, 0x3, 0x1),
        "exit": (0x27, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "Mountain Passage 1F Staircase": {
        "return_name": "Mountain Passage 2F Staircase",
        "entrance_region": "Mountain Passage 2 Exit",
        "exit_region": "Mountain Passage 3",
        "entrance": (0x27, 0x0, 0x2),
        "exit": (0x27, 0x1, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY
    },
    "Mercay NW Bamboo Cave": {
        "return_name": "Mountain Passage 1F Exit",
        "entrance_region": "Mercay NW Bamboo",
        "exit_region": "Mountain Passage 1",
        "entrance": (0xB, 0x1, 0x1),
        "exit": (0x27, 0x0, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    # OOB
    "Mercay SW OOB North Upper": {
        "return_name": "Mercay NW OOB South Upper",
        "entrance_region": "Mercay SW OoB High",
        "exit_region": "Mercay NW OoB High",
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
        "entrance_region": "Mercay SW OoB East",
        "exit_region": "Mercay NW OoB High",
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
        "entrance_region": "Mercay SW OoB East",
        "exit_region": "Mercay SE OoB",
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
        "entrance_region": "Mercay NW OoB High",
        "exit_region": "Mercay NE OoB",
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
        "entrance_region": "Mercay SE OoB",
        "exit_region": "Mercay NE OoB",
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
        "entrance_region": "Mercay SW OoB Low",
        "exit_region": "Mercay NW OoB Low",
        "entrance": (0xB, 0x0, 0xFC),
        "exit": (0xB, 0x1, 0xFB),
        "coords": (-140000, 4751, -5000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MERCAY,
        "extra_data": {"glitched": True},
    },

    # =========== TotOK ==============
    "Mercay NW Enter Temple": {
        "return_name": "TotOK Lobby Exit",
        "entrance": (0xB, 0x1, 0x2),
        "exit": (0x26, 0x00, 0x1),
        "entrance_region": "Mercay NW Temple",
        "exit_region": "TotOK Lobby",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MERCAY
    },
    "TotOK B3.5 Blue Warp": {
        "return_name": "TotOK B3.5 Warp Exit",
        "entrance_region": "TotOK B3.5",
        "exit_region": "TotOK Lobby",
        "entrance": (0x25, 0x4, 0x3),
        "exit": (0x26, 0x0, 0x3),
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
        "two_way": False
    },
    "TotOK B6.5 Yellow Warp": {
        "return_name": "TotOK Lobby Yellow Warp",
        "entrance_region": "TotOK B6 Midway",
        "exit_region": "TotOK Lobby",
        "entrance": (0x25, 0x9, 0x2),
        "exit": (0x26, 0x0, 0x6),
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
    },
    "TotOK B9.5 Blue Warp": {
        "return_name": "TotOK 9.5 Warp Exit",
        "entrance_region": "TotOK B10",
        "exit_region": "TotOK Lobby",
        "entrance": (0x25, 0xD, 0x2),
        "exit": (0x26, 0x0, 0x3),
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
        "two_way": False
    },
    "TotOK B9.5 Descend": {
        "return_name": "TotOK B10 Cave",
        "entrance_region": "TotOK B9.5",
        "exit_region": "TotOK B10",
        "entrance": (0x25, 0xD, 0x1),
        "exit": (0x25, 0xE, 0x0),
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
    },
    "TotOK CC Room Warp": {
        "return_name": "TotOK CC Warp Reverse",
        "entrance_region": "TotOK B6 Crest",
        "exit_region": "TotOK Lobby",
        "entrance": (0x25, 0x8, 0x1),
        "exit": (0x26, 0x0, 0x3),
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MERCAY,
    },
    "TotOK B6 Exit CC Room": {
        "return_name": "TotOK B6 Red Door Hourglass",
        "entrance_region": "TotOK B6 Crest",
        "exit_region": "TotOK B6",
        "entrance": (0x25, 0x8, 0x0),
        "exit": (0x25, 0x7, 0x1),
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.MERCAY,
    },
    # ========== Cannon ==========
    "Cannon Workshop East": {
        "return_name": "Eddo's Exit",
        "entrance_region": "Cannon Outside Eddo",
        "exit_region": "Eddo's Workshop",
        "entrance": (0x13, 0x0, 0x4),
        "exit": (0x13, 0xB, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Cannon Workshop West": {
        "return_name": "Fuzo's Exit",
        "entrance_region": "Cannon Island",
        "exit_region": "Fuzo's Workshop",
        "entrance": (0x13, 0x0, 0x3),
        "exit": (0x13, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Fuzo's Interior Door": {
        "return_name": "Eddo's Interior Door",
        "entrance_region": "Fuzo's Workshop",
        "exit_region": "Eddo's Workshop",
        "entrance": (0x13, 0xA, 0x1),
        "exit": (0x13, 0xB, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Cannon Bee Cave": {
        "return_name": "Bomb Flower Cave Exit",
        "entrance_region": "Cannon Island",
        "exit_region": "Bomb Flower Cave South",
        "entrance": (0x13, 0x0, 0x1),
        "exit": (0x28, 0x0, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.CANNON
    },
    "Cannon Bomb Garden Cave": {
        "return_name": "Bomb Flower Cave Staircase",
        "entrance_region": "Cannon Bomb Garden",
        "exit_region": "Bomb Flower Cave North",
        "entrance": (0x13, 0x0, 0x2),
        "exit": (0x28, 0x0, 0x1),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.CANNON
    },

    # =========== Ember Island ================
    "Ember West Port House": {
        "return_name": "Abandoned House Exit",
        "entrance": (0xD, 0x0, 0x2),
        "exit": (0xD, 0xB, 0x0),
        "entrance_region": "Ember Port",
        "exit_region": "Abandoned House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "Ember West Astrid's House": {
        "return_name": "Astrid's Exit",
        "entrance": (0xD, 0x0, 0x1),
        "exit": (0xD, 0xA, 0x0),
        "entrance_region": "Ember Port",
        "exit_region": "Astrid's House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "Astrid's Stairs": {
        "return_name": "Astrid's Basement Stairs",
        "entrance": (0xD, 0xA, 0x1),
        "exit": (0xD, 0x14, 0x0),
        "entrance_region": "Astrid's House",
        "exit_region": "Astrid's Basement",
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.EMBER
    },
    "Ember West Kayo's House": {
        "return_name": "Kayo's Exit",
        "entrance": (0xD, 0x0, 0x3),
        "exit": (0xD, 0xC, 0x0),
        "entrance_region": "Ember Port",
        "exit_region": "Kayo's House",
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
        "entrance_region": "Ember Port",
        "exit_region": "Ember Coast East",
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
        "entrance_region": "Ember Coast North",
        "exit_region": "Ember Coast East",
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
        "entrance_region": "Ember Port",
        "exit_region": "Ember Climb East",
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
        "entrance_region": "Ember Climb West",
        "exit_region": "Ember Coast East",
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
        "entrance_region": "Ember Climb West",
        "exit_region": "Ember Outside Temple",
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
        "entrance_region": "Ember Summit West",
        "exit_region": "Ember Outside Temple",
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
        "entrance_region": "Ember Summit West",
        "exit_region": "Ember Summit North",
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
        "entrance_region": "Ember Summit West",
        "exit_region": "Ember Summit East",
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.EMBER
    },

    # ========== Temple of Fire ============
    "Ember Enter Temple": {
        "return_name": "ToF Exit",
        "entrance": (0xD, 0x1, 0x0),
        "exit": (0x1C, 0x0, 0x0),
        "entrance_region": "Ember Outside Temple",
        "exit_region": "ToF 1F",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
        },
    "ToF Enter Boss": {
        "return_name": "Blaaz Exit",
        "entrance": (0x1C, 0x3, 0x1),
        "exit": (0x2B, 0x0, 0x0),
        "entrance_region": "ToF 4F",
        "exit_region": "Blaaz",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.EMBER
    },
    "ToF Blaaz Warp": {
        "entrance": (0x2B, 0x0, 0x0),
        "exit": (0xD, 0x1, 0x1),
        "entrance_region": "Blaaz",
        "exit_region": "Ember Outside Temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.EMBER
    },
    # ========== Molida ============
    "Molida South Ocara's House": {
        "return_name": "Ocara's House Exit",
        "entrance": (0xC, 0x0, 0x4),
        "exit": (0xC, 0xC, 0x1),
        "entrance_region": "Molida South",
        "exit_region": "Ocara's House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Sun Lake Cave Geozard Cave": {
        "return_name": "Octorok Cave East",
        "entrance_region": "Sun Lake Cave Post Geozard",
        "exit_region": "Octorok Cave",
        "entrance": (0xC, 0xA, 0x6),
        "exit": (0xC, 0xF, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Sun Lake Cave Back Cave": {
        "return_name": "Octorok Cave West",
        "entrance_region": "Sun Lake Cave Back",
        "exit_region": "Octorok Cave",
        "entrance": (0xC, 0xA, 0x7),
        "exit": (0xC, 0xF, 0x3),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Sun Lake Cave Bomb Cave": {
        "return_name": "Shovel Hideout Exit",
        "entrance_region": "Sun Lake Cave Back",
        "exit_region": "Shovel Hideout",
        "entrance": (0xC, 0xA, 0x5),
        "exit": (0xC, 0xF, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Sun Lake Cave Staircase": {
        "return_name": "Molida North Cliff Staircase",
        "entrance_region": "Sun Lake Cave Back",
        "exit_region": "Molida Cliff North",
        "entrance": (0xC, 0xA, 0x1),
        "exit": (0xC, 0x1, 0x1),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Cliff North": {
        "return_name": "Molida North Cliff South",
        "entrance_region": "Molida Cliff South",
        "exit_region": "Molida Cliff North",
        "entrance": (0xC, 0x0, 0xFC),
        "exit": (0xC, 0x1, 0xFB),
        "coords": (80000, 4751, -4815),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Romanos' House": {
        "return_name": "Romanos' Exit",
        "entrance_region": "Molida South",
        "exit_region": "Romanos' House",
        "entrance": (0xC, 0x0, 0x3),
        "exit": (0xC, 0xB, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Shop": {
        "return_name": "Molida Shop Exit",
        "entrance_region": "Molida South",
        "exit_region": "Molida Shop",
        "entrance": (0xC, 0x0, 0x6),
        "exit": (0xC, 0xE, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Potato's House": {
        "return_name": "Potato's Exit",
        "entrance_region": "Molida South",
        "exit_region": "Potato's house",
        "entrance": (0xC, 0x0, 0x5),
        "exit": (0xC, 0xD, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Cave": {
        "return_name": "Sun Lake Cave Exit",
        "entrance_region": "Molida South",
        "exit_region": "Sun Lake Cave",
        "entrance": (0xC, 0x0, 0x2),
        "exit": (0xC, 0xA, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "Sun Lake Cave Sun Staircase": {
        "return_name": "Molida North Staircase",
        "entrance_region": "Sun Lake Cave Sun Door",
        "exit_region": "Molida North",
        "entrance": (0xC, 0xA, 0x4),
        "exit": (0xC, 0x1, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.MOLIDA
    },
    "Molida South Dig Hole": {
        "return_name": "Sun Lake Cave South Drop",
        "two_way": False,
        "entrance_region": "Molida South",
        "exit_region": "Sun Lake Cave Upper",
        "entrance": (0xC, 0x0, 0x0),
        "exit": (0xC, 0xA, 0x3),
        "type": EntranceGroups.HOLES,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MOLIDA
    },
    "Molida North Dig Hole": {
        "return_name": "Sun Lake Cave Chest Drop",
        "two_way": False,
        "entrance_region": "Molida North",
        "exit_region": "Sun Lake Cave North Drop",
        "entrance": (0xC, 0x1, 0x2),
        "exit": (0xC, 0xA, 0x8),
        "type": EntranceGroups.HOLES,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.MOLIDA
    },

    # ========== Temple of Courage ============
    "Molida North Enter Temple": {
        "return_name": "ToC Exit",
        "entrance": (0xC, 0x1, 0x3),
        "exit": (0x1E, 0x0, 0x0),
        "entrance_region": "Molida Outside Temple",
        "exit_region": "ToC 1F",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "ToC Enter Boss": {
        "return_name": "Crayk Exit",
        "entrance": (0x1E, 0x3, 0x3),
        "exit": (0x2C, 0x0, 0x2),
        "entrance_region": "ToC 3F",
        "exit_region": "Crayk",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.MOLIDA
    },
    "ToC Crayk Warp": {
        "entrance": (0x2C, 0x0, 0x0),
        "exit": (0xC, 0x1, 0x4),
        "entrance_region": "Crayk",
        "exit_region": "Molida Outside Temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.MOLIDA
    },

    # ========== Spirit ============
    "Spirit Island Cave": {
        "return_name": "Spirit Shrine Exit",
        "entrance_region": "Spirit Island",
        "exit_region": "Spirit Shrine",
        "entrance": (0x17, 0x0, 0x1),
        "exit": (0x17, 0x1, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.SPIRIT
    },

    # ========== Gust ============
    "Gust SW Coast North": {
        "return_name": "Gust NW Coast South",
        "entrance_region": "Gust South NW Ledge",
        "exit_region": "Gust North",
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
        "entrance_region": "Gust South NW",
        "exit_region": "Gust North Above Temple",
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
        "entrance_region": "Gust South Cliffs",
        "exit_region": "Gust North Above Temple",
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
        "entrance_region": "Gust South Cliffs",
        "exit_region": "Gust North Temple Road",
        "entrance": (0xE, 0x0, 0xFC),
        "exit": (0xE, 0x1, 0xFB),
        "coords": (4452, 4751, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GUST
    },
    "Gust Cave East": {
        "return_name": "Miniblin Cave East",
        "entrance_region": "Gust South Cliffs",
        "exit_region": "Miniblin Cave",
        "entrance": (0xE, 0x0, 0x4),
        "exit": (0xE, 0xB, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },
    "Gust Cave West": {
        "return_name": "Miniblin Cave West",
        "entrance_region": "Gust South",
        "exit_region": "Miniblin Cave",
        "entrance": (0xE, 0x0, 0x3),
        "exit": (0xE, 0xB, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },
    "Gust Secret Cave": {
        "return_name": "Tiled Hideout Exit",
        "entrance_region": "Gust South",
        "exit_region": "Tiled Hideout",
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
        "entrance_region": "Gust North Outside Temple",
        "exit_region": "ToW 1F",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
        },
    "ToW Enter Boss": {
        "return_name": "Cyclok Exit",
        "entrance": (0x1D, 0x4, 0x1),
        "exit": (0x2A, 0x0, 0x1),
        "entrance_region": "ToW 2F",
        "exit_region": "Cyclok",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GUST
    },
    "ToW Cyclok Warp": {
        "entrance": (0x2A, 0x0, 0x0),
        "exit": (0xE, 0x1, 0x0),
        "entrance_region": "Post Cyclok",
        "exit_region": "Gust North Outside Temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.GUST
    },

    # ========== Bannan ============
    "Bannan West Hut": {
        "return_name": "Wayfarer's Exit",
        "entrance_region": "Bannan Island",
        "exit_region": "Wayfarer's House",
        "entrance": (0x14, 0x0, 0x2),
        "exit": (0x14, 0x1, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.BANNAN
    },
    "Bannan West Cave": {
        "return_name": "Keese Passage West Exit",
        "entrance_region": "Bannan Island",
        "exit_region": "Keese Passage West",
        "entrance": (0x14, 0x0, 0x5),
        "exit": (0x14, 0xA, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.BANNAN
    },
    "Bannan East Cave": {
        "return_name": "Keese Passage East Exit",
        "entrance_region": "Bannan East",
        "exit_region": "Keese Passage East",
        "entrance": (0x14, 0x0, 0x4),
        "exit": (0x14, 0xA, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.BANNAN
    },

    # ===== Zauz =====
    "Zauz' House": {
        "return_name": "Zauz' Exit",
        "entrance_region": "Zauz's Island",
        "exit_region": "Zauz's House",
        "entrance": (0x16, 0x0, 0x2),
        "exit": (0x16, 0xA, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.ZAUZ
    },

    # ===== Uncharted =====
    "Uncharted Cave": {
        "return_name": "Descending Cave Exit",
        "entrance_region": "Uncharted Outside Cave",
        "exit_region": "Descending Cave",
        "entrance": (0x1A, 0x0, 0x2),
        "exit": (0x1A, 0xA, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.UNCHARTED
    },
    "Descending Cave Lower Cave": {
        "return_name": "Golden Chief Exit",
        "entrance_region": "Descending Cave",
        "exit_region": "Golden Chief Cave",
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
        "entrance_region": "Goron SW",
        "exit_region": "Goron House Zero Rocks",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SE Mountain House": {
        "return_name": "Goron Mountain House Exit",
        "entrance_region": "Goron SE NW",
        "exit_region": "Goron House Right Rock",
        "entrance": (0x10, 0x3, 0x2),
        "exit": (0x10, 0xF, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Chu House": {
        "return_name": "Goron Chu House Exit",
        "entrance_region": "Goron SW",
        "exit_region": "Goron House Left Rock",
        "entrance": (0x10, 0x2, 0x3),
        "exit": (0x10, 0xD, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Rock House": {
        "return_name": "Goron Rock House Exit",
        "entrance_region": "Goron SW",
        "exit_region": "Goron House Three Rocks",
        "entrance": (0x10, 0x2, 0x2),
        "exit": (0x10, 0xC, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Shop": {
        "return_name": "Goron Shop Exit",
        "entrance_region": "Goron SW",
        "exit_region": "Goron Shop",
        "entrance": (0x10, 0x2, 0x4),
        "exit": (0x10, 0x14, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW North": {
        "return_name": "Goron NW South",
        "entrance_region": "Goron SW",
        "exit_region": "Goron NW Shortcut",
        "entrance": (0x10, 0x2, 0xFC),
        "exit": (0x10, 0x0, 0xFB),
        "coords": (-140000, 9666, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GORON
    },
    "Goron SE Coast House": {
        "return_name": "Goron Coast House Exit",
        "entrance_region": "Goron SE",
        "exit_region": "Goron House Two Rocks",
        "entrance": (0x10, 0x3, 0x1),
        "exit": (0x10, 0xE, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SE Chief House": {
        "return_name": "Goron Chief House Exit",
        "entrance_region": "Goron SE",
        "exit_region": "Goron Chief House",
        "entrance": (0x10, 0x3, 0x0),
        "exit": (0x10, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "Goron SW Coast East": {
        "return_name": "Goron SE Coast West",
        "entrance_region": "Goron SW",
        "exit_region": "Goron SE NW",
        "entrance": (0x10, 0x2, 0xFD),
        "exit": (0x10, 0x3, 0xFE),
        "coords": (-8000, 4751, 70000),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron SW Mountains East": {
        "return_name": "Goron SE Mountains West",
        "entrance_region": "Goron SW Chu Ledge",
        "exit_region": "Goron SE NW",
        "entrance": (0x10, 0x2, 0xFD),
        "exit": (0x10, 0x3, 0xFE),
        "coords": (-8000, 9666, 22500),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.GORON
    },
    "Goron SE North": {
        "return_name": "Goron NE South",
        "entrance_region": "Goron SE",
        "exit_region": "Goron NE",
        "entrance": (0x10, 0x3, 0xFC),
        "exit": (0x10, 0x1, 0xFB),
        "coords": (148000, 4751, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.GORON
    },
    "Goron South Dead End": {
        "return_name": "Goron NE Mountain West",
        "entrance_region": "Goron NW South Dead End",
        "exit_region": "Goron NE South",
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
        "entrance_region": "Goron NW North Dead End",
        "exit_region": "Goron NE Middle",
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
        "entrance_region": "Goron NW Like Like",
        "exit_region": "Goron NE Coast",
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
        "entrance_region": "Goron NW Like Like",
        "exit_region": "Goron NE Spikes",
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
        "entrance_region": "Goron NW Outside Temple",
        "exit_region": "GT 1F",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "GT Enter Boss": {
        "return_name": "Dongo Exit",
        "entrance": (0x20, 0x4, 0x1),
        "exit": (0x2E, 0x0, 0x0),
        "entrance_region": "GT B4",
        "exit_region": "Dongorongo",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GORON
    },
    "GT Dongo Warp": {
        "entrance": (0x20, 0xA, 0x0),
        "exit": (0x10, 0x0, 0x1),
        "entrance_region": "Post Dongorongo",
        "exit_region": "Goron NW Outside Temple",
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
        "entrance_region": "Frost SW",
        "exit_region": "Smart Anouki's House",
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW Chief House": {
        "return_name": "Anouki Chief's Exit",
        "entrance_region": "Frost SW",
        "exit_region": "Anouki Chief's House",
        "entrance": (0xF, 0x0, 0x1),
        "exit": (0xF, 0xA, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW Sensitive House": {
        "return_name": "Sensitive Anouki's Exit",
        "entrance_region": "Frost SW",
        "exit_region": "Sensitive Anouki's House",
        "entrance": (0xF, 0x0, 0x3),
        "exit": (0xF, 0xC, 0x0),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW North": {
        "return_name": "Frost NW South",
        "entrance_region": "Frost SW",
        "exit_region": "Frost NW",
        "entrance": (0xF, 0x0, 0xFC),
        "exit": (0xF, 0x2, 0xFB),
        "coords": (-120000, -164, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    "Frost NW Dobo's House (SW)": {
        "return_name": "Dobo's Exit",
        "entrance_region": "Frost NW",
        "exit_region": "Dobo's House",
        "entrance": (0xF, 0x2, 0x1),
        "exit": (0xF, 0xD, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Kumu's House (South)": {
        "return_name": "Kumu's Exit",
        "entrance_region": "Frost NW",
        "exit_region": "Kumu's House",
        "entrance": (0xF, 0x2, 0x2),
        "exit": (0xF, 0xE, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Fofo's House (SE)": {
        "return_name": "Fofo's Exit",
        "entrance_region": "Frost NW",
        "exit_region": "Fofo's House",
        "entrance": (0xF, 0x2, 0x3),
        "exit": (0xF, 0xF, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Mazo's House (NE)": {
        "return_name": "Mazo's Exit",
        "entrance_region": "Frost NW",
        "exit_region": "Mazo's House",
        "entrance": (0xF, 0x2, 0x6),
        "exit": (0xF, 0x12, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Aroo's House (North)": {
        "return_name": "Aroo's Exit",
        "entrance_region": "Frost NW",
        "exit_region": "Aroo's House",
        "entrance": (0xF, 0x2, 0x5),
        "exit": (0xF, 0x11, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost NW Gumo's House (NW)": {
        "return_name": "Gumo's Exit",
        "entrance_region": "Frost NW",
        "exit_region": "Gumo's House",
        "entrance": (0xF, 0x2, 0x4),
        "exit": (0xF, 0x10, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SW Cave": {
        "return_name": "Frozen Cave West Exit",
        "entrance_region": "Frost SW",
        "exit_region": "Frozen Cave",
        "entrance": (0xF, 0x0, 0x4),
        "exit": (0xF, 0x13, 0x0),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SE Cave": {
        "return_name": "Frozen Cave East Exit",
        "entrance_region": "Frost SE",
        "exit_region": "Frozen Cave",
        "entrance": (0xF, 0x3, 0x0),
        "exit": (0xF, 0x13, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "Frost SE Upper NE": {
        "return_name": "Frost NE Above Temple SE",
        "entrance_region": "Frost SE Upper East",
        "exit_region": "Frost NE Above Temple East",
        "entrance": (0xF, 0x3, 0xFC),
        "exit": (0xF, 0x1, 0xFB),
        "coords": (202000, 14582, -8192),
        "extra_data": {"x_min": 185000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    "Frost SE Upper NW": {
        "return_name": "Frost NE Above Temple SW",
        "entrance_region": "Frost SE Upper North",
        "exit_region": "Frost NE Above Temple West",
        "entrance": (0xF, 0x3, 0xFC),
        "exit": (0xF, 0x1, 0xFB),
        "coords": (166000, 14582, -8192),
        "extra_data": {"x_max": 185000},
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },
    "Frost SE Lower North": {
        "return_name": "Frost NE Lower South",
        "entrance_region": "Frost SE Exit",
        "exit_region": "Frost NE Outside Arena",
        "entrance": (0xF, 0x3, 0xFC),
        "exit": (0xF, 0x1, 0xFB),
        "coords": (185000, -164, -8192),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.UP,
        "island": EntranceGroups.FROST
    },

    # ========== Temple of Ice ============
    "Frost NE Enter Temple": {
        "return_name": "ToI Exit",
        "entrance": (0xF, 0x1, 0x0),
        "exit": (0x1F, 0x0, 0x0),
        "entrance_region": "Frost NE Outside Temple",
        "exit_region": "ToI 1F",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },
    "ToI Gleeok Warp": {
        "entrance": (0x1f, 0x6, 0x0),
        "exit": (0xF, 0x1, 0x1),
        "entrance_region": "Post Gleeok",
        "exit_region": "Frost NE Outside Temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.FROST
    },
    "ToI 1F Right Staircase": {
        "return_name": "ToI 2F Right Descent",
        "entrance": (0x1f, 0x0, 0x1),
        "exit": (0x1F, 0x3, 0x3),
        "entrance_region": "ToI 1F Ascent",
        "exit_region": "ToI 2F Right",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 2F Right Ascent": {
        "return_name": "ToI 3F Right Staircase",
        "entrance": (0x1f, 0x3, 0x2),
        "exit": (0x1F, 0x1, 0x1),
        "entrance_region": "ToI 2F Right",
        "exit_region": "ToI 3F Right",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 3F Key Door Staircase": {
        "return_name": "ToI 2F Arena Staircase",
        "entrance": (0x1f, 0x2, 0x2),
        "exit": (0x1F, 0x3, 0x1),
        "entrance_region": "ToI 3F Key Door",
        "exit_region": "ToI 2F Arena",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 2F Left Descent": {
        "return_name": "ToI 1F Beetle Staircase",
        "entrance": (0x1f, 0x3, 0x0),
        "exit": (0x1F, 0x0, 0x2),
        "entrance_region": "ToI 2F Left",
        "exit_region": "ToI 1F Beetles",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI 1F Descent": {
        "return_name": "ToI B1 Ascent",
        "entrance": (0x1f, 0x0, 0x3),
        "exit": (0x1F, 0x2, 0x1),
        "entrance_region": "ToI 1F Descent",
        "exit_region": "ToI B1 Ascent",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI B1 Descent": {
        "return_name": "ToI B2 Staircase",
        "entrance": (0x1f, 0x2, 0x2),
        "exit": (0x1F, 0x5, 0x0),
        "entrance_region": "ToI B1 Boss Door",
        "exit_region": "ToI B2",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI B1 Blue Warp": {
        "return_name": "ToI 1F Blue Warp",
        "entrance": (0x1f, 0x2, 0x7),
        "exit": (0x1F, 0x0, 0x4),
        "entrance_region": "ToI B1 Before Boss",
        "exit_region": "ToI Blue Warp",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.FROST
    },
    "ToI Enter Boss": {
        "return_name": "Gleeok Exit",
        "entrance": (0x1f, 0x2, 0x3),
        "exit": (0x2D, 0x0, 0x0),
        "entrance_region": "ToI B1 Before Boss",
        "exit_region": "Gleeok",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.FROST
    },

# ======= Dead=========
    "IotD Port Cave": {
        "return_name": "McNey's Cave East Exit",
        "entrance_region": "IotD Port",
        "exit_region": "McNay's Cave",
        "entrance": (0x15, 0x0, 0x6),
        "exit": (0x15, 0x1, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "McNey's Cave Secret Cave": {
        "return_name": "Rupoor Cave Exit",
        "entrance_region": "McNay's Cave",
        "exit_region": "Rupoor Cave",
        "entrance": (0x15, 0x1, 0x3),
        "exit": (0x15, 0x2, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "IotD Like Like Cave": {
        "return_name": "McNey's Cave West",
        "entrance_region": "Isle of the Dead",
        "exit_region": "McNay's Cave",
        "entrance": (0x15, 0x0, 0x8),
        "exit": (0x15, 0x1, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "Boulder Tunnel Cave": {
        "return_name": "Stone Treasure Cave Exit",
        "entrance_region": "Boulder Tunnel",
        "exit_region": "Stone Treasure Cave",
        "entrance": (0x15, 0x3, 0x3),
        "exit": (0x15, 0x4, 0x1),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "IotD Face Staircase": {
        "return_name": "Boulder Tunnel Staircase",
        "entrance_region": "IotD Face",
        "exit_region": "Boulder Tunnel",
        "entrance": (0x15, 0x0, 0x5),
        "exit": (0x15, 0x3, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.DEAD
    },
    "IotD Pyramid": {
        "return_name": "Brant's Exit",
        "entrance_region": "Isle of the Dead",
        "exit_region": "Brant's Temple",
        "entrance": (0x15, 0x0, 0x3),
        "exit": (0x15, 0x5, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.DEAD
    },
    "IotD Crown Staircase": {
        "return_name": "Brant's Chamber Staircase",
        "entrance_region": "IotD Crown",
        "exit_region": "Brant's Temple",
        "entrance": (0x15, 0x0, 0x4),
        "exit": (0x15, 0xA, 0x2),
        "type": EntranceGroups.STAIRS,
        "direction": EntranceGroups.DOWN,
        "island": EntranceGroups.DEAD
    },
    "IotD Dig Hole": {
        "return_name": "Boulder Tunnel Drop",
        "entrance_region": "Isle of the Dead",
        "exit_region": "Boulder Tunnel",
        "entrance": (0x15, 0x0, 0x0),
        "exit": (0x15, 0x3, 0x1),
        "type": EntranceGroups.HOLES,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.DEAD
    },
    "Brant's Maze 1": {
        "entrance_region": "Brant's Temple",
        "exit_region": "Brant's Temple Maze",
        "entrance": (0x15, 0x5, 0x2),
        "exit": (0x15, 0x6, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "never_shuffle": True,  # Doesn't do anything, isn't needed yet
        "island": EntranceGroups.DEAD
    },
    "Brant's Maze Exit": {
        "entrance_region": "Brant's Temple Maze",
        "exit_region": "Brant's Chamber",
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
        "entrance_region": "Ruins SW Maze Upper",
        "exit_region": "Ruins NW Maze Upper Exit",
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
        "entrance_region": "Ruins SW Maze Lower Exit",
        "exit_region": "Ruins NW Maze Lower Exit",
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
        "entrance_region": "Ruins NW Across Bridge",
        "exit_region": "Ruins NE Enter Upper",
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
        "entrance_region": "Ruins NW Return",
        "exit_region": "Ruins NE Doylan Bridge North",
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
        "entrance_region": "Ruins SW Port Cliff",
        "exit_region": "Ruins NW Port Cliff",
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
        "entrance_region": "Ruins SW Port Cliff",
        "exit_region": "Ruins SE Return Bridge West",
        "entrance": (0x11, 0x0, 0xFD),
        "exit": (0x11, 0x3, 0xFE),
        "coords": (4784, 9666, 51500),
        "type": EntranceGroups.OVERWORLD,
        "direction": EntranceGroups.RIGHT,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Port Cave": {
        "return_name": "Sandy Geozard Cave East",
        "entrance": (0x11, 0x0, 0x2),
        "exit": (0x11, 0xA, 0x1),
        "entrance_region": "Ruins SW Port",
        "exit_region": "Sandy Geozard Cave East",
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Cliff Cave": {
        "return_name": "Sandy Geozard Cave West",
        "entrance_region": "Ruins SW Maze Upper",
        "exit_region": "Sandy Geozard Cave West",
        "entrance": (0x11, 0x0, 0x3),
        "exit": (0x11, 0xA, 0x2),
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SW Maze Lower North": {
        "return_name": "Ruins NW Lower Maze Chest South",
        "entrance_region": "Ruins SW Maze Lower Water",
        "exit_region": "Ruins NW Maze Lower Water",
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
        "entrance_region": "Ruins NW Boulders",
        "exit_region": "Bremeur's Temple",
        "entrance": (0x11, 0x1, 0x1),
        "exit": (0x24, 0x0, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins NW Cave": {
        "return_name": "Grassy Rupee Cave Exit",
        "entrance_region": "Ruins NW Cave",
        "exit_region": "Grassy Treasure Cave",
        "entrance": (0x12, 0x1, 0x2),
        "exit": (0x12, 0xB, 0x1),
        "one_way_data": {"conditional": ["ruins_water"]},
        "type": EntranceGroups.CAVE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins NE Small Pyramid": {
        "return_name": "Doylan's Exit",
        "entrance_region": "Ruins NE Doylan Bridge",
        "exit_region": "Doylan's Temple",
        "entrance": (0x11, 0x2, 0x1),
        "exit": (0x22, 0x0, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Doylan's Staircase": {
        "return_name": "Doylan's Chamber Exit",
        "entrance_region": "Doylan's Temple",
        "exit_region": "Doylan's Chamber",
        "entrance": (0x22, 0x0, 0x2),
        "exit": (0x22, 0x1, 0x1),
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE Coast North": {
        "return_name": "Ruins NE Coast South",
        "entrance_region": "Ruins SE Coast Water",
        "exit_region": "Ruins NE Behind Pyramids Water",
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
        "entrance_region": "Ruins NW Alcove Water",
        "exit_region": "Ruins NE Lower Water South",
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
        "entrance_region": "Ruins NW Lower Water",
        "exit_region": "Ruins NE Lower Water North",
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
        "entrance_region": "Ruins SE Lower Water Bay",
        "exit_region": "Ruins NE Lower Water Bay",
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
        "entrance_region": "Ruins SE Lower Water Wall",
        "exit_region": "Ruins NE Secret Chest Water",
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
        "entrance_region": "Ruins SE Outside Pyramid",
        "exit_region": "Max's Temple",
        "entrance": (0x12, 0x3, 0x1),
        "exit": (0x23, 0x0, 0x1),
        "one_way_data": {"conditional": ["ruins_water"]},
        "type": EntranceGroups.HOUSE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "Ruins SE King's Road North": {
        "return_name": "Ruins NE King's Road South",
        "entrance_region": "Ruins SE King's Road Water",
        "exit_region": "Ruins NE Geozards Water",
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
        "entrance_region": "Ruins NE Outside Temple",
        "exit_region": "MT 1F",
        "one_way_data": {"conditional": ["ruins_water"]},
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "MT Enter Boss": {
        "return_name": "Eox Exit",
        "entrance": (0x21, 0x5, 0x2),
        "exit": (0x2F, 0x0, 0x1),
        "entrance_region": "MT B3",
        "exit_region": "Eox",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.RUINS
    },
    "MT Eox Warp": {
        "entrance": (0x21, 0x6, 0x0),
        "exit": (0x12, 0x2, 0x2),
        "entrance_region": "Post Eox",
        "exit_region": "Ruins NE Outside Temple",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.NONE,
        "two_way": False,
        "island": EntranceGroups.RUINS
    },

   # ============= SW Ocean ==================
    "Ocean SW Mercay": {
        "return_name": "Mercay SE Board Ship",
        "entrance": (0x0, 0x0, 0x2),
        "exit": (0xB, 0x3, 0x2),
        "entrance_region": "Mercay Boat",
        "exit_region": "Mercay SE",
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.MERCAY,
    },
    "Ocean SW Cannon": {
        "return_name": "Cannon Board Ship",
        "entrance_region": "Cannon Boat",
        "exit_region": "Cannon Island",
        "entrance": (0x0, 0x0, 0x4),
        "exit": (0x13, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.CANNON,
    },
    "Ocean SW Ember": {
        "return_name": "Ember West Board Ship",
        "entrance_region": "Ember Boat",
        "exit_region": "Ember Port",
        "entrance": (0x0, 0x0, 0x3),
        "exit": (0xD, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.EMBER,
    },
    "Ocean SW Molida": {
        "return_name": "Molida South Board Ship",
        "entrance_region": "Molida Boat",
        "exit_region": "Molida South",
        "entrance": (0x0, 0x0, 0x1),
        "exit": (0xC, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.MOLIDA,
    },
    "Ocean SW Spirit": {
        "return_name": "Spirit Board Ship",
        "entrance_region": "Spirit Boat",
        "exit_region": "Spirit Island",
        "entrance": (0x0, 0x0, 0x5),
        "exit": (0x17, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.SPIRIT,
    },

    # ============= NW Ocean ==================

    "Ocean NW Gust": {
        "return_name": "Gust South Board Ship",
        "entrance_region": "Gust Boat",
        "exit_region": "Gust South",
        "entrance": (0x0, 0x1, 0x0),
        "exit": (0xE, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.GUST,
    },
    "Ocean NW Bannan": {
        "return_name": "Bannan West Board Ship",
        "entrance_region": "Bannan Boat",
        "exit_region": "Bannan Island",
        "entrance": (0x0, 0x1, 0x3),
        "exit": (0x14, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.BANNAN,
    },
    "Ocean NW Zauz": {
        "return_name": "Zauz Board Ship",
        "entrance_region": "Zauz Boat",
        "exit_region": "Zauz's Island",
        "entrance": (0x0, 0x1, 0x4),
        "exit": (0x16, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.ZAUZ,
    },
    "Ocean NW Uncharted": {
        "return_name": "Uncharted Board Ship",
        "entrance_region": "Uncharted Boat",
        "exit_region": "Uncharted Island",
        "entrance": (0x0, 0x1, 0x7),
        "exit": (0x1A, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.UNCHARTED,
    },

    # ========== Ghost Ship ==========
    "Ocean NW Board Ghost Ship": {
        "return_name": "GS Exit",
        "entrance": (0, 0x1, 0xFA),
        "exit": (0x29, 0x3, 0x0),
        "extra_data": {"ship_exit": 5, "conditional": ["need_sea_chart"]},
        "entrance_region": "Ghost Ship Boat",
        "exit_region": "Ghost Ship 1F",
        "type": EntranceGroups.DUNGEON_ENTRANCE,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST
    },
    "Ghost Ship 1F Descend": {
        "return_name": "Ghost Ship B1 Ascend",
        "entrance": (0x29, 0x3, 0x1),
        "exit": (0x29, 0x0, 0x1),
        "entrance_region": "Ghost Ship 1F",
        "exit_region": "Ghost Ship B1",
        "type": EntranceGroups.DUNGEON_ROOM,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST
    },
    "Finish Ghost Ship": {
        "entrance": (0x4, 0x0, 0x0),
        "exit": (0x0, 0x1, 0x5),
        "entrance_region": "Ghost Ship Tetra",
        "exit_region": "NW Ocean",
        "type": EntranceGroups.WARP_PORTAL,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST,
        "two_way": False,
    },
    "Ghost Ship Cubus Sisters Reunion": {
        "return_name": "Cubus Sisters Blue Warp",
        "entrance": (0x29, 0x0, 0x3),
        "exit": (0x30, 0x0, 0x1),
        "entrance_region": "Ghost Ship Warp",
        "exit_region": "Cubus Sisters",
        "type": EntranceGroups.BOSS,
        "direction": EntranceGroups.INSIDE,
        "island": EntranceGroups.GHOST,
    },

    # ============= SE Ocean ==================

    "Ocean SE Goron": {
        "return_name": "Goron SW Board Ship",
        "entrance_region": "Goron Boat",
        "exit_region": "Goron SW",
        "entrance": (0x0, 0x2, 0x2),
        "exit": (0x10, 0x2, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.GORON,
    },
    "Ocean SE Harrow": {
        "return_name": "Harrow Board Ship",
        "entrance_region": "Harrow Boat",
        "exit_region": "Harrow Island",
        "entrance": (0x0, 0x2, 0x4),
        "exit": (0x18, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.NONE,
    },
    "Ocean SE Dee Ess": {
        "return_name": "Dee Ess Board Ship",
        "entrance_region": "Dee Ess Boat",
        "exit_region": "Dee Ess Island",
        "entrance": (0x0, 0x2, 0x5),
        "exit": (0x1B, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.NONE,
    },
    "Ocean SE Frost": {
        "return_name": "Frost SW Board Ship",
        "entrance_region": "Frost Boat",
        "exit_region": "Frost SW",
        "entrance": (0x0, 0x2, 0x3),
        "exit": (0xF, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.FROST,
    },

    # ============= NE Ocean ==================

    "Ocean NE IotD": {
        "return_name": "IotD Board Ship",
        "entrance_region": "IotD Boat",
        "exit_region": "IotD Port",
        "entrance": (0x0, 0x3, 0x1),
        "exit": (0x15, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.DEAD,
    },
    "Ocean NE Ruins": {
        "return_name": "Ruins SW Board Ship",
        "entrance_region": "Ruins Boat",
        "exit_region": "Ruins SW Port",
        "entrance": (0x0, 0x3, 0x2),
        "exit": (0x11, 0x0, 0x0),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.RUINS,
    },
    "Ocean NE Maze": {
        "return_name": "Maze Board Ship",
        "entrance_region": "Maze Boat",
        "exit_region": "Maze Island",
        "entrance": (0x0, 0x3, 0x3),
        "exit": (0x19, 0x0, 0x1),
        "extra_data": {"conditional": ["need_sea_chart"]},
        "type": EntranceGroups.ISLAND,
        "direction": EntranceGroups.INSIDE,
        "return_island": EntranceGroups.NONE,
    },
}
EVENT_DATA = {
    # Event entrances
    "EVENT: SS Wayfarer Give Wood Heart": {
        "two_way": False,
        "entrance_region": "SS Wayfarer Trade",
        "exit_region": "SS Wayfarer Event",
        "entrance": (0x8, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Bremeur's Temple Lower Water": {
        "two_way": False,
        "entrance_region": "Bremeur's Temple Kings Key",
        "exit_region": "Bremeur's Temple Event",
        "entrance": (0x24, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Goron NE Spike Switch": {
        "two_way": False,
        "entrance_region": "Goron NE South",
        "exit_region": "Goron NE Event",
        "entrance": (0x10, 0x1, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Meet Wayfarer": {
        "two_way": False,
        "entrance_region": "Wayfarer's House",
        "exit_region": "Wayfarer Event",
        "entrance": (0x14, 0x1, 0x0),
        "extra_data": {"shared_event": True},
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Goron SW Kill Yellow Chus": {
        "two_way": False,
        "entrance_region": "Goron Chus",
        "exit_region": "Goron Chus Event",
        "entrance": (0x10, 0x2, 0x0),
        "extra_data": {"shared_event": True},
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Goron SE Shout to Bridge Goron": {
        "two_way": False,
        "entrance_region": "Goron SE NW",
        "exit_region": "Goron SE Bridge Event",
        "entrance": (0x10, 0x3, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    # Goal Events
    "GOAL: Bellumbeck": {
        "two_way": False,
        "entrance_region": "Goal",
        "exit_region": "Goal Event Bellumbeck",
        "entrance": (0x36, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "GOAL: Triforce Door": {
        "two_way": False,
        "entrance_region": "Goal",
        "exit_region": "Goal Event Triforce",
        "entrance": (0x25, 0x9, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "GOAL": {
        "two_way": False,
        "entrance_region": "Goal",
        "exit_region": "Goal Event",
        "entrance": (0xB, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Defeat Blaaz": {
        "two_way": False,
        "entrance_region": "Post Blaaz",
        "exit_region": "Post ToF",
        "extra_data": {"shared_event": True},
        "entrance": (0x2b, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Defeat Cyclok": {
        "two_way": False,
        "entrance_region": "Post Cyclok",
        "exit_region": "Post ToW",
        "extra_data": {"shared_event": True},
        "entrance": (0x2a, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Defeat Crayk": {
        "two_way": False,
        "entrance_region": "Post Crayk",
        "exit_region": "Post ToC",
        "extra_data": {"shared_event": True},
        "entrance": (0x2c, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Rescue Tetra": {
        "two_way": False,
        "entrance_region": "Ghost Ship Tetra",
        "exit_region": "Spawn Pirate Ambush",
        "extra_data": {"shared_event": True},
        "entrance": (0x4, 0x0, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Defeat Dongorongo": {
        "two_way": False,
        "entrance_region": "Post Dongorongo",
        "exit_region": "Post GT",
        "extra_data": {"shared_event": True},
        "entrance": (0x20, 0xa, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Defeat Gleeok": {
        "two_way": False,
        "entrance_region": "Post Gleeok",
        "exit_region": "Post ToI",
        "extra_data": {"shared_event": True},
        "entrance": (0x1f, 0x6, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Defeat Eox": {
        "two_way": False,
        "entrance_region": "Post Eox",
        "exit_region": "Post MT",
        "extra_data": {"shared_event": True},
        "entrance": (0x21, 0x6, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Open Eddo's Door": {
        "two_way": False,
        "entrance_region": "Eddo's Workshop",
        "exit_region": "Eddo Event",
        "entrance": (0x13, 0xB, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
    "EVENT: Gust Windmills": {
        "two_way": False,
        "entrance_region": "Gust North Sandworms",
        "exit_region": "Gust North Event",
        "entrance": (0x13, 0xB, 0x0),
        "type": EntranceGroups.EVENT,
        "direction": EntranceGroups.NONE,
        "island": EntranceGroups.NONE,
    },
}




ENTRANCES: dict[str, "PHTransition"] = PHTransition.from_data(ENTRANCE_DATA | EVENT_DATA)
EVENTS: dict[str, "PHTransition"] = {name: entr for name, entr in ENTRANCES.items() if entr.category_group == EntranceGroups.EVENT}

counter = {}
i = 0
entrance_id_to_region = {d.id: d.entrance_region for d in ENTRANCES.values()}
entrance_id_to_entrance = {d.id: d for d in ENTRANCES.values()}
# print({key: value for key, value in counter.items() if value != 1})



if __name__ == "__main__":
    sorted_entrances = sorted(ENTRANCES, key=lambda x: (ENTRANCES[x].island, ENTRANCES[x].category_group, ENTRANCES[x].direction, ENTRANCES[x].name))
    data = [
        {
            "name": "Bannan Salvatore Cave"
        },
        {
            "name": "Bannan Wayfarer Cave"
        },
        {
            "name": "Bannan Cave East Exit"
        },
        {
            "name": "Bannan Cave West Exit"
        },
        {
            "name": "Wayfarer's Exit"
        },
        {
            "name": "Ocean NW Bannan"
        },
        {
            "name": "Bannan Boat"
        },
        {"name": "Bannan West Hut"},
        {"name": "Bannan West Cave"},
        {"name": "Keese Passage West Exit"},
        {"name": "Bannan East Cave"},
        {"name": "Keese Passage East Exit"}
    ]
    process = [i.get("name") for i in data]
    res = [i for i in sorted_entrances if i in process]
    for i in res:
        print("{" + f"\"name\": \"{i}\"" + "}, ")
    # print(f"len {len(ENTRANCES)}")


    # for name, data in ENTRANCES.items():
    #     print(f"{name}:", "{")
    #     for k, v in data.items():
    #         print(f"\t{k}: {v}")
    #     print("},")
