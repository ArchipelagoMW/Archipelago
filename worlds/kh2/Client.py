import ModuleUpdate

ModuleUpdate.update()

import os
import asyncio
import json
import requests
from pymem import pymem
from . import item_dictionary_table, exclusion_item_table, CheckDupingItems, all_locations, exclusion_table, \
    SupportAbility_Table, ActionAbility_Table, all_weapon_slot
from .Names import ItemName
from .WorldLocations import *

from NetUtils import ClientStatus
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop


class KH2Context(CommonContext):
    # command_processor: int = KH2CommandProcessor
    game = "Kingdom Hearts 2"
    items_handling = 0b111  # Indicates you get items sent from other worlds.

    def __init__(self, server_address, password):
        super(KH2Context, self).__init__(server_address, password)
        self.goofy_ability_to_slot = dict()
        self.donald_ability_to_slot = dict()
        self.all_weapon_location_id = None
        self.sora_ability_to_slot = dict()
        self.kh2_seed_save = None
        self.kh2_local_items = None
        self.growthlevel = None
        self.kh2connected = False
        self.kh2_finished_game = False
        self.serverconneced = False
        self.item_name_to_data = {name: data for name, data, in item_dictionary_table.items()}
        self.location_name_to_data = {name: data for name, data, in all_locations.items()}
        self.kh2_loc_name_to_id = None
        self.kh2_item_name_to_id = None
        self.lookup_id_to_item = None
        self.lookup_id_to_location = None
        self.sora_ability_dict = {k: v.quantity for dic in [SupportAbility_Table, ActionAbility_Table] for k, v in
                                  dic.items()}
        self.location_name_to_worlddata = {name: data for name, data, in all_world_locations.items()}

        self.sending = []
        # list used to keep track of locations+items player has. Used for disoneccting
        self.kh2_seed_save_cache = {
            "itemIndex":  -1,
            # back of soras invo is 0x25E2. Growth should be moved there
            #  Character: [back of invo, front of invo]
            "SoraInvo":   [0x25D8, 0x2546],
            "DonaldInvo": [0x26F4, 0x2658],
            "GoofyInvo":  [0x2808, 0x276C],
            "AmountInvo": {
                "Ability":      {},
                "Amount":       {
                    "Bounty": 0,
                },
                "Growth":       {
                    "High Jump":    0, "Quick Run": 0, "Dodge Roll": 0,
                    "Aerial Dodge": 0, "Glide": 0
                },
                "Bitmask":      [],
                "Weapon":       {"Sora": [], "Donald": [], "Goofy": []},
                "Equipment":    [],
                "Magic":        {
                    "Fire Element":     0,
                    "Blizzard Element": 0,
                    "Thunder Element":  0,
                    "Cure Element":     0,
                    "Magnet Element":   0,
                    "Reflect Element":  0
                },
                "StatIncrease": {
                    ItemName.MaxHPUp:         0,
                    ItemName.MaxMPUp:         0,
                    ItemName.DriveGaugeUp:    0,
                    ItemName.ArmorSlotUp:     0,
                    ItemName.AccessorySlotUp: 0,
                    ItemName.ItemSlotUp:      0,
                },
            },
        }
        self.kh2seedname = None
        self.kh2slotdata = None
        self.mem_json = None
        self.itemamount = {}
        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%\KH2AP")
        self.hitlist_bounties = 0
        # hooked object
        self.kh2 = None
        self.final_xemnas = False
        self.worldid_to_locations = {
            #  1:   {},  # world of darkness (story cutscenes)
            2:  TT_Checks,
            #  3:   {},  # destiny island doesn't have checks
            4:  HB_Checks,
            5:  BC_Checks,
            6:  Oc_Checks,
            7:  AG_Checks,
            8:  LoD_Checks,
            9:  HundredAcreChecks,
            10: PL_Checks,
            11: Atlantica_Checks,
            12: DC_Checks,
            13: TR_Checks,
            14: HT_Checks,
            15: HB_Checks,  # world map, but you only go to the world map while on the way to goa so checking hb
            16: PR_Checks,
            17: SP_Checks,
            18: TWTNW_Checks,
            #  255: {},  # starting screen
        }
        self.last_world_int = -1
        # 0x2A09C00+0x40 is the sve anchor. +1 is the last saved room
        # self.sveroom = 0x2A09C00 + 0x41
        # 0 not in battle 1 in yellow battle 2 red battle #short
        # self.inBattle = 0x2A0EAC4 + 0x40
        # self.onDeath = 0xAB9078
        # PC Address anchors
        # self.Now = 0x0714DB8 old address
        # epic addresses
        self.Now = 0x0716DF8
        self.Save = 0x09A92F0
        self.Journal = 0x743260
        self.Shop = 0x743350
        self.Slot1 = 0x2A22FD8
        # self.Sys3 = 0x2A59DF0
        # self.Bt10 = 0x2A74880
        # self.BtlEnd = 0x2A0D3E0
        # self.Slot1 = 0x2A20C98 old address

        self.kh2_game_version = None  # can be egs or steam

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
            "Accessories": [0x2514, 0x2516, 0x2518, 0x251A]
        }

        self.AbilityQuantityDict = {}
        self.ability_categories = CheckDupingItems["Abilities"]

        self.sora_ability_set = set(self.ability_categories["Sora"])
        self.donald_ability_set = set(self.ability_categories["Donald"])
        self.goofy_ability_set = set(self.ability_categories["Goofy"])

        self.all_abilities = self.sora_ability_set.union(self.donald_ability_set).union(self.goofy_ability_set)

        self.stat_increase_set = set(CheckDupingItems["Stat Increases"])
        self.AbilityQuantityDict = {item: self.item_name_to_data[item].quantity for item in self.all_abilities}

        #  Growth:[level 1,level 4,slot]
        self.growth_values_dict = {
            "High Jump":    [0x05E, 0x061, 0x25DA],
            "Quick Run":    [0x62, 0x65, 0x25DC],
            "Dodge Roll":   [0x234, 0x237, 0x25DE],
            "Aerial Dodge": [0x66, 0x069, 0x25E0],
            "Glide":        [0x6A, 0x6D, 0x25E2]
        }

        self.ability_code_list = None
        self.master_growth = {"High Jump", "Quick Run", "Dodge Roll", "Aerial Dodge", "Glide"}

        self.base_hp = 20
        self.base_mp = 100
        self.base_drive = 5
        self.base_accessory_slots = 1
        self.base_armor_slots = 1
        self.base_item_slots = 3
        self.front_ability_slots = [0x2546, 0x2658, 0x276C, 0x2548, 0x254A, 0x254C, 0x265A, 0x265C, 0x265E, 0x276E,
                                    0x2770, 0x2772]

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def connection_closed(self):
        self.kh2connected = False
        self.serverconneced = False
        if self.kh2seedname is not None and self.auth is not None:
            with open(os.path.join(self.game_communication_path, f"kh2save2{self.kh2seedname}{self.auth}.json"),
                    'w') as f:
                f.write(json.dumps(self.kh2_seed_save, indent=4))
        await super(KH2Context, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.kh2connected = False
        self.serverconneced = False
        if self.kh2seedname not in {None} and self.auth not in {None}:
            with open(os.path.join(self.game_communication_path, f"kh2save2{self.kh2seedname}{self.auth}.json"),
                    'w') as f:
                f.write(json.dumps(self.kh2_seed_save, indent=4))
        await super(KH2Context, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        if self.kh2seedname not in {None} and self.auth not in {None}:
            with open(os.path.join(self.game_communication_path, f"kh2save2{self.kh2seedname}{self.auth}.json"),
                    'w') as f:
                f.write(json.dumps(self.kh2_seed_save, indent=4))
        await super(KH2Context, self).shutdown()

    def kh2_read_short(self, address):
        return self.kh2.read_short(self.kh2.base_address + address)

    def kh2_write_short(self, address, value):
        return self.kh2.write_short(self.kh2.base_address + address, value)

    def kh2_write_byte(self, address, value):
        return self.kh2.write_bytes(self.kh2.base_address + address, value.to_bytes(1, 'big'), 1)

    def kh2_read_byte(self, address):
        return int.from_bytes(self.kh2.read_bytes(self.kh2.base_address + address, 1), "big")

    def kh2_read_int(self, address):
        return self.kh2.read_int(self.kh2.base_address + address)

    def kh2_write_int(self, address, value):
        self.kh2.write_int(self.kh2.base_address + address, value)

    def kh2_read_string(self, address, length):
        return self.kh2.read_string(self.kh2.base_address + address, length)

    def on_package(self, cmd: str, args: dict):
        if cmd in {"RoomInfo"}:
            self.kh2seedname = args['seed_name']
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            if not os.path.exists(self.game_communication_path + f"\kh2save2{self.kh2seedname}{self.auth}.json"):
                self.kh2_seed_save = {
                    "Levels":        {
                        "SoraLevel":   0,
                        "ValorLevel":  0,
                        "WisdomLevel": 0,
                        "LimitLevel":  0,
                        "MasterLevel": 0,
                        "FinalLevel":  0,
                        "SummonLevel": 0,
                    },
                    "SoldEquipment": [],
                }
                with open(os.path.join(self.game_communication_path, f"kh2save2{self.kh2seedname}{self.auth}.json"),
                        'wt') as f:
                    pass
                # self.locations_checked = set()
            elif os.path.exists(self.game_communication_path + f"\kh2save2{self.kh2seedname}{self.auth}.json"):
                with open(self.game_communication_path + f"\kh2save2{self.kh2seedname}{self.auth}.json", 'r') as f:
                    self.kh2_seed_save = json.load(f)
                    if self.kh2_seed_save is None:
                        self.kh2_seed_save = {
                            "Levels":        {
                                "SoraLevel":   0,
                                "ValorLevel":  0,
                                "WisdomLevel": 0,
                                "LimitLevel":  0,
                                "MasterLevel": 0,
                                "FinalLevel":  0,
                                "SummonLevel": 0,
                            },
                            "SoldEquipment": [],
                        }
                    # self.locations_checked = set(self.kh2_seed_save_cache["LocationsChecked"])
            # self.serverconneced = True

        if cmd in {"Connected"}:
            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Kingdom Hearts 2"]}]))
            self.kh2slotdata = args['slot_data']
            # self.kh2_local_items = {int(location): item for location, item in self.kh2slotdata["LocalItems"].items()}
            self.locations_checked = set(args["checked_locations"])

        if cmd in {"ReceivedItems"}:
            # 0x2546
            # 0x2658
            # 0x276A
            start_index = args["index"]
            if start_index == 0:
                self.kh2_seed_save_cache = {
                    "itemIndex":  -1,
                    # back of soras invo is 0x25E2. Growth should be moved there
                    #  Character: [back of invo, front of invo]
                    "SoraInvo":   [0x25D8, 0x2546],
                    "DonaldInvo": [0x26F4, 0x2658],
                    "GoofyInvo":  [0x2808, 0x276C],
                    "AmountInvo": {
                        "Ability":      {},
                        "Amount":       {
                            "Bounty": 0,
                        },
                        "Growth":       {
                            "High Jump":    0, "Quick Run": 0, "Dodge Roll": 0,
                            "Aerial Dodge": 0, "Glide": 0
                        },
                        "Bitmask":      [],
                        "Weapon":       {"Sora": [], "Donald": [], "Goofy": []},
                        "Equipment":    [],
                        "Magic":        {
                            "Fire Element":     0,
                            "Blizzard Element": 0,
                            "Thunder Element":  0,
                            "Cure Element":     0,
                            "Magnet Element":   0,
                            "Reflect Element":  0
                        },
                        "StatIncrease": {
                            ItemName.MaxHPUp:         0,
                            ItemName.MaxMPUp:         0,
                            ItemName.DriveGaugeUp:    0,
                            ItemName.ArmorSlotUp:     0,
                            ItemName.AccessorySlotUp: 0,
                            ItemName.ItemSlotUp:      0,
                        },
                    },
                }
            if start_index > self.kh2_seed_save_cache["itemIndex"] and self.serverconneced:
                self.kh2_seed_save_cache["itemIndex"] = start_index
                for item in args['items']:
                    asyncio.create_task(self.give_item(item.item, item.location))

        if cmd in {"RoomUpdate"}:
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd in {"DataPackage"}:
            if "Kingdom Hearts 2" in args["data"]["games"]:
                self.data_package_kh2_cache(args)
            if "KeybladeAbilities" in self.kh2slotdata.keys():
                # sora ability to slot
                self.AbilityQuantityDict.update(self.kh2slotdata["KeybladeAbilities"])
                # itemid:[slots that are available for that item]
                self.AbilityQuantityDict.update(self.kh2slotdata["StaffAbilities"])
                self.AbilityQuantityDict.update(self.kh2slotdata["ShieldAbilities"])

            all_weapon_location_id = []
            for weapon_location in all_weapon_slot:
                all_weapon_location_id.append(self.kh2_loc_name_to_id[weapon_location])
            self.all_weapon_location_id = set(all_weapon_location_id)

            try:
                if not self.kh2:
                    self.kh2 = pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
                    self.get_addresses()

            except Exception as e:
                if self.kh2connected:
                    self.kh2connected = False
                logger.info("Game is not open.")
            self.serverconneced = True
            asyncio.create_task(self.send_msgs([{'cmd': 'Sync'}]))

    def data_package_kh2_cache(self, args):
        self.kh2_loc_name_to_id = args["data"]["games"]["Kingdom Hearts 2"]["location_name_to_id"]
        self.lookup_id_to_location = {v: k for k, v in self.kh2_loc_name_to_id.items()}
        self.kh2_item_name_to_id = args["data"]["games"]["Kingdom Hearts 2"]["item_name_to_id"]
        self.lookup_id_to_item = {v: k for k, v in self.kh2_item_name_to_id.items()}
        self.ability_code_list = [self.kh2_item_name_to_id[item] for item in exclusion_item_table["Ability"]]

    async def checkWorldLocations(self):
        try:
            currentworldint = self.kh2_read_byte(self.Now)
            if self.last_world_int != currentworldint:
                self.last_world_int = currentworldint
                await self.send_msgs([{
                    "cmd":     "Set", "key": "Slot: " + str(self.slot) + " :CurrentWorld",
                    "default": 0, "want_reply": False, "operations": [{
                        "operation": "replace",
                        "value":     currentworldint
                    }]
                }])
            if currentworldint in self.worldid_to_locations:
                curworldid = self.worldid_to_locations[currentworldint]
                for location, data in curworldid.items():
                    if location in self.kh2_loc_name_to_id.keys():
                        locationId = self.kh2_loc_name_to_id[location]
                        if locationId not in self.locations_checked \
                                and self.kh2_read_byte(self.Save + data.addrObtained) & 0x1 << data.bitIndex > 0:
                            self.sending = self.sending + [(int(locationId))]
        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info(e)
            logger.info("line 425")

    async def checkLevels(self):
        try:
            for location, data in SoraLevels.items():
                currentLevel = self.kh2_read_byte(self.Save + 0x24FF)
                locationId = self.kh2_loc_name_to_id[location]
                if locationId not in self.locations_checked \
                        and currentLevel >= data.bitIndex:
                    if self.kh2_seed_save["Levels"]["SoraLevel"] < currentLevel:
                        self.kh2_seed_save["Levels"]["SoraLevel"] = currentLevel
                    self.sending = self.sending + [(int(locationId))]
            formDict = {
                0: ["ValorLevel", ValorLevels], 1: ["WisdomLevel", WisdomLevels], 2: ["LimitLevel", LimitLevels],
                3: ["MasterLevel", MasterLevels], 4: ["FinalLevel", FinalLevels], 5: ["SummonLevel", SummonLevels]
            }
            for i in range(6):
                for location, data in formDict[i][1].items():
                    formlevel = self.kh2_read_byte(self.Save + data.addrObtained)
                    if location in self.kh2_loc_name_to_id.keys():
                        # if current form level is above other form level
                        locationId = self.kh2_loc_name_to_id[location]
                        if locationId not in self.locations_checked \
                                and formlevel >= data.bitIndex:
                            if formlevel > self.kh2_seed_save["Levels"][formDict[i][0]]:
                                self.kh2_seed_save["Levels"][formDict[i][0]] = formlevel
                            self.sending = self.sending + [(int(locationId))]
        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info(e)
            logger.info("line 456")

    async def checkSlots(self):
        try:
            for location, data in weaponSlots.items():
                locationId = self.kh2_loc_name_to_id[location]
                if locationId not in self.locations_checked:
                    if self.kh2_read_byte(self.Save + data.addrObtained) > 0:
                        self.sending = self.sending + [(int(locationId))]

            for location, data in formSlots.items():
                locationId = self.kh2_loc_name_to_id[location]
                if locationId not in self.locations_checked and self.kh2_read_byte(self.Save + 0x06B2) == 0:
                    if self.kh2_read_byte(self.Save + data.addrObtained) & 0x1 << data.bitIndex > 0:
                        self.sending = self.sending + [(int(locationId))]
        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info(e)
            logger.info("line 475")

    async def verifyChests(self):
        try:
            for location in self.locations_checked:
                locationName = self.lookup_id_to_location[location]
                if locationName in self.chest_set:
                    if locationName in self.location_name_to_worlddata.keys():
                        locationData = self.location_name_to_worlddata[locationName]
                        if self.kh2_read_byte(
                                self.Save + locationData.addrObtained) & 0x1 << locationData.bitIndex == 0:
                            roomData = self.kh2_read_byte(self.Save + locationData.addrObtained)
                            self.kh2_write_byte(self.Save + locationData.addrObtained,
                                                roomData | 0x01 << locationData.bitIndex)

        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info(e)
            logger.info("line 491")

    async def verifyLevel(self):
        for leveltype, anchor in {
            "SoraLevel":   0x24FF,
            "ValorLevel":  0x32F6,
            "WisdomLevel": 0x332E,
            "LimitLevel":  0x3366,
            "MasterLevel": 0x339E,
            "FinalLevel":  0x33D6
        }.items():
            if self.kh2_read_byte(self.Save + anchor) < self.kh2_seed_save["Levels"][leveltype]:
                self.kh2_write_byte(self.Save + anchor, self.kh2_seed_save["Levels"][leveltype])

    async def give_item(self, item, location):
        try:
            # todo: ripout all the itemtype stuff and just have one dictionary. the only thing that needs to be tracked from the server/local is abilites
            #sleep so we can get the datapackage and not miss any items that were sent to us while we didnt have our item id dicts
            while not self.lookup_id_to_item:
                await asyncio.sleep(0.5)
            itemname = self.lookup_id_to_item[item]
            itemdata = self.item_name_to_data[itemname]
            # itemcode = self.kh2_item_name_to_id[itemname]
            if itemdata.ability:
                if location in self.all_weapon_location_id:
                    return
                if itemname in {"High Jump", "Quick Run", "Dodge Roll", "Aerial Dodge", "Glide"}:
                    self.kh2_seed_save_cache["AmountInvo"]["Growth"][itemname] += 1
                    return

                if itemname not in self.kh2_seed_save_cache["AmountInvo"]["Ability"]:
                    self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname] = []
                    #  appending the slot that the ability should be in
                if len(self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname]) < \
                        self.AbilityQuantityDict[itemname]:
                    if itemname in self.sora_ability_set:
                        ability_slot = self.kh2_seed_save_cache["SoraInvo"][0]
                        self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname].append(ability_slot)
                        self.kh2_seed_save_cache["SoraInvo"][0] -= 2
                    elif itemname in self.donald_ability_set:
                        ability_slot = self.kh2_seed_save_cache["DonaldInvo"][0]
                        self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname].append(ability_slot)
                        self.kh2_seed_save_cache["DonaldInvo"][0] -= 2
                    else:
                        ability_slot = self.kh2_seed_save_cache["GoofyInvo"][0]
                        self.kh2_seed_save_cache["AmountInvo"]["Ability"][itemname].append(ability_slot)
                        self.kh2_seed_save_cache["GoofyInvo"][0] -= 2

                    if ability_slot in self.front_ability_slots:
                        self.front_ability_slots.remove(ability_slot)

            elif itemdata.memaddr in {0x36C4, 0x36C5, 0x36C6, 0x36C0, 0x36CA}:
                # if memaddr is in a bitmask location in memory
                if itemname not in self.kh2_seed_save_cache["AmountInvo"]["Bitmask"]:
                    self.kh2_seed_save_cache["AmountInvo"]["Bitmask"].append(itemname)

            elif itemdata.memaddr in {0x3594, 0x3595, 0x3596, 0x3597, 0x35CF, 0x35D0}:
                # if memaddr is in magic addresses
                self.kh2_seed_save_cache["AmountInvo"]["Magic"][itemname] += 1

            elif itemname in self.all_equipment:
                self.kh2_seed_save_cache["AmountInvo"]["Equipment"].append(itemname)

            elif itemname in self.all_weapons:
                if itemname in self.keyblade_set:
                    self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Sora"].append(itemname)
                elif itemname in self.staff_set:
                    self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Donald"].append(itemname)
                else:
                    self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Goofy"].append(itemname)

            elif itemname in self.stat_increase_set:
                self.kh2_seed_save_cache["AmountInvo"]["StatIncrease"][itemname] += 1
            else:
                if itemname in self.kh2_seed_save_cache["AmountInvo"]["Amount"]:
                    self.kh2_seed_save_cache["AmountInvo"]["Amount"][itemname] += 1
                else:
                    self.kh2_seed_save_cache["AmountInvo"]["Amount"][itemname] = 1

        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info(e)
            logger.info("line 582")

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

    async def IsInShop(self, sellable):
        # journal = 0x741230 shop = 0x741320
        # if journal=-1 and shop = 5 then in shop
        # if journal !=-1 and shop = 10 then journal

        journal = self.kh2_read_short(self.Journal)
        shop = self.kh2_read_short(self.Shop)
        if (journal == -1 and shop == 5) or (journal != -1 and shop == 10):
            # print("your in the shop")
            sellable_dict = {}
            for itemName in sellable:
                itemdata = self.item_name_to_data[itemName]
                amount = self.kh2_read_byte(self.Save + itemdata.memaddr)
                sellable_dict[itemName] = amount
            while (journal == -1 and shop == 5) or (journal != -1 and shop == 10):
                journal = self.kh2_read_short(self.Journal)
                shop = self.kh2_read_short(self.Shop)
                await asyncio.sleep(0.5)
            for item, amount in sellable_dict.items():
                itemdata = self.item_name_to_data[item]
                afterShop = self.kh2_read_byte(self.Save + itemdata.memaddr)
                if afterShop < amount:
                    self.kh2_seed_save["SoldEquipment"].append(item)

    async def verifyItems(self):
        try:
            master_amount = set(self.kh2_seed_save_cache["AmountInvo"]["Amount"].keys())

            master_ability = set(self.kh2_seed_save_cache["AmountInvo"]["Ability"].keys())

            master_bitmask = set(self.kh2_seed_save_cache["AmountInvo"]["Bitmask"])

            master_keyblade = set(self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Sora"])
            master_staff = set(self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Donald"])
            master_shield = set(self.kh2_seed_save_cache["AmountInvo"]["Weapon"]["Goofy"])

            master_equipment = set(self.kh2_seed_save_cache["AmountInvo"]["Equipment"])

            master_magic = set(self.kh2_seed_save_cache["AmountInvo"]["Magic"].keys())

            master_stat = set(self.kh2_seed_save_cache["AmountInvo"]["StatIncrease"].keys())

            master_sell = master_equipment | master_staff | master_shield

            await asyncio.create_task(self.IsInShop(master_sell))
            # print(self.kh2_seed_save_cache["AmountInvo"]["Ability"])
            for item_name in master_amount:
                item_data = self.item_name_to_data[item_name]
                amount_of_items = 0
                amount_of_items += self.kh2_seed_save_cache["AmountInvo"]["Amount"][item_name]

                if item_name == "Torn Page":
                    # Torn Pages are handled differently because they can be consumed.
                    # Will check the progression in 100 acre and - the amount of visits
                    # amountofitems-amount of visits done
                    for location, data in tornPageLocks.items():
                        if self.kh2_read_byte(self.Save + data.addrObtained) & 0x1 << data.bitIndex > 0:
                            amount_of_items -= 1
                if self.kh2_read_byte(self.Save + item_data.memaddr) != amount_of_items and amount_of_items >= 0:
                    self.kh2_write_byte(self.Save + item_data.memaddr, amount_of_items)

            for item_name in master_keyblade:
                item_data = self.item_name_to_data[item_name]
                # if the inventory slot for that keyblade is less than the amount they should have,
                # and they are not in stt
                if self.kh2_read_byte(self.Save + item_data.memaddr) != 1 and self.kh2_read_byte(
                        self.Save + 0x1CFF) != 13:
                    # Checking form anchors for the keyblade to remove extra keyblades
                    if self.kh2_read_short(self.Save + 0x24F0) == item_data.kh2id \
                            or self.kh2_read_short(self.Save + 0x32F4) == item_data.kh2id \
                            or self.kh2_read_short(self.Save + 0x339C) == item_data.kh2id \
                            or self.kh2_read_short(self.Save + 0x33D4) == item_data.kh2id:
                        self.kh2_write_byte(self.Save + item_data.memaddr, 0)
                    else:
                        self.kh2_write_byte(self.Save + item_data.memaddr, 1)

            for item_name in master_staff:
                item_data = self.item_name_to_data[item_name]
                if self.kh2_read_byte(self.Save + item_data.memaddr) != 1 \
                        and self.kh2_read_short(self.Save + 0x2604) != item_data.kh2id \
                        and item_name not in self.kh2_seed_save["SoldEquipment"]:
                    self.kh2_write_byte(self.Save + item_data.memaddr, 1)

            for item_name in master_shield:
                item_data = self.item_name_to_data[item_name]
                if self.kh2_read_byte(self.Save + item_data.memaddr) != 1 \
                        and self.kh2_read_short(self.Save + 0x2718) != item_data.kh2id \
                        and item_name not in self.kh2_seed_save["SoldEquipment"]:
                    self.kh2_write_byte(self.Save + item_data.memaddr, 1)

            for item_name in master_ability:
                item_data = self.item_name_to_data[item_name]
                ability_slot = []
                ability_slot += self.kh2_seed_save_cache["AmountInvo"]["Ability"][item_name]
                for slot in ability_slot:
                    current = self.kh2_read_short(self.Save + slot)
                    ability = current & 0x0FFF
                    if ability | 0x8000 != (0x8000 + item_data.memaddr):
                        if current - 0x8000 > 0:
                            self.kh2_write_short(self.Save + slot, 0x8000 + item_data.memaddr)
                        else:
                            self.kh2_write_short(self.Save + slot, item_data.memaddr)
            # removes the duped ability if client gave faster than the game.

            for ability in self.front_ability_slots:
                if self.kh2_read_short(self.Save + ability) != 0:
                    print(f"removed {self.Save + ability} from {ability}")
                    self.kh2_write_short(self.Save + ability, 0)

            # remove the dummy level 1 growths if they are in these invo slots.
            for inventorySlot in {0x25CE, 0x25D0, 0x25D2, 0x25D4, 0x25D6, 0x25D8}:
                current = self.kh2_read_short(self.Save + inventorySlot)
                ability = current & 0x0FFF
                if 0x05E <= ability <= 0x06D:
                    self.kh2_write_short(self.Save + inventorySlot, 0)

            for item_name in self.master_growth:
                growthLevel = self.kh2_seed_save_cache["AmountInvo"]["Growth"][item_name]
                if growthLevel > 0:
                    slot = self.growth_values_dict[item_name][2]
                    min_growth = self.growth_values_dict[item_name][0]
                    max_growth = self.growth_values_dict[item_name][1]
                    if growthLevel > 4:
                        growthLevel = 4
                    current_growth_level = self.kh2_read_short(self.Save + slot)
                    ability = current_growth_level & 0x0FFF

                    # if the player should be getting a growth ability
                    if ability | 0x8000 != 0x8000 + min_growth - 1 + growthLevel:
                        # if it should be level one of that growth
                        if 0x8000 + min_growth - 1 + growthLevel <= 0x8000 + min_growth or ability < min_growth:
                            self.kh2_write_short(self.Save + slot, min_growth)
                        # if it is already in the inventory
                        elif ability | 0x8000 < (0x8000 + max_growth):
                            self.kh2_write_short(self.Save + slot, current_growth_level + 1)

            for item_name in master_bitmask:
                item_data = self.item_name_to_data[item_name]
                itemMemory = self.kh2_read_byte(self.Save + item_data.memaddr)
                if self.kh2_read_byte(self.Save + item_data.memaddr) & 0x1 << item_data.bitmask == 0:
                    # when getting a form anti points should be reset to 0 but bit-shift doesn't trigger the game.
                    if item_name in {"Valor Form", "Wisdom Form", "Limit Form", "Master Form", "Final Form"}:
                        self.kh2_write_byte(self.Save + 0x3410, 0)
                    self.kh2_write_byte(self.Save + item_data.memaddr, itemMemory | 0x01 << item_data.bitmask)

            for item_name in master_equipment:
                item_data = self.item_name_to_data[item_name]
                is_there = False
                if item_name in self.accessories_set:
                    Equipment_Anchor_List = self.Equipment_Anchor_Dict["Accessories"]
                else:
                    Equipment_Anchor_List = self.Equipment_Anchor_Dict["Armor"]
                    # Checking form anchors for the equipment
                for slot in Equipment_Anchor_List:
                    if self.kh2_read_short(self.Save + slot) == item_data.kh2id:
                        is_there = True
                        if self.kh2_read_byte(self.Save + item_data.memaddr) != 0:
                            self.kh2_write_byte(self.Save + item_data.memaddr, 0)
                        break
                if not is_there and item_name not in self.kh2_seed_save["SoldEquipment"]:
                    if self.kh2_read_byte(self.Save + item_data.memaddr) != 1:
                        self.kh2_write_byte(self.Save + item_data.memaddr, 1)

            for item_name in master_magic:
                item_data = self.item_name_to_data[item_name]
                amount_of_items = 0
                amount_of_items += self.kh2_seed_save_cache["AmountInvo"]["Magic"][item_name]
                if self.kh2_read_byte(self.Save + item_data.memaddr) != amount_of_items and self.kh2_read_byte(
                        self.Shop) in {10, 8}:
                    self.kh2_write_byte(self.Save + item_data.memaddr, amount_of_items)

            for item_name in master_stat:
                amount_of_items = 0
                amount_of_items += self.kh2_seed_save_cache["AmountInvo"]["StatIncrease"][item_name]
                if self.kh2_read_byte(self.Slot1 + 0x1B2) >= 5:
                    if item_name == ItemName.MaxHPUp:
                        if self.kh2_read_byte(self.Save + 0x2498) < 3:  # Non-Critical
                            Bonus = 5
                        else:  # Critical
                            Bonus = 2
                        if self.kh2_read_int(self.Slot1 + 0x004) != self.base_hp + (Bonus * amount_of_items):
                            self.kh2_write_int(self.Slot1 + 0x004, self.base_hp + (Bonus * amount_of_items))

                    elif item_name == ItemName.MaxMPUp:
                        if self.kh2_read_byte(self.Save + 0x2498) < 3:  # Non-Critical
                            Bonus = 10
                        else:  # Critical
                            Bonus = 5
                        if self.kh2_read_int(self.Slot1 + 0x184) != self.base_mp + (Bonus * amount_of_items):
                            self.kh2_write_int(self.Slot1 + 0x184, self.base_mp + (Bonus * amount_of_items))

                    elif item_name == ItemName.DriveGaugeUp:
                        current_max_drive = self.kh2_read_byte(self.Slot1 + 0x1B2)
                        # change when max drive is changed from 6 to 4
                        if current_max_drive < 9 and current_max_drive != self.base_drive + amount_of_items:
                            self.kh2_write_byte(self.Slot1 + 0x1B2, self.base_drive + amount_of_items)

                    elif item_name == ItemName.AccessorySlotUp:
                        current_accessory = self.kh2_read_byte(self.Save + 0x2501)
                        if current_accessory != self.base_accessory_slots + amount_of_items:
                            if 4 > current_accessory < self.base_accessory_slots + amount_of_items:
                                self.kh2_write_byte(self.Save + 0x2501, current_accessory + 1)
                            elif self.base_accessory_slots + amount_of_items < 4:
                                self.kh2_write_byte(self.Save + 0x2501, self.base_accessory_slots + amount_of_items)

                    elif item_name == ItemName.ArmorSlotUp:
                        current_armor_slots = self.kh2_read_byte(self.Save + 0x2500)
                        if current_armor_slots != self.base_armor_slots + amount_of_items:
                            if 4 > current_armor_slots < self.base_armor_slots + amount_of_items:
                                self.kh2_write_byte(self.Save + 0x2500, current_armor_slots + 1)
                            elif self.base_armor_slots + amount_of_items < 4:
                                self.kh2_write_byte(self.Save + 0x2500, self.base_armor_slots + amount_of_items)

                    elif item_name == ItemName.ItemSlotUp:
                        current_item_slots = self.kh2_read_byte(self.Save + 0x2502)
                        if current_item_slots != self.base_item_slots + amount_of_items:
                            if 8 > current_item_slots < self.base_item_slots + amount_of_items:
                                self.kh2_write_byte(self.Save + 0x2502, current_item_slots + 1)
                            elif self.base_item_slots + amount_of_items < 8:
                                self.kh2_write_byte(self.Save + 0x2502, self.base_item_slots + amount_of_items)

                # if self.kh2_read_byte(self.Save + item_data.memaddr) != amount_of_items \
                #        and self.kh2_read_byte(self.Slot1 + 0x1B2) >= 5 and \
                #        self.kh2_read_byte(self.Save + 0x23DF) & 0x1 << 3 > 0 and self.kh2_read_byte(0x741320) in {10, 8}:
                #    self.kh2_write_byte(self.Save + item_data.memaddr, amount_of_items)

            if "PoptrackerVersionCheck" in self.kh2slotdata:
                if self.kh2slotdata["PoptrackerVersionCheck"] > 4.2 and self.kh2_read_byte(
                        self.Save + 0x3607) != 1:  # telling the goa they are on version 4.3
                    self.kh2_write_byte(self.Save + 0x3607, 1)

        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info(e)
            logger.info("line 840")

    def get_addresses(self):
        if not self.kh2connected and self.kh2 is not None:
            if self.kh2_game_version is None:

                if self.kh2_read_string(0x09A9830, 4) == "KH2J":
                    self.kh2_game_version = "STEAM"
                    self.Now = 0x0717008
                    self.Save = 0x09A9830
                    self.Slot1 = 0x2A23518
                    self.Journal = 0x7434E0
                    self.Shop = 0x7435D0
                elif self.kh2_read_string(0x09A92F0, 4) == "KH2J":
                    self.kh2_game_version = "EGS"
                else:
                    if self.game_communication_path:
                        logger.info("Checking with most up to date addresses of github. If file is not found will be downloading datafiles. This might take a moment")
                        #if mem addresses file is found then check version and if old get new one
                        kh2memaddresses_path = os.path.join(self.game_communication_path, f"kh2memaddresses.json")
                        if not os.path.exists(kh2memaddresses_path):
                            mem_resp = requests.get("https://raw.githubusercontent.com/JaredWeakStrike/KH2APMemoryValues/master/kh2memaddresses.json")
                            if mem_resp.status_code == 200:
                                self.mem_json = json.loads(mem_resp.content)
                                with open(kh2memaddresses_path,
                                        'w') as f:
                                    f.write(json.dumps(self.mem_json, indent=4))
                        else:
                            with open(kh2memaddresses_path, 'r') as f:
                                self.mem_json = json.load(f)
                        if self.mem_json:
                            for key in self.mem_json.keys():

                                if self.kh2_read_string(eval(self.mem_json[key]["GameVersionCheck"]), 4) == "KH2J":
                                    self.Now = eval(self.mem_json[key]["Now"])
                                    self.Save=eval(self.mem_json[key]["Save"])
                                    self.Slot1 = eval(self.mem_json[key]["Slot1"])
                                    self.Journal = eval(self.mem_json[key]["Journal"])
                                    self.Shop = eval(self.mem_json[key]["Shop"])
                                    self.kh2_game_version = key

            if self.kh2_game_version is not None:
                logger.info(f"You are now auto-tracking {self.kh2_game_version}")
                self.kh2connected = True
            else:
                logger.info("Your game version does not match what the client requires. Check in the "
                            "kingdom-hearts-2-final-mix channel for more information on correcting the game "
                            "version.")
                self.kh2connected = False


def finishedGame(ctx: KH2Context):
    if ctx.kh2slotdata['FinalXemnas'] == 1:
        if not ctx.final_xemnas and ctx.kh2_read_byte(
                ctx.Save + all_world_locations[LocationName.FinalXemnas].addrObtained) \
                & 0x1 << all_world_locations[LocationName.FinalXemnas].bitIndex > 0:
            ctx.final_xemnas = True
    # three proofs
    if ctx.kh2slotdata['Goal'] == 0:
        if ctx.kh2_read_byte(ctx.Save + 0x36B2) > 0 \
                and ctx.kh2_read_byte(ctx.Save + 0x36B3) > 0 \
                and ctx.kh2_read_byte(ctx.Save + 0x36B4) > 0:
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False
    elif ctx.kh2slotdata['Goal'] == 1:
        if ctx.kh2_read_byte(ctx.Save + 0x3641) >= ctx.kh2slotdata['LuckyEmblemsRequired']:
            if ctx.kh2_read_byte(ctx.Save + 0x36B3) < 1:
                ctx.kh2_write_byte(ctx.Save + 0x36B2, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B3, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B4, 1)
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False
    elif ctx.kh2slotdata['Goal'] == 2:
        # for backwards compat
        if "hitlist" in ctx.kh2slotdata:
            locations = ctx.sending
            for boss in ctx.kh2slotdata["hitlist"]:
                if boss in locations:
                    ctx.hitlist_bounties += 1
        if ctx.hitlist_bounties >= ctx.kh2slotdata["BountyRequired"] or ctx.kh2_seed_save_cache["AmountInvo"]["Amount"][
            "Bounty"] >= ctx.kh2slotdata["BountyRequired"]:
            if ctx.kh2_read_byte(ctx.Save + 0x36B3) < 1:
                ctx.kh2_write_byte(ctx.Save + 0x36B2, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B3, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B4, 1)
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
        return False
    elif ctx.kh2slotdata["Goal"] == 3:
        if ctx.kh2_seed_save_cache["AmountInvo"]["Amount"]["Bounty"] >= ctx.kh2slotdata["BountyRequired"] and \
                ctx.kh2_read_byte(ctx.Save + 0x3641) >= ctx.kh2slotdata['LuckyEmblemsRequired']:
            if ctx.kh2_read_byte(ctx.Save + 0x36B3) < 1:
                ctx.kh2_write_byte(ctx.Save + 0x36B2, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B3, 1)
                ctx.kh2_write_byte(ctx.Save + 0x36B4, 1)
                logger.info("The Final Door is now Open")
            if ctx.kh2slotdata['FinalXemnas'] == 1:
                if ctx.final_xemnas:
                    return True
                return False
            return True
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
                if finishedGame(ctx) and not ctx.kh2_finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.kh2_finished_game = True
                if ctx.sending:
                    message = [{"cmd": 'LocationChecks', "locations": ctx.sending}]
                    await ctx.send_msgs(message)
            elif not ctx.kh2connected and ctx.serverconneced:
                logger.info("Game Connection lost. waiting 15 seconds until trying to reconnect.")
                ctx.kh2 = None
                while not ctx.kh2connected and ctx.serverconneced:
                    await asyncio.sleep(15)
                    ctx.kh2 = pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
                    ctx.get_addresses()
        except Exception as e:
            if ctx.kh2connected:
                ctx.kh2connected = False
            logger.info(e)
            logger.info("line 940")
        await asyncio.sleep(0.5)


def launch():
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
