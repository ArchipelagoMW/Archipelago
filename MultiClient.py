import argparse
import asyncio
import json
import logging
import urllib.parse
import atexit
import time
import functools
import webbrowser
import multiprocessing
import socket
import sys
import typing
import os
import subprocess

from random import randrange

from Utils import get_item_name_from_id, get_location_name_from_address, ReceivedItem

exit_func = atexit.register(input, "Press enter to close.")

import ModuleUpdate

ModuleUpdate.update()

import colorama
import websockets
import prompt_toolkit

from prompt_toolkit.patch_stdout import patch_stdout
from NetUtils import Endpoint
import WebUI

import Regions
import Utils


def create_named_task(coro, *args, name=None):
    if not name:
        name = coro.__name__
    if sys.version_info.major > 2 and sys.version_info.minor > 7:
        return asyncio.create_task(coro, *args, name=name)
    else:
        return asyncio.create_task(coro, *args)


class Context():
    def __init__(self, snes_address, server_address, password, found_items, port: int):
        self.snes_address = snes_address
        self.server_address = server_address

        # WebUI Stuff
        self.ui_node = WebUI.WebUiClient()
        self.custom_address = None
        self.webui_socket_port: typing.Optional[int] = port
        self.hint_cost = 0
        self.check_points = 0
        self.forfeit_mode = ''
        self.remaining_mode = ''
        self.hint_points = 0
        # End WebUI Stuff

        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        self.snes_socket = None
        self.snes_state = SNES_DISCONNECTED
        self.snes_attached_device = None
        self.snes_reconnect_address = None
        self.snes_recv_queue = asyncio.Queue()
        self.snes_request_lock = asyncio.Lock()
        self.is_sd2snes = False
        self.snes_write_buffer = []

        self.server_task = None
        self.server: typing.Optional[Endpoint] = None
        self.password = password
        self.server_version = (0, 0, 0)

        self.team = None
        self.slot = None
        self.player_names: typing.Dict[int: str] = {}
        self.locations_checked = set()
        self.locations_scouted = set()
        self.items_received = []
        self.locations_info = {}
        self.awaiting_rom = False
        self.rom = None
        self.prev_rom = None
        self.auth = None
        self.found_items = found_items
        self.finished_game = False
        self.slow_mode = False

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def disconnect(self):
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
            self.ui_node.send_connection_status(self)
        if self.server_task is not None:
            await self.server_task

    async def send_msgs(self, msgs):
        if not self.server or not self.server.socket.open or self.server.socket.closed:
            return
        await self.server.socket.send(json.dumps(msgs))

color_codes = {'reset': 0, 'bold': 1, 'underline': 4, 'black': 30, 'red': 31, 'green': 32, 'yellow': 33, 'blue': 34,
               'magenta': 35, 'cyan': 36, 'white': 37, 'black_bg': 40, 'red_bg': 41, 'green_bg': 42, 'yellow_bg': 43,
               'blue_bg': 44, 'purple_bg': 45, 'cyan_bg': 46, 'white_bg': 47}


def color_code(*args):
    return '\033[' + ';'.join([str(color_codes[arg]) for arg in args]) + 'm'


def color(text, *args):
    return color_code(*args) + text + color_code('reset')


START_RECONNECT_DELAY = 5
SNES_RECONNECT_DELAY = 5
SERVER_RECONNECT_DELAY = 5

ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

ROMNAME_START = SRAM_START + 0x2000
ROMNAME_SIZE = 0x15

INGAME_MODES = {0x07, 0x09, 0x0b}
ENDGAME_MODES = {0x19, 0x1a}

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
                     'Desert Palace - Boss': (0x33, 0x800),
                     'Eastern Palace - Compass Chest': (0xa8, 0x10),
                     'Eastern Palace - Big Chest': (0xa9, 0x10),
                     'Eastern Palace - Cannonball Chest': (0xb9, 0x10),
                     'Eastern Palace - Big Key Chest': (0xb8, 0x10),
                     'Eastern Palace - Map Chest': (0xaa, 0x10),
                     'Eastern Palace - Boss': (0xc8, 0x800),
                     'Hyrule Castle - Boomerang Chest': (0x71, 0x10),
                     'Hyrule Castle - Map Chest': (0x72, 0x10),
                     "Hyrule Castle - Zelda's Chest": (0x80, 0x10),
                     'Sewers - Dark Cross': (0x32, 0x10),
                     'Sewers - Secret Room - Left': (0x11, 0x10),
                     'Sewers - Secret Room - Middle': (0x11, 0x20),
                     'Sewers - Secret Room - Right': (0x11, 0x40),
                     'Sanctuary': (0x12, 0x10),
                     'Castle Tower - Room 03': (0xe0, 0x10),
                     'Castle Tower - Dark Maze': (0xd0, 0x10),
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
                     'Swamp Palace - Big Chest': (0x36, 0x10),
                     'Swamp Palace - Compass Chest': (0x46, 0x10),
                     'Swamp Palace - Big Key Chest': (0x35, 0x10),
                     'Swamp Palace - West Chest': (0x34, 0x10),
                     'Swamp Palace - Flooded Room - Left': (0x76, 0x10),
                     'Swamp Palace - Flooded Room - Right': (0x76, 0x20),
                     'Swamp Palace - Waterfall Room': (0x66, 0x10),
                     'Swamp Palace - Boss': (0x6, 0x800),
                     "Thieves' Town - Big Key Chest": (0xdb, 0x20),
                     "Thieves' Town - Map Chest": (0xdb, 0x10),
                     "Thieves' Town - Compass Chest": (0xdc, 0x10),
                     "Thieves' Town - Ambush Chest": (0xcb, 0x10),
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
                     'Skull Woods - Bridge Room': (0x59, 0x10),
                     'Skull Woods - Boss': (0x29, 0x800),
                     'Ice Palace - Compass Chest': (0x2e, 0x10),
                     'Ice Palace - Freezor Chest': (0x7e, 0x10),
                     'Ice Palace - Big Chest': (0x9e, 0x10),
                     'Ice Palace - Iced T Room': (0xae, 0x10),
                     'Ice Palace - Spike Room': (0x5f, 0x10),
                     'Ice Palace - Big Key Chest': (0x1f, 0x10),
                     'Ice Palace - Map Chest': (0x3f, 0x10),
                     'Ice Palace - Boss': (0xde, 0x800),
                     'Misery Mire - Big Chest': (0xc3, 0x10),
                     'Misery Mire - Map Chest': (0xc3, 0x20),
                     'Misery Mire - Main Lobby': (0xc2, 0x10),
                     'Misery Mire - Bridge Chest': (0xa2, 0x10),
                     'Misery Mire - Spike Chest': (0xb3, 0x10),
                     'Misery Mire - Compass Chest': (0xc1, 0x10),
                     'Misery Mire - Big Key Chest': (0xd1, 0x10),
                     'Misery Mire - Boss': (0x90, 0x800),
                     'Turtle Rock - Compass Chest': (0xd6, 0x10),
                     'Turtle Rock - Roller Room - Left': (0xb7, 0x10),
                     'Turtle Rock - Roller Room - Right': (0xb7, 0x20),
                     'Turtle Rock - Chain Chomps': (0xb6, 0x10),
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
                     "Ganons Tower - Bob's Torch": (0x8c, 0x400),
                     'Ganons Tower - Hope Room - Left': (0x8c, 0x20),
                     'Ganons Tower - Hope Room - Right': (0x8c, 0x40),
                     'Ganons Tower - Tile Room': (0x8d, 0x10),
                     'Ganons Tower - Compass Room - Top Left': (0x9d, 0x10),
                     'Ganons Tower - Compass Room - Top Right': (0x9d, 0x20),
                     'Ganons Tower - Compass Room - Bottom Left': (0x9d, 0x40),
                     'Ganons Tower - Compass Room - Bottom Right': (0x9d, 0x80),
                     'Ganons Tower - DMs Room - Top Left': (0x7b, 0x10),
                     'Ganons Tower - DMs Room - Top Right': (0x7b, 0x20),
                     'Ganons Tower - DMs Room - Bottom Left': (0x7b, 0x40),
                     'Ganons Tower - DMs Room - Bottom Right': (0x7b, 0x80),
                     'Ganons Tower - Map Chest': (0x8b, 0x10),
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
                     'Ganons Tower - Pre-Moldorm Chest': (0x3d, 0x40),
                     'Ganons Tower - Validation Chest': (0x4d, 0x10)}
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
location_table_misc = {'Bottle Merchant': (0x3c9, 0x2),
                       'Purple Chest': (0x3c9, 0x10),
                       "Link's Uncle": (0x3c6, 0x1),
                       'Hobo': (0x3c9, 0x1)}

SNES_DISCONNECTED = 0
SNES_CONNECTING = 1
SNES_CONNECTED = 2
SNES_ATTACHED = 3


def launch_qusb2snes(ctx: Context):
    qusb2snes_path = Utils.get_options()["general_options"]["qusb2snes"]

    if not os.path.isfile(qusb2snes_path):
        qusb2snes_path = Utils.local_path(qusb2snes_path)

    if os.path.isfile(qusb2snes_path):
        ctx.ui_node.log_info(f"Attempting to start {qusb2snes_path}")
        import subprocess
        subprocess.Popen(qusb2snes_path, cwd=os.path.dirname(qusb2snes_path))
    else:
        ctx.ui_node.log_info(
            f"Attempt to start (Q)Usb2Snes was aborted as path {qusb2snes_path} was not found, "
            f"please start it yourself if it is not running")


async def _snes_connect(ctx: Context, address: str):
    address = f"ws://{address}" if "://" not in address else address

    ctx.ui_node.log_info("Connecting to QUsb2snes at %s ..." % address)
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
                ctx.ui_node.log_error(f"Error connecting to QUsb2snes ({problem})")

                if len(seen_problems) == 1:
                    # this is the first problem. Let's try launching QUsb2snes if it isn't already running
                    launch_qusb2snes(ctx)

            await asyncio.sleep(1)
        else:
            return snes_socket


async def get_snes_devices(ctx: Context):
    socket = await _snes_connect(ctx, ctx.snes_address)  # establish new connection to poll
    DeviceList_Request = {
        "Opcode": "DeviceList",
        "Space": "SNES"
    }
    await socket.send(json.dumps(DeviceList_Request))

    reply = json.loads(await socket.recv())
    devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None

    if not devices:
        ctx.ui_node.log_info('No SNES device found. Ensure QUsb2Snes is running and connect it to the multibridge.')
        while not devices:
            await asyncio.sleep(1)
            await socket.send(json.dumps(DeviceList_Request))
            reply = json.loads(await socket.recv())
            devices = reply['Results'] if 'Results' in reply and len(reply['Results']) > 0 else None

    ctx.ui_node.send_device_list(devices)
    await socket.close()
    return devices


async def snes_connect(ctx: Context, address):
    global SNES_RECONNECT_DELAY
    if ctx.snes_socket is not None and ctx.snes_state == SNES_CONNECTED:
        ctx.ui_node.log_error('Already connected to snes')
        return

    recv_task = None
    ctx.snes_state = SNES_CONNECTING
    socket = await _snes_connect(ctx, address)
    ctx.snes_socket = socket
    ctx.snes_state = SNES_CONNECTED

    try:
        devices = await get_snes_devices(ctx)

        if len(devices) == 1:
            device = devices[0]
        elif ctx.ui_node.manual_snes and ctx.ui_node.manual_snes in devices:
            device = ctx.ui_node.manual_snes
        elif ctx.snes_reconnect_address:
            if ctx.snes_attached_device[1] in devices:
                device = ctx.snes_attached_device[1]
            else:
                device = devices[ctx.snes_attached_device[0]]
        else:
            await snes_disconnect(ctx)
            return


        ctx.ui_node.log_info("Attaching to " + device)

        Attach_Request = {
            "Opcode": "Attach",
            "Space": "SNES",
            "Operands": [device]
        }
        await ctx.snes_socket.send(json.dumps(Attach_Request))
        ctx.snes_state = SNES_ATTACHED
        ctx.snes_attached_device = (devices.index(device), device)
        ctx.ui_node.send_connection_status(ctx)

        if 'sd2snes' in device.lower() or (len(device) == 4 and device[:3] == 'COM'):
            ctx.ui_node.log_info("SD2SNES Detected")
            ctx.is_sd2snes = True
            await ctx.snes_socket.send(json.dumps({"Opcode" : "Info", "Space" : "SNES"}))
            reply = json.loads(await ctx.snes_socket.recv())
            if reply and 'Results' in reply:
                ctx.ui_node.log_info(reply['Results'])
        else:
            ctx.is_sd2snes = False

        ctx.snes_reconnect_address = address
        recv_task = asyncio.create_task(snes_recv_loop(ctx))
        SNES_RECONNECT_DELAY = START_RECONNECT_DELAY

    except Exception as e:

        if recv_task is not None:
            if not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
        else:
            if ctx.snes_socket is not None:
                if not ctx.snes_socket.closed:
                    await ctx.snes_socket.close()
                ctx.snes_socket = None
            ctx.snes_state = SNES_DISCONNECTED
        if not ctx.snes_reconnect_address:
            ctx.ui_node.log_error("Error connecting to snes (%s)" % e)
        else:
            ctx.ui_node.log_error(f"Error connecting to snes, attempt again in {SNES_RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))
        SNES_RECONNECT_DELAY *= 2


async def snes_disconnect(ctx: Context):
    if ctx.snes_socket:
        if not ctx.snes_socket.closed:
            await ctx.snes_socket.close()
        ctx.snes_socket = None


async def snes_autoreconnect(ctx: Context):
    # unfortunately currently broken. See: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1033
    # with prompt_toolkit.shortcuts.ProgressBar() as pb:
    #    for _ in pb(range(100)):
    #        await asyncio.sleep(RECONNECT_DELAY/100)

    await asyncio.sleep(SNES_RECONNECT_DELAY)
    if ctx.snes_reconnect_address and ctx.snes_socket is None:
        await snes_connect(ctx, ctx.snes_reconnect_address)


async def snes_recv_loop(ctx: Context):
    try:
        async for msg in ctx.snes_socket:
            ctx.snes_recv_queue.put_nowait(msg)
        ctx.ui_node.log_warning("Snes disconnected")
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
        ctx.ui_node.log_error("Lost connection to the snes, type /snes to reconnect")
    finally:
        socket, ctx.snes_socket = ctx.snes_socket, None
        if socket is not None and not socket.closed:
            await socket.close()

        ctx.snes_state = SNES_DISCONNECTED
        ctx.snes_recv_queue = asyncio.Queue()
        ctx.hud_message_queue = []
        ctx.ui_node.send_connection_status(ctx)

        ctx.rom = None

        if ctx.snes_reconnect_address:
            ctx.ui_node.log_info(f"...reconnecting in {SNES_RECONNECT_DELAY}s")
            asyncio.create_task(snes_autoreconnect(ctx))


async def snes_read(ctx : Context, address, size):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNES_ATTACHED or ctx.snes_socket is None or not ctx.snes_socket.open or ctx.snes_socket.closed:
            return None

        GetAddress_Request = {
            "Opcode" : "GetAddress",
            "Space" : "SNES",
            "Operands" : [hex(address)[2:], hex(size)[2:]]
        }
        try:
            await ctx.snes_socket.send(json.dumps(GetAddress_Request))
        except websockets.ConnectionClosed:
            return None

        data = bytes()
        while len(data) < size:
            try:
                data += await asyncio.wait_for(ctx.snes_recv_queue.get(), 5)
            except asyncio.TimeoutError:
                break

        if len(data) != size:
            logging.error('Error reading %s, requested %d bytes, received %d' % (hex(address), size, len(data)))
            if len(data):
                ctx.ui_node.log_error(str(data))
                ctx.ui_node.log_warning('Unable to connect to SNES Device because QUsb2Snes broke temporarily.'
                                        'Try un-selecting and re-selecting the SNES Device.')
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                await ctx.snes_socket.close()
            return None

        return data
    finally:
        ctx.snes_request_lock.release()


async def snes_write(ctx : Context, write_list):
    try:
        await ctx.snes_request_lock.acquire()

        if ctx.snes_state != SNES_ATTACHED or ctx.snes_socket is None or not ctx.snes_socket.open or ctx.snes_socket.closed:
            return False

        PutAddress_Request = {
            "Opcode" : "PutAddress",
            "Operands" : []
        }

        if ctx.is_sd2snes:
            cmd = b'\x00\xE2\x20\x48\xEB\x48'

            for address, data in write_list:
                if (address < WRAM_START) or ((address + len(data)) > (WRAM_START + WRAM_SIZE)):
                    ctx.ui_node.log_error("SD2SNES: Write out of range %s (%d)" % (hex(address), len(data)))
                    return False
                for ptr, byte in enumerate(data, address + 0x7E0000 - WRAM_START):
                    cmd += b'\xA9' # LDA
                    cmd += bytes([byte])
                    cmd += b'\x8F' # STA.l
                    cmd += bytes([ptr & 0xFF, (ptr >> 8) & 0xFF, (ptr >> 16) & 0xFF])

            cmd += b'\xA9\x00\x8F\x00\x2C\x00\x68\xEB\x68\x28\x6C\xEA\xFF\x08'

            PutAddress_Request['Space'] = 'CMD'
            PutAddress_Request['Operands'] = ["2C00", hex(len(cmd)-1)[2:], "2C00", "1"]
            try:
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(json.dumps(PutAddress_Request))
                if ctx.snes_socket is not None:
                    await ctx.snes_socket.send(cmd)
            except websockets.ConnectionClosed:
                return False
        else:
            PutAddress_Request['Space'] = 'SNES'
            try:
                #will pack those requests as soon as qusb2snes actually supports that for real
                for address, data in write_list:
                    PutAddress_Request['Operands'] = [hex(address)[2:], hex(len(data))[2:]]
                    if ctx.snes_socket is not None:
                        await ctx.snes_socket.send(json.dumps(PutAddress_Request))
                    if ctx.snes_socket is not None:
                        await ctx.snes_socket.send(data)
            except websockets.ConnectionClosed:
                return False

        return True
    finally:
        ctx.snes_request_lock.release()


def snes_buffered_write(ctx : Context, address, data):
    if len(ctx.snes_write_buffer) > 0 and (ctx.snes_write_buffer[-1][0] + len(ctx.snes_write_buffer[-1][1])) == address:
        ctx.snes_write_buffer[-1] = (ctx.snes_write_buffer[-1][0], ctx.snes_write_buffer[-1][1] + data)
    else:
        ctx.snes_write_buffer.append((address, data))


async def snes_flush_writes(ctx : Context):
    if not ctx.snes_write_buffer:
        return

    await snes_write(ctx, ctx.snes_write_buffer)
    ctx.snes_write_buffer = []


async def send_msgs(websocket, msgs):
    if not websocket or not websocket.open or websocket.closed:
        return
    await websocket.send(json.dumps(msgs))


async def server_loop(ctx: Context, address=None):
    global SERVER_RECONNECT_DELAY
    ctx.ui_node.send_connection_status(ctx)
    cached_address = None
    if ctx.server and ctx.server.socket:
        ctx.ui_node.log_error('Already connected')
        return

    if address is None:  # set through CLI or BMBP
        address = ctx.server_address
    if address is None:  # see if this is an old connection
        await asyncio.sleep(0.5)  # wait for snes connection to succeed if possible.
        rom = ctx.rom if ctx.rom else None
        try:
            servers = cached_address = Utils.persistent_load()["servers"]
            address = servers[rom] if rom and rom in servers else servers["default"]
        except Exception as e:
            logging.debug(f"Could not find cached server address. {e}")

    # Wait for the user to provide a multiworld server address
    if not address:
        logging.info('Please connect to a multiworld server.')
        ctx.ui_node.poll_for_server_ip()
        return

    address = f"ws://{address}" if "://" not in address else address
    port = urllib.parse.urlparse(address).port or 38281

    ctx.ui_node.log_info('Connecting to multiworld server at %s' % address)
    try:
        socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None)
        ctx.server = Endpoint(socket)
        ctx.ui_node.log_info('Connected')
        ctx.server_address = address
        ctx.ui_node.send_connection_status(ctx)
        SERVER_RECONNECT_DELAY = START_RECONNECT_DELAY
        async for data in ctx.server.socket:
            for msg in json.loads(data):
                cmd, args = (msg[0], msg[1]) if len(msg) > 1 else (msg, None)
                await process_server_cmd(ctx, cmd, args)
        ctx.ui_node.log_warning('Disconnected from multiworld server, type /connect to reconnect')
    except WebUI.WaitingForUiException:
        pass
    except ConnectionRefusedError:
        if cached_address:
            ctx.ui_node.log_error('Unable to connect to multiworld server at cached address. '
                                  'Please use the connect button above.')
        else:
            ctx.ui_node.log_error('Connection refused by the multiworld server')
    except (OSError, websockets.InvalidURI):
        ctx.ui_node.log_error('Failed to connect to the multiworld server')
    except Exception as e:
        ctx.ui_node.log_error('Lost connection to the multiworld server, type /connect to reconnect')
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
    finally:
        ctx.awaiting_rom = False
        ctx.auth = None
        ctx.items_received = []
        ctx.locations_info = {}
        ctx.server_version = (0, 0, 0)
        if ctx.server and ctx.server.socket is not None:
            await ctx.server.socket.close()
        ctx.server = None
        ctx.server_task = None
        if ctx.server_address:
            ctx.ui_node.log_info(f"... reconnecting in {SERVER_RECONNECT_DELAY}s")
            ctx.ui_node.send_connection_status(ctx)
            asyncio.create_task(server_autoreconnect(ctx))
        SERVER_RECONNECT_DELAY *= 2

async def server_autoreconnect(ctx: Context):
    # unfortunately currently broken. See: https://github.com/prompt-toolkit/python-prompt-toolkit/issues/1033
    # with prompt_toolkit.shortcuts.ProgressBar() as pb:
    #    for _ in pb(range(100)):
    #        await asyncio.sleep(RECONNECT_DELAY/100)
    await asyncio.sleep(SERVER_RECONNECT_DELAY)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx))


async def process_server_cmd(ctx: Context, cmd, args):
    if cmd == 'RoomInfo':
        ctx.ui_node.log_info('--------------------------------')
        ctx.ui_node.log_info('Room Information:')
        ctx.ui_node.log_info('--------------------------------')
        version = args.get("version", "unknown Bonta Protocol")
        if isinstance(version, list):
            ctx.server_version = tuple(version)
            version = ".".join(str(item) for item in version)
        else:
            ctx.server_version = (0, 0, 0)
        ctx.ui_node.log_info(f'Server protocol version: {version}')
        if "tags" in args:
            ctx.ui_node.log_info("Server protocol tags: " + ", ".join(args["tags"]))
        if args['password']:
            ctx.ui_node.log_info('Password required')
        if "forfeit_mode" in args: # could also be version > 2.2.1, but going with implicit content here
            logging.info("Forfeit setting: "+args["forfeit_mode"])
            logging.info("Remaining setting: "+args["remaining_mode"])
            logging.info(f"A !hint costs {args['hint_cost']} points and you get {args['location_check_points']}"
                         f" for each location checked.")
            ctx.hint_cost = int(args['hint_cost'])
            ctx.check_points = int(args['location_check_points'])
            ctx.forfeit_mode = args['forfeit_mode']
            ctx.remaining_mode = args['remaining_mode']
            ctx.ui_node.send_game_info(ctx)
        if len(args['players']) < 1:
            ctx.ui_node.log_info('No player connected')
        else:
            args['players'].sort()
            current_team = -1
            ctx.ui_node.log_info('Connected players:')
            for team, slot, name in args['players']:
                if team != current_team:
                    ctx.ui_node.log_info(f'  Team #{team + 1}')
                    current_team = team
                ctx.ui_node.log_info('    %s (Player %d)' % (name, slot))
        await server_auth(ctx, args['password'])

    elif cmd == 'ConnectionRefused':
        if 'InvalidPassword' in args:
            ctx.ui_node.log_error('Invalid password')
            ctx.password = None
            await server_auth(ctx, True)
        if 'InvalidRom' in args:
            if ctx.snes_socket is not None and not ctx.snes_socket.closed:
                asyncio.create_task(ctx.snes_socket.close())
            raise Exception(
                'Invalid ROM detected, please verify that you have loaded the correct rom and reconnect your snes (/snes)')
        if 'SlotAlreadyTaken' in args:
            Utils.persistent_store("servers", "default", ctx.server_address)
            Utils.persistent_store("servers", ctx.rom, ctx.server_address)
            raise Exception('Player slot already in use for that team')
        if 'IncompatibleVersion' in args:
            raise Exception('Server reported your client version as incompatible')
        raise Exception('Connection refused by the multiworld host')

    elif cmd == 'Connected':
        Utils.persistent_store("servers", "default", ctx.server_address)
        Utils.persistent_store("servers", ctx.rom, ctx.server_address)
        ctx.team, ctx.slot = args[0]
        ctx.player_names = {p: n for p, n in args[1]}
        msgs = []
        if ctx.locations_checked:
            msgs.append(['LocationChecks', [Regions.location_table[loc][0] for loc in ctx.locations_checked]])
        if ctx.locations_scouted:
            msgs.append(['LocationScouts', list(ctx.locations_scouted)])
        if msgs:
            await ctx.send_msgs(msgs)
        if ctx.finished_game:
            await send_finished_game(ctx)

    elif cmd == 'ReceivedItems':
        start_index, items = args
        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [['Sync']]
            if ctx.locations_checked:
                sync_msg.append(['LocationChecks', [Regions.location_table[loc][0] for loc in ctx.locations_checked]])
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            for item in items:
                ctx.items_received.append(ReceivedItem(*item))
        ctx.watcher_event.set()

    elif cmd == 'LocationInfo':
        for location, item, player in args:
            if location not in ctx.locations_info:
                replacements = {0xA2: 'Small Key', 0x9D: 'Big Key', 0x8D: 'Compass', 0x7D: 'Map'}
                item_name = replacements.get(item, get_item_name_from_id(item))
                ctx.ui_node.log_info(
                    f"Saw {color(item_name, 'red', 'bold')} at {list(Regions.location_table.keys())[location - 1]}")
                ctx.locations_info[location] = (item, player)
        ctx.watcher_event.set()

    elif cmd == 'ItemSent':
        player_sent, location, player_recvd, item = args
        ctx.ui_node.notify_item_sent(ctx.player_names[player_sent], ctx.player_names[player_recvd],
                                     get_item_name_from_id(item), get_location_name_from_address(location),
                                     player_sent == ctx.slot, player_recvd == ctx.slot)
        item = color(get_item_name_from_id(item), 'cyan' if player_sent != ctx.slot else 'green')
        player_sent = color(ctx.player_names[player_sent], 'yellow' if player_sent != ctx.slot else 'magenta')
        player_recvd = color(ctx.player_names[player_recvd], 'yellow' if player_recvd != ctx.slot else 'magenta')
        logging.info(
            '%s sent %s to %s (%s)' % (player_sent, item, player_recvd, color(get_location_name_from_address(location),
                                                                              'blue_bg', 'white')))

    elif cmd == 'ItemFound':
        found = ReceivedItem(*args)
        ctx.ui_node.notify_item_found(ctx.player_names[found.player], get_item_name_from_id(found.item),
                                      get_location_name_from_address(found.location), found.player == ctx.slot)
        item = color(get_item_name_from_id(found.item), 'cyan' if found.player != ctx.slot else 'green')
        player_sent = color(ctx.player_names[found.player], 'yellow' if found.player != ctx.slot else 'magenta')
        logging.info('%s found %s (%s)' % (player_sent, item, color(get_location_name_from_address(found.location),
                                                                    'blue_bg', 'white')))

    elif cmd == 'Missing':
        if 'locations' in args:
            locations = json.loads(args['locations'])
            for location in locations:
                ctx.ui_node.log_info(f'Missing: {location}')
            ctx.ui_node.log_info(f'Found {len(locations)} missing location checks')

    elif cmd == 'Hint':
        hints = [Utils.Hint(*hint) for hint in args]
        for hint in hints:
            ctx.ui_node.send_hint(ctx.player_names[hint.finding_player], ctx.player_names[hint.receiving_player],
                                  get_item_name_from_id(hint.item), get_location_name_from_address(hint.location),
                                  hint.found, hint.finding_player == ctx.slot, hint.receiving_player == ctx.slot,
                                  hint.entrance if hint.entrance else None)
            item = color(get_item_name_from_id(hint.item), 'green' if hint.found else 'cyan')
            player_find = color(ctx.player_names[hint.finding_player],
                                'yellow' if hint.finding_player != ctx.slot else 'magenta')
            player_recvd = color(ctx.player_names[hint.receiving_player],
                                 'yellow' if hint.receiving_player != ctx.slot else 'magenta')

            text = f"[Hint]: {player_recvd}'s {item} is " \
                   f"at {color(get_location_name_from_address(hint.location), 'blue_bg', 'white')} " \
                   f"in {player_find}'s World"
            if hint.entrance:
                text += " at " + color(hint.entrance, 'white_bg', 'black')
            logging.info(text + (f". {color('(found)', 'green_bg', 'black')} " if hint.found else "."))

    elif cmd == "AliasUpdate":
        ctx.player_names = {p: n for p, n in args}

    elif cmd == 'Print':
        ctx.ui_node.log_info(args)

    elif cmd == 'HintPointUpdate':
        ctx.hint_points = args[0]

    else:
        logging.debug(f"unknown command {args}")


def get_tags(ctx: Context):
    tags = ['AP']
    if ctx.found_items:
        tags.append('FoundItems')
    return tags


async def server_auth(ctx: Context, password_requested):
    if password_requested and not ctx.password:
        ctx.ui_node.log_info('Enter the password required to join this game:')
        ctx.password = await console_input(ctx)
    if ctx.rom is None:
        ctx.awaiting_rom = True
        ctx.ui_node.log_info(
            'No ROM detected, awaiting snes connection to authenticate to the multiworld server (/snes)')
        return
    ctx.awaiting_rom = False
    ctx.auth = ctx.rom
    auth = ctx.rom if ctx.server_version > (2, 4, 0) else list(ctx.rom.encode())
    await ctx.send_msgs([['Connect', {
        'password': ctx.password, 'rom': auth, 'version': Utils._version_tuple, 'tags': get_tags(ctx),
        'uuid': Utils.get_unique_identifier()
    }]])


async def console_input(ctx : Context):
    ctx.input_requests += 1
    return await ctx.input_queue.get()


async def connect(ctx: Context, address=None):
    await ctx.disconnect()
    ctx.server_task = asyncio.create_task(server_loop(ctx, address))


from MultiServer import CommandProcessor, mark_raw


class ClientCommandProcessor(CommandProcessor):
    def __init__(self, ctx: Context):
        self.ctx = ctx

    def output(self, text: str):
        self.ctx.ui_node.log_info(text)

    def _cmd_exit(self) -> bool:
        """Close connections and client"""
        self.ctx.exit_event.set()
        return True

    @mark_raw
    def _cmd_snes(self, snes_address: str = "") -> bool:
        """Connect to a snes. Optionally include network address of a snes to connect to, otherwise show available devices"""
        self.ctx.snes_reconnect_address = None
        asyncio.create_task(snes_connect(self.ctx, snes_address if snes_address else self.ctx.snes_address))
        return True

    def _cmd_snes_close(self) -> bool:
        """Close connection to a currently connected snes"""
        self.ctx.snes_reconnect_address = None
        if self.ctx.snes_socket is not None and not self.ctx.snes_socket.closed:
            asyncio.create_task(self.ctx.snes_socket.close())
            return True
        else:
            return False

    def _cmd_connect(self, address: str = "") -> bool:
        """Connect to a MultiWorld Server"""
        self.ctx.server_address = None
        asyncio.create_task(connect(self.ctx, address if address else None))
        return True

    def _cmd_disconnect(self) -> bool:
        """Disconnect from a MultiWorld Server"""
        self.ctx.server_address = None
        asyncio.create_task(self.ctx.disconnect())
        return True

    def _cmd_received(self) -> bool:
        """List all received items"""
        self.ctx.ui_node.log_info('Received items:')
        for index, item in enumerate(self.ctx.items_received, 1):
            self.ctx.ui_node.notify_item_received(self.ctx.player_names[item.player], get_item_name_from_id(item.item),
                                                  get_location_name_from_address(item.location), index,
                                                  len(self.ctx.items_received))
            logging.info('%s from %s (%s) (%d/%d in list)' % (
                color(get_item_name_from_id(item.item), 'red', 'bold'),
                color(self.ctx.player_names[item.player], 'yellow'),
                get_location_name_from_address(item.location), index, len(self.ctx.items_received)))
        return True

    def _cmd_missing(self) -> bool:
        """List all missing location checks, from your local game state"""
        count = 0
        for location in [k for k, v in Regions.location_table.items() if type(v[0]) is int]:
            if location not in self.ctx.locations_checked:
                self.output('Missing: ' + location)
                count += 1

        if count:
            self.output(f"Found {count} missing location checks")
        else:
            self.output("No missing location checks found.")
        return True

    def _cmd_show_items(self, toggle: str = "") -> bool:
        """Toggle showing of items received across the team"""
        if toggle:
            self.ctx.found_items = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.found_items = not self.ctx.found_items
        self.ctx.ui_node.log_info(f"Set showing team items to {self.ctx.found_items}")
        asyncio.create_task(self.ctx.send_msgs([['UpdateTags', get_tags(self.ctx)]]))
        return True

    def _cmd_slow_mode(self, toggle: str = ""):
        """Toggle slow mode, which limits how fast you send / receive items."""
        if toggle:
            self.ctx.slow_mode = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.slow_mode = not self.ctx.slow_mode

        self.ctx.ui_node.log_info(f"Setting slow mode to {self.ctx.slow_mode}")

    def _cmd_web(self):
        if self.ctx.webui_socket_port:
            webbrowser.open(f'http://localhost:5050?port={self.ctx.webui_socket_port}')
        else:
            self.output("Web UI was never started.")

    def default(self, raw: str):
        asyncio.create_task(self.ctx.send_msgs([['Say', raw]]))


async def console_loop(ctx: Context):
    session = prompt_toolkit.PromptSession()
    commandprocessor = ClientCommandProcessor(ctx)
    while not ctx.exit_event.is_set():
        try:
            with patch_stdout():
                input_text = await session.prompt_async()

            if ctx.input_requests > 0:
                ctx.input_requests -= 1
                ctx.input_queue.put_nowait(input_text)
                continue

            if not input_text:
                continue
            commandprocessor(input_text)
        except Exception as e:
            logging.exception(e)
        await snes_flush_writes(ctx)


async def track_locations(ctx : Context, roomid, roomdata):
    new_locations = []

    def new_check(location):
        ctx.locations_checked.add(location)
        ctx.ui_node.log_info("New check: %s (%d/216)" % (location, len(ctx.locations_checked)))
        ctx.ui_node.send_location_check(ctx, location)
        new_locations.append(Regions.location_table[location][0])

    for location, (loc_roomid, loc_mask) in location_table_uw.items():
        if location not in ctx.locations_checked and loc_roomid == roomid and (roomdata << 4) & loc_mask != 0:
            new_check(location)

    uw_begin = 0x129
    uw_end = 0
    uw_unchecked = {}
    for location, (roomid, mask) in location_table_uw.items():
        if location not in ctx.locations_checked:
            uw_unchecked[location] = (roomid, mask)
            uw_begin = min(uw_begin, roomid)
            uw_end = max(uw_end, roomid + 1)
    if uw_begin < uw_end:
        uw_data = await snes_read(ctx, SAVEDATA_START + (uw_begin * 2), (uw_end - uw_begin) * 2)
        if uw_data is not None:
            for location, (roomid, mask) in uw_unchecked.items():
                offset = (roomid - uw_begin) * 2
                roomdata = uw_data[offset] | (uw_data[offset + 1] << 8)
                if roomdata & mask != 0:
                    new_check(location)

    ow_begin = 0x82
    ow_end = 0
    ow_unchecked = {}
    for location, screenid in location_table_ow.items():
        if location not in ctx.locations_checked:
            ow_unchecked[location] = screenid
            ow_begin = min(ow_begin, screenid)
            ow_end = max(ow_end, screenid + 1)
    if ow_begin < ow_end:
        ow_data = await snes_read(ctx, SAVEDATA_START + 0x280 + ow_begin, ow_end - ow_begin)
        if ow_data is not None:
            for location, screenid in ow_unchecked.items():
                if ow_data[screenid - ow_begin] & 0x40 != 0:
                    new_check(location)

    if not all([location in ctx.locations_checked for location in location_table_npc.keys()]):
        npc_data = await snes_read(ctx, SAVEDATA_START + 0x410, 2)
        if npc_data is not None:
            npc_value = npc_data[0] | (npc_data[1] << 8)
            for location, mask in location_table_npc.items():
                if npc_value & mask != 0 and location not in ctx.locations_checked:
                    new_check(location)

    if not all([location in ctx.locations_checked for location in location_table_misc.keys()]):
        misc_data = await snes_read(ctx, SAVEDATA_START + 0x3c6, 4)
        if misc_data is not None:
            for location, (offset, mask) in location_table_misc.items():
                assert(0x3c6 <= offset <= 0x3c9)
                if misc_data[offset - 0x3c6] & mask != 0 and location not in ctx.locations_checked:
                    new_check(location)

    await ctx.send_msgs([['LocationChecks', new_locations]])


async def send_finished_game(ctx: Context):
    try:
        await ctx.send_msgs([['GameFinished', '']])
        ctx.finished_game = True
    except Exception as ex:
        logging.exception(ex)


async def game_watcher(ctx : Context):
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
            rom = await snes_read(ctx, ROMNAME_START, ROMNAME_SIZE)
            if rom is None or rom == bytes([0] * ROMNAME_SIZE):
                continue

            ctx.rom = rom.decode()
            if not ctx.prev_rom or ctx.prev_rom != ctx.rom:
                ctx.locations_checked = set()
                ctx.locations_scouted = set()
            ctx.prev_rom = ctx.rom

            if ctx.awaiting_rom:
                await server_auth(ctx, False)

        if ctx.auth and ctx.auth != ctx.rom:
            ctx.ui_node.log_warning("ROM change detected, please reconnect to the multiworld server")
            await ctx.disconnect()

        gamemode = await snes_read(ctx, WRAM_START + 0x10, 1)
        gameend = await snes_read(ctx, SAVEDATA_START + 0x443, 1)
        game_timer = await snes_read(ctx, SAVEDATA_START + 0x42E, 4)
        if gamemode is None or gameend is None or game_timer is None or \
                (gamemode[0] not in INGAME_MODES and gamemode[0] not in ENDGAME_MODES):
            continue

        delay = 7 if ctx.slow_mode else 2
        if gameend[0]:
            if not ctx.finished_game:
                await(send_finished_game(ctx))

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
        assert RECV_ITEM_ADDR == RECV_PROGRESS_ADDR + 2
        recv_item = data[2]
        assert ROOMID_ADDR == RECV_PROGRESS_ADDR + 4
        roomid = data[4] | (data[5] << 8)
        assert ROOMDATA_ADDR == RECV_PROGRESS_ADDR + 6
        roomdata = data[6]
        assert SCOUT_LOCATION_ADDR == RECV_PROGRESS_ADDR + 7
        scout_location = data[7]

        if recv_index < len(ctx.items_received) and recv_item == 0:
            item = ctx.items_received[recv_index]
            ctx.ui_node.notify_item_received(ctx.player_names[item.player], get_item_name_from_id(item.item),
                                             get_location_name_from_address(item.location), recv_index + 1,
                                             len(ctx.items_received))
            logging.info('Received %s from %s (%s) (%d/%d in list)' % (
                color(get_item_name_from_id(item.item), 'red', 'bold'), color(ctx.player_names[item.player], 'yellow'),
                get_location_name_from_address(item.location), recv_index + 1, len(ctx.items_received)))
            recv_index += 1
            snes_buffered_write(ctx, RECV_PROGRESS_ADDR, bytes([recv_index & 0xFF, (recv_index >> 8) & 0xFF]))
            snes_buffered_write(ctx, RECV_ITEM_ADDR, bytes([item.item]))
            snes_buffered_write(ctx, RECV_ITEM_PLAYER_ADDR, bytes([item.player if item.player != ctx.slot else 0]))
        if scout_location > 0 and scout_location in ctx.locations_info:
            snes_buffered_write(ctx, SCOUTREPLY_LOCATION_ADDR, bytes([scout_location]))
            snes_buffered_write(ctx, SCOUTREPLY_ITEM_ADDR, bytes([ctx.locations_info[scout_location][0]]))
            snes_buffered_write(ctx, SCOUTREPLY_PLAYER_ADDR, bytes([ctx.locations_info[scout_location][1]]))

        await snes_flush_writes(ctx)

        if scout_location > 0 and scout_location not in ctx.locations_scouted:
            ctx.locations_scouted.add(scout_location)
            ctx.ui_node.log_info(f'Scouting item at {list(Regions.location_table.keys())[scout_location - 1]}')
            await ctx.send_msgs([['LocationScouts', [scout_location]]])
        await track_locations(ctx, roomid, roomdata)


async def run_game(romfile):
    auto_start = Utils.get_options()["general_options"].get("rom_start", True)
    if auto_start is True:
        import webbrowser
        webbrowser.open(romfile)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, romfile],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def websocket_server(websocket: websockets.WebSocketServerProtocol, path, ctx: Context):
    endpoint = Endpoint(websocket)
    ctx.ui_node.endpoints.append(endpoint)
    process_command = ClientCommandProcessor(ctx)
    try:
        async for incoming_data in websocket:
            try:
                data = json.loads(incoming_data)
                logging.debug(f"WebUIData:{data}")
                if ('type' not in data) or ('content' not in data):
                    raise Exception('Invalid data received in websocket')

                elif data['type'] == 'webStatus':
                    if data['content'] == 'connections':
                        ctx.ui_node.send_connection_status(ctx)
                    elif data['content'] == 'devices':
                        await get_snes_devices(ctx)
                    elif data['content'] == 'gameInfo':
                        ctx.ui_node.send_game_info(ctx)
                    elif data['content'] == 'checkData':
                        ctx.ui_node.send_location_check(ctx, 'Waiting for check...')

                elif data['type'] == 'webConfig':
                    if 'serverAddress' in data['content']:
                        ctx.server_address = data['content']['serverAddress']
                        await connect(ctx, data['content']['serverAddress'])
                    elif 'deviceId' in data['content']:
                        # Allow a SNES disconnect via UI sending -1 as new device
                        if data['content']['deviceId'] == "-1":
                            ctx.ui_node.manual_snes = None
                            ctx.snes_reconnect_address = None
                            await snes_disconnect(ctx)
                        else:
                            await snes_disconnect(ctx)
                            ctx.ui_node.manual_snes = data['content']['deviceId']
                            await snes_connect(ctx, ctx.snes_address)

                elif data['type'] == 'webControl':
                    if 'disconnect' in data['content']:
                        await ctx.disconnect()

                elif data['type'] == 'webCommand':
                    process_command(data['content'])
            except json.JSONDecodeError:
                pass
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
    finally:
        await ctx.ui_node.disconnect(endpoint)


async def main():
    multiprocessing.freeze_support()
    parser = argparse.ArgumentParser()
    parser.add_argument('diff_file', default="", type=str, nargs="?",
                        help='Path to a Berserker Multiworld Binary Patch file')
    parser.add_argument('--snes', default='localhost:8080', help='Address of the QUsb2snes server.')
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('--founditems', default=False, action='store_true',
                        help='Show items found by other players for themselves.')
    parser.add_argument('--disable_web_ui', default=False, action='store_true', help="Turn off emitting a webserver for the webbrowser based user interface.")
    args = parser.parse_args()
    logging.basicConfig(format='%(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))

    if args.diff_file:
        import Patch
        logging.info("Patch file was supplied. Creating sfc rom..")
        meta, romfile = Patch.create_rom_file(args.diff_file)
        args.connect = meta["server"]
        logging.info(f"Wrote rom file to {romfile}")
        adjustedromfile, adjusted = Utils.get_adjuster_settings(romfile)
        if adjusted:
            try:
                os.replace(adjustedromfile, romfile)
                adjustedromfile = romfile
            except Exception as e:
                logging.exception(e)
        asyncio.create_task(run_game(adjustedromfile if adjusted else romfile))

    port = None
    if not args.disable_web_ui:
        # Find an available port on the host system to use for hosting the websocket server
        while True:
            port = randrange(49152, 65535)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                if not sock.connect_ex(('localhost', port)) == 0:
                    break
        import threading
        WebUI.start_server(
            port, on_start=threading.Timer(1, webbrowser.open, (f'http://localhost:5050?port={port}',)).start)

    ctx = Context(args.snes, args.connect, args.password, args.founditems, port)
    input_task = create_named_task(console_loop(ctx), name="Input")
    if not args.disable_web_ui:
        ui_socket = websockets.serve(functools.partial(websocket_server, ctx=ctx),
                                     'localhost', port, ping_timeout=None, ping_interval=None)
        await ui_socket

    if ctx.server_task is None:
        ctx.server_task = create_named_task(server_loop(ctx), name="ServerLoop")

    watcher_task = create_named_task(game_watcher(ctx), name="GameWatcher")

    await ctx.exit_event.wait()
    ctx.server_address = None
    ctx.snes_reconnect_address = None

    await watcher_task

    if ctx.server is not None and not ctx.server.socket.closed:
        await ctx.server.socket.close()
    if ctx.server_task is not None:
        await ctx.server_task

    if ctx.snes_socket is not None and not ctx.snes_socket.closed:
        await ctx.snes_socket.close()

    while ctx.input_requests > 0:
        ctx.input_queue.put_nowait(None)
        ctx.input_requests -= 1

    await input_task

if __name__ == '__main__':
    colorama.init()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
    colorama.deinit()
    atexit.unregister(exit_func)
