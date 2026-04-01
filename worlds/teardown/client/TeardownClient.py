import asyncio
import sys
from argparse import Namespace
from enum import Enum
from typing import TYPE_CHECKING, Any

from CommonClient import CommonContext, gui_enabled, logger, server_loop
from NetUtils import ClientStatus
import Utils



class TeardownContext(CommonContext):
    game = "Teardown"
    items_handling = 0b111

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "ReceivedItems":
            for item in args['items']:
                # This just prints the item ID to your console so you know it's working
                print(f"Received Item ID: {item.item} from Slot: {item.player}")


async def launch():
    ctx = TeardownContext(None, None)

    # This launches the standard Archipelago text interface
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await server_loop(ctx)


if __name__ == "__launch__":
    Utils.init_logging("TeardownClient")
    asyncio.run(launch())