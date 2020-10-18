from __future__ import annotations

import argparse
import asyncio
import functools
import json
import logging
import zlib
import collections
import typing
import inspect
import weakref
import datetime
import threading
import random

import ModuleUpdate

ModuleUpdate.update()

import websockets
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout
from fuzzywuzzy import process as fuzzy_process

import Items
import Regions
import Utils
from Utils import get_item_name_from_id, get_location_name_from_address, ReceivedItem, _version_tuple
from NetUtils import Node, Endpoint

console_names = frozenset(set(Items.item_table) | set(Regions.location_table) | set(Items.item_name_groups))

CLIENT_PLAYING = 0
CLIENT_GOAL = 1



class Client(Endpoint):
    version: typing.List[int] = [0, 0, 0]
    tags: typing.List[str] = []

    def __init__(self, socket: websockets.server.WebSocketServerProtocol, ctx: Context):
        super().__init__(socket)
        self.auth = False
        self.name = None
        self.team = None
        self.slot = None
        self.send_index = 0
        self.tags = []
        self.version = [0, 0, 0]
        self.messageprocessor = client_message_processor(ctx, self)
        self.ctx = weakref.ref(ctx)

    @property
    def wants_item_notification(self):
        return self.auth and "FoundItems" in self.tags


class Context(Node):
    def __init__(self, host: str, port: int, server_password: str, password: str, location_check_points: int,
                 hint_cost: int, item_cheat: bool, forfeit_mode: str = "disabled", remaining_mode: str = "disabled",
                 auto_shutdown: typing.SupportsFloat = 0, compatibility: int = 2):
        super(Context, self).__init__()
        self.compatibility: int = compatibility
        self.shutdown_task = None
        self.data_filename = None
        self.save_filename = None
        self.saving = False
        self.player_names = {}
        self.rom_names = {}
        self.allow_forfeits = {}
        self.remote_items = set()
        self.locations = {}
        self.host = host
        self.port = port
        self.server_password = server_password
        self.password = password
        self.server = None
        self.countdown_timer = 0
        self.received_items = {}
        self.name_aliases: typing.Dict[typing.Tuple[int, int], str] = {}
        self.location_checks = collections.defaultdict(set)
        self.hint_cost = hint_cost
        self.location_check_points = location_check_points
        self.hints_used = collections.defaultdict(int)
        self.hints: typing.Dict[typing.Tuple[int, int], typing.Set[Utils.Hint]] = collections.defaultdict(set)
        self.forfeit_mode: str = forfeit_mode
        self.remaining_mode: str = remaining_mode
        self.item_cheat = item_cheat
        self.running = True
        self.client_activity_timers: typing.Dict[
            typing.Tuple[int, int], datetime.datetime] = {}  # datetime of last new item check
        self.client_connection_timers: typing.Dict[
            typing.Tuple[int, int], datetime.datetime] = {}  # datetime of last connection
        self.client_game_state: typing.Dict[typing.Tuple[int, int], int] = collections.defaultdict(int)
        self.er_hint_data: typing.Dict[int, typing.Dict[int, str]] = {}
        self.auto_shutdown = auto_shutdown
        self.commandprocessor = ServerCommandProcessor(self)
        self.embedded_blacklist = {"host", "port"}
        self.client_ids: typing.Dict[typing.Tuple[int, int], datetime.datetime] = {}
        self.auto_save_interval = 60  # in seconds
        self.auto_saver_thread = None
        self.save_dirty = False
        self.tags = ['AP']

    def load(self, multidatapath: str, use_embedded_server_options: bool = False):
        with open(multidatapath, 'rb') as f:
            self._load(json.loads(zlib.decompress(f.read()).decode("utf-8-sig")),
                       use_embedded_server_options)

        self.data_filename = multidatapath

    def _load(self, jsonobj: dict, use_embedded_server_options: bool):
        for team, names in enumerate(jsonobj['names']):
            for player, name in enumerate(names, 1):
                self.player_names[(team, player)] = name

        if "rom_strings" in jsonobj:
            self.rom_names = {rom: (team, slot) for slot, team, rom in jsonobj['rom_strings']}
        else:
            self.rom_names = {bytes(letter for letter in rom).decode(): (team, slot) for slot, team, rom in
                              jsonobj['roms']}
        self.remote_items = set(jsonobj['remote_items'])
        self.locations = {tuple(k): tuple(v) for k, v in jsonobj['locations']}
        if "er_hint_data" in jsonobj:
            self.er_hint_data = {int(player): {int(address): name for address, name in loc_data.items()}
                                 for player, loc_data in jsonobj["er_hint_data"].items()}
        if use_embedded_server_options:
            server_options = jsonobj.get("server_options", {})
            self._set_options(server_options)

    def _set_options(self, server_options: dict):

        sentinel = object()
        for key, value in server_options.items():
            if key not in self.embedded_blacklist:
                current = getattr(self, key, sentinel)
                if current is not sentinel:
                    logging.debug(f"Setting server option {key} to {value} from supplied multidata")
                    setattr(self, key, value)
        self.item_cheat = not server_options.get("disable_item_cheat", True)

    def save(self, now=False) -> bool:
        if self.saving:
            if now:
                self.save_dirty = False
                return self._save()

            self.save_dirty = True
            return True

        return False

    def _save(self, exit_save:bool=False) -> bool:
        try:
            jsonstr = json.dumps(self.get_save())
            with open(self.save_filename, "wb") as f:
                f.write(zlib.compress(jsonstr.encode("utf-8")))
        except Exception as e:
            logging.exception(e)
            return False
        else:
            return True

    def init_save(self, enabled: bool = True):
        self.saving = enabled
        if self.saving:
            if not self.save_filename:
                self.save_filename = (self.data_filename[:-9] if self.data_filename[-9:] == 'multidata' else (
                        self.data_filename + '_')) + 'multisave'
            try:
                with open(self.save_filename, 'rb') as f:
                    jsonobj = json.loads(zlib.decompress(f.read()).decode("utf-8"))
                    self.set_save(jsonobj)
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
                        logging.debug("Saving multisave via thread.")
                        self.save_dirty = False
                        self._save()

            self.auto_saver_thread = threading.Thread(target=save_regularly, daemon=True)
            self.auto_saver_thread.start()

            import atexit
            atexit.register(self._save, True)  # make sure we save on exit too

    def get_save(self) -> dict:
        d = {
            "rom_names": list(self.rom_names.items()),
            "received_items": tuple((k, v) for k, v in self.received_items.items()),
            "hints_used": tuple((key, value) for key, value in self.hints_used.items()),
            "hints": tuple(
                (key, list(hint.re_check(self, key[0]) for hint in value)) for key, value in self.hints.items()),
            "location_checks": tuple((key, tuple(value)) for key, value in self.location_checks.items()),
            "name_aliases": tuple((key, value) for key, value in self.name_aliases.items()),
            "client_game_state": tuple((key, value) for key, value in self.client_game_state.items()),
            "client_activity_timers": tuple(
                (key, value.timestamp()) for key, value in self.client_activity_timers.items()),
            "client_connection_timers": tuple(
                (key, value.timestamp()) for key, value in self.client_connection_timers.items()),
        }
        return d

    def set_save(self, savedata: dict):
        rom_names = savedata["rom_names"]  # convert from TrackerList to List in case of ponyorm
        try:
            adjusted = {rom: (team, slot) for rom, (team, slot) in rom_names}
        except TypeError:
            adjusted = {tuple(rom): (team, slot) for (rom, (team, slot)) in rom_names}  # old format, ponyorm friendly
            if self.rom_names != adjusted:
                logging.warning('Save file mismatch, will start a new game')
                return
        else:
            if adjusted != self.rom_names:
                logging.warning('Save file mismatch, will start a new game')
                return

        received_items = {tuple(k): [ReceivedItem(*i) for i in v] for k, v in savedata["received_items"]}

        self.received_items = received_items
        self.hints_used.update({tuple(key): value for key, value in savedata["hints_used"]})
        if "hints" in savedata:
            self.hints.update(
                {tuple(key): set(Utils.Hint(*hint) for hint in value) for key, value in savedata["hints"]})
        else:  # backwards compatiblity for <= 2.0.2
            old_hints = {tuple(key): set(value) for key, value in savedata["hints_sent"]}
            for team_slot, item_or_location_s in old_hints.items():
                team, slot = team_slot
                for item_or_location in item_or_location_s:
                    if item_or_location in Items.item_table:
                        hints = collect_hints(self, team, slot, item_or_location)
                    else:
                        hints = collect_hints_location(self, team, slot, item_or_location)
                    for hint in hints:
                        self.hints[team, hint.receiving_player].add(hint)
                        # even if it is the same hint, it won't be duped due to set
                        self.hints[team, hint.finding_player].add(hint)
        if "name_aliases" in savedata:
            self.name_aliases.update({tuple(key): value for key, value in savedata["name_aliases"]})
            if "client_game_state" in savedata:
                self.client_game_state.update({tuple(key): value for key, value in savedata["client_game_state"]})
                if "client_activity_timers" in savedata:
                    self.client_connection_timers.update(
                        {tuple(key): datetime.datetime.fromtimestamp(value, datetime.timezone.utc) for key, value
                         in savedata["client_connection_timers"]})
                    self.client_activity_timers.update(
                        {tuple(key): datetime.datetime.fromtimestamp(value, datetime.timezone.utc) for key, value
                         in savedata["client_activity_timers"]})

        self.location_checks.update({tuple(key): set(value) for key, value in savedata["location_checks"]})

        logging.info(f'Loaded save file with {sum([len(p) for p in received_items.values()])} received items '
                     f'for {len(received_items)} players')

    def get_aliased_name(self, team: int, slot: int):
        if (team, slot) in self.name_aliases:
            return f"{self.name_aliases[team, slot]} ({self.player_names[team, slot]})"
        else:
            return self.player_names[team, slot]

    def notify_all(self, text):
        logging.info("Notice (all): %s" % text)
        self.broadcast_all([['Print', text]])

    def notify_client(self, client: Client, text: str):
        if not client.auth:
            return
        logging.info("Notice (Player %s in team %d): %s" % (client.name, client.team + 1, text))
        asyncio.create_task(self.send_msgs(client, [['Print', text]]))

    def broadcast_team(self, team, msgs):
        for client in self.endpoints:
            if client.auth and client.team == team:
                asyncio.create_task(self.send_msgs(client, msgs))

    def broadcast_all(self, msgs):
        msgs = json.dumps(msgs)
        for endpoint in self.endpoints:
            if endpoint.auth:
                asyncio.create_task(self.send_json_msgs(endpoint, msgs))

    async def disconnect(self, endpoint):
        await super(Context, self).disconnect(endpoint)
        await on_client_disconnected(self, endpoint)


# separated out, due to compatibilty between clients
def notify_hints(ctx: Context, team: int, hints: typing.List[Utils.Hint]):
    cmd = json.dumps([["Hint", hints]])  # make sure it is a list, as it can be set internally
    texts = [['Print', format_hint(ctx, team, hint)] for hint in hints]
    for _, text in texts:
        logging.info("Notice (Team #%d): %s" % (team + 1, text))

    for client in ctx.endpoints:
        if client.auth and client.team == team:
            asyncio.create_task(ctx.send_json_msgs(client, cmd))


def update_aliases(ctx: Context, team: int, client: typing.Optional[Client] = None):
    cmd = json.dumps([["AliasUpdate",
                       [(key[1], ctx.get_aliased_name(*key)) for key, value in ctx.player_names.items() if
                        key[0] == team]]])
    if client is None:
        for client in ctx.endpoints:
            if client.team == team and client.auth and client.version > [2, 0, 3]:
                asyncio.create_task(ctx.send_json_msgs(client, cmd))
    else:
        asyncio.create_task(ctx.send_json_msgs(client, cmd))


async def server(websocket, path, ctx: Context):
    client = Client(websocket, ctx)
    ctx.endpoints.append(client)

    try:
        await on_client_connected(ctx, client)
        async for data in websocket:
            for msg in json.loads(data):
                if len(msg) == 1:
                    cmd = msg
                    args = None
                else:
                    cmd = msg[0]
                    args = msg[1]
                await process_client_cmd(ctx, client, cmd, args)
    except Exception as e:
        if not isinstance(e, websockets.WebSocketException):
            logging.exception(e)
    finally:
        await ctx.disconnect(client)


async def on_client_connected(ctx: Context, client: Client):
    await ctx.send_msgs(client, [['RoomInfo', {
        'password': ctx.password is not None,
        'players': [(client.team, client.slot, ctx.name_aliases.get((client.team, client.slot), client.name)) for client
                    in ctx.endpoints if client.auth],
        # tags are for additional features in the communication.
        # Name them by feature or fork, as you feel is appropriate.
        'tags': ctx.tags,
        'version': Utils._version_tuple,
        'forfeit_mode': ctx.forfeit_mode,
        'remaining_mode': ctx.remaining_mode,
        'hint_cost': ctx.hint_cost,
        'location_check_points': ctx.location_check_points
    }]])


async def on_client_disconnected(ctx: Context, client: Client):
    if client.auth:
        await on_client_left(ctx, client)


async def on_client_joined(ctx: Context, client: Client):
    version_str = '.'.join(str(x) for x in client.version)
    ctx.notify_all(
        f"{ctx.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1}) has joined the game. "
        f"Client({version_str}), {client.tags}).")
    ctx.client_connection_timers[client.team, client.slot] = datetime.datetime.now(datetime.timezone.utc)

async def on_client_left(ctx: Context, client: Client):
    ctx.notify_all("%s (Team #%d) has left the game" % (ctx.get_aliased_name(client.team, client.slot), client.team + 1))
    ctx.client_connection_timers[client.team, client.slot] = datetime.datetime.now(datetime.timezone.utc)
    if ctx.commandprocessor.client == Client:
        ctx.commandprocessor.client = None


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

async def missing(ctx: Context, client: Client, locations: list):
    await ctx.send_msgs(client, [['Missing', {
        'locations': json.dumps(locations)
    }]])


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


def get_received_items(ctx: Context, team: int, player: int) -> typing.List[ReceivedItem]:
    return ctx.received_items.setdefault((team, player), [])


def tuplize_received_items(items):
    return [(item.item, item.location, item.player) for item in items]


def send_new_items(ctx: Context):
    for client in ctx.endpoints:
        if not client.auth:
            continue
        items = get_received_items(ctx, client.team, client.slot)
        if len(items) > client.send_index:
            asyncio.create_task(ctx.send_msgs(client, [
                ['ReceivedItems', (client.send_index, tuplize_received_items(items)[client.send_index:])]]))
            client.send_index = len(items)


def forfeit_player(ctx: Context, team: int, slot: int):
    all_locations = {values[0] for values in Regions.location_table.values() if type(values[0]) is int}
    ctx.notify_all("%s (Team #%d) has forfeited" % (ctx.player_names[(team, slot)], team + 1))
    register_location_checks(ctx, team, slot, all_locations)


def get_remaining(ctx: Context, team: int, slot: int) -> typing.List[int]:
    items = []
    for (location, location_slot) in ctx.locations:
        if location_slot == slot and location not in ctx.location_checks[team, slot]:
            items.append(ctx.locations[location, slot][0])  # item ID
    return sorted(items)


def register_location_checks(ctx: Context, team: int, slot: int, locations):
    found_items = False
    new_locations = set(locations) - ctx.location_checks[team, slot]
    if new_locations:
        ctx.client_activity_timers[team, slot] = datetime.datetime.now(datetime.timezone.utc)
        for location in new_locations:
            if (location, slot) in ctx.locations:
                target_item, target_player = ctx.locations[(location, slot)]
                if target_player != slot or slot in ctx.remote_items:
                    found = False
                    recvd_items = get_received_items(ctx, team, target_player)
                    for recvd_item in recvd_items:
                        if recvd_item.location == location and recvd_item.player == slot:
                            found = True
                            break

                    if not found:
                        new_item = ReceivedItem(target_item, location, slot)
                        recvd_items.append(new_item)
                        if slot != target_player:
                            ctx.broadcast_team(team, [['ItemSent', (slot, location, target_player, target_item)]])
                    logging.info('(Team #%d) %s sent %s to %s (%s)' % (
                    team + 1, ctx.player_names[(team, slot)], get_item_name_from_id(target_item),
                    ctx.player_names[(team, target_player)], get_location_name_from_address(location)))
                    found_items = True
                elif target_player == slot:  # local pickup, notify clients of the pickup
                    if location not in ctx.location_checks[team, slot]:
                        for client in ctx.endpoints:
                                if client.team == team and client.wants_item_notification:
                                    asyncio.create_task(
                                        ctx.send_msgs(client, [['ItemFound', (target_item, location, slot)]]))
        ctx.location_checks[team, slot] |= new_locations
        send_new_items(ctx)

        if found_items:
            for client in ctx.endpoints:
                if client.team == team and client.slot == slot:
                    asyncio.create_task(ctx.send_msgs(client, [["HintPointUpdate", (get_client_points(ctx, client),)]]))
        ctx.save()


def notify_team(ctx: Context, team: int, text: str):
    logging.info("Notice (Team #%d): %s" % (team + 1, text))
    ctx.broadcast_team(team, [['Print', text]])



def collect_hints(ctx: Context, team: int, slot: int, item: str) -> typing.List[Utils.Hint]:
    hints = []
    seeked_item_id = Items.item_table[item][3]
    for check, result in ctx.locations.items():
        item_id, receiving_player = result
        if receiving_player == slot and item_id == seeked_item_id:
            location_id, finding_player = check
            found = location_id in ctx.location_checks[team, finding_player]
            entrance = ctx.er_hint_data.get(finding_player, {}).get(location_id, "")
            hints.append(Utils.Hint(receiving_player, finding_player, location_id, item_id, found, entrance))

    return hints


def collect_hints_location(ctx: Context, team: int, slot: int, location: str) -> typing.List[Utils.Hint]:
    hints = []
    seeked_location = Regions.location_table[location][0]
    for check, result in ctx.locations.items():
        location_id, finding_player = check
        if finding_player == slot and location_id == seeked_location:
            item_id, receiving_player = result
            found = location_id in ctx.location_checks[team, finding_player]
            entrance = ctx.er_hint_data.get(finding_player, {}).get(location_id, "")
            hints.append(Utils.Hint(receiving_player, finding_player, location_id, item_id, found, entrance))
            break  # each location has 1 item
    return hints


def format_hint(ctx: Context, team: int, hint: Utils.Hint) -> str:
    text = f"[Hint]: {ctx.player_names[team, hint.receiving_player]}'s " \
           f"{Items.lookup_id_to_name[hint.item]} is " \
           f"at {get_location_name_from_address(hint.location)} " \
           f"in {ctx.player_names[team, hint.finding_player]}'s World"

    if hint.entrance:
        text += f" at {hint.entrance}"
    return text + (". (found)" if hint.found else ".")


def get_intended_text(input_text: str, possible_answers: typing.Iterable[str]= console_names) -> typing.Tuple[str, bool, str]:
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
        commands.update({name[5:].lower(): method for name, method in attrs.items() if
                         name.startswith("_cmd_")})
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
        self.output(str(exception))


class CommonCommandProcessor(CommandProcessor):
    ctx: Context

    simple_options = {"hint_cost": int,
                      "location_check_points": int,
                      "server_password": str,
                      "password": str,
                      "forfeit_mode": str,
                      "item_cheat": bool,
                      "auto_save_interval": int,
                      "compatibility": int}

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
        for option in self.simple_options:
            if option == "server_password" and self.marker == "!":  #Do not display the server password to the client.
                self.output(f"Option server_password is set to {('*' * random.randint(4,16))}")
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
        if output.lower().startswith("!admin login"):  # disallow others from seeing the supplied password, whether or not it is correct.
            output = f"!admin login {('*' * random.randint(4, 16))}"
        elif output.lower().startswith("!admin /option server_password"):  # disallow others from knowing what the new remote administration password is.
            output = f"!admin /option server_password {('*' * random.randint(4, 16))}"
        self.ctx.notify_all(self.ctx.get_aliased_name(self.client.team, self.client.slot) + ': ' + output)  # Otherwise notify the others what is happening.

        if not self.ctx.server_password:
            self.output("Sorry, Remote administration is disabled")
            return False

        if not command:
            if self.is_authenticated():
                self.output("Usage: !admin [Server command].\nUse !admin /help for help.\nUse !admin logout to log out of the current session.")
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
            if self.ctx.client_game_state[self.client.team, self.client.slot] == CLIENT_GOAL:
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
                self.output("Remaining items: " + ", ".join(Items.lookup_id_to_name.get(item_id, "unknown item")
                                                            for item_id in remaining_item_ids))
            else:
                self.output("No remaining items found.")
            return True
        elif self.ctx.remaining_mode == "disabled":
            self.output(
                "Sorry, !remaining has been disabled on this server.")
            return False
        else:  # is goal
            if self.ctx.client_game_state[self.client.team, self.client.slot] == CLIENT_GOAL:
                remaining_item_ids = get_remaining(self.ctx, self.client.team, self.client.slot)
                if remaining_item_ids:
                    self.output("Remaining items: " + ", ".join(Items.lookup_id_to_name.get(item_id, "unknown item")
                                                                for item_id in remaining_item_ids))
                else:
                    self.output("No remaining items found.")
                return True
            else:
                self.output(
                    "Sorry, !remaining requires you to have beaten the game on this server")
                if self.client.version < [2, 1, 0]:
                    self.output(
                        "Your client is too old to send game beaten information. Please update, load you savegame and reconnect.")
                return False


    def _cmd_missing(self) -> bool:
        """List all missing location checks from the server's perspective"""

        locations = []
        for location_id, location_name in Regions.lookup_id_to_name.items():  # cheat console is -1, keep in mind
            if location_id != -1 and location_id not in self.ctx.location_checks[self.client.team, self.client.slot]:
                locations.append(location_name)

        if len(locations) > 0:
            if self.client.version < [2, 3, 0]:
                buffer = ""
                for location in locations:
                    buffer += f'Missing: {location}\n'
                self.output(buffer + f"Found {len(locations)} missing location checks")
            else:
                asyncio.create_task(missing(self.ctx, self.client, locations))
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
            item_name, usable, response = get_intended_text(item_name, Items.item_table.keys())
            if usable:
                new_item = ReceivedItem(Items.item_table[item_name][3], -1, self.client.slot)
                get_received_items(self.ctx, self.client.team, self.client.slot).append(new_item)
                self.ctx.notify_all('Cheat console: sending "' + item_name + '" to ' + self.ctx.get_aliased_name(self.client.team, self.client.slot))
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
        """Use !hint {item_name/location_name}, for example !hint Lamp or !hint Link's House. """
        points_available = get_client_points(self.ctx, self.client)
        if not item_or_location:
            self.output(f"A hint costs {self.ctx.hint_cost} points. "
                        f"You have {points_available} points.")
            hints = {hint.re_check(self.ctx, self.client.team) for hint in
                     self.ctx.hints[self.client.team, self.client.slot]}
            self.ctx.hints[self.client.team, self.client.slot] = hints
            notify_hints(self.ctx, self.client.team, list(hints))
            return True
        else:
            item_name, usable, response = get_intended_text(item_or_location)
            if usable:
                if item_name in Items.hint_blacklist:
                    self.output(f"Sorry, \"{item_name}\" is marked as non-hintable.")
                    hints = []
                elif item_name in Items.item_name_groups:
                    hints = []
                    for item in Items.item_name_groups[item_name]:
                        hints.extend(collect_hints(self.ctx, self.client.team, self.client.slot, item))
                elif item_name in Items.item_table:  # item name
                    hints = collect_hints(self.ctx, self.client.team, self.client.slot, item_name)
                else:  # location name
                    hints = collect_hints_location(self.ctx, self.client.team, self.client.slot, item_name)

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
                        elif self.ctx.hint_cost:
                            can_pay = points_available // self.ctx.hint_cost
                        else:
                            can_pay = 1000

                        random.shuffle(not_found_hints)

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
                                    "Could not pay for everything. Rerun the hint later with more points to get the remaining hints.")
                            else:
                                self.output(f"You can't afford the hint. "
                                            f"You have {points_available} points and need at least "
                                            f"{self.ctx.hint_cost}")
                        notify_hints(self.ctx, self.client.team, hints)
                        self.ctx.save()
                        return True

                else:
                    self.output("Nothing found. Item/Location may not exist.")
                    return False
            else:
                self.output(response)
                return False


def get_client_points(ctx: Context, client: Client) -> int:
    return (ctx.location_check_points * len(ctx.location_checks[client.team, client.slot]) -
            ctx.hint_cost * ctx.hints_used[client.team, client.slot])

async def process_client_cmd(ctx: Context, client: Client, cmd, args):
    if type(cmd) is not str:
        await ctx.send_msgs(client, [['InvalidCmd']])
        return

    if cmd == 'Connect':
        if not args or type(args) is not dict or \
                'password' not in args or type(args['password']) not in [str, type(None)] or \
                'rom' not in args or type(args['rom']) not in (list, str):
            await ctx.send_msgs(client, [['InvalidArguments', 'Connect']])
            return

        errors = set()
        if ctx.password is not None and args['password'] != ctx.password:
            errors.add('InvalidPassword')
        if type(args["rom"]) == list:
            args["rom"] = bytes(letter for letter in args["rom"]).decode()
        if args['rom'] not in ctx.rom_names:
            errors.add('InvalidRom')
        else:
            team, slot = ctx.rom_names[args['rom']]
            # this can only ever be 0 or 1 elements
            clients = [c for c in ctx.endpoints if c.auth and c.slot == slot and c.team == team]
            if clients:
                # likely same player with a "ghosted" slot. We bust the ghost.
                if "uuid" in args and ctx.client_ids[team, slot] == args["uuid"]:
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
        if "AP" not in args.get('tags', Client.tags):
            errors.add('IncompatibleVersion')
        elif ctx.compatibility == 0 and args.get('version', Client.version) != list(_version_tuple):
            errors.add('IncompatibleVersion')
        if errors:
            logging.info(f"A client connection was refused due to: {errors}")
            await ctx.send_msgs(client, [['ConnectionRefused', list(errors)]])
        else:
            ctx.client_ids[client.team, client.slot] = args.get("uuid", None)
            client.auth = True
            client.version = args.get('version', Client.version)
            client.tags = args.get('tags', Client.tags)
            reply = [['Connected', [(client.team, client.slot),
                                    [(p, ctx.get_aliased_name(t, p)) for (t, p), n in ctx.player_names.items() if
                                     t == client.team]]]]
            items = get_received_items(ctx, client.team, client.slot)
            if items:
                reply.append(['ReceivedItems', (0, tuplize_received_items(items))])
                client.send_index = len(items)
            await ctx.send_msgs(client, reply)
            await on_client_joined(ctx, client)

    if client.auth:
        if cmd == 'Sync':
            items = get_received_items(ctx, client.team, client.slot)
            if items:
                client.send_index = len(items)
                await ctx.send_msgs(client, [['ReceivedItems', (0, tuplize_received_items(items))]])

        elif cmd == 'LocationChecks':
            if type(args) is not list:
                await ctx.send_msgs(client, [['InvalidArguments', 'LocationChecks']])
                return
            register_location_checks(ctx, client.team, client.slot, args)

        elif cmd == 'LocationScouts':
            if type(args) is not list:
                await ctx.send_msgs(client, [['InvalidArguments', 'LocationScouts']])
                return
            locs = []
            for location in args:
                if type(location) is not int or 0 >= location > len(Regions.location_table):
                    await ctx.send_msgs(client, [['InvalidArguments', 'LocationScouts']])
                    return
                loc_name = list(Regions.location_table.keys())[location - 1]
                target_item, target_player = ctx.locations[(Regions.location_table[loc_name][0], client.slot)]

                replacements = {'SmallKey': 0xA2, 'BigKey': 0x9D, 'Compass': 0x8D, 'Map': 0x7D}
                item_type = [i[2] for i in Items.item_table.values() if type(i[3]) is int and i[3] == target_item]
                if item_type:
                    target_item = replacements.get(item_type[0], target_item)

                locs.append([loc_name, location, target_item, target_player])

            # logging.info(f"{client.name} in team {client.team+1} scouted {', '.join([l[0] for l in locs])}")
            await ctx.send_msgs(client, [['LocationInfo', [l[1:] for l in locs]]])

        elif cmd == 'UpdateTags':
            if not args or type(args) is not list:
                await ctx.send_msgs(client, [['InvalidArguments', 'UpdateTags']])
                return
            client.tags = args

        elif cmd == 'GameFinished':
            if ctx.client_game_state[client.team, client.slot] != CLIENT_GOAL:
                finished_msg = f'{ctx.get_aliased_name(client.team, client.slot)} (Team #{client.team + 1}) has found the triforce.'
                ctx.notify_all(finished_msg)
                ctx.client_game_state[client.team, client.slot] = CLIENT_GOAL
                if "auto" in ctx.forfeit_mode:
                    forfeit_player(ctx, client.team, client.slot)

        if cmd == 'Say':
            if type(args) is not str or not args.isprintable():
                await ctx.send_msgs(client, [['InvalidArguments', 'Say']])
                return

            client.messageprocessor(args)


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
                self.output(f"Player {player_name} has to follow the server restrictions on use of the !forfeit command.")
                return True

        self.output(f"Could not find player {player_name} to forbid the !forfeit command for.")
        return False

    def _cmd_send(self, player_name: str, *item_name: str) -> bool:
        """Sends an item to the specified player"""
        seeked_player, usable, response = get_intended_text(player_name, self.ctx.player_names.values())
        if usable:
            item = " ".join(item_name)
            item, usable, response = get_intended_text(item, Items.item_table.keys())
            if usable:
                for client in self.ctx.endpoints:
                    if client.name == seeked_player:
                        new_item = ReceivedItem(Items.item_table[item][3], -1, client.slot)
                        get_received_items(self.ctx, client.team, client.slot).append(new_item)
                        self.ctx.notify_all('Cheat console: sending "' + item + '" to ' + self.ctx.get_aliased_name(client.team, client.slot))
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
            for (team, slot), name in self.ctx.player_names.items():
                if name == seeked_player:
                    item = " ".join(item_or_location)
                    item, usable, response = get_intended_text(item)
                    if usable:
                        if item in Items.item_name_groups:
                            hints = []
                            for item in Items.item_name_groups[item]:
                                hints.extend(collect_hints(self.ctx, team, slot, item))
                        elif item in Items.item_table:  # item name
                            hints = collect_hints(self.ctx, team, slot, item)
                        else:  # location name
                            hints = collect_hints_location(self.ctx, team, slot, item)
                        notify_hints(self.ctx, team, hints)
                        return True
                    else:
                        self.output(response)
                        return False

        else:
            self.output(response)
            return False

    def _cmd_option(self, option_name: str, option: str):
        """Set options for the server. Warning: expires on restart"""

        attrtype = self.simple_options.get(option_name, None)
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
            known = (f"{option}:{otype}" for option, otype in self.simple_options.items())
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
    parser.add_argument('--host', default=defaults["host"])
    parser.add_argument('--port', default=defaults["port"], type=int)
    parser.add_argument('--server_password', default=defaults["server_password"])
    parser.add_argument('--password', default=defaults["password"])
    parser.add_argument('--multidata', default=defaults["multidata"])
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
    #1 -> recommended for friendly racing, only allow Berserker's Multiworld, to disallow old /getitem for example
    #0 -> recommended for tournaments to force a level playing field, only allow an exact version match
    """)
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
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))

    ctx = Context(args.host, args.port, args.server_password, args.password, args.location_check_points,
                  args.hint_cost, not args.disable_item_cheat, args.forfeit_mode, args.remaining_mode,
                  args.auto_shutdown, args.compatibility)

    data_filename = args.multidata

    try:
        if not data_filename:
            import tkinter
            import tkinter.filedialog
            root = tkinter.Tk()
            root.withdraw()
            data_filename = tkinter.filedialog.askopenfilename(filetypes=(("Multiworld data", "*.multidata"),))

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
