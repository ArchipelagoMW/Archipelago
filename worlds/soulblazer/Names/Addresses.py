# PROM addresses
LAIR_DATA = 0x00BA0D
CHEST_POINTERS = 0x00A9DE
CHEST_DATA = 0x00AADE
NPC_REWARD_DATA = 0x017740

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



# WRAM Addresses


EVENT_FLAGS = 0x001A5E #Used to check for deathtoll defeat.
EVENT_FLAGS_WIN = EVENT_FLAGS + 0x1F
EVENT_FLAGS_WIN_BIT = 0x02
CHEST_OPENED_TABLE = 0x001A7E
NPC_RELEASE_TABLE = 0x001ADE
NPC_REWARD_TABLE = 0x001B13
NPC_REWARD_TABLE_SIZE = 0x08
PLAYER_NAME = 0x001B92
PLAYER_NAME_SIZE = 0x08
PLAYER_CURRENT_HEALTH = 0x001B88 #TODO: use this for deathlink
CURRENT_MAP_NUMBER = 0x001C6A
RX_ADDR = 0x001DA0

LAIR_SPAWN_TABLE = 0x010203
LAIR_SPAWN_TABLE_SIZE = 0x200
RECEIVE_COUNT = 0x00

