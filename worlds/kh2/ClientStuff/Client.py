from __future__ import annotations
import ModuleUpdate
import Utils

ModuleUpdate.update()
import os
import asyncio
import json
import requests

from pymem import pymem
from worlds.kh2 import item_dictionary_table, exclusion_item_table, CheckDupingItems, all_locations, exclusion_table, \
    SupportAbility_Table, ActionAbility_Table, all_weapon_slot
from worlds.kh2.Names import ItemName
from .WorldLocations import *

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop
from .CMDProcessor import KH2CommandProcessor
from .SendChecks import finishedGame


class KH2Context(CommonContext):
    command_processor = KH2CommandProcessor
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
        self.serverconnected = False
        self.item_name_to_data = {name: data for name, data, in item_dictionary_table.items()}
        self.location_name_to_data = {name: data for name, data, in all_locations.items()}
        self.kh2_data_package = {}
        self.kh2_loc_name_to_id = None
        self.kh2_item_name_to_id = None
        self.lookup_id_to_item = None
        self.lookup_id_to_location = None
        self.sora_ability_dict = {k: v.quantity for dic in [SupportAbility_Table, ActionAbility_Table] for k, v in
                                  dic.items()}
        self.location_name_to_worlddata = {name: data for name, data, in all_world_locations.items()}

        self.slot_name = None
        self.disconnect_from_server = False
        self.sending = []
        # queue for the strings to display on the screen
        self.queued_puzzle_popup = []
        self.queued_info_popup = []
        self.queued_chest_popup = []

        # special characters for printing in game
        # A dictionary of all the special characters, which
        # are hard to convert through a mathematical formula.
        self.special_dict = {
            ' ': 0x01, '\n': 0x02, '-': 0x54, '!': 0x48, '?': 0x49, '%': 0x4A, '/': 0x4B,
            '.': 0x4F, ',': 0x50, ';': 0x51, ':': 0x52, '\'': 0x57, '(': 0x5A, ')': 0x5B,
            '[': 0x62, ']': 0x63, 'à': 0xB7, 'á': 0xB8, 'â': 0xB9, 'ä': 0xBA, 'è': 0xBB,
            'é': 0xBC, 'ê': 0xBD, 'ë': 0xBE, 'ì': 0xBF, 'í': 0xC0, 'î': 0xC1, 'ï': 0xC2,
            'ñ': 0xC3, 'ò': 0xC4, 'ó': 0xC5, 'ô': 0xC6, 'ö': 0xC7, 'ù': 0xC8, 'ú': 0xC9,
            'û': 0xCA, 'ü': 0xCB, 'ç': 0xE8, 'À': 0xD0, 'Á': 0xD1, 'Â': 0xD2, 'Ä': 0xD3,
            'È': 0xD4, 'É': 0xD5, 'Ê': 0xD6, 'Ë': 0xD7, 'Ì': 0xD8, 'Í': 0xD9, 'Î': 0xDA,
            'Ï': 0xDB, 'Ñ': 0xDC, 'Ò': 0xDD, 'Ó': 0xDE, 'Ô': 0xDF, 'Ö': 0xE0, 'Ù': 0xE1,
            'Ú': 0xE2, 'Û': 0xE3, 'Ü': 0xE4, '¡': 0xE5, '¿': 0xE6, 'Ç': 0xE7
        }

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
                "Equipment":    {},  # ItemName: Amount
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
        self.kh2_seed_save_path_join = None

        self.kh2slotdata = None
        self.mem_json = None
        self.itemamount = {}
        self.client_settings = {
            "send_truncate_first":    "playername",  # there is no need to truncate item names for info popup
            "receive_truncate_first": "playername",  # truncation order. Can be PlayerName or ItemName
            "send_popup_type":        "chest",  # type of popup when you receive an item
            "receive_popup_type":     "chest",  # can be Puzzle, Info, Chest or None
        }

        if "localappdata" in os.environ:
            self.game_communication_path = os.path.expandvars(r"%localappdata%\KH2AP")
            self.kh2_client_settings = f"kh2_client_settings.json"
            self.kh2_client_settings_join = os.path.join(self.game_communication_path, self.kh2_client_settings)
            if not os.path.exists(self.game_communication_path):
                os.makedirs(self.game_communication_path)
            if not os.path.exists(self.kh2_client_settings_join):
                # make the json with the settings
                with open(self.kh2_client_settings_join, "wt") as f:
                    f.close()
            elif os.path.exists(self.kh2_client_settings_join):
                with open(self.kh2_client_settings_join) as f:
                    # if the file isnt empty load it
                    # this is the best I could fine to valid json stuff https://stackoverflow.com/questions/23344948/validate-and-format-json-files
                    try:
                        self.kh2_seed_save = json.load(f)
                    except json.decoder.JSONDecodeError:
                        pass
                        # this is what is effectively doing on
                        # self.client_settings = default
                    f.close()

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
        #Sora,Donald and Goofy are always in your party
        self.WorldIDtoParty = {
            4:  "Beast",
            6:  "Auron",
            7:  "Aladdin",
            8:  "Mulan",
            10: "Simba",
            14: "Jack Skellington",
            16: "Jack Sparrow",
            17: "Tron",
            18: "Riku"
        }
        self.last_world_int = -1
        # PC Address anchors
        # epic .10 addresses
        self.Now = 0x0716DF8
        self.Save = 0x9A9330
        self.Journal = 0x743260
        self.Shop = 0x743350
        self.Slot1 = 0x2A23018
        self.InfoBarPointer = 0xABE2A8
        self.isDead = 0x0BEEF28

        self.FadeStatus = 0xABAF38
        self.PlayerGaugePointer = 0x0ABCCC8

        self.kh2_game_version = None  # can be egs or steam

        self.kh2_seed_save_path = None

        self.chest_set = set(exclusion_table["Chests"])
        self.keyblade_set = set(CheckDupingItems["Weapons"]["Keyblades"])
        self.staff_set = set(CheckDupingItems["Weapons"]["Staffs"])
        self.shield_set = set(CheckDupingItems["Weapons"]["Shields"])

        self.all_weapons = self.keyblade_set.union(self.staff_set).union(self.shield_set)

        self.equipment_categories = CheckDupingItems["Equipment"]
        self.armor_set = set(self.equipment_categories["Armor"])
        self.accessories_set = set(self.equipment_categories["Accessories"])
        self.all_equipment = self.armor_set.union(self.accessories_set)
        self.CharacterAnchors = {
            "Sora":             0x24F0,
            "Donald":           0x2604,
            "Goofy":            0x2718,
            "Auron":            0x2940,
            "Mulan":            0x2A54,
            "Aladdin":          0x2B68,
            "Jack Sparrow":     0x2C7C,
            "Beast":            0x2D90,
            "Jack Skellington": 0x2EA4,
            "Simba":            0x2FB8,
            "Tron":             0x30CC,
            "Riku":             0x31E0
        }
        self.Equipment_Anchor_Dict = {
            #Sora, Donald, Goofy in that order
            # each slot is a short, Sora Anchor:0x24F0, Donald Anchor: 0x2604, Goofy Anchor: 0x2718
            # Each of these has 8 slots that could have them no matter how many slots are unlocked
            # If Ability Ring on slot 5 of sora
            # ReadShort(Save+CharacterAnchors["Sora"]+Equiptment_Anchor["Accessories][4 (index 5)]) == self.item_name_to_data[item_name].memaddr
            "Armor":       [0x14, 0x16, 0x18, 0x1A, 0x1C, 0x1E, 0x20, 0x22],

            "Accessories": [0x24, 0x26, 0x28, 0x2A, 0x2C, 0x2E, 0x30, 0x32]
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

        self.deathlink_toggle = False
        self.deathlink_blacklist = []

    from .ReadAndWrite import kh2_read_longlong, kh2_read_int, kh2_read_string, kh2_read_byte, kh2_write_bytes, kh2_write_int, kh2_write_short, kh2_write_byte, kh2_read_short, kh2_return_base_address
    from .SendChecks import checkWorldLocations, checkSlots, checkLevels, verifyChests, verifyLevel
    from .RecieveItems import displayPuzzlePieceTextinGame, displayInfoTextinGame, displayChestTextInGame, verifyItems, give_item, IsInShop, to_khscii

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(KH2Context, self).server_auth(password_requested)
        await self.get_username()
        # if slot name != first time login or previous name
        # and seed name is none or saved seed name
        if not self.slot_name and not self.kh2seedname:
            await self.send_connect()
        elif self.slot_name == self.auth and self.kh2seedname:
            await self.send_connect()
        else:
            logger.info(f"You are trying to connect with data still cached in the client. Close client or connect to the correct slot: {self.slot_name}")
            self.serverconnected = False
            self.disconnect_from_server = True

    # to not softlock the client when you connect to the wrong slot/game
    def event_invalid_slot(self):
        self.kh2seedname = None
        CommonContext.event_invalid_slot(self)

    def event_invalid_game(self):
        self.kh2seedname = None
        CommonContext.event_invalid_slot(self)

    async def connection_closed(self):
        self.kh2connected = False
        self.serverconnected = False
        if self.kh2seedname is not None and self.auth is not None:
            with open(self.kh2_seed_save_path_join, 'w') as f:
                f.write(json.dumps(self.kh2_seed_save, indent=4))
                f.close()
        await super(KH2Context, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.kh2connected = False
        self.serverconnected = False
        self.locations_checked = []
        if self.kh2seedname not in {None} and self.auth not in {None}:
            with open(self.kh2_seed_save_path_join, 'w') as f:
                f.write(json.dumps(self.kh2_seed_save, indent=4))
                f.close()
        await super(KH2Context, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        if self.kh2seedname not in {None} and self.auth not in {None}:
            with open(self.kh2_seed_save_path_join, 'w') as f:
                f.write(json.dumps(self.kh2_seed_save, indent=4))
                f.close()
        with open(self.kh2_client_settings_join, 'w') as f2:
            f2.write(json.dumps(self.client_settings, indent=4))
            f2.close()
        await super(KH2Context, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd == "RoomInfo":
            if not self.kh2seedname:
                self.kh2seedname = args['seed_name']
            elif self.kh2seedname != args['seed_name']:
                self.disconnect_from_server = True
                self.serverconnected = False
                self.kh2connected = False
                logger.info("Connection to the wrong seed, connect to the correct seed or close the client.")
                return
            self.kh2_seed_save_path = f"kh2save2{self.kh2seedname}{self.auth}.json"
            self.kh2_seed_save_path_join = os.path.join(self.game_communication_path, Utils.get_file_safe_name(self.kh2_seed_save_path))

            if not os.path.exists(self.kh2_seed_save_path_join):
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
                    # Item: Amount of them sold
                    "SoldEquipment": dict(),
                }
                with open(self.kh2_seed_save_path_join, 'wt') as f:
                    f.close()
            elif os.path.exists(self.kh2_seed_save_path_join):
                with open(self.kh2_seed_save_path_join) as f:
                    try:
                        self.kh2_seed_save = json.load(f)
                    except json.decoder.JSONDecodeError:
                        self.kh2_seed_save = None
                    if self.kh2_seed_save is None or self.kh2_seed_save == {}:
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
                            # Item: Amount of them sold
                            "SoldEquipment": dict(),
                        }
                    f.close()

        if cmd == "Connected":
            self.kh2slotdata = args['slot_data']

            self.kh2_data_package = Utils.load_data_package_for_checksum(
                    "Kingdom Hearts 2", self.checksums["Kingdom Hearts 2"])

            if "location_name_to_id" in self.kh2_data_package:
                self.data_package_kh2_cache(
                        self.kh2_data_package["location_name_to_id"], self.kh2_data_package["item_name_to_id"])
                self.connect_to_game()
            else:
                asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Kingdom Hearts 2"]}]))

            self.locations_checked = set(args["checked_locations"])

        if cmd == "ReceivedItems":
            # Sora   Front of Ability List:0x2546
            # Donald Front of Ability List:0x2658
            # Goofy  Front of Ability List:0x276A
            start_index = args["index"]
            if start_index == 0:
                self.kh2_seed_save_cache = {
                    "itemIndex":  -1,
                    #  back of soras invo is 0x25E2. Growth should be moved there
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
                        "Equipment":    {},  # ItemName: Amount
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
            if start_index > self.kh2_seed_save_cache["itemIndex"] and self.serverconnected:
                self.kh2_seed_save_cache["itemIndex"] = start_index
                for item in args['items']:
                    networkItem = NetworkItem(*item)

                    # actually give player the item
                    asyncio.create_task(self.give_item(networkItem.item, networkItem.location))

        if cmd == "RoomUpdate":
            if "checked_locations" in args:
                new_locations = set(args["checked_locations"])
                self.locations_checked |= new_locations

        if cmd == "DataPackage":
            if "Kingdom Hearts 2" in args["data"]["games"]:
                self.data_package_kh2_cache(
                        args["data"]["games"]["Kingdom Hearts 2"]["location_name_to_id"],
                        args["data"]["games"]["Kingdom Hearts 2"]["item_name_to_id"])
                self.connect_to_game()
                asyncio.create_task(self.send_msgs([{'cmd': 'Sync'}]))

        if cmd == "PrintJSON":
            # shamelessly stolen from kh1
            if args.get("type") == "ItemSend":
                item = args["item"]
                networkItem = NetworkItem(*item)
                itemId = networkItem.item
                receiverID = args["receiving"]
                senderID = networkItem.player
                receive_popup_type = self.client_settings["receive_popup_type"].lower()
                send_popup_type = self.client_settings["send_popup_type"].lower()
                receive_truncate_first = self.client_settings["receive_truncate_first"].lower()
                send_truncate_first = self.client_settings["send_truncate_first"].lower()
                # checking if sender is the kh2 player, and you aren't sending yourself the item
                if receiverID == self.slot and senderID != self.slot:  # item is sent to you and is not from yourself
                    itemName = self.item_names.lookup_in_game(itemId)
                    playerName = self.player_names[networkItem.player]  # player that sent you the item
                    totalLength = len(itemName) + len(playerName)

                    if receive_popup_type == "info":  # no restrictions on size here
                        temp_length = f"Obtained {itemName} from {playerName}"
                        if totalLength > 90:
                            self.queued_info_popup += [temp_length[:90]]  # slice it to be 90
                        else:
                            self.queued_info_popup += [temp_length]
                    else:  # either chest or puzzle. they are handled the same length wise
                        totalLength = len(itemName) + len(playerName)
                        while totalLength > 25:
                            if receive_truncate_first == "playername":
                                if len(playerName) > 5:
                                    playerName = playerName[:-1]
                                else:
                                    itemName = itemName[:-1]
                            else:
                                if len(ItemName) > 15:
                                    itemName = itemName[:-1]
                                else:
                                    playerName = playerName[:-1]
                            totalLength = len(itemName) + len(playerName)
                        # from  =6. totalLength of the string cant be over 31 or game crash
                        if receive_popup_type == "puzzle":  # sanitize ItemName and receiver name
                            self.queued_puzzle_popup += [f"{itemName} from {playerName}"]
                        else:
                            self.queued_chest_popup += [f"{itemName} from {playerName}"]

                if receiverID != self.slot and senderID == self.slot:  #item is sent to other players
                    itemName = self.item_names.lookup_in_slot(itemId, receiverID)
                    playerName = self.player_names[receiverID]
                    totalLength = len(itemName) + len(playerName)
                    if send_popup_type == "info":
                        if totalLength > 90:
                            temp_length = f"Sent {itemName} to {playerName}"
                            self.queued_info_popup += [temp_length[:90]]  #slice it to be 90
                        else:
                            self.queued_info_popup += [f"Sent {itemName} to {playerName}"]
                    else:  # else chest or puzzle. they are handled the same length wise
                        while totalLength > 27:
                            if send_truncate_first == "playername":
                                if len(playerName) > 5: #limit player name to at least be 5 characters
                                    playerName = playerName[:-1]
                                else:
                                    itemName = itemName[:-1]
                            else:
                                if len(ItemName) > 15: # limit item name to at least be 15 characters
                                    itemName = itemName[:-1]
                                else:
                                    playerName = playerName[:-1]
                            totalLength = len(itemName) + len(playerName)
                        if send_popup_type == "puzzle":
                            # to = 4 totalLength of the string cant be over 31 or game crash
                            self.queued_puzzle_popup += [f"{itemName} to {playerName}"]
                        else:
                            self.queued_chest_popup += [f"{itemName} to {playerName}"]

    def connect_to_game(self):
        if "KeybladeAbilities" in self.kh2slotdata.keys():
            # sora ability to slot
            self.AbilityQuantityDict.update(self.kh2slotdata["KeybladeAbilities"])
            # itemid:[slots that are available for that item]
            self.AbilityQuantityDict.update(self.kh2slotdata["StaffAbilities"])
            self.AbilityQuantityDict.update(self.kh2slotdata["ShieldAbilities"])

        self.all_weapon_location_id = {self.kh2_loc_name_to_id[loc] for loc in all_weapon_slot}

        try:
            if not self.kh2:
                self.kh2 = pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
                self.get_addresses()

        except Exception as e:
            if self.kh2connected:
                self.kh2connected = False
            logger.info("Game is not open. If it is open run the launcher/client as admin.")
        self.serverconnected = True
        self.slot_name = self.auth

    def data_package_kh2_cache(self, loc_to_id, item_to_id):
        self.kh2_loc_name_to_id = loc_to_id
        self.lookup_id_to_location = {v: k for k, v in self.kh2_loc_name_to_id.items()}
        self.kh2_item_name_to_id = item_to_id
        self.lookup_id_to_item = {v: k for k, v in self.kh2_item_name_to_id.items()}
        self.ability_code_list = [self.kh2_item_name_to_id[item] for item in exclusion_item_table["Ability"]]

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        """Gets dispatched when a new DeathLink is triggered by another linked player."""
        if data["source"] not in self.deathlink_blacklist:
            self.last_death_link = max(data["time"], self.last_death_link)
            text = data.get("cause", "")
            if text:
                logger.info(f"DeathLink: {text}")
            else:
                logger.info(f"DeathLink: Received from {data['source']}")
            # kills sora by setting flag for the lua to read
            self.kh2_write_byte(0x810000, 1)

    async def is_dead(self):
        # General Death link logic: if hp is 0 and sora has 5 drive gauge and deathlink flag isnt set
        # if deathlink is on and script is hasnt killed sora and sora isnt dead
        if self.deathlink_toggle and self.kh2_read_byte(0x810000) == 0 and self.kh2_read_byte(0x810001) != 0:
            # set deathlink flag so it doesn't send out bunch
            # basically making the game think it got its death from a deathlink instead of from the game
            self.kh2_write_byte(0x810000, 0)
            # 0x810001 is set to 1 when you die via the goa script. This is done because the polling rate for the client can miss a death
            # but the lua script runs eveery frame so we cant miss them now
            self.kh2_write_byte(0x810001, 0)
            #todo: read these from the goa lua instead since the deathlink is after they contiune which means that its just before they would've gotten into the fight
            Room = self.kh2_read_byte(0x810002)
            Event = self.kh2_read_byte(0x810003)
            World = self.kh2_read_byte(0x810004)
            if (World, Room, Event) in DeathLinkPair.keys():

                logger.info(f"Deathlink: {self.player_names[self.slot]} died to {DeathLinkPair[(World,Room, Event)]}.")
                await self.send_death(death_text=f"{self.player_names[self.slot]} died to {DeathLinkPair[(World,Room, Event)]}.")
            else:
                logger.info(f"Deathlink: {self.player_names[self.slot]} lost their heart to darkness.")
                await self.send_death(death_text=f"{self.player_names[self.slot]} lost their heart to darkness.")

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

    def get_addresses(self):
        if not self.kh2connected and self.kh2 is not None:
            if self.kh2_game_version is None:
                # current verions is .10 then runs the get from github stuff
                if self.kh2_read_string(0x9A98B0, 4) == "KH2J":
                    self.kh2_game_version = "STEAM"
                    self.Now = 0x0717008
                    self.Save = 0x09A98B0
                    self.Slot1 = 0x2A23598
                    self.Journal = 0x7434E0
                    self.Shop = 0x7435D0
                    self.InfoBarPointer = 0xABE828
                    self.isDead = 0x0BEF4A8
                    self.FadeStatus = 0xABB4B8
                    self.PlayerGaugePointer = 0x0ABD248
                elif self.kh2_read_string(0x9A9330, 4) == "KH2J":
                    self.kh2_game_version = "EGS"
                else:
                    if self.game_communication_path:
                        logger.info("Checking with most up to date addresses from the addresses json.")
                        # if mem addresses file is found then check version and if old get new one
                        kh2memaddresses_path = os.path.join(self.game_communication_path, "kh2memaddresses.json")
                        if not os.path.exists(kh2memaddresses_path):
                            logger.info("File is not found. Downloading json with memory addresses. This might take a moment")
                            mem_resp = requests.get("https://raw.githubusercontent.com/JaredWeakStrike/KH2APMemoryValues/master/kh2memaddresses.json")
                            if mem_resp.status_code == 200:
                                self.mem_json = json.loads(mem_resp.content)
                                with open(kh2memaddresses_path, 'w') as f:
                                    f.write(json.dumps(self.mem_json, indent=4))
                                    f.close()
                        else:
                            with open(kh2memaddresses_path) as f:
                                self.mem_json = json.load(f)
                                f.close()
                        if self.mem_json:
                            for key in self.mem_json.keys():
                                if self.kh2_read_string(int(self.mem_json[key]["GameVersionCheck"], 0), 4) == "KH2J":
                                    self.Now = int(self.mem_json[key]["Now"], 0)
                                    self.Save = int(self.mem_json[key]["Save"], 0)
                                    self.Slot1 = int(self.mem_json[key]["Slot1"], 0)
                                    self.Journal = int(self.mem_json[key]["Journal"], 0)
                                    self.Shop = int(self.mem_json[key]["Shop"], 0)
                                    self.InfoBarPointer = int(self.mem_json[key]["InfoBarPointer"], 0)
                                    self.isDead = int(self.mem_json[key]["isDead"], 0)
                                    self.FadeStatus = int(self.mem_json[key]["FadeStatus"], 0)
                                    self.PlayerGaugePointer = int(self.mem_json[key]["PlayerGaugePointer"], 0)
                                    self.kh2_game_version = key

            if self.kh2_game_version is not None:
                logger.info(f"You are now auto-tracking {self.kh2_game_version}")
                self.kh2connected = True
            else:
                logger.info("Your game version does not match what the client requires. Check in the "
                            "kingdom-hearts-2-final-mix channel for more information on correcting the game "
                            "version.")
                self.kh2connected = False


async def kh2_watcher(ctx: KH2Context):
    while not ctx.exit_event.is_set():
        try:
            if ctx.kh2connected and ctx.serverconnected:
                ctx.sending = []
                await asyncio.create_task(ctx.checkWorldLocations())
                await asyncio.create_task(ctx.checkLevels())
                await asyncio.create_task(ctx.checkSlots())
                await asyncio.create_task(ctx.verifyChests())
                await asyncio.create_task(ctx.verifyItems())
                await asyncio.create_task(ctx.verifyLevel())
                await asyncio.create_task(ctx.is_dead())

                if (ctx.deathlink_toggle and "DeathLink" not in ctx.tags) or (not ctx.deathlink_toggle and "DeathLink" in ctx.tags):
                    await ctx.update_death_link(ctx.deathlink_toggle)

                if finishedGame(ctx) and not ctx.kh2_finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    ctx.kh2_finished_game = True

                if ctx.sending:
                    message = [{"cmd": 'LocationChecks', "locations": ctx.sending}]
                    await ctx.send_msgs(message)

                if ctx.queued_puzzle_popup:
                    await asyncio.create_task(ctx.displayPuzzlePieceTextinGame(ctx.queued_puzzle_popup[0]))  # send the num 1 index of whats in the queue
                if ctx.queued_info_popup:
                    await asyncio.create_task(ctx.displayInfoTextinGame(ctx.queued_info_popup[0]))
                if ctx.queued_chest_popup:
                    await asyncio.create_task(ctx.displayChestTextInGame(ctx.queued_chest_popup[0]))

            elif not ctx.kh2connected and ctx.serverconnected:
                logger.info("Game Connection lost. trying to reconnect.")
                ctx.kh2 = None
                #todo: change this to be an option for the client to auto reconnect with the default being yes
                # reason is because the await sleep causes the client to hang if you close the game then the client without disconnecting.
                while not ctx.kh2connected and ctx.serverconnected:
                    try:
                        ctx.kh2 = pymem.Pymem(process_name="KINGDOM HEARTS II FINAL MIX")
                        ctx.get_addresses()
                        logger.info("Game Connection Established.")
                    except Exception as e:
                        await asyncio.sleep(5)
            if ctx.disconnect_from_server:
                ctx.disconnect_from_server = False
                await ctx.disconnect()
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
