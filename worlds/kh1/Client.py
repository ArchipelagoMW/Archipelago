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
death_link = False
item_num = 1

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
    
    def _cmd_deathlink(self):
        """Toggles Deathlink"""
        global death_link
        if death_link:
            death_link = False
            self.output(f"Death Link turned off")
        else:
            death_link = True
            self.output(f"Death Link turned on")
    
    def _cmd_goal(self):
        """Prints goal setting"""
        if "goal" in self.ctx.slot_data.keys():
            self.output(str(self.ctx.slot_data["goal"]))
        else:
            self.output("Unknown")
    
    def _cmd_eotw_unlock(self):
        """Prints End of the World Unlock setting"""
        if "required_reports_door" in self.ctx.slot_data.keys():
            if self.ctx.slot_data["required_reports_door"] > 13:
                self.output("Item")
            else:
                self.output(str(self.ctx.slot_data["required_reports_eotw"]) + " reports")
        else:
            self.output("Unknown")
    
    def _cmd_door_unlock(self):
        """Prints Final Rest Door Unlock setting"""
        if "door" in self.ctx.slot_data.keys():
            if self.ctx.slot_data["door"] == "reports":
                self.output(str(self.ctx.slot_data["required_reports_door"]) + " reports")
            else:
                self.output(str(self.ctx.slot_data["door"]))
        else:
            self.output("Unknown")
    
    def _cmd_advanced_logic(self):
        """Prints advanced logic setting"""
        if "advanced_logic" in self.ctx.slot_data.keys():
            self.output(str(self.ctx.slot_data["advanced_logic"]))
        else:
            self.output("Unknown")

class KH1Context(CommonContext):
    command_processor: int = KH1ClientCommandProcessor
    game = "Kingdom Hearts"
    items_handling = 0b111  # full remote

    def __init__(self, server_address, password):
        super(KH1Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False
        self.hinted_synth_location_ids = False
        self.slot_data = {}
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
        global item_num
        item_num = 1

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
        global item_num
        item_num = 1

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            for ss in self.checked_locations:
                filename = f"send{ss}"
                with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                    f.close()
            
            #Handle Slot Data
            self.slot_data = args['slot_data']
            for key in list(args['slot_data'].keys()):
                with open(os.path.join(self.game_communication_path, key + ".cfg"), 'w') as f:
                    f.write(str(args['slot_data'][key]))
                    f.close()
                    
            ###Support Legacy Games
            if "Required Reports" in list(args['slot_data'].keys()) and "required_reports_eotw" not in list(args['slot_data'].keys()):
                reports_required = args['slot_data']["Required Reports"]
                with open(os.path.join(self.game_communication_path, "required_reports.cfg"), 'w') as f:
                    f.write(str(reports_required))
                    f.close()
            ###End Support Legacy Games
            
            #End Handle Slot Data

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                global item_num
                for item in args['items']:
                    found = False
                    item_filename = f"AP_{str(item_num)}.item"
                    for filename in os.listdir(self.game_communication_path):
                        if filename == item_filename:
                            found = True
                    if not found:
                        with open(os.path.join(self.game_communication_path, item_filename), 'w') as f:
                            f.write(str(NetworkItem(*item).item) + "\n" + str(NetworkItem(*item).location) + "\n" + str(NetworkItem(*item).player))
                            f.close()
                            item_num = item_num + 1

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

        if cmd in {"PrintJSON"} and "type" in args:
            if args["type"] == "ItemSend":
                item = args["item"]
                networkItem = NetworkItem(*item)
                recieverID = args["receiving"]
                senderID = networkItem.player
                locationID = networkItem.location
                if recieverID != self.slot and senderID == self.slot:
                    itemName = self.item_names.lookup_in_slot(networkItem.item, recieverID)
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

    def on_deathlink(self, data: dict[str, object]):
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")
        else:
            logger.info(f"DeathLink: Received from {data['source']}")
        with open(os.path.join(self.game_communication_path, 'dlreceive'), 'w') as f:
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
        global death_link
        if death_link and "DeathLink" not in ctx.tags:
            await ctx.update_death_link(death_link)
        if not death_link and "DeathLink" in ctx.tags:
            await ctx.update_death_link(death_link)
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
                if file.find("dlsend") > -1 and "DeathLink" in ctx.tags:
                    st = file.split("dlsend", -1)[1]
                    if st != "nil":
                        if timegm(time.strptime(st, '%Y%m%d%H%M%S')) > ctx.last_death_link and int(time.time()) % int(timegm(time.strptime(st, '%Y%m%d%H%M%S'))) < 10:
                            await ctx.send_death(death_text = "Sora was defeated!")
                if file.find("insynthshop") > -1:
                    if not ctx.hinted_synth_location_ids:
                        await ctx.send_msgs([{
                            "cmd": "LocationScouts",
                            "locations": [2656401,2656402,2656403,2656404,2656405,2656406],
                            "create_as_hint": 2
                        }])
                        ctx.hinted_synth_location_ids = True
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
    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()
