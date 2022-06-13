from __future__ import annotations
import os
import logging
import asyncio
import string
import urllib.parse
import multiprocessing
import sys
import typing
import time

import websockets

import Utils

if __name__ == "__main__":
    Utils.init_logging("ffpsClient", exception_logger="Client")

from MultiServer import CommandProcessor
from NetUtils import Endpoint, decode, NetworkItem, encode, JSONtoTextParser, ClientStatus, Permission
from Utils import Version, stream_input
from worlds import network_data_package, AutoWorldRegister, ffps
from CommonClient import *
from worlds.ffps import FFPSWorld, item_table, advancement_table
import bsdiff4


class FFPSCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True

    def _cmd_patch(self):
        """Patch the vanilla game."""
        bsdiff4.file_patch(os.getcwd() + "/FFPS Game/Pizzeria Simulator.exe", os.getcwd() + "/FFPS Game/FFPS Mod.exe", ffps.data_path("patch.bsdiff"))
        self.output(f"Done!")


class FFPSContext(CommonContext):
    command_processor: int = FFPSCommandProcessor
    game = "FFPS"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.syncing = False
        self.max_anim = 4
        self.recieved_stages = 0
        self.recieved_cups = 0
        self.recieved_speakers = 0
        self.game = 'FFPS'

    async def connection_closed(self):
        await super().connection_closed()
        self.recieved_stages = 0
        self.recieved_cups = 0
        self.recieved_speakers = 0

    def on_package(self, cmd: str, args: dict):
        asyncio.create_task(process_ffps_cmd(self, cmd, args))

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(FFPSContext, self).server_auth(password_requested)
        if not self.auth:
            logger.info('Enter slot name:')
            self.auth = await self.console_input()

        await self.send_connect()


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
        ctx.connected_success = False
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


async def not_in_use(filename):
    try:
        os.rename(filename, filename)
        return True
    except:
        return False


async def process_ffps_cmd(ctx: FFPSContext, cmd: str, args: dict):
    if cmd == 'Connected':
        ctx.max_anim = args["slot_data"]["max_anim_appears"]
        path = os.path.expandvars("%appdata%/MMFApplications/FNAF6")
        if not os.path.exists(path):
            with open(path, "w") as f:
                f.close()

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
            if os.path.exists(os.path.expandvars("%appdata%/MMFApplications/FNAF6")):
                for item in args['items']:
                    while True:
                        try:
                            with open(os.path.expandvars("%appdata%/MMFApplications/FNAF6"), 'r+') as f:
                                lines = f.read()
                                item_got = item_table[FFPSWorld.item_id_to_name[NetworkItem(*item).item]].setId
                                if (lines.count("m2")+lines.count("m3")+lines.count("m4")+lines.count("m5")) < ctx.max_anim and (item_got == "m2" or item_got == "m3" or item_got == "m4" or item_got == "m5"):
                                    f.write(str(item_got)+"=1\n")
                                if not item_got == "m2" and not item_got == "m3" and not item_got == "m4" and not item_got == "m5" and not item_got == "speakers" and not item_got == "cups" and not item_got == "stage":
                                    f.write(str(item_got)+"=1\n")
                                if not lines.__contains__("stage="):
                                    f.write("stage=0\n")
                                if not lines.__contains__("cups="):
                                    f.write("cups=0\n")
                                if not lines.__contains__("speakers="):
                                    f.write("speakers=0\n")
                                if not lines.__contains__("money="):
                                    f.write("money=100\n")
                                if not lines.__contains__("first="):
                                    f.write("first=1\n")
                                if not lines.__contains__("night="):
                                    f.write("night=1\n")
                                if not lines.__contains__("phase="):
                                    f.write("phase=1\n")
                                f.close()
                            break
                        except PermissionError:
                            continue
                    while True:
                        try:
                            with open(os.path.expandvars("%appdata%/MMFApplications/FNAF6"), "r") as file:
                                replacement = ""
                                for line in file:
                                    line = line.strip()
                                    if item_table[FFPSWorld.item_id_to_name[NetworkItem(*item).item]].setId == "stage":
                                        if line.__contains__("stage="):
                                            ctx.recieved_stages += 1
                                            changes = line.replace("stage="+line[line.find("stage=")+6], "stage="+str(ctx.recieved_stages))
                                        else:
                                            changes = line
                                    elif item_table[FFPSWorld.item_id_to_name[NetworkItem(*item).item]].setId == "cups":
                                        if line.__contains__("cups="):
                                            ctx.recieved_cups += 1
                                            changes = line.replace("cups="+line[line.find("cups=")+5], "cups="+str(ctx.recieved_cups))
                                        else:
                                            changes = line
                                    elif item_table[FFPSWorld.item_id_to_name[NetworkItem(*item).item]].setId == "speakers":
                                        if line.__contains__("speakers="):
                                            ctx.recieved_speakers += 1
                                            changes = line.replace("speakers="+line[line.find("speakers=")+9], "speakers="+str(ctx.recieved_speakers))
                                        else:
                                            changes = line
                                    else:
                                        changes = line
                                    replacement = replacement + changes + "\n"
                                file.close()
                            break
                        except PermissionError:
                            continue
                    lines_to_simplify = replacement.splitlines()
                    temp_lines = []
                    if lines_to_simplify.count("[FNAF6]") <= 0:
                        temp_lines.append("[FNAF6]\n")
                    for ln in lines_to_simplify:
                        if temp_lines.count(ln+"\n") <= 0:
                            temp_lines.append(ln+"\n")
                    anim_count = 0
                    for itm in ctx.items_received:
                        if item_table[FFPSWorld.item_id_to_name[itm.item]].setId == "m2" or item_table[FFPSWorld.item_id_to_name[itm.item]].setId == "m3" or item_table[FFPSWorld.item_id_to_name[itm.item]].setId == "m4" or item_table[FFPSWorld.item_id_to_name[itm.item]].setId == "m5":
                            anim_count += 1
                    if anim_count >= 4:
                        temp_lines.append("canWin=1\n")
                    lines_to_simplify = temp_lines
                    while True:
                        try:
                            with open(os.path.expandvars("%appdata%/MMFApplications/FNAF6"), "w") as fout:
                                fout.writelines(lines_to_simplify)
                                fout.close()
                            break
                        except PermissionError:
                            continue
                    ctx.items_received.append(NetworkItem(*item))
        ctx.watcher_event.set()


async def game_watcher(ctx: FFPSContext):
    while not ctx.exit_event.is_set():
        if ctx.syncing:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        path = os.path.expandvars("%appdata%/MMFApplications/FNAF6BOUGHT")
        sending = []
        victory = False
        while True:
            try:
                with open(os.path.expandvars("%appdata%/MMFApplications/FNAF6"), 'r+') as f:
                    lines = f.read()
                    if not lines.__contains__("stage="):
                        f.write("stage=0\n")
                    if not lines.__contains__("cups="):
                        f.write("cups=0\n")
                    if not lines.__contains__("speakers="):
                        f.write("speakers=0\n")
                    if not lines.__contains__("money="):
                        f.write("money=100\n")
                    if not lines.__contains__("first="):
                        f.write("first=1\n")
                    if not lines.__contains__("night="):
                        f.write("night=1\n")
                    if not lines.__contains__("phase="):
                        f.write("phase=1\n")
                    f.close()
                break
            except PermissionError:
                continue
        while True:
            try:
                with open(path, 'r') as f:
                    filesread = f.read()
                    for name, data in advancement_table.items():
                        if data.setId == "stage" or data.setId == "cups" or data.setId == "speakers":
                            for i in range(int([int(s) for s in name.split() if s.isdigit()][0]), 10):
                                if data.setId+"="+str(i) in filesread and not str(data.id)+"=sent" in filesread:
                                    sending = sending+[(int(data.id))]
                                    break
                        elif data.setId in filesread and data.setId != "" and not str(data.id)+"=sent" in filesread:
                            sending = sending+[(int(data.id))]
                    f.close()
                break
            except PermissionError:
                continue
        while True:
            try:
                with open(path, 'r+') as f:
                    f.read()
                    for itm in sending:
                        f.write(str(itm)+"=sent\n")
                    f.close()
                break
            except PermissionError:
                continue
        path = os.path.expandvars("%appdata%/MMFApplications/VICTORYFFPS")
        if os.path.exists(path):
            while True:
                try:
                    with open(path, 'r+') as f:
                        filesread = f.readlines()
                        if filesread.__contains__("[FIN]\n") and filesread.__contains__("fin=1\n"):
                            victory = True
                        f.close()
                    break
                except PermissionError:
                    continue
        if victory:
            os.remove(path)
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    async def main():
        multiprocessing.freeze_support()
        parser = get_base_parser()
        parser.add_argument('apz5_file', default="", type=str, nargs="?",
                            help='Path to an APZ5 file')
        args = parser.parse_args()

        ctx = FFPSContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        if not os.path.exists(os.getcwd() + "/FFPS Game"):
            os.mkdir(os.getcwd() + "/FFPS Game")

        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="FFPSProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        await progression_watcher

    import colorama

    parser = get_base_parser(description="FFPS Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()

    asyncio.run(main())
    colorama.deinit()
