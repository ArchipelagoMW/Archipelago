from __future__ import annotations
import logging
import typing
import asyncio
import urllib.parse

import prompt_toolkit
import websockets
from prompt_toolkit.patch_stdout import patch_stdout

import Utils
from MultiServer import CommandProcessor

from NetUtils import Endpoint, decode, NetworkItem, encode, JSONtoTextParser, color, ClientStatus
from Utils import Version

# logging note:
# logging.* gets send to only the text console, logger.* gets send to the WebUI as well, if it's initialized.
from worlds import network_data_package
from worlds.alttp import Items, Regions

logger = logging.getLogger("Client")

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
        asyncio.create_task(self.ctx.connect(address if address else None))
        return True

    def _cmd_disconnect(self) -> bool:
        """Disconnect from a MultiWorld Server"""
        self.ctx.server_address = None
        asyncio.create_task(self.ctx.disconnect())
        return True

    def _cmd_received(self) -> bool:
        """List all received items"""
        logger.info('Received items:')
        for index, item in enumerate(self.ctx.items_received, 1):
            self.ctx.ui_node.notify_item_received(self.ctx.player_names[item.player], self.ctx.item_name_getter(item.item),
                                                  self.ctx.location_name_getter(item.location), index,
                                                  len(self.ctx.items_received),
                                                  self.ctx.item_name_getter(item.item) in Items.progression_items)
            logging.info('%s from %s (%s) (%d/%d in list)' % (
                color(self.ctx.item_name_getter(item.item), 'red', 'bold'),
                color(self.ctx.player_names[item.player], 'yellow'),
                self.ctx.location_name_getter(item.location), index, len(self.ctx.items_received)))
        return True

    def _cmd_missing(self) -> bool:
        """List all missing location checks, from your local game state"""
        count = 0
        checked_count = 0
        for location, location_id in Regions.lookup_name_to_id.items():
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



    def _cmd_ready(self):
        self.ctx.ready = not self.ctx.ready
        if self.ctx.ready:
            state = ClientStatus.CLIENT_READY
            self.output("Readied up.")
        else:
            state = ClientStatus.CLIENT_CONNECTED
            self.output("Unreadied.")
        asyncio.create_task(self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": state}]))

    def default(self, raw: str):
        asyncio.create_task(self.ctx.send_msgs([{"cmd": "Say", "text": raw}]))

class CommonContext():
    starting_reconnect_delay = 5
    current_reconnect_delay = starting_reconnect_delay
    command_processor = ClientCommandProcessor
    def __init__(self, server_address, password, found_items: bool):
        # server state
        self.server_address = server_address
        self.password = password
        self.server_task = None
        self.server: typing.Optional[Endpoint] = None
        self.server_version = Version(0, 0, 0)

        # own state
        self.finished_game = False
        self.ready = False
        self.found_items = found_items
        self.team = None
        self.slot = None
        self.auth = None
        self.ui_node = None

        self.locations_checked: typing.Set[int] = set()
        self.locations_scouted: typing.Set[int] = set()
        self.items_received = []
        self.missing_locations: typing.List[int] = []
        self.checked_locations: typing.List[int] = []
        self.locations_info = {}

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        # game state
        self.player_names: typing.Dict[int: str] = {}
        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()

        self.slow_mode = False
        self.jsontotextparser = JSONtoTextParser(self)
        self.set_getters(network_data_package)

    async def connection_closed(self):
        self.auth = None
        self.items_received = []
        self.locations_info = {}
        self.server_version = Version(0, 0, 0)
        if self.server and self.server.socket is not None:
            await self.server.socket.close()
        self.server = None
        self.server_task = None

    def set_getters(self, data_package: dict, network=False):
        if not network:  # local data; check if newer data was already downloaded
            local_package = Utils.persistent_load().get("datapackage", {}).get("latest", {})
            if local_package and local_package["version"] > network_data_package["version"]:
                data_package: dict = local_package
        elif network:  # check if data from server is newer
            for key, value in data_package.items():
                if type(value) == dict:  # convert to int keys
                    data_package[key] = \
                        {int(subkey) if subkey.isdigit() else subkey: subvalue for subkey, subvalue in value.items()}

            if data_package["version"] > network_data_package["version"]:
                Utils.persistent_store("datapackage", "latest", network_data_package)

        item_lookup: dict = data_package["lookup_any_item_id_to_name"]
        locations_lookup: dict = data_package["lookup_any_location_id_to_name"]

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
            self.ui_node.send_connection_status(self)
        if self.server_task is not None:
            await self.server_task

    async def send_msgs(self, msgs):
        if not self.server or not self.server.socket.open or self.server.socket.closed:
            return
        await self.server.socket.send(encode(msgs))

    def consume_players_package(self, package: typing.List[tuple]):
        self.player_names = {slot: name for team, slot, name, orig_name in package if self.team == team}

    def event_invalid_slot(self):
        raise Exception('Invalid Slot; please verify that you have connected to the correct world.')

    async def server_auth(self, password_requested):
        if password_requested and not self.password:
            logger.info('Enter the password required to join this game:')
            self.password = await self.console_input()
            return self.password

    async def console_input(self):
        self.input_requests += 1
        return await self.input_queue.get()

    async def connect(self, address= None):
        await self.disconnect()
        self.server_task = asyncio.create_task(server_loop(self, address))


async def server_loop(ctx: CommonContext, address=None):
    ui_node = getattr(ctx, "ui_node", None)
    if ui_node:
        ui_node.send_connection_status(ctx)
    cached_address = None
    if ctx.server and ctx.server.socket:
        logger.error('Already connected')
        return

    if address is None:  # set through CLI or APBP
        address = ctx.server_address

    # Wait for the user to provide a multiworld server address
    if not address:
        logger.info('Please connect to an Archipelago server.')
        if ui_node:
            ui_node.poll_for_server_ip()
        return

    address = f"ws://{address}" if "://" not in address else address
    port = urllib.parse.urlparse(address).port or 38281

    logger.info(f'Connecting to Archipelago server at {address}')
    try:
        socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None)
        ctx.server = Endpoint(socket)
        logger.info('Connected')
        ctx.server_address = address
        if ui_node:
            ui_node.send_connection_status(ctx)
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
            logger.error('Connection refused by the multiworld server')
    except (OSError, websockets.InvalidURI):
        logger.error('Failed to connect to the multiworld server')
    except Exception as e:
        logger.error('Lost connection to the multiworld server, type /connect to reconnect')
        if not isinstance(e, websockets.WebSocketException):
            logger.exception(e)
    finally:
        await ctx.connection_closed()
        if ctx.server_address:
            logger.info(f"... reconnecting in {ctx.current_reconnect_delay}s")
            if ui_node:
                ui_node.send_connection_status(ctx)
            asyncio.create_task(server_autoreconnect(ctx))
        ctx.current_reconnect_delay *= 2


async def server_autoreconnect(ctx: CommonContext):
    await asyncio.sleep(ctx.current_reconnect_delay)
    if ctx.server_address and ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx))


async def process_server_cmd(ctx: CommonContext, args: dict):
    try:
        cmd = args["cmd"]
    except:
        logger.exception(f"Could not get command from {args}")
        raise
    if cmd == 'RoomInfo':
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
        logger.info(f"Forfeit setting: {args['forfeit_mode']}")
        logger.info(f"Remaining setting: {args['remaining_mode']}")
        logger.info(f"A !hint costs {args['hint_cost']} points and you get {args['location_check_points']}"
                     f" for each location checked.")
        ctx.hint_cost = int(args['hint_cost'])
        ctx.check_points = int(args['location_check_points'])
        ctx.forfeit_mode = args['forfeit_mode']
        ctx.remaining_mode = args['remaining_mode']
        if ctx.ui_node:
            ctx.ui_node.send_game_info(ctx)
        if len(args['players']) < 1:
            logger.info('No player connected')
        else:
            args['players'].sort()
            current_team = -1
            logger.info('Players:')
            for team, slot, name in args['players']:
                if team != current_team:
                    logger.info(f'  Team #{team + 1}')
                    current_team = team
                logger.info('    %s (Player %d)' % (name, slot))
        if args["datapackage_version"] > network_data_package["version"]:
            await ctx.send_msgs([{"cmd": "GetDataPackage"}])
        await ctx.server_auth(args['password'])

    elif cmd == 'DataPackage':
        logger.info("Got new ID/Name Datapackage")
        ctx.set_getters(args['data'], network=True)

    elif cmd == 'ConnectionRefused':
        errors = args["errors"]
        if 'InvalidSlot' in errors:
            ctx.event_invalid_slot()

        elif 'SlotAlreadyTaken' in errors:
            raise Exception('Player slot already in use for that team')
        elif 'IncompatibleVersion' in errors:
            raise Exception('Server reported your client version as incompatible')
        # last to check, recoverable problem
        elif 'InvalidPassword' in errors:
            logger.error('Invalid password')
            ctx.password = None
            await ctx.server_auth(True)
        else:
            raise Exception("Unknown connection errors: " + str(errors))
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
        ctx.missing_locations = args["missing_locations"]
        ctx.checked_locations = args["checked_locations"]

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

    elif cmd == 'Print':
        logger.info(args["text"])

    elif cmd == 'PrintJSON':
        if not ctx.found_items and args.get("type", None) == "ItemSend" and args["receiving"] == args["sending"]:
            pass  # don't want info on other player's local pickups.
        logger.info(ctx.jsontotextparser(args["data"]))

    elif cmd == 'InvalidArguments':
        logger.warning(f"Invalid Arguments: {args['text']}")

    else:
        logger.debug(f"unknown command {cmd}")


async def console_loop(ctx: CommonContext):
    import sys
    commandprocessor = ctx.command_processor(ctx)
    while not ctx.exit_event.is_set():
        try:
            input_text = await asyncio.get_event_loop().run_in_executor(
                None, sys.stdin.readline
            )
            input_text = input_text.strip()

            if ctx.input_requests > 0:
                ctx.input_requests -= 1
                ctx.input_queue.put_nowait(input_text)
                continue

            if input_text:
                commandprocessor(input_text)
        except Exception as e:
            logging.exception(e)
