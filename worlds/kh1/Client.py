from __future__ import annotations
import os
import json
import sys
import asyncio
import shutil
import logging
import re

import ModuleUpdate
ModuleUpdate.update()

import Utils

check_num = 0

logger = logging.getLogger("Client")

if __name__ == "__main__":
    Utils.init_logging("KH1Client", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

class KH1ClientCommandProcessor(ClientCommandProcessor):
    pass
    #def _cmd_test(self):
    #    """Test"""
    #    self.output(f"Test")


class KH1Context(CommonContext):
    command_processor: int = KH1ClientCommandProcessor
    game = "Kingdom Hearts"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super(KH1Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        # self.game_communication_path: files go in this path to pass data between us and the actual game
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%/KH1FM")
        else:
            self.game_communication_path = os.path.expandvars(r"$HOME/KH1FM")
        if not os.path.exists(self.game_communication_path):
            os.makedirs(self.game_communication_path)
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH1Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(KH1Context, self).connection_closed()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root + "/" + file)

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(KH1Context, self).shutdown()
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    check_num = 0
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith("AP"):
                            if int(filename.split("_")[-1].split(".")[0]) > check_num:
                                check_num = int(filename.split("_")[-1].split(".")[0])
                    item_id = ""
                    location_id = ""
                    player = ""
                    found = False
                    for filename in os.listdir(self.game_communication_path):
                        if filename.startswith(f"AP"):
                            with open(os.path.join(self.game_communication_path, filename), 'r') as f:
                                item_id = str(f.readline()).replace("\n", "")
                                location_id = str(f.readline()).replace("\n", "")
                                player = str(f.readline()).replace("\n", "")
                                if str(item_id) == str(NetworkItem(*item).item) and str(location_id) == str(NetworkItem(*item).location) and str(player) == str(NetworkItem(*item).player):
                                    found = True
                    if not found:
                        filename = f"AP_{str(check_num+1)}.item"
                        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                            f.write(str(NetworkItem(*item).item) + "\n" + str(NetworkItem(*item).location) + "\n" + str(NetworkItem(*item).player))
                            f.close()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

        if cmd in {"PrintJSON"} and args["type"] == "ItemSend":
            item = args["item"]
            networkItem = NetworkItem(*item)
            recieverID = args["receiving"]
            senderID = networkItem.player
            locationID = networkItem.location
            if recieverID != self.slot and senderID == self.slot:
                itemName = self.item_names[networkItem.item]
                itemCategory = networkItem.flags
                recieverName = self.player_names[recieverID]
                filename = "sent"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.write(
                      re.sub('[^A-Za-z0-9 ]+', '',str(itemName))[:15] + "\n"
                    + re.sub('[^A-Za-z0-9 ]+', '',str(recieverName))[:6] + "\n"
                    + str(itemCategory) + "\n"
                    + str(locationID))
                    f.close()

#f.write(self.item_names[NetworkItem(*item).item] + "\n" + self.location_names[NetworkItem(*item).location] + "\n" + self.player_names[NetworkItem(*item).player])



        #last resort we can probably do better
        #input: Krujo sent Magic Upgrade to Tim ((TT3) LocationName)
        # if cmd in {"PrintJSON"}:
        #     data = args["data"]
        #     if data[0]:
        #         msg = str(data[0]["text"]);
        #         #player send a location
        #         # if msg.startswith(self.auth + " sent "): #debug
        #         with open(os.path.join(self.game_communication_path, "sent"), 'w') as f:
        #             msg = msg.replace(self.auth + " sent ", "")
        #             #Magic Upgrade to Tim ((TT3) LocationName)
        #             splitTo = msg.split(" to ")
        #             targetPlayer = splitTo[1].split(" ")[0]
        #             f.close()





    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class KH1Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago KH1 Client"

        self.ui = KH1Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


async def game_watcher(ctx: KH1Context):
    from worlds.kh1.Locations import lookup_id_to_name
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        for root, dirs, files in os.walk(ctx.game_communication_path):
            for file in files:
                if file.find("send") > -1:
                    st = file.split("send", -1)[1]
                    if st != "nil":
                        sending = sending+[(int(st))]
                if file.find("victory") > -1:
                    victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


def launch():
    async def main(args):
        ctx = KH1Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="KH1ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="KH1 Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
