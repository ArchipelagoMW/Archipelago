import asyncio
import Utils
import websockets
import functools
from copy import deepcopy
from typing import List, Any, Iterable
from NetUtils import decode, encode, JSONtoTextParser, JSONMessagePart, NetworkItem, NetworkPlayer
from MultiServer import Endpoint
from CommonClient import CommonContext, gui_enabled, ClientCommandProcessor, logger, get_base_parser

DEBUG = False


class AHITJSONToTextParser(JSONtoTextParser):
    def _handle_color(self, node: JSONMessagePart):
        return self._handle_text(node)  # No colors for the in-game text


class AHITCommandProcessor(ClientCommandProcessor):
    def _cmd_ahit(self):
        """Check AHIT Connection State"""
        if isinstance(self.ctx, AHITContext):
            logger.info(f"AHIT Status: {self.ctx.get_ahit_status()}")


class AHITContext(CommonContext):
    command_processor = AHITCommandProcessor
    game = "A Hat in Time"

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.proxy = None
        self.proxy_task = None
        self.gamejsontotext = AHITJSONToTextParser(self)
        self.autoreconnect_task = None
        self.endpoint = None
        self.items_handling = 0b111
        self.room_info = None
        self.connected_msg = None
        self.game_connected = False
        self.awaiting_info = False
        self.full_inventory: List[Any] = []
        self.server_msgs: List[Any] = []

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(AHITContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def get_ahit_status(self) -> str:
        if not self.is_proxy_connected():
            return "Not connected to A Hat in Time"

        return "Connected to A Hat in Time"

    async def send_msgs_proxy(self, msgs: Iterable[dict]) -> bool:
        """ `msgs` JSON serializable """
        if not self.endpoint or not self.endpoint.socket.open or self.endpoint.socket.closed:
            return False

        if DEBUG:
            logger.info(f"Outgoing message: {msgs}")

        await self.endpoint.socket.send(msgs)
        return True

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def disconnect_proxy(self):
        if self.endpoint and not self.endpoint.socket.closed:
            await self.endpoint.socket.close()
        if self.proxy_task is not None:
            await self.proxy_task

    def is_connected(self) -> bool:
        return self.server and self.server.socket.open

    def is_proxy_connected(self) -> bool:
        return self.endpoint and self.endpoint.socket.open

    def on_print_json(self, args: dict):
        text = self.gamejsontotext(deepcopy(args["data"]))
        msg = {"cmd": "PrintJSON", "data": [{"text": text}], "type": "Chat"}
        self.server_msgs.append(encode([msg]))

        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def update_items(self):
        # just to be safe - we might still have an inventory from a different room
        if not self.is_connected():
            return

        self.server_msgs.append(encode([{"cmd": "ReceivedItems", "index": 0, "items": self.full_inventory}]))

    def on_package(self, cmd: str, args: dict):
        if cmd == "Connected":
            json = args
            # This data is not needed and causes the game to freeze for long periods of time in large asyncs.
            if "slot_info" in json.keys():
                json["slot_info"] = {}
            if "players" in json.keys():
                me: NetworkPlayer
                for n in json["players"]:
                    if n.slot == json["slot"] and n.team == json["team"]:
                        me = n
                        break

                # Only put our player info in there as we actually need it
                json["players"] = [me]
            if DEBUG:
                print(json)
            self.connected_msg = encode([json])
            if self.awaiting_info:
                self.server_msgs.append(self.room_info)
                self.update_items()
                self.awaiting_info = False

        elif cmd == "RoomUpdate":
            # Same story as above
            json = args
            if "players" in json.keys():
                json["players"] = []

            self.server_msgs.append(encode(json))

        elif cmd == "ReceivedItems":
            if args["index"] == 0:
                self.full_inventory.clear()

            for item in args["items"]:
                self.full_inventory.append(NetworkItem(*item))

            self.server_msgs.append(encode([args]))

        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]
            self.room_info = encode([args])

        else:
            if cmd != "PrintJSON":
                self.server_msgs.append(encode([args]))

    def run_gui(self):
        from kvui import GameManager

        class AHITManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago A Hat in Time Client"

        self.ui = AHITManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def proxy(websocket, path: str = "/", ctx: AHITContext = None):
    ctx.endpoint = Endpoint(websocket)
    try:
        await on_client_connected(ctx)

        if ctx.is_proxy_connected():
            async for data in websocket:
                if DEBUG:
                    logger.info(f"Incoming message: {data}")

                for msg in decode(data):
                    if msg["cmd"] == "Connect":
                        # Proxy is connecting, make sure it is valid
                        if msg["game"] != "A Hat in Time":
                            logger.info("Aborting proxy connection: game is not A Hat in Time")
                            await ctx.disconnect_proxy()
                            break

                        if ctx.seed_name:
                            seed_name = msg.get("seed_name", "")
                            if seed_name != "" and seed_name != ctx.seed_name:
                                logger.info("Aborting proxy connection: seed mismatch from save file")
                                logger.info(f"Expected: {ctx.seed_name}, got: {seed_name}")
                                text = encode([{"cmd": "PrintJSON",
                                                "data": [{"text": "Connection aborted - save file to seed mismatch"}]}])
                                await ctx.send_msgs_proxy(text)
                                await ctx.disconnect_proxy()
                                break

                        if ctx.auth:
                            name = msg.get("name", "")
                            if name != "" and name != ctx.auth:
                                logger.info("Aborting proxy connection: player name mismatch from save file")
                                logger.info(f"Expected: {ctx.auth}, got: {name}")
                                text = encode([{"cmd": "PrintJSON",
                                                "data": [{"text": "Connection aborted - player name mismatch"}]}])
                                await ctx.send_msgs_proxy(text)
                                await ctx.disconnect_proxy()
                                break

                        if ctx.connected_msg and ctx.is_connected():
                            await ctx.send_msgs_proxy(ctx.connected_msg)
                            ctx.update_items()
                        continue

                    if not ctx.is_proxy_connected():
                        break

                    await ctx.send_msgs([msg])

    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logger.exception(e)
    finally:
        await ctx.disconnect_proxy()


async def on_client_connected(ctx: AHITContext):
    if ctx.room_info and ctx.is_connected():
        await ctx.send_msgs_proxy(ctx.room_info)
    else:
        ctx.awaiting_info = True


async def proxy_loop(ctx: AHITContext):
    try:
        while not ctx.exit_event.is_set():
            if len(ctx.server_msgs) > 0:
                for msg in ctx.server_msgs:
                    await ctx.send_msgs_proxy(msg)

                ctx.server_msgs.clear()
            await asyncio.sleep(0.1)
    except Exception as e:
        logger.exception(e)
        logger.info("Aborting AHIT Proxy Client due to errors")


def launch():
    async def main():
        parser = get_base_parser()
        args = parser.parse_args()

        ctx = AHITContext(args.connect, args.password)
        logger.info("Starting A Hat in Time proxy server")
        ctx.proxy = websockets.serve(functools.partial(proxy, ctx=ctx),
                                     host="localhost", port=11311, ping_timeout=999999, ping_interval=999999)
        ctx.proxy_task = asyncio.create_task(proxy_loop(ctx), name="ProxyLoop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.proxy
        await ctx.proxy_task
        await ctx.exit_event.wait()

    Utils.init_logging("AHITClient")
    # options = Utils.get_options()

    import colorama
    colorama.just_fix_windows_console()
    asyncio.run(main())
    colorama.deinit()
