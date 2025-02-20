from __future__ import annotations

import logging
import asyncio
import shutil
import time

import Utils

from NetUtils import ClientStatus, color
from worlds.AutoSNIClient import SNIClient

from . import Shops, Regions
from .Rom import ROM_PLAYER_LIMIT

snes_logger = logging.getLogger("SNES")

GAME_ALTTP = "A Link to the Past"

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

ROMNAME_START = SRAM_START + 0x2000
ROMNAME_SIZE = 0x15

INGAME_MODES = {0x07, 0x09, 0x0b}
ENDGAME_MODES = {0x19, 0x1a}
DEATH_MODES = {0x12}

SAVEDATA_START = WRAM_START + 0xF000
SAVEDATA_SIZE = 0x500

RECV_PROGRESS_ADDR = SAVEDATA_START + 0x4D0         # 2 bytes
RECV_ITEM_ADDR = SAVEDATA_START + 0x4D2             # 1 byte
RECV_ITEM_PLAYER_ADDR = SAVEDATA_START + 0x4D3      # 1 byte
ROOMID_ADDR = SAVEDATA_START + 0x4D4                # 2 bytes
ROOMDATA_ADDR = SAVEDATA_START + 0x4D6              # 1 byte
SCOUT_LOCATION_ADDR = SAVEDATA_START + 0x4D7        # 1 byte
SCOUTREPLY_LOCATION_ADDR = SAVEDATA_START + 0x4D8   # 1 byte
SCOUTREPLY_ITEM_ADDR = SAVEDATA_START + 0x4D9       # 1 byte
SCOUTREPLY_PLAYER_ADDR = SAVEDATA_START + 0x4DA     # 1 byte
SHOP_ADDR = SAVEDATA_START + 0x302                  # 2 bytes
SHOP_LEN = (len(Shops.shop_table) * 3) + 5

DEATH_LINK_ACTIVE_ADDR = ROMNAME_START + 0x15       # 1 byte

location_shop_ids = set([info[0] for name, info in Shops.shop_table.items()])

location_table_uw = {"Blind's Hideout - Top": (0x11d, 0x10),
                     "Blind's Hideout - Left": (0x11d, 0x20),
                     "Blind's Hideout - Right": (0x11d, 0x40),
                     "Blind's Hideout - Far Left": (0x11d, 0x80),
                     "Blind's Hideout - Far Right": (0x11d, 0x100),
                     'Secret Passage': (0x55, 0x10),
                     'Waterfall Fairy - Left': (0x114, 0x10),
                     'Waterfall Fairy - Right': (0x114, 0x20),
                     "King's Tomb": (0x113, 0x10),
                     'Floodgate Chest': (0x10b, 0x10),
                     "Link's House": (0x104, 0x10),
                     'Kakariko Tavern': (0x103, 0x10),
                     'Chicken House': (0x108, 0x10),
                     "Aginah's Cave": (0x10a, 0x10),
                     "Sahasrahla's Hut - Left": (0x105, 0x10),
                     "Sahasrahla's Hut - Middle": (0x105, 0x20),
                     "Sahasrahla's Hut - Right": (0x105, 0x40),
                     'Kakariko Well - Top': (0x2f, 0x10),
                     'Kakariko Well - Left': (0x2f, 0x20),
                     'Kakariko Well - Middle': (0x2f, 0x40),
                     'Kakariko Well - Right': (0x2f, 0x80),
                     'Kakariko Well - Bottom': (0x2f, 0x100),
                     'Lost Woods Hideout': (0xe1, 0x200),
                     'Lumberjack Tree': (0xe2, 0x200),
                     'Cave 45': (0x11b, 0x400),
                     'Graveyard Cave': (0x11b, 0x200),
                     'Checkerboard Cave': (0x126, 0x200),
                     'Mini Moldorm Cave - Far Left': (0x123, 0x10),
                     'Mini Moldorm Cave - Left': (0x123, 0x20),
                     'Mini Moldorm Cave - Right': (0x123, 0x40),
                     'Mini Moldorm Cave - Far Right': (0x123, 0x80),
                     'Mini Moldorm Cave - Generous Guy': (0x123, 0x400),
                     'Ice Rod Cave': (0x120, 0x10),
                     'Bonk Rock Cave': (0x124, 0x10),
                     'Desert Palace - Big Chest': (0x73, 0x10),
                     'Desert Palace - Torch': (0x73, 0x400),
                     'Desert Palace - Map Chest': (0x74, 0x10),
                     'Desert Palace - Compass Chest': (0x85, 0x10),
                     'Desert Palace - Big Key Chest': (0x75, 0x10),
                     'Desert Palace - Desert Tiles 1 Pot Key': (0x63, 0x400),
                     'Desert Palace - Beamos Hall Pot Key': (0x53, 0x400),
                     'Desert Palace - Desert Tiles 2 Pot Key': (0x43, 0x400),
                     'Desert Palace - Boss': (0x33, 0x800),
                     'Eastern Palace - Compass Chest': (0xa8, 0x10),
                     'Eastern Palace - Big Chest': (0xa9, 0x10),
                     'Eastern Palace - Dark Square Pot Key': (0xba, 0x400),
                     'Eastern Palace - Dark Eyegore Key Drop': (0x99, 0x400),
                     'Eastern Palace - Cannonball Chest': (0xb9, 0x10),
                     'Eastern Palace - Big Key Chest': (0xb8, 0x10),
                     'Eastern Palace - Map Chest': (0xaa, 0x10),
                     'Eastern Palace - Boss': (0xc8, 0x800),
                     'Hyrule Castle - Boomerang Chest': (0x71, 0x10),
                     'Hyrule Castle - Boomerang Guard Key Drop': (0x71, 0x400),
                     'Hyrule Castle - Map Chest': (0x72, 0x10),
                     'Hyrule Castle - Map Guard Key Drop': (0x72, 0x400),
                     "Hyrule Castle - Zelda's Chest": (0x80, 0x10),
                     'Hyrule Castle - Big Key Drop': (0x80, 0x400),
                     'Sewers - Dark Cross': (0x32, 0x10),
                     'Sewers - Key Rat Key Drop': (0x21, 0x400),
                     'Sewers - Secret Room - Left': (0x11, 0x10),
                     'Sewers - Secret Room - Middle': (0x11, 0x20),
                     'Sewers - Secret Room - Right': (0x11, 0x40),
                     'Sanctuary': (0x12, 0x10),
                     'Castle Tower - Room 03': (0xe0, 0x10),
                     'Castle Tower - Dark Maze': (0xd0, 0x10),
                     'Castle Tower - Dark Archer Key Drop': (0xc0, 0x400),
                     'Castle Tower - Circle of Pots Key Drop': (0xb0, 0x400),
                     'Spectacle Rock Cave': (0xea, 0x400),
                     'Paradox Cave Lower - Far Left': (0xef, 0x10),
                     'Paradox Cave Lower - Left': (0xef, 0x20),
                     'Paradox Cave Lower - Right': (0xef, 0x40),
                     'Paradox Cave Lower - Far Right': (0xef, 0x80),
                     'Paradox Cave Lower - Middle': (0xef, 0x100),
                     'Paradox Cave Upper - Left': (0xff, 0x10),
                     'Paradox Cave Upper - Right': (0xff, 0x20),
                     'Spiral Cave': (0xfe, 0x10),
                     'Tower of Hera - Basement Cage': (0x87, 0x400),
                     'Tower of Hera - Map Chest': (0x77, 0x10),
                     'Tower of Hera - Big Key Chest': (0x87, 0x10),
                     'Tower of Hera - Compass Chest': (0x27, 0x20),
                     'Tower of Hera - Big Chest': (0x27, 0x10),
                     'Tower of Hera - Boss': (0x7, 0x800),
                     'Hype Cave - Top': (0x11e, 0x10),
                     'Hype Cave - Middle Right': (0x11e, 0x20),
                     'Hype Cave - Middle Left': (0x11e, 0x40),
                     'Hype Cave - Bottom': (0x11e, 0x80),
                     'Hype Cave - Generous Guy': (0x11e, 0x400),
                     'Peg Cave': (0x127, 0x400),
                     'Pyramid Fairy - Left': (0x116, 0x10),
                     'Pyramid Fairy - Right': (0x116, 0x20),
                     'Brewery': (0x106, 0x10),
                     'C-Shaped House': (0x11c, 0x10),
                     'Chest Game': (0x106, 0x400),
                     'Mire Shed - Left': (0x10d, 0x10),
                     'Mire Shed - Right': (0x10d, 0x20),
                     'Superbunny Cave - Top': (0xf8, 0x10),
                     'Superbunny Cave - Bottom': (0xf8, 0x20),
                     'Spike Cave': (0x117, 0x10),
                     'Hookshot Cave - Top Right': (0x3c, 0x10),
                     'Hookshot Cave - Top Left': (0x3c, 0x20),
                     'Hookshot Cave - Bottom Right': (0x3c, 0x80),
                     'Hookshot Cave - Bottom Left': (0x3c, 0x40),
                     'Mimic Cave': (0x10c, 0x10),
                     'Swamp Palace - Entrance': (0x28, 0x10),
                     'Swamp Palace - Map Chest': (0x37, 0x10),
                     'Swamp Palace - Pot Row Pot Key': (0x38, 0x400),
                     'Swamp Palace - Trench 1 Pot Key': (0x37, 0x400),
                     'Swamp Palace - Hookshot Pot Key': (0x36, 0x400),
                     'Swamp Palace - Big Chest': (0x36, 0x10),
                     'Swamp Palace - Compass Chest': (0x46, 0x10),
                     'Swamp Palace - Trench 2 Pot Key': (0x35, 0x400),
                     'Swamp Palace - Big Key Chest': (0x35, 0x10),
                     'Swamp Palace - West Chest': (0x34, 0x10),
                     'Swamp Palace - Flooded Room - Left': (0x76, 0x10),
                     'Swamp Palace - Flooded Room - Right': (0x76, 0x20),
                     'Swamp Palace - Waterfall Room': (0x66, 0x10),
                     'Swamp Palace - Waterway Pot Key': (0x16, 0x400),
                     'Swamp Palace - Boss': (0x6, 0x800),
                     "Thieves' Town - Big Key Chest": (0xdb, 0x20),
                     "Thieves' Town - Map Chest": (0xdb, 0x10),
                     "Thieves' Town - Compass Chest": (0xdc, 0x10),
                     "Thieves' Town - Ambush Chest": (0xcb, 0x10),
                     "Thieves' Town - Hallway Pot Key": (0xbc, 0x400),
                     "Thieves' Town - Spike Switch Pot Key": (0xab, 0x400),
                     "Thieves' Town - Attic": (0x65, 0x10),
                     "Thieves' Town - Big Chest": (0x44, 0x10),
                     "Thieves' Town - Blind's Cell": (0x45, 0x10),
                     "Thieves' Town - Boss": (0xac, 0x800),
                     'Skull Woods - Compass Chest': (0x67, 0x10),
                     'Skull Woods - Map Chest': (0x58, 0x20),
                     'Skull Woods - Big Chest': (0x58, 0x10),
                     'Skull Woods - Pot Prison': (0x57, 0x20),
                     'Skull Woods - Pinball Room': (0x68, 0x10),
                     'Skull Woods - Big Key Chest': (0x57, 0x10),
                     'Skull Woods - West Lobby Pot Key': (0x56, 0x400),
                     'Skull Woods - Bridge Room': (0x59, 0x10),
                     'Skull Woods - Spike Corner Key Drop': (0x39, 0x400),
                     'Skull Woods - Boss': (0x29, 0x800),
                     'Ice Palace - Jelly Key Drop': (0x0e, 0x400),
                     'Ice Palace - Compass Chest': (0x2e, 0x10),
                     'Ice Palace - Conveyor Key Drop': (0x3e, 0x400),
                     'Ice Palace - Freezor Chest': (0x7e, 0x10),
                     'Ice Palace - Big Chest': (0x9e, 0x10),
                     'Ice Palace - Iced T Room': (0xae, 0x10),
                     'Ice Palace - Many Pots Pot Key': (0x9f, 0x400),
                     'Ice Palace - Spike Room': (0x5f, 0x10),
                     'Ice Palace - Big Key Chest': (0x1f, 0x10),
                     'Ice Palace - Hammer Block Key Drop': (0x3f, 0x400),
                     'Ice Palace - Map Chest': (0x3f, 0x10),
                     'Ice Palace - Boss': (0xde, 0x800),
                     'Misery Mire - Big Chest': (0xc3, 0x10),
                     'Misery Mire - Map Chest': (0xc3, 0x20),
                     'Misery Mire - Main Lobby': (0xc2, 0x10),
                     'Misery Mire - Bridge Chest': (0xa2, 0x10),
                     'Misery Mire - Spikes Pot Key': (0xb3, 0x400),
                     'Misery Mire - Spike Chest': (0xb3, 0x10),
                     'Misery Mire - Fishbone Pot Key': (0xa1, 0x400),
                     'Misery Mire - Conveyor Crystal Key Drop': (0xc1, 0x400),
                     'Misery Mire - Compass Chest': (0xc1, 0x10),
                     'Misery Mire - Big Key Chest': (0xd1, 0x10),
                     'Misery Mire - Boss': (0x90, 0x800),
                     'Turtle Rock - Compass Chest': (0xd6, 0x10),
                     'Turtle Rock - Roller Room - Left': (0xb7, 0x10),
                     'Turtle Rock - Roller Room - Right': (0xb7, 0x20),
                     'Turtle Rock - Pokey 1 Key Drop': (0xb6, 0x400),
                     'Turtle Rock - Chain Chomps': (0xb6, 0x10),
                     'Turtle Rock - Pokey 2 Key Drop': (0x13, 0x400),
                     'Turtle Rock - Big Key Chest': (0x14, 0x10),
                     'Turtle Rock - Big Chest': (0x24, 0x10),
                     'Turtle Rock - Crystaroller Room': (0x4, 0x10),
                     'Turtle Rock - Eye Bridge - Bottom Left': (0xd5, 0x80),
                     'Turtle Rock - Eye Bridge - Bottom Right': (0xd5, 0x40),
                     'Turtle Rock - Eye Bridge - Top Left': (0xd5, 0x20),
                     'Turtle Rock - Eye Bridge - Top Right': (0xd5, 0x10),
                     'Turtle Rock - Boss': (0xa4, 0x800),
                     'Palace of Darkness - Shooter Room': (0x9, 0x10),
                     'Palace of Darkness - The Arena - Bridge': (0x2a, 0x20),
                     'Palace of Darkness - Stalfos Basement': (0xa, 0x10),
                     'Palace of Darkness - Big Key Chest': (0x3a, 0x10),
                     'Palace of Darkness - The Arena - Ledge': (0x2a, 0x10),
                     'Palace of Darkness - Map Chest': (0x2b, 0x10),
                     'Palace of Darkness - Compass Chest': (0x1a, 0x20),
                     'Palace of Darkness - Dark Basement - Left': (0x6a, 0x10),
                     'Palace of Darkness - Dark Basement - Right': (0x6a, 0x20),
                     'Palace of Darkness - Dark Maze - Top': (0x19, 0x10),
                     'Palace of Darkness - Dark Maze - Bottom': (0x19, 0x20),
                     'Palace of Darkness - Big Chest': (0x1a, 0x10),
                     'Palace of Darkness - Harmless Hellway': (0x1a, 0x40),
                     'Palace of Darkness - Boss': (0x5a, 0x800),
                     'Ganons Tower - Conveyor Cross Pot Key': (0x8b, 0x400),
                     "Ganons Tower - Bob's Torch": (0x8c, 0x400),
                     'Ganons Tower - Hope Room - Left': (0x8c, 0x20),
                     'Ganons Tower - Hope Room - Right': (0x8c, 0x40),
                     'Ganons Tower - Tile Room': (0x8d, 0x10),
                     'Ganons Tower - Compass Room - Top Left': (0x9d, 0x10),
                     'Ganons Tower - Compass Room - Top Right': (0x9d, 0x20),
                     'Ganons Tower - Compass Room - Bottom Left': (0x9d, 0x40),
                     'Ganons Tower - Compass Room - Bottom Right': (0x9d, 0x80),
                     'Ganons Tower - Conveyor Star Pits Pot Key': (0x7b, 0x400),
                     'Ganons Tower - DMs Room - Top Left': (0x7b, 0x10),
                     'Ganons Tower - DMs Room - Top Right': (0x7b, 0x20),
                     'Ganons Tower - DMs Room - Bottom Left': (0x7b, 0x40),
                     'Ganons Tower - DMs Room - Bottom Right': (0x7b, 0x80),
                     'Ganons Tower - Map Chest': (0x8b, 0x10),
                     'Ganons Tower - Double Switch Pot Key': (0x9b, 0x400),
                     'Ganons Tower - Firesnake Room': (0x7d, 0x10),
                     'Ganons Tower - Randomizer Room - Top Left': (0x7c, 0x10),
                     'Ganons Tower - Randomizer Room - Top Right': (0x7c, 0x20),
                     'Ganons Tower - Randomizer Room - Bottom Left': (0x7c, 0x40),
                     'Ganons Tower - Randomizer Room - Bottom Right': (0x7c, 0x80),
                     "Ganons Tower - Bob's Chest": (0x8c, 0x80),
                     'Ganons Tower - Big Chest': (0x8c, 0x10),
                     'Ganons Tower - Big Key Room - Left': (0x1c, 0x20),
                     'Ganons Tower - Big Key Room - Right': (0x1c, 0x40),
                     'Ganons Tower - Big Key Chest': (0x1c, 0x10),
                     'Ganons Tower - Mini Helmasaur Room - Left': (0x3d, 0x10),
                     'Ganons Tower - Mini Helmasaur Room - Right': (0x3d, 0x20),
                     'Ganons Tower - Mini Helmasaur Key Drop': (0x3d, 0x400),
                     'Ganons Tower - Pre-Moldorm Chest': (0x3d, 0x40),
                     'Ganons Tower - Validation Chest': (0x4d, 0x10)}

collect_ignore_locations = {Regions.lookup_name_to_id[name] for name in {
    'Eastern Palace - Boss',
    'Desert Palace - Boss',
    'Tower of Hera - Boss',
    'Palace of Darkness - Boss',
    'Swamp Palace - Boss',
    'Skull Woods - Boss',
    "Thieves' Town - Boss",
    'Ice Palace - Boss',
    'Misery Mire - Boss',
    'Turtle Rock - Boss',
    'Sahasrahla',
    'Master Sword Pedestal',  # can circumvent ganon pedestal's goal's pendant collection
}}

location_table_uw_id = {Regions.lookup_name_to_id[name]: data for name, data in location_table_uw.items()}

location_table_npc = {'Mushroom': 0x1000,
                      'King Zora': 0x2,
                      'Sahasrahla': 0x10,
                      'Blacksmith': 0x400,
                      'Magic Bat': 0x8000,
                      'Sick Kid': 0x4,
                      'Library': 0x80,
                      'Potion Shop': 0x2000,
                      'Old Man': 0x1,
                      'Ether Tablet': 0x100,
                      'Catfish': 0x20,
                      'Stumpy': 0x8,
                      'Bombos Tablet': 0x200}

location_table_npc_id = {Regions.lookup_name_to_id[name]: data for name, data in location_table_npc.items()}

location_table_ow = {'Flute Spot': 0x2a,
                     'Sunken Treasure': 0x3b,
                     "Zora's Ledge": 0x81,
                     'Lake Hylia Island': 0x35,
                     'Maze Race': 0x28,
                     'Desert Ledge': 0x30,
                     'Master Sword Pedestal': 0x80,
                     'Spectacle Rock': 0x3,
                     'Pyramid': 0x5b,
                     'Digging Game': 0x68,
                     'Bumper Cave Ledge': 0x4a,
                     'Floating Island': 0x5}

location_table_ow_id = {Regions.lookup_name_to_id[name]: data for name, data in location_table_ow.items()}

location_table_misc = {'Bottle Merchant': (0x3c9, 0x2),
                       'Purple Chest': (0x3c9, 0x10),
                       "Link's Uncle": (0x3c6, 0x1),
                       'Hobo': (0x3c9, 0x1)}
location_table_misc_id = {Regions.lookup_name_to_id[name]: data for name, data in location_table_misc.items()}


def should_collect(ctx, location_id: int) -> bool:
    return ctx.allow_collect and location_id not in collect_ignore_locations and location_id in ctx.checked_locations \
            and location_id not in ctx.locations_checked and location_id in ctx.locations_info \
            and ctx.locations_info[location_id].player != ctx.slot


async def track_locations(ctx, roomid, roomdata) -> bool:
    from SNIClient import snes_read, snes_buffered_write, snes_flush_writes
    location_id: int
    new_locations = []

    def new_check(location_id):
        new_locations.append(location_id)
        ctx.locations_checked.add(location_id)
        location = ctx.location_names.lookup_in_game(location_id)
        snes_logger.info(
            f'New Check: {location} ' +
            f'({len(ctx.checked_locations) + 1 if ctx.checked_locations else len(ctx.locations_checked)}/' +
            f'{len(ctx.missing_locations) + len(ctx.checked_locations)})')

    try:
        shop_data = await snes_read(ctx, SHOP_ADDR, SHOP_LEN)
        shop_data_changed = False
        shop_data = list(shop_data)
        for cnt, b in enumerate(shop_data):
            location_id = Shops.SHOP_ID_START + cnt
            if int(b) and location_id not in ctx.locations_checked:
                new_check(location_id)
            if should_collect(ctx, location_id):
                if not int(b):
                    shop_data[cnt] += 1
                    shop_data_changed = True
        if shop_data_changed:
            snes_buffered_write(ctx, SHOP_ADDR, bytes(shop_data))
    except Exception as e:
        snes_logger.info(f"Exception: {e}")

    for location_id, (loc_roomid, loc_mask) in location_table_uw_id.items():
        try:
            if location_id not in ctx.locations_checked and loc_roomid == roomid and \
                    (roomdata << 4) & loc_mask != 0:
                new_check(location_id)
        except Exception as e:
            snes_logger.exception(f"Exception: {e}")

    uw_begin = 0x129
    ow_end = uw_end = 0
    uw_unchecked = {}
    uw_checked = {}
    for location, (roomid, mask) in location_table_uw.items():
        location_id = Regions.lookup_name_to_id[location]
        if location_id not in ctx.locations_checked:
            uw_unchecked[location_id] = (roomid, mask)
            uw_begin = min(uw_begin, roomid)
            uw_end = max(uw_end, roomid + 1)
        if should_collect(ctx, location_id):
            uw_begin = min(uw_begin, roomid)
            uw_end = max(uw_end, roomid + 1)
            uw_checked[location_id] = (roomid, mask)

    if uw_begin < uw_end:
        uw_data = await snes_read(ctx, SAVEDATA_START + (uw_begin * 2), (uw_end - uw_begin) * 2)
        if uw_data is not None:
            for location_id, (roomid, mask) in uw_unchecked.items():
                offset = (roomid - uw_begin) * 2
                roomdata = uw_data[offset] | (uw_data[offset + 1] << 8)
                if roomdata & mask != 0:
                    new_check(location_id)
            if uw_checked:
                uw_data = list(uw_data)
                for location_id, (roomid, mask) in uw_checked.items():
                    offset = (roomid - uw_begin) * 2
                    roomdata = uw_data[offset] | (uw_data[offset + 1] << 8)
                    roomdata |= mask
                    uw_data[offset] = roomdata & 0xFF
                    uw_data[offset + 1] = roomdata >> 8
                snes_buffered_write(ctx, SAVEDATA_START + (uw_begin * 2), bytes(uw_data))

    ow_begin = 0x82
    ow_unchecked = {}
    ow_checked = {}
    for location_id, screenid in location_table_ow_id.items():
        if location_id not in ctx.locations_checked:
            ow_unchecked[location_id] = screenid
            ow_begin = min(ow_begin, screenid)
            ow_end = max(ow_end, screenid + 1)
            if should_collect(ctx, location_id):
                ow_checked[location_id] = screenid

    if ow_begin < ow_end:
        ow_data = await snes_read(ctx, SAVEDATA_START + 0x280 + ow_begin, ow_end - ow_begin)
        if ow_data is not None:
            for location_id, screenid in ow_unchecked.items():
                if ow_data[screenid - ow_begin] & 0x40 != 0:
                    new_check(location_id)
            if ow_checked:
                ow_data = list(ow_data)
                for location_id, screenid in ow_checked.items():
                    ow_data[screenid - ow_begin] |= 0x40
                snes_buffered_write(ctx, SAVEDATA_START + 0x280 + ow_begin, bytes(ow_data))

    if not ctx.locations_checked.issuperset(location_table_npc_id):
        npc_data = await snes_read(ctx, SAVEDATA_START + 0x410, 2)
        if npc_data is not None:
            npc_value_changed = False
            npc_value = npc_data[0] | (npc_data[1] << 8)
            for location_id, mask in location_table_npc_id.items():
                if npc_value & mask != 0 and location_id not in ctx.locations_checked:
                    new_check(location_id)
                if should_collect(ctx, location_id):
                    npc_value |= mask
                    npc_value_changed = True
            if npc_value_changed:
                npc_data = bytes([npc_value & 0xFF, npc_value >> 8])
                snes_buffered_write(ctx, SAVEDATA_START + 0x410, npc_data)

    if not ctx.locations_checked.issuperset(location_table_misc_id):
        misc_data = await snes_read(ctx, SAVEDATA_START + 0x3c6, 4)
        if misc_data is not None:
            misc_data = list(misc_data)
            misc_data_changed = False
            for location_id, (offset, mask) in location_table_misc_id.items():
                assert (0x3c6 <= offset <= 0x3c9)
                if misc_data[offset - 0x3c6] & mask != 0 and location_id not in ctx.locations_checked:
                    new_check(location_id)
                if should_collect(ctx, location_id):
                    misc_data_changed = True
                    misc_data[offset - 0x3c6] |= mask
            if misc_data_changed:
                snes_buffered_write(ctx, SAVEDATA_START + 0x3c6, bytes(misc_data))

    if new_locations:
        # verify rom is still the same:
        rom_name = await snes_read(ctx, ROMNAME_START, ROMNAME_SIZE)
        if rom_name is None or all(byte == b"\x00" for byte in rom_name) or rom_name[:2] != b"AP" or \
                rom_name != ctx.rom:
            snes_logger.info(f"Discarding recent {len(new_locations)} checks as ROM Status has changed.")
            return False
        else:
            await ctx.check_locations(new_locations)
    await snes_flush_writes(ctx)
    return True


class ALTTPSNIClient(SNIClient):
    game = "A Link to the Past"
    patch_suffix = [".aplttp", ".apz3"]

    async def deathlink_kill_player(self, ctx):
        from SNIClient import DeathState, snes_read, snes_buffered_write, snes_flush_writes
        invincible = await snes_read(ctx, WRAM_START + 0x037B, 1)
        last_health = await snes_read(ctx, WRAM_START + 0xF36D, 1)
        await asyncio.sleep(0.25)
        health = await snes_read(ctx, WRAM_START + 0xF36D, 1)
        if not invincible or not last_health or not health:
            ctx.death_state = DeathState.dead
            ctx.last_death_link = time.time()
            return
        if not invincible[0] and last_health[0] == health[0]:
            snes_buffered_write(ctx, WRAM_START + 0xF36D, bytes([0]))  # set current health to 0
            snes_buffered_write(ctx, WRAM_START + 0x0373,
                                bytes([8]))  # deal 1 full heart of damage at next opportunity

        await snes_flush_writes(ctx)
        await asyncio.sleep(1)

        gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
        if not gamemode or gamemode[0] in DEATH_MODES:
            ctx.death_state = DeathState.dead

    async def validate_rom(self, ctx) -> bool:
        from SNIClient import snes_read

        rom_name = await snes_read(ctx, ROMNAME_START, ROMNAME_SIZE)
        if rom_name is None or all(byte == b"\x00" for byte in rom_name) or rom_name[:2] != b"AP":
            return False

        ctx.game = self.game
        ctx.items_handling = 0b001  # full local

        ctx.rom = rom_name

        death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR, 1)

        if death_link:
            ctx.allow_collect = bool(death_link[0] & 0b100)
            ctx.death_link_allow_survive = bool(death_link[0] & 0b10)
            await ctx.update_death_link(bool(death_link[0] & 0b1))

        return True

    async def game_watcher(self, ctx):
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes
        gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
        if "DeathLink" in ctx.tags and gamemode and ctx.last_death_link + 1 < time.time():
            currently_dead = gamemode[0] in DEATH_MODES
            await ctx.handle_deathlink_state(currently_dead,
                                             ctx.player_names[ctx.slot] + " ran out of hearts." if ctx.slot else "")

        gameend = await snes_read(ctx, SAVEDATA_START + 0x443, 1)
        game_timer = await snes_read(ctx, SAVEDATA_START + 0x42E, 4)
        if gamemode is None or gameend is None or game_timer is None or \
                (gamemode[0] not in INGAME_MODES and gamemode[0] not in ENDGAME_MODES):
            return

        if gameend[0]:
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        if gamemode in ENDGAME_MODES:  # triforce room and credits
            return

        data = await snes_read(ctx, RECV_PROGRESS_ADDR, 8)
        if data is None:
            return

        recv_index = data[0] | (data[1] << 8)
        recv_item = data[2]
        roomid = data[4] | (data[5] << 8)
        roomdata = data[6]
        scout_location = data[7]

        if recv_index < len(ctx.items_received) and recv_item == 0:
            item = ctx.items_received[recv_index]
            recv_index += 1
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(ctx.item_names.lookup_in_game(item.item), 'red', 'bold'),
                color(ctx.player_names[item.player], 'yellow'),
                ctx.location_names.lookup_in_slot(item.location, item.player), recv_index, len(ctx.items_received)))

            snes_buffered_write(ctx, RECV_PROGRESS_ADDR,
                                bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))
            snes_buffered_write(ctx, RECV_ITEM_ADDR,
                                bytes([item.item]))
            snes_buffered_write(ctx, RECV_ITEM_PLAYER_ADDR,
                                bytes([min(ROM_PLAYER_LIMIT, item.player) if item.player != ctx.slot else 0]))
        if scout_location > 0 and scout_location in ctx.locations_info:
            snes_buffered_write(ctx, SCOUTREPLY_LOCATION_ADDR,
                                bytes([scout_location]))
            snes_buffered_write(ctx, SCOUTREPLY_ITEM_ADDR,
                                bytes([ctx.locations_info[scout_location].item]))
            snes_buffered_write(ctx, SCOUTREPLY_PLAYER_ADDR,
                                bytes([min(ROM_PLAYER_LIMIT, ctx.locations_info[scout_location].player)]))

        await snes_flush_writes(ctx)

        if scout_location > 0 and scout_location not in ctx.locations_scouted:
            ctx.locations_scouted.add(scout_location)
            await ctx.send_msgs([{"cmd": "LocationScouts", "locations": [scout_location]}])
        same_rom = await track_locations(ctx, roomid, roomdata)
        if not same_rom:
            return


def get_alttp_settings(romfile: str):
    import LttPAdjuster

    adjustedromfile = ''
    if vars(Utils.get_adjuster_settings_no_defaults(GAME_ALTTP)):
        last_settings = Utils.get_adjuster_settings(GAME_ALTTP)

        allow_list = {"music", "menuspeed", "heartbeep", "heartcolor", "ow_palettes", "quickswap",
                    "uw_palettes", "sprite", "sword_palettes", "shield_palettes", "hud_palettes",
                    "reduceflashing", "deathlink", "allowcollect", "oof"}
        choice = 'no'
        if 'ask' in last_settings.auto_apply:
            printed_options = {name: value for name, value in vars(last_settings).items() if name in allow_list}
            
            sprite_pool = {}
            for sprite in last_settings.sprite_pool:
                if sprite in sprite_pool:
                    sprite_pool[sprite] += 1
                else:
                    sprite_pool[sprite] = 1
                if sprite_pool:
                    printed_options["sprite_pool"] = sprite_pool
            import pprint

            from CommonClient import gui_enabled
            if gui_enabled:

                try:
                    from tkinter import Tk, PhotoImage, Label, LabelFrame, Frame, Button
                    applyPromptWindow = Tk()
                except Exception as e:
                    logging.error('Could not load tkinter, which is likely not installed.')
                    return '', False

                applyPromptWindow.resizable(False, False)
                applyPromptWindow.protocol('WM_DELETE_WINDOW', lambda: onButtonClick())
                logo = PhotoImage(file=Utils.local_path('data', 'icon.png'))
                applyPromptWindow.tk.call('wm', 'iconphoto', applyPromptWindow._w, logo)
                applyPromptWindow.wm_title("Last adjuster settings LttP")

                label = LabelFrame(applyPromptWindow,
                                   text='Last used adjuster settings were found. Would you like to apply these?')
                label.grid(column=0, row=0, padx=5, pady=5, ipadx=5, ipady=5)
                label.grid_columnconfigure(0, weight=1)
                label.grid_columnconfigure(1, weight=1)
                label.grid_columnconfigure(2, weight=1)
                label.grid_columnconfigure(3, weight=1)

                def onButtonClick(answer: str = 'no'):
                    setattr(onButtonClick, 'choice', answer)
                    applyPromptWindow.destroy()

                framedOptions = Frame(label)
                framedOptions.grid(column=0, columnspan=4, row=0)
                framedOptions.grid_columnconfigure(0, weight=1)
                framedOptions.grid_columnconfigure(1, weight=1)
                framedOptions.grid_columnconfigure(2, weight=1)
                curRow = 0
                curCol = 0
                for name, value in printed_options.items():
                    Label(framedOptions, text=name + ": " + str(value)).grid(column=curCol, row=curRow, padx=5)
                    if (curCol == 2):
                        curRow += 1
                        curCol = 0
                    else:
                        curCol += 1

                yesButton = Button(label, text='Yes', command=lambda: onButtonClick('yes'), width=10)
                yesButton.grid(column=0, row=1)
                noButton = Button(label, text='No', command=lambda: onButtonClick('no'), width=10)
                noButton.grid(column=1, row=1)
                alwaysButton = Button(label, text='Always', command=lambda: onButtonClick('always'), width=10)
                alwaysButton.grid(column=2, row=1)
                neverButton = Button(label, text='Never', command=lambda: onButtonClick('never'), width=10)
                neverButton.grid(column=3, row=1)

                Utils.tkinter_center_window(applyPromptWindow)
                applyPromptWindow.mainloop()
                choice = getattr(onButtonClick, 'choice')
            else:
                choice = input(f"Last used adjuster settings were found. Would you like to apply these? \n"
                               f"{pprint.pformat(printed_options)}\n"
                               f"Enter yes, no, always or never: ")
            if choice and choice.startswith("y"):
                choice = 'yes'
            elif choice and "never" in choice:
                choice = 'no'
                last_settings.auto_apply = 'never'
                Utils.persistent_store("adjuster", GAME_ALTTP, last_settings)
            elif choice and "always" in choice:
                choice = 'yes'
                last_settings.auto_apply = 'always'
                Utils.persistent_store("adjuster", GAME_ALTTP, last_settings)
            else:
                choice = 'no'
        elif 'never' in last_settings.auto_apply:
            choice = 'no'
        elif 'always' in last_settings.auto_apply:
            choice = 'yes'

        if 'yes' in choice:
            import LttPAdjuster
            from .Rom import get_base_rom_path
            last_settings.rom = romfile
            last_settings.baserom = get_base_rom_path()
            last_settings.world = None

            if last_settings.sprite_pool:
                from LttPAdjuster import AdjusterWorld
                last_settings.world = AdjusterWorld(getattr(last_settings, "sprite_pool"))

            adjusted = True
            _, adjustedromfile = LttPAdjuster.adjust(last_settings)

            if hasattr(last_settings, "world"):
                delattr(last_settings, "world")
        else:
            adjusted = False
        if adjusted:
            try:
                shutil.move(adjustedromfile, romfile)
                adjustedromfile = romfile
            except Exception as e:
                logging.exception(e)
    else:
        adjusted = False
    return adjustedromfile, adjusted
