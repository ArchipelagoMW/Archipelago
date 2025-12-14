from __future__ import annotations
from ast import Dict
from enum import IntEnum
import ModuleUpdate
import Utils

ModuleUpdate.update()
import os
import asyncio
import json
import requests

from .Socket import KH2Socket
from worlds.kh2 import item_dictionary_table, exclusion_item_table, CheckDupingItems, all_locations, exclusion_table, \
    SupportAbility_Table, ActionAbility_Table, all_weapon_slot, Summon_Checks, popups_set
from worlds.kh2.Names import ItemName
from .WorldLocations import *

from NetUtils import ClientStatus, NetworkItem
from CommonClient import gui_enabled, logger, get_base_parser, CommonContext, server_loop
from .CMDProcessor import KH2CommandProcessor
slot_data_sent = False

class MessageType (IntEnum):
    Invalid = -1,
    Test = 0,
    WorldLocationChecked = 1,
    LevelChecked = 2,
    KeybladeChecked = 3,
    SlotData = 4,
    BountyList = 5,
    Deathlink = 6,
    NotificationType = 7,
    NotificationMessage = 8,
    ReceiveItem = 10,
    RequestAllItems = 11,
    Handshake  = 12,
    Victory = 19,
    Closed = 20

class KH2Context(CommonContext):
    command_processor = KH2CommandProcessor
    game = "Kingdom Hearts 2"
    items_handling = 0b111  # Indicates you get items sent from other worlds.
    socket: KH2Socket = None
    check_location_IDs = []
    received_items_IDs = []

    def __init__(self, server_address, password):
        super(KH2Context, self).__init__(server_address, password)

        #Socket
        self.socket = KH2Socket(self)
        asyncio.create_task(self.socket.start_server(), name="KH2SocketServer")

        self.kh2connectionconfirmed = False
        self.kh2connectionsearching = False
        self.number_of_abilities_sent = dict()
        self.all_party_abilities = dict()
        self.kh2_local_items = None
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

        self.kh2seedname = None

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
        self.current_world_int = -1
        self.sora_form_levels = {
            "Sora": 1,
            "ValorLevel": 1,
            "WisdomLevel": 1,
            "LimitLevel": 1,
            "MasterLevel": 1,
            "FinalLevel": 1,
            "SummonLevel": 1,
        }
        self.sora_levels = {
            "SoraLevel": 1,
            "ValorLevel": 1,
            "WisdomLevel": 1,
            "LimitLevel": 1,
            "MasterLevel": 1,
            "FinalLevel": 1,
            "SummonLevel": 1,
        }
        self.world_locations_checked = list()
        self.Room = -1
        self.Event = -1
        self.World = -1
        self.SoraDied = False
        self.keyblade_ability_checked = list()

        self.master_growth = {"High Jump", "Quick Run", "Dodge Roll", "Aerial Dodge", "Glide"}

        self.deathlink_toggle = False
        self.deathlink_blacklist = []

    from .SendChecks import checkWorldLocations, checkSlots, checkLevels

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
        self.serverconnected = False
        await super(KH2Context, self).connection_closed()

    async def disconnect(self, allow_autoreconnect: bool = False):
        self.serverconnected = False
        self.locations_checked = []
        await super(KH2Context, self).disconnect()

    @property
    def endpoints(self):
        if self.server:
            return [self.server]
        else:
            return []

    async def shutdown(self):
        with open(self.kh2_client_settings_join, 'w') as f2:
            f2.write(json.dumps(self.client_settings, indent=4))
            f2.close()
        try:
            self.socket.send(MessageType.Closed, ())
            self.socket.shutdown_server()
        except:
            pass
        await super(KH2Context, self).shutdown()

    def on_package(self, cmd: str, args: dict):
        if cmd == "RoomInfo":
            if not self.kh2seedname:
                self.kh2seedname = args['seed_name']
            elif self.kh2seedname != args['seed_name']:
                self.disconnect_from_server = True
                self.serverconnected = False
                logger.info("Connection to the wrong seed, connect to the correct seed or close the client.")
                return

        if cmd == "Connected":
            self.kh2slotdata = args['slot_data']
            self.all_party_abilities = {**self.kh2slotdata["SoraAbilities"], **self.kh2slotdata["DonaldAbilities"], **self.kh2slotdata["GoofyAbilities"]}

            self.kh2_data_package = Utils.load_data_package_for_checksum(
                    "Kingdom Hearts 2", self.checksums["Kingdom Hearts 2"])

            if "location_name_to_id" in self.kh2_data_package:
                self.data_package_kh2_cache(
                        self.kh2_data_package["location_name_to_id"], self.kh2_data_package["item_name_to_id"])
                self.connect_to_game()
            else:
                asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Kingdom Hearts 2"]}]))

            self.locations_checked = set(args["checked_locations"])

            global slot_data_sent
            if not slot_data_sent:
                if self.kh2connectionconfirmed:
                    if self.kh2slotdata['BountyBosses']:
                        for location in self.kh2slotdata['BountyBosses']:
                            self.socket.send(MessageType.BountyList, [location])
                    self.socket.send_slot_data('Final Xemnas;' + str(self.kh2slotdata['FinalXemnas']))
                    self.socket.send_slot_data('Goal;' +str(self.kh2slotdata['Goal']))
                    self.socket.send_slot_data('LuckyEmblemsRequired;' + str(self.kh2slotdata['LuckyEmblemsRequired']))
                    self.socket.send_slot_data('BountyRequired;' + str(self.kh2slotdata['BountyRequired']))
                    self.socket.send(MessageType.NotificationType, ["R", self.client_settings["receive_popup_type"]])
                    self.socket.send(MessageType.NotificationType, ["S", self.client_settings["send_popup_type"]])
                    self.socket.send(MessageType.Deathlink, [str(self.deathlink_toggle)])
                    slot_data_sent = True

        if cmd == "ReceivedItems":
            index = args["index"]
            if self.serverconnected:
                converted_items = list()
                for item in args['items']:
                    name = self.lookup_id_to_item[item.item]
                    item_to_send = self.item_name_to_data[name]
                    msg_to_send = list()
                    if item_to_send.ability:
                        ability_found = self.number_of_abilities_sent.get(name)
                        if not ability_found:
                            self.number_of_abilities_sent[name] = 1
                        else:
                            self.number_of_abilities_sent[name] += 1
                        if name not in self.master_growth:
                            if self.number_of_abilities_sent.get(name) <= self.all_party_abilities.get(name):
                                if "Donald" in name:
                                    msg_to_send = [str(item_to_send.kh2id), "Donald", str(index)]
                                    converted_items.append(msg_to_send)
                                    self.received_items_IDs.append(msg_to_send)
                                elif "Goofy" in name:
                                    msg_to_send = [str(item_to_send.kh2id), "Goofy", str(index)]
                                    converted_items.append(msg_to_send)
                                    self.received_items_IDs.append(msg_to_send)
                                else:
                                    msg_to_send = [str(item_to_send.kh2id), "Sora", str(index)]
                                    converted_items.append(msg_to_send)
                                    self.received_items_IDs.append(msg_to_send)
                        else:
                            msg_to_send = [str(item_to_send.kh2id), "Sora", str(index)]
                            converted_items.append(msg_to_send)
                            self.received_items_IDs.append(msg_to_send)
                    else:
                        msg_to_send = [str(item_to_send.kh2id), "false", str(index)]
                        converted_items.append(msg_to_send)
                        self.received_items_IDs.append(msg_to_send)
                    index += 1
                if self.kh2connectionconfirmed:
                    #sleep so we can get the datapackage and not miss any items that were sent to us while we didnt have our item id dicts
                    while not self.lookup_id_to_item:
                        asyncio.sleep(0.5)
                    while len(converted_items) >= 1:
                        self.socket.send_Item(converted_items[0])
                        converted_items.pop(0)

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
                if receiverID == self.slot and senderID != self.slot and receive_popup_type != "none":  # item is sent to you and is not from yourself
                    itemName = self.item_names.lookup_in_game(itemId).replace(";",":")
                    playerName = self.player_names[networkItem.player].replace(";",":")  # player that sent you the item
                    totalLength = len(itemName) + len(playerName)

                    if receive_popup_type == "info":  # no restrictions on size here
                        if totalLength > 90:
                            temp_length = f"Obtained {itemName} from {playerName}"
                            self.socket.send(MessageType.NotificationMessage, ["R", temp_length[:90]])
                        else:
                            self.socket.send(MessageType.NotificationMessage,["R", f"Obtained {itemName} from {playerName}"])
                    else:  # either chest or puzzle. they are handled the same length wise
                        totalLength = len(itemName) + len(playerName)
                        while totalLength > 25:
                            if receive_truncate_first == "playername":
                                if len(playerName) > 5:
                                    playerName = playerName[:-1]
                                else:
                                    itemName = itemName[:-1]
                            else:
                                if len(itemName) > 15:
                                    itemName = itemName[:-1]
                                else:
                                    playerName = playerName[:-1]
                            totalLength = len(itemName) + len(playerName)
                        # from  =6. totalLength of the string cant be over 31 or game crash
                        # sanitize ItemName and receiver name
                        self.socket.send(MessageType.NotificationMessage, ["R", f"{itemName} from {playerName}"]) # sanitize ItemName and receiver name

                if receiverID != self.slot and senderID == self.slot and send_popup_type != "none":  #item is sent to other players
                    itemName = self.item_names.lookup_in_slot(itemId, receiverID).replace(";",":")
                    playerName = self.player_names[receiverID].replace(";",":")
                    totalLength = len(itemName) + len(playerName)
                    if send_popup_type == "info":
                        if totalLength > 90:
                            temp_length = f"Sent {itemName} to {playerName}"
                            self.socket.send(MessageType.NotificationMessage, ["S", temp_length[:90]])  #slice it to be 90
                        else:
                            self.socket.send(MessageType.NotificationMessage,["S", f"Sent {itemName} to {playerName}"])
                    else:  # else chest or puzzle. they are handled the same length wise
                        while totalLength > 27:
                            if send_truncate_first == "playername":
                                if len(playerName) > 5: #limit player name to at least be 5 characters
                                    playerName = playerName[:-1]
                                else:
                                    itemName = itemName[:-1]
                            else:
                                if len(itemName) > 15: # limit item name to at least be 15 characters
                                    itemName = itemName[:-1]
                                else:
                                    playerName = playerName[:-1]
                            totalLength = len(itemName) + len(playerName)
                        self.socket.send(MessageType.NotificationMessage,["S", f"{itemName} to {playerName}"])

    def connect_to_game(self):
        self.serverconnected = True
        self.slot_name = self.auth

    def data_package_kh2_cache(self, loc_to_id, item_to_id):
        self.kh2_loc_name_to_id = loc_to_id
        self.lookup_id_to_location = {v: k for k, v in self.kh2_loc_name_to_id.items()}
        self.kh2_item_name_to_id = item_to_id
        self.lookup_id_to_item = {v: k for k, v in self.kh2_item_name_to_id.items()}

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        if (self.deathlink_toggle):
            """Gets dispatched when a new DeathLink is triggered by another linked player."""
            if data["source"] not in self.deathlink_blacklist:
                self.last_death_link = max(data["time"], self.last_death_link)
                text = data.get("cause", "")
                if text:
                    logger.info(f"DeathLink: {text}")
                else:
                    logger.info(f"DeathLink: Received from {data['source']}")
                self.socket.send(MessageType.Deathlink,())

    async def is_dead(self):
        if (self.deathlink_toggle and self.SoraDied):
            if (self.World, self.Room, self.Event) in DeathLinkPair.keys():
                logger.info(f"Deathlink: {self.player_names[self.slot]} died to {DeathLinkPair[(self.World,self.Room, self.Event)]}.")
                await self.send_death(death_text=f"{self.player_names[self.slot]} died to {DeathLinkPair[(self.World,self.Room, self.Event)]}.")
            else:
                logger.info(f"Deathlink: {self.player_names[self.slot]} lost their heart to darkness.")
                await self.send_death(death_text=f"{self.player_names[self.slot]} lost their heart to darkness.")
            self.World = -1
            self.Room = -1
            self.Event = -1
            self.SoraDied = False

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

    def get_items(self):
        """Resend all items and info upon client request"""
        if self.kh2slotdata['BountyBosses']:
            for location in self.kh2slotdata['BountyBosses']:
                self.socket.send(MessageType.BountyList, [location])
        self.socket.send_slot_data('Final Xemnas;' + str(self.kh2slotdata['FinalXemnas']))
        self.socket.send_slot_data('Goal;' +str(self.kh2slotdata['Goal']))
        self.socket.send_slot_data('LuckyEmblemsRequired;' + str(self.kh2slotdata['LuckyEmblemsRequired']))
        self.socket.send_slot_data('BountyRequired;' + str(self.kh2slotdata['BountyRequired']))
        self.socket.send(MessageType.NotificationType, ["R", self.client_settings["receive_popup_type"]])
        self.socket.send(MessageType.NotificationType, ["S", self.client_settings["send_popup_type"]])
        self.socket.send(MessageType.Deathlink, [str(self.deathlink_toggle)])
        slot_data_sent = True

        for item in self.received_items_IDs:
             self.socket.send_Item(item)



async def kh2_watcher(ctx: KH2Context):
    while not ctx.exit_event.is_set():
        try:
            #Check for game connection
            if not ctx.kh2connected:
                if not ctx.kh2connectionsearching:
                    logger.info("Searching for KH2 Game Client...")
                    ctx.kh2connectionsearching = True
                if ctx.socket.isConnected:
                    logger.info(f"KH2 Game Client Found")
                    ctx.kh2connected = True

            if ctx.kh2connectionconfirmed and ctx.serverconnected:
                ctx.sending = []
                await asyncio.create_task(ctx.checkWorldLocations())
                await asyncio.create_task(ctx.checkLevels())
                await asyncio.create_task(ctx.checkSlots())
                await asyncio.create_task(ctx.is_dead())

                if (ctx.deathlink_toggle and "DeathLink" not in ctx.tags) or (not ctx.deathlink_toggle and "DeathLink" in ctx.tags):
                    await ctx.update_death_link(ctx.deathlink_toggle)

                if ctx.kh2_finished_game:
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

                if ctx.sending:
                    ctx.sending = list(await ctx.check_locations(ctx.sending))
                    message = [{"cmd": 'LocationChecks', "locations": ctx.sending}]
                    await ctx.send_msgs(message)
            if ctx.disconnect_from_server:
                ctx.disconnect_from_server = False
                await ctx.disconnect()
        except Exception as e:
            if ctx.kh2connected:
                ctx.kh2connected = False
                ctx.kh2connectionsearching = False
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
