import argparse
import asyncio
import functools
import json
import logging
import zlib
import collections
import typing

import ModuleUpdate

ModuleUpdate.update()

import websockets
import prompt_toolkit
from prompt_toolkit.patch_stdout import patch_stdout
from fuzzywuzzy import process as fuzzy_process

import Items
import Regions
import Utils
from MultiClient import ReceivedItem, get_item_name_from_id, get_location_name_from_address

console_names = frozenset(set(Items.item_table) | set(Regions.location_table))


class Client:
    version: typing.List[int] = [0, 0, 0]
    tags: typing.List[str] = []

    def __init__(self, socket: websockets.server.WebSocketServerProtocol):
        self.socket = socket
        self.auth = False
        self.name = None
        self.team = None
        self.slot = None
        self.send_index = 0
        self.tags = []
        self.version = [0, 0, 0]

    @property
    def wants_item_notification(self):
        return self.auth and "FoundItems" in self.tags


class Context:
    def __init__(self, host: str, port: int, password: str, location_check_points: int, hint_cost: int,
                 item_cheat: bool):
        self.data_filename = None
        self.save_filename = None
        self.disable_save = False
        self.player_names = {}
        self.rom_names = {}
        self.remote_items = set()
        self.locations = {}
        self.host = host
        self.port = port
        self.password = password
        self.server = None
        self.countdown_timer = 0
        self.clients = []
        self.received_items = {}
        self.location_checks = collections.defaultdict(set)
        self.hint_cost = hint_cost
        self.location_check_points = location_check_points
        self.hints_used = collections.defaultdict(int)
        self.hints_sent = collections.defaultdict(set)
        self.item_cheat = item_cheat

    def get_save(self) -> dict:
        return {
            "rom_names": list(self.rom_names.items()),
            "received_items": tuple((k, v) for k, v in self.received_items.items()),
            "hints_used" : tuple((key,value) for key, value in self.hints_used.items()),
            "hints_sent" : tuple((key,tuple(value)) for key, value in self.hints_sent.items()),
            "location_checks" : tuple((key,tuple(value)) for key, value in self.location_checks.items())
        }

    def set_save(self, savedata: dict):
        rom_names = savedata["rom_names"]
        received_items = {tuple(k): [ReceivedItem(*i) for i in v] for k, v in savedata["received_items"]}
        if not all([self.rom_names[tuple(rom)] == (team, slot) for rom, (team, slot) in rom_names]):
            raise Exception('Save file mismatch, will start a new game')
        self.received_items = received_items
        self.hints_used.update({tuple(key): value for key, value in savedata["hints_used"]})
        self.hints_sent.update({tuple(key): set(value) for key, value in savedata["hints_sent"]})
        self.location_checks.update({tuple(key): set(value) for key, value in savedata["location_checks"]})
        logging.info(f'Loaded save file with {sum([len(p) for p in received_items.values()])} received items '
                     f'for {len(received_items)} players')


async def send_msgs(websocket, msgs):
    if not websocket or not websocket.open or websocket.closed:
        return
    try:
        await websocket.send(json.dumps(msgs))
    except websockets.ConnectionClosed:
        pass

def broadcast_all(ctx : Context, msgs):
    for client in ctx.clients:
        if client.auth:
            asyncio.create_task(send_msgs(client.socket, msgs))

def broadcast_team(ctx : Context, team, msgs):
    for client in ctx.clients:
        if client.auth and client.team == team:
            asyncio.create_task(send_msgs(client.socket, msgs))

def notify_all(ctx : Context, text):
    logging.info("Notice (all): %s" % text)
    broadcast_all(ctx, [['Print', text]])


def notify_team(ctx: Context, team: int, text: str):
    logging.info("Notice (Team #%d): %s" % (team + 1, text))
    broadcast_team(ctx, team, [['Print', text]])


def notify_client(client: Client, text: str):
    if not client.auth:
        return
    logging.info("Notice (Player %s in team %d): %s" % (client.name, client.team + 1, text))
    asyncio.create_task(send_msgs(client.socket, [['Print', text]]))


# separated out, due to compatibilty between client's
def notify_hints(ctx: Context, team: int, hints: typing.List[Utils.Hint]):
    cmd = [["Hint", hints]]
    texts = [['Print', format_hint(ctx, team, hint)] for hint in hints]
    for _, text in texts:
        logging.info("Notice (Team #%d): %s" % (team + 1, text))
    for client in ctx.clients:
        if client.auth and client.team == team:
            if "Berserker" in client.tags:
                payload = cmd
            else:
                payload = texts
            asyncio.create_task(send_msgs(client.socket, payload))

async def server(websocket, path, ctx: Context):
    client = Client(websocket)
    ctx.clients.append(client)

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
        await on_client_disconnected(ctx, client)
        ctx.clients.remove(client)

async def on_client_connected(ctx: Context, client: Client):
    await send_msgs(client.socket, [['RoomInfo', {
        'password': ctx.password is not None,
        'players': [(client.team, client.slot, client.name) for client in ctx.clients if client.auth],
        # tags are for additional features in the communication.
        # Name them by feature or fork, as you feel is appropriate.
        'tags': ['Berserker'],
        'version': [1, 2, 0]
    }]])

async def on_client_disconnected(ctx: Context, client: Client):
    if client.auth:
        await on_client_left(ctx, client)

async def on_client_joined(ctx: Context, client: Client):
    notify_all(ctx, "%s (Team #%d) has joined the game. Client(%s, %s)." % (client.name, client.team + 1,
                                                                            ".".join(str(x) for x in client.version),
                                                                            client.tags))

async def on_client_left(ctx: Context, client: Client):
    notify_all(ctx, "%s (Team #%d) has left the game" % (client.name, client.team + 1))

async def countdown(ctx: Context, timer):
    notify_all(ctx, f'[Server]: Starting countdown of {timer}s')
    if ctx.countdown_timer:
        ctx.countdown_timer = timer  # timer is already running, set it to a different time
    else:
        ctx.countdown_timer = timer
        while ctx.countdown_timer > 0:
            notify_all(ctx, f'[Server]: {ctx.countdown_timer}')
            ctx.countdown_timer -= 1
            await asyncio.sleep(1)
        notify_all(ctx, f'[Server]: GO')

def get_connected_players_string(ctx: Context):
    auth_clients = {(c.team, c.slot) for c in ctx.clients if c.auth}

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
    for client in ctx.clients:
        if not client.auth:
            continue
        items = get_received_items(ctx, client.team, client.slot)
        if len(items) > client.send_index:
            asyncio.create_task(send_msgs(client.socket, [['ReceivedItems', (client.send_index, tuplize_received_items(items)[client.send_index:])]]))
            client.send_index = len(items)


def forfeit_player(ctx: Context, team: int, slot: int):
    all_locations = {values[0] for values in Regions.location_table.values() if type(values[0]) is int}
    notify_all(ctx, "%s (Team #%d) has forfeited" % (ctx.player_names[(team, slot)], team + 1))
    register_location_checks(ctx, team, slot, all_locations)


def register_location_checks(ctx: Context, team: int, slot: int, locations):
    found_items = False
    for location in locations:
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
                        broadcast_team(ctx, team, [['ItemSent', (slot, location, target_player, target_item)]])
                    logging.info('(Team #%d) %s sent %s to %s (%s)' % (
                    team + 1, ctx.player_names[(team, slot)], get_item_name_from_id(target_item),
                    ctx.player_names[(team, target_player)], get_location_name_from_address(location)))
                    found_items = True
            elif target_player == slot:  # local pickup, notify clients of the pickup
                if location not in ctx.location_checks[team, slot]:
                    for client in ctx.clients:
                        if client.team == team and client.wants_item_notification:
                            asyncio.create_task(
                                send_msgs(client.socket, [['ItemFound', (target_item, location, slot)]]))
    ctx.location_checks[team, slot] |= set(locations)
    send_new_items(ctx)

    if found_items:
        save(ctx)


def save(ctx: Context):
    if not ctx.disable_save:
        try:
            jsonstr = json.dumps(ctx.get_save())
            with open(ctx.save_filename, "wb") as f:
                f.write(zlib.compress(jsonstr.encode("utf-8")))
        except Exception as e:
            logging.exception(e)


def collect_hints(ctx: Context, team: int, slot: int, item: str) -> typing.List[Utils.Hint]:
    hints = []
    seeked_item_id = Items.item_table[item][3]
    for check, result in ctx.locations.items():
        item_id, receiving_player = result
        if receiving_player == slot and item_id == seeked_item_id:
            location_id, finding_player = check
            found = location_id in ctx.location_checks[team, finding_player]
            hints.append(Utils.Hint(receiving_player, finding_player, location_id, item_id, found))

    return hints


def collect_hints_location(ctx: Context, team: int, slot: int, location: str) -> typing.List[Utils.Hint]:
    hints = []
    seeked_location = Regions.location_table[location][0]
    for check, result in ctx.locations.items():
        location_id, finding_player = check
        if finding_player == slot and location_id == seeked_location:
            item_id, receiving_player = result
            found = location_id in ctx.location_checks[team, finding_player]
            hints.append(Utils.Hint(receiving_player, finding_player, location_id, item_id, found))
            break # each location has 1 item
    return hints


def format_hint(ctx: Context, team: int, hint: Utils.Hint) -> str:
    return f"[Hint]: {ctx.player_names[team, hint.receiving_player]}'s " \
           f"{Items.lookup_id_to_name[hint.item]} can be found " \
           f"at {get_location_name_from_address(hint.location)} " \
           f"in {ctx.player_names[team, hint.finding_player]}'s World." \
           + (" (found)" if hint.found else "")


def get_intended_text(input_text: str, possible_answers: typing.Iterable[str]= console_names) -> typing.Tuple[str, bool, str]:
    picks = fuzzy_process.extract(input_text, possible_answers, limit=2)
    dif = picks[0][1] - picks[1][1]
    if picks[0][1] == 100:
        return picks[0][0], True, "Perfect Match"
    elif picks[0][1] < 75:
        return picks[0][0], False, f"Didn't find something that closely matches, did you mean {picks[0][0]}?"
    elif dif > 5:
        return picks[0][0], True, "Close Match"
    else:
        return picks[0][0], False, f"Too many close matches, did you mean {picks[0][0]}?"


async def process_client_cmd(ctx: Context, client: Client, cmd, args):
    if type(cmd) is not str:
        await send_msgs(client.socket, [['InvalidCmd']])
        return

    if cmd == 'Connect':
        if not args or type(args) is not dict or \
                'password' not in args or type(args['password']) not in [str, type(None)] or \
                'rom' not in args or type(args['rom']) is not list:
            await send_msgs(client.socket, [['InvalidArguments', 'Connect']])
            return

        errors = set()
        if ctx.password is not None and args['password'] != ctx.password:
            errors.add('InvalidPassword')

        if tuple(args['rom']) not in ctx.rom_names:
            errors.add('InvalidRom')
        else:
            team, slot = ctx.rom_names[tuple(args['rom'])]
            if any([c.slot == slot and c.team == team for c in ctx.clients if c.auth]):
                errors.add('SlotAlreadyTaken')
            else:
                client.name = ctx.player_names[(team, slot)]
                client.team = team
                client.slot = slot

        if errors:
            await send_msgs(client.socket, [['ConnectionRefused', list(errors)]])
        else:
            client.auth = True
            client.version = args.get('version', Client.version)
            client.tags = args.get('tags', Client.tags)
            reply = [['Connected', [(client.team, client.slot),
                                    [(p, n) for (t, p), n in ctx.player_names.items() if t == client.team]]]]
            items = get_received_items(ctx, client.team, client.slot)
            if items:
                reply.append(['ReceivedItems', (0, tuplize_received_items(items))])
                client.send_index = len(items)
            await send_msgs(client.socket, reply)
            await on_client_joined(ctx, client)

    if not client.auth:
        return

    if cmd == 'Sync':
        items = get_received_items(ctx, client.team, client.slot)
        if items:
            client.send_index = len(items)
            await send_msgs(client.socket, [['ReceivedItems', (0, tuplize_received_items(items))]])

    if cmd == 'LocationChecks':
        if type(args) is not list:
            await send_msgs(client.socket, [['InvalidArguments', 'LocationChecks']])
            return
        register_location_checks(ctx, client.team, client.slot, args)

    if cmd == 'LocationScouts':
        if type(args) is not list:
            await send_msgs(client.socket, [['InvalidArguments', 'LocationScouts']])
            return
        locs = []
        for location in args:
            if type(location) is not int or 0 >= location > len(Regions.location_table):
                await send_msgs(client.socket, [['InvalidArguments', 'LocationScouts']])
                return
            loc_name = list(Regions.location_table.keys())[location - 1]
            target_item, target_player = ctx.locations[(Regions.location_table[loc_name][0], client.slot)]

            replacements = {'SmallKey': 0xA2, 'BigKey': 0x9D, 'Compass': 0x8D, 'Map': 0x7D}
            item_type = [i[2] for i in Items.item_table.values() if type(i[3]) is int and i[3] == target_item]
            if item_type:
                target_item = replacements.get(item_type[0], target_item)

            locs.append([loc_name, location, target_item, target_player])

        logging.info(f"{client.name} in team {client.team+1} scouted {', '.join([l[0] for l in locs])}")
        await send_msgs(client.socket, [['LocationInfo', [l[1:] for l in locs]]])

    if cmd == 'UpdateTags':
        if not args or type(args) is not list:
            await send_msgs(client.socket, [['InvalidArguments', 'UpdateTags']])
            return
        client.tags = args

    if cmd == 'Say':
        if type(args) is not str or not args.isprintable():
            await send_msgs(client.socket, [['InvalidArguments', 'Say']])
            return

        notify_all(ctx, client.name + ': ' + args)

        if args.startswith('!players'):
            notify_all(ctx, get_connected_players_string(ctx))
        elif args.startswith('!forfeit'):
            forfeit_player(ctx, client.team, client.slot)
        elif args.startswith('!countdown'):
            try:
                timer = int(args.split()[1])
            except (IndexError, ValueError):
                timer = 10
            asyncio.create_task(countdown(ctx, timer))
        elif args.startswith('!getitem') and ctx.item_cheat:
            item_name = args[9:].lower()
            item_name, usable, response = get_intended_text(item_name, Items.item_table.keys())
            if usable:
                new_item = ReceivedItem(Items.item_table[item_name][3], -1, client.slot)
                get_received_items(ctx, client.team, client.slot).append(new_item)
                notify_all(ctx, 'Cheat console: sending "' + item_name + '" to ' + client.name)
                send_new_items(ctx)
            else:
                notify_client(client, response)
        elif args.startswith("!hint"):
            points_available = ctx.location_check_points * len(ctx.location_checks[client.team, client.slot]) - \
                               ctx.hint_cost * ctx.hints_used[client.team, client.slot]
            item_name = args[6:]

            if not item_name:
                notify_client(client, "Use !hint {item_name/location_name}, "
                                      "for example !hint Lamp or !hint Link's House. "
                                      f"A hint costs {ctx.hint_cost} points. "
                                      f"You have {points_available} points.")
                for item_name in ctx.hints_sent[client.team, client.slot]:
                    if item_name in Items.item_table:  # item name
                        hints = collect_hints(ctx, client.team, client.slot, item_name)
                    else:  # location name
                        hints = collect_hints_location(ctx, client.team, client.slot, item_name)
                    notify_hints(ctx, client.team, hints)
            else:
                item_name, usable, response = get_intended_text(item_name)
                if usable:
                    if item_name in Items.hint_blacklist:
                        notify_client(client, f"Sorry, \"{item_name}\" is marked as non-hintable.")
                        hints = []
                    elif item_name in Items.item_table:  # item name
                        hints = collect_hints(ctx, client.team, client.slot, item_name)
                    else:  # location name
                        hints = collect_hints_location(ctx, client.team, client.slot, item_name)

                    if hints:
                        if item_name in ctx.hints_sent[client.team, client.slot]:
                            notify_hints(ctx, client.team, hints)
                            notify_client(client, "Hint was previously used, no points deducted.")
                        else:
                            found = 0
                            for hint in hints:
                                found += 1 - hint.found
                            if not found:
                                notify_hints(ctx, client.team, hints)
                                notify_client(client, "No new items found, no points deducted.")
                            else:
                                if ctx.hint_cost:
                                    can_pay = points_available // (ctx.hint_cost * found) >= 1
                                else:
                                    can_pay = True

                                if can_pay:
                                    ctx.hints_used[client.team, client.slot] += found
                                    ctx.hints_sent[client.team, client.slot].add(item_name)
                                    notify_hints(ctx, client.team, hints)
                                    save(ctx)
                                else:
                                    notify_client(client, f"You can't afford the hint. "
                                                          f"You have {points_available} points and need at least {ctx.hint_cost}, "
                                                          f"more if multiple items are still to be found.")
                    else:
                        notify_client(client, "Nothing found. Item/Location may not exist.")
                else:
                    notify_client(client, response)


def set_password(ctx : Context, password):
    ctx.password = password
    logging.warning('Password set to ' + password if password else 'Password disabled')


async def console(ctx: Context):
    session = prompt_toolkit.PromptSession()
    running = True
    while running:
        with patch_stdout():
            input_text = await session.prompt_async()
        try:

            command = input_text.split()
            if not command:
                continue

            if command[0] == '/exit':
                await ctx.server.ws_server._close()
                running = False

            if command[0] == '/players':
                logging.info(get_connected_players_string(ctx))
            if command[0] == '/password':
                set_password(ctx, command[1] if len(command) > 1 else None)
            if command[0] == '/kick' and len(command) > 1:
                team = int(command[2]) - 1 if len(command) > 2 and command[2].isdigit() else None
                for client in ctx.clients:
                    if client.auth and client.name.lower() == command[1].lower() and (team is None or team == client.team):
                        if client.socket and not client.socket.closed:
                            await client.socket.close()

            if command[0] == '/forfeitslot' and len(command) > 1 and command[1].isdigit():
                if len(command) > 2 and command[2].isdigit():
                    team = int(command[1]) - 1
                    slot = int(command[2])
                else:
                    team = 0
                    slot = int(command[1])
                forfeit_player(ctx, team, slot)
            if command[0] == '/forfeitplayer' and len(command) > 1:
                seeked_player = command[1].lower()
                for (team, slot), name in ctx.player_names.items():
                    if name.lower() == seeked_player:
                        forfeit_player(ctx, team, slot)
            if command[0] == '/senditem':
                if len(command) <= 2:
                    logging.info("Use /senditem {Playername} {itemname}\nFor example /senditem Berserker Lamp")
                else:
                    seeked_player, usable, response = get_intended_text(command[1], ctx.player_names.values())
                    if usable:
                        item = " ".join(command[2:])
                        item, usable, response = get_intended_text(item, Items.item_table.keys())
                        if usable:
                            for client in ctx.clients:
                                if client.name == seeked_player:
                                    new_item = ReceivedItem(Items.item_table[item][3], -1, client.slot)
                                    get_received_items(ctx, client.team, client.slot).append(new_item)
                                    notify_all(ctx, 'Cheat console: sending "' + item + '" to ' + client.name)
                            send_new_items(ctx)
                        else:
                            logging.warning(response)
                    else:
                        logging.warning(response)
            if command[0] == '/hint':
                if len(command) <= 2:
                    logging.info("Use /hint {Playername} {itemname/locationname}\nFor example /hint Berserker Lamp")
                else:
                    seeked_player, usable, response = get_intended_text(command[1], ctx.player_names.values())
                    if usable:
                        for (team, slot), name in ctx.player_names.items():
                            if name == seeked_player:
                                item = " ".join(command[2:])
                                item, usable, response = get_intended_text(item)
                                if usable:
                                    if item in Items.item_table: #item name
                                        hints = collect_hints(ctx, team, slot, item)
                                        notify_hints(ctx, team, hints)
                                    else: #location name
                                        hints = collect_hints_location(ctx, team, slot, item)
                                        notify_hints(ctx, team, hints)
                                else:
                                    logging.warning(response)
                    else:
                        logging.warning(response)

            if command[0][0] != '/':
                notify_all(ctx, '[Server]: ' + input_text)
        except:
            import traceback
            traceback.print_exc()


async def forward_port(port: int):
    import upnpy
    import socket

    upnp = upnpy.UPnP()
    upnp.discover()
    device = upnp.get_igd()

    service = device['WANPPPConnection.1']

    # get own lan IP
    ip = socket.gethostbyname(socket.gethostname())

    # This specific action returns an empty dict: {}
    service.AddPortMapping(
        NewRemoteHost='',
        NewExternalPort=port,
        NewProtocol='TCP',
        NewInternalPort=port,
        NewInternalClient=ip,
        NewEnabled=1,
        NewPortMappingDescription='Berserker\'s Multiworld',
        NewLeaseDuration=60 * 60 * 24  # 24 hours
    )

    logging.info(f"Attempted to forward port {port} to {ip}, your local ip address.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    defaults = Utils.get_options()["server_options"]
    parser.add_argument('--host', default=defaults["host"])
    parser.add_argument('--port', default=defaults["port"], type=int)
    parser.add_argument('--password', default=defaults["password"])
    parser.add_argument('--multidata', default=defaults["multidata"])
    parser.add_argument('--savefile', default=defaults["savefile"])
    parser.add_argument('--disable_save', default=defaults["disable_save"], action='store_true')
    parser.add_argument('--loglevel', default=defaults["loglevel"],
                        choices=['debug', 'info', 'warning', 'error', 'critical'])
    parser.add_argument('--location_check_points', default=defaults["location_check_points"], type=int)
    parser.add_argument('--hint_cost', default=defaults["hint_cost"], type=int)
    parser.add_argument('--disable_item_cheat', default=defaults["disable_item_cheat"], action='store_true')
    parser.add_argument('--port_forward', default=defaults["port_forward"], action='store_true')
    args = parser.parse_args()
    return args


async def main(args: argparse.Namespace):
    logging.basicConfig(format='[%(asctime)s] %(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))
    portforwardtask = None
    if args.port_forward:
        portforwardtask = asyncio.create_task(forward_port(args.port))

    ctx = Context(args.host, args.port, args.password, args.location_check_points, args.hint_cost,
                  not args.disable_item_cheat)

    ctx.data_filename = args.multidata

    try:
        if not ctx.data_filename:
            import tkinter
            import tkinter.filedialog
            root = tkinter.Tk()
            root.withdraw()
            ctx.data_filename = tkinter.filedialog.askopenfilename(filetypes=(("Multiworld data","*multidata"),))

        with open(ctx.data_filename, 'rb') as f:
            jsonobj = json.loads(zlib.decompress(f.read()).decode("utf-8"))
            for team, names in enumerate(jsonobj['names']):
                for player, name in enumerate(names, 1):
                    ctx.player_names[(team, player)] = name
            ctx.rom_names = {tuple(rom): (team, slot) for slot, team, rom in jsonobj['roms']}
            ctx.remote_items = set(jsonobj['remote_items'])
            ctx.locations = {tuple(k): tuple(v) for k, v in jsonobj['locations']}
    except Exception as e:
        logging.error('Failed to read multiworld data (%s)' % e)
        return

    ip = args.host if args.host else Utils.get_public_ipv4()



    ctx.disable_save = args.disable_save
    if not ctx.disable_save:
        if not ctx.save_filename:
            ctx.save_filename = (ctx.data_filename[:-9] if ctx.data_filename[-9:] == 'multidata' else (
                    ctx.data_filename + '_')) + 'multisave'
        try:
            with open(ctx.save_filename, 'rb') as f:
                jsonobj = json.loads(zlib.decompress(f.read()).decode("utf-8"))
                ctx.set_save(jsonobj)
        except FileNotFoundError:
            logging.error('No save data found, starting a new game')
        except Exception as e:
            logging.exception(e)
    if portforwardtask:
        try:
            await portforwardtask
        except:
            logging.exception("Automatic port forwarding failed with:")
    ctx.server = websockets.serve(functools.partial(server, ctx=ctx), ctx.host, ctx.port, ping_timeout=None,
                                  ping_interval=None)
    logging.info('Hosting game at %s:%d (%s)' % (ip, ctx.port,
                                                 'No password' if not ctx.password else 'Password: %s' % ctx.password))
    await ctx.server
    await console(ctx)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(parse_args()))
    loop.close()
