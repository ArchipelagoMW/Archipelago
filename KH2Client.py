from __future__ import annotations
import os
import sys
import asyncio
import shutil
from pymem.process import *
from pymem import memory
import ModuleUpdate
ModuleUpdate.update()

import Utils

if __name__ == "__main__":
    Utils.init_logging("KH2Client", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop


class KH2CommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
def _cmd_autotrack(self):
        """Start Autotracking"""
        # first get pid, see the 32-bit solution

        PROCNAME = "KINGDOM HEARTS II FINAL MIX"


        try:
           kh2=pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
        except:
            self.output("Game is not Open")
        #Save = 0x09A70B0
        ##pid = None
        ##
        ##
        ##for proc in psutil.process_iter():
        ##    if PROCNAME in proc.name():
        ##       pid = proc.pid
        ##       base=int(proc.memory_maps(False)[0].addr,0)
        ##
        #kh2=pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
        #
        #yourmom=kh2.base_address + Save+0x23DF
        ##if kh2.read_bytes(yourmom,1)&0x04:
        ##	print("your mom")
        ##else:
        ##	print("")
        #
        #chestvalue=int.from_bytes(kh2.read_bytes(yourmom,1), "big")
        ##check if chest is already opened 
        ##chestvalue is total amount of chests opened. 
        #print(kh2.write_bytes(yourmom,(chestvalue|0x1<<2).to_bytes(1,'big'),1))
        #
        #
        #
        ##opens the chest at value 2 and keeps all the other chests the same
        #kh2.write_bytes(yourmom,(chestvalue|0x1<<2).to_bytes(1,'big'),1)

    #def _cmd_gb(self):
    #    """Check Gameboy Connection State"""
    #    if isinstance(self.ctx, KH2Context):
    #        logger.info("debussy")

class KH2Context(CommonContext):
    command_processor: int = KH2CommandProcessor
    game = "Kingdom Hearts 2"
    items_handling = 0b001  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(KH2Context, self).__init__(server_address, password)
        self.send_index: int = 0
        self.syncing = False
        self.awaiting_bridge = False


    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(KH2Context, self).connection_closed()
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
        await super(KH2Context, self).shutdown()
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
                    filename = f"AP_{str(NetworkItem(*item).location)}PLR{str(NetworkItem(*item).player)}.item"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.write(str(NetworkItem(*item).item))
                        f.close()

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                for ss in self.checked_locations:
                    filename = f"send{ss}"
                    with open(os.path.join(self.game_communication_path, filename), 'w') as f:
                        f.close()

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task."""
        from kvui import GameManager

        class KH2Manager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago KH2 Client"

        self.ui = KH2Manager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")


#for loop to dictate what world you are in
#once figured out the world run through the locations
#for location in agchecks:
#if location in checked_locations continue
#else check if location is opened
#if location is checked append to checked_locations
#if location in the dummy 14 list then send location.item

#dummy locations should be in slot data after generation hopefully

async def kh2_watcher(ctx: KH2Context):
    #from worlds.KH2.Locations import lookup_id_to_name
    while not ctx.exit_event.is_set():
        if ctx.syncing == True:
            sync_msg = [{'cmd': 'Sync'}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
        sending = []
        victory = False
        #for root, dirs, files in os.walk(ctx.game_communication_path):
        #    for file in files:
        #        if file.find("send") > -1:
        #            st = file.split("send", -1)[1]
        #            sending = sending+[(int(st))]
        #        if file.find("victory") > -1:
        #            victory = True
        ctx.locations_checked = sending
        message = [{"cmd": 'LocationChecks', "locations": sending}]
        await ctx.send_msgs(message)
        if not ctx.finished_game and victory:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            ctx.finished_game = True
        await asyncio.sleep(0.1)


if __name__ == '__main__':
    async def main(args):
        ctx = KH2Context(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            kh2_watcher(ctx), name="KH2ProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama

    parser = get_base_parser(description="KH2 Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.init()
    asyncio.run(main(args))
    colorama.deinit()
