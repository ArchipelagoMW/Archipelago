# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

# PROM addresses
LAIR_DATA = 0x00BA0D
LAIR_DATA_SIZE = 0x20
LAIRS_COUNT = 420
CHEST_POINTERS = 0x00A9DE
CHEST_DATA = 0x00AADE
WEAPON_STRENGTH_DATA = 0x0161AD
ARMOR_DEFENSE_DATA = 0x0161C6
WEAPON_REQUIRED_LEVEL_DATA = 0x0161CE
RANDO_SETTINGS = 0x017730
STONES_REQUIRED = RANDO_SETTINGS
ACT_PROGRESSION = STONES_REQUIRED+1
OPEN_DEATHTOLL = ACT_PROGRESSION+1
NPC_REWARD_DATA = 0x017740
TEXT_SPEED = 0x02796C

SNES_ROMNAME_START = 0x7FC0
ROMNAME_SIZE = 0x15

# Chest addresses arent packed as nicely and chest ID 0x17 has two entries
CHEST_ADDRESSES = [
    # Trial Room
    [0xAADE],
    # Gras Valley Secret Cave
    [0xAAE5],
    [0xAAEB],
    # Underground castle west
    [0xAAF2],
    [0xAAF8],
    [0xAAFE],
    # Underground castle east
    [0xAB05],
    # Leo's painting
    [0xAB0C],
    [0xAB12],
    # Greenwood
    [0xAB1A],
    # Greenwood tunnels
    [0xAB21],
    # Water shrine B1
    [0xAB28],
    # Water shrine B2
    [0xAB2F],
    [0xAB35],
    # Water shrine B3
    [0xAB3C],
    [0xAB42],
    # Fire shrine B1
    [0xAB49],
    # Fire shrine B2
    [0xAB50],
    [0xAB56],
    # Fire shrine B3
    [0xAB5D],
    [0xAB63],
    # Light Shrine B1
    [0xAB6A],
    # Seabed sanctuary
    [0xAB71, 0xAB77],
    [0xAB7D],
    # Seabed Secret Cave
    [0xAB84],
    [0xAB8A],
    [0xAB90],
    [0xAB96],
    # Southerta
    [0xAB9D],
    # Rockbird
    [0xABA4],
    [0xABAA],
    # Durean
    [0xABB1],
    [0xABB7],
    # Ghost ship
    [0xABBE],
    # Seabed reef
    [0xABC5],
    # Mountain Slope 1
    [0xABCC],
    # Mountain Slope 4-pack
    [0xABD3],
    [0xABD9],
    [0xABDF],
    [0xABE5],
    # Laynole
    [0xABEC],
    [0xABF2],
    [0xABF8],
    # Leo's Lab zantestu
    [0xABFF],
    # Power Plant
    [0xAC06],
    # Model Town 1
    [0xAC0D],
    [0xAC13],
    [0xAC19],
    # Model Town 2
    [0xAC20],
    [0xAC26],
    # Magridd Castle B1
    [0xAC2D],
    [0xAC33],
    # Magridd Castle B2
    [0xAC3A],
    [0xAC40],
    [0xAC46],
    # Magridd Castle B3
    [0xAC4D],
    # Magridd Castle Right Tower F2
    [0xAC54],
    [0xAC5A],
    # Magridd Castle Right Tower F3
    [0xAC61],
    [0xAC67],
    # World of Evil 1
    [0xAC6E],
    [0xAC74],
    [0xAC7A],
    # World of Evil 2
    [0xAC81],
    # World of Evil 3
    [0xAC88],
    [0xAC8E],
]

# The bitflags for Chests in ram are in a different order than the chests in ROM. The 8th bit is used by the game
# for... something but is not actually part of the address, so any index >= 0x80 needs to have the high bit cleared
# to be a valid index into memory.
CHEST_FLAG_INDEXES = [
    0x00,
    0x05,
    0x06,
    0x01,
    0x02,
    0x03,
    0x04,
    0x09,
    0x0A,
    0x0C,
    0x0D,
    0x0B,
    0x0E,
    0x0F,
    0x10,
    0x11,
    0x12,
    0x14,
    0x13,
    0x15,
    0x16,
    0x42,
    0x17,
    0x18,
    0x19,
    0x1A,
    0x1B,
    0x1C,
    0x1D,
    0x1E,
    0x1F,
    0x20,
    0x21,
    0x22,
    0x23,
    0x24,
    0x25,
    0x26,
    0x27,
    0x28,
    0x29,
    0x2A,
    0x41,
    0x3F,
    0x2B,
    0x2C, # 0xAC & 0x7F,
    0x2D, # 0xAD & 0x7F,
    0x2E, # 0xAE & 0x7F,
    0x2F, # 0xAF & 0x7F,
    0x30, # 0xB0 & 0x7F,
    0x31,
    0x40,
    0x32, # 0xB2 & 0x7F,
    0x33, # 0xB3 & 0x7F,
    0x43, # 0xC3 & 0x7F,
    0x34, # 0xB4 & 0x7F,
    0x3D, # 0xBD & 0x7F,
    0x3E, # 0xBE & 0x7F,
    0x35,
    0x36,
    0x37,
    0x38,
    0x39,
    0x3A,
    0x3B,
    0x3C,
]


# WRAM Addresses

# Map/SubMap numbers are different from MapIDs, but there is a 1-1 mapping.
MAP_NUMBER = 0x000314 + WRAM_START
MAP_SUB_NUMBER = 0x000316 + WRAM_START
POSITION_INT_X = 0x000378 + WRAM_START
POSITION_INT_Y = 0x00037A + WRAM_START
ENTITIES_TABLE = 0x000800 + WRAM_START
ENTITY_SIZE = 0x40
ENTITY_COUNT = 0x40
EVENT_FLAGS = 0x001A5E + WRAM_START  # Used to check for deathtoll defeat.
EVENT_FLAGS_WIN = EVENT_FLAGS + 0x1F
EVENT_FLAGS_WIN_BIT = 0x02
CHEST_OPENED_TABLE = 0x001A7E + WRAM_START
NPC_RELEASE_TABLE = 0x001ADE + WRAM_START
NPC_REWARD_TABLE = 0x001B13 + WRAM_START
NPC_REWARD_TABLE_SIZE = 0x08
PLAYER_NAME = 0x001B92 + WRAM_START
PLAYER_NAME_SIZE = 0x09
PLAYER_CURRENT_HEALTH = 0x001B88 + WRAM_START  # TODO: use this for deathlink
CURRENT_MAP_ID = 0x001C6A + WRAM_START
RX_STATUS = 0x001DA0 + WRAM_START
RX_INCREMENT = RX_STATUS + 1
RX_ID = RX_INCREMENT + 1
RX_UNUSED = RX_ID + 1
RX_OPERAND = RX_UNUSED + 1
RX_SENDER = RX_OPERAND + 2
RX_SENDER_SIZE = 17
TX_STATUS = 0x001DC0 + WRAM_START
TX_ITEM_NAME = TX_STATUS + 1
TX_NAME_SIZE = 23
TX_ADDRESSEE = TX_ITEM_NAME + TX_NAME_SIZE
TX_ADDRESSEE_SIZE = 19

LAIR_SPAWN_TABLE = 0x010203 + WRAM_START
LAIR_SPAWN_TABLE_SIZE = 0x200
RECEIVE_COUNT = 0x001AD3 + WRAM_START
