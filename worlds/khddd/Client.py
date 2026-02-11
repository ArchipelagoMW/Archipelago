from __future__ import annotations
import sys
import asyncio

from datetime import datetime, timedelta
from typing import Dict

import ModuleUpdate
ModuleUpdate.update()

import Utils
item_num = 1

from .Socket import KHDDDSocket, SlotDataType, DDDCommand

if __name__ == "__main__":
    Utils.init_logging("KHDDDClient", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

def check_stdin() -> None:
    if Utils.is_windows and sys.stdin:
        print("WARNING: Console input is not routed reliably on Windows, use the GUI instead.")

class KHDDDClientCommandProcessor(ClientCommandProcessor):

    def __init__(self, ctx):
        super().__init__(ctx)

    def _cmd_drop(self):
        """Instantly drops the player."""
        self.ctx.socket.send_client_cmd(DDDCommand.DROP, "")
        self.output("Dropping player.")

    def _cmd_unstuck(self):
        """Sends the inactive character to the World Map."""
        self.ctx.socket.send_client_cmd(DDDCommand.UNSTUCK, "")
        self.output("Sending inactive character to the World Map.")

    def _cmd_deathlink(self):
        """Toggles Deathlink"""
        self.ctx.death_link = not self.ctx.death_link
        asyncio.create_task(self.ctx.update_death_link(self.ctx.death_link)).add_done_callback(
            lambda _: self.output(f"Death Link turned {'on' if self.ctx.death_link else 'off'}"))
        self.ctx.socket.send_client_cmd(DDDCommand.DEATH_LINK, str(self.ctx.death_link))



class KHDDDContext(CommonContext):
    command_processor: int = KHDDDClientCommandProcessor
    game = "Kingdom Hearts Dream Drop Distance"
    items_handling = 0b111 #Attempt full remote
    death_link: bool = False

    sent_notifications = 0

    #Vars for socket
    socket: KHDDDSocket = None
    check_location_IDs = []
    slot_data_info: Dict[str, str] = {}
    _connectedToAp: bool = False
    _connectedToDDD: bool = False

    _get_items_running = False

    def __init__(self, server_address, password):
        super(KHDDDContext, self).__init__(server_address, password)

        #Socket
        self.socket = KHDDDSocket(self)
        asyncio.create_task(self.socket.start_server(), name="KHDDDSocketServer")

    async def server_auth(self, password_requested:bool = False):
        if password_requested and not self.password:
            await super(KHDDDContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        await super(KHDDDContext, self).connection_closed()
        self._connectedToAp = False
        self.slot_data_info = {}

    @property
    def connectedToAp(self) -> bool:
        return self._connectedToAp
    @connectedToAp.setter
    def connectedToAp(self, value: bool):
        self._connectedToAp = value

    @property
    def connectedToDDD(self) -> bool:
        return self._connectedToDDD
    @connectedToDDD.setter
    def connectedToDDD(self, value: bool):
        self._connectedToDDD = value

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(KHDDDContext, self).shutdown()
        self.socket.send(20, ["Closing"])
        self.socket.shutdown_server()
    
    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
            self.connectedToAp = True
            self.slot_data_info = args['slot_data']
            asyncio.create_task(self.send_slot_data(), name="KHDDDSendSlotData")
        
        if cmd in {"ReceivedItems"}:
            if len(args["items"]) > 0:
                self.socket.send_multipleItems(args["items"], len(self.items_received))
            else:
                self.socket.send_singleItem(args["items"][0].item, len(self.items_received))

        #Send item notifications to game
        if cmd in {"PrintJSON"} and "type" in args:
            if args["type"] == "ItemSend":
                item = args["item"]
                networkItem = NetworkItem(*item)
                receiverID = args["receiving"]
                senderID = networkItem.player
                if receiverID == self.slot or senderID == self.slot:
                    itemName = self.item_names.lookup_in_slot(networkItem.item, receiverID)[:20]
                    itemCategory = networkItem.flags
                    receiverName = self.player_names[receiverID][:20]
                    #message = ""
                    if senderID == self.slot and receiverID != senderID: # Item sent to someone else
                        #message = itemName + "\nTo " + receiverName
                        #logger.info(message)
                        self.socket.item_msg(str(itemName), str(receiverName), str(itemCategory))


    def on_deathlink(self, data: dict[str, object]):
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"Deathlink: {text}")
        else:
            logger.info(f"Deathlink: Received from {data['source']}")
        #Send to the game
        self.socket.send(8, [str(int(data["time"]))])

    def run_gui(self):
        """Import kivy UI system and start running it as self.ui_task"""
        from kvui import GameManager

        class KHDDDManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago KHDDD Client"

        self.ui = KHDDDManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def get_items(self):
        """Send all received items to the game client. This can't be async 
        because of message handler, so putting it into an internal async function 
        and running it with the Utils fire and forget function."""
        @staticmethod
        async def async_get_items(ctx: KHDDDContext):
            try:
                while not ctx.exit_event.is_set() and not ctx.connectedToAp:
                    await asyncio.sleep(5)
                if ctx.connectedToAp: #should catch drop traps somehow in multi-sends to prevent drop on connect
                    ctx.socket.send_multipleItems(ctx.items_received, len(ctx.items_received))
            finally:
                ctx._get_items_running = False

        if not self._get_items_running:
            self._get_items_running = True
            Utils.async_start(async_get_items(self), name="KHDDDGetItems")

    def get_slot_data(self):
        Utils.async_start(self.send_slot_data(), name="KHDDDGetSlotData")

    async def send_slot_data(self):
        while not self.exit_event.is_set():
            if not self.connectedToDDD or self._get_items_running:
                await asyncio.sleep(5)
                continue
            elif self.slot_data_info:
                for key, value in self.slot_data_info.items():
                    if key in SlotDataType.__members__.keys():
                        self.socket.send_slot_data(SlotDataType[key], str(value))
                break


async def game_watcher(ctx: KHDDDContext):
    while not ctx.exit_event.is_set():
        try:
            if not ctx.connectedToDDD:
                await asyncio.sleep(5)     
                continue

            if ctx.socket.deathTime != "" and ctx.death_link:
                # New death detected, parse deathTime as local datetime
                death_time = datetime.strptime(ctx.socket.deathTime, '%Y%m%d%H%M%S')
                ctx.socket.deathTime = ""
                time_window = timedelta(seconds=20)
                if death_time + time_window >= datetime.now():
                    logger.info(f"Sending deathlink...")
                    await ctx.send_death(death_text=f"{ctx.username} fell to a nightmare")

            if ctx.socket.goaled and not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

            ctx.locations_checked = ctx.check_location_IDs
            message = [{"cmd": 'LocationChecks', "locations": ctx.check_location_IDs}]
            await ctx.send_msgs(message)
            await asyncio.sleep(0.5)


        except Exception as e:
            logger.error(f"Error in game watcher: {e}")
            ctx.connectedToDDD = False
            continue

def launch():

    async def main(args):
        ctx = KHDDDContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        progression_watcher = asyncio.create_task(
            game_watcher(ctx), name="KHDDDProgressionWatcher")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await progression_watcher

        await ctx.shutdown()

    import colorama
        
    parser = get_base_parser(description="KHDDD Client, for text interfacing.")

    args, rest = parser.parse_known_args()
    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()