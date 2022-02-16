from __future__ import annotations
import logging
import asyncio
import urllib.parse
import sys
import typing
import time

import websockets

import Utils

if __name__ == "__main__":
    Utils.init_logging("TextClient", exception_logger="Client")

from MultiServer import CommandProcessor
from NetUtils import Endpoint, decode, NetworkItem, encode, JSONtoTextParser, ClientStatus, Permission
from Utils import Version, stream_input
from worlds import network_data_package, AutoWorldRegister

logger = logging.getLogger("Client")

# without terminal we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv


class ClientCommandProcessor(CommandProcessor):
    def __init__(self, ctx: CommonContext):
        self.ctx = ctx

    def output(self, text: str):
        logger.info(text)

    def _cmd_exit(self) -> bool:
        """Close connections and client"""
        self.ctx.exit_event.set()
        return True

    def _cmd_connect(self, address: str = "") -> bool:
        """Connect to a MultiWorld Server"""
        self.ctx.server_address = None
        asyncio.create_task(self.ctx.connect(address if address else None), name="connecting")
        return True

    def _cmd_disconnect(self) -> bool:
        """Disconnect from a MultiWorld Server"""
        self.ctx.server_address = None
        asyncio.create_task(self.ctx.disconnect(), name="disconnecting")
        return True

    def _cmd_received(self) -> bool:
        """List all received items"""
        logger.info(f'{len(self.ctx.items_received)} received items:')
        for index, item in enumerate(self.ctx.items_received, 1):
            self.output(f"{self.ctx.item_name_getter(item.item)} from {self.ctx.player_names[item.player]}")
        return True

    def _cmd_missing(self) -> bool:
        """List all missing location checks, from your local game state"""
        if not self.ctx.game:
            self.output("No game set, cannot determine missing checks.")
            return False
        count = 0
        checked_count = 0
        for location, location_id in AutoWorldRegister.world_types[self.ctx.game].location_name_to_id.items():
            if location_id < 0:
                continue
            if location_id not in self.ctx.locations_checked:
                if location_id in self.ctx.missing_locations:
                    self.output('Missing: ' + location)
                    count += 1
                elif location_id in self.ctx.checked_locations:
                    self.output('Checked: ' + location)
                    count += 1
                    checked_count += 1

        if count:
            self.output(
                f"Found {count} missing location checks{f'. {checked_count} location checks previously visited.' if checked_count else ''}")
        else:
            self.output("No missing location checks found.")
        return True

    def _cmd_items(self):
        """List all item names for the currently running game."""
        self.output(f"Item Names for {self.ctx.game}")
        for item_name in AutoWorldRegister.world_types[self.ctx.game].item_name_to_id:
            self.output(item_name)

    def _cmd_locations(self):
        """List all location names for the currently running game."""
        self.output(f"Location Names for {self.ctx.game}")
        for location_name in AutoWorldRegister.world_types[self.ctx.game].location_name_to_id:
            self.output(location_name)

    def _cmd_ready(self):
        """Send ready status to server."""
        self.ctx.ready = not self.ctx.ready
        if self.ctx.ready:
            state = ClientStatus.CLIENT_READY
            self.output("Readied up.")
        else:
            state = ClientStatus.CLIENT_CONNECTED
            self.output("Unreadied.")
        asyncio.create_task(self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": state}]), name="send StatusUpdate")

    def default(self, raw: str):
        raw = self.ctx.on_user_say(raw)
        if raw:
            asyncio.create_task(self.ctx.send_msgs([{"cmd": "Say", "text": raw}]), name="send Say")


class CommonContext():
    tags: typing.Set[str] = {"AP"}
    starting_reconnect_delay: int = 5
    current_reconnect_delay: int = starting_reconnect_delay
    command_processor: int = ClientCommandProcessor
    game = None
    ui = None
    keep_alive_task = None
    items_handling: typing.Optional[int] = None

    def __init__(self, server_address, password):
        # server state
        self.server_address = server_address
        self.password = password
        self.server_task = None
        self.server: typing.Optional[Endpoint] = None
        self.server_version = Version(0, 0, 0)
        self.hint_cost: typing.Optional[int] = None
        self.games: typing.Dict[int, str] = {}
        self.permissions = {
            "forfeit": "disabled",
            "collect": "disabled",
            "remaining": "disabled",
        }

        # own state
        self.finished_game = False
        self.ready = False
        self.team = None
        self.slot = None
        self.auth = None
        self.seed_name = None

        self.locations_checked: typing.Set[int] = set()  # local state
        self.locations_scouted: typing.Set[int] = set()
        self.items_received = []
        self.missing_locations: typing.Set[int] = set()
        self.checked_locations: typing.Set[int] = set()  # server state
        self.locations_info = {}

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        self.last_death_link: float = time.time()  # last send/received death link on AP layer

        # game state
        self.player_names: typing.Dict[int: str] = {0: "Archipelago"}
        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()

        self.slow_mode = False
        self.jsontotextparser = JSONtoTextParser(self)
        self.set_getters(network_data_package)

        # execution
        self.keep_alive_task = asyncio.create_task(keep_alive(self), name="Bouncy")

    @property
    def total_locations(self) -> typing.Optional[int]:
        """Will return None until connected."""
        if self.checked_locations or self.missing_locations:
            return len(self.checked_locations | self.missing_locations)

    async def connection_closed(self):
        self.auth = None
        self.items_received = []
        self.locations_info = {}
        self.server_version = Version(0, 0, 0)
        if self.server and self.server.socket is not None:
            await self.server.socket.close()
        self.server = None
        self.server_task = None

    # noinspection PyAttributeOutsideInit
    def set_getters(self, data_package: dict, network=False):
        if not network:  # local data; check if newer data was already downloaded
            local_package = Utils.persistent_load().get("datapackage", {}).get("latest", {})
            if local_package and local_package["version"] > network_data_package["version"]:
                data_package: dict = local_package
        elif network:  # check if data from server is newer

            if data_package["version"] > network_data_package["version"]:
                Utils.persistent_store("datapackage", "latest", network_data_package)

        item_lookup: dict = {}
        locations_lookup: dict = {}
        for game, gamedata in data_package["games"].items():
            for item_name, item_id in gamedata["item_name_to_id"].items():
                item_lookup[item_id] = item_name
            for location_name, location_id in gamedata["location_name_to_id"].items():
                locations_lookup[location_id] = location_name

        def get_item_name_from_id(code: int):
            return item_lookup.get(code, f'Unknown item (ID:{code})')

        self.item_name_getter = get_item_name_from_id

        def get_location_name_from_address(address: int):
            return locations_lookup.get(address, f'Unknown location (ID:{address})')

        self.location_name_getter = get_location_name_from_address

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def disconnect(self):
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task is not None:
            await self.server_task

    async def send_msgs(self, msgs):
        if not self.server or not self.server.socket.open or self.server.socket.closed:
            return
        await self.server.socket.send(encode(msgs))

    def consume_players_package(self, package: typing.List[tuple]):
        self.player_names = {slot: name for team, slot, name, orig_name in package if self.team == team}
        self.player_names[0] = "Archipelago"

    def event_invalid_slot(self):
        raise Exception('Invalid Slot; please verify that you have connected to the correct world.')

    def event_invalid_game(self):
        raise Exception('Invalid Game; please verify that you connected with the right game to the correct world.')

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()
            return self.password

    async def send_connect(self, **kwargs):
        payload = {
            'cmd': 'Connect',
            'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
            'tags': self.tags, 'items_handling': self.items_handling,
            'uuid': Utils.get_unique_identifier(), 'game': self.game
        }
        if kwargs:
            payload.update(kwargs)
        await self.send_msgs([payload])

    async def console_input(self):
        self.input_requests += 1
        return await self.input_queue.get()

    async def connect(self, address=None):
        await self.disconnect()
        self.server_task = asyncio.create_task(server_loop(self, address), name="server loop")

    def on_print(self, args: dict):
        logger.info(args["text"])

    def on_print_json(self, args: dict):
        if self.ui:
            self.ui.print_json(args["data"])
        else:
            text = self.jsontotextparser(args["data"])
            logger.info(text)

    def on_package(self, cmd: str, args: dict):
        """For custom package handling in subclasses."""
        pass

    def on_user_say(self, text: str) -> typing.Optional[str]:
        """Gets called before sending a Say to the server from the user.
        Returned text is sent, or sending is aborted if None is returned."""
        return text

    def update_permissions(self, permissions: typing.Dict[str, int]):
        for permission_name, permission_flag in permissions.items():
            try:
                flag = Permission(permission_flag)
                logger.info(f"{permission_name.capitalize()} permission: {flag.name}")
                self.permissions[permission_name] = flag.name
            except Exception as e:  # safeguard against permissions that may be implemented in the future
                logger.exception(e)

    async def shutdown(self):
        self.server_address = None
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task:
            await self.server_task

        while self.input_requests > 0:
            self.input_queue.put_nowait(None)
            self.input_requests -= 1
        self.keep_alive_task.cancel()

    # DeathLink hooks

    def on_deathlink(self, data: dict):
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")

    async def send_death(self, death_text: str = ""):
        logger.info("DeathLink: Sending death to your friends...")
        self.last_death_link = time.time()
        await self.send_msgs([{
            "cmd": "Bounce", "tags": ["DeathLink"],
            "data": {
                "time": self.last_death_link,
                "source": self.player_names[self.slot],
                "cause": death_text
            }
        }])

    async def update_death_link(self, death_link):
        old_tags = self.tags.copy()
        if death_link:
            self.tags.add("DeathLink")
        else:
            self.tags -= {"DeathLink"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])


async def keep_alive(ctx: CommonContext, seconds_between_checks=100):
    """some ISPs/network configurations drop TCP connections if no payload is sent (ignore TCP-keep-alive)
     so we send a payload to prevent drop and if we were dropped anyway this will cause an auto-reconnect."""
    seconds_elapsed = 0
    while not ctx.exit_event.is_set():
        await asyncio.sleep(1)  # short sleep to not block program shutdown
        if ctx.server and ctx.slot:
            seconds_elapsed += 1
            if seconds_elapsed > seconds_between_checks:
                await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot]}])
                seconds_elapsed = 0


async def server_loop(ctx: CommonContext, address=None):
    cached_address = None
    if ctx.server and ctx.server.socket:
        logger.error('Already connected')
        return

    if address is None:  # set through CLI or APBP
        address = ctx.server_address

    # Wait for the user to provide a multiworld server address
    if not address:
        logger.info('Please connect to an Archipelago server.')
        return

    address = f"ws://{address}" if "://" not in address else address
    port = urllib.parse.urlparse(address).port or 38281

    logger.info(f'Connecting to Archipelago server at {address}')
    try:
        socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None)
        ctx.server = Endpoint(socket)
        logger.info('Connected')
        ctx.server_address = address
        ctx.current_reconnect_delay = ctx.starting_reconnect_delay
        async for data in ctx.server.socket:
            for msg in decode(data):
                await process_server_cmd(ctx, msg)
        logger.warning('Disconnected from multiworld server, type /connect to reconnect')
    except ConnectionRefusedError:
        if cached_address:
            logger.error('Unable to connect to multiworld server at cached address. '
                         'Please use the connect button above.')
        else:
            logger.exception('Connection refused by the multiworld server')
    except websockets.InvalidURI:
        logger.exception('Failed to connect to the multiworld server (invalid URI)')
    except (OSError, websockets.InvalidURI):
        logger.exception('Failed to connect to the multiworld server')
    except Exception as e:
        logger.exception('Lost connection to the multiworld server, type /connect to reconnect')
    finally:
        await ctx.connection_closed()
        if ctx.server_address:
            logger.info(f"... reconnecting in {ctx.current_reconnect_delay}s")
            asyncio.create_task(server_autoreconnect(ctx), name="server auto reconnect")
        ctx.current_reconnect_delay *= 2


async def server_autoreconnect(ctx: CommonContext):
    await asyncio.sleep(ctx.current_reconnect_delay)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")


async def process_server_cmd(ctx: CommonContext, args: dict):
    try:
        cmd = args["cmd"]
    except:
        logger.exception(f"Could not get command from {args}")
        raise
    if cmd == 'RoomInfo':
        if ctx.seed_name and ctx.seed_name != args["seed_name"]:
            logger.info("The server is running a different multiworld than your client is. (invalid seed_name)")
        else:
            logger.info('--------------------------------')
            logger.info('Room Information:')
            logger.info('--------------------------------')
            version = args["version"]
            ctx.server_version = tuple(version)
            version = ".".join(str(item) for item in version)

            logger.info(f'Server protocol version: {version}')
            logger.info("Server protocol tags: " + ", ".join(args["tags"]))
            if args['password']:
                logger.info('Password required')
            ctx.update_permissions(args.get("permissions", {}))
            if "games" in args:
                ctx.games = {x: game for x, game in enumerate(args["games"], start=1)}
            logger.info(
                f"A !hint costs {args['hint_cost']}% of your total location count as points"
                f" and you get {args['location_check_points']}"
                f" for each location checked. Use !hint for more information.")
            ctx.hint_cost = int(args['hint_cost'])
            ctx.check_points = int(args['location_check_points'])

            if len(args['players']) < 1:
                logger.info('No player connected')
            else:
                args['players'].sort()
                current_team = -1
                logger.info('Players:')
                for network_player in args['players']:
                    if network_player.team != current_team:
                        logger.info(f'  Team #{network_player.team + 1}')
                        current_team = network_player.team
                    logger.info('    %s (Player %d)' % (network_player.alias, network_player.slot))
            if args["datapackage_version"] > network_data_package["version"] or args["datapackage_version"] == 0:
                await ctx.send_msgs([{"cmd": "GetDataPackage"}])
            await ctx.server_auth(args['password'])

    elif cmd == 'DataPackage':
        logger.info("Got new ID/Name Datapackage")
        ctx.set_getters(args['data'], network=True)

    elif cmd == 'ConnectionRefused':
        errors = args["errors"]
        if 'InvalidSlot' in errors:
            ctx.event_invalid_slot()
        elif 'InvalidGame' in errors:
            ctx.event_invalid_game()
        elif 'SlotAlreadyTaken' in errors:
            raise Exception('Player slot already in use for that team')
        elif 'IncompatibleVersion' in errors:
            raise Exception('Server reported your client version as incompatible')
        elif 'InvalidItemsHandling' in errors:
            raise Exception('The item handling flags requested by the client are not supported')
        # last to check, recoverable problem
        elif 'InvalidPassword' in errors:
            logger.error('Invalid password')
            ctx.password = None
            await ctx.server_auth(True)
        elif errors:
            raise Exception("Unknown connection errors: " + str(errors))
        else:
            raise Exception('Connection refused by the multiworld host, no reason provided')

    elif cmd == 'Connected':
        ctx.team = args["team"]
        ctx.slot = args["slot"]
        ctx.consume_players_package(args["players"])
        msgs = []
        if ctx.locations_checked:
            msgs.append({"cmd": "LocationChecks",
                         "locations": list(ctx.locations_checked)})
        if ctx.locations_scouted:
            msgs.append({"cmd": "LocationScouts",
                         "locations": list(ctx.locations_scouted)})
        if msgs:
            await ctx.send_msgs(msgs)
        if ctx.finished_game:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        # Get the server side view of missing as of time of connecting.
        # This list is used to only send to the server what is reported as ACTUALLY Missing.
        # This also serves to allow an easy visual of what locations were already checked previously
        # when /missing is used for the client side view of what is missing.
        ctx.missing_locations = set(args["missing_locations"])
        ctx.checked_locations = set(args["checked_locations"])

    elif cmd == 'ReceivedItems':
        start_index = args["index"]

        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                 "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        if start_index == len(ctx.items_received):
            for item in args['items']:
                ctx.items_received.append(NetworkItem(*item))
        ctx.watcher_event.set()

    elif cmd == 'LocationInfo':
        for item, location, player in args['locations']:
            if location not in ctx.locations_info:
                ctx.locations_info[location] = (item, player)
        ctx.watcher_event.set()

    elif cmd == "RoomUpdate":
        if "players" in args:
            ctx.consume_players_package(args["players"])
        if "hint_points" in args:
            ctx.hint_points = args['hint_points']
        if "checked_locations" in args:
            checked = set(args["checked_locations"])
            ctx.checked_locations |= checked
            ctx.missing_locations -= checked
        if "permissions" in args:
            ctx.update_permissions(args["permissions"])

    elif cmd == 'Print':
        ctx.on_print(args)

    elif cmd == 'PrintJSON':
        ctx.on_print_json(args)

    elif cmd == 'InvalidPacket':
        logger.warning(f"Invalid Packet of {args['type']}: {args['text']}")

    elif cmd == "Bounced":
        tags = args.get("tags", [])
        # we can skip checking "DeathLink" in ctx.tags, as otherwise we wouldn't have been send this
        if "DeathLink" in tags and ctx.last_death_link != args["data"]["time"]:
            ctx.on_deathlink(args["data"])

    else:
        logger.debug(f"unknown command {cmd}")

    ctx.on_package(cmd, args)


async def console_loop(ctx: CommonContext):
    import sys
    commandprocessor = ctx.command_processor(ctx)
    queue = asyncio.Queue()
    stream_input(sys.stdin, queue)
    while not ctx.exit_event.is_set():
        try:
            input_text = await queue.get()
            queue.task_done()

            if ctx.input_requests > 0:
                ctx.input_requests -= 1
                ctx.input_queue.put_nowait(input_text)
                continue

            if input_text:
                commandprocessor(input_text)
        except Exception as e:
            logger.exception(e)


def get_base_parser(description=None):
    import argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if sys.stdout:  # If terminal output exists, offer gui-less mode
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")
    return parser


if __name__ == '__main__':
    # Text Mode to use !hint and such with games that have no text entry

    class TextContext(CommonContext):
        tags = {"AP", "IgnoreGame", "TextOnly"}
        game = "Archipelago"
        items_handling = 0  # don't receive any NetworkItems

        async def server_auth(self, password_requested: bool = False):
            if password_requested and not self.password:
                await super(TextContext, self).server_auth(password_requested)
            if not self.auth:
                logger.info('Enter slot name:')
                self.auth = await self.console_input()

            await self.send_connect()

        def on_package(self, cmd: str, args: dict):
            if cmd == "Connected":
                self.game = self.games.get(self.slot, None)


    async def main(args):
        ctx = TextContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        input_task = None
        if gui_enabled:
            from kvui import TextManager
            ctx.ui = TextManager(ctx)
            ui_task = asyncio.create_task(ctx.ui.async_run(), name="UI")
        else:
            ui_task = None
        if sys.stdin:
            input_task = asyncio.create_task(console_loop(ctx), name="Input")
        await ctx.exit_event.wait()

        await ctx.shutdown()
        if ui_task:
            await ui_task

        if input_task:
            input_task.cancel()

    import colorama

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(args))
    loop.close()
    colorama.deinit()
