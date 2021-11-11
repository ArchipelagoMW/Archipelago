import asyncio
import base64
import json

import websockets

import Utils
from CommonClient import init_logging, CommonContext, server_loop, gui_enabled, console_loop, ClientCommandProcessor, \
    logger


class FF1CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_send(self, location_id: int):
        """Test sending a location"""
        if not self.ctx.game:
            self.output("No game set, cannot send location.")
            return
        asyncio.create_task(self.ctx.send_msgs([
            {"cmd": "LocationChecks",
             "locations": [int(location_id)]}
        ]))


class FF1Context(CommonContext):
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.lua_socket = None

    command_processor = FF1CommandProcessor

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FF1Context, self).server_auth(password_requested)
        if not self.auth:
            logger.info('Enter slot name:')
            self.auth = await self.console_input()

        await self.send_msgs([{"cmd": 'Connect',
                               'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
                               'tags': {},
                               'uuid': Utils.get_unique_identifier(), 'game': 'Final Fantasy'
                               }])

    def on_package(self, cmd: str, args: dict):
        if cmd == 'Connected':
            self.game = self.games.get(self.slot, None)
        elif cmd == 'ReceivedItems':
            msg = base64.b64encode(json.dumps({"type": 0x00, "address": 0x6201}).encode("ascii"))
            print(self.lua_socket.send(msg))


def create_lua_handler(ctx: FF1Context):
    async def lua_handler(websocket, path: str):
        async for message in websocket:
            print("Websocket Message" + message)

    return lua_handler


if __name__ == '__main__':
    # Text Mode to use !hint and such with games that have no text entry
    init_logging("TextClient")


    async def main(args):
        ctx = FF1Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            input_task = None
            from kvui import TextManager
            ctx.ui = TextManager(ctx)
            ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
        else:
            input_task = asyncio.create_task(console_loop(ctx), name="Input")
            ui_task = None
        async with websockets.serve(create_lua_handler(ctx), "127.0.0.1", 43885, ping_interval=2) as lua_socket:
            ctx.lua_socket = lua_socket.sockets[0]
            await asyncio.gather(ctx.exit_event.wait())

        ctx.server_address = None
        if ctx.server and not ctx.server.socket.closed:
            await ctx.server.socket.close()
        if ctx.server_task:
            await ctx.server_task

        while ctx.input_requests > 0:
            ctx.input_queue.put_nowait(None)
            ctx.input_requests -= 1

        if ui_task:
            await ui_task

        if input_task:
            input_task.cancel()


    import argparse
    import colorama

    parser = argparse.ArgumentParser(description="FF1 Archipelago Client")
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if not Utils.is_frozen():  # Frozen state has no cmd window in the first place
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")

    args, rest = parser.parse_known_args()
    colorama.init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
    colorama.deinit()
