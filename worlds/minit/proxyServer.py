import asyncio
# import json
# from uuid import uuid4
from aiohttp import web

from .MinitClient import ProxyGameContext
from CommonClient import logger


class Webserver:
    def __init__(self, ctx: ProxyGameContext):
        self.app = web.Application()
        self.host = "localhost"
        self.port = "11311"
        self.ctx = ctx

        self.connected = False

    async def initializer(self) -> web.Application:
        self.app.router.add_post('/Locations', self.ctx.locationHandler)
        self.app.router.add_post('/Goal', self.ctx.goalHandler)
        self.app.router.add_post('/Death', self.ctx.deathHandler)
        self.app.router.add_get('/Deathpoll', self.ctx.deathpollHandler)
        self.app.router.add_get('/Items', self.ctx.itemsHandler)
        self.app.router.add_get('/Datapackage', self.ctx.datapackageHandler)
        self.app.router.add_get('/ErConnections', self.ctx.erConnHandler)
        return self.app

    async def my_run_app(self, app, host, port):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host, port)
        await site.start()

        while True:
            await asyncio.sleep(3600)  # sleep forever

    async def run(self):
        if not self.connected:
            await self.my_run_app(
                app=await self.initializer(),
                host=self.host, port=self.port
                )
            self.connected = True
            return self.connected
        else:
            logger.info('Already connected')
            return


async def http_server_loop(wb: Webserver) -> None:
    try:
        logger.info('Trying to launch http server')
        await wb.run()
    finally:
        logger.info('http_server_loop ended')
    # TODO: handle exceptions in some way like this
    # except websockets.InvalidMessage:
    #     # probably encrypted
    #     if address.startswith("ws://"):
    #         # try wss
    #         await server_loop(ctx, "ws" + address[1:])
    #     else:
    #         ctx.handle_connection_loss(f"Lost connection to the multiworld server due to InvalidMessage"
    #                                    f"{reconnect_hint()}")
    # except ConnectionRefusedError:
    #     wb.ctx.handle_connection_loss("Connection refused by the server. "
    #                                "May not be running Archipelago on that address or port.")
    # # except websockets.InvalidURI:
    # #     wb.ctx.handle_connection_loss("Failed to connect to the multiworld server (invalid URI)")
    # except OSError:
    #     wb.ctx.handle_connection_loss("Failed to connect to the multiworld server")
    # except Exception:
    #     wb.ctx.handle_connection_loss(f"Lost connection to the multiworld server{reconnect_hint()}")
    # finally:
    #     await wb.ctx.connection_closed()
    #     if wb.ctx.server_address and wb.ctx.username and not wb.ctx.disconnected_intentionally:
    #         logger.info(f"... automatically reconnecting in {wb.ctx.current_reconnect_delay} seconds")
    #         assert wb.ctx.autoreconnect_task is None
    #         wb.ctx.autoreconnect_task = asyncio.create_task(server_autoreconnect(wb.ctx), name="server auto reconnect")
    #     wb.ctx.current_reconnect_delay *= 2


if __name__ == '__main__':
    ctx = ProxyGameContext("localhost", "")
    webserver = Webserver(ctx)
    webserver.run()
