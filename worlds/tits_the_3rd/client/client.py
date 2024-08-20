import asyncio
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

    async def server_auth(self, password_requested: bool = False):
        """Wrapper for login."""
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

async def tits_the_3rd_watcher(ctx: TitsThe3rdContext):
    """
    Client loop, watching the Trails in the Sky the 3rd game process.
    Handles game hook attachments, checking locations, giving items, calling scena methods, etc.

    Args:
        ctx (TitsThe3rdContext): The Trails in the Sky the 3rd context instance.
    """
    while not ctx.exit_event.is_set():
        if not ctx.game_interface.is_connected():
            logger.info("Waiting for connection to Trails in the Sky The Third")
            await ctx.game_interface.connect()
        await asyncio.sleep(1)

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
