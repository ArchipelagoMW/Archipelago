from __future__ import annotations
import os
import sys
import asyncio
import shutil
from pymem.process import *
from pymem import memory
import ModuleUpdate
ModuleUpdate.update()
from worlds.kh2.Items import DonaldAbility_Table,GoofyAbility_Table
from worlds.kh2 import all_locations, item_dictionary_table
import Utils
from worlds.kh2 import WorldLocations
import typing


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

kh2_loc_name_to_id=network_data_package["games"]["Kingdom Hearts 2"]["location_name_to_id"]


class KH2CommandProcessor(ClientCommandProcessor):
    def _cmd_autotrack(self):
            """Start Autotracking"""
            #hooking into the game
            try:    
                self.ctx.kh2=pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
                logger.info("You are now autotracking")
            except:
                logger.info("Game is not opened/autotrackable")
                return

            self.ctx.kh2connected=True
            


class KH2Context(CommonContext):
    command_processor: int = KH2CommandProcessor
    game = "Kingdom Hearts 2"
    items_handling = 0b101  # Indicates you get items sent from other worlds.

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
        self.KH2_status = CONNECTION_INITIAL_STATUS
        #self.awaiting_rom = False
        self.location_table = {}
        self.collectible_table = {}
        self.collectible_override_flags_address = 0
        self.collectible_offsets = {}
        self.sending = []
        #self.deathlink_enabled = False
        #self.deathlink_pending = False
        #self.deathlink_sent_this_death = False
        #self.deathlink_client_override = False
        #self.version_warning = False
        self.kh2= None
        self.ItemIsSafe = False
        self.game_connected = False
        self.worldid={
	        1 : WorldLocations.TWTNW_Checks,#world of darkness (story cutscenes)
	        2 : WorldLocations.TT_Checks,
	        3 : WorldLocations.TT_Checks,#destiny island doesnt have checks to ima put tt checks here
	        4 : WorldLocations.HB_Checks,
	        5 : WorldLocations.BC_Checks ,
	        6 : WorldLocations.Oc_Checks,
	        7 : WorldLocations.AG_Checks,#Agrabah world id
	        8 : WorldLocations.LoD_Checks,
	        9 : WorldLocations.HundredAcreChecks,
	        10 : WorldLocations.PL_Checks,
	        11 : WorldLocations.DC_Checks ,#atlantica isnt a supported world. if you go in atlantica it will check dc
	        12 : WorldLocations.DC_Checks, 
	        13 : WorldLocations.TR_Checks, 
	        14 : WorldLocations.HT_Checks,
            15 : WorldLocations.HB_Checks,#world map but you only go to the world map while on the way to goa so checking hb
	        16 : WorldLocations.PR_Checks ,
	        17 : WorldLocations.SP_Checks,
	        18 : WorldLocations.TWTNW_Checks ,
	        255: WorldLocations.HB_Checks,#starting screen
	        }

        #these locations have world ids for twtnw
        #LocationName.XigbarDataDefenseBoost:                0x64,
        #LocationName.RoxasDataMagicBoost:                   0x63,
        #LocationName.SaixDataDefenseBoost:                  0x6D,
        #LocationName.LuxordDataAPBoost:                     0x65,
        #these locations have world ids for hb
        #LocationName.MarluxiaDataLostIllusion:      0x96,
        #LocationName.ZexionDataLostIllusion:                      0x98,
        #LocationName.LarxeneDataLostIllusion:            0x94,
        #LocationName.LexaeusDataLostIllusion:           0x93,
        #LocationName.VexenDataLostIllusion:           0x92,
        #if every data is in their normal world

        #kh2.base_address+variable
                #the back of sora's inventory
        #subtract 2 everytime sora gets a ability from ap
        self.backofinventory = 0x25CC
        self.donaldbackofinventory=0x2678
        self.goofybackofinventory=0x278E
        #string for determining who the item is for in the party
        self.character="Sora"
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
        #self.SoraLevel=0
        self.ValorLevel=0
        self.WisdomLevel=0
        self.LimitLevel=0
        self.MasterLevel=0
        self.FinalLevel=0
        #self.SoraLevel=0
        #short for ability byte for items

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.kh2connected=False
        await super(KH2Context, self).connection_closed()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        await super(KH2Context, self).shutdown()




    def give_growth(self,itemcode):
        #Credit to num for the goa and RedBuddha for porting it to python
        #growth is added onto the current growth. Save+0x25CE... is the spots in inventory where they are kept
        #high jump
        if itemcode.memaddr==0x05E:
           self.growthlevel=self.kh2.read_short(self.kh2.base_address + self.Save+0x25CE)
           self.ability = self.growthlevel & 0x0FFF
           if self.ability | 0x8000 < 0x805E:
               self.kh2.write_short(self.kh2.base_address + self.Save+0x25CE, 0x05E)
           elif self.ability | 0x8000 < 0x8061:
               self.kh2.write_short(self.kh2.base_address + self.Save+0x25CE, self.growthlevel+1)
            #quick run
        elif itemcode.memaddr==0x062:
            self.growthlevel=self.kh2.read_short(self.kh2.base_address + self.Save+0x25D0)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x8062:
                #giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D0, 0x062)
            elif self.ability | 0x8000 < 0x8065:
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D0, self.growthlevel+1)
            #dodge roll
        elif itemcode.memaddr==0x234:
            self.growthlevel=self.kh2.read_short(self.kh2.base_address + self.Save+0x25D2)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x8234:
                #giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D2, 0x234)
            elif self.ability | 0x8000 < 0x8237:
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D2, self.growthlevel+1)
            #aerial dodge
        elif itemcode.memaddr==0x066:
            self.growthlevel=self.kh2.read_short(self.kh2.base_address + self.Save+0x25D4)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x8066:
                #giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D4, 0x066)
            elif self.ability | 0x8000 < 0x8069:
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D4, self.growthlevel+1)
            #glide
        else:
            self.growthlevel=self.kh2.read_short(self.kh2.base_address + self.Save+0x25D6)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x806A:
                #giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D6, 0x06A)
            elif self.ability | 0x8000 < 0x806D:
                self.kh2.write_short(self.kh2.base_address + self.Save+0x25D6, self.growthlevel+1)
        
    async def give_item(self,itemcode,char):
        while self.kh2connected==False:
            await asyncio.sleep(1)
        itemMemory=0
        try:
            while int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+0x0714DB8,1), "big")==255:
                await asyncio.sleep(0.5)
            while int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+0x8E9DA3,1), "big")>0 or int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+0xAB8BC7,1), "big")>0:
                await asyncio.sleep(0.5)
            if itemcode.ability:
                if char=="Donald":
                    self.kh2.write_short(self.kh2.base_address + self.Save+self.donaldbackofinventory, itemcode.memaddr)
                    self.donaldbackofinventory-=2
                elif char=="Goofy":
                    self.kh2.write_short(self.kh2.base_address + self.Save+self.goofybackofinventory, itemcode.memaddr)
                    self.goofybackofinventory-=2
                else:
                    if itemcode.memaddr in {0x05E,0x062,0x066,0x06A,0x234}:
                        self.give_growth(itemcode)
                    else:
                        #cannot give stuff past this point or the game will crash
                        if self.backofinventory==0x2544:
                            return
                        self.kh2.write_short(self.kh2.base_address + self.Save+self.backofinventory, itemcode.memaddr)
                        self.backofinventory-=2
            elif itemcode.bitmask>0:
                itemMemory=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.Save+itemcode.memaddr,1), "big")

                self.kh2.write_bytes(self.kh2.base_address+self.Save+itemcode.memaddr,(itemMemory|0x01<<itemcode.bitmask).to_bytes(1,'big'),1)
            else:

                amount=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.Save+itemcode.memaddr,1), "big")
                self.kh2.write_bytes(self.kh2.base_address + self.Save+itemcode.memaddr,(amount+1).to_bytes(1,'big'),1)
        except:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
                return
    async def ItemSafe(self,args,svestate):
        try: 
            await self.roomSave(args,svestate)
        except:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
                return

        #print("Your Item Is now Safe")


    async def roomSave(self,args,svestate):
        while svestate==self.kh2.read_short(self.kh2.base_address+self.sveroom):
           deathstate=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.onDeath,2), "big")
           if deathstate==1024 or deathstate==1280:
               #print("you have died")
               #cannot give item on death screen so waits untill they are not dead
               while deathstate==1024 or deathstate==1280:
                   deathstate=int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+self.onDeath,2), "big")
                   await asyncio.sleep(0.5)
               #print("You have been sent you items again")
               #give item because they have not room saved and are dead
               for item in args['items']:
                   itemname=self.lookup_id_to_item[item.item]
                   itemcode=self.item_name_to_data[itemname]
                   #default false
                   if itemname in DonaldAbility_Table.keys():
                       self.character="Donald"
                       asyncio.create_task(self.give_item(itemcode,"Donald"))
                   elif itemname in GoofyAbility_Table.keys():
                    asyncio.create_task(self.give_item(itemcode,"Goofy"))
                   else:
                       asyncio.create_task(self.give_item(itemcode,"Sora"))
           await asyncio.sleep(0.5)        
    

      

    def on_package(self, cmd: str, args: dict):
        if cmd in {"Connected"}:
                slot_data=args['slot_data']
                for item in slot_data["StationOfCalling_locations"]:
                    if item in self.item_name_to_data:
                        itemcode=self.item_name_to_data[item]
                    else:
                        itemcode=self.item_name_to_data["Lucky Emblem"]
                    if item in DonaldAbility_Table.keys():
                       self.character="Donald"
                       asyncio.create_task(self.give_item(itemcode,"Donald"))
                    elif item in GoofyAbility_Table.keys():
                        asyncio.create_task(self.give_item(itemcode,"Goofy"))
                    else:
                        asyncio.create_task(self.give_item(itemcode,"Sora"))
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    itemname=self.lookup_id_to_item[item.item]
                    itemcode=self.item_name_to_data[itemname]
                    if itemname in DonaldAbility_Table.keys():
                       self.character="Donald"
                       asyncio.create_task(self.give_item(itemcode,"Donald"))
                    elif itemname in GoofyAbility_Table.keys():
                        asyncio.create_task(self.give_item(itemcode,"Goofy"))
                    else:
                           asyncio.create_task(self.give_item(itemcode,"Sora"))

                try:
                    svestate=self.kh2.read_short(self.kh2.base_address+self.sveroom)  
                    asyncio.create_task(self.ItemSafe(args,svestate))
                except:
                    if self.kh2connected:
                        logger.info("Connection Lost, Please /autotrack")
                        self.kh2connected = False
                        return
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

    async def checkWorldLocations(self):
        try:
            curworldid=(self.worldid[int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+0x0714DB8,1), "big")])
            for location,data in curworldid.items():
                if location not in self.locations_checked:
                        if(int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save+data.addrObtained,1), "big") & 0x1<<data.bitIndex)>0:
                            self.locations_checked.add(location)
                            #message = [{"cmd": 'LocationChecks', "locations": boobies[location]}]
                            self.sending = self.sending+[(int(kh2_loc_name_to_id[location]))]
                            #message = [{"cmd": 'LocationChecks', "locations": sending}]    
                        elif data.addrObtained<1000:
                        #    #checking a data check
                            while int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x714DB8+1,1), "big")==data.addrObtained:
                                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x2A0DC00,1), "big")==data.bitIndex:
                                    self.sending = self.sending+[(int(kh2_loc_name_to_id[location]))]
                                await asyncio.sleep(0.5)
        except:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
                return
        #print(WorldLocations.SoraLevels.items())
        
    async def checkLevels(self):
        for location,data in WorldLocations.SoraLevels.items():
            if location not in self.locations_checked:
                try:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+ self.Save + 0x24FF,1), "big")>=data.bitIndex:
                        self.locations_checked.add(location)
                        #message = [{"cmd": 'LocationChecks', "locations": boobies[location]}]
                        #self.SoraLevel+=1
                        self.sending = self.sending+[(int(kh2_loc_name_to_id[location]))]
                        #message = [{"cmd": 'LocationChecks', "locations": sending}]
                    else:
                         break
                except:
                    if self.kh2connected:
                        logger.info("Connection Lost, Please /autotrack")
                        self.kh2connected = False
                        return
        #i=1
        formDict = {0: WorldLocations.ValorLevels, 1:  WorldLocations.WisdomLevels, 2:  WorldLocations.LimitLevels, 3:  WorldLocations.MasterLevels, 4:  WorldLocations.FinalLevels}
        for i in range(5):
            for location,data in formDict[i].items():
                if location not in self.locations_checked:
                    #print(location)
                    try:
                        
                        if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+ self.Save + data.addrObtained,1), "big")>=data.bitIndex:
                            self.locations_checked.add(location)
                            self.sending = self.sending+[(int(kh2_loc_name_to_id[location]))]
                    except:
                        if self.kh2connected:
                            logger.info("Connection Lost, Please /autotrack")
                            self.kh2connected = False
                            return


    #checks for items that has checks on their item slot
    async def checkSlots(self):
        for location,data in WorldLocations.weaponSlots.items():
           if location not in self.locations_checked:
                try:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address+ self.Save + data.addrObtained,1), "big")>0:
                        self.locations_checked.add(location)
                        self.sending = self.sending+[(int(kh2_loc_name_to_id[location]))]
                except:
                    if self.kh2connected:
                        logger.info("Connection Lost, Please /autotrack")
                        self.kh2connected = False
                    return
        for location,data in WorldLocations.formSlots.items():
            if location not in self.locations_checked:
                try:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save+data.addrObtained,1), "big") & 0x1<<data.bitIndex>0:
                        self.locations_checked.add(location)
                        self.sending = self.sending+[(int(kh2_loc_name_to_id[location]))]
                except:
                    if self.kh2connected:
                        logger.info("Connection Lost, Please /autotrack")
                        self.kh2connected = False
                        return
  
  



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
    while not ctx.exit_event.is_set():
        if ctx.kh2connected:     
           #msg = get_payload(ctx).encode()
           #writer.write(msg)
           #writer.write(b'\n')
            try:
                ctx.KH2_status=CONNECTION_CONNECTED_STATUS
                #await asyncio.wait(timeout=1.5)
                try:
                    ctx.sending = []
                    await asyncio.create_task(ctx.checkWorldLocations())
                    await asyncio.create_task(ctx.checkLevels())
                    await asyncio.create_task(ctx.checkSlots())
                    #ctx.locations_checked = ctx.sending
                    message = [{"cmd": 'LocationChecks', "locations": ctx.sending}]
                    await ctx.send_msgs(message)
                except:
                    logger.debug("Read failed due to Connection Lost,Please /autotrack")
                    ctx.KH2_status = CONNECTION_RESET_STATUS
                    ctx.kh2connected = False
            except:
                logger.info("Connection Lost, Please /autotrack")
                ctx.KH2_status = CONNECTION_RESET_STATUS
                ctx.kh2connected = False
        await asyncio.sleep(0.5)   
            


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
