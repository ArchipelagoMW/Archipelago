import random
import typing
from worlds.seaofthieves.Locations.Shop.Balance import Balance
from worlds.seaofthieves.Locations.Shop.ShopLocation import ShopLocation
from worlds.seaofthieves.Client.PlayerInventory import PlayerInventory
from worlds.seaofthieves.Locations.Shop.ShopWarehouse import ShopWarehouse
from worlds.seaofthieves.Hint import Hint, HintStringLibrary, HintLibrary
import os

HINT_IDX = "HINT_IDX"
import colorama

class HintLibraryTracker:

    def __init__(self):
        self.idx_fill = 0
        self.idx_trap = 0
        self.idx_prog = 0

class Shop:

    def __init__(self):

        self.ctx = None

        self.shopWarehouse: typing.Optional[ShopWarehouse] = None
        self.hint_library: typing.Optional[HintStringLibrary] = None
        self.hint_library_tracker: HintLibraryTracker = HintLibraryTracker()


        self.menu = {
            1: ["Buy Generic Hint", 10000, 0],
            2: ["Buy Personal Progression Hint", 15000, 25],
        }
        self.menu_count = len(self.menu)
        self.total_count = self.menu_count
        pass

    def menu_text(self, playerInventory: PlayerInventory):
        st: str = ""

        # Show Base Menu
        for key in self.menu.keys():

            if key <= self.menu_count:
                st += "[ " + str(key) + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(
                    self.menu[key][2]) + " dabloons] \n"
            elif self.menu[key][0].startswith("SOLD OUT"):
                st += "[ " + str(key) + " ] SOLD OUT\n"

            else:
                shopLoc: ShopLocation = self.menu[key][4]
                isReachable: bool = self.isLocationReachable(shopLoc, playerInventory)
                if not isReachable:
                    st += "[ {} ] -- Locked by logic -> {}\n".format(str(key), shopLoc.locDetails.webLocationCollection.logicToString())
                else:
                    st += "[ " + str(key) + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(
                        self.menu[key][2]) + " dabloons] \n"


        return st

    def loadFromWarehouse(self, playerInventory: PlayerInventory) -> None:
        cnt: int = self.menu_count + 1
        item_name_set: typing.Set[str] = set()
        for itm in playerInventory.item_ids_in_inventory.keys():
            item_name_set.add(playerInventory.item_ids_in_inventory[itm])
        for group in self.shopWarehouse.name_to_group.keys():
            for shopLocation in self.shopWarehouse.name_to_group[group].shop_locations:

                self.menu[cnt] = ["[{}] Buy {}".format(shopLocation.shop_abrev ,shopLocation.item_name_override),
                                  shopLocation.locDetails.cost.gold,
                                  shopLocation.locDetails.cost.dabloons,
                                  shopLocation.locDetails.cost.ancient_coins,
                                  shopLocation]
                cnt += 1
        self.total_count = cnt-1

    def addWarehouse(self, warehouse: ShopWarehouse, playerInventory: PlayerInventory):
        self.shopWarehouse = warehouse
        self.loadFromWarehouse(playerInventory)

    def addHintLibarary(self, hint_library: HintStringLibrary, playerInventory: PlayerInventory):
        self.hint_library = hint_library

    def info(self, pinvent: PlayerInventory):
        self.ctx.output("===========================================")
        self.ctx.output("Your Balance " + pinvent.getNominalBalance().displayString())
        self.ctx.output(self.menu_text(pinvent))
        self.ctx.output("Your Balance " + pinvent.getNominalBalance().displayString())
        self.ctx.output("===========================================")
        self.ctx.output("Enter " + "/buy #" + " to purchase.")

    def get_next_hint(self, type: HintLibrary.Type) -> str:
        ret: str
        if type == HintLibrary.Type.TRAP and len(self.hint_library.trap) > self.hint_library_tracker.idx_trap:
            ret = self.hint_library.trap[self.hint_library_tracker.idx_trap]
            self.hint_library_tracker.idx_trap += 1
        elif type == HintLibrary.Type.FILLER and len(self.hint_library.filler) > self.hint_library_tracker.idx_fill:
            ret = self.hint_library.filler[self.hint_library_tracker.idx_fill]
            self.hint_library_tracker.idx_fill += 1
        elif type == HintLibrary.Type.PROGRESSIVE and len(self.hint_library.progressive) > self.hint_library_tracker.idx_prog:
            ret = self.hint_library.progressive[self.hint_library_tracker.idx_prog]
            self.hint_library_tracker.idx_prog += 1
        else:
            ret = "No hints remaining in this category."

        return ret

    def executeAction(self, menu_line_number: str, playerInventory: PlayerInventory) -> typing.Optional[int]:
        menu_line_number: int = int(menu_line_number)
        if menu_line_number == 0:
            return None

        if menu_line_number < 1 or menu_line_number > self.total_count:
            self.ctx.output("Invalid Option")
            return None

        purchase: Balance = Balance(0, self.menu[menu_line_number][2], self.menu[menu_line_number][1])
        if playerInventory.canAfford(purchase):
            playerInventory.spend(purchase)

            if menu_line_number == 1:
                hint = self.get_next_hint(HintLibrary.Type.PROGRESSIVE) #TODO actually make this work
                self.ctx.output(hint)
                playerInventory.add_hint(hint)
                return 1

            elif menu_line_number == 2:
                hint = self.get_next_hint(HintLibrary.Type.PROGRESSIVE)
                self.ctx.output(hint)
                playerInventory.add_hint(hint)
                return 2

            elif menu_line_number > self.menu_count and menu_line_number <= self.total_count and self.menu[menu_line_number][0] != "SOLD OUT!":

                shoploc: ShopLocation = self.menu[menu_line_number][4]
                isReachable: bool = self.isLocationReachable(shoploc, playerInventory)
                if not isReachable:
                    self.ctx.output("Cannot Purchase, must complete the following logic: {}".format(shoploc.locDetails.webLocationCollection.logicToString()))

                    # refund
                    playerInventory.add(purchase)

                else:
                    playerInventory.add_item_to_client(shoploc.locDetails.id)
                    self.menu[menu_line_number][0] = "SOLD OUT!"
                    self.menu[menu_line_number][2] = 0
                    self.menu[menu_line_number][1] = 0
                    return menu_line_number


            else:
                self.ctx.output("Shop error, refunding tokens")
                playerInventory.add(purchase)

            return menu_line_number

        else:
            self.ctx.output("Cannot afford selected option")

        return None

    def isLocationReachable(self, shopLocation: ShopLocation, playerInventory: PlayerInventory) -> bool:
        return shopLocation.locDetails.webLocationCollection.isAnyReachable(playerInventory.get_item_names_in_inventory())