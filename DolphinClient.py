from __future__ import annotations

import sys
import threading
import time
import multiprocessing
import os
import subprocess
import base64
import logging
import asyncio
import enum
import typing

from json import loads, dumps

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser

import Utils
from Utils import async_start
from MultiServer import mark_raw
if typing.TYPE_CHECKING:
    from worlds.AutoSNIClient import SNIClient

if __name__ == "__main__":
    Utils.init_logging("DolphinClient", exception_logger="Client")

import colorama
from websockets.client import connect as websockets_connect, WebSocketClientProtocol
from websockets.exceptions import WebSocketException, ConnectionClosed

dolphin_logger = logging.getLogger("Dolphin")

class DolphinClientCommandProcessor(ClientCommandProcessor):
    ctx: DolphinContext

    def _cmd_slow_mode(self, toggle: str = "") -> None:
        """Toggle slow mode, which limits how fast you send / receive items."""
        if toggle:
            self.ctx.slow_mode = toggle.lower() in {"1", "true", "on"}
        else:
            self.ctx.slow_mode = not self.ctx.slow_mode

        self.output(f"Setting slow mode to {self.ctx.slow_mode}")

class DolphinContext(CommonContext):
    command_processor: typing.Type[SNIClientCommandProcessor] = SNIClientCommandProcessor
    game: typing.Optional[str] = None  # set in validate_rom
    items_handling: typing.Optional[int] = None  # set in game_watcher
    snes_reconnect_address: typing.Optional[str]
    slow_mode: bool

    awaiting_rom: bool