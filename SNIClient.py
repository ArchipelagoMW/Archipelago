from __future__ import annotations

import sys
import threading
import time
import multiprocessing
import os
import subprocess
import base64
import shutil
import logging
import asyncio
from json import loads, dumps

import ModuleUpdate
ModuleUpdate.update()

from Utils import init_logging

if __name__ == "__main__":
    init_logging("SNIClient", exception_logger="Client")

import colorama

from NetUtils import *
from worlds.alttp import Regions, Shops
from worlds.alttp.Rom import ROM_PLAYER_LIMIT
from worlds.sm.Rom import ROM_PLAYER_LIMIT as SM_ROM_PLAYER_LIMIT
from worlds.smz3.Rom import ROM_PLAYER_LIMIT as SMZ3_ROM_PLAYER_LIMIT
import Utils
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
from Patch import GAME_ALTTP, GAME_SM, GAME_SMZ3

snes_logger = logging.getLogger("SNES")

from MultiServer import mark_raw


class DeathState(enum.IntEnum):
    killing_player = 1
    alive = 2
    dead = 3


class SNIClientCommandProcessor(ClientCommandProcessor):
    ctx: Context

    def _cmd_slow_mode(self, toggle: str = ""):
        """Toggle slow mode, which limits how fast you send / receive items."""
        if toggle:
            self.ctx.slow_mode = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.slow_mode = not self.ctx.slow_mode

        self.output(f"Setting slow mode to {self.ctx.slow_mode}")

    @mark_raw
    def _cmd_snes(self, snes_options: str = "") -> bool:
        """Connect to a snes. Optionally include network address of a snes to connect to,
        otherwise show available devices; and a SNES device number if more than one SNES is detected.
        Examples: "/snes", "/snes 1", "/snes localhost:8080 1" """

        snes_address = self.ctx.snes_address
        snes_device_number = -1

        options = snes_options.split()
        num_options = len(options)

        if num_options > 0:
            snes_device_number = int(options[0])

        if num_options > 1:
            snes_address = options[0]
            snes_device_number = int(options[1])

        self.ctx.snes_reconnect_address = None
        asyncio.create_task(snes_connect(self.ctx, snes_address, snes_device_number), name="SNES Connect")
        return True

    def _cmd_snes_close(self) -> bool:
        """Close connection to a currently connected snes"""
        self.ctx.snes_reconnect_address = None
        if self.ctx.snes_socket is not None and not self.ctx.snes_socket.closed:
            asyncio.create_task(self.ctx.snes_socket.close())
            return True
        else:
            return False

    # Left here for quick re-addition for debugging.
    # def _cmd_snes_write(self, address, data):
    #     """Write the specified byte (base10) to the SNES' memory address (base16)."""
    #     if self.ctx.snes_state != SNESState.SNES_ATTACHED:
    #         self.output("No attached SNES Device.")
    #         return False
    #     snes_buffered_write(self.ctx, int(address, 16), bytes([int(data)]))
    #     asyncio.create_task(snes_flush_writes(self.ctx))
    #     self.output("Data Sent")
    #     return True

    # def _cmd_snes_read(self, address, size=1):
    #     """Read the SNES' memory address (base16)."""
    #     if self.ctx.snes_state != SNESState.SNES_ATTACHED:
    #         self.output("No attached SNES Device.")
    #         return False
    #     data = await snes_read(self.ctx, int(address, 16), size)
    #     self.output(f"Data Read: {data}")
    #     return True


class Context(CommonContext):
    command_processor = SNIClientCommandProcessor
    game = "A Link to the Past"
    items_handling = None  # set in game_watcher

    def __init__(self, snes_address, server_address, password):
        super(Context, self).__init__(server_address, password)

        # snes stuff
        self.snes_address = snes_address
        self.snes_socket = None
        self.snes_state = SNESState.SNES_DISCONNECTED
        self.snes_attached_device = None
        self.snes_reconnect_address = None
        self.snes_recv_queue = asyncio.Queue()
        self.snes_request_lock = asyncio.Lock()
        self.snes_write_buffer = []
        self.snes_connector_lock = threading.Lock()
        self.death_state = DeathState.alive  # for death link flop behaviour
        self.killing_player_task = None
        self.allow_collect = False

        self.awaiting_rom = False
        self.rom = None
        self.prev_rom = None

    async def connection_closed(self):
        await super(Context, self).connection_closed()
        self.awaiting_rom = False

    def event_invalid_slot(self):
        if self.snes_socket is not None and not self.snes_socket.closed:
            asyncio.create_task(self.snes_socket.close())
        raise Exception('Invalid ROM detected, '
                        'please verify that you have loaded the correct rom and reconnect your snes (/snes)')

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Context, self).server_auth(password_requested)
        if self.rom is None:
            self.awaiting_rom = True
            snes_logger.info(
                'No ROM detected, awaiting snes connection to authenticate to the multiworld server (/snes)')
            return
        self.awaiting_rom = False
        self.auth = self.rom
        auth = base64.b64encode(self.rom).decode()
        await self.send_connect(name=auth)

    def on_deathlink(self, data: dict):
        if not self.killing_player_task or self.killing_player_task.done():
            self.killing_player_task = asyncio.create_task(deathlink_kill_player(self))
        super(Context, self).on_deathlink(data)

    async def handle_deathlink_state(self, currently_dead: bool):
        # in this state we only care about triggering a death send
        if self.death_state == DeathState.alive:
            if currently_dead:
                self.death_state = DeathState.dead
                await self.send_death()
        # in this state we care about confirming a kill, to move state to dead
        elif self.death_state == DeathState.killing_player:
            # this is being handled in deathlink_kill_player(ctx) already
            pass
        # in this state we wait until the player is alive again
        elif self.death_state == DeathState.dead:
            if not currently_dead:
                self.death_state = DeathState.alive

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected", "RoomUpdate"}:
            if "checked_locations" in args and args["checked_locations"]:
                new_locations = set(args["checked_locations"])
                self.checked_locations |= new_locations
                self.locations_scouted |= new_locations
                # Items belonging to the player should not be marked as checked in game, since the player will likely need that item.
                # Once the games handled by SNIClient gets made to be remote items, this will no longer be needed.
                asyncio.create_task(self.send_msgs([{"cmd": "LocationScouts", "locations": list(new_locations)}]))

    def run_gui(self):
        from kvui import GameManager

        class SNIManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago"),
                ("SNES", "SNES"),
            ]
            base_title = "Archipelago SNI Client"

        self.ui = SNIManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def deathlink_kill_player(ctx: Context):
    ctx.death_state = DeathState.killing_player
    while ctx.death_state == DeathState.killing_player and \
            ctx.snes_state == SNESState.SNES_ATTACHED:
        if ctx.game == GAME_ALTTP:
            invincible = await snes_read(ctx, WRAM_START + 0x037B, 1)
            last_health = await snes_read(ctx, WRAM_START + 0xF36D, 1)
            await asyncio.sleep(0.25)
            health = await snes_read(ctx, WRAM_START + 0xF36D, 1)
            if not invincible or not last_health or not health:
                ctx.death_state = DeathState.dead
                ctx.last_death_link = time.time()
                continue
            if not invincible[0] and last_health[0] == health[0]:
                snes_buffered_write(ctx, WRAM_START + 0xF36D, bytes([0]))  # set current health to 0
                snes_buffered_write(ctx, WRAM_START + 0x0373,
                                    bytes([8]))  # deal 1 full heart of damage at next opportunity
        elif ctx.game == GAME_SM:
            snes_buffered_write(ctx, WRAM_START + 0x09C2, bytes([1, 0]))  # set current health to 1 (to prevent saving with 0 energy)
            snes_buffered_write(ctx, WRAM_START + 0x0A50, bytes([255])) # deal 255 of damage at next opportunity
            if not ctx.death_link_allow_survive:
                snes_buffered_write(ctx, WRAM_START + 0x09D6, bytes([0, 0]))  # set current reserve to 0
        await snes_flush_writes(ctx)
        await asyncio.sleep(1)

        if ctx.game == GAME_ALTTP:
            gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
            if not gamemode or gamemode[0] in DEATH_MODES:
                ctx.death_state = DeathState.dead
        elif ctx.game == GAME_SM:
            gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
            health = await snes_read(ctx, WRAM_START + 0x09C2, 2)
            if health is not None:
                health = health[0] | (health[1] << 8)
            if not gamemode or gamemode[0] in SM_DEATH_MODES or (
                    ctx.death_link_allow_survive and health is not None and health > 0):
                ctx.death_state = DeathState.dead
        ctx.last_death_link = time.time()


SNES_RECONNECT_DELAY = 5

# LttP
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

# SM
SM_ROMNAME_START = 0x007FC0

SM_INGAME_MODES = {0x07, 0x09, 0x0b}
SM_ENDGAME_MODES = {0x26, 0x27}
SM_DEATH_MODES = {0x15, 0x17, 0x18, 0x19, 0x1A}

SM_RECV_PROGRESS_ADDR = SRAM_START + 0x2000         # 2 bytes
SM_RECV_ITEM_ADDR = SAVEDATA_START + 0x4D2          # 1 byte
SM_RECV_ITEM_PLAYER_ADDR = SAVEDATA_START + 0x4D3   # 1 byte

SM_DEATH_LINK_ACTIVE_ADDR = ROM_START + 0x277f04    # 1 byte
SM_REMOTE_ITEM_FLAG_ADDR = ROM_START + 0x277f06    # 1 byte

# SMZ3
SMZ3_ROMNAME_START = 0x00FFC0

SMZ3_INGAME_MODES = {0x07, 0x09, 0x0b}
SMZ3_ENDGAME_MODES = {0x26, 0x27}
SMZ3_DEATH_MODES = {0x15, 0x17, 0x18, 0x19, 0x1A}

SMZ3_RECV_PROGRESS_ADDR = SRAM_START + 0x4000         # 2 bytes
SMZ3_RECV_ITEM_ADDR = SAVEDATA_START + 0x4D2          # 1 byte
SMZ3_RECV_ITEM_PLAYER_ADDR = SAVEDATA_START + 0x4D3   # 1 byte


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
                     'Hyrule Castle - Key Rat Key Drop': (0x21, 0x400),
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

boss_locations = {Regions.lookup_name_to_id[name] for name in {'Eastern Palace - Boss',
                                                                           'Desert Palace - Boss',
                                                                           'Tower of Hera - Boss',
                                                                           'Palace of Darkness - Boss',
                                                                           'Swamp Palace - Boss',
                                                                           'Skull Woods - Boss',
                                                                           "Thieves' Town - Boss",
                                                                           'Ice Palace - Boss',
                                                                           'Misery Mire - Boss',
                                                                           'Turtle Rock - Boss',
                                                                           'Sahasrahla'}}

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


class SNESState(enum.IntEnum):
    SNES_DISCONNECTED = 0
    SNES_CONNECTING = 1
    SNES_CONNECTED = 2
    SNES_ATTACHED = 3


def launch_sni(ctx: Context):
    sni_path = Utils.get_options()["lttp_options"]["sni"]

    if not os.path.isdir(sni_path):
        sni_path = Utils.local_path(sni_path)
    if os.path.isdir(sni_path):
        dir_entry: os.DirEntry
        for dir_entry in os.scandir(sni_path):
            if dir_entry.is_file():
                lower_file = dir_entry.name.lower()
                if (lower_file.startswith("sni.") and not lower_file.endswith(".proto")) or (lower_file == "sni"):
                    sni_path = dir_entry.path
                    break

    if os.path.isfile(sni_path):
        snes_logger.info(f"Attempting to start {sni_path}")
        import sys
        if not sys.stdout:  # if it spawns a visible console, may as well populate it
            subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path))
        else:
            proc = subprocess.Popen(os.path.abspath(sni_path), cwd=os.path.dirname(sni_path),
                                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                proc.wait(.1)  # wait a bit to see if startup fails (missing dependencies)
                snes_logger.info('Failed to start SNI. Try running it externally for error output.')
            except subprocess.TimeoutExpired:
                pass  # seems to be running

    else:
        snes_logger.info(
            f"Attempt to start SNI was aborted as path {sni_path} was not found, "
            f"please start it yourself if it is not running")


async def _snes_connect(ctx: Context, address: str):
    address = f"ws://{address}" if "://" not in address else address
    snes_logger.info("Connecting to SNI at %s ..." % address)
    seen_problems = set()
    succesful = False
    while not succesful:
        try:
            snes_socket = await websockets.connect(address, ping_timeout=None, ping_interval=None)
            succesful = True
        except Exception as e:
            problem = "%s" % e
            # only tell the user about new problems, otherwise silently lay in wait for a working connection
            if problem not in seen_problems:
                seen_problems.add(problem)
                snes_logger.error(f"Error connecting to SNI ({problem})")

                if len(seen_problems) == 1:
                    # this is the first problem. Let's try launching SNI if it isn't already running
                    launch_sni(ctx)

            await asyncio.sleep(1)
        else:
            return snes_socket


async def get_snes_devices(ctx: Context):
    socket = await _snes_connect(ctx, ctx.snes_address)  # establish new connection to poll
    DeviceList_Request = {
        "Opcode": "DeviceList",
        "Space": "SNES"
    }
    await socket.send(dumps(DeviceList_Request))

    reply = loads(await socket.recv())
    devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None

    if not devices:
        snes_logger.info('No SNES device found. Please connect a SNES device to SNI.')
        while not devices:
            await asyncio.sleep(1)
            await socket.send(dumps(DeviceList_Request))
            reply = loads(await socket.recv())
            devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None
    await verify_snes_app(socket)
    await socket.close()
    return devices


async def verify_snes_app(socket):
    AppVersion_Request = {
        "Opcode": "AppVersion",
    }
    await socket.send(dumps(AppVersion_Request))

    app: str = loads(await socket.recv())["Results"][0]
    if "SNI" not in app:
        snes_logger.warning(f"Warning: Did not find SNI as the endpoint, instead {app} was found.")


async def snes_connect(ctx: Context, address, deviceIndex=-1):
    global SNES_RECONNECT_DELAY
    if ctx.snes_socket is not None and ctx.snes_state == SNESState.SNES_CONNECTED:
        if ctx.rom:
            snes_logger.error('Already connected to SNES, with rom loaded.')
        else:
            snes_logger.error('Already connected to SNI, likely awaiting a device.')
        return

    device = None
    recv_task = None
    ctx.snes_state = SNESState.SNES_CONNECTING
    socket = await _snes_connect(ctx, address)
    ctx.snes_socket = socket
    ctx.snes_state = SNESState.SNES_CONNECTED

    try:
        devices = await get_snes_devices(ctx)
        device_count = len(devices)

        if device_count == 1:
            device = devices[0]
        elif ctx.snes_reconnect_address:
            if ctx.snes_attached_device[1] in devices:
                device = ctx.snes_attached_device[1]
            else:
                device = devices[ctx.snes_attached_device[0]]
        elif device_count > 1:
            if deviceIndex == -1:
                snes_logger.info(f"Found {device_count} SNES devices. "
                                 f"Connect to one with /snes <address> <device number>. For example /snes {address} 1")

                for idx, availableDevice in enumerate(devices):
                    snes_logger.info(str(idx + 1) + ": " + availableDevice)

            elif (deviceIndex < 0) or (deviceIndex - 1) > device_count:
                snes_logger.warning("SNES device number out of range")

            else:
                device = devices[deviceIndex - 1]

        if device is None:
            await snes_disconnect(ctx)
            return

        snes_logger.info("Attaching to " + device)

        Attach_Request = {
            "Opcode": "Attach",
            "Space": "SNES",
            "Operands": [device]
        }
        await ctx.snes_socket.send(dumps(Attach_Request))
        ctx.snes_state = SNESState.SNES_ATTACHED
        ctx.snes_attached_device = (devices.index(device), device)
        ctx.snes_reconnect_address = address
        recv_task = asyncio.create_task(snes_recv_loop(ctx))

    except Exception as e:
        if recv_task is not None:
            if not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
        else:
            if ctx.snes_socket is not None:
                if not ctx.snes_socket.closed:
                    await ctx.snes_socket.close()
                ctx.snes_socket = None
            ctx.snes_state = SNESState.SNES_DISCONNECTED
        if not ctx.snes_reconnect_address:
            snes_logger.error("Error connecting to snes (%s)" % e)
        else:
            snes_logger.error(f"Error connecting to snes, attempt again in {SNES_RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))
        SNES_RECONNECT_DELAY *= 2

    else:
        SNES_RECONNECT_DELAY = ctx.starting_reconnect_delay
        snes_logger.info(f"Attached to {device}")


async def snes_disconnect(ctx: Context):
    if ctx.snes_socket:
        if not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        ctx.snes_socket = None


async def snes_autoreconnect(ctx: Context):
    await asyncio.sleep(SNES_RECONNECT_DELAY)
    if ctx.snes_reconnect_address and ctx.snes_socket is None:
        await snes_connect(ctx, ctx.snes_reconnect_address)


async def snes_recv_loop(ctx: Context):
    try:
        async for msg in ctx.snes_socket:
            ctx.snes_recv_queue.put_nowait(msg)
        snes_logger.warning("Snes disconnected")
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            snes_logger.exception(e)
        snes_logger.error("Lost connection to the snes, type /snes to reconnect")
    finally:
        socket, ctx.snes_socket = ctx.snes_socket, None
        if socket is not None and not socket.closed:
            await socket.close()

        ctx.snes_state = SNESState.SNES_DISCONNECTED
        ctx.snes_recv_queue = asyncio.Queue()
        ctx.hud_message_queue = []

        ctx.rom = None

        if ctx.snes_reconnect_address:
            snes_logger.info(f"...reconnecting in {SNES_RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))


async def snes_read(ctx: Context, address, size):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNESState.SNES_ATTACHED or ctx.snes_socket is None or not ctx.snes_socket.open or ctx.snes_socket.closed:
            return None

        GetAddress_Request = {
            "Opcode": "GetAddress",
            "Space": "SNES",
            "Operands": [hex(address)[2:], hex(size)[2:]]
        }
        try:
            await ctx.snes_socket.send(dumps(GetAddress_Request))
        except websockets.ConnectionClosed:
            return None

        data = bytes()
        while len(data) < size:
            try:
                data += await asyncio.wait_for(ctx.snes_recv_queue.get(), 5)
            except asyncio.TimeoutError:
                break

        if len(data) != size:
            snes_logger.error('Error reading %s, requested %d bytes, received %d' % (hex(address), size, len(data)))
            if len(data):
                snes_logger.error(str(data))
                snes_logger.warning('Communication Failure with SNI')
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
            return None

        return data
    finally:
        ctx.snes_request_lock.release()


async def snes_write(ctx: Context, write_list):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNESState.SNES_ATTACHED or ctx.snes_socket is None or \
                not ctx.snes_socket.open or ctx.snes_socket.closed:
            return False

        PutAddress_Request = {"Opcode": "PutAddress", "Operands": [], 'Space': 'SNES'}
        try:
            for address, data in write_list:
                PutAddress_Request['Operands'] = [hex(address)[2:], hex(len(data))[2:]]
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(dumps(PutAddress_Request))
                    await ctx.snes_socket.send(data)
                else:
                    snes_logger.warning(f"Could not send data to SNES: {data}")
        except websockets.ConnectionClosed:
            return False

        return True
    finally:
        ctx.snes_request_lock.release()


def snes_buffered_write(ctx: Context, address, data):
    if ctx.snes_write_buffer and (ctx.snes_write_buffer[-1][0] + len(ctx.snes_write_buffer[-1][1])) == address:
        # append to existing write command, bundling them
        ctx.snes_write_buffer[-1] = (ctx.snes_write_buffer[-1][0], ctx.snes_write_buffer[-1][1] + data)
    else:
        ctx.snes_write_buffer.append((address, data))


async def snes_flush_writes(ctx: Context):
    if not ctx.snes_write_buffer:
        return

    # swap buffers
    ctx.snes_write_buffer, writes = [], ctx.snes_write_buffer
    await snes_write(ctx, writes)


async def track_locations(ctx: Context, roomid, roomdata):
    new_locations = []

    def new_check(location_id):
        new_locations.append(location_id)
        ctx.locations_checked.add(location_id)
        location = ctx.location_name_getter(location_id)
        snes_logger.info(
            f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')

    try:
        shop_data = await snes_read(ctx, SHOP_ADDR, SHOP_LEN)
        shop_data_changed = False
        shop_data = list(shop_data)
        for cnt, b in enumerate(shop_data):
            location = Shops.SHOP_ID_START + cnt
            if int(b) and location not in ctx.locations_checked:
                new_check(location)
            if ctx.allow_collect and location in ctx.checked_locations and location not in ctx.locations_checked \
                    and location in ctx.locations_info and ctx.locations_info[location].player != ctx.slot:
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
        if ctx.allow_collect and location_id not in boss_locations and location_id in ctx.checked_locations \
                and location_id not in ctx.locations_checked and location_id in ctx.locations_info \
                and ctx.locations_info[location_id].player != ctx.slot:
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
            if ctx.allow_collect and location_id in ctx.checked_locations and location_id in ctx.locations_info \
                    and ctx.locations_info[location_id].player != ctx.slot:
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
                if ctx.allow_collect and location_id not in boss_locations and location_id in ctx.checked_locations \
                        and location_id not in ctx.locations_checked and location_id in ctx.locations_info \
                        and ctx.locations_info[location_id].player != ctx.slot:
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
                if ctx.allow_collect and location_id in ctx.checked_locations and location_id not in ctx.locations_checked \
                        and location_id in ctx.locations_info and ctx.locations_info[location_id].player != ctx.slot:
                    misc_data_changed = True
                    misc_data[offset - 0x3c6] |= mask
            if misc_data_changed:
                snes_buffered_write(ctx, SAVEDATA_START + 0x3c6, bytes(misc_data))


    if new_locations:
        await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])
    await snes_flush_writes(ctx)


async def game_watcher(ctx: Context):
    prev_game_timer = 0
    perf_counter = time.perf_counter()
    while not ctx.exit_event.is_set():
        try:
            await asyncio.wait_for(ctx.watcher_event.wait(), 0.125)
        except asyncio.TimeoutError:
            pass
        ctx.watcher_event.clear()

        if not ctx.rom:
            ctx.finished_game = False
            ctx.death_link_allow_survive = False
            game_name = await snes_read(ctx, SM_ROMNAME_START, 5)
            if game_name is None:
                continue
            elif game_name[:2] == b"SM":
                ctx.game = GAME_SM
                # versions lower than 0.3.0 dont have item handling flag nor remote item support
                romVersion = int(game_name[2:5].decode('UTF-8'))
                if romVersion < 30:
                    ctx.items_handling = 0b001 # full local 
                else:
                    item_handling = await snes_read(ctx, SM_REMOTE_ITEM_FLAG_ADDR, 1)
                    ctx.items_handling = 0b001 if item_handling is None else item_handling[0]
            else:
                game_name = await snes_read(ctx, SMZ3_ROMNAME_START, 3)
                if game_name == b"ZSM":
                    ctx.game = GAME_SMZ3
                    ctx.items_handling = 0b101  # local items and remote start inventory
                else:
                    ctx.game = GAME_ALTTP
                    ctx.items_handling = 0b001  # full local

            rom = await snes_read(ctx, SM_ROMNAME_START if ctx.game == GAME_SM else SMZ3_ROMNAME_START if ctx.game == GAME_SMZ3 else ROMNAME_START, ROMNAME_SIZE)
            if rom is None or rom == bytes([0] * ROMNAME_SIZE):
                continue

            ctx.rom = rom
            if ctx.game != GAME_SMZ3:
                death_link = await snes_read(ctx, DEATH_LINK_ACTIVE_ADDR if ctx.game == GAME_ALTTP else
                                             SM_DEATH_LINK_ACTIVE_ADDR, 1)
                if death_link:
                    ctx.allow_collect = bool(death_link[0] & 0b100)
                    ctx.death_link_allow_survive = bool(death_link[0] & 0b10)
                    await ctx.update_death_link(bool(death_link[0] & 0b1))
            if not ctx.prev_rom or ctx.prev_rom != ctx.rom:
                ctx.locations_checked = set()
                ctx.locations_scouted = set()
                ctx.locations_info = {}
            ctx.prev_rom = ctx.rom

            if ctx.awaiting_rom:
                await ctx.server_auth(False)

        if ctx.auth and ctx.auth != ctx.rom:
            snes_logger.warning("ROM change detected, please reconnect to the multiworld server")
            await ctx.disconnect()

        if ctx.game == GAME_ALTTP:
            gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
            if "DeathLink" in ctx.tags and gamemode and ctx.last_death_link + 1 < time.time():
                currently_dead = gamemode[0] in DEATH_MODES
                await ctx.handle_deathlink_state(currently_dead)

            gameend = await snes_read(ctx, SAVEDATA_START + 0x443, 1)
            game_timer = await snes_read(ctx, SAVEDATA_START + 0x42E, 4)
            if gamemode is None or gameend is None or game_timer is None or \
                    (gamemode[0] not in INGAME_MODES and gamemode[0] not in ENDGAME_MODES):
                continue

            delay = 7 if ctx.slow_mode else 2
            if gameend[0]:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True

                if time.perf_counter() - perf_counter < delay:
                    continue
                else:
                    perf_counter = time.perf_counter()
            else:
                game_timer = game_timer[0] | (game_timer[1] << 8) | (game_timer[2] << 16) | (game_timer[3] << 24)
                if abs(game_timer - prev_game_timer) < (delay * 60):
                    continue
                else:
                    prev_game_timer = game_timer

            if gamemode in ENDGAME_MODES:  # triforce room and credits
                continue

            data = await snes_read(ctx, RECV_PROGRESS_ADDR, 8)
            if data is None:
                continue

            recv_index = data[0] | (data[1] << 8)
            recv_item = data[2]
            roomid = data[4] | (data[5] << 8)
            roomdata = data[6]
            scout_location = data[7]

            if recv_index < len(ctx.items_received) and recv_item == 0:
                item = ctx.items_received[recv_index]
                recv_index += 1
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_name_getter(item.item), 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_name_getter(item.location), recv_index, len(ctx.items_received)))

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
            await track_locations(ctx, roomid, roomdata)
        elif ctx.game == GAME_SM:
            gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
            if "DeathLink" in ctx.tags and gamemode and ctx.last_death_link + 1 < time.time():
                currently_dead = gamemode[0] in SM_DEATH_MODES
                await ctx.handle_deathlink_state(currently_dead)
            if gamemode is not None and gamemode[0] in SM_ENDGAME_MODES:
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
                continue

            data = await snes_read(ctx, SM_RECV_PROGRESS_ADDR + 0x680, 4)
            if data is None:
                continue

            recv_index = data[0] | (data[1] << 8)
            recv_item = data[2] | (data[3] << 8)

            while (recv_index < recv_item):
                itemAdress = recv_index * 8
                message = await snes_read(ctx, SM_RECV_PROGRESS_ADDR + 0x700 + itemAdress, 8)
                # worldId = message[0] | (message[1] << 8)  # unused
                # itemId = message[2] | (message[3] << 8)  # unused
                itemIndex = (message[4] | (message[5] << 8)) >> 3

                recv_index += 1
                snes_buffered_write(ctx, SM_RECV_PROGRESS_ADDR + 0x680,
                                    bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))

                from worlds.sm.Locations import locations_start_id
                location_id = locations_start_id + itemIndex

                ctx.locations_checked.add(location_id)
                location = ctx.location_name_getter(location_id)
                snes_logger.info(
                    f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

            data = await snes_read(ctx, SM_RECV_PROGRESS_ADDR + 0x600, 4)
            if data is None:
                continue

            # recv_itemOutPtr = data[0] | (data[1] << 8) # unused
            itemOutPtr = data[2] | (data[3] << 8)

            from worlds.sm.Items import items_start_id
            from worlds.sm.Locations import locations_start_id
            if itemOutPtr < len(ctx.items_received):
                item = ctx.items_received[itemOutPtr]
                itemId = item.item - items_start_id
                if bool(ctx.items_handling & 0b010):
                    locationId = (item.location - locations_start_id) if (item.location >= 0 and item.player == ctx.slot) else 0xFF
                else:
                    locationId = 0x00 #backward compat

                playerID = item.player if item.player <= SM_ROM_PLAYER_LIMIT else 0
                snes_buffered_write(ctx, SM_RECV_PROGRESS_ADDR + itemOutPtr * 4, bytes(
                	[playerID & 0xFF, (playerID >> 8) & 0xFF, itemId & 0xFF, locationId & 0xFF]))
                itemOutPtr += 1
                snes_buffered_write(ctx, SM_RECV_PROGRESS_ADDR + 0x602,
                                    bytes([itemOutPtr & 0xFF, (itemOutPtr >> 8) & 0xFF]))
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_name_getter(item.item), 'red', 'bold'),
                    color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_name_getter(item.location), itemOutPtr, len(ctx.items_received)))
            await snes_flush_writes(ctx)
        elif ctx.game == GAME_SMZ3:
            currentGame = await snes_read(ctx, SRAM_START + 0x33FE, 2)
            if (currentGame is not None):
                if (currentGame[0] != 0):
                    gamemode = await snes_read(ctx, WRAM_START + 0x0998, 1)
                    endGameModes = SM_ENDGAME_MODES
                else:
                    gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
                    endGameModes = ENDGAME_MODES

            if gamemode is not None and (gamemode[0] in endGameModes):
                if not ctx.finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
                continue

            data = await snes_read(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x680, 4)
            if data is None:
                continue

            recv_index = data[0] | (data[1] << 8)
            recv_item = data[2] | (data[3] << 8)

            while (recv_index < recv_item):
                itemAdress = recv_index * 8
                message = await snes_read(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x700 + itemAdress, 8)
                # worldId = message[0] | (message[1] << 8)  # unused
                # itemId = message[2] | (message[3] << 8)  # unused
                isZ3Item = ((message[5] & 0x80) != 0)
                maskedPart = (message[5] & 0x7F) if isZ3Item else message[5]
                itemIndex = ((message[4] | (maskedPart << 8)) >> 3) + (256 if isZ3Item else 0)

                recv_index += 1
                snes_buffered_write(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x680, bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))

                from worlds.smz3.TotalSMZ3.Location import locations_start_id
                location_id = locations_start_id + itemIndex

                ctx.locations_checked.add(location_id)
                location = ctx.location_name_getter(location_id)
                snes_logger.info(f'New Check: {location} ({len(ctx.locations_checked)}/{len(ctx.missing_locations) + len(ctx.checked_locations)})')
                await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": [location_id]}])

            data = await snes_read(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x600, 4)
            if data is None:
                continue

            # recv_itemOutPtr = data[0] | (data[1] << 8) # unused
            itemOutPtr = data[2] | (data[3] << 8)

            from worlds.smz3.TotalSMZ3.Item import items_start_id
            if itemOutPtr < len(ctx.items_received):
                item = ctx.items_received[itemOutPtr]
                itemId = item.item - items_start_id

                playerID = item.player if item.player <= SMZ3_ROM_PLAYER_LIMIT else 0
                snes_buffered_write(ctx, SMZ3_RECV_PROGRESS_ADDR + itemOutPtr * 4, bytes([playerID & 0xFF, (playerID >> 8) & 0xFF, itemId & 0xFF, (itemId >> 8) & 0xFF]))
                itemOutPtr += 1
                snes_buffered_write(ctx, SMZ3_RECV_PROGRESS_ADDR + 0x602, bytes([itemOutPtr & 0xFF, (itemOutPtr >> 8) & 0xFF]))
                logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                    color(ctx.item_name_getter(item.item), 'red', 'bold'), color(ctx.player_names[item.player], 'yellow'),
                    ctx.location_name_getter(item.location), itemOutPtr, len(ctx.items_received)))
            await snes_flush_writes(ctx)


async def run_game(romfile):
    auto_start = Utils.get_options()["lttp_options"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def main():
    multiprocessing.freeze_support()
    parser = get_base_parser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Archipelago Binary Patch file')
    parser.add_argument('--snes', default='localhost:8080', help='Address of the SNI server.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()

    if args.diff_file:
        import Patch
        logging.info("Patch file was supplied. Creating sfc rom..")
        meta, romfile = Patch.create_rom_file(args.diff_file)
        if "server" in meta:
            args.connect = meta["server"]
        logging.info(f"Wrote rom file to {romfile}")
        if args.diff_file.endswith(".apsoe"):
            import webbrowser
            webbrowser.open("http://www.evermizer.com/apclient/" +
                            (f"#server={meta['server']}" if "server" in meta else ""))
            logging.info("Starting Evermizer Client in your Browser...")
            import time
            time.sleep(3)
            sys.exit()
        elif args.diff_file.endswith((".apbp", ".apz3", ".aplttp")):
            adjustedromfile, adjusted = get_alttp_settings(romfile)
            asyncio.create_task(run_game(adjustedromfile if adjusted else romfile))
        else:
            asyncio.create_task(run_game(romfile))

    ctx = Context(args.snes, args.connect, args.password)
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    snes_connect_task = asyncio.create_task(snes_connect(ctx, ctx.snes_address), name="SNES Connect")
    watcher_task = asyncio.create_task(game_watcher(ctx), name="GameWatcher")

    await ctx.exit_event.wait()

    ctx.server_address = None
    ctx.snes_reconnect_address = None
    if ctx.snes_socket is not None and not ctx.snes_socket.closed:
        await ctx.snes_socket.close()
    if snes_connect_task:
        snes_connect_task.cancel()
    await watcher_task
    await ctx.shutdown()


def get_alttp_settings(romfile: str):
    lastSettings = Utils.get_adjuster_settings(GAME_ALTTP)
    adjusted = False
    adjustedromfile = ''
    if lastSettings:
        choice = 'no'
        if not hasattr(lastSettings, 'auto_apply') or 'ask' in lastSettings.auto_apply:

            whitelist = {"music", "menuspeed", "heartbeep", "heartcolor", "ow_palettes", "quickswap",
                         "uw_palettes", "sprite", "sword_palettes", "shield_palettes", "hud_palettes",
                         "reduceflashing", "deathlink", "allowcollect"}
            printed_options = {name: value for name, value in vars(lastSettings).items() if name in whitelist}
            if hasattr(lastSettings, "sprite_pool"):
                sprite_pool = {}
                for sprite in lastSettings.sprite_pool:
                    if sprite in sprite_pool:
                        sprite_pool[sprite] += 1
                    else:
                        sprite_pool[sprite] = 1
                    if sprite_pool:
                        printed_options["sprite_pool"] = sprite_pool
            import pprint

            if gui_enabled:

                from tkinter import Tk, PhotoImage, Label, LabelFrame, Frame, Button
                applyPromptWindow = Tk()
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
                lastSettings.auto_apply = 'never'
                Utils.persistent_store("adjuster", GAME_ALTTP, lastSettings)
            elif choice and "always" in choice:
                choice = 'yes'
                lastSettings.auto_apply = 'always'
                Utils.persistent_store("adjuster", GAME_ALTTP, lastSettings)
            else:
                choice = 'no'
        elif 'never' in lastSettings.auto_apply:
            choice = 'no'
        elif 'always' in lastSettings.auto_apply:
            choice = 'yes'

        if 'yes' in choice:
            from worlds.alttp.Rom import get_base_rom_path
            lastSettings.rom = romfile
            lastSettings.baserom = get_base_rom_path()
            lastSettings.world = None

            if hasattr(lastSettings, "sprite_pool"):
                from LttPAdjuster import AdjusterWorld
                lastSettings.world = AdjusterWorld(getattr(lastSettings, "sprite_pool"))

            adjusted = True
            import LttPAdjuster
            _, adjustedromfile = LttPAdjuster.adjust(lastSettings)

            if hasattr(lastSettings, "world"):
                delattr(lastSettings, "world")
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


if __name__ == '__main__':
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
