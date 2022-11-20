from __future__ import annotations

import asyncio
import copy
import ctypes
import logging
import multiprocessing
import os.path
import re
import sys
import typing
import queue
from pathlib import Path

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
from MultiServer import mark_raw
from Utils import init_logging, is_windows

if __name__ == "__main__":
    init_logging("DarkSoulsClient", exception_logger="Client")

logger = logging.getLogger("Client")
darksouls_logger = logging.getLogger("DarkSouls3")

import nest_asyncio
import colorama
from NetUtils import RawJSONtoTextParser
from worlds import network_data_package

nest_asyncio.apply()
max_bonus: int = 8
victory_modulo: int = 100


class DarkSouls3ClientProcessor(ClientCommandProcessor):
    ctx: DS3Context

    @mark_raw
    def _cmd_id(self, name: str = "") -> bool:
        """Gets the id of a specific location on the current client version"""
        ds3_game = network_data_package["games"]["Dark Souls III"]
        ds3_location_ids = ds3_game["location_name_to_id"]
        ds3_item_ids = ds3_game["item_name_to_id"]

        if name in ds3_location_ids:
            id = ds3_location_ids[name]
            self.output(name + " is a location with ID [" + str(id) + "] on the current version")
            return True

        if name in ds3_item_ids:
            id = ds3_item_ids[name]
            self.output(name + " is an item with ID [" + str(id) + "] on the current version")
            return True

        self.output("Could not find a location or item by the name of '" + name + "'")
        return False


class DS3Context(CommonContext):
    command_processor = DarkSouls3ClientProcessor
    game = "Dark Souls III"

    def __init__(self, *args, **kwargs):
        super(DS3Context, self).__init__(*args, **kwargs)
        self.raw_text_parser = RawJSONtoTextParser(self)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(DS3Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def run_gui(self):
        super(DS3Context, self).run_gui()
        self.ui.base_title = "Archipelago Dark Souls III Client"


async def main():
    multiprocessing.freeze_support()
    parser = get_base_parser()
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    args = parser.parse_args()

    ctx = DS3Context(args.connect, args.password)
    ctx.auth = args.name
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()

    await ctx.shutdown()


if __name__ == '__main__':
    colorama.init()
    asyncio.run(main())
    colorama.deinit()
