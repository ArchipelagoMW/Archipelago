import os
import asyncio
import ModuleUpdate
import json
import Utils
from pymem import pymem
from worlds.kh2.Items import exclusionItem_table, CheckDupingItems
from worlds.kh2 import all_locations, item_dictionary_table, exclusion_table

from worlds.kh2.WorldLocations import *

from worlds import network_data_package

if __name__ == "__main__":
    Utils.init_logging("KH2Client", exception_logger="Client")

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, ClientCommandProcessor, \
    CommonContext, server_loop

ModuleUpdate.update()

kh2_loc_name_to_id = network_data_package["games"]["Kingdom Hearts 2"]["location_name_to_id"]


# class KH2CommandProcessor(ClientCommandProcessor):


class KH2Context(CommonContext):
    # command_processor: int = KH2CommandProcessor
    game = "Kingdom Hearts 2"
    items_handling = 0b101  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(KH2Context, self).__init__(server_address, password)
        self.kh2LocalItems = None
        self.ability = None
        self.growthlevel = None
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
        self.location_name_to_worlddata = {name: data for name, data, in all_world_locations.items()}

        self.location_table = {}
        self.collectible_table = {}
        self.collectible_override_flags_address = 0
        self.collectible_offsets = {}
        self.sending = []
        # list used to keep track of locations+items player has. Used for disoneccting
        self.kh2seedsave = None
        self.slotDataProgressionNames = {}
        self.kh2seedname = None
        self.kh2slotdata = None
        self.itemamount = {}
        # sora equipped, valor equipped, master equipped, final equipped
        self.keybladeAnchorList = (0x24F0, 0x32F4, 0x339C, 0x33D4)
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%\KH2AP")
        self.amountOfPieces = 0
        # hooked object
        self.kh2 = None
        self.ItemIsSafe = False
        self.game_connected = False
        self.finalxemnas = False
        self.worldid = {
            #  1:   {},  # world of darkness (story cutscenes)
            2:  TT_Checks,
            #  3:   {},  # destiny island doesn't have checks to ima put tt checks here
            4:  HB_Checks,
            5:  BC_Checks,
            6:  Oc_Checks,
            7:  AG_Checks,
            8:  LoD_Checks,
            9:  HundredAcreChecks,
            10: PL_Checks,
            11: DC_Checks,  # atlantica isn't a supported world. if you go in atlantica it will check dc
            12: DC_Checks,
            13: TR_Checks,
            14: HT_Checks,
            15: HB_Checks,  # world map, but you only go to the world map while on the way to goa so checking hb
            16: PR_Checks,
            17: SP_Checks,
            18: TWTNW_Checks,
            #  255: {},  # starting screen
        }
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

        self.chest_set = set(exclusion_table["Chests"])

        self.keyblade_set = set(CheckDupingItems["Weapons"]["Keyblades"])
        self.staff_set = set(CheckDupingItems["Weapons"]["Staffs"])
        self.shield_set = set(CheckDupingItems["Weapons"]["Shields"])

        self.all_weapons = self.keyblade_set.union(self.staff_set).union(self.shield_set)

        self.equipment_categories = CheckDupingItems["Equipment"]
        self.armor_set = set(self.equipment_categories["Armor"])
        self.accessories_set = set(self.equipment_categories["Accessories"])
        self.all_equipment = self.armor_set.union(self.accessories_set)

        self.Equipment_Anchor_Dict = {
            "Armor":       [0x2504, 0x2506, 0x2508, 0x250A],
            "Accessories": [0x2514, 0x2516, 0x2518, 0x251A]}

        self.AbilityQuantityDict = {}
        self.ability_categories = CheckDupingItems["Abilities"]

        self.sora_ability_set = set(self.ability_categories["Sora"])
        self.donald_ability_set = set(self.ability_categories["Donald"])
        self.goofy_ability_set = set(self.ability_categories["Goofy"])

        self.all_abilities = self.sora_ability_set.union(self.donald_ability_set).union(self.goofy_ability_set)

        self.boost_set = set(CheckDupingItems["Boosts"])
        self.stat_increase_set = set(CheckDupingItems["Stat Increases"])
        self.AbilityQuantityDict = {item: self.item_name_to_data[item].quantity for item in self.all_abilities}
        #  Growth:[level 1,level 4,slot]
        self.growth_values_dict = {"High Jump":    [0x05E, 0x061, 0x25DA],
                                   "Quick Run":    [0x62, 0x65, 0x25DC],
                                   "Dodge Roll":   [0x234, 0x237, 0x25DE],
                                   "Aerial Dodge": [0x066, 0x069, 0x25E0],
                                   "Glide":        [0x6A, 0x6D, 0x25E2]}
        self.boost_to_anchor_dict = {
            "Power Boost":   0x24F9,
            "Magic Boost":   0x24FA,
            "Defense Boost": 0x24FB,
            "AP Boost":      0x24F8}

        self.AbilityCodeList = [self.item_name_to_data[item].code for item in exclusionItem_table["Ability"]]
        self.master_growth = {"High Jump", "Quick Run", "Dodge Roll", "Aerial Dodge", "Glide"}

        self.bitmask_item_code = [
            0x130000, 0x130001, 0x130002, 0x130003, 0x130004, 0x130005, 0x130006, 0x130007
            , 0x130008, 0x130009, 0x13000A, 0x13000B, 0x13000C
            , 0x13001F, 0x130020, 0x130021, 0x130022, 0x130023
            , 0x13002A, 0x13002B, 0x13002C, 0x13002D]

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.kh2connected = False
        self.serverconneced = False
        if self.kh2seedname is not None and self.auth is not None:
            with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}{self.auth}.json"),
                      'w') as f:
                f.write(json.dumps(self.kh2seedsave, indent=4))
        await super(KH2Context, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.kh2connected = False
        self.serverconneced = False
        if self.kh2seedname not in {None} and self.auth not in {None}:
            with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}{self.auth}.json"),
                      'w') as f:
                f.write(json.dumps(self.kh2seedsave, indent=4))
        await super(KH2Context, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        if self.kh2seedname not in {None} and self.auth not in {None}:
            with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}{self.auth}.json"),
                      'w') as f:
                f.write(json.dumps(self.kh2seedsave, indent=4))
        await super(KH2Context, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd in {"RoomInfo"}:
            self.kh2seedname = args['seed_name']
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            if not os.path.exists(self.game_communication_path + f"\kh2save{self.kh2seedname}{self.auth}.json"):
                self.kh2seedsave = {"itemIndex":        -1,
                                    # back of soras invo is 0x25E2. Growth should be moved there
                                    #  Character: [back of invo, front of invo]
                                    "SoraInvo":         [0x25D8, 0x2546],
                                    "DonaldInvo":       [0x26F4, 0x2658],
                                    "GoofyInvo":        [0x280A, 0x276C],
                                    "AmountInvo":       {
                                        "ServerItems": {
                                            "Ability":      {},
                                            "Amount":       {},
                                            "Growth":       {"High Jump":    0, "Quick Run": 0, "Dodge Roll": 0,
                                                             "Aerial Dodge": 0,
                                                             "Glide":        0},
                                            "Bitmask":      [],
                                            "Weapon":       {"Sora": [], "Donald": [], "Goofy": []},
                                            "Equipment":    [],
                                            "Magic":        {},
                                            "StatIncrease": {},
                                            "Boost":        {},
                                        },
                                        "LocalItems":  {
                                            "Ability":      {},
                                            "Amount":       {},
                                            "Growth":       {"High Jump":    0, "Quick Run": 0, "Dodge Roll": 0,
                                                             "Aerial Dodge": 0, "Glide": 0},
                                            "Bitmask":      [],
                                            "Weapon":       {"Sora": [], "Donald": [], "Goofy": []},
                                            "Equipment":    [],
                                            "Magic":        {},
                                            "StatIncrease": {},
                                            "Boost":        {},
                                        }},
                                    #  1,3,255 are in this list in case the player gets locations in those "worlds" and I need to still have them checked
                                    "LocationsChecked": [],
                                    "Levels":           {
                                        "SoraLevel":   0,
                                        "ValorLevel":  0,
                                        "WisdomLevel": 0,
                                        "LimitLevel":  0,
                                        "MasterLevel": 0,
                                        "FinalLevel":  0,
                                    },
                                    "SoldEquipment":    [],
                                    "SoldBoosts":       {"Power Boost":   0,
                                                         "Magic Boost":   0,
                                                         "Defense Boost": 0,
                                                         "AP Boost":      0}
                                    }
                with open(os.path.join(self.game_communication_path, f"kh2save{self.kh2seedname}{self.auth}.json"),
                          'wt') as f:
                    pass
                self.locations_checked = set()
            elif os.path.exists(self.game_communication_path + f"\kh2save{self.kh2seedname}{self.auth}.json"):
                with open(self.game_communication_path + f"\kh2save{self.kh2seedname}{self.auth}.json", 'r') as f:
                    self.kh2seedsave = json.load(f)
                    self.locations_checked = set(self.kh2seedsave["LocationsChecked"])
            self.serverconneced = True

        if cmd in {"Connected"}:
            self.kh2slotdata = args['slot_data']
            self.kh2LocalItems = {int(location): item for location, item in self.kh2slotdata["LocalItems"].items()}
            try:
                self.kh2 = pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
                logger.info("You are now auto-tracking")
                self.kh2connected = True
            except Exception as e:
                logger.info("Line 247")
                if self.kh2connected:
                    logger.info("Connection Lost")
                    self.kh2connected = False
                logger.info(e)

        if cmd in {"ReceivedItems"}:
            start_index = args["index"]
            if start_index == 0:
                # resetting everything that were sent from the server
                self.kh2seedsave["SoraInvo"][0] = 0x25D8
                self.kh2seedsave["DonaldInvo"][0] = 0x26F4
                self.kh2seedsave["GoofyInvo"][0] = 0x280A
                self.kh2seedsave["itemIndex"] = - 1
                self.kh2seedsave["AmountInvo"]["ServerItems"] = {
                    "Ability":      {},
                    "Amount":       {},
                    "Growth":       {"High Jump":    0, "Quick Run": 0, "Dodge Roll": 0,
                                     "Aerial Dodge": 0,
                                     "Glide":        0},
                    "Bitmask":      [],
                    "Weapon":       {"Sora": [], "Donald": [], "Goofy": []},
                    "Equipment":    [],
                    "Magic":        {},
                    "StatIncrease": {},
                    "Boost":        {},
                }
            if start_index > self.kh2seedsave["itemIndex"]:
                self.kh2seedsave["itemIndex"] = start_index
                for item in args['items']:
                    asyncio.create_task(self.give_item(item.item))

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                # TODO: make this take locations from other players on the same slot so proper coop happens
                #  items_to_give = [self.kh2slotdata["LocalItems"][str(location_id)] for location_id in new_locations if
                #                 location_id in self.kh2LocalItems.keys()]
                self.checked_locations |= new_locations

    async def checkWorldLocations(self):
        try:
            currentworldint = int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x0714DB8, 1), "big")
            if currentworldint in self.worldid:
                curworldid = self.worldid[currentworldint]
                for location, data in curworldid.items():
                    locationId = kh2_loc_name_to_id[location]
                    if locationId not in self.locations_checked \
                            and (int.from_bytes(
                            self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                            "big") & 0x1 << data.bitIndex) > 0:
                        self.sending = self.sending + [(int(locationId))]
        except Exception as e:
            logger.info("Line 285")
            if self.kh2connected:
                logger.info("Connection Lost.")
                self.kh2connected = False
            logger.info(e)

    async def checkLevels(self):
        try:
            for location, data in SoraLevels.items():
                currentLevel = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + 0x24FF, 1), "big")
                locationId = kh2_loc_name_to_id[location]
                if locationId not in self.locations_checked \
                        and currentLevel >= data.bitIndex:
                    if self.kh2seedsave["Levels"]["SoraLevel"] < currentLevel:
                        self.kh2seedsave["Levels"]["SoraLevel"] = currentLevel
                    self.sending = self.sending + [(int(locationId))]
            formDict = {
                0: ["ValorLevel", ValorLevels], 1: ["WisdomLevel", WisdomLevels], 2: ["LimitLevel", LimitLevels],
                3: ["MasterLevel", MasterLevels], 4: ["FinalLevel", FinalLevels]}
            for i in range(5):
                for location, data in formDict[i][1].items():
                    formlevel = int.from_bytes(
                            self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1), "big")
                    locationId = kh2_loc_name_to_id[location]
                    if locationId not in self.locations_checked \
                            and formlevel >= data.bitIndex:
                        if formlevel > self.kh2seedsave["Levels"][formDict[i][0]]:
                            self.kh2seedsave["Levels"][formDict[i][0]] = formlevel
                        self.sending = self.sending + [(int(locationId))]
        except Exception as e:
            logger.info("Line 312")
            if self.kh2connected:
                logger.info("Connection Lost.")
                self.kh2connected = False
            logger.info(e)

    async def checkSlots(self):
        try:
            for location, data in weaponSlots.items():
                locationId = kh2_loc_name_to_id[location]
                if locationId not in self.locations_checked:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                      "big") > 0:
                        self.sending = self.sending + [(int(locationId))]

            for location, data in formSlots.items():
                locationId = kh2_loc_name_to_id[location]
                if locationId not in self.locations_checked:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                      "big") & 0x1 << data.bitIndex > 0:
                        # self.locations_checked
                        self.sending = self.sending + [(int(locationId))]

        except Exception as e:
            if self.kh2connected:
                logger.info("Line 333")
                logger.info("Connection Lost.")
                self.kh2connected = False
            logger.info(e)

    async def verifyChests(self):
        try:
            for location in self.locations_checked:
                locationName = self.lookup_id_to_Location[location]
                if locationName in self.chest_set:
                    if locationName in self.location_name_to_worlddata.keys():
                        locationData = self.location_name_to_worlddata[locationName]
                        if int.from_bytes(
                                self.kh2.read_bytes(self.kh2.base_address + self.Save + locationData.addrObtained, 1),
                                "big") & 0x1 << locationData.bitIndex == 0:
                            roomData = int.from_bytes(
                                    self.kh2.read_bytes(self.kh2.base_address + self.Save + locationData.addrObtained,
                                                        1), "big")
                            self.kh2.write_bytes(self.kh2.base_address + self.Save + locationData.addrObtained,
                                                 (roomData | 0x01 << locationData.bitIndex).to_bytes(1, 'big'), 1)

        except Exception as e:
            if self.kh2connected:
                logger.info("Line 350")
                logger.info("Connection Lost.")
                self.kh2connected = False
            logger.info(e)

    async def verifyLevel(self):
        for leveltype, anchor in {"SoraLevel":   0x24FF,
                                  "ValorLevel":  0x32F6,
                                  "WisdomLevel": 0x332E,
                                  "LimitLevel":  0x3366,
                                  "MasterLevel": 0x339E,
                                  "FinalLevel":  0x33D6}.items():
            if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + anchor, 1), "big") < \
                    self.kh2seedsave["Levels"][leveltype]:
                self.kh2.write_bytes(self.kh2.base_address + self.Save + anchor,
                                     (self.kh2seedsave["Levels"][leveltype]).to_bytes(1, 'big'), 1)

    async def give_item(self, item, ItemType="ServerItems"):
        try:
            itemname = self.lookup_id_to_item[item]
            itemcode = self.item_name_to_data[itemname]
            if itemcode.ability:
                abilityInvoType = 0
                TwilightZone = 2
                if ItemType == "LocalItems":
                    abilityInvoType = 1
                    TwilightZone = -2
                if itemname in {"High Jump", "Quick Run", "Dodge Roll", "Aerial Dodge", "Glide"}:
                    self.kh2seedsave["AmountInvo"][ItemType]["Growth"][itemname] += 1
                    return

                if itemname not in self.kh2seedsave["AmountInvo"][ItemType]["Ability"]:
                    self.kh2seedsave["AmountInvo"][ItemType]["Ability"][itemname] = []
                    #  appending the slot that the ability should be in

                if len(self.kh2seedsave["AmountInvo"][ItemType]["Ability"][itemname]) < \
                        self.AbilityQuantityDict[itemname]:
                    if itemname in self.sora_ability_set:
                        self.kh2seedsave["AmountInvo"][ItemType]["Ability"][itemname].append(
                                self.kh2seedsave["SoraInvo"][abilityInvoType])
                        self.kh2seedsave["SoraInvo"][abilityInvoType] -= TwilightZone
                    elif itemname in self.donald_ability_set:
                        self.kh2seedsave["AmountInvo"][ItemType]["Ability"][itemname].append(
                                self.kh2seedsave["DonaldInvo"][abilityInvoType])
                        self.kh2seedsave["DonaldInvo"][abilityInvoType] -= TwilightZone
                    else:
                        self.kh2seedsave["AmountInvo"][ItemType]["Ability"][itemname].append(
                                self.kh2seedsave["GoofyInvo"][abilityInvoType])
                        self.kh2seedsave["GoofyInvo"][abilityInvoType] -= TwilightZone

            elif itemcode.code in self.bitmask_item_code:

                if itemname not in self.kh2seedsave["AmountInvo"][ItemType]["Bitmask"]:
                    self.kh2seedsave["AmountInvo"][ItemType]["Bitmask"].append(itemname)

            elif itemcode.memaddr in {0x3594, 0x3595, 0x3596, 0x3597, 0x35CF, 0x35D0}:

                if itemname in self.kh2seedsave["AmountInvo"][ItemType]["Magic"]:
                    self.kh2seedsave["AmountInvo"][ItemType]["Magic"][itemname] += 1
                else:
                    self.kh2seedsave["AmountInvo"][ItemType]["Magic"][itemname] = 1
            elif itemname in self.all_equipment:

                self.kh2seedsave["AmountInvo"][ItemType]["Equipment"].append(itemname)

            elif itemname in self.all_weapons:
                if itemname in self.keyblade_set:
                    self.kh2seedsave["AmountInvo"][ItemType]["Weapon"]["Sora"].append(itemname)
                elif itemname in self.staff_set:
                    self.kh2seedsave["AmountInvo"][ItemType]["Weapon"]["Donald"].append(itemname)
                else:
                    self.kh2seedsave["AmountInvo"][ItemType]["Weapon"]["Goofy"].append(itemname)

            elif itemname in self.boost_set:
                if itemname in self.kh2seedsave["AmountInvo"][ItemType]["Boost"]:
                    self.kh2seedsave["AmountInvo"][ItemType]["Boost"][itemname] += 1
                else:
                    self.kh2seedsave["AmountInvo"][ItemType]["Boost"][itemname] = 1

            elif itemname in self.stat_increase_set:

                if itemname in self.kh2seedsave["AmountInvo"][ItemType]["StatIncrease"]:
                    self.kh2seedsave["AmountInvo"][ItemType]["StatIncrease"][itemname] += 1
                else:
                    self.kh2seedsave["AmountInvo"][ItemType]["StatIncrease"][itemname] = 1

            else:
                if itemname in self.kh2seedsave["AmountInvo"][ItemType]["Amount"]:
                    self.kh2seedsave["AmountInvo"][ItemType]["Amount"][itemname] += 1
                else:
                    self.kh2seedsave["AmountInvo"][ItemType]["Amount"][itemname] = 1

        except Exception as e:
            if self.kh2connected:
                logger.info("Line 398")
                logger.info("Connection Lost.")
                self.kh2connected = False
            logger.info(e)

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

    async def IsInShop(self, sellable, master_boost):
        # journal = 0x741230 shop = 0x741320
        # if journal=-1 and shop = 5 then in shop
        # if journam !=-1 and shop = 10 then journal
        journal = self.kh2.read_short(self.kh2.base_address + 0x741230)
        shop = self.kh2.read_short(self.kh2.base_address + 0x741320)
        if (journal == -1 and shop == 5) or (journal != -1 and shop == 10):
            # print("your in the shop")
            sellable_dict = {}
            for itemName in sellable:
                itemdata = self.item_name_to_data[itemName]
                amount = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + itemdata.memaddr, 1), "big")
                sellable_dict[itemName] = amount
            while (journal == -1 and shop == 5) or (journal != -1 and shop == 10):
                journal = self.kh2.read_short(self.kh2.base_address + 0x741230)
                shop = self.kh2.read_short(self.kh2.base_address + 0x741320)
                await asyncio.sleep(0.5)
            for item, amount in sellable_dict.items():
                itemdata = self.item_name_to_data[item]
                afterShop = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + itemdata.memaddr, 1), "big")
                if afterShop < amount:
                    if item in master_boost:
                        self.kh2seedsave["SoldBoosts"][item] += (amount - afterShop)
                    else:
                        self.kh2seedsave["SoldEquipment"].append(item)

    async def verifyItems(self):
        try:
            local_amount = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Amount"].keys())
            server_amount = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Amount"].keys())
            master_amount = local_amount | server_amount

            local_ability = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Ability"].keys())
            server_ability = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Ability"].keys())
            master_ability = local_ability | server_ability

            local_bitmask = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Bitmask"])
            server_bitmask = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Bitmask"])
            master_bitmask = local_bitmask | server_bitmask

            local_keyblade = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Weapon"]["Sora"])
            local_staff = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Weapon"]["Donald"])
            local_shield = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Weapon"]["Goofy"])

            server_keyblade = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Weapon"]["Sora"])
            server_staff = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Weapon"]["Donald"])
            server_shield = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Weapon"]["Goofy"])

            master_keyblade = local_keyblade | server_keyblade
            master_staff = local_staff | server_staff
            master_shield = local_shield | server_shield

            local_equipment = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Equipment"])
            server_equipment = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Equipment"])
            master_equipment = local_equipment | server_equipment

            local_magic = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Magic"].keys())
            server_magic = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Magic"].keys())
            master_magic = local_magic | server_magic

            local_stat = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["StatIncrease"].keys())
            server_stat = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["StatIncrease"].keys())
            master_stat = local_stat | server_stat

            local_boost = set(self.kh2seedsave["AmountInvo"]["LocalItems"]["Boost"].keys())
            server_boost = set(self.kh2seedsave["AmountInvo"]["ServerItems"]["Boost"].keys())
            master_boost = local_boost | server_boost

            master_sell = master_equipment | master_staff | master_shield | master_boost
            await asyncio.create_task(self.IsInShop(master_sell, master_boost))
            for itemName in master_amount:
                itemData = self.item_name_to_data[itemName]
                amountOfItems = 0
                if itemName in local_amount:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["LocalItems"]["Amount"][itemName]
                if itemName in server_amount:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["ServerItems"]["Amount"][itemName]

                if itemName == "Torn Page":
                    # Torn Pages are handled differently because they can be consumed.
                    # Will check the progression in 100 acre and - the amount of visits
                    # amountofitems-amount of visits done
                    for location, data in tornPageLocks.items():
                        if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + data.addrObtained, 1),
                                          "big") & 0x1 << data.bitIndex > 0:
                            amountOfItems -= 1
                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                  "big") != amountOfItems and amountOfItems >= 0:
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         amountOfItems.to_bytes(1, 'big'), 1)

            for itemName in master_keyblade:
                itemData = self.item_name_to_data[itemName]
                # if the inventory slot for that keyblade is less than the amount they should have
                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                  "big") != 1 and int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x1CFF, 1),
                                                                 "big") != 13:
                    # Checking form anchors for the keyblade
                    if self.kh2.read_short(self.kh2.base_address + self.Save + 0x24F0) == itemData.kh2id \
                            or self.kh2.read_short(self.kh2.base_address + self.Save + 0x32F4) == itemData.kh2id \
                            or self.kh2.read_short(self.kh2.base_address + self.Save + 0x339C) == itemData.kh2id \
                            or self.kh2.read_short(self.kh2.base_address + self.Save + 0x33D4) == itemData.kh2id:
                        self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                             (0).to_bytes(1, 'big'), 1)
                    else:
                        self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                             (1).to_bytes(1, 'big'), 1)
            for itemName in master_staff:
                itemData = self.item_name_to_data[itemName]
                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                  "big") != 1 \
                        and self.kh2.read_short(self.kh2.base_address + self.Save + 0x2604) != itemData.kh2id \
                        and itemName not in self.kh2seedsave["SoldEquipment"]:
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         (1).to_bytes(1, 'big'), 1)

            for itemName in master_shield:
                itemData = self.item_name_to_data[itemName]
                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                  "big") != 1 \
                        and self.kh2.read_short(self.kh2.base_address + self.Save + 0x2718) != itemData.kh2id \
                        and itemName not in self.kh2seedsave["SoldEquipment"]:
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         (1).to_bytes(1, 'big'), 1)

            for itemName in master_ability:
                itemData = self.item_name_to_data[itemName]
                ability_slot = []
                if itemName in local_ability:
                    ability_slot += self.kh2seedsave["AmountInvo"]["LocalItems"]["Ability"][itemName]
                if itemName in server_ability:
                    ability_slot += self.kh2seedsave["AmountInvo"]["ServerItems"]["Ability"][itemName]
                for slot in ability_slot:
                    current = self.kh2.read_short(self.kh2.base_address + self.Save + slot)
                    ability = current & 0x0FFF
                    if ability | 0x8000 != (0x8000 + itemData.memaddr):
                        if current - 0x8000 > 0:
                            self.kh2.write_short(self.kh2.base_address + self.Save + slot, (0x8000 + itemData.memaddr))
                        else:
                            self.kh2.write_short(self.kh2.base_address + self.Save + slot, itemData.memaddr)
            # removes the duped ability if client gave faster than the game.
            for charInvo in {"SoraInvo", "DonaldInvo", "GoofyInvo"}:
                if self.kh2.read_short(self.kh2.base_address + self.Save + self.kh2seedsave[charInvo][1]) != 0 and \
                        self.kh2seedsave[charInvo][1] + 2 < self.kh2seedsave[charInvo][0]:
                    self.kh2.write_short(self.kh2.base_address + self.Save + self.kh2seedsave[charInvo][1], 0)
            # remove the dummy level 1 growths if they are in these invo slots.
            for inventorySlot in {0x25CE, 0x25D0, 0x25D2, 0x25D4, 0x25D6, 0x25D8}:
                current = self.kh2.read_short(self.kh2.base_address + self.Save + inventorySlot)
                ability = current & 0x0FFF
                if 0x05E <= ability <= 0x06D:
                    self.kh2.write_short(self.kh2.base_address + self.Save + inventorySlot, 0)

            for itemName in self.master_growth:
                growthLevel = self.kh2seedsave["AmountInvo"]["ServerItems"]["Growth"][itemName] \
                              + self.kh2seedsave["AmountInvo"]["LocalItems"]["Growth"][itemName]
                if growthLevel > 0:
                    slot = self.growth_values_dict[itemName][2]
                    min_growth = self.growth_values_dict[itemName][0]
                    max_growth = self.growth_values_dict[itemName][1]
                    if growthLevel > 4:
                        growthLevel = 4
                    current_growth_level = self.kh2.read_short(self.kh2.base_address + self.Save + slot)
                    ability = current_growth_level & 0x0FFF
                    # if the player should be getting a growth ability
                    if ability | 0x8000 != 0x8000 + min_growth - 1 + growthLevel:
                        # if it should be level one of that growth
                        if 0x8000 + min_growth - 1 + growthLevel <= 0x8000 + min_growth or ability < min_growth:
                            self.kh2.write_short(self.kh2.base_address + self.Save + slot, min_growth)
                        # if it is already in the inventory
                        elif ability | 0x8000 < (0x8000 + max_growth):
                            self.kh2.write_short(self.kh2.base_address + self.Save + slot, current_growth_level + 1)

            for itemName in master_bitmask:
                itemData = self.item_name_to_data[itemName]
                itemMemory = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1), "big")
                if (int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                   "big") & 0x1 << itemData.bitmask) == 0:
                    # when getting a form anti points should be reset to 0 but bit-shift doesn't trigger the game.
                    if itemName in {"Valor Form", "Wisdom Form", "Limit Form", "Master Form", "Final Form"}:
                        self.kh2.write_bytes(self.kh2.base_address + self.Save + 0x3410,
                                             (0).to_bytes(1, 'big'), 1)
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         (itemMemory | 0x01 << itemData.bitmask).to_bytes(1, 'big'), 1)

            for itemName in master_equipment:
                itemData = self.item_name_to_data[itemName]
                isThere = False
                if itemName in self.accessories_set:
                    Equipment_Anchor_List = self.Equipment_Anchor_Dict["Accessories"]
                else:
                    Equipment_Anchor_List = self.Equipment_Anchor_Dict["Armor"]
                    # Checking form anchors for the equipment
                for slot in Equipment_Anchor_List:
                    if self.kh2.read_short(self.kh2.base_address + self.Save + slot) == itemData.kh2id:
                        isThere = True
                        if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                          "big") != 0:
                            self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                                 (0).to_bytes(1, 'big'), 1)
                        break
                if not isThere and itemName not in self.kh2seedsave["SoldEquipment"]:
                    if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                      "big") != 1:
                        self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                             (1).to_bytes(1, 'big'), 1)

            for itemName in master_magic:
                itemData = self.item_name_to_data[itemName]
                amountOfItems = 0
                if itemName in local_magic:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["LocalItems"]["Magic"][itemName]
                if itemName in server_magic:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["ServerItems"]["Magic"][itemName]
                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                  "big") != amountOfItems \
                        and int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + 0x741320, 1), "big") in {10, 8}:
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         amountOfItems.to_bytes(1, 'big'), 1)

            for itemName in master_stat:
                itemData = self.item_name_to_data[itemName]
                amountOfItems = 0
                if itemName in local_stat:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["LocalItems"]["StatIncrease"][itemName]
                if itemName in server_stat:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["ServerItems"]["StatIncrease"][itemName]

                # 0x130293 is Crit_1's location id for touching the computer
                if int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                                  "big") != amountOfItems \
                        and int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + self.Slot1 + 0x1B2, 1),
                                           "big") >= 5 and int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + 0x23DF, 1),
                        "big") > 0:
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         amountOfItems.to_bytes(1, 'big'), 1)

            for itemName in master_boost:
                itemData = self.item_name_to_data[itemName]
                amountOfItems = 0
                if itemName in local_boost:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["LocalItems"]["Boost"][itemName]
                if itemName in server_boost:
                    amountOfItems += self.kh2seedsave["AmountInvo"]["ServerItems"]["Boost"][itemName]
                amountOfBoostsInInvo = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + itemData.memaddr, 1),
                        "big")
                amountOfUsedBoosts = int.from_bytes(
                        self.kh2.read_bytes(self.kh2.base_address + self.Save + self.boost_to_anchor_dict[itemName], 1),
                        "big")
                # Ap Boots start at +50 for some reason
                if itemName == "AP Boost":
                    amountOfUsedBoosts -= 50
                totalBoosts = (amountOfBoostsInInvo + amountOfUsedBoosts)
                if totalBoosts <= amountOfItems - self.kh2seedsave["SoldBoosts"][
                    itemName] and amountOfBoostsInInvo < 255:
                    self.kh2.write_bytes(self.kh2.base_address + self.Save + itemData.memaddr,
                                         (amountOfBoostsInInvo + 1).to_bytes(1, 'big'), 1)

        except Exception as e:
            logger.info("Line 573")
            if self.kh2connected:
                logger.info("Connection Lost.")
                self.kh2connected = False
            logger.info(e)


def finishedGame(ctx: KH2Context, message):
    if ctx.kh2slotdata['FinalXemnas'] == 1:
        if 0x1301ED in message[0]["locations"]:
            ctx.finalxemnas = True
    # three proofs
    if ctx.kh2slotdata['Goal'] == 0:
        if int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x36B2, 1), "big") > 0 \
                and int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x36B3, 1), "big") > 0 \
                and int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x36B4, 1), "big") > 0:
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.finalxemnas:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    elif ctx.kh2slotdata['Goal'] == 1:
        if int.from_bytes(ctx.kh2.read_bytes(ctx.kh2.base_address + ctx.Save + 0x3641, 1), "big") >= \
                ctx.kh2slotdata['LuckyEmblemsRequired']:
            ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B2, (1).to_bytes(1, 'big'), 1)
            ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B3, (1).to_bytes(1, 'big'), 1)
            ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B4, (1).to_bytes(1, 'big'), 1)
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.finalxemnas:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False
    elif ctx.kh2slotdata['Goal'] == 2:
        for boss in ctx.kh2slotdata["hitlist"]:
            if boss in message[0]["locations"]:
                ctx.amountOfPieces += 1
        if ctx.amountOfPieces >= ctx.kh2slotdata["BountyRequired"]:
            ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B2, (1).to_bytes(1, 'big'), 1)
            ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B3, (1).to_bytes(1, 'big'), 1)
            ctx.kh2.write_bytes(ctx.kh2.base_address + ctx.Save + 0x36B4, (1).to_bytes(1, 'big'), 1)
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.finalxemnas:
                    return True
                else:
                    return False
            else:
                return True
        else:
            return False


async def kh2_watcher(ctx: KH2Context):
    while not ctx.exit_event.is_set():
        try:
            if ctx.kh2connected and ctx.serverconneced:
                ctx.sending = []
                await asyncio.create_task(ctx.checkWorldLocations())
                await asyncio.create_task(ctx.checkLevels())
                await asyncio.create_task(ctx.checkSlots())
                await asyncio.create_task(ctx.verifyChests())
                await asyncio.create_task(ctx.verifyItems())
                await asyncio.create_task(ctx.verifyLevel())
                message = [{"cmd": 'LocationChecks', "locations": ctx.sending}]
                if finishedGame(ctx, message):
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.finished_game = True
                location_ids = []
                location_ids = [location for location in message[0]["locations"] if location not in location_ids]
                for location in location_ids:
                    if location not in ctx.locations_checked:
                        ctx.locations_checked.add(location)
                        ctx.kh2seedsave["LocationsChecked"].append(location)
                        if location in ctx.kh2LocalItems:
                            item = ctx.kh2slotdata["LocalItems"][str(location)]
                            await asyncio.create_task(ctx.give_item(item, "LocalItems"))
                await ctx.send_msgs(message)
            elif not ctx.kh2connected and ctx.serverconneced:
                logger.info("Game is not open. Disconnecting from Server.")
                await ctx.disconnect()
        except Exception as e:
            logger.info("Line 661")
            if ctx.kh2connected:
                logger.info("Connection Lost.")
                ctx.kh2connected = False
            logger.info(e)
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
