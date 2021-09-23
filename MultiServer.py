from __future__ import annotations

import argparse
import asyncio
import functools
import logging
import zlib
import collections
import typing
import inspect
import weakref
import datetime
import threading
import random
import pickle

import ModuleUpdate
import NetUtils

ModuleUpdate.update()

import websockets
import colorama
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout
from fuzzywuzzy import process as fuzzy_process

from worlds.AutoWorld import AutoWorldRegister
proxy_worlds = {name: world(None, 0) for name, world in AutoWorldRegister.world_types.items()}
from worlds import network_data_package, lookup_any_item_id_to_name, lookup_any_location_id_to_name
import Utils
from Utils import get_item_name_from_id, get_location_name_from_id, \
    version_tuple, restricted_loads, Version
from NetUtils import Endpoint, ClientStatus, NetworkItem, decode, encode, NetworkPlayer

colorama.init()


class Client(Endpoint):
    version = Version(0, 0, 0)
    tags: typing.List[str] = []

    def __init__(self, socket: websockets.WebSocketServerProtocol, ctx: Context):
        super().__init__(socket)
        self.auth = False
        self.name = None
        self.team = None
        self.slot = None
        self.send_index = 0
        self.tags = []
        self.messageprocessor = client_message_processor(ctx, self)
        self.ctx = weakref.ref(ctx)


team_slot = typing.Tuple[int, int]


class Context:
    dumper = staticmethod(encode)
    loader = staticmethod(decode)

    simple_options = {"hint_cost": int,
                      "location_check_points": int,
                      "server_password": str,
                      "password": str,
                      "forfeit_mode": str,
                      "remaining_mode": str,
                      "item_cheat": bool,
                      "compatibility": int}

    def __init__(self, host: str, port: int, server_password: str, password: str, location_check_points: int,
                 hint_cost: int, item_cheat: bool, forfeit_mode: str = "disabled", remaining_mode: str = "disabled",
                 auto_shutdown: typing.SupportsFloat = 0, compatibility: int = 2, log_network: bool = False):
        super(Context, self).__init__()
        self.log_network = log_network
        self.endpoints = []
        self.compatibility: int = compatibility
        self.shutdown_task = None
        self.data_filename = None
        self.save_filename = None
        self.saving = False
        self.player_names: typing.Dict[team_slot, str] = {}
        self.player_name_lookup: typing.Dict[str, team_slot] = {}
        self.connect_names = {}  # names of slots clients can connect to
        self.allow_forfeits = {}
        self.remote_items = set()
        self.remote_start_inventory = set()
        self.locations: typing.Dict[int, typing.Dict[int, typing.Tuple[int, int]]] = {}
        self.host = host
        self.port = port
        self.server_password = server_password
        self.password = password
        self.server = None
        self.countdown_timer = 0
        self.received_items = {}
        self.name_aliases: typing.Dict[team_slot, str] = {}
        self.location_checks = collections.defaultdict(set)
        self.hint_cost = hint_cost
        self.location_check_points = location_check_points
        self.hints_used = collections.defaultdict(int)
        self.hints: typing.Dict[team_slot, typing.Set[NetUtils.Hint]] = collections.defaultdict(set)
        self.forfeit_mode: str = forfeit_mode
        self.remaining_mode: str = remaining_mode
        self.item_cheat = item_cheat
        self.running = True
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
        self.minimum_client_versions: typing.Dict[int, Utils.Version] = {}
        self.seed_name = ""
        self.random = random.Random()

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
        else:
            if self.log_network:
                logging.info(f"Outgoing broadcast: {msg}")
            return True

    def broadcast_all(self, msgs):
        msgs = self.dumper(msgs)
        endpoints = (endpoint for endpoint in self.endpoints if endpoint.auth)
        asyncio.create_task(self.broadcast_send_encoded_msgs(endpoints, msgs))

    def broadcast_team(self, team: int, msgs):
        msgs = self.dumper(msgs)
        endpoints = (endpoint for endpoint in self.endpoints if endpoint.auth and endpoint.team == team)
        asyncio.create_task(self.broadcast_send_encoded_msgs(endpoints, msgs))

    def broadcast(self, endpoints: typing.Iterable[Endpoint], msgs):
        msgs = self.dumper(msgs)
        asyncio.create_task(self.broadcast_send_encoded_msgs(endpoints, msgs))

    async def disconnect(self, endpoint):
        if endpoint in self.endpoints:
            self.endpoints.remove(endpoint)
        await on_client_disconnected(self, endpoint)

    # text

    def notify_all(self, text):
        logging.info("Notice (all): %s" % text)
        self.broadcast_all([{"cmd": "Print", "text": text}])

    def notify_client(self, client: Client, text: str):
        if not client.auth:
            return
        logging.info("Notice (Player %s in team %d): %s" % (client.name, client.team + 1, text))
        asyncio.create_task(self.send_msgs(client, [{"cmd": "Print", "text": text}]))

    def notify_client_multiple(self, client: Client, texts: typing.List[str]):
        if not client.auth:
            return
        asyncio.create_task(self.send_msgs(client, [{"cmd": "Print", "text": text} for text in texts]))

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

        self._load(self._decompress(data), use_embedded_server_options)
        self.data_filename = multidatapath

    @staticmethod
    def _decompress(data: bytes) -> dict:
        format_version = data[0]
        if format_version != 1:
            raise Exception("Incompatible multidata.")
        return restricted_loads(zlib.decompress(data[1:]))

    def _load(self, decoded_obj: dict, use_embedded_server_options: bool):

        mdata_ver = decoded_obj["minimum_versions"]["server"]
        if mdata_ver > Utils.version_tuple:
            raise RuntimeError(f"Supplied Multidata (.archipelago) requires a server of at least version {mdata_ver},"
                               f"however this server is of version {Utils.version_tuple}")
        clients_ver = decoded_obj["minimum_versions"].get("clients", {})
        self.minimum_client_versions = {}
        for player, version in clients_ver.items():
            self.minimum_client_versions[player] = Utils.Version(*version)

        for team, names in enumerate(decoded_obj['names']):
            for player, name in enumerate(names, 1):
                self.player_names[team, player] = name
                self.player_name_lookup[name] = team, player
        self.seed_name = decoded_obj["seed_name"]
        self.random.seed(self.seed_name)
        self.connect_names = decoded_obj['connect_names']
        self.remote_items = decoded_obj['remote_items']
        self.remote_start_inventory = decoded_obj.get('remote_start_inventory', decoded_obj['remote_items'])
        self.locations = decoded_obj['locations']
        self.slot_data = decoded_obj['slot_data']
        self.er_hint_data = {int(player): {int(address): name for address, name in loc_data.items()}
                             for player, loc_data in decoded_obj["er_hint_data"].items()}
        self.games = decoded_obj["games"]
        # award remote-items start inventory:
        for team in range(len(decoded_obj['names'])):
            for slot, item_codes in decoded_obj["precollected_items"].items():
                if slot in self.remote_start_inventory:
                    self.received_items[team, slot] = [NetworkItem(item_code, -2, 0) for item_code in item_codes]
            for slot, hints in decoded_obj["precollected_hints"].items():
                self.hints[team, slot].update(hints)
        if use_embedded_server_options:
            server_options = decoded_obj.get("server_options", {})
            self._set_options(server_options)

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
                self.save_filename = name + '.apsave' if ext.lower() in ('.archipelago','.zip') \
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
                import time
                while self.running:
                    time.sleep(self.auto_save_interval)
                    if self.save_dirty:
                        logging.debug("Saving via thread.")
                        self.save_dirty = False
                        self._save()

            self.auto_saver_thread = threading.Thread(target=save_regularly, daemon=True)
            self.auto_saver_thread.start()

            import atexit
            atexit.register(self._save, True)  # make sure we save on exit too

    def get_save(self) -> dict:
        self.recheck_hints()
        d = {
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
            "random_state": self.random.getstate()
        }

        return d

    def set_save(self, savedata: dict):
        if self.connect_names != savedata["connect_names"]:
            raise Exception("This savegame does not appear to match the loaded multiworld.")
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
        if "random_state" in savedata:
            self.random.setstate(savedata["random_state"])
        logging.info(f'Loaded save file with {sum([len(p) for p in self.received_items.values()])} received items '
                     f'for {len(self.received_items)} players')

    # rest

    def get_hint_cost(self, slot):
        if self.hint_cost:
            return max(0, int(self.hint_cost * 0.01 * len(self.locations[slot])))
        return 0

    def recheck_hints(self):
        for team, slot in self.hints:
            self.hints[team, slot] = {
                hint.re_check(self, team) for hint in
                self.hints[team, slot]
            }

    def get_players_package(self):
        return [NetworkPlayer(t, p, self.get_aliased_name(t, p), n) for (t, p), n in self.player_names.items()]

    def _set_options(self, server_options: dict):
        for key, value in server_options.items():
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


def notify_hints(ctx: Context, team: int, hints: typing.List[NetUtils.Hint]):
    concerns = collections.defaultdict(list)
    for hint in hints:
        net_msg = hint.as_network_message()
        concerns[hint.receiving_player].append(net_msg)
        if not hint.local:
            concerns[hint.finding_player].append(net_msg)
    for text in (format_hint(ctx, team, hint) for hint in hints):
        logging.info("Notice (Team #%d): %s" % (team + 1, text))

    for client in ctx.endpoints:
        if client.auth and client.team == team:
            client_hints = concerns[client.slot]
            if client_hints:
                asyncio.create_task(ctx.send_msgs(client, client_hints))


def update_aliases(ctx: Context, team: int, client: typing.Optional[Client] = None):
    cmd = ctx.dumper([{"cmd": "RoomUpdate",
                       "players": ctx.get_players_package()}])
    if client is None:
        for client in ctx.endpoints:
            if client.team == team and client.auth:
                asyncio.create_task(ctx.send_encoded_msgs(client, cmd))
    else:
        asyncio.create_task(ctx.send_encoded_msgs(client, cmd))


async def server(websocket, path, ctx: Context):
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
    await ctx.send_msgs(client, [{
        'cmd': 'RoomInfo',
        'password': ctx.password is not None,
        'players': [
            NetworkPlayer(client.team, client.slot, ctx.name_aliases.get((client.team, client.slot), client.name),
                          client.name) for client
            in ctx.endpoints if client.auth],
        # tags are for additional features in the communication.
        # Name them by feature or fork, as you feel is appropriate.
        'tags': ctx.tags,
        'version': Utils.version_tuple,
        'forfeit_mode': ctx.forfeit_mode,
        'remaining_mode': ctx.remaining_mode,
        'hint_cost': ctx.hint_cost,
        'location_check_points': ctx.location_check_points,
        'datapackage_version': network_data_package["version"],
        'datapackage_versions': {game: game_data["version"] for game, game_data
                                 in network_data_package["games"].items()},
        'seed_name': ctx.seed_name
    }])


async def on_client_disconnected(ctx: Context, client: Client):
    if client.auth:
        await on_client_left(ctx, client)


async def on_client_joined(ctx: Context, client: Client):
    update_client_status(ctx, client, ClientStatus.CLIENT_CONNECTED)
    version_str = '.'.join(str(x) for x in client.version)
    ctx.notify_all(
        f"{ctx.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1}) "
        f"playing {ctx.games[client.slot]} has joined. "
        f"Client({version_str}), {client.tags}).")
    # TODO: remove with 0.2
    if client.version < Version(0, 1, 7):
        ctx.notify_client(client,
                          "Warning: Your client's datapackage handling may be unsupported soon. (Version < 0.1.7)")

    ctx.client_connection_timers[client.team, client.slot] = datetime.datetime.now(datetime.timezone.utc)


async def on_client_left(ctx: Context, client: Client):
    update_client_status(ctx, client, ClientStatus.CLIENT_UNKNOWN)
    ctx.notify_all(
        "%s (Team #%d) has left the game" % (ctx.get_aliased_name(client.team, client.slot), client.team + 1))
    ctx.client_connection_timers[client.team, client.slot] = datetime.datetime.now(datetime.timezone.utc)


async def countdown(ctx: Context, timer):
    ctx.notify_all(f'[Server]: Starting countdown of {timer}s')
    if ctx.countdown_timer:
        ctx.countdown_timer = timer  # timer is already running, set it to a different time
    else:
        ctx.countdown_timer = timer
        while ctx.countdown_timer > 0:
            ctx.notify_all(f'[Server]: {ctx.countdown_timer}')
            ctx.countdown_timer -= 1
            await asyncio.sleep(1)
        ctx.notify_all(f'[Server]: GO')
        ctx.countdown_timer = 0


def get_players_string(ctx: Context):
    auth_clients = {(c.team, c.slot) for c in ctx.endpoints if c.auth}

    player_names = sorted(ctx.player_names.keys())
    current_team = -1
    text = ''
    for team, slot in player_names:
        player_name = ctx.player_names[team, slot]
        if team != current_team:
            text += f':: Team #{team + 1}: '
            current_team = team
        if (team, slot) in auth_clients:
            text += f'{player_name} '
        else:
            text += f'({player_name}) '
    return f'{len(auth_clients)} players of {len(ctx.player_names)} connected ' + text[:-1]


def get_received_items(ctx: Context, team: int, player: int) -> typing.List[NetworkItem]:
    return ctx.received_items.setdefault((team, player), [])


def send_new_items(ctx: Context):
    for client in ctx.endpoints:
        if client.auth:  # can't send to disconnected client
            items = get_received_items(ctx, client.team, client.slot)
            if len(items) > client.send_index:
                asyncio.create_task(ctx.send_msgs(client, [{
                    "cmd": "ReceivedItems",
                    "index": client.send_index,
                    "items": items[client.send_index:]}]))
                client.send_index = len(items)


def forfeit_player(ctx: Context, team: int, slot: int):
    # register any locations that are in the multidata
    all_locations = set(ctx.locations[slot])
    ctx.notify_all("%s (Team #%d) has forfeited" % (ctx.player_names[(team, slot)], team + 1))
    register_location_checks(ctx, team, slot, all_locations)


def get_remaining(ctx: Context, team: int, slot: int) -> typing.List[int]:
    items = []
    for location_id in ctx.locations[slot]:
        if location_id not in ctx.location_checks[team, slot]:
            items.append(ctx.locations[slot][location_id][0])  # item ID
    return sorted(items)


def register_location_checks(ctx: Context, team: int, slot: int, locations: typing.Iterable[int]):
    new_locations = set(locations) - ctx.location_checks[team, slot]
    if new_locations:
        ctx.client_activity_timers[team, slot] = datetime.datetime.now(datetime.timezone.utc)
        for location in new_locations:
            if location in ctx.locations[slot]:
                item_id, target_player = ctx.locations[slot][location]
                new_item = NetworkItem(item_id, location, slot)
                if target_player != slot or slot in ctx.remote_items:
                    get_received_items(ctx, team, target_player).append(new_item)

                logging.info('(Team #%d) %s sent %s to %s (%s)' % (
                    team + 1, ctx.player_names[(team, slot)], get_item_name_from_id(item_id),
                    ctx.player_names[(team, target_player)], get_location_name_from_id(location)))
                info_text = json_format_send_event(new_item, target_player)
                ctx.broadcast_team(team, [info_text])

        ctx.location_checks[team, slot] |= new_locations
        send_new_items(ctx)
        for client in ctx.endpoints:
            if client.team == team and client.slot == slot:
                asyncio.create_task(ctx.send_msgs(client, [{"cmd": "RoomUpdate",
                                                            "hint_points": get_client_points(ctx, client)}]))

        ctx.save()


def notify_team(ctx: Context, team: int, text: str):
    logging.info("Notice (Team #%d): %s" % (team + 1, text))
    ctx.broadcast_team(team, [['Print', {"text": text}]])


def collect_hints(ctx: Context, team: int, slot: int, item: str) -> typing.List[NetUtils.Hint]:
    hints = []
    seeked_item_id = proxy_worlds[ctx.games[slot]].item_name_to_id[item]
    for finding_player, check_data in ctx.locations.items():
        for location_id, result in check_data.items():
            item_id, receiving_player = result
            if receiving_player == slot and item_id == seeked_item_id:
                found = location_id in ctx.location_checks[team, finding_player]
                entrance = ctx.er_hint_data.get(finding_player, {}).get(location_id, "")
                hints.append(NetUtils.Hint(receiving_player, finding_player, location_id, item_id, found, entrance))

    return hints


def collect_hints_location(ctx: Context, team: int, slot: int, location: str) -> typing.List[NetUtils.Hint]:
    seeked_location: int = proxy_worlds[ctx.games[slot]].location_name_to_id[location]
    item_id, receiving_player = ctx.locations[slot].get(seeked_location, (None, None))
    if item_id:
        found = seeked_location in ctx.location_checks[team, slot]
        entrance = ctx.er_hint_data.get(slot, {}).get(seeked_location, "")
        return [NetUtils.Hint(receiving_player, slot, seeked_location, item_id, found, entrance)]
    return []


def format_hint(ctx: Context, team: int, hint: NetUtils.Hint) -> str:
    text = f"[Hint]: {ctx.player_names[team, hint.receiving_player]}'s " \
           f"{lookup_any_item_id_to_name[hint.item]} is " \
           f"at {get_location_name_from_id(hint.location)} " \
           f"in {ctx.player_names[team, hint.finding_player]}'s World"

    if hint.entrance:
        text += f" at {hint.entrance}"
    return text + (". (found)" if hint.found else ".")


def json_format_send_event(net_item: NetworkItem, receiving_player: int):
    parts = []
    NetUtils.add_json_text(parts, net_item.player, type=NetUtils.JSONTypes.player_id)
    if net_item.player == receiving_player:
        NetUtils.add_json_text(parts, " found their ")
        NetUtils.add_json_text(parts, net_item.item, type=NetUtils.JSONTypes.item_id)
    else:
        NetUtils.add_json_text(parts, " sent ")
        NetUtils.add_json_text(parts, net_item.item, type=NetUtils.JSONTypes.item_id)
        NetUtils.add_json_text(parts, " to ")
        NetUtils.add_json_text(parts, receiving_player, type=NetUtils.JSONTypes.player_id)

    NetUtils.add_json_text(parts, " (")
    NetUtils.add_json_text(parts, net_item.location, type=NetUtils.JSONTypes.location_id)
    NetUtils.add_json_text(parts, ")")

    return {"cmd": "PrintJSON", "data": parts, "type": "ItemSend",
            "receiving": receiving_player,
            "item": net_item}


def get_intended_text(input_text: str, possible_answers) -> typing.Tuple[str, bool, str]:
    picks = fuzzy_process.extract(input_text, possible_answers, limit=2)
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


def mark_raw(function):
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
        asyncio.create_task(countdown(self.ctx, timer))
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
            self.ctx.notify_all(self.ctx.get_aliased_name(self.client.team, self.client.slot) + ': ' + raw)
        return super(ClientMessageProcessor, self).__call__(raw)

    def output(self, text):
        self.ctx.notify_client(self.client, text)

    def default(self, raw: str):
        pass  # default is client sending just text

    def is_authenticated(self):
        return self.ctx.commandprocessor.client == self.client

    @mark_raw
    def _cmd_admin(self, command: str = ""):
        """Allow remote administration of the multiworld server"""

        output = f"!admin {command}"
        if output.lower().startswith(
                "!admin login"):  # disallow others from seeing the supplied password, whether or not it is correct.
            output = f"!admin login {('*' * random.randint(4, 16))}"
        elif output.lower().startswith(
                "!admin /option server_password"):  # disallow others from knowing what the new remote administration password is.
            output = f"!admin /option server_password {('*' * random.randint(4, 16))}"
        self.ctx.notify_all(self.ctx.get_aliased_name(self.client.team,
                                                      self.client.slot) + ': ' + output)  # Otherwise notify the others what is happening.

        if not self.ctx.server_password:
            self.output("Sorry, Remote administration is disabled")
            return False

        if not command:
            if self.is_authenticated():
                self.output(
                    "Usage: !admin [Server command].\nUse !admin /help for help.\nUse !admin logout to log out of the current session.")
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
        """Get information about connected and missing players"""
        if len(self.ctx.player_names) < 10:
            self.ctx.notify_all(get_players_string(self.ctx))
        else:
            self.output(get_players_string(self.ctx))
        return True

    def _cmd_forfeit(self) -> bool:
        """Surrender and send your remaining items out to their recipients"""
        if self.ctx.allow_forfeits.get((self.client.team, self.client.slot), False):
            forfeit_player(self.ctx, self.client.team, self.client.slot)
            return True
        if "enabled" in self.ctx.forfeit_mode:
            forfeit_player(self.ctx, self.client.team, self.client.slot)
            return True
        elif "disabled" in self.ctx.forfeit_mode:
            self.output(
                "Sorry, client forfeiting has been disabled on this server. You can ask the server admin for a /forfeit")
            return False
        else:  # is auto or goal
            if self.ctx.client_game_state[self.client.team, self.client.slot] == ClientStatus.CLIENT_GOAL:
                forfeit_player(self.ctx, self.client.team, self.client.slot)
                return True
            else:
                self.output(
                    "Sorry, client forfeiting requires you to have beaten the game on this server."
                    " You can ask the server admin for a /forfeit")
                return False

    def _cmd_remaining(self) -> bool:
        """List remaining items in your game, but not their location or recipient"""
        if self.ctx.remaining_mode == "enabled":
            remaining_item_ids = get_remaining(self.ctx, self.client.team, self.client.slot)
            if remaining_item_ids:
                self.output("Remaining items: " + ", ".join(lookup_any_item_id_to_name.get(item_id, "unknown item")
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
                    self.output("Remaining items: " + ", ".join(lookup_any_item_id_to_name.get(item_id, "unknown item")
                                                                for item_id in remaining_item_ids))
                else:
                    self.output("No remaining items found.")
                return True
            else:
                self.output(
                    "Sorry, !remaining requires you to have beaten the game on this server")
                return False

    def _cmd_missing(self) -> bool:
        """List all missing location checks from the server's perspective"""

        locations = get_missing_checks(self.ctx, self.client)

        if locations:
            texts = [f'Missing: {get_location_name_from_id(location)}' for location in locations]
            texts.append(f"Found {len(locations)} missing location checks")
            self.ctx.notify_client_multiple(self.client, texts)
        else:
            self.output("No missing location checks found.")
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
            world = proxy_worlds[self.ctx.games[self.client.slot]]
            item_name, usable, response = get_intended_text(item_name,
                                                            world.item_names)
            if usable:
                new_item = NetworkItem(world.create_item(item_name).code, -1, self.client.slot)
                get_received_items(self.ctx, self.client.team, self.client.slot).append(new_item)
                self.ctx.notify_all(
                    'Cheat console: sending "' + item_name + '" to ' + self.ctx.get_aliased_name(self.client.team,
                                                                                                 self.client.slot))
                send_new_items(self.ctx)
                return True
            else:
                self.output(response)
                return False
        else:
            self.output("Cheating is disabled.")
            return False

    @mark_raw
    def _cmd_hint(self, item_or_location: str = "") -> bool:
        """Use !hint {item_name/location_name},
        for example !hint Lamp or !hint Link's House to get a spoiler peek for that location or item.
        If hint costs are on, this will only give you one new result,
        you can rerun the command to get more in that case."""
        points_available = get_client_points(self.ctx, self.client)
        if not item_or_location:
            hints = {hint.re_check(self.ctx, self.client.team) for hint in
                     self.ctx.hints[self.client.team, self.client.slot]}
            self.ctx.hints[self.client.team, self.client.slot] = hints
            notify_hints(self.ctx, self.client.team, list(hints))
            self.output(f"A hint costs {self.ctx.get_hint_cost(self.client.slot)} points. "
                        f"You have {points_available} points.")
            return True
        else:
            world = proxy_worlds[self.ctx.games[self.client.slot]]
            item_name, usable, response = get_intended_text(item_or_location, world.all_names)
            if usable:
                if item_name in world.hint_blacklist:
                    self.output(f"Sorry, \"{item_name}\" is marked as non-hintable.")
                    hints = []
                elif item_name in world.item_name_groups:
                    hints = []
                    for item in world.item_name_groups[item_name]:
                        hints.extend(collect_hints(self.ctx, self.client.team, self.client.slot, item))
                elif item_name in world.item_names:  # item name
                    hints = collect_hints(self.ctx, self.client.team, self.client.slot, item_name)
                else:  # location name
                    hints = collect_hints_location(self.ctx, self.client.team, self.client.slot, item_name)
                cost = self.ctx.get_hint_cost(self.client.slot)
                if hints:
                    new_hints = set(hints) - self.ctx.hints[self.client.team, self.client.slot]
                    old_hints = set(hints) - new_hints
                    if old_hints:
                        notify_hints(self.ctx, self.client.team, list(old_hints))
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

                        hints = found_hints
                        while can_pay > 0:
                            if not not_found_hints:
                                break
                            hint = not_found_hints.pop()
                            hints.append(hint)
                            can_pay -= 1
                            self.ctx.hints_used[self.client.team, self.client.slot] += 1

                            if not hint.found:
                                self.ctx.hints[self.client.team, hint.finding_player].add(hint)
                                self.ctx.hints[self.client.team, hint.receiving_player].add(hint)

                        if not_found_hints:
                            if hints:
                                self.output(
                                    "There may be more hintables, you can rerun the command to find more.")
                            else:
                                self.output(f"You can't afford the hint. "
                                            f"You have {points_available} points and need at least "
                                            f"{self.ctx.get_hint_cost(self.client.slot)}")
                        notify_hints(self.ctx, self.client.team, hints)
                        self.ctx.save()
                        return True

                else:
                    self.output("Nothing found. Item/Location may not exist.")
                    return False
            else:
                self.output(response)
                return False


def get_checked_checks(ctx: Context, client: Client) -> typing.List[int]:
    return [location_id for
            location_id in ctx.locations[client.slot] if
            location_id in ctx.location_checks[client.team, client.slot]]


def get_missing_checks(ctx: Context, client: Client) -> typing.List[int]:
    return [location_id for
            location_id in ctx.locations[client.slot] if
            location_id not in ctx.location_checks[client.team, client.slot]]


def get_client_points(ctx: Context, client: Client) -> int:
    return (ctx.location_check_points * len(ctx.location_checks[client.team, client.slot]) -
            ctx.get_hint_cost(client.slot) * ctx.hints_used[client.team, client.slot])


async def process_client_cmd(ctx: Context, client: Client, args: dict):
    try:
        cmd: str = args["cmd"]
    except:
        logging.exception(f"Could not get command from {args}")
        await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "cmd",
                                      "text": f"Could not get command from {args} at `cmd`"}])
        raise

    if type(cmd) is not str:
        await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "cmd",
                                      "text": f"Command should be str, got {type(cmd)}"}])
        return

    if cmd == 'Connect':
        if not args or 'password' not in args or type(args['password']) not in [str, type(None)] or \
                'game' not in args:
            await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments", 'text': 'Connect'}])
            return

        errors = set()
        if ctx.password and args['password'] != ctx.password:
            errors.add('InvalidPassword')

        if args['name'] not in ctx.connect_names:
            logging.info((args["name"], ctx.connect_names))
            errors.add('InvalidSlot')
        else:
            team, slot = ctx.connect_names[args['name']]
            game = ctx.games[slot]
            if "IgnoreGame" not in args["tags"] and args['game'] != game:
                errors.add('InvalidGame')
            # this can only ever be 0 or 1 elements
            clients = [c for c in ctx.endpoints if c.auth and c.slot == slot and c.team == team]
            if clients:
                # likely same player with a "ghosted" slot. We bust the ghost.
                if "uuid" in args and ctx.client_ids[team, slot] == args["uuid"]:
                    await ctx.send_msgs(clients[0], [{"cmd": "Print", "text": "You are getting kicked "
                                                                              "by yourself reconnecting."}])
                    await clients[0].socket.close()  # we have to await the DC of the ghost, so not to create data pasta
                    client.name = ctx.player_names[(team, slot)]
                    client.team = team
                    client.slot = slot
                else:
                    errors.add('SlotAlreadyTaken')
            else:
                client.name = ctx.player_names[(team, slot)]
                client.team = team
                client.slot = slot
                minver = ctx.minimum_client_versions[slot]
                if minver > args['version']:
                    errors.add('IncompatibleVersion')

        # only exact version match allowed
        if ctx.compatibility == 0 and args['version'] != version_tuple:
            errors.add('IncompatibleVersion')
        if errors:
            logging.info(f"A client connection was refused due to: {errors}, the sent connect information was {args}.")
            await ctx.send_msgs(client, [{"cmd": "ConnectionRefused", "errors": list(errors)}])
        else:
            ctx.client_ids[client.team, client.slot] = args["uuid"]
            client.auth = True
            client.version = args['version']
            client.tags = args['tags']
            reply = [{
                "cmd": "Connected",
                "team": client.team, "slot": client.slot,
                "players": ctx.get_players_package(),
                "missing_locations": get_missing_checks(ctx, client),
                "checked_locations": get_checked_checks(ctx, client),
                # get is needed for old multidata that was sparsely populated
                "slot_data": ctx.slot_data.get(client.slot, {})
            }]
            items = get_received_items(ctx, client.team, client.slot)
            if items:
                reply.append({"cmd": 'ReceivedItems', "index": 0, "items": items})
                client.send_index = len(items)

            await ctx.send_msgs(client, reply)
            await on_client_joined(ctx, client)

    elif cmd == "GetDataPackage":
        exclusions = set(args.get("exclusions", []))
        if exclusions:
            games = {name: game_data for name, game_data in network_data_package["games"].items()
                     if name not in exclusions}
            package = network_data_package.copy()
            package["games"] = games
            await ctx.send_msgs(client, [{"cmd": "DataPackage",
                                          "data": package}])
        else:
            await ctx.send_msgs(client, [{"cmd": "DataPackage",
                                          "data": network_data_package}])
    elif client.auth:
        if cmd == 'Sync':
            items = get_received_items(ctx, client.team, client.slot)
            if items:
                client.send_index = len(items)
                await ctx.send_msgs(client, [{"cmd": "ReceivedItems", "index": 0,
                                              "items": items}])

        elif cmd == 'LocationChecks':
            register_location_checks(ctx, client.team, client.slot, args["locations"])

        elif cmd == 'LocationScouts':
            locs = []
            for location in args["locations"]:
                if type(location) is not int or location not in lookup_any_location_id_to_name:
                    await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments", "text": 'LocationScouts'}])
                    return
                target_item, target_player = ctx.locations[client.slot][location]
                locs.append(NetworkItem(target_item, location, target_player))

            await ctx.send_msgs(client, [{'cmd': 'LocationInfo', 'locations': locs}])

        elif cmd == 'StatusUpdate':
            update_client_status(ctx, client, args["status"])

        elif cmd == 'Say':
            if "text" not in args or type(args["text"]) is not str or not args["text"].isprintable():
                await ctx.send_msgs(client, [{'cmd': 'InvalidPacket', "type": "arguments", "text": 'Say'}])
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


def update_client_status(ctx: Context, client: Client, new_status: ClientStatus):
    current = ctx.client_game_state[client.team, client.slot]
    if current != ClientStatus.CLIENT_GOAL:  # can't undo goal completion
        if new_status == ClientStatus.CLIENT_GOAL:
            finished_msg = f'{ctx.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1}) has completed their goal.'
            ctx.notify_all(finished_msg)
            if "auto" in ctx.forfeit_mode:
                forfeit_player(ctx, client.team, client.slot)
            elif proxy_worlds[ctx.games[client.slot]].forced_auto_forfeit:
                forfeit_player(ctx, client.team, client.slot)

        ctx.client_game_state[client.team, client.slot] = new_status


class ServerCommandProcessor(CommonCommandProcessor):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        super(ServerCommandProcessor, self).__init__()

    def output(self, text: str):
        if self.client:
            self.ctx.notify_client(self.client, text)
        super(ServerCommandProcessor, self).output(text)

    def default(self, raw: str):
        self.ctx.notify_all('[Server]: ' + raw)

    @mark_raw
    def _cmd_kick(self, player_name: str) -> bool:
        """Kick specified player from the server"""
        for client in self.ctx.endpoints:
            if client.auth and client.name.lower() == player_name.lower() and client.socket and not client.socket.closed:
                asyncio.create_task(client.socket.close())
                self.output(f"Kicked {self.ctx.get_aliased_name(client.team, client.slot)}")
                if self.ctx.commandprocessor.client == client:
                    self.ctx.commandprocessor.client = None
                return True

        self.output(f"Could not find player {player_name} to kick")
        return False

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

    def _cmd_exit(self) -> bool:
        """Shutdown the server"""
        asyncio.create_task(self.ctx.server.ws_server._close())
        if self.ctx.shutdown_task:
            self.ctx.shutdown_task.cancel()
        self.ctx.running = False
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

    @mark_raw
    def _cmd_forfeit(self, player_name: str) -> bool:
        """Send out the remaining items from a player's game to their intended recipients"""
        seeked_player = player_name.lower()
        for (team, slot), name in self.ctx.player_names.items():
            if name.lower() == seeked_player:
                forfeit_player(self.ctx, team, slot)
                return True

        self.output(f"Could not find player {player_name} to forfeit")
        return False

    @mark_raw
    def _cmd_allow_forfeit(self, player_name: str) -> bool:
        """Allow the specified player to use the !forfeit command"""
        seeked_player = player_name.lower()
        for (team, slot), name in self.ctx.player_names.items():
            if name.lower() == seeked_player:
                self.ctx.allow_forfeits[(team, slot)] = True
                self.output(f"Player {player_name} is now allowed to use the !forfeit command at any time.")
                return True

        self.output(f"Could not find player {player_name} to allow the !forfeit command for.")
        return False

    @mark_raw
    def _cmd_forbid_forfeit(self, player_name: str) -> bool:
        """"Disallow the specified player from using the !forfeit command"""
        seeked_player = player_name.lower()
        for (team, slot), name in self.ctx.player_names.items():
            if name.lower() == seeked_player:
                self.ctx.allow_forfeits[(team, slot)] = False
                self.output(
                    f"Player {player_name} has to follow the server restrictions on use of the !forfeit command.")
                return True

        self.output(f"Could not find player {player_name} to forbid the !forfeit command for.")
        return False

    def _cmd_send(self, player_name: str, *item_name: str) -> bool:
        """Sends an item to the specified player"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            team, slot = self.ctx.player_name_lookup[seeked_player]
            item = " ".join(item_name)
            world = proxy_worlds[self.ctx.games[slot]]
            item, usable, response = get_intended_text(item, world.item_names)
            if usable:
                new_item = NetworkItem(world.item_name_to_id[item], -1, 0)
                get_received_items(self.ctx, team, slot).append(new_item)
                self.ctx.notify_all('Cheat console: sending "' + item + '" to ' +
                                    self.ctx.get_aliased_name(team, slot))
                send_new_items(self.ctx)
                return True
            else:
                self.output(response)
                return False
        else:
            self.output(response)
            return False

    def _cmd_hint(self, player_name: str, *item_or_location: str) -> bool:
        """Send out a hint for a player's item or location to their team"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            team, slot = self.ctx.player_name_lookup[seeked_player]
            item = " ".join(item_or_location)
            world = proxy_worlds[self.ctx.games[slot]]
            item, usable, response = get_intended_text(item, world.all_names)
            if usable:
                if item in world.item_name_groups:
                    hints = []
                    for item in world.item_name_groups[item]:
                        hints.extend(collect_hints(self.ctx, team, slot, item))
                elif item in world.item_names:  # item name
                    hints = collect_hints(self.ctx, team, slot, item)
                else:  # location name
                    hints = collect_hints_location(self.ctx, team, slot, item)
                if hints:
                    notify_hints(self.ctx, team, hints)
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
        """Set options for the server. Warning: expires on restart"""

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
            return True
        else:
            known = (f"{option}:{otype}" for option, otype in self.ctx.simple_options.items())
            self.output(f"Unrecognized Option {option_name}, known: "
                        f"{', '.join(known)}")
            return False


async def console(ctx: Context):
    session = prompt_toolkit.PromptSession()
    while ctx.running:
        with patch_stdout():
            input_text = await session.prompt_async()
        try:
            ctx.commandprocessor(input_text)
        except:
            import traceback
            traceback.print_exc()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    defaults = Utils.get_options()["server_options"]
    parser.add_argument('multidata', nargs="?", default=defaults["multidata"])
    parser.add_argument('--host', default=defaults["host"])
    parser.add_argument('--port', default=defaults["port"], type=int)
    parser.add_argument('--server_password', default=defaults["server_password"])
    parser.add_argument('--password', default=defaults["password"])
    parser.add_argument('--savefile', default=defaults["savefile"])
    parser.add_argument('--disable_save', default=defaults["disable_save"], action='store_true')
    parser.add_argument('--loglevel', default=defaults["loglevel"],
                        choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('--location_check_points', default=defaults["location_check_points"], type=int)
    parser.add_argument('--hint_cost', default=defaults["hint_cost"], type=int)
    parser.add_argument('--disable_item_cheat', default=defaults["disable_item_cheat"], action='store_true')
    parser.add_argument('--forfeit_mode', default=defaults["forfeit_mode"], nargs='?',
                        choices=['auto', 'enabled', 'disabled', "goal", "auto-enabled"], help='''\
                             Select !forfeit Accessibility. (default: %(default)s)
                             auto:     Automatic "forfeit" on goal completion
                             enabled:  !forfeit is always available
                             disabled: !forfeit is never available
                             goal:     !forfeit can be used after goal completion
                             auto-enabled: !forfeit is available and automatically triggered on goal completion
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
                        help='retrieve forfeit, remaining and hint options from the multidata file,'
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
    while ctx.running:
        if not ctx.client_activity_timers.values():
            asyncio.create_task(ctx.server.ws_server._close())
            ctx.running = False
            if to_cancel:
                for task in to_cancel:
                    task.cancel()
            logging.info("Shutting down due to inactivity.")
        else:
            newest_activity = max(ctx.client_activity_timers.values())
            delta = datetime.datetime.now(datetime.timezone.utc) - newest_activity
            seconds = ctx.auto_shutdown - delta.total_seconds()
            if seconds < 0:
                asyncio.create_task(ctx.server.ws_server._close())
                ctx.running = False
                if to_cancel:
                    for task in to_cancel:
                        task.cancel()
                logging.info("Shutting down due to inactivity.")
            else:
                await asyncio.sleep(seconds)


async def main(args: argparse.Namespace):
    logging.basicConfig(force=True,
                        format='[%(asctime)s] %(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))

    ctx = Context(args.host, args.port, args.server_password, args.password, args.location_check_points,
                  args.hint_cost, not args.disable_item_cheat, args.forfeit_mode, args.remaining_mode,
                  args.auto_shutdown, args.compatibility, args.log_network)
    data_filename = args.multidata

    try:
        if not data_filename:
            import tkinter
            import tkinter.filedialog
            root = tkinter.Tk()
            root.withdraw()
            data_filename = tkinter.filedialog.askopenfilename(filetypes=(("Multiworld data", "*.archipelago *.zip"),))

        ctx.load(data_filename, args.use_embedded_options)

    except Exception as e:
        logging.exception('Failed to read multiworld data (%s)' % e)
        raise

    ctx.init_save(not args.disable_save)

    ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, ctx.port, ping_timeout=None,
                                  ping_interval=None)
    ip = args.host if args.host else Utils.get_public_ipv4()
    logging.info('Hosting game at %s:%d (%s)' % (ip, ctx.port,
                                                 'No password' if not ctx.password else 'Password: %s' % ctx.password))

    await ctx.server
    console_task = asyncio.create_task(console(ctx))
    if ctx.auto_shutdown:
        ctx.shutdown_task = asyncio.create_task(auto_shutdown(ctx, [console_task]))
    await console_task
    if ctx.shutdown_task:
        await ctx.shutdown_task


client_message_processor = ClientMessageProcessor

if __name__ == '__main__':
    try:
        asyncio.run(main(parse_args()))
    except asyncio.exceptions.CancelledError:
        pass
