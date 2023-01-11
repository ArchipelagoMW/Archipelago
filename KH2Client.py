from __future__ import annotations
import os
import sys
import asyncio
import shutil
from pymem.process import *
from pymem import memory
import ModuleUpdate
ModuleUpdate.update()
from worlds.kh2 import all_locations, item_dictionary_table
import Utils
import subprocess
import typing
import time

if __name__ == "__main__":
    Utils.init_logging("KH2Client", exception_logger="Client")

from NetUtils import NetworkItem, ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

from worlds import network_data_package

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator, then restart oot_connector.lua"
CONNECTION_REFUSED_STATUS = "Connection refused. Please start your emulator and make sure oot_connector.lua is running"
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator, then restart oot_connector.lua"
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

boobies=network_data_package["games"]["Kingdom Hearts 2"]["location_name_to_id"]


class KH2CommandProcessor(ClientCommandProcessor):
    def _cmd_resync(self):
        """Manually trigger a resync."""
        self.output(f"Syncing items.")
        self.ctx.syncing = True
        for locationdata in all_locations:
            print(all_locations[locationdata].addrCheck)

    def _cmd_autotrack(self):
            """Start Autotracking"""
            # first get pid, see the 32-bit solution
            try:          
                self.ctx.kh2=pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
            except:
                print("Game is not opened/autotrackable")
                return

            self.ctx.kh2connected=True
            
#def process_exists(process_name):
    
           #try:
           #   
           #except:
           #    self.output("Game is not Open")
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
        self.KH2_sync_task = None
        self.syncing = False
        self.kh2connected = False

        self.item_name_to_data = {name: data for name, data, in item_dictionary_table.items()}
        self.location_name_to_data = {name: data for name, data, in all_locations.items()}
        self.lookup_id_to_item: typing.Dict[int, str] = {data.code: item_name for item_name, data in item_dictionary_table.items() if
                                            data.code}
        self.lookup_id_to_Location: typing.Dict[int, str] = {data.code: item_name for item_name, data in all_locations.items() if
                                                data.code}
        #self.KH2_status = CONNECTION_INITIAL_STATUS
        #self.awaiting_rom = False
        self.location_table = {}
        self.collectible_table = {}
        self.collectible_override_flags_address = 0
        self.collectible_offsets = {}
        #self.deathlink_enabled = False
        #self.deathlink_pending = False
        #self.deathlink_sent_this_death = False
        #self.deathlink_client_override = False
        #self.version_warning = False
        self.kh2= None
        self.ItemIsSafe = False
        self.game_connected = False
        self.worldid={
	        1 : "GoA",
	        2 : "TwilightTown" ,
	        3 : "DestinyIsland",
	        4 : "HollowBastion",
	        5 : "BeastsCastle" ,
	        6 : "OlympusColiseum",
	        7 : "Agrabah" ,
	        8 : "LandofDragons",
	        9 : "HundredAcreWood",
	        10 : "PrideLands" ,
	        11 : "Atlantica" ,
	        12 : "DisneyCastle", 
	        13 : "TimelessRiver", 
	        14 : "HalloweenTown",
	        16 : "PortRoyal" ,
	        17 : "SpaceParanoids",
	        18 : "TWTNW" ,
	        255: "GoA"
	        }

        #kh2.base_address+variable
                #the back of sora's inventory
        #subtract 2 everytime sora gets a ability from ap
        self.backofinventory = 0x25CC
        #0x0x2A09C00+0x40 is the sve anchor. +1 is the last saved room
        self.sveroom = 0x2A09C00+0x41
        #0 not in battle 1 in yellow battle 2 red battle #short
        self.inBattle= 0x2A0EAC4+0x40
        #byte
        self.onDeath=0xAB9078
        # PC Address anchors
        self.Now = 0x0714DB8
        self.Save = 0x09A70B0
        self.Sys3 = 0x2A59DF0
        self.Bt10 = 0x2A74880
        self.BtlEnd = 0x2A0D3E0
        self.Slot1 = 0x2A20C98

        #short for ability byte for items

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

#while loop to NOT give item while on death screen
#need to figure out how to tell room address
#initialize the room before the while loop. Probably at the start of a package
#figure out if the room and the going into the room is the same address. I.E. the little platform going into xigbar fight
#look into wait functions to wait for address changes
    def give_item(self,itemcode):
        if itemcode.ability:
            self.kh2.write_short(self.kh2.base_address + self.Save+self.backofinventory, itemcode.memaddr)
        elif itemcode.bitmask>0:
            itemmemory=int.from_bytes( self.kh2.read_bytes( self.kh2.base_address+self.Save+itemmemory,1), "big")
            #write item into the address of that item. then turn on the bitmask of the item.
            self.kh2.write_bytes(self.kh2.base_address+self.Save+itemcode.memaddr,(itemmemory|itemcode.bitmask).to_bytes(1,'big'),1)
        else:
            #Increasing the memory for item by 1 byte
            amount=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.Save+itemcode.memaddr,1), "big")
            self.kh2.write_bytes(self.kh2.base_address + self.Save+itemcode.memaddr,(amount+1).to_bytes(1,'big'),1)

    async def ItemSafe(self,args,svestate):          
        await self.roomSave(args,svestate)
        print("Your Item Is now Safe")


    async def roomSave(self,args,svestate):
        while svestate==self.kh2.read_short(self.kh2.base_address+self.sveroom):
           deathstate=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.onDeath,2), "big")
           if deathstate==1024 or deathstate==1280:
               print("you have died")
               #cannot give item on death screen so waits untill they are not dead
               while deathstate==1024 or deathstate==1280:
                   deathstate=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.onDeath,2), "big")
                   await asyncio.sleep(1)
               print("You have been sent you items again")
               #give item because they have not room saved and are dead
               for item in args['items']:
                   itemname=self.lookup_id_to_item[item.item]
                   itemcode=self.item_name_to_data[itemname]
                   #default false
                   self.give_item(itemcode)
           await asyncio.sleep(1)        
    

      

    def on_package(self, cmd: str, args: dict):
        #if cmd in {"Connected"}:
        #    if not os.path.exists(self.game_communication_path):
        #        os.makedirs(self.game_communication_path)
        #    for ss in self.checked_locations:
        #        filename = f"send{ss}"
        #        with open(os.path.join(self.game_communication_path, filename), 'w') as f:
        #            f.close()
        if cmd in {"ReceivedItems"}:
            #start_index = args["index"]
            #if start_index != len(self.items_received):
                for item in args['items']:
                    itemname=self.lookup_id_to_item[item.item]
                    itemcode=self.item_name_to_data[itemname]
                    #default false
                    self.give_item(itemcode)
                svestate=self.kh2.read_short(self.kh2.base_address+self.sveroom)  
                asyncio.create_task(self.ItemSafe(args,svestate))
        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.checked_locations |= new_locations

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
    
#async def parse_payload(payload: dict, ctx: KH2Context, force: bool):
#
#    # Refuse to do anything if ROM is detected as changed
#    if ctx.auth and payload['playerName'] != ctx.auth:
#        logger.warning("ROM change detected. Disconnecting and reconnecting...")
#        ctx.deathlink_enabled = False
#        ctx.deathlink_client_override = False
#        ctx.finished_game = False
#        ctx.location_table = {}
#        ctx.collectible_table = {}
#        ctx.deathlink_pending = False
#        ctx.deathlink_sent_this_death = False
#        ctx.auth = payload['playerName']
#        await ctx.send_connect()
#        return
#
#    # Turn on deathlink if it is on, and if the client hasn't overriden it
#    if payload['deathlinkActive'] and not ctx.deathlink_enabled and not ctx.deathlink_client_override:
#        await ctx.update_death_link(True)
#        ctx.deathlink_enabled = True
#
#    # Game completion handling
#    if payload['gameComplete'] and not ctx.finished_game:
#        await ctx.send_msgs([{
#            "cmd": "StatusUpdate",
#            "status": 30
#        }])
#        ctx.finished_game = True
#
#    # Locations handling
#    locations = payload['locations']
#    collectibles = payload['collectibles']
#
#    if ctx.location_table != locations or ctx.collectible_table != collectibles:
#        ctx.location_table = locations
#        ctx.collectible_table = collectibles
#        locs1 = [oot_loc_name_to_id[loc] for loc, b in ctx.location_table.items() if b]
#        locs2 = [int(loc) for loc, b in ctx.collectible_table.items() if b]
#        await ctx.send_msgs([{
#            "cmd": "LocationChecks",
#            "locations": locs1 + locs2
#        }])
#
#    # Deathlink handling


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
    logger.info("Please use /autotrack")
   #while not ctx.exit_event.is_set():
   #    if "KINGDOM HEARTS II" in str(subprocess.check_output('tasklist')):
   #        pass
            
            
        #print(ctx.kh2.propertyprocess_base)
        
        #if ctx.kh2.propertyprocess_base>0:
        #    sync_msg = [{'cmd': 'Sync'}]
        #    #if ctx.locations_checked:
        #    #    sync_msg.append({"cmd": "LocationChecks", "locations": list(ctx.locations_checked)})
        #    #await ctx.send_msgs(sync_msg)
        #    #ctx.syncing = False
        #else:
        #    try:
        #        logger.debug("Attempting to connect to N64")
        #        ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 28921), timeout=10)
        #        ctx.n64_status = CONNECTION_TENTATIVE_STATUS
        #    except TimeoutError:
        #        logger.debug("Connection Timed Out, Trying Again")
        #        ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
        #        continue
        #    except ConnectionRefusedError:
        #        logger.debug("Connection Refused, Trying Again")
        #        ctx.n64_status = CONNECTION_REFUSED_STATUS
        #        continue        
       #sending = []
       #victory = False
       #for root, dirs, files in os.walk(ctx.game_communication_path):
       #    for file in files:
       #        if file.find("send") > -1:
       #            st = file.split("send", -1)[1]
       #            sending = sending+[(int(st))]
       #        if file.find("victory") > -1:
       #            victory = True
       #ctx.locations_checked = sending
       #message = [{"cmd": 'LocationChecks', "locations": sending}]
       #await ctx.send_msgs(message)
       #if not ctx.finished_game and victory:
       #    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
       #    ctx.finished_game = True
       #await asyncio.sleep(0.1)


if __name__ == '__main__':
    async def main(args):
        ctx = KH2Context(args.connect, args.password)
        #oot_loc_name_to_id = network_data_package["games"]["Kingdom Hearts 2"]["item_name_to_kh2id"]
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
