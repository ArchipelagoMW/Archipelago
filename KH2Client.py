from __future__ import annotations
import os
import asyncio
from pymem import pymem
import ModuleUpdate

ModuleUpdate.update()
from worlds.kh2.Items import DonaldAbility_Table, GoofyAbility_Table,exclusionItem_table
from worlds.kh2 import all_locations, item_dictionary_table
import Utils
from worlds.kh2 import WorldLocations
import typing
import json
import json

if __name__ == "__main__":
    Utils.init_logging("KH2Client", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

from worlds import network_data_package

kh2_loc_name_to_id = network_data_package["games"]["Kingdom Hearts 2"]["location_name_to_id"]


class KH2CommandProcessor(ClientCommandProcessor):
    def _cmd_autotrack(self):
        """Start Autotracking"""
        # hooking into the game

        if self.ctx.kh2connected:
            logger.info("You are already autotracking")
            return
        try:
            self.ctx.kh2 = pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
            logger.info("You are now auto-tracking")
            self.ctx.kh2connected = True
        except Exception as e:
            if self.ctx.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
            print(e)


class KH2Context(CommonContext):
    command_processor: int = KH2CommandProcessor
    game = "Kingdom Hearts 2"
    items_handling = 0b101  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(KH2Context, self).__init__(server_address, password)
        self.KH2_sync_task = None
        self.syncing = False
        self.kh2connected = False
        self.serverconneced = False
        self.item_name_to_data = {name: data for name, data, in item_dictionary_table.items()}
        self.location_name_to_data = {name: data for name, data, in all_locations.items()}
        self.lookup_id_to_item: typing.Dict[int, str] = {data.code: item_name for item_name, data in
                                                         item_dictionary_table.items() if data.code}
        self.lookup_id_to_Location: typing.Dict[int, str] = {data.code: item_name for item_name, data in
                                                             all_locations.items() if data.code}
        self.location_table = {}
        self.collectible_table = {}
        self.collectible_override_flags_address = 0
        self.collectible_offsets = {}
        self.sending = []
        # flag for if the player has gotten their starting inventory from the server
        self.hasStartingInvo = False
        self.hasThreeProofs=False
        # list used to keep track of locations+items player has. Used for disoneccting
        self.kh2seedsave = {"checked_locations": {"0": []}, "starting_inventory": self.hasStartingInvo}
        self.kh2seedname = None
        self.kh2slotdata = None
        self.inventoryslot={}
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%\KH2AP")
        self.amountOfPieces = 0
        # hooked object
        self.kh2 = None
        self.ItemIsSafe = False
        self.game_connected = False
        self.worldid = {
            1:   WorldLocations.TWTNW_Checks,  # world of darkness (story cutscenes)
            2:   WorldLocations.TT_Checks,
            3:   WorldLocations.TT_Checks,  # destiny island doesnt have checks to ima put tt checks here
            4:   WorldLocations.HB_Checks,
            5:   WorldLocations.BC_Checks,
            6:   WorldLocations.Oc_Checks,
            7:   WorldLocations.AG_Checks,  # Agrabah world id
            8:   WorldLocations.LoD_Checks,
            9:   WorldLocations.HundredAcreChecks,
            10:  WorldLocations.PL_Checks,
            11:  WorldLocations.DC_Checks,  # atlantica isnt a supported world. if you go in atlantica it will check dc
            12:  WorldLocations.DC_Checks,
            13:  WorldLocations.TR_Checks,
            14:  WorldLocations.HT_Checks,
            15:  WorldLocations.HB_Checks,
            # world map but you only go to the world map while on the way to goa so checking hb
            16:  WorldLocations.PR_Checks,
            17:  WorldLocations.SP_Checks,
            18:  WorldLocations.TWTNW_Checks,
            255: WorldLocations.HB_Checks,  # starting screen
        }

        # back of inventory
        # subtract 2 everytime someone gets a ability from ap
        self.backofinventory = 0x25CC
        self.donaldbackofinventory = 0x2678
        self.goofybackofinventory = 0x278E
        # 0x2A09C00+0x40 is the sve anchor. +1 is the last saved room
        self.sveroom = 0x2A09C00 + 0x41
        # 0 not in battle 1 in yellow battle 2 red battle #short
        self.inBattle = 0x2A0EAC4 + 0x40
        self.onDeath = 0xAB9078
        # PC Address anchors
        self.Now = 0x0714DB8
        self.Save = 0x09A70B0
        self.Sys3 = 0x2A59DF0
        self.Bt10 = 0x2A74880
        self.BtlEnd = 0x2A0D3E0
        self.Slot1 = 0x2A20C98

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.kh2connected = False
        with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}.json"), 'w') as f:
            f.write(json.dumps(self.kh2seedsave, indent=4))
        await super(KH2Context, self).connection_closed()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}.json"), 'w') as f:
            f.write(json.dumps(self.kh2seedsave, indent=4))
        await super(KH2Context, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"RoomInfo"}:
            self.kh2seedname = args['seed_name']
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            if not os.path.exists(self.game_communication_path + f"\kh2save{self.kh2seedname}.json"):
                with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}.json"), 'wt') as f:
                    pass
            elif os.path.exists(self.game_communication_path + f"\kh2save{self.kh2seedname}.json"):
                with open(self.game_communication_path + f"\kh2save{self.kh2seedname}.json", 'r') as f:
                    self.kh2seedsave = json.load(f)

        if cmd in {"Connected"}:
            for player in args['players']:
                if str(player.slot) not in self.kh2seedsave["checked_locations"]:
                    self.kh2seedsave["checked_locations"].update({str(player.slot): []})
            self.kh2slotdata = args['slot_data']
            self.serverconneced = True
        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index != len(self.items_received):
                for item in args['items']:
                    itemname = self.lookup_id_to_item[item.item]
                    itemcode = self.item_name_to_data[itemname]
                    if item.location in {-2}:
                        if not self.kh2seedsave["starting_inventory"]:
                            if itemname in DonaldAbility_Table.keys():
                                asyncio.create_task(self.give_item(itemcode, "Donald"))
                            elif itemname in GoofyAbility_Table.keys():
                                asyncio.create_task(self.give_item(itemcode, "Goofy"))
                            else:
                                asyncio.create_task(self.give_item(itemcode, "Sora"))
                    elif item.location not in self.kh2seedsave["checked_locations"][
                        str(item.player)] or item.location in {-1}:
                        if itemname in DonaldAbility_Table.keys():
                            asyncio.create_task(self.give_item(itemcode, "Donald"))
                        elif itemname in GoofyAbility_Table.keys():
                            asyncio.create_task(self.give_item(itemcode, "Goofy"))
                        else:
                            asyncio.create_task(self.give_item(itemcode, "Sora"))
                if not self.kh2seedsave["starting_inventory"]:
                    self.kh2seedsave["starting_inventory"] = True
                try:
                    asyncio.create_task(self.ItemSafe(args))
                except Exception as e:
                    if self.kh2connected:
                        logger.info("Connection Lost, Please /autotrack")
                        self.kh2connected = False
                    print(e)

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.checked_locations |= new_locations

    async def checkWorldLocations(self):
        try:
            curworldid = (
            self.worldid[int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x0714DB8, 1), "big")])
            for location, data in curworldid.items():
                if location not in self.locations_checked:
                    if (int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                       "big") & 0x1 << data.bitIndex) > 0:
                        self.locations_checked.add(location)
                        self.sending = self.sending + [(int(kh2_loc_name_to_id[location]))]
        except Exception as e:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
            print(e)

    async def checkLevels(self):
        try:
            for location, data in WorldLocations.SoraLevels.items():
                if location not in self.locations_checked:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + 0x24FF, 1),
                                      "big") >= data.bitIndex:
                        self.locations_checked.add(location)
                        self.sending = self.sending + [(int(kh2_loc_name_to_id[location]))]
                    else:
                        break
            formDict = {
                0: WorldLocations.ValorLevels, 1: WorldLocations.WisdomLevels, 2: WorldLocations.LimitLevels,
                3: WorldLocations.MasterLevels, 4: WorldLocations.FinalLevels}
            for i in range(5):
                for location, data in formDict[i].items():
                    if location not in self.locations_checked:
                        if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                          "big") >= data.bitIndex:
                            self.locations_checked.add(location)
                            self.sending = self.sending + [(int(kh2_loc_name_to_id[location]))]
        except Exception as e:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
            print(e)
            # checks for items that has checks on their item slot

    async def checkSlots(self):
        try:
            for location, data in WorldLocations.weaponSlots.items():
                if location not in self.locations_checked:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                      "big") > 0:
                        self.locations_checked.add(location)
                        self.sending = self.sending + [(int(kh2_loc_name_to_id[location]))]

            for location, data in WorldLocations.formSlots.items():
                if location not in self.locations_checked:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                      "big") & 0x1 << data.bitIndex > 0:
                        self.locations_checked.add(location)
                        self.sending = self.sending + [(int(kh2_loc_name_to_id[location]))]
        except Exception as e:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
            print(e)

    async def give_item(self, itemcode, char):
        while not self.kh2connected:
            await asyncio.sleep(1)
        itemMemory = 0
        try:
            # cannot give items during loading screens
            # 0x8E9DA3=load 0xAB8BC7=black 0x2A148E8=controable
            while int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x0714DB8, 1), "big") == 255:
                await asyncio.sleep(0.5)
            if itemcode.ability:
                if char == "Donald":
                    self.kh2.write_short(self.kh2.base_address + self.Save + self.donaldbackofinventory,
                                         itemcode.memaddr)
                    self.donaldbackofinventory -= 2
                elif char == "Goofy":
                    self.kh2.write_short(self.kh2.base_address + self.Save + self.goofybackofinventory,
                                         itemcode.memaddr)
                    self.goofybackofinventory -= 2
                else:
                    if itemcode.memaddr in {0x05E, 0x062, 0x066, 0x06A, 0x234}:
                        self.give_growth(itemcode)
                    else:
                        # cannot give stuff past this point or the game will crash
                        if self.backofinventory == 0x2544:
                            return
                        self.kh2.write_short(self.kh2.base_address + self.Save + self.backofinventory, itemcode.memaddr)
                        self.backofinventory -= 2
            elif itemcode.bitmask > 0:
                while int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x8E9DA3, 1),
                                     "big") != 0 or int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + 0xAB8BC7, 1), "big") != 0 \
                        or int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x2A148E8, 1), "big") != 0:
                    await asyncio.sleep(1)
                itemMemory = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + itemcode.memaddr, 1), "big")
                self.kh2.write_bytes(self.kh2.base_address + self.Save + itemcode.memaddr,
                                     (itemMemory | 0x01 << itemcode.bitmask).to_bytes(1, 'big'), 1)
            else:
                while int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x8E9DA3, 1),
                                     "big") != 0 or int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + 0xAB8BC7, 1), "big") != 0 \
                        or int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x2A148E8, 1), "big") != 0:
                    await asyncio.sleep(1)
                # only give statsanity items when drive gauge max is more than 0
                # 2A20C58+base_address+1B2
                amount = int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemcode.memaddr, 1),
                                        "big")
                self.kh2.write_bytes(self.kh2.base_address + self.Save + itemcode.memaddr,
                                     (amount + 1).to_bytes(1, 'big'), 1)
        except Exception as e:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
            print(e)

    async def ItemSafe(self, args):
        while not self.kh2connected:
            await asyncio.sleep(1)
        try:
            svestate = self.kh2.read_short(self.kh2.base_address + self.sveroom)
            await self.roomSave(args, svestate)
        except Exception as e:
            if self.kh2connected:
                logger.info("Connection Lost, Please /autotrack")
                self.kh2connected = False
            print(e)

    async def roomSave(self, args, svestate):
        while svestate == self.kh2.read_short(self.kh2.base_address + self.sveroom):
            deathstate = int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.onDeath, 2), "big")
            if deathstate == 1024 or deathstate == 1280:
                # cannot give item on death screen so waits untill they are not dead
                while deathstate == 1024 or deathstate == 1280:
                    deathstate = int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.onDeath, 2), "big")
                    await asyncio.sleep(0.5)
                # give item because they have not room saved and are dead
                for item in args['items']:
                    itemname = self.lookup_id_to_item[item.item]
                    itemcode = self.item_name_to_data[itemname]
                    if itemname in exclusionItem_table["Ability"] and itemcode.memaddr not in {0x05E, 0x062, 0x066, 0x06A, 0x234}:
                        self.backofinventory+=2
                    if itemname in DonaldAbility_Table.keys():
                        asyncio.create_task(self.give_item(itemcode, "Donald"))
                    elif itemname in GoofyAbility_Table.keys():
                        asyncio.create_task(self.give_item(itemcode, "Goofy"))
                    else:
                        asyncio.create_task(self.give_item(itemcode, "Sora"))
            await asyncio.sleep(1)
        try:
            for item in args['items']:
                if item.location not in self.kh2seedsave["checked_locations"][
                    str(item.player)] and item.location not in {-1, -2}:
                    self.kh2seedsave["checked_locations"][str(item.player)].append(item.location)
        except Exception as e:
            print(e)

    def give_growth(self, itemcode):
        # Credit to num for the goa code and RedBuddha for porting it to python
        # growth is added onto the current growth. Save+0x25CE... is the spots in inventory where they are kept
        # high jump
        if itemcode.memaddr == 0x05E:
            self.growthlevel = self.kh2.read_short(self.kh2.base_address + self.Save + 0x25CE)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x805E:
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25CE, 0x05E)
            elif self.ability | 0x8000 < 0x8061:
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25CE, self.growthlevel + 1)
            # quick run
        elif itemcode.memaddr == 0x062:
            self.growthlevel = self.kh2.read_short(self.kh2.base_address + self.Save + 0x25D0)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x8062:
                # giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D0, 0x062)
            elif self.ability | 0x8000 < 0x8065:
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D0, self.growthlevel + 1)
            # dodge roll
        elif itemcode.memaddr == 0x234:
            self.growthlevel = self.kh2.read_short(self.kh2.base_address + self.Save + 0x25D2)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x8234:
                # giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D2, 0x234)
            elif self.ability | 0x8000 < 0x8237:
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D2, self.growthlevel + 1)
            # aerial dodge
        elif itemcode.memaddr == 0x066:
            self.growthlevel = self.kh2.read_short(self.kh2.base_address + self.Save + 0x25D4)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x8066:
                # giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D4, 0x066)
            elif self.ability | 0x8000 < 0x8069:
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D4, self.growthlevel + 1)
            # glide
        else:
            self.growthlevel = self.kh2.read_short(self.kh2.base_address + self.Save + 0x25D6)
            self.ability = self.growthlevel & 0x0FFF
            if self.ability | 0x8000 < 0x806A:
                # giving level one of the ability
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D6, 0x06A)
            elif self.ability | 0x8000 < 0x806D:
                self.kh2.write_short(self.kh2.base_address + self.Save + 0x25D6, self.growthlevel + 1)

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


async def kh2_watcher(ctx: KH2Context):
    logger.info("Please use /autotrack")
    while not ctx.exit_event.is_set():
        if ctx.kh2connected and ctx.serverconneced:
            try:
                ctx.sending = []
                await asyncio.create_task(ctx.checkWorldLocations())
                await asyncio.create_task(ctx.checkLevels())
                await asyncio.create_task(ctx.checkSlots())
                message = [{"cmd": 'LocationChecks', "locations": ctx.sending}]
                # three proofs
                if ctx.kh2slotdata['Goal'] == 0:
                    if ctx.kh2slotdata['FinalXemnas'] == 1:
                        if 1245677 in message[0]["locations"]:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                    else:
                        if int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x36B2, 1), "big") > 0 \
                                and int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x36B3, 1),
                                                   "big") > 0 \
                                and int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x36B4, 1),
                                                   "big") > 0:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                elif ctx.kh2slotdata['Goal'] == 1:
                    if not ctx.hasThreeProofs and int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x3641, 1), "big") >= \
                            ctx.kh2slotdata['LuckyEmblemsRequired']:
                        ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B2, (1).to_bytes(1, 'big'), 1)
                        ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B3, (1).to_bytes(1, 'big'), 1)
                        ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B4, (1).to_bytes(1, 'big'), 1)
                        ctx.hasThreeProofs=True
                    if ctx.kh2slotdata['FinalXemnas'] == 1:
                            if 1245677 in message[0]["locations"]:
                                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                                ctx.finished_game = True
                    else:
                        if int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x3641, 1), "big") >= \
                                ctx.kh2slotdata['LuckyEmblemsRequired']:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                elif ctx.kh2slotdata['Goal'] == 2:
                    requiredAmountPieces = ctx.kh2slotdata["UltimaWeaponRequired"]
                    for boss in ctx.kh2slotdata["hitlist"]:
                        if boss in message[0]["locations"]:
                            ctx.amountOfPieces += 1
                    if not ctx.hasThreeProofs and ctx.amountOfPieces >= requiredAmountPieces:
                        ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B2, (1).to_bytes(1, 'big'), 1)
                        ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B3, (1).to_bytes(1, 'big'), 1)
                        ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B4, (1).to_bytes(1, 'big'), 1)
                        ctx.hasThreeProofs=True
                    if ctx.kh2slotdata['FinalXemnas'] == 1:
                        if 1245677 in message[0]["locations"]:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                            ctx.finished_game = True
                    elif ctx.amountOfPieces >= requiredAmountPieces:
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                        ctx.finished_game = True
                await ctx.send_msgs(message)
            except Exception as e:
                if ctx.kh2connected:
                    logger.info("Connection Lost, Please /autotrack")
                    ctx.kh2connected = False
                print(e)
        await asyncio.sleep(0.5)


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
