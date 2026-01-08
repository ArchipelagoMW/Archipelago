import asyncio
import subprocess
import json
import time
import os
import bsdiff4
import urllib.parse
import aiohttp.web
from argparse import ArgumentParser, Namespace

import Utils
from NetUtils import ClientStatus, RawJSONtoTextParser
from CommonClient import (
    CommonContext,
    gui_enabled,
    logger,
    get_base_parser,
    server_loop,
    ClientCommandProcessor,
)

from .Items import item_table
from .ERData import er_entrances, game_entrances
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as SuperContext
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as SuperContext

try:
    from CommonClient import handle_url_arg
except ImportError:
    # back compat, can delete once 0.6.0 is old enough
    def handle_url_arg(args: Namespace, parser: ArgumentParser | None = None) -> Namespace:
        """
        Parse the url arg "archipelago://name:pass@host:port" from launcher into correct launch args for CommonClient
        If alternate data is required the urlparse response is saved back to args.url if valid
        """
        if not args.url:
            return args

        url = urllib.parse.urlparse(args.url)
        if url.scheme != "archipelago":
            if not parser:
                parser = get_base_parser()
            parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")
            return args

        args.url = url
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

        return args


def check_locations(ctx: CommonContext, request: list[int]) -> json:
    # Back compat, remove when 0.6.2 is old enough
    needed_updates = set(request).difference(
        ctx.locations_checked)
    locationmessage = [{
        "cmd": "LocationChecks",
        "locations": list(needed_updates)
        }]
    return locationmessage


DEBUG = False
GAMENAME = "Minit"
ITEMS_HANDLING = 0b111
PATCH_VERSION = 1.0


def data_path(file_name: str):
    import pkgutil
    return pkgutil.get_data(__name__, "data/" + file_name)


class MinitCommandProcessor(ClientCommandProcessor):

    def _cmd_patch(self):
        """Patch and launch the game."""
        if isinstance(self.ctx, ProxyGameContext):
            self.ctx.patch_game()

    def _cmd_amnisty(self, total: int = 1):
        """Set the Death Amnisty value. Default 1."""
        self.ctx.death_amnisty_total = int(total)
        self.ctx.death_amnisty_count = 0
        logger.info(f"Amnisty set to {self.ctx.death_amnisty_total}. \
            Deaths towards Amnisty reset.")


class ProxyGameContext(SuperContext):
    game = GAMENAME
    httpServer_task: asyncio.Task[None] | None = None
    command_processor = MinitCommandProcessor
    tags = set()
    last_sent_death: float = time.time()
    slot_data: dict[str, any]
    death_amnisty_total: int
    death_amnisty_count: int
    goals: list[str]

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.gamejsontotext = RawJSONtoTextParser(self)
        self.items_handling = ITEMS_HANDLING
        self.locations_checked = []
        self.datapackage = []
        self.death_amnisty_total = 1  # should be rewritten by slot data
        self.death_amnisty_count = 0

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = "Minit Client"
        return ui

    def patch_game(self):
        from . import MinitWorld
        try:
            data_file = MinitWorld.settings.data_file
            data_file.validate(data_file)
        except FileNotFoundError:
            logger.info("Patch cancelled")
            # TODO: consider clearing the path since the one we were given is invalid
            return
        except ValueError:
            logger.info("Selected game is not vanilla, please reset the game and repatch")
            # TODO: consider clearing the path since the one we were given is invalid
            return

        basepath = os.path.dirname(data_file)
        patched_name = f"ap_v{PATCH_VERSION}_data.win"
        patched_path = os.path.join(basepath, patched_name)

        if not os.path.isfile(patched_path):
            with open(data_file, "rb") as f:
                patchedFile = bsdiff4.patch(f.read(), data_path("patch.bsdiff"))
            with open(patched_path, "wb") as f:
                f.write(patchedFile)
            logger.info("Patch complete")
        else:
            logger.info("Found patched file, skipping patching process")
        exe_path = os.path.join(basepath, "minit.exe")
        if not os.path.isfile(exe_path):
            exe_path = os.path.join(basepath, "minitGMS2.exe")
            if not os.path.isfile(exe_path):
                logger.info("No known Minit executible in the install folder")
                return
        subprocess.Popen([exe_path, "-game", patched_path])

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == 'Connected':
            self.slot_data = args["slot_data"]
            self.death_amnisty_total = self.slot_data["death_amnisty_total"]
            # if load(ctx.locations_info):
            #     load(ctx.locations_info)
            # else:
            Utils.async_start(self.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.missing_locations),
                "create_as_hint": 0
                }]))
            self.goals = self.slot_data["goals"]
            Utils.async_start(self.update_death_link(self.slot_data["death_link"]))

        # if cmd == 'LocationInfo':
        #     save(ctx.locations_info)
        # if cmd == 'ReceivedItems':
        #     #TODO make this actually send minit a ping
        #      - or check if it can be handled with ctx.watcher_event instead
        #     logger.info("send minit a ping")

    async def send_death(self, death_text: str = ""):
        self.death_amnisty_count += 1
        if self.death_amnisty_count == self.death_amnisty_total:
            await super().send_death(death_text)
            self.last_sent_death = time.time()
            self.death_amnisty_count = 0

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(ProxyGameContext, self).server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def locationHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle POST at /Locations that uses scouts to return useful info"""
        requestjson = await request.json()

        try:
            await self.check_locations(requestjson["Locations"])
        except:  # TODO figure out what the exception actually is
            # back compat, can just let check_locations run when 0.6.0 is old enough
            await self.send_msgs(check_locations(self, requestjson["Locations"]))

        localResponse = self.build_local_locations_response(requestjson)
        return aiohttp.web.json_response(localResponse)

    async def goalHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle POST at /Goal"""
        requestjson = await request.text()
        response = self.build_goal_response(requestjson)
        if response:
            await self.send_msgs(response)
        return aiohttp.web.json_response(response)

    async def deathHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle POST at /Death"""
        if self.slot_data["death_link"]:
            response = self.build_deathlink_response()
            await self.send_death(f"{self.player_names[self.slot]} ran out of time")  # consider more silly messages
            return aiohttp.web.json_response(response)
        else:
            return aiohttp.web.json_response("deathlink disabled")

    async def deathpollHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle GET at /Deathpoll"""
        if self.slot_data["death_link"]:
            cTime = 0
            while (cTime < 20):
                if self.last_death_link > self.last_sent_death:
                    self.last_sent_death = self.last_death_link
                    return aiohttp.web.json_response({"Deathlink": True})
                else:
                    cTime += 1
                    await asyncio.sleep(1)
            return aiohttp.web.json_response({"Deathlink": False})
        else:
            return aiohttp.web.json_response("deathlink disabled")

    async def itemsHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle GET at /Items"""
        response = self.build_item_response()
        return aiohttp.web.json_response(response)

    async def datapackageHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle GET at /Datapackage"""
        response = self.build_datapackage_response()
        # response = {'datapackage':'FROM MINIT - need to figure out data'}
        # await self.send_msgs(response)
        return aiohttp.web.json_response(response)

    async def erConnHandler(self, request: aiohttp.web.Request) -> aiohttp.web.Response:
        """handle GET at /ErConnections"""
        response = self.build_er_response()
        return aiohttp.web.json_response(response)

    def build_er_response(self):
        """
        erMessage format:
        {"Entrances": [
            "hom10_10": [
                {
                    "direction": "south",
                    "baseCoor": 0,
                    "offset": 224,
                    "out": {
                        "room": "hom10_10",
                        "x": 0,
                        "y": 0,
                    }
                },
                {
                    "direction": "north",
                    "baseCoor": 0,
                    "offset": 224,
                    "out": {
                        "room": "hom10_10",
                        "x": 0,
                        "y": 0,
                    }
                }
            ],
            "rom10_10": [
                {
                    "direction": "south",
                    "baseCoor": 0,
                    "offset": 224,
                    "out": {
                        "room": "hom10_10",
                        "x": 0,
                        "y": 0,
                    }
                },
                {
                    "direction": "door",
                    "x": 0,
                    "y": 224,
                    "out": {
                        "room": "hom10_10",
                        "x": 0,
                        "y": 0,
                    }
                }
            ]
        ]}
        """
        connections = self.slot_data["ER_connections"]
        if not connections:
            return "ER Disabled"
        er_data_lookup = {data.entrance_name: data for data in er_entrances}
        erMessage = {"Entrances": game_entrances}
        for connection in connections:
            left, right = connection
            left_entrance = er_data_lookup[left]
            right_entrance = er_data_lookup[right]
            left_tile = left_entrance.room_tile
            left_name = left_entrance.entrance_name

            for index, entrance in enumerate(erMessage["Entrances"][left_tile]):
                if left_name == entrance["CName"]:
                    erMessage["Entrances"][left_tile][index]["out"] = {
                        "tile": right_entrance.room_tile,
                        "x": right_entrance.x_cord,
                        "y": right_entrance.y_cord,
                        "offDir": right_entrance.offset_direction,
                        "offNum": right_entrance.offset_value,
                        }

        return erMessage

    def build_deathlink_response(self):
        return "death sent"

    def build_goal_response(self, request: str):
        if request in self.goals:
            goalmessage = [{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
                }]
        else:
            goalmessage = None
        return goalmessage

    def build_local_locations_response(self, request: json) -> json:
        """
        expecting request to be json body in the form of
        {"LocationResponse":
            {"Player": "qwint", "Item": "ItemGrinder", "Code": 60017}
        - for a local item
        {"LocationResponse": {"Player": "OtherPlayer", "Item": "ItemGrinder"}
        - for a remote item
        """

        locations = set(request["Locations"]).difference(self.locations_checked)
        if len(locations) != 1:
            return {"Location": "Not found in scout cache"}  # TODO update if client can handle

        location = request["Locations"][0]
        if not self.locations_info:
            return {"Location": "Not found in scout cache"}  # TODO update if client can handle

        if location not in self.locations_info:
            return {"Location": "Not found in scout cache"}  # TODO update if client can handle

        loc = self.locations_info[location]
        slot = loc.player
        player = self.slot_info[loc.player].name
        item = self.item_names.lookup_in_slot(loc.item, slot)
        code = loc.item

        if self.slot_concerns_self(slot):
            locationmessage = {
                "Player": player,
                "Item": item,
                "Code": code}
        else:
            locationmessage = {"Player": player, "Item": item}
        return locationmessage

    def build_item_response(self):
        """
        expecting request to be json body in the form of
        {"Items": [123,456],"Coins":2, "Hearts": 1, "Tentacles":4}
        """
        itemIds = []
        coins = 0
        hearts = 0
        tentacles = 0
        swordsF = 0
        swordsR = 0
        for item in self.items_received:
            # TODO - change to lookup ids for actual item names
            if item[0] == 60000:
                coins += 1
            elif item[0] == 60001:
                hearts += 1
            elif item[0] == 60002:
                tentacles += 1
            elif item[0] == 60021:
                swordsF += 1
            elif item[0] == 60022:
                swordsR += 1
            else:
                itemIds.append(item[0])
        itemmessage = {
            "Items": itemIds,
            "Coins": coins,
            "Hearts": hearts,
            "Tentacles": tentacles,
            "swordsF": swordsF,
            "swordsR": swordsR,
        }
        return itemmessage

    # TODO update to transform the data
    # - will eventually handle the datapackage from
    # - CommonContext.consume_network_data_package() to make them minit pretty
    def build_datapackage_response(self):
        datapackagemessage = [{"cmd": "blah", "data": "blah"}]
        return datapackagemessage


async def main(args):
    from .proxyServer import Webserver, http_server_loop

    ctx = ProxyGameContext(args.connect, args.password)
    webserver = Webserver(ctx)
    ctx.httpServer_task = asyncio.create_task(http_server_loop(webserver), name="http server loop")

    ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    await ctx.exit_event.wait()
    await ctx.shutdown()


def launch(*args):
    import colorama

    parser = get_base_parser(description="Minit Archipelago Client.")
    parser.add_argument("url", nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(args)

    args = handle_url_arg(args, parser=parser)

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()


if __name__ == '__main__':
    import sys
    launch(*sys.argv[-1:])
