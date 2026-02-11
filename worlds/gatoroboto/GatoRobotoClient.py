from __future__ import annotations
import os
import asyncio
import typing
import bsdiff4
import shutil
import json
import psutil
import uuid

import Utils

from NetUtils import NetworkItem, ClientStatus
from worlds import gatoroboto
from MultiServer import mark_raw
from CommonClient import CommonContext, server_loop, \
    gui_enabled, ClientCommandProcessor, logger, get_base_parser
from Utils import async_start, is_linux

"""
Notes on things ive learned:
locations_checked = list maintained by client of locations youve checked
checked_locations = list from server of locations youve checked
"""

class GatoRobotoPath:
    @classmethod
    def steam_install(cls) -> list[str]:
        if is_linux:
            return [os.path.expanduser("~/.local/share/Steam/steamapps/common/Gato Roboto")] # running w/ proton

        # default, Utils.is_windows
        return ["C:\\Program Files (x86)\\Steam\\steamapps\\common\\Gato Roboto", "C:\\Program Files\\Steam\\steamapps\\common\\Gato Roboto"]

    @classmethod
    def save_game_folder(cls) -> str:
        if is_linux:
            return os.path.expanduser("~/.local/share/Steam/steamapps/compatdata/916730/pfx/drive_c/users/steamuser/AppData/Local/GatoRoboto") # running w/ proton

        # default, Utils.is_windows
        return os.path.expandvars(r"%localappdata%/GatoRoboto")

class GatoRobotoCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx) 

    @staticmethod
    def print_log(msg):
        logger.info(msg)
        
    @mark_raw
    def _cmd_auto_patch(self, steam_install: str  = ""):
        """Patch the game automatically."""
        if isinstance(self.ctx, GatoRobotoContext):
            
            #Validate file or set to default path
            if steam_install == "" or not os.path.exists(steam_install):
                for possible_install_location in list(f"{GatoRobotoPath.steam_install()}"):
                    if os.path.exists(possible_install_location):
                        steam_install = possible_install_location
                        break
            
            #If no valid file error out
            if (not os.path.exists(steam_install)
                or not os.path.isfile(os.path.join(steam_install, "data.win"))):
                self.output("ERROR: Cannot find Gato Roboto. Please rerun the command with the correct folder."
                            " command. \"/auto_patch (Steam directory)\".")
            #Patch game if valid file
            else:                
                self.ctx.patch_game(steam_install)
                self.output("Patching successful!")
                
    def _cmd_resync(self):
        """Manually trigger a resync."""
        if isinstance(self.ctx, GatoRobotoContext):
            self.output(f"Syncing items.")
            self.ctx.syncing = True

class GatoRobotoContext(CommonContext):
    tags: dict = {"AP", "Online"}
    game: str = "Gato Roboto"
    command_processor: GatoRobotoCommandProcessor = GatoRobotoCommandProcessor
    checks_to_consume: list[NetworkItem] = []
    cur_client_items: list[int] = []
    read_client_items: bool = False
    game_id: str = ""
    cur_start_index: int = 0
    items_handling = 0b111
    
    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.game = "Gato Roboto"
        self.syncing = False
        
    @staticmethod
    def patch_game(filepath):
        #Save vanilla game data for backup purposes
        os.makedirs(name=f"{filepath}/VanillaData", exist_ok=True)
        shutil.copy(f"{filepath}/data.win", f"{filepath}/VanillaData")
        
        #Write patched game data
        with open(f"{filepath}/data.win", "rb") as f:
            patched_file: bytes = bsdiff4.patch(f.read(), gatoroboto.data_path("patch.bsdiff"))
        with open(f"{filepath}/data.win", "wb") as f:
            f.write(patched_file)

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd, args):
        #print("Got Package: " + cmd) #remove for final
        
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game
        
        async_start(process_gatoroboto_cmd(self, cmd, args))
        
    async def connect(self, address: typing.Optional[str] = None):
        await super().connect(address)

    async def disconnect(self, allow_autoreconnect: bool = False):
        await super().disconnect(allow_autoreconnect)

    async def connection_closed(self):
        await super().connection_closed()

    async def shutdown(self):
        await super().shutdown()
        
    def run_gui(self):
        from kvui import GameManager

        class UTManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Archipelago Gato Roboto Client"

        self.ui = UTManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")
        
async def game_watcher(ctx: GatoRobotoContext):    
    printed_connecting: bool = False
     
    while not ctx.exit_event.is_set():
        await asyncio.sleep(0.1)
        
        if not printed_connecting:
            ctx.command_processor.print_log("Waiting for Connection to Game")
            printed_connecting = True
        
        #read initial data for syncing items with the client
        if not ctx.read_client_items and os.path.exists(f"{GatoRobotoPath.save_game_folder()}/init.json"):
            #print("Received Init")
            ctx.command_processor.print_log("Connected to Game")
            
            try:
                with open(f"{GatoRobotoPath.save_game_folder()}/init.json", 'r+') as f:
                    items_init: dict = get_clean_game_comms_file(f)
                    ctx.cur_client_items = []
                    
                    for key in items_init:
                        if key != "game_id":
                            ctx.cur_client_items.append(int(key))
                        
                ctx.read_client_items = True
                        
                os.remove(f"{GatoRobotoPath.save_game_folder()}/init.json")
            except PermissionError:
                print("⚠ File is locked by another program. Skipping read.")
                await asyncio.sleep(0.3)
            
        #check if game disconnects
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/off.json"):
            try:
                #print("Received off")
                ctx.command_processor.print_log("Lost Connection to Game")
                ctx.command_processor.print_log("Waiting for Connection to Game")
                os.remove(f"{GatoRobotoPath.save_game_folder()}/off.json")
                ctx.cur_client_items = []
                ctx.read_client_items = False
                
                #send game id for syncing
                json_out: dict = {
                    "game_id": ctx.game_id
                }
                
                item_in_json: str = json.dumps(json_out, indent=4)
                
                with open(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", 'w') as f:
                    f.write(item_in_json)
            
                if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/gameid.json"):
                    os.remove(f"{GatoRobotoPath.save_game_folder()}/gameid.json")
            
                os.rename(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", f"{GatoRobotoPath.save_game_folder()}/gameid.json")
            except PermissionError:
                print("⚠ File is locked by another program, skipping read.")
                await asyncio.sleep(0.3)
            
        #handle client restarts and game crashes via exe check
        flag = False
        for process in psutil.process_iter(attrs=["exe"]):
            try:
                exe_path: str = process.info["exe"]
                if exe_path and "gatoroboto" in exe_path.lower():  # ✅ Check if not None
                    flag = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        try:
            #if client has restarted, re-request init file
            if flag and not ctx.read_client_items and not os.path.exists(f"{GatoRobotoPath.save_game_folder()}/req_init.json"):
                open(f"{GatoRobotoPath.save_game_folder()}/req_init.json", "a").close()
            #handle game restart via hard close or crash
            elif not flag and ctx.read_client_items:
                ctx.command_processor.print_log("Lost Connection to Game")
                ctx.command_processor.print_log("Waiting for Connection to Game")
                ctx.cur_client_items = []
                ctx.read_client_items = False
                
                if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/gameid.json"):
                    os.remove(f"{GatoRobotoPath.save_game_folder()}/gameid.json")
                
                json_out: dict = {
                    "game_id": ctx.game_id
                }
                
                item_in_json: str = json.dumps(json_out, indent=4)
                
                with open(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", 'w') as f:
                    f.write(item_in_json)
            
                os.rename(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", f"{GatoRobotoPath.save_game_folder()}/gameid.json")
        except PermissionError:
            print("⚠ File is locked by another program, skipping read.")
            await asyncio.sleep(0.3)
        
        #watch for received locations from game
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/locations.json"):
            print("Received Locations")
            try:
                with open(f"{GatoRobotoPath.save_game_folder()}/locations.json", "r+") as f:
                    locations_in: dict = get_clean_game_comms_file(f)
                    
                    sending: list[int] = []
                    
                    for key in locations_in:
                        if str(key).isdigit():
                            if ctx.missing_locations.__contains__(int(key)) and int(locations_in[str(key)]) > 0:
                                print("Found Location to Send")
                                sending.append(int(key))
                    
                    if len(sending) != 0:
                        await ctx.send_msgs([{"cmd": "LocationChecks", "locations": sending}])
                
                os.remove(f"{GatoRobotoPath.save_game_folder()}/locations.json")
            except PermissionError:
                print("⚠ File is locked by another program, skipping read.")
                await asyncio.sleep(0.3)
            except TypeError:
                print("⚠ Error in reading file, skipping read.")
        
        #check if wincon present
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/victory.json") and not ctx.finished_game:
            try:
                #print("Received Victory")
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    
                os.remove(f"{GatoRobotoPath.save_game_folder()}/victory.json")
            except PermissionError:
                print("⚠ File is locked by another program, skipping read.")
                await asyncio.sleep(0.3)
            
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/cur_region.json"):
            try:
                #print("New Region")
                with open(f"{GatoRobotoPath.save_game_folder()}/cur_region.json", "r+") as f:
                    locations_in: dict = get_clean_game_comms_file(f)
                    
                    await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot],
                        "data": {
                            "type": "MapUpdate",
                            "mapId": int(locations_in["Region"]),
                        }
                    }])
                    
                os.remove(f"{GatoRobotoPath.save_game_folder()}/cur_region.json")
            except PermissionError:
                print("⚠ File is locked by another program, skipping read.")
                await asyncio.sleep(0.3)
        
        #consume items in fifo order, filter out received items
        try:
            if (len(ctx.checks_to_consume) > 0 
                and ctx.read_client_items 
                and not os.path.exists(f"{GatoRobotoPath.save_game_folder()}/items.json")):
                # print("Received Items JSON")
                flag: bool = True
                while len(ctx.checks_to_consume) > 0 and flag:
                    cur_item: NetworkItem = ctx.checks_to_consume.pop(0)
                    
                    if not ctx.cur_client_items.__contains__(int(cur_item.item)):
                        ctx.cur_client_items.append(int(cur_item.item))
                        
                        item_in = {
                            "item": int(cur_item.item),
                            "item_index": len(ctx.cur_client_items)
                        }
                        
                        item_in_json: str = json.dumps(item_in, indent=4)
                
                        with open(f"{GatoRobotoPath.save_game_folder()}/tmp_it.json", 'w') as f:
                            f.write(item_in_json)
                    
                        os.rename(f"{GatoRobotoPath.save_game_folder()}/tmp_it.json", f"{GatoRobotoPath.save_game_folder()}/items.json")

                        flag = False    
                        
                    rec_flag: bool = False
                    for item in ctx.items_received:
                        if item.item == cur_item.item:
                            rec_flag = True
                    
                    if not rec_flag:
                        ctx.items_received.append(cur_item)
        except PermissionError:
                print("⚠ File is locked by another program, skipping read.")
                await asyncio.sleep(0.3)
        
        #resync, and attempt to send client all items received
        if ctx.syncing:
            ctx.items_received = []
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
            ctx.syncing = False
            
async def process_gatoroboto_cmd(ctx: GatoRobotoContext, cmd: str, args: dict):
    if cmd == "Bounced":
        print(args)
    
    if cmd == "Connected":
        # Do all file init here
        if not os.path.exists(f"{GatoRobotoPath.save_game_folder()}"):
            os.mkdir(f"{GatoRobotoPath.save_game_folder()}")
            
        id: str
        if "game_id" in args["slot_data"]:
            id = args["slot_data"]["game_id"]
        else:
            id = str(uuid.uuid4())
            args["slot_data"]["game_id"] = id
            
        ctx.game_id = id
            
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/gameid.json"):
            os.remove(f"{GatoRobotoPath.save_game_folder()}/gameid.json")
            
        json_out: dict = {
            "game_id": id
        }
        
        item_in_json: str = json.dumps(json_out, indent=4)
        
        with open(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", 'w') as f:
            f.write(item_in_json)
    
        os.rename(f"{GatoRobotoPath.save_game_folder()}/tmp_id.json", f"{GatoRobotoPath.save_game_folder()}/gameid.json")

            
    if cmd == "ReceivedItems":
        #print("GOT SOME ITEMS")
        #print(str(args["items"]))
        ctx.watcher_event.set()
        
        start_index: int = args["index"]
        
        if start_index == 0:
            ctx.items_received = []
        elif start_index != len(ctx.items_received):
            sync_msg = [{"cmd": "Sync"}]
            if ctx.locations_checked:
                sync_msg.append({"cmd": "LocationChecks",
                                 "locations": list(ctx.locations_checked)})
            await ctx.send_msgs(sync_msg)
        
        if start_index == len(ctx.items_received):
            
            # Send items to items queue
            for item in args["items"]:
                net_item = NetworkItem(*item)
                ctx.checks_to_consume.append(net_item)
            
            ctx.cur_start_index = start_index

def get_clean_game_comms_file(f) -> dict | None:
    content = f.read()

    cleaned_content = content.replace("\x00", "").strip()

    if not cleaned_content.endswith("}"):
        cleaned_content += "}"

    try:
        cleaned_json: dict = json.loads(cleaned_content)
    except json.JSONDecodeError:
        print("Error: Invalid JSON file, unable to fix.")
        return None
    
    if content != cleaned_content:
        f.seek(0)
        f.truncate()
        f.write(cleaned_content)
        print("JSON file cleaned successfully.")
        
    return cleaned_json
         
def launch():        
    async def _main():
        ctx = GatoRobotoContext(None, None)
        
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/item.json"):
            os.remove(f"{GatoRobotoPath.save_game_folder()}/item.json")
            
        if os.path.exists(f"{GatoRobotoPath.save_game_folder()}/gameid.json"):
            os.remove(f"{GatoRobotoPath.save_game_folder()}/gameid.json")
            
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="server loop")
        asyncio.create_task(
            game_watcher(ctx), name="GatoRobotoProgressionWatcher")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    Utils.init_logging("GatoRobotoClient", exception_logger="Client")
    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()

    parser = get_base_parser(description="Gato Roboto Client, for text interfacing.")
    args = parser.parse_args()
        

