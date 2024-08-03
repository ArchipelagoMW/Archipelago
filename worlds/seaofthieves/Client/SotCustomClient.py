from __future__ import annotations

import random
import time

# CommonClient import first to trigger ModuleUpdater
# import winsound
from worlds.seaofthieves.Locations.LocationCollection import LocationDetailsCollection, LocDetails
from worlds.seaofthieves.Items.ItemCollection import ItemCollection
from worlds.seaofthieves.Items.Items import Items
from worlds.seaofthieves.Items.ItemDetail import ItemDetail
from worlds.seaofthieves.Client.Shop import Shop
from worlds.seaofthieves.Client.SotWebOptions import SotWebOptions
from worlds.seaofthieves import ClientInput
import worlds.seaofthieves.Client.PlayerInventory as PlayerInventory
import colorama
import CommonClient
from CommonClient import CommonContext, server_loop, ClientCommandProcessor, gui_enabled, get_base_parser
import worlds.seaofthieves.Client.SOTDataAnalyzer as SOTDataAnalyzer
import typing
from NetUtils import ClientStatus, NetworkItem, JSONtoTextParser, JSONMessagePart, add_json_item, add_json_location, \
    add_json_text, JSONTypes
import worlds.seaofthieves.Client.UserInformation as UserInformation
import asyncio
import Utils
from typing import NamedTuple
from worlds.seaofthieves.Client.NetworkProtocol.PrintJsonPacket import PrintJsonPacket
from worlds.seaofthieves.Client.NetworkProtocol.ReceivedItemsPacket import ReceivedItemsPacket
from worlds.seaofthieves.Client.NetworkProtocol.SetReply import SetReplyPacket
import worlds.seaofthieves.Locations.Shop.Balance as Balance


class Version(NamedTuple):
    major: int
    minor: int
    build: int


class SOT_CommandProcessor(ClientCommandProcessor):
    ctx: SOT_Context

    def _cmd_hints(self) -> bool:
        """Displays hints you have purchased"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        for hint in self.ctx.playerInventory.get_hints():
            self.output(hint)
        return True

    def _cmd_tracker(self) -> bool:
        """Displays autotracker"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        self.output("Auto tracker is on if true: " +str(self.ctx.message_displayed))
        return True

    def _cmd_forceunlock(self) -> bool:
        """Removes all location logic restrictions"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        self.output("All location restrictions removed, tracking all. (Activates in 10 seconds)")
        self.ctx.forceUnlock = True

    # def _cmd_linkShip(self, command: str) -> bool:
    #     """Tracks another ship on this world"""
    #     if not self.ctx.connected_to_server:
    #         self.output("Connect to server before issuing this command.")
    #         return True
    #     self.output("Not Implemented")
    #     return False
    #
    # def _cmd_linkPirate(self, command: str) -> bool:
    #     """Tracks another pirate on this world"""
    #     if not self.ctx.connected_to_server:
    #         self.output("Connect to server before issuing this command.")
    #         return True
    #     self.output("Not Implemented")
    #     return False

    def _cmd_shop(self) -> bool:
        """Opens the shop"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        self.ctx.shop.info(self.ctx.playerInventory)
        return True

    def _cmd_buy(self, menu_line_number):
        """Allows you to buy an item from the shop"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        menu_line_number = str(menu_line_number)
        menu_lin_numbeer_executed: typing.Optional[int] = self.ctx.shop.executeAction(menu_line_number, self.ctx.playerInventory)


    def _cmd_locs(self, arg: typing.Optional[str] = None):
        """Displays locations you can currently complete (argument -f adds display of filler locations)"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        loc_details_possible: typing.List[LocDetails] = self.ctx.locationsReachableWithCurrentItems()

        possible_progression_locations = 0
        possible_filler_locations = 0

        for loc in loc_details_possible:
            if loc.id not in self.ctx.locations_checked:
                if loc.doRandomize:
                    possible_progression_locations += 1
                else:
                    possible_filler_locations += 1

        show_fillers: bool = arg == "-f"

        num = 1
        for loc in loc_details_possible:
            if loc.id not in self.ctx.locations_checked and (show_fillers or loc.doRandomize):
                self.output("{}. [{}] {}".format(num, loc.id, loc.name))
                num += 1

        display_strings: typing.List[str] = [
            "Total Locations Remaining: {}".format(possible_progression_locations + possible_filler_locations),
            "Total Locations w/ possible progression: {}".format(possible_progression_locations),
            "Total Locations w/ filler: {}".format(possible_filler_locations)
        ]
        for ln in display_strings:
            self.output(ln)

    def _cmd_complete(self, locId):
        """Force completes a check. Enter "-all" to complete all checks displayed with locs command"""
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True

        if locId == "-all" or locId == "-allf":
            loc_details_possible: typing.List[LocDetails] = self.ctx.locationsReachableWithCurrentItems()
            for loc in loc_details_possible:
                if loc.id not in self.ctx.locations_checked and (locId == "-allf" or loc.doRandomize):
                    self.ctx.locations_checked.add(int(loc.id))
                    self.ctx.analyzer.stopTracking(int(loc.id))

        else:
            self.ctx.locations_checked.add(int(locId))
            self.ctx.analyzer.stopTracking(int(locId))

    def _cmd_connect(self, address: str = "") -> bool:
        if self.ctx.userInformation.generationData is None:
            self.output("Stop, you must first upload your SOTCI file!")
            return False
        else:
            asyncio.create_task(self.ctx.connect(address))

    def _cmd_mrkrabs(self):
        if not self.ctx.connected_to_server:
            self.output("Connect to server before issuing this command.")
            return True
        """Gives you alot of money"""
        self.output("You now have alot of money.")
        self.ctx.playerInventory.addBalanceClient(Balance.Balance(100000000, 100000000, 10000000))

    def _cmd_setmode(self, mode):

        """Sets mode, pass "NA" for pirate mode, or pass your ship number for ship mode"""
        ship = mode

        pirate = None
        if ship == "NA":
            ship = None
            pirate = "pirateMode"  # this just needs to be not null

        self.ctx.userInformation.analyzerDetails = UserInformation.SotAnalyzerDetails(ship, pirate)
        self.ctx.analyzer.settings = SOTDataAnalyzer.SOTDataAnalyzerSettings(self.ctx.userInformation.analyzerDetails)
        self.output("Mode set to {}".format(mode))

    def _cmd_setcookie(self):
        """Sets msCookie, pass "Absolute Filepath" to cookie without quotes"""

        try:
            cookie_file_name = Utils.open_filename('Select Cookie.txt file', (('APSOT File', ('.txt',)),))
            file = open(cookie_file_name, "r")
            real_cookie = str(file.read())
            file.close()
        except Exception as e:
            self.output("Error uploading cookie file, was your filepath correct? {}".format(e))
            return

        if len(real_cookie) > 1:
            self.ctx.setCookie(real_cookie)
            self.output("Cookie Set Successfully")
        else:
            self.output("Error setting cookie, either could not locate file or file was empty")



class SOT_Context(CommonContext):
    command_processor = SOT_CommandProcessor

    def __init__(self, serverAddress: typing.Optional[str] = None, serverPassword: typing.Optional[str] = None):
        super().__init__(serverAddress, serverPassword)
        Utils.init_logging("Sea of Thieves Client")
        self.stop_application: bool = False

        self.webOptions: SotWebOptions = SotWebOptions()

        self.userInformation = UserInformation.UserInformation()
        self.analyzer: typing.Optional[SOTDataAnalyzer.SOTDataAnalyzer] = SOTDataAnalyzer.SOTDataAnalyzer(
            self.userInformation)
        self.known_items_received: typing.List = []  # used to track measured received counts
        self.locationDetailsCollection: LocationDetailsCollection = LocationDetailsCollection()
        self.itemCollection: ItemCollection = ItemCollection()
        self.shop: Shop = Shop()
        self.shop.ctx = self
        self.playerInventory: PlayerInventory = PlayerInventory.PlayerInventory()
        self.connected_to_server: bool = False
        self.originalBalance: Balance.Balance | None = None
        self.forceUnlock: bool = False
        self.active_tasks: typing.List[asyncio.Task] = []
        self.message_displayed = False

        self.shop_history_queue: typing.List[int] = list()

    async def updaterLoopa(self):
        await self.updaterLoop()

    def create_tasks(self):
        self.active_tasks.append(asyncio.create_task(CommonClient.server_loop(self), name="server loop"))

        try:
            apsot_file = Utils.open_filename('Select APSOT file', (('APSOT File', ('.apsot',)),))
            client_input: ClientInput = ClientInput()
            client_input.from_fire(apsot_file)
            self.userInformation.generationData = client_input
        except Exception as e:
            self.output("Error uploading sotci file, was your filepath correct? {}".format(e))
            exit(1)
        self.active_tasks.append(asyncio.create_task(self.updaterLoopa(), name="game watcher"))

    def run_gui_and_cli(self):
        if CommonClient.gui_enabled:
            self.run_gui()
        self.run_cli()

    async def application_exit(self):
        await self.exit_event.wait()
        await self.end_tasks()

    async def end_tasks(self):
        self.stop_application = True
        for task in self.active_tasks:
            await task

    async def updaterLoop(self):
        first_pass = True
        exception_attempts = 0
        while not self.stop_application:
            try:
                await asyncio.sleep(1)
                if self.connected_to_server:
                    if first_pass:
                        await self.init_notif()
                        #await self.init_shop_history()
                        first_pass = False
                    else:
                        try:
                            self.updateSotPlayerBalance()
                            self.updateAnalyzerWithLocationsPossible()
                            await self.collectLocationsAndSendInformation()
                        except Exception as e:
                            self.output("Error occurred: " + str(e))
            except Exception as e:
                self.output("Updater Loop Unrecoverable Failure (Stopping Application after 3 attempts): " + str(e))
                exception_attempts += 1
                if exception_attempts == 3:
                    self.stop_application = True

        # stop the processes
        if self.analyzer is not None:
            self.analyzer.stop_tasks()

    def setCookie(self, value: typing.Optional[str]):

        if value is None:
            self.userInformation.loginCreds = None
            self.webOptions.setQueries(False)
        else:
            self.userInformation.loginCreds = UserInformation.SotLoginCredentials(value)
            self.webOptions.setQueries(True)

        self.analyzer.rebuild_web_collector(self.userInformation.loginCreds)

    def output(self, text):
        self.command_processor.output(self.command_processor, text)


    async def init_notif(self):
        keys: typing.List[str] = [Items.kraken.name]
        await self.snd_notify(keys)
        return

    def locationsReachableWithCurrentItems(self, forceUnlock: bool = False) -> typing.List[LocDetails]:

        currentItems: typing.Set[str] = set()

        # check out our current items
        for item in self.items_received:
            item_id = item.item
            name: str = self.itemCollection.getNameFromId(item_id)

            # if the name is null, there is a bug but we should handle it here
            if (name != ""):
                currentItems.add(name)

        return self.locationDetailsCollection.findDetailsCheckable(currentItems, forceUnlock)

    def on_package(self, cmd: str, args: dict):
        if cmd == "RoomInfo":
            try:
                if not self.userInformation.hasEnoughToPlay():
                    self.output("\nConnection prevented. You must first upload your SOTCI file!")
                    asyncio.create_task(self.disconnect())
                    return
                asyncio.create_task(self.snd_connect())
            except Exception as e:
                self.output("There was an issue where you did not select an input file at launch or it was not detected. Please close launcher and retry {}".format(e))

        elif cmd == "Connected":

            self.connected_to_server = True
            self.locationDetailsCollection.applyOptions(self.userInformation.generationData.sotOptionsDerived
                                                        , random.Random())
            self.locationDetailsCollection.addAll()
            self.locationDetailsCollection.applyRegionDiver(self.userInformation.generationData.regionRules)
            self.locations_checked = set(args["checked_locations"])
            self.shop.addWarehouse(self.userInformation.generationData.shopWarehouse, self.playerInventory)
            self.shop.addHintLibarary(self.userInformation.generationData.hintLibrary, self.playerInventory)


        elif cmd == "LocationInfo":
            pass
            # TODO we should acknowledge the items have been received and stop sending them again

        elif cmd == "RoomUpdate":
            pass

        elif cmd == "Bounced":
            pass

        elif cmd == "Retrieved":
            pass

        elif cmd == "ReceivedItems":

            received_items_packet: ReceivedItemsPacket = ReceivedItemsPacket(args)
            if received_items_packet.items is not None:
                self.items_received = received_items_packet.items
                for item in self.items_received:
                    self.playerInventory.add_item(item.item, self.itemCollection.getNameFromId(item.item))
                    self.applyMoneyIfMoney(item)
                    if Items.pirate_legend.id == item.item:
                        self.finished_game = True
                        # we could send the signal here to finish the game, but if it got dropped that would be bad
                        # instead we do it in the main game loop

        elif cmd == "PrintJSON":
            printJsonPacket: PrintJsonPacket = PrintJsonPacket(args)
            printJsonPacket.print()

        elif cmd == "SetReply":
            setReplyPacket: SetReplyPacket = SetReplyPacket(args)
            if setReplyPacket.key is Items.kraken.name:
                puns = [
                    "Captain! " + colorama.Fore.YELLOW + "Another Player " + colorama.Fore.RESET + "leveraged to much naval real estate and succumbed to collections",
                    "Captain! " + colorama.Fore.YELLOW + "Another Player " + colorama.Fore.RESET + "invested their money in an MLM",
                    "Captain! " + colorama.Fore.YELLOW + "Another Player " + colorama.Fore.RESET + "sent their money to a long lost royal relative stuck in prison"
                ]

                print(random.choice(puns))

            # self.playAudio(setReplyPacket.key)

        else:
            self.output("Error: Server requested unsupported feature '{0}'".format(cmd))
            # this is where you read slot data if any

    def applyMoneyIfMoney(self, itm: NetworkItem):

        gold_ids: typing.Dict[int, int] = {Items.gold_50.id: Items.gold_50.numeric_value,
                                           Items.gold_100.id: Items.gold_100.numeric_value,
                                           Items.gold_500.id: Items.gold_500.numeric_value}

        dabloon_ids: typing.Dict[int, int] = {Items.dabloons_25.id: Items.dabloons_25.numeric_value}

        coin_ids: typing.Dict[int, int] = {Items.ancient_coins_10.id: Items.ancient_coins_10.numeric_value}
        item_id = itm.item
        if item_id in gold_ids.keys():
            gold_val = gold_ids[item_id]
            ac = 0
            db = 0
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        elif item_id == Items.kraken:
            self.output(
                "Captain! The legendary " + colorama.Fore.YELLOW + Items.kraken.name + colorama.Style.RESET_ALL + " is coming for your " + colorama.Fore.GREEN + "COINS" + colorama.Fore.RESET + ". You are now broke.")
            self.playerInventory.setBalanceSot(Balance.Balance(-10000, -10000, -10000))
            self.snd_add(Items.kraken.name)

        elif item_id in dabloon_ids.keys():
            gold_val = 0
            ac = 0
            db = dabloon_ids[item_id]
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        elif item_id in coin_ids.keys():
            gold_val = 0
            ac = coin_ids[item_id]
            db = 0
            self.playerInventory.addBalanceClient(Balance.Balance(ac, db, gold_val))

        return

    def acknowledgeItemsReceived(self):
        self.known_items_received = self.items_received

    def updateAnalyzerWithLocationsPossible(self):

        loc_details_possible: typing.List[LocDetails] = self.locationsReachableWithCurrentItems(self.forceUnlock)

        if self.webOptions.allowCaptainQuery:
            for loc_detail in loc_details_possible:
                try:
                    self.analyzer.allowTrackingOfLocation(loc_detail)
                except Exception as e:
                    pass
                    #self.output("Recoverable error, did you /setmode? - Auto-tracker failed for: {} [{}]".format(loc_detail.name, loc_detail.id))


        self.acknowledgeItemsReceived()

    def updateSotPlayerBalance(self):

        if not self.webOptions.allowBalanceQuery:
            return

        if self.message_displayed == False:
            self.output("AUTO TRACKER ENABLED")
            self.message_displayed = True

        new_balance = self.analyzer.getBalance()
        if self.originalBalance is None:
            self.originalBalance = new_balance
        new_balance = new_balance - self.originalBalance
        self.playerInventory.setBalanceSot(new_balance)

    async def collectLocationsAndSendInformation(self):

        await self.snd_sync()  # get items from the server
        self.discoverCheckedLocationsAndStopTracking()  # look at what locations the player has checked
        await self.snd_location_checks()  # notify the server of those locations
        await self.snd_location_souts()  # notify the server of those locations
        await self.notifyServerIfGameIsFinished() # tell the server if we have finished the game
        await self.save_client_volitile_data_to_server_for_backup() # save data that would be destroyed on client close that we would like to keep

    async def save_client_volitile_data_to_server_for_backup(self):

        # save shop history
        while len(self.shop_history_queue) > 0:
            value = self.shop_history_queue.pop()
            await self.snd_add(value)
        return

    async def notifyServerIfGameIsFinished(self):
        if self.finished_game:
            await self.snd_game_finished()

    def discoverCheckedLocationsAndStopTracking(self):
        # We may not be allowed to query the players url
        if self.webOptions.allowCaptainQuery:
            self.analyzer.update()
            completedChecks: typing.Dict[int, bool] = self.analyzer.getAllCompletedChecks()
            for k in completedChecks.keys():
                if completedChecks[k]:
                    self.locations_checked.add(k)
                    self.analyzer.stopTracking(k)

        # check if the player bought any items?
        for loc_id in self.playerInventory.itemsToSendToClient:
            self.locations_checked.add(loc_id)
        self.playerInventory.itemsToSendToClient.clear()

    async def snd_notify(self, keys: typing.List[str]):
        await self.send_msgs([
            {
                "cmd": "SetNotify",
                "keys": keys,
            }
        ])

    async def snd_sync(self):
        await self.send_msgs([
            {
                "cmd": "Sync"
            }
        ])

    async def snd_location_checks(self):
        msg = [
            {
                "cmd": "LocationChecks",
                "locations": list(self.locations_checked)
            }
        ]
        await self.send_msgs(msg)

    async def snd_location_souts(self):
        msg = [
            {
                "cmd": "LocationScouts",
                "locations": list(self.locations_checked)
            }
        ]
        await self.send_msgs(msg)

    async def snd_get(self, list_keys):
        # Sync server items to us
        await self.send_msgs([
            {
                "keys": list_keys,
            }
        ])
    async def snd_add(self, key):
        # Sync server items to us
        await self.send_msgs([
            {
                "cmd": "Set",
                "key": key,
                "default": 0,
                "want_reply": 1,
                "operations": [{"operation": "add", "value": 1}]
            }
        ])

    async def snd_set(self, key, value):
        # Sync server items to us
        await self.send_msgs([
            {
                "cmd": "Set",
                "key": key,
                "default": 0,
                "want_reply": 1,
                "operations": [{"operation": "replace", "value": value}]
            }
        ])

    async def snd_connect(self):

        username = self.userInformation.generationData.sotOptionsDerived.player_name
        await self.send_msgs([
            {
                "cmd": "Connect",
                "game": "Sea of Thieves",
                "password": "",
                "name": username,
                "uuid": username,
                "items_handling": 0b111,
                "slot_data": True,
                "tags": [],
                "version": Version(1, 1, 1)
            }
        ])
        return

    async def snd_game_finished(self):
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
