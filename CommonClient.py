from __future__ import annotations

import collections
import copy
import logging
import asyncio
import urllib.parse
import sys
import typing
import time
import functools
import warnings

import ModuleUpdate
ModuleUpdate.update()

import websockets

import Utils

if __name__ == "__main__":
    Utils.init_logging("TextClient", exception_logger="Client")

from MultiServer import CommandProcessor
from NetUtils import (Endpoint, decode, NetworkItem, encode, JSONtoTextParser, ClientStatus, Permission, NetworkSlot,
                      RawJSONtoTextParser, add_json_text, add_json_location, add_json_item, JSONTypes, HintStatus, SlotType)
from Utils import Version, stream_input, async_start
from worlds import network_data_package, AutoWorldRegister
import os
import ssl

if typing.TYPE_CHECKING:
    import kvui

logger = logging.getLogger("Client")

# without terminal, we have to use gui mode
gui_enabled = not sys.stdout or "--nogui" not in sys.argv


@Utils.cache_argsless
def get_ssl_context():
    import certifi
    return ssl.create_default_context(ssl.Purpose.SERVER_AUTH, cafile=certifi.where())


class ClientCommandProcessor(CommandProcessor):
    """
    The Command Processor will parse every method of the class that starts with "_cmd_" as a command to be called
    when parsing user input, i.e. _cmd_exit will be called when the user sends the command "/exit".

    The decorator @mark_raw can be imported from MultiServer and tells the parser to only split on the first
    space after the command i.e. "/exit one two three" will be passed in as method("one two three") with mark_raw
    and method("one", "two", "three") without.

    In addition all docstrings for command methods will be displayed to the user on launch and when using "/help"
    """
    def __init__(self, ctx: CommonContext):
        self.ctx = ctx

    def output(self, text: str):
        """Helper function to abstract logging to the CommonClient UI"""
        logger.info(text)

    def _cmd_exit(self) -> bool:
        """Close connections and client"""
        self.ctx.exit_event.set()
        return True

    def _cmd_connect(self, address: str = "") -> bool:
        """Connect to a MultiWorld Server"""
        if address:
            self.ctx.server_address = None
            self.ctx.username = None
            self.ctx.password = None
        elif not self.ctx.server_address:
            self.output("Please specify an address.")
            return False
        async_start(self.ctx.connect(address if address else None), name="connecting")
        return True

    def _cmd_disconnect(self) -> bool:
        """Disconnect from a MultiWorld Server"""
        async_start(self.ctx.disconnect(), name="disconnecting")
        return True

    def _cmd_received(self) -> bool:
        """List all received items"""
        item: NetworkItem
        self.output(f'{len(self.ctx.items_received)} received items, sorted by time:')
        for index, item in enumerate(self.ctx.items_received, 1):
            parts = []
            add_json_item(parts, item.item, self.ctx.slot, item.flags)
            add_json_text(parts, " from ")
            add_json_location(parts, item.location, item.player)
            add_json_text(parts, " by ")
            add_json_text(parts, item.player, type=JSONTypes.player_id)
            self.ctx.on_print_json({"data": parts, "cmd": "PrintJSON"})
        return True

    def _cmd_missing(self, filter_text = "") -> bool:
        """List all missing location checks, from your local game state.
        Can be given text, which will be used as filter."""
        if not self.ctx.game:
            self.output("No game set, cannot determine missing checks.")
            return False
        count = 0
        checked_count = 0
        for location, location_id in AutoWorldRegister.world_types[self.ctx.game].location_name_to_id.items():
            if filter_text and filter_text not in location:
                continue
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
        if not self.ctx.game:
            self.output("No game set, cannot determine existing items.")
            return False
        self.output(f"Item Names for {self.ctx.game}")
        for item_name in AutoWorldRegister.world_types[self.ctx.game].item_name_to_id:
            self.output(item_name)

    def _cmd_item_groups(self):
        """List all item group names for the currently running game."""
        if not self.ctx.game:
            self.output("No game set, cannot determine existing item groups.")
            return False
        self.output(f"Item Group Names for {self.ctx.game}")
        for group_name in AutoWorldRegister.world_types[self.ctx.game].item_name_groups:
            self.output(group_name)

    def _cmd_locations(self):
        """List all location names for the currently running game."""
        if not self.ctx.game:
            self.output("No game set, cannot determine existing locations.")
            return False
        self.output(f"Location Names for {self.ctx.game}")
        for location_name in AutoWorldRegister.world_types[self.ctx.game].location_name_to_id:
            self.output(location_name)

    def _cmd_location_groups(self):
        """List all location group names for the currently running game."""
        if not self.ctx.game:
            self.output("No game set, cannot determine existing location groups.")
            return False
        self.output(f"Location Group Names for {self.ctx.game}")
        for group_name in AutoWorldRegister.world_types[self.ctx.game].location_name_groups:
            self.output(group_name)

    def _cmd_ready(self):
        """Send ready status to server."""
        self.ctx.ready = not self.ctx.ready
        if self.ctx.ready:
            state = ClientStatus.CLIENT_READY
            self.output("Readied up.")
        else:
            state = ClientStatus.CLIENT_CONNECTED
            self.output("Unreadied.")
        async_start(self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": state}]), name="send StatusUpdate")

    def default(self, raw: str):
        """The default message parser to be used when parsing any messages that do not match a command"""
        raw = self.ctx.on_user_say(raw)
        if raw:
            async_start(self.ctx.send_msgs([{"cmd": "Say", "text": raw}]), name="send Say")


class CommonContext:
    # The following attributes are used to Connect and should be adjusted as needed in subclasses
    tags: typing.Set[str] = {"AP"}
    game: typing.Optional[str] = None
    items_handling: typing.Optional[int] = None
    want_slot_data: bool = True  # should slot_data be retrieved via Connect

    class NameLookupDict:
        """A specialized dict, with helper methods, for id -> name item/location data package lookups by game."""
        def __init__(self, ctx: CommonContext, lookup_type: typing.Literal["item", "location"]):
            self.ctx: CommonContext = ctx
            self.lookup_type: typing.Literal["item", "location"] = lookup_type
            self._unknown_item: typing.Callable[[int], str] = lambda key: f"Unknown {lookup_type} (ID: {key})"
            self._archipelago_lookup: typing.Dict[int, str] = {}
            self._flat_store: typing.Dict[int, str] = Utils.KeyedDefaultDict(self._unknown_item)
            self._game_store: typing.Dict[str, typing.ChainMap[int, str]] = collections.defaultdict(
                lambda: collections.ChainMap(self._archipelago_lookup, Utils.KeyedDefaultDict(self._unknown_item)))
            self.warned: bool = False

        # noinspection PyTypeChecker
        def __getitem__(self, key: str) -> typing.Mapping[int, str]:
            # TODO: In a future version (0.6.0?) this should be simplified by removing implicit id lookups support.
            if isinstance(key, int):
                if not self.warned:
                    # Use warnings instead of logger to avoid deprecation message from appearing on user side.
                    self.warned = True
                    warnings.warn(f"Implicit name lookup by id only is deprecated and only supported to maintain "
                                  f"backwards compatibility for now. If multiple games share the same id for a "
                                  f"{self.lookup_type}, name could be incorrect. Please use "
                                  f"`{self.lookup_type}_names.lookup_in_game()` or "
                                  f"`{self.lookup_type}_names.lookup_in_slot()` instead.")
                return self._flat_store[key]  # type: ignore

            return self._game_store[key]

        def __len__(self) -> int:
            return len(self._game_store)

        def __iter__(self) -> typing.Iterator[str]:
            return iter(self._game_store)

        def __repr__(self) -> str:
            return self._game_store.__repr__()

        def lookup_in_game(self, code: int, game_name: typing.Optional[str] = None) -> str:
            """Returns the name for an item/location id in the context of a specific game or own game if `game` is
            omitted.
            """
            if game_name is None:
                game_name = self.ctx.game
                assert game_name is not None, f"Attempted to lookup {self.lookup_type} with no game name available."

            return self._game_store[game_name][code]

        def lookup_in_slot(self, code: int, slot: typing.Optional[int] = None) -> str:
            """Returns the name for an item/location id in the context of a specific slot or own slot if `slot` is
            omitted.

            Use of `lookup_in_slot` should not be used when not connected to a server. If looking in own game, set
            `ctx.game` and use `lookup_in_game` method instead.
            """
            if slot is None:
                slot = self.ctx.slot
                assert slot is not None, f"Attempted to lookup {self.lookup_type} with no slot info available."

            return self.lookup_in_game(code, self.ctx.slot_info[slot].game)

        def update_game(self, game: str, name_to_id_lookup_table: typing.Dict[str, int]) -> None:
            """Overrides existing lookup tables for a particular game."""
            id_to_name_lookup_table = Utils.KeyedDefaultDict(self._unknown_item)
            id_to_name_lookup_table.update({code: name for name, code in name_to_id_lookup_table.items()})
            self._game_store[game] = collections.ChainMap(self._archipelago_lookup, id_to_name_lookup_table)
            self._flat_store.update(id_to_name_lookup_table)  # Only needed for legacy lookup method.
            if game == "Archipelago":
                # Keep track of the Archipelago data package separately so if it gets updated in a custom datapackage,
                # it updates in all chain maps automatically.
                self._archipelago_lookup.clear()
                self._archipelago_lookup.update(id_to_name_lookup_table)

    # defaults
    starting_reconnect_delay: int = 5
    current_reconnect_delay: int = starting_reconnect_delay
    command_processor: typing.Type[CommandProcessor] = ClientCommandProcessor
    ui: typing.Optional["kvui.GameManager"] = None
    ui_task: typing.Optional["asyncio.Task[None]"] = None
    input_task: typing.Optional["asyncio.Task[None]"] = None
    keep_alive_task: typing.Optional["asyncio.Task[None]"] = None
    server_task: typing.Optional["asyncio.Task[None]"] = None
    autoreconnect_task: typing.Optional["asyncio.Task[None]"] = None
    disconnected_intentionally: bool = False
    server: typing.Optional[Endpoint] = None
    server_version: Version = Version(0, 0, 0)
    generator_version: Version = Version(0, 0, 0)
    current_energy_link_value: typing.Optional[int] = None  # to display in UI, gets set by server
    max_size: int = 16*1024*1024  # 16 MB of max incoming packet size

    last_death_link: float = time.time()  # last send/received death link on AP layer

    # remaining type info
    slot_info: typing.Dict[int, NetworkSlot]
    server_address: typing.Optional[str]
    password: typing.Optional[str]
    hint_cost: typing.Optional[int]
    hint_points: typing.Optional[int]
    player_names: typing.Dict[int, str]

    finished_game: bool
    ready: bool
    team: typing.Optional[int]
    slot: typing.Optional[int]
    auth: typing.Optional[str]
    seed_name: typing.Optional[str]

    # locations
    locations_checked: typing.Set[int]  # local state
    locations_scouted: typing.Set[int]
    items_received: typing.List[NetworkItem]
    missing_locations: typing.Set[int]  # server state
    checked_locations: typing.Set[int]  # server state
    server_locations: typing.Set[int]  # all locations the server knows of, missing_location | checked_locations
    locations_info: typing.Dict[int, NetworkItem]

    # data storage
    stored_data: typing.Dict[str, typing.Any]
    stored_data_notification_keys: typing.Set[str]

    # internals
    # current message box through kvui
    _messagebox: typing.Optional["kvui.MessageBox"] = None
    # message box reporting a loss of connection
    _messagebox_connection_loss: typing.Optional["kvui.MessageBox"] = None

    def __init__(self, server_address: typing.Optional[str] = None, password: typing.Optional[str] = None) -> None:
        # server state
        self.server_address = server_address
        self.username = None
        self.password = password
        self.hint_cost = None
        self.slot_info = {}
        self.permissions = {
            "release": "disabled",
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

        self.locations_checked = set()  # local state
        self.locations_scouted = set()
        self.items_received = []
        self.missing_locations = set()  # server state
        self.checked_locations = set()  # server state
        self.server_locations = set()  # all locations the server knows of, missing_location | checked_locations
        self.locations_info = {}

        self.stored_data = {}
        self.stored_data_notification_keys = set()

        self.input_queue = asyncio.Queue()
        self.input_requests = 0

        # game state
        self.player_names = {0: "Archipelago"}
        self.exit_event = asyncio.Event()
        self.watcher_event = asyncio.Event()

        self.item_names = self.NameLookupDict(self, "item")
        self.location_names = self.NameLookupDict(self, "location")
        self.versions = {}
        self.checksums = {}

        self.jsontotextparser = JSONtoTextParser(self)
        self.rawjsontotextparser = RawJSONtoTextParser(self)
        self.update_data_package(network_data_package)

        # execution
        self.keep_alive_task = asyncio.create_task(keep_alive(self), name="Bouncy")

    @property
    def suggested_address(self) -> str:
        if self.server_address:
            return self.server_address
        return Utils.persistent_load().get("client", {}).get("last_server_address", "")

    @functools.cached_property
    def raw_text_parser(self) -> RawJSONtoTextParser:
        return RawJSONtoTextParser(self)

    @property
    def total_locations(self) -> typing.Optional[int]:
        """Will return None until connected."""
        if self.checked_locations or self.missing_locations:
            return len(self.checked_locations | self.missing_locations)

    async def connection_closed(self):
        if self.server and self.server.socket is not None:
            await self.server.socket.close()
        self.reset_server_state()

    def reset_server_state(self):
        self.auth = None
        self.slot = None
        self.team = None
        self.items_received = []
        self.locations_info = {}
        self.server_version = Version(0, 0, 0)
        self.generator_version = Version(0, 0, 0)
        self.server = None
        self.server_task = None
        self.hint_cost = None
        self.permissions = {
            "release": "disabled",
            "collect": "disabled",
            "remaining": "disabled",
        }

    async def disconnect(self, allow_autoreconnect: bool = False):
        if not allow_autoreconnect:
            self.disconnected_intentionally = True
            if self.cancel_autoreconnect():
                logger.info("Cancelled auto-reconnect.")
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task is not None:
            await self.server_task
        self.ui.update_hints()

    async def send_msgs(self, msgs: typing.List[typing.Any]) -> None:
        """ `msgs` JSON serializable """
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

    async def get_username(self):
        if not self.auth:
            self.auth = self.username
            if not self.auth:
                logger.info('Enter slot name:')
                self.auth = await self.console_input()

    async def send_connect(self, **kwargs: typing.Any) -> None:
        """
        Send a `Connect` packet to log in to the server,
        additional keyword args can override any value in the connection packet
        """
        payload = {
            'cmd': 'Connect',
            'password': self.password, 'name': self.auth, 'version': Utils.version_tuple,
            'tags': self.tags, 'items_handling': self.items_handling,
            'uuid': Utils.get_unique_identifier(), 'game': self.game, "slot_data": self.want_slot_data,
        }
        if kwargs:
            payload.update(kwargs)
        await self.send_msgs([payload])
        await self.send_msgs([{"cmd": "Get", "keys": ["_read_race_mode"]}])

    async def console_input(self) -> str:
        if self.ui:
            self.ui.focus_textinput()
        self.input_requests += 1
        return await self.input_queue.get()

    async def connect(self, address: typing.Optional[str] = None) -> None:
        """ disconnect any previous connection, and open new connection to the server """
        await self.disconnect()
        self.server_task = asyncio.create_task(server_loop(self, address), name="server loop")

    def cancel_autoreconnect(self) -> bool:
        if self.autoreconnect_task:
            self.autoreconnect_task.cancel()
            self.autoreconnect_task = None
            return True
        return False

    def slot_concerns_self(self, slot) -> bool:
        """Helper function to abstract player groups, should be used instead of checking slot == self.slot directly."""
        if slot == self.slot:
            return True
        if slot in self.slot_info:
            return self.slot in self.slot_info[slot].group_members
        return False

    def is_echoed_chat(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out messages sent by self."""
        return print_json_packet.get("type", "") == "Chat" \
            and print_json_packet.get("team", None) == self.team \
            and print_json_packet.get("slot", None) == self.slot

    def is_uninteresting_item_send(self, print_json_packet: dict) -> bool:
        """Helper function for filtering out ItemSend prints that do not concern the local player."""
        return print_json_packet.get("type", "") == "ItemSend" \
            and not self.slot_concerns_self(print_json_packet["receiving"]) \
            and not self.slot_concerns_self(print_json_packet["item"].player)

    def on_print(self, args: dict):
        logger.info(args["text"])

    def on_print_json(self, args: dict):
        if self.ui:
            # send copy to UI
            self.ui.print_json(copy.deepcopy(args["data"]))

        logging.getLogger("FileLog").info(self.rawjsontotextparser(copy.deepcopy(args["data"])),
                                          extra={"NoStream": True})
        logging.getLogger("StreamLog").info(self.jsontotextparser(copy.deepcopy(args["data"])),
                                            extra={"NoFile": True})

    def on_package(self, cmd: str, args: dict):
        """For custom package handling in subclasses."""
        pass

    def on_user_say(self, text: str) -> typing.Optional[str]:
        """Gets called before sending a Say to the server from the user.
        Returned text is sent, or sending is aborted if None is returned."""
        return text

    def on_ui_command(self, text: str) -> None:
        """Gets called by kivy when the user executes a command starting with `/` or `!`.
        The command processor is still called; this is just intended for command echoing."""
        self.ui.print_json([{"text": text, "type": "color", "color": "orange"}])

    def update_permissions(self, permissions: typing.Dict[str, int]):
        """Internal method to parse and save server permissions from RoomInfo"""
        for permission_name, permission_flag in permissions.items():
            try:
                flag = Permission(permission_flag)
                logger.info(f"{permission_name.capitalize()} permission: {flag.name}")
                self.permissions[permission_name] = flag.name
            except Exception as e:  # safeguard against permissions that may be implemented in the future
                logger.exception(e)

    async def shutdown(self):
        self.server_address = ""
        self.username = None
        self.password = None
        self.cancel_autoreconnect()
        if self.server and not self.server.socket.closed:
            await self.server.socket.close()
        if self.server_task:
            await self.server_task

        while self.input_requests > 0:
            self.input_queue.put_nowait(None)
            self.input_requests -= 1
        self.keep_alive_task.cancel()
        if self.ui_task:
            await self.ui_task
        if self.input_task:
            self.input_task.cancel()
    
    # Hints
    def update_hint(self, location: int, finding_player: int, status: typing.Optional[HintStatus]) -> None:
        msg = {"cmd": "UpdateHint", "location": location, "player": finding_player}
        if status is not None:
            msg["status"] = status
        async_start(self.send_msgs([msg]), name="update_hint")
    
    # DataPackage
    async def prepare_data_package(self, relevant_games: typing.Set[str],
                                   remote_date_package_versions: typing.Dict[str, int],
                                   remote_data_package_checksums: typing.Dict[str, str]):
        """Validate that all data is present for the current multiworld.
        Download, assimilate and cache missing data from the server."""
        # by documentation any game can use Archipelago locations/items -> always relevant
        relevant_games.add("Archipelago")

        needed_updates: typing.Set[str] = set()
        for game in relevant_games:
            if game not in remote_date_package_versions and game not in remote_data_package_checksums:
                continue

            remote_version: int = remote_date_package_versions.get(game, 0)
            remote_checksum: typing.Optional[str] = remote_data_package_checksums.get(game)

            if remote_version == 0 and not remote_checksum:  # custom data package and no checksum for this game
                needed_updates.add(game)
                continue

            cached_version: int = self.versions.get(game, 0)
            cached_checksum: typing.Optional[str] = self.checksums.get(game)
            # no action required if cached version is new enough
            if (not remote_checksum and (remote_version > cached_version or remote_version == 0)) \
                    or remote_checksum != cached_checksum:
                local_version: int = network_data_package["games"].get(game, {}).get("version", 0)
                local_checksum: typing.Optional[str] = network_data_package["games"].get(game, {}).get("checksum")
                if ((remote_checksum or remote_version <= local_version and remote_version != 0)
                        and remote_checksum == local_checksum):
                    self.update_game(network_data_package["games"][game], game)
                else:
                    cached_game = Utils.load_data_package_for_checksum(game, remote_checksum)
                    cache_version: int = cached_game.get("version", 0)
                    cache_checksum: typing.Optional[str] = cached_game.get("checksum")
                    # download remote version if cache is not new enough
                    if (not remote_checksum and (remote_version > cache_version or remote_version == 0)) \
                            or remote_checksum != cache_checksum:
                        needed_updates.add(game)
                    else:
                        self.update_game(cached_game, game)
        if needed_updates:
            await self.send_msgs([{"cmd": "GetDataPackage", "games": [game_name]} for game_name in needed_updates])

    def update_game(self, game_package: dict, game: str):
        self.item_names.update_game(game, game_package["item_name_to_id"])
        self.location_names.update_game(game, game_package["location_name_to_id"])
        self.versions[game] = game_package.get("version", 0)
        self.checksums[game] = game_package.get("checksum")

    def update_data_package(self, data_package: dict):
        for game, game_data in data_package["games"].items():
            self.update_game(game_data, game)

    def consume_network_data_package(self, data_package: dict):
        self.update_data_package(data_package)
        current_cache = Utils.persistent_load().get("datapackage", {}).get("games", {})
        current_cache.update(data_package["games"])
        Utils.persistent_store("datapackage", "games", current_cache)
        logger.info(f"Got new ID/Name DataPackage for {', '.join(data_package['games'])}")
        for game, game_data in data_package["games"].items():
            Utils.store_data_package_for_checksum(game, game_data)

    # data storage

    def set_notify(self, *keys: str) -> None:
        """Subscribe to be notified of changes to selected data storage keys.

        The values can be accessed via the "stored_data" attribute of this context, which is a dictionary mapping the
        names of the data storage keys to the latest values received from the server.
        """
        if new_keys := (set(keys) - self.stored_data_notification_keys):
            self.stored_data_notification_keys.update(new_keys)
            async_start(self.send_msgs([{"cmd": "Get",
                                         "keys": list(new_keys)},
                                        {"cmd": "SetNotify",
                                         "keys": list(new_keys)}]))

    # DeathLink hooks

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")

    async def send_death(self, death_text: str = ""):
        """Helper function to send a deathlink using death_text as the unique death cause string."""
        if self.server and self.server.socket:
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

    async def update_death_link(self, death_link: bool):
        """Helper function to set Death Link connection tag on/off and update the connection if already connected."""
        old_tags = self.tags.copy()
        if death_link:
            self.tags.add("DeathLink")
        else:
            self.tags -= {"DeathLink"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    def gui_error(self, title: str, text: typing.Union[Exception, str]) -> typing.Optional["kvui.MessageBox"]:
        """Displays an error messagebox in the loaded Kivy UI. Override if using a different UI framework"""
        if not self.ui:
            return None
        title = title or "Error"
        from kvui import MessageBox
        if self._messagebox:
            self._messagebox.dismiss()
        # make "Multiple exceptions" look nice
        text = str(text).replace('[Errno', '\n[Errno').strip()
        # split long messages into title and text
        parts = title.split('. ', 1)
        if len(parts) == 1:
            parts = title.split(', ', 1)
        if len(parts) > 1:
            text = parts[1] + '\n\n' + text
            title = parts[0]
        # display error
        self._messagebox = MessageBox(title, text, error=True)
        self._messagebox.open()
        return self._messagebox

    def handle_connection_loss(self, msg: str) -> None:
        """Helper for logging and displaying a loss of connection. Must be called from an except block."""
        exc_info = sys.exc_info()
        logger.exception(msg, exc_info=exc_info, extra={'compact_gui': True})
        self._messagebox_connection_loss = self.gui_error(msg, exc_info[1])

    def make_gui(self) -> typing.Type["kvui.GameManager"]:
        """To return the Kivy App class needed for run_gui so it can be overridden before being built"""
        from kvui import GameManager

        class TextManager(GameManager):
            base_title = "Archipelago Text Client"

        return TextManager

    def run_gui(self):
        """Import kivy UI system from make_gui() and start running it as self.ui_task."""
        ui_class = self.make_gui()
        self.ui = ui_class(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def run_cli(self):
        if sys.stdin:
            if sys.stdin.fileno() != 0:
                from multiprocessing import parent_process
                if parent_process():
                    return  # ignore MultiProcessing pipe

            # steam overlay breaks when starting console_loop
            if 'gameoverlayrenderer' in os.environ.get('LD_PRELOAD', ''):
                logger.info("Skipping terminal input, due to conflicting Steam Overlay detected. Please use GUI only.")
            else:
                self.input_task = asyncio.create_task(console_loop(self), name="Input")


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


async def server_loop(ctx: CommonContext, address: typing.Optional[str] = None) -> None:
    if ctx.server and ctx.server.socket:
        logger.error('Already connected')
        return

    if address is None:  # set through CLI or APBP
        address = ctx.server_address

    # Wait for the user to provide a multiworld server address
    if not address:
        logger.info('Please connect to an Archipelago server.')
        return

    ctx.cancel_autoreconnect()
    if ctx._messagebox_connection_loss:
        ctx._messagebox_connection_loss.dismiss()
        ctx._messagebox_connection_loss = None

    address = f"ws://{address}" if "://" not in address \
        else address.replace("archipelago://", "ws://")

    server_url = urllib.parse.urlparse(address)
    if server_url.username:
        ctx.username = server_url.username
    if server_url.password:
        ctx.password = server_url.password

    def reconnect_hint() -> str:
        return ", type /connect to reconnect" if ctx.server_address else ""

    logger.info(f'Connecting to Archipelago server at {address}')
    try:
        port = server_url.port or 38281  # raises ValueError if invalid
        socket = await websockets.connect(address, port=port, ping_timeout=None, ping_interval=None,
                                          ssl=get_ssl_context() if address.startswith("wss://") else None,
                                          max_size=ctx.max_size)
        if ctx.ui is not None:
            ctx.ui.update_address_bar(server_url.netloc)
        ctx.server = Endpoint(socket)
        logger.info('Connected')
        ctx.server_address = address
        ctx.current_reconnect_delay = ctx.starting_reconnect_delay
        ctx.disconnected_intentionally = False
        async for data in ctx.server.socket:
            for msg in decode(data):
                await process_server_cmd(ctx, msg)
        logger.warning(f"Disconnected from multiworld server{reconnect_hint()}")
    except websockets.InvalidMessage:
        # probably encrypted
        if address.startswith("ws://"):
            # try wss
            await server_loop(ctx, "ws" + address[1:])
        else:
            ctx.handle_connection_loss(f"Lost connection to the multiworld server due to InvalidMessage"
                                       f"{reconnect_hint()}")
    except ConnectionRefusedError:
        ctx.handle_connection_loss("Connection refused by the server. "
                                   "May not be running Archipelago on that address or port.")
    except websockets.InvalidURI:
        ctx.handle_connection_loss("Failed to connect to the multiworld server (invalid URI)")
    except OSError:
        ctx.handle_connection_loss("Failed to connect to the multiworld server")
    except Exception:
        ctx.handle_connection_loss(f"Lost connection to the multiworld server{reconnect_hint()}")
    finally:
        await ctx.connection_closed()
        if ctx.server_address and ctx.username and not ctx.disconnected_intentionally:
            logger.info(f"... automatically reconnecting in {ctx.current_reconnect_delay} seconds")
            assert ctx.autoreconnect_task is None
            ctx.autoreconnect_task = asyncio.create_task(server_autoreconnect(ctx), name="server auto reconnect")
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
            msg = "The server is running a different multiworld than your client is. (invalid seed_name)"
            logger.info(msg, extra={'compact_gui': True})
            ctx.gui_error('Error', msg)
        else:
            logger.info('--------------------------------')
            logger.info('Room Information:')
            logger.info('--------------------------------')
            version = args["version"]
            ctx.server_version = Version(*version)

            if "generator_version" in args:
                ctx.generator_version = Version(*args["generator_version"])
                logger.info(f'Server protocol version: {ctx.server_version.as_simple_string()}, '
                            f'generator version: {ctx.generator_version.as_simple_string()}, '
                            f'tags: {", ".join(args["tags"])}')
            else:
                logger.info(f'Server protocol version: {ctx.server_version.as_simple_string()}, '
                            f'tags: {", ".join(args["tags"])}')
            if args['password']:
                logger.info('Password required')
            ctx.update_permissions(args.get("permissions", {}))
            logger.info(
                f"A !hint costs {args['hint_cost']}% of your total location count as points"
                f" and you get {args['location_check_points']}"
                f" for each location checked. Use !hint for more information.")
            ctx.hint_cost = int(args['hint_cost'])
            ctx.check_points = int(args['location_check_points'])

            if "players" in args:  # TODO remove when servers sending this are outdated
                players = args.get("players", [])
                if len(players) < 1:
                    logger.info('No player connected')
                else:
                    players.sort()
                    current_team = -1
                    logger.info('Connected Players:')
                    for network_player in players:
                        if network_player.team != current_team:
                            logger.info(f'  Team #{network_player.team + 1}')
                            current_team = network_player.team
                        logger.info('    %s (Player %d)' % (network_player.alias, network_player.slot))

            # update data package
            data_package_versions = args.get("datapackage_versions", {})
            data_package_checksums = args.get("datapackage_checksums", {})
            await ctx.prepare_data_package(set(args["games"]), data_package_versions, data_package_checksums)

            await ctx.server_auth(args['password'])

    elif cmd == 'DataPackage':
        ctx.consume_network_data_package(args['data'])

    elif cmd == 'ConnectionRefused':
        errors = args["errors"]
        if 'InvalidSlot' in errors:
            ctx.disconnected_intentionally = True
            ctx.event_invalid_slot()
        elif 'InvalidGame' in errors:
            ctx.disconnected_intentionally = True
            ctx.event_invalid_game()
        elif 'IncompatibleVersion' in errors:
            raise Exception('Server reported your client version as incompatible. '
                            'This probably means you have to update.')
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
        ctx.username = ctx.auth
        ctx.team = args["team"]
        ctx.slot = args["slot"]
        # int keys get lost in JSON transfer
        ctx.slot_info = {0: NetworkSlot("Archipelago", "Archipelago", SlotType.player)}
        ctx.slot_info.update({int(pid): data for pid, data in args["slot_info"].items()})
        ctx.hint_points = args.get("hint_points", 0)
        ctx.consume_players_package(args["players"])
        ctx.stored_data_notification_keys.add(f"_read_hints_{ctx.team}_{ctx.slot}")
        msgs = []
        if ctx.locations_checked:
            msgs.append({"cmd": "LocationChecks",
                         "locations": list(ctx.locations_checked)})
        if ctx.locations_scouted:
            msgs.append({"cmd": "LocationScouts",
                         "locations": list(ctx.locations_scouted)})
        if ctx.stored_data_notification_keys:
            msgs.append({"cmd": "Get",
                         "keys": list(ctx.stored_data_notification_keys)})
            msgs.append({"cmd": "SetNotify",
                         "keys": list(ctx.stored_data_notification_keys)})
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
        ctx.server_locations = ctx.missing_locations | ctx. checked_locations

        server_url = urllib.parse.urlparse(ctx.server_address)
        Utils.persistent_store("client", "last_server_address", server_url.netloc)

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
        for item in [NetworkItem(*item) for item in args['locations']]:
            ctx.locations_info[item.location] = item
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

    elif cmd == "Retrieved":
        ctx.stored_data.update(args["keys"])
        if ctx.ui and f"_read_hints_{ctx.team}_{ctx.slot}" in args["keys"]:
            ctx.ui.update_hints()

    elif cmd == "SetReply":
        ctx.stored_data[args["key"]] = args["value"]
        if ctx.ui and f"_read_hints_{ctx.team}_{ctx.slot}" == args["key"]:
            ctx.ui.update_hints()
        elif args["key"].startswith("EnergyLink"):
            ctx.current_energy_link_value = args["value"]
            if ctx.ui:
                ctx.ui.set_new_energy_link_value()
    else:
        logger.debug(f"unknown command {cmd}")

    ctx.on_package(cmd, args)


async def console_loop(ctx: CommonContext):
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


def get_base_parser(description: typing.Optional[str] = None):
    """Base argument parser to be reused for components subclassing off of CommonClient"""
    import argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--connect', default=None, help='Address of the multiworld host.')
    parser.add_argument('--password', default=None, help='Password of the multiworld host.')
    if sys.stdout:  # If terminal output exists, offer gui-less mode
        parser.add_argument('--nogui', default=False, action='store_true', help="Turns off Client GUI.")
    return parser


def run_as_textclient(*args):
    class TextContext(CommonContext):
        # Text Mode to use !hint and such with games that have no text entry
        tags = CommonContext.tags | {"TextOnly"}
        game = ""  # empty matches any game since 0.3.2
        items_handling = 0b111  # receive all items for /received
        want_slot_data = False  # Can't use game specific slot_data

        async def server_auth(self, password_requested: bool = False):
            if password_requested and not self.password:
                await super(TextContext, self).server_auth(password_requested)
            await self.get_username()
            await self.send_connect()

        def on_package(self, cmd: str, args: dict):
            if cmd == "Connected":
                self.game = self.slot_info[self.slot].game

        async def disconnect(self, allow_autoreconnect: bool = False):
            self.game = ""
            await super().disconnect(allow_autoreconnect)

    async def main(args):
        ctx = TextContext(args.connect, args.password)
        ctx.auth = args.name
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="Gameless Archipelago Client, for text interfacing.")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    # handle if text client is launched using the "archipelago://name:pass@host:port" url from webhost
    if args.url:
        url = urllib.parse.urlparse(args.url)
        if url.scheme == "archipelago":
            args.connect = url.netloc
            if url.username:
                args.name = urllib.parse.unquote(url.username)
            if url.password:
                args.password = urllib.parse.unquote(url.password)
        else:
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

    # use colorama to display colored text highlighting on windows
    colorama.init()

    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)  # force log-level to work around log level resetting to WARNING
    run_as_textclient(*sys.argv[1:])  # default value for parse_args
