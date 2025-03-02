import asyncio
import hashlib
import time
from typing import Optional

import colorama

from .memory_io import TitsThe3rdMemoryIO
from CommonClient import (
    CommonContext,
    get_base_parser,
    gui_enabled,
    logger,
    server_loop,
)

class TitsThe3rdContext(CommonContext):
    """Trails in the Sky the 3rd Context"""
    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)
        self.game = "Trails in the Sky the 3rd"
        self.items_handling = 0b011  # items from both your own and other worlds are sent through AP.
        self.game_interface = TitsThe3rdMemoryIO(self.exit_event)
        self.world_player_identifier: bytes = b"\x00\x00\x00\x00"

    def reset_client_state(self):
        """
        Resets the client state to the initial state.
        """
        self.world_player_identifier = b"\x00\x00\x00\x00"

    async def server_auth(self, password_requested: bool = False):
        """Wrapper for login."""
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            # if we dont have the seed name from the RoomInfo packet, wait until we do.
            while not self.seed_name:
                time.sleep(1)
            # Hash the seed name + player name and take the first 4 bytes as the world player identifier.
            self.world_player_identifier = f"{self.seed_name}-{self.auth}"
            self.world_player_identifier = (hashlib.sha256(self.world_player_identifier.encode()).digest())[:4]
        if cmd == "RoomInfo":
            self.seed_name = args["seed_name"]

    def client_recieved_initial_server_data(self):
        """
        This returns true if the client has finished the initial conversation with the server.
        This means:
            - Authenticated with the server (self.auth is set)
            - RoomInfo package recieved (self.seed_name is set)
            - World player identifier is calculated based on the seed and player name (self.world_player_identifier is set)
        """
        return (
            self.auth and
            self.seed_name and
            self.world_player_identifier
        )

    async def wait_for_ap_connection(self):
        """
        This method waits until the client finishes the initial connection with the server.
        See client_recieved_initial_server_data for wait requirements
        """
        if self.client_recieved_initial_server_data():
            return
        logger.info("Waiting for connect from server...")
        while not self.client_recieved_initial_server_data() and not self.exit_event.is_set():
            await asyncio.sleep(1)
        if not self.exit_event.is_set():
            # wait an extra second to process data
            await asyncio.sleep(1)
            logger.info("Received initial data from server!")

async def tits_the_3rd_watcher(ctx: TitsThe3rdContext):
    """
    Client loop, watching the Trails in the Sky the 3rd game process.
    Handles game hook attachments, checking locations, giving items, calling scena methods, etc.

    Args:
        ctx (TitsThe3rdContext): The Trails in the Sky the 3rd context instance.
    """
    await ctx.wait_for_ap_connection()
    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)

        if not ctx.server:
            # client disconnected from server
            ctx.reset_client_state()
            await ctx.wait_for_ap_connection()
            continue

        if not ctx.game_interface.is_connected():
            logger.info("Waiting for connection to Trails in the Sky The Third")
            await ctx.game_interface.connect()
            continue

        if ctx.game_interface.should_write_world_player_identifier():
            ctx.game_interface.write_world_player_identifier(ctx.world_player_identifier)
            continue

def launch():
    """
    Launch a client instance (wrapper / args parser)
    """
    async def main(args):
        """
        Launch a client instance (threaded)
        """
        ctx = TitsThe3rdContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="TitsThe3rdServerLoop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        watcher = asyncio.create_task(
            tits_the_3rd_watcher(ctx),
            name="TitsThe3rdProgressionWatcher"
        )
        await ctx.exit_event.wait()
        await watcher
        await ctx.shutdown()

    parser = get_base_parser(description="Trails in the Sky the 3rd Client")
    args, _ = parser.parse_known_args()

    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
