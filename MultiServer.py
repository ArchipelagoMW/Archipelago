import argparse
import asyncio
import functools
import json
import logging
import re
import shlex
import urllib.request
import zlib

import ModuleUpdate
ModuleUpdate.update()

import websockets
import aioconsole

import Items
import Regions
from MultiClient import ReceivedItem, get_item_name_from_id, get_location_name_from_address

class Client:
    def __init__(self, socket):
        self.socket = socket
        self.auth = False
        self.name = None
        self.team = None
        self.slot = None
        self.send_index = 0

class Context:
    def __init__(self, host, port, password):
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

def notify_team(ctx : Context, team : int, text : str):
    logging.info("Notice (Team #%d): %s" % (team+1, text))
    broadcast_team(ctx, team, [['Print', text]])

def notify_client(client : Client, text : str):
    if not client.auth:
        return
    logging.info("Notice (Player %s in team %d): %s" % (client.name, client.team+1, text))
    asyncio.create_task(send_msgs(client.socket,  [['Print', text]]))

async def server(websocket, path, ctx : Context):
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

async def on_client_connected(ctx : Context, client : Client):
    await send_msgs(client.socket, [['RoomInfo', {
        'password': ctx.password is not None,
        'players': [(client.team, client.slot, client.name) for client in ctx.clients if client.auth]
    }]])

async def on_client_disconnected(ctx : Context, client : Client):
    if client.auth:
        await on_client_left(ctx, client)

async def on_client_joined(ctx : Context, client : Client):
    notify_all(ctx, "%s (Team #%d) has joined the game" % (client.name, client.team + 1))

async def on_client_left(ctx : Context, client : Client):
    notify_all(ctx, "%s (Team #%d) has left the game" % (client.name, client.team + 1))

async def countdown(ctx : Context, timer):
    notify_all(ctx, f'[Server]: Starting countdown of {timer}s')
    if ctx.countdown_timer:
        ctx.countdown_timer = timer
        return

    ctx.countdown_timer = timer
    while ctx.countdown_timer > 0:
        notify_all(ctx, f'[Server]: {ctx.countdown_timer}')
        ctx.countdown_timer -= 1
        await asyncio.sleep(1)
    notify_all(ctx, f'[Server]: GO')

def get_connected_players_string(ctx : Context):
    auth_clients = [c for c in ctx.clients if c.auth]
    if not auth_clients:
        return 'No player connected'

    auth_clients.sort(key=lambda c: (c.team, c.slot))
    current_team = 0
    text = 'Team #1: '
    for c in auth_clients:
        if c.team != current_team:
            text += f':: Team #{c.team + 1}: '
            current_team = c.team
        text += f'{c.name} '
    return 'Connected players: ' + text[:-1]

def get_received_items(ctx : Context, team, player):
    return ctx.received_items.setdefault((team, player), [])

def tuplize_received_items(items):
    return [(item.item, item.location, item.player) for item in items]

def send_new_items(ctx : Context):
    for client in ctx.clients:
        if not client.auth:
            continue
        items = get_received_items(ctx, client.team, client.slot)
        if len(items) > client.send_index:
            asyncio.create_task(send_msgs(client.socket, [['ReceivedItems', (client.send_index, tuplize_received_items(items)[client.send_index:])]]))
            client.send_index = len(items)

def forfeit_player(ctx : Context, team, slot):
    all_locations = [values[0] for values in Regions.location_table.values() if type(values[0]) is int]
    notify_all(ctx, "%s (Team #%d) has forfeited" % (ctx.player_names[(team, slot)], team + 1))
    register_location_checks(ctx, team, slot, all_locations)

def register_location_checks(ctx : Context, team, slot, locations):
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
                    logging.info('(Team #%d) %s sent %s to %s (%s)' % (team+1, ctx.player_names[(team, slot)], get_item_name_from_id(target_item), ctx.player_names[(team, target_player)], get_location_name_from_address(location)))
                    found_items = True
    send_new_items(ctx)

    if found_items and not ctx.disable_save:
        try:
            with open(ctx.save_filename, "wb") as f:
                jsonstr = json.dumps((list(ctx.rom_names.items()),
                                      [(k, [i.__dict__ for i in v]) for k, v in ctx.received_items.items()]))
                f.write(zlib.compress(jsonstr.encode("utf-8")))
        except Exception as e:
            logging.exception(e)

async def process_client_cmd(ctx : Context, client : Client, cmd, args):
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
            reply = [['Connected', [(client.team, client.slot), [(p, n) for (t, p), n in ctx.player_names.items() if t == client.team]]]]
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

    if cmd == 'Say':
        if type(args) is not str or not args.isprintable():
            await send_msgs(client.socket, [['InvalidArguments', 'Say']])
            return

        notify_all(ctx, client.name + ': ' + args)

        if args.startswith('!players'):
            notify_all(ctx, get_connected_players_string(ctx))
        if args.startswith('!forfeit'):
            forfeit_player(ctx, client.team, client.slot)
        if args.startswith('!countdown'):
            try:
                timer = int(args.split()[1])
            except (IndexError, ValueError):
                timer = 10
            asyncio.create_task(countdown(ctx, timer))

def set_password(ctx : Context, password):
    ctx.password = password
    logging.warning('Password set to ' + password if password is not None else 'Password disabled')

async def console(ctx : Context):
    while True:
        input = await aioconsole.ainput()
        try:

            command = shlex.split(input)
            if not command:
                continue

            if command[0] == '/exit':
                ctx.server.ws_server.close()
                break

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
            if command[0] == '/senditem' and len(command) > 2:
                [(player, item)] = re.findall(r'\S* (\S*) (.*)', input)
                if item in Items.item_table:
                    for client in ctx.clients:
                        if client.auth and client.name.lower() == player.lower():
                            new_item = ReceivedItem(Items.item_table[item][3], "cheat console", client.slot)
                            get_received_items(ctx, client.team, client.slot).append(new_item)
                            notify_all(ctx, 'Cheat console: sending "' + item + '" to ' + client.name)
                    send_new_items(ctx)
                else:
                    logging.warning("Unknown item: " + item)
            if command[0] == '/hint':
                for (team,slot), name in ctx.player_names.items():
                    if len(command) == 1:
                        print("Use /hint {Playername} {itemname}\nFor example /hint Berserker Lamp")
                    elif name.lower() == command[1].lower():
                        item = " ".join(command[2:])
                        if item in Items.item_table:
                            seeked_item_id = Items.item_table[item][3]
                            for check, result in ctx.locations.items():
                                item_id, receiving_player = result
                                if receiving_player == slot and item_id == seeked_item_id:
                                    location_id, finding_player = check
                                    name_finder = ctx.player_names[team, finding_player]
                                    hint = f"[Hint]: {name}'s {item} can be found at " \
                                           f"{get_location_name_from_address(location_id)} in {name_finder}'s World"
                                    notify_team(ctx, team, hint)
                        else:
                            logging.warning("Unknown item: " + item)
            if command[0][0] != '/':
                notify_all(ctx, '[Server]: ' + input)
        except:
            import traceback
            traceback.print_exc()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=None)
    parser.add_argument('--port', default=38281, type=int)
    parser.add_argument('--password', default=None)
    parser.add_argument('--multidata', default=None)
    parser.add_argument('--savefile', default=None)
    parser.add_argument('--disable_save', default=False, action='store_true')
    parser.add_argument('--loglevel', default='info', choices=['debug', 'info', 'warning', 'error', 'critical'])
    args = parser.parse_args()

    logging.basicConfig(format='[%(asctime)s] %(message)s', level=getattr(logging, args.loglevel.upper(), logging.INFO))

    ctx = Context(args.host, args.port, args.password)

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

    ip = urllib.request.urlopen('https://v4.ident.me').read().decode('utf8') if not ctx.host else ctx.host
    logging.info('Hosting game at %s:%d (%s)' % (ip, ctx.port, 'No password' if not ctx.password else 'Password: %s' % ctx.password))

    ctx.disable_save = args.disable_save
    if not ctx.disable_save:
        if not ctx.save_filename:
            ctx.save_filename = (ctx.data_filename[:-9] if ctx.data_filename[-9:] == 'multidata' else (ctx.data_filename + '_')) + 'multisave'
        try:
            with open(ctx.save_filename, 'rb') as f:
                jsonobj = json.loads(zlib.decompress(f.read()).decode("utf-8"))
                rom_names = jsonobj[0]
                received_items = {tuple(k): [ReceivedItem(**i) for i in v] for k, v in jsonobj[1]}
                if not all([ctx.rom_names[tuple(rom)] == (team, slot) for rom, (team, slot) in rom_names]):
                    raise Exception('Save file mismatch, will start a new game')
                ctx.received_items = received_items
                logging.info('Loaded save file with %d received items for %d players' % (sum([len(p) for p in received_items.values()]), len(received_items)))
        except FileNotFoundError:
            logging.error('No save data found, starting a new game')
        except Exception as e:
            logging.info(e)

    ctx.server = websockets.serve(functools.partial(server,ctx=ctx), ctx.host, ctx.port, ping_timeout=None, ping_interval=None)
    await ctx.server
    await console(ctx)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
    loop.close()
