from __future__ import annotations
import logging
import asyncio
import urllib.parse
import sys
import typing
import time
import functools

import ModuleUpdate
ModuleUpdate.update()

import websockets

import Utils


from MultiServer import CommandProcessor
from NetUtils import Endpoint, decode, NetworkItem, encode, JSONtoTextParser, \
    ClientStatus, Permission, NetworkSlot, RawJSONtoTextParser
from Utils import Version, stream_input, async_start
from worlds import network_data_package, AutoWorldRegister
from CommonClient import CommonContext
from DolphinClient import dolphin_logger
from worlds.AutoDolphinClient import DolphinClient
import os

dolphin_logger = logging.getLogger("Dolphin")

ROM_START = 
WRAM_START = 
WRAM_SIZE = 
SRAM_START = 

Galaxy_ROMNAME_START = 
Galaxy_ROMHASH_START = 
ROMNAME_SIZE = 
ROMHASH_SIZE = 

Galaxy_FILE_NAME_ADDR = WRAM_START + 

class GalaxyDolphinClient(DolphinClient):
    game = "Super Mario Galaxy"

    async def validate_rom(self, ctx: DolphinContext) -> bool:

        rom_name = await dol_read(ctx, Galaxy_ROMHASH_START, ROMHASH_SIZE)
        return await super().validate_rom(ctx)
