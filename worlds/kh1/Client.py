from __future__ import annotations
import os
import json
import sys
import asyncio
import shutil
import logging
import re
import time
from calendar import timegm

import ModuleUpdate
ModuleUpdate.update()

import Utils

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
    def __init__(self, ctx):
        super().__init__(ctx)
    
    def _cmd_slot_data(self):
        """Prints slot data settings for the connected seed"""
        for key in self.ctx.slot_data.keys():
            if key not in ["remote_location_ids", "synthesis_item_name_byte_arrays"]:
                self.output(str(key) + ": " + str(self.ctx.slot_data[key]))
    
    def _cmd_deathlink(self):
        """If your Death Link setting is set to "Toggle", use this command to turn Death Link on and off."""
        if "death_link" in self.ctx.slot_data.keys():
            if self.ctx.slot_data["death_link"] == "toggle":
                if self.ctx.death_link:
                    self.ctx.death_link = False
                    self.output(f"Death Link turned off")
                else:
                    self.ctx.death_link = True
                    self.output(f"Death Link turned on")
            else:
                self.output(f"'death_link' is not set to 'toggle' for this seed.")
                self.output(f"'death_link' = " + str(self.ctx.slot_data["death_link"]))
        else:
            self.output(f"No 'death_link' in slot_data keys. You probably aren't connected or are playing an older seed.")
    
    def _cmd_communication_path(self):
        """Opens a file browser to allow Linux users to manually set their %LOCALAPPDATA% path"""
        directory = Utils.open_directory("Select %LOCALAPPDATA% dir", "~/.local/share/Steam/steamapps/compatdata/2552430/pfx/drive_c/users/steamuser/AppData/Local")
        if directory:
            directory += "/KH1FM"
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.ctx.game_communication_path = directory
        else:
            self.output(self.ctx.game_communication_path)

class KH1Context(CommonContext):
    command_processor: int = KH1ClientCommandProcessor
    game = "Kingdom Hearts"
    items_handling = 0b011  # full remote except start inventory

    def __init__(self, server_address, password):
        super(KH1Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.hinted_location_ids: list[int] = []
        self.slot_data: dict = {}

        # Moved globals into instance attributes
        self.death_link: bool = False
        self.item_num: int = 1
        self.remote_location_ids: list[int] = []

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
        for root, dirs, files in os.walk(self.game_communication_path):
            for file in files:
                if file.find("obtain") <= -1:
                    os.remove(root+"/"+file)
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
        self.item_num = 1

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
        self.item_num = 1

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w', encoding='utf-8') as f:
                    f.close()
            
            # Handle Slot Data
            self.slot_data = args['slot_data']
            for key in list(args['slot_data'].keys()):
                with open(os.path.join(self.game_communication_path, key + ".cfg"), 'w', encoding='utf-8') as f:
                    f.write(str(args['slot_data'][key]))
                    f.close()
                if key == "remote_location_ids":
                    self.remote_location_ids = args['slot_data'][key]
                if key == "death_link":
                    if args['slot_data']["death_link"] != "off":
                        self.death_link = True
            # End Handle Slot Data

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    found = False
                    item_filename = f"AP_{str(self.item_num)}.item"
                    for filename in os.listdir(self.game_communication_path):
                        if filename == item_filename:
                            found = True
                    if not found:
                        if (NetworkItem(*item).player == self.slot and (NetworkItem(*item).location in self.remote_location_ids) or (NetworkItem(*item).location < 0)) or NetworkItem(*item).player != self.slot:
                            with open(os.path.join(self.game_communication_path, item_filename), 'w', encoding='utf-8') as f:
                                f.write(str(NetworkItem(*item).item) + "\n" + str(NetworkItem(*item).location) + "\n" + str(NetworkItem(*item).player))
                                f.close()
                                self.item_num += 1

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w', encoding='utf-8') as f:
                        f.close()

        if cmd in {"PrintJSON"} and "type" in args:
            if args["type"] == "ItemSend":
                item = args["item"]
                networkItem = NetworkItem(*item)
                receiverID = args["receiving"]
                senderID = networkItem.player
                locationID = networkItem.location
                if receiverID == self.slot or senderID == self.slot:
                    itemName = self.item_names.lookup_in_slot(networkItem.item, receiverID)[:20]
                    itemCategory = networkItem.flags
                    receiverName = self.player_names[receiverID][:20]
                    senderName = self.player_names[senderID][:20]
                    message = ""
                    if receiverID == self.slot and receiverID != senderID: # Item received from someone else
                        message = "From " + senderName + "\n" + itemName
                    elif senderID == self.slot and receiverID != senderID: # Item sent to someone else
                        message = itemName + "\nTo " + receiverName
                    elif locationID in self.remote_location_ids: # Found a remote item
                        message = itemName
                    filename = "msg"
                    if message != "":
                        if not os.path.exists(self.game_communication_path + "/" + filename):
                            with open(os.path.join(self.game_communication_path, filename), 'w', encoding='utf-8') as f:
                                f.write(message)
                                f.close()
            if args["type"] == "ItemCheat":
                item = args["item"]
                networkItem = NetworkItem(*item)
                receiverID = args["receiving"]
                if receiverID == self.slot:
                    itemName = self.item_names.lookup_in_slot(networkItem.item, receiverID)[:20]
                    filename = "msg"
                    message = "Received " + itemName + "\nfrom server"
                    if not os.path.exists(self.game_communication_path + "/" + filename):
                        with open(os.path.join(self.game_communication_path, filename), 'w', encoding='utf-8') as f:
                            f.write(message)
                            f.close()

    def on_deathlink(self, data: dict[str, object]):
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")
        with open(os.path.join(self.game_communication_path, 'dlreceive'), 'w', encoding='utf-8') as f:
            f.write(str(int(data["time"])))
            f.close()

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
    from .Locations import lookup_id_to_name
    while not ctx.exit_event.is_set():
        if ctx.death_link and "DeathLink" not in ctx.tags:
            await ctx.update_death_link(ctx.death_link)
        if not ctx.death_link and "DeathLink" in ctx.tags:
            await ctx.update_death_link(ctx.death_link)
        if ctx.syncing is True:
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
                if file.find("dlsend") > -1 and "DeathLink" in ctx.tags:
                    st = file.split("dlsend", -1)[1]
                    if st != "nil":
                        if timegm(time.strptime(st, '%Y%m%d%H%M%S')) > ctx.last_death_link and int(time.time()) % int(timegm(time.strptime(st, '%Y%m%d%H%M%S'))) < 10:
                            await ctx.send_death(death_text = "Sora was defeated!")
                if file.find("hint") > -1:
                    hint_location_id = int(file.split("hint", -1)[1])
                    if hint_location_id not in ctx.hinted_location_ids:
                        await ctx.send_msgs([{
                            "cmd": "LocationScouts",
                            "locations": [hint_location_id],
                            "create_as_hint": 2
                        }])
                        ctx.hinted_location_ids.append(hint_location_id)
        ctx.locations_checked = sending
        await ctx.check_locations(sending)
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
    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
