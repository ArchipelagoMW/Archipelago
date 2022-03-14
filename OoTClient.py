import asyncio
import json
import time
from asyncio import StreamReader, StreamWriter

import Utils
from CommonClient import CommonContext, server_loop, gui_enabled, console_loop,
    ClientCommandProcessor, logger, get_base_parser

class OoTCommandProcessor(ClientCommandProcessor):
    pass

class OoTContext(CommonContext): 
    pass

async def n64_sync_task(ctx: OoTContext): 
    pass

if __name__ == '__main__':

    Utils.init_logging("OoTClient")

    async def main(args):
        ctx = OoTContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")
        if gui_enabled:
            input_task = None
            from kvui import OoTManager
            ctx.ui = OoTManager(ctx)
            ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
        else:
            input_task = asyncio.create_task(console_loop(ctx), name="Input")
            ui_task = None

        ctx.n64_sync_task = asyncio.create_task(n64_sync_task(ctx), name="N64 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

        if ui_task:
            await ui_task

        if input_task:
            input_task.cancel()

    import colorama

    parser = get_base_parser()
    args, rest = parser.parse_known_args()
    colorama.init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
    colorama.deinit()
