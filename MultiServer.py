from __future__ import annotations

import argparse
import asyncio
import copy
import collections
import datetime
import functools
import hashlib
import inspect
import itertools
import logging
import operator
import pickle
import random
import threading
import time
import typing
import weakref
import zlib

import ModuleUpdate

ModuleUpdate.update()

if typing.TYPE_CHECKING:
    import ssl

import websockets
import colorama
try:
    # ponyorm is a requirement for webhost, not default server, so may not be importable
    from pony.orm.dbapiprovider import OperationalError
except ImportError:
    OperationalError = ConnectionError

import NetUtils
import Utils
from Utils import version_tuple, restricted_loads, Version, async_start
from NetUtils import Endpoint, ClientStatus, NetworkItem, decode, encode, NetworkPlayer, Permission, NetworkSlot, \
    SlotType, LocationStore

min_client_version = Version(0, 1, 6)
colorama.init()


def remove_from_list(container, value):
    try:
        container.remove(value)
    except ValueError:
        pass
    return container


def pop_from_container(container, value):
    try:
        container.pop(value)
    except ValueError:
        pass
    return container


def update_dict(dictionary, entries):
    dictionary.update(entries)
    return dictionary


# functions callable on storable data on the server by clients
modify_functions = {
    "add": operator.add,  # add together two objects, using python's "+" operator (works on strings and lists as append)
    "mul": operator.mul,
    "mod": operator.mod,
    "max": max,
    "min": min,
    "replace": lambda old, new: new,
    "default": lambda old, new: old,
    "pow": operator.pow,
    # bitwise:
    "xor": operator.xor,
    "or": operator.or_,
    "and": operator.and_,
    "left_shift": operator.lshift,
    "right_shift": operator.rshift,
    # lists/dicts
    "remove": remove_from_list,
    "pop": pop_from_container,
    "update": update_dict,
}


def get_saving_second(seed_name: str, interval: int = 60) -> int:
    # save at expected times so other systems using savegame can expect it
    # represents the target second of the auto_save_interval at which to save
    return int(hashlib.sha256(seed_name.encode()).hexdigest(), 16) % interval


class Client(Endpoint):
    version = Version(0, 0, 0)
    tags: typing.List[str] = []
    remote_items: bool
    remote_start_inventory: bool
    no_items: bool
    no_locations: bool

    def __init__(self, socket: websockets.WebSocketServerProtocol, ctx: Context):
        super().__init__(socket)
        self.auth = False
        self.team = None
        self.slot = None
        self.send_index = 0
        self.tags = []
        self.messageprocessor = client_message_processor(ctx, self)
        self.ctx = weakref.ref(ctx)

    @property
    def items_handling(self):
        if self.no_items:
            return 0
        return 1 + (self.remote_items << 1) + (self.remote_start_inventory << 2)

    @items_handling.setter
    def items_handling(self, value: int):
        if not (value & 0b001) and (value & 0b110):
            raise ValueError("Invalid flag combination")
        self.no_items = not (value & 0b001)
        self.remote_items = bool(value & 0b010)
        self.remote_start_inventory = bool(value & 0b100)

    @property
    def name(self) -> str:
        ctx = self.ctx()
        if ctx:
            return ctx.player_names[self.team, self.slot]
        return "Deallocated"


team_slot = typing.Tuple[int, int]


class Context:
    dumper = staticmethod(encode)
    loader = staticmethod(decode)

    simple_options = {"hint_cost": int,
                      "location_check_points": int,
                      "server_password": str,
                      "password": str,
                      "release_mode": str,
                      "remaining_mode": str,
                      "collect_mode": str,
                      "item_cheat": bool,
                      "compatibility": int}
    # team -> slot id -> list of clients authenticated to slot.
    clients: typing.Dict[int, typing.Dict[int, typing.List[Client]]]
    locations: LocationStore  # typing.Dict[int, typing.Dict[int, typing.Tuple[int, int, int]]]
    location_checks: typing.Dict[typing.Tuple[int, int], typing.Set[int]]
    hints_used: typing.Dict[typing.Tuple[int, int], int]
    groups: typing.Dict[int, typing.Set[int]]
    save_version = 2
    stored_data: typing.Dict[str, object]
    read_data: typing.Dict[str, object]
    stored_data_notification_clients: typing.Dict[str, typing.Set[Client]]
    slot_info: typing.Dict[int, NetworkSlot]
    generator_version = Version(0, 0, 0)
    checksums: typing.Dict[str, str]
    item_names: typing.Dict[int, str] = Utils.KeyedDefaultDict(lambda code: f'Unknown item (ID:{code})')
    item_name_groups: typing.Dict[str, typing.Dict[str, typing.Set[str]]]
    location_names: typing.Dict[int, str] = Utils.KeyedDefaultDict(lambda code: f'Unknown location (ID:{code})')
    location_name_groups: typing.Dict[str, typing.Dict[str, typing.Set[str]]]
    all_item_and_group_names: typing.Dict[str, typing.Set[str]]
    all_location_and_group_names: typing.Dict[str, typing.Set[str]]
    non_hintable_names: typing.Dict[str, typing.Set[str]]

    def __init__(self, host: str, port: int, server_password: str, password: str, location_check_points: int,
                 hint_cost: int, item_cheat: bool, release_mode: str = "disabled", collect_mode="disabled",
                 remaining_mode: str = "disabled", auto_shutdown: typing.SupportsFloat = 0, compatibility: int = 2,
                 log_network: bool = False):
        super(Context, self).__init__()
        self.slot_info = {}
        self.log_network = log_network
        self.endpoints = []
        self.clients = {}
        self.compatibility: int = compatibility
        self.shutdown_task = None
        self.data_filename = None
        self.save_filename = None
        self.saving = False
        self.player_names: typing.Dict[team_slot, str] = {}
        self.player_name_lookup: typing.Dict[str, team_slot] = {}
        self.connect_names = {}  # names of slots clients can connect to
        self.allow_releases = {}
        self.host = host
        self.port = port
        self.server_password = server_password
        self.password = password
        self.server = None
        self.countdown_timer = 0
        self.received_items = {}
        self.start_inventory = {}
        self.name_aliases: typing.Dict[team_slot, str] = {}
        self.location_checks = collections.defaultdict(set)
        self.hint_cost = hint_cost
        self.location_check_points = location_check_points
        self.hints_used = collections.defaultdict(int)
        self.hints: typing.Dict[team_slot, typing.Set[NetUtils.Hint]] = collections.defaultdict(set)
        self.release_mode: str = release_mode
        self.remaining_mode: str = remaining_mode
        self.collect_mode: str = collect_mode
        self.item_cheat = item_cheat
        self.exit_event = asyncio.Event()
        self.client_activity_timers: typing.Dict[
            team_slot, datetime.datetime] = {}  # datetime of last new item check
        self.client_connection_timers: typing.Dict[
            team_slot, datetime.datetime] = {}  # datetime of last connection
        self.client_game_state: typing.Dict[team_slot, int] = collections.defaultdict(int)
        self.er_hint_data: typing.Dict[int, typing.Dict[int, str]] = {}
        self.auto_shutdown = auto_shutdown
        self.commandprocessor = ServerCommandProcessor(self)
        self.embedded_blacklist = {"host", "port"}
        self.client_ids: typing.Dict[typing.Tuple[int, int], datetime.datetime] = {}
        self.auto_save_interval = 60  # in seconds
        self.auto_saver_thread = None
        self.save_dirty = False
        self.tags = ['AP']
        self.games: typing.Dict[int, str] = {}
        self.minimum_client_versions: typing.Dict[int, Version] = {}
        self.seed_name = ""
        self.groups = {}
        self.group_collected: typing.Dict[int, typing.Set[int]] = {}
        self.random = random.Random()
        self.stored_data = {}
        self.stored_data_notification_clients = collections.defaultdict(weakref.WeakSet)
        self.read_data = {}

        # init empty to satisfy linter, I suppose
        self.gamespackage = {}
        self.checksums = {}
        self.item_name_groups = {}
        self.location_name_groups = {}
        self.all_item_and_group_names = {}
        self.all_location_and_group_names = {}
        self.non_hintable_names = collections.defaultdict(frozenset)

        self._load_game_data()

    # Data package retrieval
    def _load_game_data(self):
        import worlds
        self.gamespackage = worlds.network_data_package["games"]

        self.item_name_groups = {world_name: world.item_name_groups for world_name, world in
                                 worlds.AutoWorldRegister.world_types.items()}
        self.location_name_groups = {world_name: world.location_name_groups for world_name, world in
                                     worlds.AutoWorldRegister.world_types.items()}
        for world_name, world in worlds.AutoWorldRegister.world_types.items():
            self.non_hintable_names[world_name] = world.hint_blacklist

    def _init_game_data(self):
        for game_name, game_package in self.gamespackage.items():
            if "checksum" in game_package:
                self.checksums[game_name] = game_package["checksum"]
            for item_name, item_id in game_package["item_name_to_id"].items():
                self.item_names[item_id] = item_name
            for location_name, location_id in game_package["location_name_to_id"].items():
                self.location_names[location_id] = location_name
            self.all_item_and_group_names[game_name] = \
                set(game_package["item_name_to_id"]) | set(self.item_name_groups[game_name])
            self.all_location_and_group_names[game_name] = \
                set(game_package["location_name_to_id"]) | set(self.location_name_groups.get(game_name, []))

    def item_names_for_game(self, game: str) -> typing.Optional[typing.Dict[str, int]]:
        return self.gamespackage[game]["item_name_to_id"] if game in self.gamespackage else None

    def location_names_for_game(self, game: str) -> typing.Optional[typing.Dict[str, int]]:
        return self.gamespackage[game]["location_name_to_id"] if game in self.gamespackage else None

    # General networking
    async def send_msgs(self, endpoint: Endpoint, msgs: typing.Iterable[dict]) -> bool:
        if not endpoint.socket or not endpoint.socket.open:
            return False
        msg = self.dumper(msgs)
        try:
            await endpoint.socket.send(msg)
        except websockets.ConnectionClosed:
            logging.exception(f"Exception during send_msgs, could not send {msg}")
            await self.disconnect(endpoint)
            return False
        else:
            if self.log_network:
                logging.info(f"Outgoing message: {msg}")
            return True

    async def send_encoded_msgs(self, endpoint: Endpoint, msg: str) -> bool:
        if not endpoint.socket or not endpoint.socket.open:
            return False
        try:
            await endpoint.socket.send(msg)
        except websockets.ConnectionClosed:
            logging.exception("Exception during send_encoded_msgs")
            await self.disconnect(endpoint)
            return False
        else:
            if self.log_network:
                logging.info(f"Outgoing message: {msg}")
            return True

    async def broadcast_send_encoded_msgs(self, endpoints: typing.Iterable[Endpoint], msg: str) -> bool:
        sockets = []
        for endpoint in endpoints:
            if endpoint.socket and endpoint.socket.open:
                sockets.append(endpoint.socket)
        try:
            websockets.broadcast(sockets, msg)
        except RuntimeError:
            logging.exception("Exception during broadcast_send_encoded_msgs")
            return False
        else:
            if self.log_network:
                logging.info(f"Outgoing broadcast: {msg}")
            return True

    def broadcast_all(self, msgs: typing.List[dict]):
        msgs = self.dumper(msgs)
        endpoints = (endpoint for endpoint in self.endpoints if endpoint.auth)
        async_start(self.broadcast_send_encoded_msgs(endpoints, msgs))

    def broadcast_text_all(self, text: str, additional_arguments: dict = {}):
        logging.info("Notice (all): %s" % text)
        self.broadcast_all([{**{"cmd": "PrintJSON", "data": [{ "text": text }]}, **additional_arguments}])

    def broadcast_team(self, team: int, msgs: typing.List[dict]):
        msgs = self.dumper(msgs)
        endpoints = (endpoint for endpoint in itertools.chain.from_iterable(self.clients[team].values()))
        async_start(self.broadcast_send_encoded_msgs(endpoints, msgs))

    def broadcast(self, endpoints: typing.Iterable[Client], msgs: typing.List[dict]):
        msgs = self.dumper(msgs)
        async_start(self.broadcast_send_encoded_msgs(endpoints, msgs))

    async def disconnect(self, endpoint: Client):
        if endpoint in self.endpoints:
            self.endpoints.remove(endpoint)
        if endpoint.slot and endpoint in self.clients[endpoint.team][endpoint.slot]:
            self.clients[endpoint.team][endpoint.slot].remove(endpoint)
        await on_client_disconnected(self, endpoint)

    def notify_client(self, client: Client, text: str, additional_arguments: dict = {}):
        if not client.auth:
            return
        logging.info("Notice (Player %s in team %d): %s" % (client.name, client.team + 1, text))
        async_start(self.send_msgs(client, [{"cmd": "PrintJSON", "data": [{ "text": text }], **additional_arguments}]))

    def notify_client_multiple(self, client: Client, texts: typing.List[str], additional_arguments: dict = {}):
        if not client.auth:
            return
        async_start(self.send_msgs(client,
                                   [{"cmd": "PrintJSON", "data": [{ "text": text }], **additional_arguments}
                                    for text in texts]))

    # loading
    def load(self, multidatapath: str, use_embedded_server_options: bool = False):
        if multidatapath.lower().endswith(".zip"):
            import zipfile
            with zipfile.ZipFile(multidatapath) as zf:
                for file in zf.namelist():
                    if file.endswith(".archipelago"):
                        data = zf.read(file)
                        break
                else:
                    raise Exception("No .archipelago found in archive.")
        else:
            with open(multidatapath, 'rb') as f:
                data = f.read()

        self._load(self.decompress(data), {}, use_embedded_server_options)
        self.data_filename = multidatapath

    @staticmethod
    def decompress(data: bytes) -> dict:
        format_version = data[0]
        if format_version > 3:
            raise Utils.VersionException("Incompatible multidata.")
        return restricted_loads(zlib.decompress(data[1:]))

    def _load(self, decoded_obj: dict, game_data_packages: typing.Dict[str, typing.Any],
              use_embedded_server_options: bool):

        self.read_data = {}
        mdata_ver = decoded_obj["minimum_versions"]["server"]
        if mdata_ver > version_tuple:
            raise RuntimeError(f"Supplied Multidata (.archipelago) requires a server of at least version {mdata_ver},"
                               f"however this server is of version {version_tuple}")
        self.generator_version = Version(*decoded_obj["version"])
        clients_ver = decoded_obj["minimum_versions"].get("clients", {})
        self.minimum_client_versions = {}
        for player, version in clients_ver.items():
            self.minimum_client_versions[player] = max(Version(*version), min_client_version)

        self.slot_info = decoded_obj["slot_info"]
        self.games = {slot: slot_info.game for slot, slot_info in self.slot_info.items()}
        self.groups = {slot: slot_info.group_members for slot, slot_info in self.slot_info.items()
                       if slot_info.type == SlotType.group}

        self.clients = {0: {}}
        slot_info: NetworkSlot
        slot_id: int

        team_0 = self.clients[0]
        for slot_id, slot_info in self.slot_info.items():
            team_0[slot_id] = []
            self.player_names[0, slot_id] = slot_info.name
            self.player_name_lookup[slot_info.name] = 0, slot_id
            self.read_data[f"hints_{0}_{slot_id}"] = lambda local_team=0, local_player=slot_id: \
                list(self.get_rechecked_hints(local_team, local_player))

        self.seed_name = decoded_obj["seed_name"]
        self.random.seed(self.seed_name)
        self.connect_names = decoded_obj['connect_names']
        self.locations = LocationStore(decoded_obj.pop("locations"))  # pre-emptively free memory
        self.slot_data = decoded_obj['slot_data']
        for slot, data in self.slot_data.items():
            self.read_data[f"slot_data_{slot}"] = lambda data=data: data
        self.er_hint_data = {int(player): {int(address): name for address, name in loc_data.items()}
                             for player, loc_data in decoded_obj["er_hint_data"].items()}

        # load start inventory:
        for slot, item_codes in decoded_obj["precollected_items"].items():
            self.start_inventory[slot] = [NetworkItem(item_code, -2, 0) for item_code in item_codes]

        for slot, hints in decoded_obj["precollected_hints"].items():
            self.hints[0, slot].update(hints)

        # declare slots that aren't players as done
        for slot, slot_info in self.slot_info.items():
            if slot_info.type.always_goal:
                for team in self.clients:
                    self.client_game_state[team, slot] = ClientStatus.CLIENT_GOAL

        if use_embedded_server_options:
            server_options = decoded_obj.get("server_options", {})
            self._set_options(server_options)

        # embedded data package
        for game_name, data in decoded_obj.get("datapackage", {}).items():
            if game_name in game_data_packages:
                data = game_data_packages[game_name]
            logging.info(f"Loading embedded data package for game {game_name}")
            self.gamespackage[game_name] = data
            self.item_name_groups[game_name] = data["item_name_groups"]
            if "location_name_groups" in data:
                self.location_name_groups[game_name] = data["location_name_groups"]
                del data["location_name_groups"]
            del data["item_name_groups"]  # remove from data package, but keep in self.item_name_groups
        self._init_game_data()
        for game_name, data in self.item_name_groups.items():
            self.read_data[f"item_name_groups_{game_name}"] = lambda lgame=game_name: self.item_name_groups[lgame]
        for game_name, data in self.location_name_groups.items():
            self.read_data[f"location_name_groups_{game_name}"] = lambda lgame=game_name: self.location_name_groups[lgame]

    # saving

    def save(self, now=False) -> bool:
        if self.saving:
            if now:
                self.save_dirty = False
                return self._save()

            self.save_dirty = True
            return True

        return False

    def _save(self, exit_save: bool = False) -> bool:
        try:
            encoded_save = pickle.dumps(self.get_save())
            with open(self.save_filename, "wb") as f:
                f.write(zlib.compress(encoded_save))
        except Exception as e:
            logging.exception(e)
            return False
        else:
            return True

    def init_save(self, enabled: bool = True):
        self.saving = enabled
        if self.saving:
            if not self.save_filename:
                import os
                name, ext = os.path.splitext(self.data_filename)
                self.save_filename = name + '.apsave' if ext.lower() in ('.archipelago', '.zip') \
                    else self.data_filename + '_' + 'apsave'
            try:
                with open(self.save_filename, 'rb') as f:
                    save_data = restricted_loads(zlib.decompress(f.read()))
                    self.set_save(save_data)
            except FileNotFoundError:
                logging.error('No save data found, starting a new game')
            except Exception as e:
                logging.exception(e)
            self._start_async_saving()

    def _start_async_saving(self):
        if not self.auto_saver_thread:
            def save_regularly():
                # time.time() is platform dependent, so using the expensive datetime method instead
                def get_datetime_second():
                    now = datetime.datetime.now()
                    return now.second + now.microsecond * 0.000001

                second = get_saving_second(self.seed_name, self.auto_save_interval)
                while not self.exit_event.is_set():
                    try:
                        next_wakeup = (second - get_datetime_second()) % self.auto_save_interval
                        time.sleep(max(1.0, next_wakeup))
                        if self.save_dirty:
                            logging.debug("Saving via thread.")
                            self._save()
                    except OperationalError as e:
                        logging.exception(e)
                        logging.info(f"Saving failed. Retry in {self.auto_save_interval} seconds.")
                    else:
                        self.save_dirty = False
            self.auto_saver_thread = threading.Thread(target=save_regularly, daemon=True)
            self.auto_saver_thread.start()

            import atexit
            atexit.register(self._save, True)  # make sure we save on exit too

    def get_save(self) -> dict:
        self.recheck_hints()
        d = {
            "version": self.save_version,
            "connect_names": self.connect_names,
            "received_items": self.received_items,
            "hints_used": dict(self.hints_used),
            "hints": dict(self.hints),
            "location_checks": dict(self.location_checks),
            "name_aliases": self.name_aliases,
            "client_game_state": dict(self.client_game_state),
            "client_activity_timers": tuple(
                (key, value.timestamp()) for key, value in self.client_activity_timers.items()),
            "client_connection_timers": tuple(
                (key, value.timestamp()) for key, value in self.client_connection_timers.items()),
            "random_state": self.random.getstate(),
            "group_collected": dict(self.group_collected),
            "stored_data": self.stored_data,
            "game_options": {"hint_cost": self.hint_cost, "location_check_points": self.location_check_points,
                             "server_password": self.server_password, "password": self.password,
                             "release_mode": self.release_mode,
                             "remaining_mode": self.remaining_mode, "collect_mode": self.collect_mode,
                             "item_cheat": self.item_cheat, "compatibility": self.compatibility}

        }

        return d

    def set_save(self, savedata: dict):
        if self.connect_names != savedata["connect_names"]:
            raise Exception("This savegame does not appear to match the loaded multiworld.")
        if savedata["version"] > self.save_version:
            raise Exception("This savegame is newer than the server.")
        self.received_items = savedata["received_items"]
        self.hints_used.update(savedata["hints_used"])
        self.hints.update(savedata["hints"])

        self.name_aliases.update(savedata["name_aliases"])
        self.client_game_state.update(savedata["client_game_state"])
        self.client_connection_timers.update(
            {tuple(key): datetime.datetime.fromtimestamp(value, datetime.timezone.utc) for key, value
             in savedata["client_connection_timers"]})
        self.client_activity_timers.update(
            {tuple(key): datetime.datetime.fromtimestamp(value, datetime.timezone.utc) for key, value
             in savedata["client_activity_timers"]})
        self.location_checks.update(savedata["location_checks"])
        self.random.setstate(savedata["random_state"])

        if "game_options" in savedata:
            self.hint_cost = savedata["game_options"]["hint_cost"]
            self.location_check_points = savedata["game_options"]["location_check_points"]
            self.server_password = savedata["game_options"]["server_password"]
            self.password = savedata["game_options"]["password"]
            self.release_mode = savedata["game_options"].get("release_mode", savedata["game_options"].get("forfeit_mode", "goal"))
            self.remaining_mode = savedata["game_options"]["remaining_mode"]
            self.collect_mode = savedata["game_options"]["collect_mode"]
            self.item_cheat = savedata["game_options"]["item_cheat"]
            self.compatibility = savedata["game_options"]["compatibility"]

        if "group_collected" in savedata:
            self.group_collected = savedata["group_collected"]

        if "stored_data" in savedata:
            self.stored_data = savedata["stored_data"]
        # count items and slots from lists for items_handling = remote
        logging.info(
            f'Loaded save file with {sum([len(v) for k, v in self.received_items.items() if k[2]])} received items '
            f'for {sum(k[2] for k in self.received_items)} players')

    # rest

    def get_hint_cost(self, slot):
        if self.hint_cost:
            return max(1, int(self.hint_cost * 0.01 * len(self.locations[slot])))
        return 0

    def recheck_hints(self, team: typing.Optional[int] = None, slot: typing.Optional[int] = None):
        for hint_team, hint_slot in self.hints:
            if (team is None or team == hint_team) and (slot is None or slot == hint_slot):
                self.hints[hint_team, hint_slot] = {
                    hint.re_check(self, hint_team) for hint in
                    self.hints[hint_team, hint_slot]
                }

    def get_rechecked_hints(self, team: int, slot: int):
        self.recheck_hints(team, slot)
        return self.hints[team, slot]

    def get_players_package(self):
        return [NetworkPlayer(t, p, self.get_aliased_name(t, p), n) for (t, p), n in self.player_names.items()]

    def slot_set(self, slot) -> typing.Set[int]:
        """Returns the slot IDs that concern that slot,
        as in expands groups out and returns back the input for solo."""
        return self.groups.get(slot, {slot})

    def _set_options(self, server_options: dict):
        for key, value in server_options.items():
            if key == "forfeit_mode":
                key = "release_mode"
            data_type = self.simple_options.get(key, None)
            if data_type is not None:
                if value not in {False, True, None}:  # some can be boolean OR text, such as password
                    try:
                        value = data_type(value)
                    except Exception as e:
                        try:
                            raise Exception(f"Could not set server option {key}, skipping.") from e
                        except Exception as e:
                            logging.exception(e)
                logging.debug(f"Setting server option {key} to {value} from supplied multidata")
                setattr(self, key, value)
            elif key == "disable_item_cheat":
                self.item_cheat = not bool(value)
            else:
                logging.debug(f"Unrecognized server option {key}")

    def get_aliased_name(self, team: int, slot: int):
        if (team, slot) in self.name_aliases:
            return f"{self.name_aliases[team, slot]} ({self.player_names[team, slot]})"
        else:
            return self.player_names[team, slot]

    def notify_hints(self, team: int, hints: typing.List[NetUtils.Hint], only_new: bool = False):
        """Send and remember hints."""
        if only_new:
            hints = [hint for hint in hints if hint not in self.hints[team, hint.finding_player]]
        if not hints:
            return
        new_hint_events: typing.Set[int] = set()
        concerns = collections.defaultdict(list)
        for hint in sorted(hints, key=operator.attrgetter('found'), reverse=True):
            data = (hint, hint.as_network_message())
            for player in self.slot_set(hint.receiving_player):
                concerns[player].append(data)
            if not hint.local and data not in concerns[hint.finding_player]:
                concerns[hint.finding_player].append(data)
            # remember hints in all cases
            if not hint.found:
                # since hints are bidirectional, finding player and receiving player,
                # we can check once if hint already exists
                if hint not in self.hints[team, hint.finding_player]:
                    self.hints[team, hint.finding_player].add(hint)
                    new_hint_events.add(hint.finding_player)
                    for player in self.slot_set(hint.receiving_player):
                        self.hints[team, player].add(hint)
                        new_hint_events.add(player)

            logging.info("Notice (Team #%d): %s" % (team + 1, format_hint(self, team, hint)))
        for slot in new_hint_events:
            self.on_new_hint(team, slot)
        for slot, hint_data in concerns.items():
            clients = self.clients[team].get(slot)
            if not clients:
                continue
            client_hints = [datum[1] for datum in sorted(hint_data, key=lambda x: x[0].finding_player == slot)]
            for client in clients:
                async_start(self.send_msgs(client, client_hints))

    # "events"

    def on_goal_achieved(self, client: Client):
        finished_msg = f'{self.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1})' \
                       f' has completed their goal.'
        self.broadcast_text_all(finished_msg, {"type": "Goal", "team": client.team, "slot": client.slot})
        if "auto" in self.collect_mode:
            collect_player(self, client.team, client.slot)
        if "auto" in self.release_mode:
            release_player(self, client.team, client.slot)
        self.save()  # save goal completion flag

    def on_new_hint(self, team: int, slot: int):
        key: str = f"_read_hints_{team}_{slot}"
        targets: typing.Set[Client] = set(self.stored_data_notification_clients[key])
        if targets:
            self.broadcast(targets, [{"cmd": "SetReply", "key": key, "value": self.hints[team, slot]}])
        self.broadcast(self.clients[team][slot], [{
            "cmd": "RoomUpdate",
            "hint_points": get_slot_points(self, team, slot)
        }])


def update_aliases(ctx: Context, team: int):
    cmd = ctx.dumper([{"cmd": "RoomUpdate",
                       "players": ctx.get_players_package()}])

    for clients in ctx.clients[team].values():
        for client in clients:
            async_start(ctx.send_encoded_msgs(client, cmd))


async def server(websocket, path: str = "/", ctx: Context = None):
    client = Client(websocket, ctx)
    ctx.endpoints.append(client)

    try:
        if ctx.log_network:
            logging.info("Incoming connection")
        await on_client_connected(ctx, client)
        if ctx.log_network:
            logging.info("Sent Room Info")
        async for data in websocket:
            if ctx.log_network:
                logging.info(f"Incoming message: {data}")
            for msg in decode(data):
                await process_client_cmd(ctx, client, msg)
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
    finally:
        if ctx.log_network:
            logging.info("Disconnected")
        await ctx.disconnect(client)


async def on_client_connected(ctx: Context, client: Client):
    players = []
    for team, clients in ctx.clients.items():
        for slot, connected_clients in clients.items():
            if connected_clients:
                name = ctx.player_names[team, slot]
                players.append(
                    NetworkPlayer(team, slot,
                                  ctx.name_aliases.get((team, slot), name), name)
                )
    games = {ctx.games[x] for x in range(1, len(ctx.games) + 1)}
    games.add("Archipelago")
    await ctx.send_msgs(client, [{
        'cmd': 'RoomInfo',
        'password': bool(ctx.password),
        'games': games,
        # tags are for additional features in the communication.
        # Name them by feature or fork, as you feel is appropriate.
        'tags': ctx.tags,
        'version': version_tuple,
        'generator_version': ctx.generator_version,
        'permissions': get_permissions(ctx),
        'hint_cost': ctx.hint_cost,
        'location_check_points': ctx.location_check_points,
        'datapackage_versions': {game: game_data["version"] for game, game_data
                                 in ctx.gamespackage.items() if game in games},
        'datapackage_checksums': {game: game_data["checksum"] for game, game_data
                                  in ctx.gamespackage.items() if game in games and "checksum" in game_data},
        'seed_name': ctx.seed_name,
        'time': time.time(),
    }])


def get_permissions(ctx) -> typing.Dict[str, Permission]:
    return {
        "release": Permission.from_text(ctx.release_mode),
        "remaining": Permission.from_text(ctx.remaining_mode),
        "collect": Permission.from_text(ctx.collect_mode)
    }


async def on_client_disconnected(ctx: Context, client: Client):
    if client.auth:
        await on_client_left(ctx, client)


async def on_client_joined(ctx: Context, client: Client):
    if ctx.client_game_state[client.team, client.slot] == ClientStatus.CLIENT_UNKNOWN:
        update_client_status(ctx, client, ClientStatus.CLIENT_CONNECTED)
    version_str = '.'.join(str(x) for x in client.version)
    verb = "tracking" if "Tracker" in client.tags else "playing"
    ctx.broadcast_text_all(
        f"{ctx.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1}) "
        f"{verb} {ctx.games[client.slot]} has joined. "
        f"Client({version_str}), {client.tags}.",
        {"type": "Join", "team": client.team, "slot": client.slot, "tags": client.tags})
    ctx.notify_client(client, "Now that you are connected, "
                              "you can use !help to list commands to run via the server. "
                              "If your client supports it, "
                              "you may have additional local commands you can list with /help.",
                      {"type": "Tutorial"})
    ctx.client_connection_timers[client.team, client.slot] = datetime.datetime.now(datetime.timezone.utc)


async def on_client_left(ctx: Context, client: Client):
    if len(ctx.clients[client.team][client.slot]) < 1:
        update_client_status(ctx, client, ClientStatus.CLIENT_UNKNOWN)
        ctx.client_connection_timers[client.team, client.slot] = datetime.datetime.now(datetime.timezone.utc)
    ctx.broadcast_text_all(
        "%s (Team #%d) has left the game" % (ctx.get_aliased_name(client.team, client.slot), client.team + 1),
        {"type": "Part", "team": client.team, "slot": client.slot})


async def countdown(ctx: Context, timer: int):
    ctx.broadcast_text_all(f"[Server]: Starting countdown of {timer}s", {"type": "Countdown", "countdown": timer})
    if ctx.countdown_timer:
        ctx.countdown_timer = timer  # timer is already running, set it to a different time
    else:
        ctx.countdown_timer = timer
        while ctx.countdown_timer > 0:
            ctx.broadcast_text_all(f"[Server]: {ctx.countdown_timer}",
                {"type": "Countdown", "countdown": ctx.countdown_timer})
            ctx.countdown_timer -= 1
            await asyncio.sleep(1)
        ctx.broadcast_text_all(f"[Server]: GO", {"type": "Countdown", "countdown": 0})
        ctx.countdown_timer = 0


def get_players_string(ctx: Context):
    auth_clients = {(c.team, c.slot) for c in ctx.endpoints if c.auth}

    player_names = sorted(ctx.player_names.keys())
    current_team = -1
    text = ''
    total = 0
    for team, slot in player_names:
        if ctx.slot_info[slot].type == SlotType.player:
            total += 1
            player_name = ctx.player_names[team, slot]
            if team != current_team:
                text += f':: Team #{team + 1}: '
                current_team = team
            if (team, slot) in auth_clients:
                text += f'{player_name} '
            else:
                text += f'({player_name}) '
    return f'{len(auth_clients)} players of {total} connected ' + text[:-1]


def get_status_string(ctx: Context, team: int, tag: str):
    text = f"Player Status on team {team}:"
    for slot in ctx.locations:
        connected = len(ctx.clients[team][slot])
        tagged = len([client for client in ctx.clients[team][slot] if tag in client.tags])
        completion_text = f"({len(ctx.location_checks[team, slot])}/{len(ctx.locations[slot])})"
        tag_text = f" {tagged} of which are tagged {tag}" if connected and tag else ""
        goal_text = " and has finished." if ctx.client_game_state[team, slot] == ClientStatus.CLIENT_GOAL else "."
        text += f"\n{ctx.get_aliased_name(team, slot)} has {connected} connection{'' if connected == 1 else 's'}" \
                f"{tag_text}{goal_text} {completion_text}"
    return text


def get_received_items(ctx: Context, team: int, player: int, remote_items: bool) -> typing.List[NetworkItem]:
    return ctx.received_items.setdefault((team, player, remote_items), [])


def get_start_inventory(ctx: Context, player: int, remote_start_inventory: bool) -> typing.List[NetworkItem]:
    return ctx.start_inventory.setdefault(player, []) if remote_start_inventory else []


def send_new_items(ctx: Context):
    for team, clients in ctx.clients.items():
        for slot, clients in clients.items():
            for client in clients:
                if client.no_items:
                    continue
                start_inventory = get_start_inventory(ctx, slot, client.remote_start_inventory)
                items = get_received_items(ctx, team, slot, client.remote_items)
                if len(start_inventory) + len(items) > client.send_index:
                    first_new_item = max(0, client.send_index - len(start_inventory))
                    async_start(ctx.send_msgs(client, [{
                        "cmd": "ReceivedItems",
                        "index": client.send_index,
                        "items": start_inventory[client.send_index:] + items[first_new_item:]}]))
                    client.send_index = len(start_inventory) + len(items)


def update_checked_locations(ctx: Context, team: int, slot: int):
    ctx.broadcast(ctx.clients[team][slot],
                  [{"cmd": "RoomUpdate", "checked_locations": get_checked_checks(ctx, team, slot)}])


def release_player(ctx: Context, team: int, slot: int):
    """register any locations that are in the multidata"""
    all_locations = set(ctx.locations[slot])
    ctx.broadcast_text_all("%s (Team #%d) has released all remaining items from their world."
                           % (ctx.player_names[(team, slot)], team + 1),
                           {"type": "Release", "team": team, "slot": slot})
    register_location_checks(ctx, team, slot, all_locations)
    update_checked_locations(ctx, team, slot)


def collect_player(ctx: Context, team: int, slot: int, is_group: bool = False):
    """register any locations that are in the multidata, pointing towards this player"""
    all_locations = ctx.locations.get_for_player(slot)

    ctx.broadcast_text_all("%s (Team #%d) has collected their items from other worlds."
                           % (ctx.player_names[(team, slot)], team + 1),
                           {"type": "Collect", "team": team, "slot": slot})
    for source_player, location_ids in all_locations.items():
        register_location_checks(ctx, team, source_player, location_ids, count_activity=False)
        update_checked_locations(ctx, team, source_player)

    if not is_group:
        for group, group_players in ctx.groups.items():
            if slot in group_players:
                group_collected_players = ctx.group_collected.setdefault(group, set())
                group_collected_players.add(slot)
                if set(group_players) == group_collected_players:
                    collect_player(ctx, team, group, True)


def get_remaining(ctx: Context, team: int, slot: int) -> typing.List[int]:
    return ctx.locations.get_remaining(ctx.location_checks, team, slot)


def send_items_to(ctx: Context, team: int, target_slot: int, *items: NetworkItem):
    for target in ctx.slot_set(target_slot):
        for item in items:
            if item.player != target_slot:
                get_received_items(ctx, team, target, False).append(item)
            get_received_items(ctx, team, target, True).append(item)


def register_location_checks(ctx: Context, team: int, slot: int, locations: typing.Iterable[int],
                             count_activity: bool = True):
    new_locations = set(locations) - ctx.location_checks[team, slot]
    new_locations.intersection_update(ctx.locations[slot])  # ignore location IDs unknown to this multidata
    if new_locations:
        if count_activity:
            ctx.client_activity_timers[team, slot] = datetime.datetime.now(datetime.timezone.utc)
        for location in new_locations:
            item_id, target_player, flags = ctx.locations[slot][location]
            new_item = NetworkItem(item_id, location, slot, flags)
            send_items_to(ctx, team, target_player, new_item)

            logging.info('(Team #%d) %s sent %s to %s (%s)' % (
                team + 1, ctx.player_names[(team, slot)], ctx.item_names[item_id],
                ctx.player_names[(team, target_player)], ctx.location_names[location]))
            info_text = json_format_send_event(new_item, target_player)
            ctx.broadcast_team(team, [info_text])

        ctx.location_checks[team, slot] |= new_locations
        send_new_items(ctx)
        ctx.broadcast(ctx.clients[team][slot], [{
            "cmd": "RoomUpdate",
            "hint_points": get_slot_points(ctx, team, slot),
            "checked_locations": new_locations,  # send back new checks only
        }])

        ctx.save()


def collect_hints(ctx: Context, team: int, slot: int, item: typing.Union[int, str]) -> typing.List[NetUtils.Hint]:
    hints = []
    slots: typing.Set[int] = {slot}
    for group_id, group in ctx.groups.items():
        if slot in group:
            slots.add(group_id)

    seeked_item_id = item if isinstance(item, int) else ctx.item_names_for_game(ctx.games[slot])[item]
    for finding_player, location_id, item_id, receiving_player, item_flags \
            in ctx.locations.find_item(slots, seeked_item_id):
        found = location_id in ctx.location_checks[team, finding_player]
        entrance = ctx.er_hint_data.get(finding_player, {}).get(location_id, "")
        hints.append(NetUtils.Hint(receiving_player, finding_player, location_id, item_id, found, entrance,
                                   item_flags))

    return hints


def collect_hint_location_name(ctx: Context, team: int, slot: int, location: str) -> typing.List[NetUtils.Hint]:
    seeked_location: int = ctx.location_names_for_game(ctx.games[slot])[location]
    return collect_hint_location_id(ctx, team, slot, seeked_location)


def collect_hint_location_id(ctx: Context, team: int, slot: int, seeked_location: int) -> typing.List[NetUtils.Hint]:
    result = ctx.locations[slot].get(seeked_location, (None, None, None))
    if any(result):
        item_id, receiving_player, item_flags = result

        found = seeked_location in ctx.location_checks[team, slot]
        entrance = ctx.er_hint_data.get(slot, {}).get(seeked_location, "")
        return [NetUtils.Hint(receiving_player, slot, seeked_location, item_id, found, entrance, item_flags)]
    return []


def format_hint(ctx: Context, team: int, hint: NetUtils.Hint) -> str:
    text = f"[Hint]: {ctx.player_names[team, hint.receiving_player]}'s " \
           f"{ctx.item_names[hint.item]} is " \
           f"at {ctx.location_names[hint.location]} " \
           f"in {ctx.player_names[team, hint.finding_player]}'s World"

    if hint.entrance:
        text += f" at {hint.entrance}"
    return text + (". (found)" if hint.found else ".")


def json_format_send_event(net_item: NetworkItem, receiving_player: int):
    parts = []
    NetUtils.add_json_text(parts, net_item.player, type=NetUtils.JSONTypes.player_id)
    if net_item.player == receiving_player:
        NetUtils.add_json_text(parts, " found their ")
        NetUtils.add_json_item(parts, net_item.item, net_item.player, net_item.flags)
    else:
        NetUtils.add_json_text(parts, " sent ")
        NetUtils.add_json_item(parts, net_item.item, receiving_player, net_item.flags)
        NetUtils.add_json_text(parts, " to ")
        NetUtils.add_json_text(parts, receiving_player, type=NetUtils.JSONTypes.player_id)

    NetUtils.add_json_text(parts, " (")
    NetUtils.add_json_location(parts, net_item.location, net_item.player)
    NetUtils.add_json_text(parts, ")")

    return {"cmd": "PrintJSON", "data": parts, "type": "ItemSend",
            "receiving": receiving_player,
            "item": net_item}


def get_intended_text(input_text: str, possible_answers) -> typing.Tuple[str, bool, str]:
    picks = Utils.get_fuzzy_results(input_text, possible_answers, limit=2)
    if len(picks) > 1:
        dif = picks[0][1] - picks[1][1]
        if picks[0][1] == 100:
            return picks[0][0], True, "Perfect Match"
        elif picks[0][1] < 75:
            return picks[0][0], False, f"Didn't find something that closely matches, " \
                                       f"did you mean {picks[0][0]}? ({picks[0][1]}% sure)"
        elif dif > 5:
            return picks[0][0], True, "Close Match"
        else:
            return picks[0][0], False, f"Too many close matches, did you mean {picks[0][0]}? ({picks[0][1]}% sure)"
    else:
        if picks[0][1] > 90:
            return picks[0][0], True, "Only Option Match"
        else:
            return picks[0][0], False, f"Did you mean {picks[0][0]}? ({picks[0][1]}% sure)"


class CommandMeta(type):
    def __new__(cls, name, bases, attrs):
        commands = attrs["commands"] = {}
        for base in bases:
            commands.update(base.commands)
        commands.update({command_name[5:]: method for command_name, method in attrs.items() if
                         command_name.startswith("_cmd_")})
        return super(CommandMeta, cls).__new__(cls, name, bases, attrs)


_Return = typing.TypeVar("_Return")
# TODO: when python 3.10 is lowest supported, typing.ParamSpec


def mark_raw(function: typing.Callable[[typing.Any], _Return]) -> typing.Callable[[typing.Any], _Return]:
    function.raw_text = True
    return function


class CommandProcessor(metaclass=CommandMeta):
    commands: typing.Dict[str, typing.Callable]
    client = None
    marker = "/"

    def output(self, text: str):
        print(text)

    def __call__(self, raw: str) -> typing.Optional[bool]:
        if not raw:
            return
        try:
            command = raw.split()
            basecommand = command[0]
            if basecommand[0] == self.marker:
                method = self.commands.get(basecommand[1:].lower(), None)
                if not method:
                    self._error_unknown_command(basecommand[1:])
                else:
                    if getattr(method, "raw_text", False):  # method is requesting unprocessed text data
                        arg = raw.split(maxsplit=1)
                        if len(arg) > 1:
                            return method(self, arg[1])  # argument text was found, so pass it along
                        else:
                            return method(self)  # argument may be optional, try running without args
                    else:
                        return method(self, *command[1:])  # pass each word as argument
            else:
                self.default(raw)
        except Exception as e:
            self._error_parsing_command(e)

    def get_help_text(self) -> str:
        s = ""
        for command, method in self.commands.items():
            spec = inspect.signature(method).parameters
            argtext = ""
            for argname, parameter in spec.items():
                if argname == "self":
                    continue

                if isinstance(parameter.default, str):
                    if not parameter.default:
                        argname = f"[{argname}]"
                    else:
                        argname += "=" + parameter.default
                argtext += argname
                argtext += " "
            s += f"{self.marker}{command} {argtext}\n    {method.__doc__}\n"
        return s

    def _cmd_help(self):
        """Returns the help listing"""
        self.output(self.get_help_text())

    def _cmd_license(self):
        """Returns the licensing information"""
        license = getattr(CommandProcessor, "license", None)
        if not license:
            with open(Utils.local_path("LICENSE")) as f:
                CommandProcessor.license = f.read()
        self.output(CommandProcessor.license)

    def default(self, raw: str):
        self.output("Echo: " + raw)

    def _error_unknown_command(self, raw: str):
        self.output(f"Could not find command {raw}. Known commands: {', '.join(self.commands)}")

    def _error_parsing_command(self, exception: Exception):
        import traceback
        self.output(traceback.format_exc())


class CommonCommandProcessor(CommandProcessor):
    ctx: Context

    def _cmd_countdown(self, seconds: str = "10") -> bool:
        """Start a countdown in seconds"""
        try:
            timer = int(seconds, 10)
        except ValueError:
            timer = 10
        async_start(countdown(self.ctx, timer))
        return True

    def _cmd_options(self):
        """List all current options. Warning: lists password."""
        self.output("Current options:")
        for option in self.ctx.simple_options:
            if option == "server_password" and self.marker == "!":  # Do not display the server password to the client.
                self.output(f"Option server_password is set to {('*' * random.randint(4, 16))}")
            else:
                self.output(f"Option {option} is set to {getattr(self.ctx, option)}")


class ClientMessageProcessor(CommonCommandProcessor):
    marker = "!"

    def __init__(self, ctx: Context, client: Client):
        self.ctx = ctx
        self.client = client

    def __call__(self, raw: str) -> typing.Optional[bool]:
        if not raw.startswith("!admin"):
            self.ctx.broadcast_text_all(self.ctx.get_aliased_name(self.client.team, self.client.slot) + ': ' + raw,
                                        {"type": "Chat", "team": self.client.team, "slot": self.client.slot, "message": raw})
        return super(ClientMessageProcessor, self).__call__(raw)

    def output(self, text: str):
        self.ctx.notify_client(self.client, text, {"type": "CommandResult"})

    def output_multiple(self, texts: typing.List[str]):
        self.ctx.notify_client_multiple(self.client, texts, {"type": "CommandResult"})

    def default(self, raw: str):
        pass  # default is client sending just text

    def is_authenticated(self):
        return self.ctx.commandprocessor.client == self.client

    @mark_raw
    def _cmd_admin(self, command: str = ""):
        """Allow remote administration of the multiworld server
        Usage: "!admin login <password>" in order to log in to the remote interface.
        Once logged in, you can then use "!admin <command>" to issue commands.
        If you need further help once logged in.  use "!admin /help" """

        output = f"!admin {command}"
        if output.lower().startswith(
                "!admin login"):  # disallow others from seeing the supplied password, whether it is correct.
            output = f"!admin login {('*' * random.randint(4, 16))}"
        elif output.lower().startswith(
                # disallow others from knowing what the new remote administration password is.
                "!admin /option server_password"):
            output = f"!admin /option server_password {('*' * random.randint(4, 16))}"
        self.ctx.broadcast_text_all(self.ctx.get_aliased_name(self.client.team, self.client.slot) + ': ' + output,
                                    {"type": "Chat", "team": self.client.team, "slot": self.client.slot, "message": output})

        if not self.ctx.server_password:
            self.output("Sorry, Remote administration is disabled")
            return False

        if not command:
            if self.is_authenticated():
                self.output("Usage: !admin [Server command].\nUse !admin /help for help.\n"
                            "Use !admin logout to log out of the current session.")
            else:
                self.output("Usage: !admin login [password]")
            return True

        if command.startswith("login "):
            if command == f"login {self.ctx.server_password}":
                self.output("Login successful. You can now issue server side commands.")
                self.ctx.commandprocessor.client = self.client
                return True
            else:
                self.output("Password incorrect.")
                return False

        if not self.is_authenticated():
            self.output("You must first login using !admin login [password]")
            return False

        if command == "logout":
            self.output("Logout successful. You can no longer issue server side commands.")
            self.ctx.commandprocessor.client = None
            return True

        return self.ctx.commandprocessor(command)

    def _cmd_players(self) -> bool:
        """Get information about connected and missing players."""
        if len(self.ctx.player_names) < 10:
            self.ctx.broadcast_text_all(get_players_string(self.ctx), {"type": "CommandResult"})
        else:
            self.output(get_players_string(self.ctx))
        return True

    def _cmd_status(self, tag:str="") -> bool:
        """Get status information about your team.
        Optionally mention a Tag name and get information on who has that Tag.
        For example: DeathLink or EnergyLink."""
        self.output(get_status_string(self.ctx, self.client.team, tag))
        return True

    def _cmd_release(self) -> bool:
        """Sends remaining items in your world to their recipients."""
        if self.ctx.allow_releases.get((self.client.team, self.client.slot), False):
            release_player(self.ctx, self.client.team, self.client.slot)
            return True
        if "enabled" in self.ctx.release_mode:
            release_player(self.ctx, self.client.team, self.client.slot)
            return True
        elif "disabled" in self.ctx.release_mode:
            self.output("Sorry, client item releasing has been disabled on this server. "
                        "You can ask the server admin for a /release")
            return False
        else:  # is auto or goal
            if self.ctx.client_game_state[self.client.team, self.client.slot] == ClientStatus.CLIENT_GOAL:
                release_player(self.ctx, self.client.team, self.client.slot)
                return True
            else:
                self.output(
                    "Sorry, client item releasing requires you to have beaten the game on this server."
                    " You can ask the server admin for a /release")
                return False

    def _cmd_collect(self) -> bool:
        """Send your remaining items to yourself"""
        if "enabled" in self.ctx.collect_mode:
            collect_player(self.ctx, self.client.team, self.client.slot)
            return True
        elif "disabled" in self.ctx.collect_mode:
            self.output(
                "Sorry, client collecting has been disabled on this server. You can ask the server admin for a /collect")
            return False
        else:  # is auto or goal
            if self.ctx.client_game_state[self.client.team, self.client.slot] == ClientStatus.CLIENT_GOAL:
                collect_player(self.ctx, self.client.team, self.client.slot)
                return True
            else:
                self.output(
                    "Sorry, client collecting requires you to have beaten the game on this server."
                    " You can ask the server admin for a /collect")
                return False

    def _cmd_remaining(self) -> bool:
        """List remaining items in your game, but not their location or recipient"""
        if self.ctx.remaining_mode == "enabled":
            remaining_item_ids = get_remaining(self.ctx, self.client.team, self.client.slot)
            if remaining_item_ids:
                self.output("Remaining items: " + ", ".join(self.ctx.item_names[item_id]
                                                            for item_id in remaining_item_ids))
            else:
                self.output("No remaining items found.")
            return True
        elif self.ctx.remaining_mode == "disabled":
            self.output(
                "Sorry, !remaining has been disabled on this server.")
            return False
        else:  # is goal
            if self.ctx.client_game_state[self.client.team, self.client.slot] == ClientStatus.CLIENT_GOAL:
                remaining_item_ids = get_remaining(self.ctx, self.client.team, self.client.slot)
                if remaining_item_ids:
                    self.output("Remaining items: " + ", ".join(self.ctx.item_names[item_id]
                                                                for item_id in remaining_item_ids))
                else:
                    self.output("No remaining items found.")
                return True
            else:
                self.output(
                    "Sorry, !remaining requires you to have beaten the game on this server")
                return False

    def _cmd_missing(self, filter_text="") -> bool:
        """List all missing location checks from the server's perspective.
        Can be given text, which will be used as filter."""

        locations = get_missing_checks(self.ctx, self.client.team, self.client.slot)

        if locations:
            names = [self.ctx.location_names[location] for location in locations]
            if filter_text:
                names = [name for name in names if filter_text in name]
            texts = [f'Missing: {name}' for name in names]
            if filter_text:
                texts.append(f"Found {len(locations)} missing location checks, displaying {len(names)} of them.")
            else:
                texts.append(f"Found {len(locations)} missing location checks")
            self.output_multiple(texts)
        else:
            self.output("No missing location checks found.")
        return True

    def _cmd_checked(self, filter_text="") -> bool:
        """List all done location checks from the server's perspective.
        Can be given text, which will be used as filter."""

        locations = get_checked_checks(self.ctx, self.client.team, self.client.slot)

        if locations:
            names = [self.ctx.location_names[location] for location in locations]
            if filter_text:
                names = [name for name in names if filter_text in name]
            texts = [f'Checked: {name}' for name in names]
            if filter_text:
                texts.append(f"Found {len(locations)} done location checks, displaying {len(names)} of them.")
            else:
                texts.append(f"Found {len(locations)} done location checks")
            self.output_multiple(texts)
        else:
            self.output("No done location checks found.")
        return True

    @mark_raw
    def _cmd_alias(self, alias_name: str = ""):
        """Set your alias to the passed name."""
        if alias_name:
            alias_name = alias_name[:16].strip()
            self.ctx.name_aliases[self.client.team, self.client.slot] = alias_name
            self.output(f"Hello, {alias_name}")
            update_aliases(self.ctx, self.client.team)
            self.ctx.save()
            return True
        elif (self.client.team, self.client.slot) in self.ctx.name_aliases:
            del (self.ctx.name_aliases[self.client.team, self.client.slot])
            self.output("Removed Alias")
            update_aliases(self.ctx, self.client.team)
            self.ctx.save()
            return True
        return False

    @mark_raw
    def _cmd_getitem(self, item_name: str) -> bool:
        """Cheat in an item, if it is enabled on this server"""
        if self.ctx.item_cheat:
            names = self.ctx.item_names_for_game(self.ctx.games[self.client.slot])
            item_name, usable, response = get_intended_text(
                item_name,
                names
            )
            if usable:
                new_item = NetworkItem(names[item_name], -1, self.client.slot)
                get_received_items(self.ctx, self.client.team, self.client.slot, False).append(new_item)
                get_received_items(self.ctx, self.client.team, self.client.slot, True).append(new_item)
                self.ctx.broadcast_text_all(
                    'Cheat console: sending "' + item_name + '" to ' + self.ctx.get_aliased_name(self.client.team,
                                                                                                 self.client.slot),
                    {"type": "ItemCheat", "team": self.client.team, "receiving": self.client.slot, "item": new_item})
                send_new_items(self.ctx)
                return True
            else:
                self.output(response)
                return False
        else:
            self.output("Cheating is disabled.")
            return False

    def get_hints(self, input_text: str, for_location: bool = False) -> bool:
        points_available = get_client_points(self.ctx, self.client)
        cost = self.ctx.get_hint_cost(self.client.slot)

        if not input_text:
            hints = {hint.re_check(self.ctx, self.client.team) for hint in
                     self.ctx.hints[self.client.team, self.client.slot]}
            self.ctx.hints[self.client.team, self.client.slot] = hints
            self.ctx.notify_hints(self.client.team, list(hints))
            self.output(f"A hint costs {self.ctx.get_hint_cost(self.client.slot)} points. "
                        f"You have {points_available} points.")
            return True

        elif input_text.isnumeric():
            game = self.ctx.games[self.client.slot]
            hint_id = int(input_text)
            hint_name = self.ctx.item_names[hint_id] \
                if not for_location and hint_id in self.ctx.item_names \
                else self.ctx.location_names[hint_id] \
                if for_location and hint_id in self.ctx.location_names \
                else None
            if hint_name in self.ctx.non_hintable_names[game]:
                self.output(f"Sorry, \"{hint_name}\" is marked as non-hintable.")
                hints = []
            elif not for_location:
                hints = collect_hints(self.ctx, self.client.team, self.client.slot, hint_id)
            else:
                hints = collect_hint_location_id(self.ctx, self.client.team, self.client.slot, hint_id)

        else:
            game = self.ctx.games[self.client.slot]
            if game not in self.ctx.all_item_and_group_names:
                self.output("Can't look up item/location for unknown game. Hint for ID instead.")
                return False
            names = self.ctx.all_location_and_group_names[game] \
                if for_location else \
                self.ctx.all_item_and_group_names[game]
            hint_name, usable, response = get_intended_text(input_text, names)

            if usable:
                if hint_name in self.ctx.non_hintable_names[game]:
                    self.output(f"Sorry, \"{hint_name}\" is marked as non-hintable.")
                    hints = []
                elif not for_location and hint_name in self.ctx.item_name_groups[game]:  # item group name
                    hints = []
                    for item_name in self.ctx.item_name_groups[game][hint_name]:
                        if item_name in self.ctx.item_names_for_game(game):  # ensure item has an ID
                            hints.extend(collect_hints(self.ctx, self.client.team, self.client.slot, item_name))
                elif not for_location and hint_name in self.ctx.item_names_for_game(game):  # item name
                    hints = collect_hints(self.ctx, self.client.team, self.client.slot, hint_name)
                elif hint_name in self.ctx.location_name_groups[game]:  # location group name
                    hints = []
                    for loc_name in self.ctx.location_name_groups[game][hint_name]:
                        if loc_name in self.ctx.location_names_for_game(game):
                            hints.extend(collect_hint_location_name(self.ctx, self.client.team, self.client.slot, loc_name))
                else:  # location name
                    hints = collect_hint_location_name(self.ctx, self.client.team, self.client.slot, hint_name)

            else:
                self.output(response)
                return False

        if hints:
            new_hints = set(hints) - self.ctx.hints[self.client.team, self.client.slot]
            old_hints = set(hints) - new_hints
            if old_hints:
                self.ctx.notify_hints(self.client.team, list(old_hints))
                if not new_hints:
                    self.output("Hint was previously used, no points deducted.")
            if new_hints:
                found_hints = [hint for hint in new_hints if hint.found]
                not_found_hints = [hint for hint in new_hints if not hint.found]

                if not not_found_hints:  # everything's been found, no need to pay
                    can_pay = 1000
                elif cost:
                    can_pay = int((points_available // cost) > 0)  # limit to 1 new hint per call
                else:
                    can_pay = 1000

                self.ctx.random.shuffle(not_found_hints)
                # By popular vote, make hints prefer non-local placements
                not_found_hints.sort(key=lambda hint: int(hint.receiving_player != hint.finding_player))

                hints = found_hints
                while can_pay > 0:
                    if not not_found_hints:
                        break
                    hint = not_found_hints.pop()
                    hints.append(hint)
                    can_pay -= 1
                    self.ctx.hints_used[self.client.team, self.client.slot] += 1
                    points_available = get_client_points(self.ctx, self.client)

                if not_found_hints:
                    if hints and cost and int((points_available // cost) == 0):
                        self.output(
                            f"There may be more hintables, however, you cannot afford to pay for any more. "
                            f" You have {points_available} and need at least "
                            f"{self.ctx.get_hint_cost(self.client.slot)}.")
                    elif hints:
                        self.output(
                            "There may be more hintables, you can rerun the command to find more.")
                    else:
                        self.output(f"You can't afford the hint. "
                                    f"You have {points_available} points and need at least "
                                    f"{self.ctx.get_hint_cost(self.client.slot)}.")
                self.ctx.notify_hints(self.client.team, hints)
                self.ctx.save()
                return True

        else:
            if points_available >= cost:
                if for_location:
                    self.output(f"Nothing found for recognized location name \"{hint_name}\". "
                                f"Location appears to not exist in this multiworld.")
                else:
                    self.output(f"Nothing found for recognized item name \"{hint_name}\". "
                                f"Item appears to not exist in this multiworld.")
            else:
                self.output(f"You can't afford the hint. "
                            f"You have {points_available} points and need at least "
                            f"{self.ctx.get_hint_cost(self.client.slot)}.")
            return False

    @mark_raw
    def _cmd_hint(self, item_name: str = "") -> bool:
        """Use !hint {item_name},
        for example !hint Lamp to get a spoiler peek for that item.
        If hint costs are on, this will only give you one new result,
        you can rerun the command to get more in that case."""
        return self.get_hints(item_name)

    @mark_raw
    def _cmd_hint_location(self, location: str = "") -> bool:
        """Use !hint_location {location_name},
        for example !hint_location atomic-bomb to get a spoiler peek for that location."""
        return self.get_hints(location, True)


def get_checked_checks(ctx: Context, team: int, slot: int) -> typing.List[int]:
    return ctx.locations.get_checked(ctx.location_checks, team, slot)


def get_missing_checks(ctx: Context, team: int, slot: int) -> typing.List[int]:
    return ctx.locations.get_missing(ctx.location_checks, team, slot)


def get_client_points(ctx: Context, client: Client) -> int:
    return (ctx.location_check_points * len(ctx.location_checks[client.team, client.slot]) -
            ctx.get_hint_cost(client.slot) * ctx.hints_used[client.team, client.slot])


def get_slot_points(ctx: Context, team: int, slot: int) -> int:
    return (ctx.location_check_points * len(ctx.location_checks[team, slot]) -
            ctx.get_hint_cost(slot) * ctx.hints_used[team, slot])


async def process_client_cmd(ctx: Context, client: Client, args: dict):
    try:
        cmd: str = args["cmd"]
    except:
        logging.exception(f"Could not get command from {args}")
        await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "cmd", "original_cmd": None,
                                      "text": f"Could not get command from {args} at `cmd`"}])
        raise

    if type(cmd) is not str:
        await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "cmd", "original_cmd": None,
                                      "text": f"Command should be str, got {type(cmd)}"}])
        return

    if cmd == 'Connect':
        if not args or 'password' not in args or type(args['password']) not in [str, type(None)] or \
                'game' not in args:
            await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments", 'text': 'Connect',
                                          "original_cmd": cmd}])
            return

        errors = set()
        if ctx.password and args['password'] != ctx.password:
            errors.add('InvalidPassword')

        if args['name'] not in ctx.connect_names:
            errors.add('InvalidSlot')
        else:
            team, slot = ctx.connect_names[args['name']]
            game = ctx.games[slot]
            ignore_game = ("TextOnly" in args["tags"] or "Tracker" in args["tags"]) and not args.get("game")
            if not ignore_game and args['game'] != game:
                errors.add('InvalidGame')
            minver = min_client_version if ignore_game else ctx.minimum_client_versions[slot]
            if minver > args['version']:
                errors.add('IncompatibleVersion')
            try:
                client.items_handling = args['items_handling']
            except (ValueError, TypeError):
                errors.add('InvalidItemsHandling')

        # only exact version match allowed
        if ctx.compatibility == 0 and args['version'] != version_tuple:
            errors.add('IncompatibleVersion')
        if errors:
            logging.info(f"A client connection was refused due to: {errors}, the sent connect information was {args}.")
            await ctx.send_msgs(client, [{"cmd": "ConnectionRefused", "errors": list(errors)}])
        else:
            team, slot = ctx.connect_names[args['name']]
            if client.auth and client.team is not None and client.slot in ctx.clients[client.team]:
                ctx.clients[team][slot].remove(client)  # re-auth, remove old entry
                if client.team != team or client.slot != slot:
                    client.auth = False  # swapping Team/Slot
            client.team = team
            client.slot = slot

            ctx.client_ids[client.team, client.slot] = args["uuid"]
            ctx.clients[team][slot].append(client)
            client.version = args['version']
            client.tags = args['tags']
            client.no_locations = 'TextOnly' in client.tags or 'Tracker' in client.tags
            connected_packet = {
                "cmd": "Connected",
                "team": client.team, "slot": client.slot,
                "players": ctx.get_players_package(),
                "missing_locations": get_missing_checks(ctx, team, slot),
                "checked_locations": get_checked_checks(ctx, team, slot),
                "slot_info": ctx.slot_info,
                "hint_points": get_slot_points(ctx, team, slot),
            }
            reply = [connected_packet]
            start_inventory = get_start_inventory(ctx, slot, client.remote_start_inventory)
            items = get_received_items(ctx, client.team, client.slot, client.remote_items)
            if (start_inventory or items) and not client.no_items:
                reply.append({"cmd": 'ReceivedItems', "index": 0, "items": start_inventory + items})
                client.send_index = len(start_inventory) + len(items)
            if not client.auth:  # if this was a Re-Connect, don't print to console
                client.auth = True
                await on_client_joined(ctx, client)
            if args.get("slot_data", True):
                connected_packet["slot_data"] = ctx.slot_data[client.slot]
            await ctx.send_msgs(client, reply)

    elif cmd == "GetDataPackage":
        exclusions = args.get("exclusions", [])
        if "games" in args:
            games = {name: game_data for name, game_data in ctx.gamespackage.items()
                     if name in set(args.get("games", []))}
            await ctx.send_msgs(client, [{"cmd": "DataPackage",
                                          "data": {"games": games}}])
        # TODO: remove exclusions behaviour around 0.5.0
        elif exclusions:
            exclusions = set(exclusions)
            games = {name: game_data for name, game_data in ctx.gamespackage.items()
                     if name not in exclusions}

            package = {"games": games}
            await ctx.send_msgs(client, [{"cmd": "DataPackage",
                                          "data": package}])

        else:
            await ctx.send_msgs(client, [{"cmd": "DataPackage",
                                          "data": {"games": ctx.gamespackage}}])

    elif client.auth:
        if cmd == "ConnectUpdate":
            if not args:
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments", 'text': cmd,
                                              "original_cmd": cmd}])
                return

            if args.get('items_handling', None) is not None and client.items_handling != args['items_handling']:
                try:
                    client.items_handling = args['items_handling']
                    start_inventory = get_start_inventory(ctx, client.slot, client.remote_start_inventory)
                    items = get_received_items(ctx, client.team, client.slot, client.remote_items)
                    if (items or start_inventory) and not client.no_items:
                        client.send_index = len(start_inventory) + len(items)
                        await ctx.send_msgs(client, [{"cmd": "ReceivedItems", "index": 0,
                                                      "items": start_inventory + items}])
                    else:
                        client.send_index = 0
                except (ValueError, TypeError) as err:
                    await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', 'type': 'arguments',
                                                  'text': f'Invalid items_handling: {err}',
                                                  'original_cmd': cmd}])
                    return

            if "tags" in args:
                old_tags = client.tags
                client.tags = args["tags"]
                if set(old_tags) != set(client.tags):
                    client.no_locations = 'TextOnly' in client.tags or 'Tracker' in client.tags
                    ctx.broadcast_text_all(
                        f"{ctx.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1}) has changed tags "
                        f"from {old_tags} to {client.tags}.",
                        {"type": "TagsChanged", "team": client.team, "slot": client.slot, "tags": client.tags})

        elif cmd == 'Sync':
            start_inventory = get_start_inventory(ctx, client.slot, client.remote_start_inventory)
            items = get_received_items(ctx, client.team, client.slot, client.remote_items)
            if (start_inventory or items) and not client.no_items:
                client.send_index = len(start_inventory) + len(items)
                await ctx.send_msgs(client, [{"cmd": "ReceivedItems", "index": 0,
                                              "items": start_inventory + items}])

        elif cmd == 'LocationChecks':
            if client.no_locations:
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "cmd",
                                              "text": "Trackers can't register new Location Checks",
                                              "original_cmd": cmd}])
            else:
                register_location_checks(ctx, client.team, client.slot, args["locations"])

        elif cmd == 'LocationScouts':
            locs = []
            create_as_hint: int = int(args.get("create_as_hint", 0))
            hints = []
            for location in args["locations"]:
                if type(location) is not int:
                    await ctx.send_msgs(client,
                                        [{'cmd': 'InvalidPacket', "type": "arguments", "text": 'LocationScouts',
                                          "original_cmd": cmd}])
                    return

                target_item, target_player, flags = ctx.locations[client.slot][location]
                if create_as_hint:
                    hints.extend(collect_hint_location_id(ctx, client.team, client.slot, location))
                locs.append(NetworkItem(target_item, location, target_player, flags))
            ctx.notify_hints(client.team, hints, only_new=create_as_hint == 2)
            if locs and create_as_hint:
                ctx.save()
            await ctx.send_msgs(client, [{'cmd': 'LocationInfo', 'locations': locs}])

        elif cmd == 'StatusUpdate':
            update_client_status(ctx, client, args["status"])

        elif cmd == 'Say':
            if "text" not in args or type(args["text"]) is not str or not args["text"].isprintable():
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments", "text": 'Say',
                                              "original_cmd": cmd}])
                return

            client.messageprocessor(args["text"])

        elif cmd == "Bounce":
            games = set(args.get("games", []))
            tags = set(args.get("tags", []))
            slots = set(args.get("slots", []))
            args["cmd"] = "Bounced"
            msg = ctx.dumper([args])

            for bounceclient in ctx.endpoints:
                if client.team == bounceclient.team and (ctx.games[bounceclient.slot] in games or
                                                         set(bounceclient.tags) & tags or
                                                         bounceclient.slot in slots):
                    await ctx.send_encoded_msgs(bounceclient, msg)

        elif cmd == "Get":
            if "keys" not in args or type(args["keys"]) != list:
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments",
                                              "text": 'Retrieve', "original_cmd": cmd}])
                return
            args["cmd"] = "Retrieved"
            keys = args["keys"]
            args["keys"] = {
                key: ctx.read_data.get(key[6:], lambda: None)() if key.startswith("_read_") else
                     ctx.stored_data.get(key, None)
                for key in keys
            }
            await ctx.send_msgs(client, [args])

        elif cmd == "Set":
            if "key" not in args or args["key"].startswith("_read_") or \
                    "operations" not in args or not type(args["operations"]) == list:
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments",
                                              "text": 'Set', "original_cmd": cmd}])
                return
            args["cmd"] = "SetReply"
            value = ctx.stored_data.get(args["key"], args.get("default", 0))
            args["original_value"] = copy.copy(value)
            for operation in args["operations"]:
                func = modify_functions[operation["operation"]]
                value = func(value, operation["value"])
            ctx.stored_data[args["key"]] = args["value"] = value
            targets = set(ctx.stored_data_notification_clients[args["key"]])
            if args.get("want_reply", True):
                targets.add(client)
            if targets:
                ctx.broadcast(targets, [args])
            ctx.save()

        elif cmd == "SetNotify":
            if "keys" not in args or type(args["keys"]) != list:
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments",
                                              "text": 'SetNotify', "original_cmd": cmd}])
                return
            for key in args["keys"]:
                ctx.stored_data_notification_clients[key].add(client)


def update_client_status(ctx: Context, client: Client, new_status: ClientStatus):
    current = ctx.client_game_state[client.team, client.slot]
    if current != ClientStatus.CLIENT_GOAL:  # can't undo goal completion
        if new_status == ClientStatus.CLIENT_GOAL:
            ctx.on_goal_achieved(client)

        ctx.client_game_state[client.team, client.slot] = new_status
        ctx.save()


class ServerCommandProcessor(CommonCommandProcessor):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        super(ServerCommandProcessor, self).__init__()

    def output(self, text: str):
        if self.client:
            self.ctx.notify_client(self.client, text, {"type": "AdminCommandResult"})
        super(ServerCommandProcessor, self).output(text)

    def default(self, raw: str):
        self.ctx.broadcast_text_all('[Server]: ' + raw, {"type": "ServerChat", "message": raw})

    def _cmd_save(self) -> bool:
        """Save current state to multidata"""
        if self.ctx.saving:
            self.ctx.save(True)
            self.output("Game saved")
            return True
        else:
            self.output("Saving is disabled.")
            return False

    def _cmd_players(self) -> bool:
        """Get information about connected players"""
        self.output(get_players_string(self.ctx))
        return True

    def _cmd_status(self, tag: str = "") -> bool:
        """Get status information about teams.
        Optionally mention a Tag name and get information on who has that Tag.
        For example: DeathLink or EnergyLink."""
        for team in self.ctx.clients:
            self.output(get_status_string(self.ctx, team, tag))
        return True

    def _cmd_exit(self) -> bool:
        """Shutdown the server"""
        self.ctx.server.ws_server.close()
        if self.ctx.shutdown_task:
            self.ctx.shutdown_task.cancel()
        self.ctx.exit_event.set()
        return True

    @mark_raw
    def _cmd_alias(self, player_name_then_alias_name):
        """Set a player's alias, by listing their base name and then their intended alias."""
        player_name, alias_name = player_name_then_alias_name.split(" ", 1)
        player_name, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            for (team, slot), name in self.ctx.player_names.items():
                if name == player_name:
                    if alias_name:
                        alias_name = alias_name.strip()[:15]
                        self.ctx.name_aliases[team, slot] = alias_name
                        self.output(f"Named {player_name} as {alias_name}")
                        update_aliases(self.ctx, team)
                        self.ctx.save()
                        return True
                    else:
                        del (self.ctx.name_aliases[team, slot])
                        self.output(f"Removed Alias for {player_name}")
                        update_aliases(self.ctx, team)
                        self.ctx.save()
                        return True
        else:
            self.output(response)
            return False

    def resolve_player(self, input_name: str) -> typing.Optional[typing.Tuple[int, int, str]]:
        """ returns (team, slot, player name) """
        # TODO: clean up once we disallow multidata < 0.3.6, which has CI unique names
        # first match case
        for (team, slot), name in self.ctx.player_names.items():
            if name == input_name:
                return team, slot, name

        # if no case-sensitive match, then match without case only if there's only 1 match
        input_lower = input_name.lower()
        match: typing.Optional[typing.Tuple[int, int, str]] = None
        for (team, slot), name in self.ctx.player_names.items():
            lowered = name.lower()
            if lowered == input_lower:
                if match:
                    return None  # ambiguous input_name
                match = (team, slot, name)
        return match

    @mark_raw
    def _cmd_collect(self, player_name: str) -> bool:
        """Send out the remaining items to player."""
        player = self.resolve_player(player_name)
        if player:
            team, slot, _ = player
            collect_player(self.ctx, team, slot)
            return True

        self.output(f"Could not find player {player_name} to collect")
        return False

    @mark_raw
    def _cmd_release(self, player_name: str) -> bool:
        """Send out the remaining items from a player to their intended recipients."""
        player = self.resolve_player(player_name)
        if player:
            team, slot, _ = player
            release_player(self.ctx, team, slot)
            return True

        self.output(f"Could not find player {player_name} to release")
        return False

    @mark_raw
    def _cmd_allow_release(self, player_name: str) -> bool:
        """Allow the specified player to use the !release command."""
        player = self.resolve_player(player_name)
        if player:
            team, slot, name = player
            self.ctx.allow_releases[(team, slot)] = True
            self.output(f"Player {name} is now allowed to use the !release command at any time.")
            return True

        self.output(f"Could not find player {player_name} to allow the !release command for.")
        return False

    @mark_raw
    def _cmd_forbid_release(self, player_name: str) -> bool:
        """"Disallow the specified player from using the !release command."""
        player = self.resolve_player(player_name)
        if player:
            team, slot, name = player
            self.ctx.allow_releases[(team, slot)] = False
            self.output(f"Player {name} has to follow the server restrictions on use of the !release command.")
            return True

        self.output(f"Could not find player {player_name} to forbid the !release command for.")
        return False

    def _cmd_send_multiple(self, amount: typing.Union[int, str], player_name: str, *item_name: str) -> bool:
        """Sends multiples of an item to the specified player"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            team, slot = self.ctx.player_name_lookup[seeked_player]
            item_name = " ".join(item_name)
            names = self.ctx.item_names_for_game(self.ctx.games[slot])
            item_name, usable, response = get_intended_text(item_name, names)
            if usable:
                amount: int = int(amount)
                new_items = [NetworkItem(names[item_name], -1, 0) for _ in range(int(amount))]
                send_items_to(self.ctx, team, slot, *new_items)

                send_new_items(self.ctx)
                self.ctx.broadcast_text_all(
                    'Cheat console: sending ' + ('' if amount == 1 else f'{amount} of ') +
                    f'"{item_name}" to {self.ctx.get_aliased_name(team, slot)}')
                return True
            else:
                self.output(response)
                return False
        else:
            self.output(response)
            return False

    def _cmd_send(self, player_name: str, *item_name: str) -> bool:
        """Sends an item to the specified player"""
        return self._cmd_send_multiple(1, player_name, *item_name)

    def _cmd_send_location(self, player_name: str, *location_name: str) -> bool:
        """Send out item from a player's location as though they checked it"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            team, slot = self.ctx.player_name_lookup[seeked_player]
            game = self.ctx.games[slot]
            full_name = " ".join(location_name)

            if full_name.isnumeric():
                location, usable, response = int(full_name), True, None
            elif self.ctx.location_names_for_game(game) is not None:
                location, usable, response = get_intended_text(full_name, self.ctx.location_names_for_game(game))
            else:
                self.output("Can't look up location for unknown game. Send by ID instead.")
                return False

            if usable:
                if isinstance(location, int):
                    register_location_checks(self.ctx, team, slot, [location])
                else:
                    seeked_location: int = self.ctx.location_names_for_game(self.ctx.games[slot])[location]
                    register_location_checks(self.ctx, team, slot, [seeked_location])
                return True
            else:
                self.output(response)
                return False

        else:
            self.output(response)
            return False

    def _cmd_hint(self, player_name: str, *item_name: str) -> bool:
        """Send out a hint for a player's item to their team"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            team, slot = self.ctx.player_name_lookup[seeked_player]
            game = self.ctx.games[slot]
            full_name = " ".join(item_name)

            if full_name.isnumeric():
                item, usable, response = int(full_name), True, None
            elif game in self.ctx.all_item_and_group_names:
                item, usable, response = get_intended_text(full_name, self.ctx.all_item_and_group_names[game])
            else:
                self.output("Can't look up item for unknown game. Hint for ID instead.")
                return False

            if usable:
                if game in self.ctx.item_name_groups and item in self.ctx.item_name_groups[game]:
                    hints = []
                    for item_name_from_group in self.ctx.item_name_groups[game][item]:
                        if item_name_from_group in self.ctx.item_names_for_game(game):  # ensure item has an ID
                            hints.extend(collect_hints(self.ctx, team, slot, item_name_from_group))
                else:  # item name or id
                    hints = collect_hints(self.ctx, team, slot, item)

                if hints:
                    self.ctx.notify_hints(team, hints)

                else:
                    self.output("No hints found.")
                return True
            else:
                self.output(response)
                return False

        else:
            self.output(response)
            return False

    def _cmd_hint_location(self, player_name: str, *location_name: str) -> bool:
        """Send out a hint for a player's location to their team"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            team, slot = self.ctx.player_name_lookup[seeked_player]
            game = self.ctx.games[slot]
            full_name = " ".join(location_name)

            if full_name.isnumeric():
                location, usable, response = int(full_name), True, None
            elif self.ctx.location_names_for_game(game) is not None:
                location, usable, response = get_intended_text(full_name, self.ctx.location_names_for_game(game))
            else:
                self.output("Can't look up location for unknown game. Hint for ID instead.")
                return False

            if usable:
                if isinstance(location, int):
                    hints = collect_hint_location_id(self.ctx, team, slot, location)
                else:
                    hints = collect_hint_location_name(self.ctx, team, slot, location)
                if hints:
                    self.ctx.notify_hints(team, hints)
                else:
                    self.output("No hints found.")
                return True
            else:
                self.output(response)
                return False

        else:
            self.output(response)
            return False

    def _cmd_option(self, option_name: str, option: str):
        """Set options for the server."""

        attrtype = self.ctx.simple_options.get(option_name, None)
        if attrtype:
            if attrtype == bool:
                def attrtype(input_text: str):
                    return input_text.lower() not in {"off", "0", "false", "none", "null", "no"}
            elif attrtype == str and option_name.endswith("password"):
                def attrtype(input_text: str):
                    if input_text.lower() in {"null", "none", '""', "''"}:
                        return None
                    return input_text
            setattr(self.ctx, option_name, attrtype(option))
            self.output(f"Set option {option_name} to {getattr(self.ctx, option_name)}")
            if option_name in {"release_mode", "remaining_mode", "collect_mode"}:
                self.ctx.broadcast_all([{"cmd": "RoomUpdate", 'permissions': get_permissions(self.ctx)}])
            elif option_name in {"hint_cost", "location_check_points"}:
                self.ctx.broadcast_all([{"cmd": "RoomUpdate", option_name: getattr(self.ctx, option_name)}])
            return True
        else:
            known = (f"{option}:{otype}" for option, otype in self.ctx.simple_options.items())
            self.output(f"Unrecognized Option {option_name}, known: "
                        f"{', '.join(known)}")
            return False


async def console(ctx: Context):
    import sys
    queue = asyncio.Queue()
    worker = Utils.stream_input(sys.stdin, queue)
    while not ctx.exit_event.is_set():
        try:
            # I don't get why this while loop is needed. Works fine without it on clients,
            # but the queue.get() for server never fulfills if the queue is empty when entering the await.
            while queue.qsize() == 0:
                await asyncio.sleep(0.05)
                if not worker.is_alive():
                    return
            input_text = await queue.get()
            queue.task_done()
            ctx.commandprocessor(input_text)
        except:
            import traceback
            traceback.print_exc()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    defaults = Utils.get_options()["server_options"].as_dict()
    parser.add_argument('multidata', nargs="?", default=defaults["multidata"])
    parser.add_argument('--host', default=defaults["host"])
    parser.add_argument('--port', default=defaults["port"], type=int)
    parser.add_argument('--server_password', default=defaults["server_password"])
    parser.add_argument('--password', default=defaults["password"])
    parser.add_argument('--savefile', default=defaults["savefile"])
    parser.add_argument('--disable_save', default=defaults["disable_save"], action='store_true')
    parser.add_argument('--cert', help="Path to a SSL Certificate for encryption.")
    parser.add_argument('--cert_key', help="Path to SSL Certificate Key file")
    parser.add_argument('--loglevel', default=defaults["loglevel"],
                        choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('--location_check_points', default=defaults["location_check_points"], type=int)
    parser.add_argument('--hint_cost', default=defaults["hint_cost"], type=int)
    parser.add_argument('--disable_item_cheat', default=defaults["disable_item_cheat"], action='store_true')
    parser.add_argument('--release_mode', default=defaults["release_mode"], nargs='?',
                        choices=['auto', 'enabled', 'disabled', "goal", "auto-enabled"], help='''\
                             Select !release Accessibility. (default: %(default)s)
                             auto:     Automatic "release" on goal completion
                             enabled:  !release is always available
                             disabled: !release is never available
                             goal:     !release can be used after goal completion
                             auto-enabled: !release is available and automatically triggered on goal completion
                             ''')
    parser.add_argument('--collect_mode', default=defaults["collect_mode"], nargs='?',
                        choices=['auto', 'enabled', 'disabled', "goal", "auto-enabled"], help='''\
                             Select !collect Accessibility. (default: %(default)s)
                             auto:     Automatic "collect" on goal completion
                             enabled:  !collect is always available
                             disabled: !collect is never available
                             goal:     !collect can be used after goal completion
                             auto-enabled: !collect is available and automatically triggered on goal completion
                             ''')
    parser.add_argument('--remaining_mode', default=defaults["remaining_mode"], nargs='?',
                        choices=['enabled', 'disabled', "goal"], help='''\
                             Select !remaining Accessibility. (default: %(default)s)
                             enabled:  !remaining is always available
                             disabled: !remaining is never available
                             goal:     !remaining can be used after goal completion
                             ''')
    parser.add_argument('--auto_shutdown', default=defaults["auto_shutdown"], type=int,
                        help="automatically shut down the server after this many minutes without new location checks. "
                             "0 to keep running. Not yet implemented.")
    parser.add_argument('--use_embedded_options', action="store_true",
                        help='retrieve release, remaining and hint options from the multidata file,'
                             ' instead of host.yaml')
    parser.add_argument('--compatibility', default=defaults["compatibility"], type=int,
                        help="""
    #2 -> recommended for casual/cooperative play, attempt to be compatible with everything across all versions
    #1 -> recommended for friendly racing, tries to block third party clients
    #0 -> recommended for tournaments to force a level playing field, only allow an exact version match
    """)
    parser.add_argument('--log_network', default=defaults["log_network"], action="store_true")
    args = parser.parse_args()
    return args


async def auto_shutdown(ctx, to_cancel=None):
    await asyncio.sleep(ctx.auto_shutdown)
    while not ctx.exit_event.is_set():
        if not ctx.client_activity_timers.values():
            ctx.server.ws_server.close()
            ctx.exit_event.set()
            if to_cancel:
                for task in to_cancel:
                    task.cancel()
            logging.info("Shutting down due to inactivity.")
        else:
            newest_activity = max(ctx.client_activity_timers.values())
            delta = datetime.datetime.now(datetime.timezone.utc) - newest_activity
            seconds = ctx.auto_shutdown - delta.total_seconds()
            if seconds < 0:
                ctx.server.ws_server.close()
                ctx.exit_event.set()
                if to_cancel:
                    for task in to_cancel:
                        task.cancel()
                logging.info("Shutting down due to inactivity.")
            else:
                await asyncio.sleep(seconds)


def load_server_cert(path: str, cert_key: typing.Optional[str]) -> "ssl.SSLContext":
    import ssl
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ssl_context.load_default_certs()
    ssl_context.load_cert_chain(path, cert_key if cert_key else path)
    return ssl_context


async def main(args: argparse.Namespace):
    Utils.init_logging("Server", loglevel=args.loglevel.lower())

    ctx = Context(args.host, args.port, args.server_password, args.password, args.location_check_points,
                  args.hint_cost, not args.disable_item_cheat, args.release_mode, args.collect_mode,
                  args.remaining_mode,
                  args.auto_shutdown, args.compatibility, args.log_network)
    data_filename = args.multidata

    if not data_filename:
        try:
            filetypes = (("Multiworld data", (".archipelago", ".zip")),)
            data_filename = Utils.open_filename("Select multiworld data", filetypes)

        except Exception as e:
            if isinstance(e, ImportError) or (e.__class__.__name__ == "TclError" and "no display" in str(e)):
                if not isinstance(e, ImportError):
                    logging.error(f"Failed to load tkinter ({e})")
                logging.info("Pass a multidata filename on command line to run headless.")
                # when cx_Freeze'd the built-in exit is not available, so we import sys.exit instead
                import sys
                sys.exit(1)
            raise

        if not data_filename:
            logging.info("No file selected. Exiting.")
            import sys
            sys.exit(1)

    try:
        ctx.load(data_filename, args.use_embedded_options)

    except Exception as e:
        logging.exception(f"Failed to read multiworld data ({e})")
        raise

    ctx.init_save(not args.disable_save)

    ssl_context = load_server_cert(args.cert, args.cert_key) if args.cert else None

    ctx.server = websockets.serve(functools.partial(server, ctx=ctx), host=ctx.host, port=ctx.port, ssl=ssl_context)
    ip = args.host if args.host else Utils.get_public_ipv4()
    logging.info('Hosting game at %s:%d (%s)' % (ip, ctx.port,
                                                 'No password' if not ctx.password else 'Password: %s' % ctx.password))

    await ctx.server
    console_task = asyncio.create_task(console(ctx))
    if ctx.auto_shutdown:
        ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, [console_task]))
    await ctx.exit_event.wait()
    console_task.cancel()
    if ctx.shutdown_task:
        await ctx.shutdown_task


client_message_processor = ClientMessageProcessor

if __name__ == '__main__':
    try:
        asyncio.run(main(parse_args()))
    except asyncio.exceptions.CancelledError:
        pass
