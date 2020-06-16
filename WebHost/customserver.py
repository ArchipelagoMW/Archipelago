import functools
import logging
import os
import sys

import websockets

from WebHost import LOGS_FOLDER, multidata_folder


def run_server_process(multidata: str):
    async def main():
        logging.basicConfig(format='[%(asctime)s] %(message)s',
                            level=logging.INFO,
                            filename=os.path.join(LOGS_FOLDER, multidata + ".txt"))
        ctx = Context("", 0, "", 1, 1000,
                      True, "enabled", "goal", 0)
        ctx.load(os.path.join(multidata_folder, multidata), True)
        ctx.auto_shutdown = 24 * 60 * 60  # 24 hours
        ctx.init_save()

        ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, 0, ping_timeout=None,
                                      ping_interval=None)

        await ctx.server
        for wssocket in ctx.server.ws_server.sockets:
            socketname = wssocket.getsockname()
            if wssocket.family == socket.AF_INET6:
                logging.info(f'Hosting game at [{get_public_ipv6()}]:{socketname[1]}')
            elif wssocket.family == socket.AF_INET:
                logging.info(f'Hosting game at {get_public_ipv4()}:{socketname[1]}')
        ctx.auto_shutdown = 6 * 60
        ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, []))
        while ctx.running:
            await asyncio.sleep(1)
        await ctx.shutdown_task
        logging.info("Shutting down")

    import asyncio
    if ".." not in sys.path:
        sys.path.append("..")
    from MultiServer import Context, server, auto_shutdown
    from Utils import get_public_ipv4, get_public_ipv6
    import socket
    asyncio.run(main())
