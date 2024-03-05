import typing
import settings
from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from .Locations import all_locations, location_table, bowsers, bowsersMini, event, hidden, coins
from .Options import MLSSOptions
from .Items import MLSSItem, itemList, item_frequencies, item_table
from .Names.LocationName import LocationName
from .Client import MLSSClient
from .Regions import create_regions, connect_regions
from .Rom import MLSSDeltaPatch, Rom
from .Rules import set_rules


class MLSSWebWorld(WebWorld):
    theme = 'partyTime'
    bug_report_page = "https://github.com/jamesbrq/ArchipelagoMLSS/issues"
    tutorials = [
        Tutorial(
            tutorial_name='Setup Guide',
            description='A guide to setting up Mario & Luigi: Superstar Saga for Archipelago.',
            language='English',
            file_name='setup_en.md',
            link='setup/en',
            authors=['jamesbrq']
        )
    ]


class MLSSSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the MLSS US rom"""
        copy_to = "Mario & Luigi - Superstar Saga (U).gba"
        description = "MLSS ROM File"
        md5s = ["4b1a5897d89d9e74ec7f630eefdfd435"]

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: bool = True


class MLSSWorld(World):
    """
    Adventure with Mario and Luigi together in the Beanbean Kingdom
    to stop the evil cackletta and retrieve the Beanstar.
    """
    game = "Mario & Luigi Superstar Saga"
    web = MLSSWebWorld()
    data_version = 1
    options_dataclass = MLSSOptions
    options: MLSSOptions
    settings: typing.ClassVar[MLSSSettings]
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    required_client_version = (0, 4, 4)

    excluded_locations = []

    def generate_early(self) -> None:
        self.excluded_locations = []
        if self.options.chuckle_beans == 0:
            self.excluded_locations += [location.name for location in all_locations if "Digspot" in location.name]
        if self.options.castle_skip:
            self.excluded_locations += [location.name for location in all_locations if "Bowser" in location.name]
        if self.options.chuckle_beans == 1:
            self.excluded_locations = [location.name for location in all_locations if location.id in hidden]
        if self.options.skip_minecart:
            self.excluded_locations += [LocationName.HoohooMountainBaseMinecartCaveDigspot]
        if self.options.disable_surf:
            self.excluded_locations += [LocationName.SurfMinigame]
        if self.options.harhalls_pants:
            self.excluded_locations += [LocationName.HarhallsPants]
        if not self.options.coins:
            self.excluded_locations += [location.name for location in all_locations if location in coins]

    def create_regions(self) -> None:
        create_regions(self, self.excluded_locations)
        connect_regions(self)

    def fill_slot_data(self) -> dict:
        return {
            "CastleSkip": self.options.castle_skip.value,
            "SkipMinecart": self.options.skip_minecart.value,
            "DisableSurf": self.options.disable_surf.value,
            "HarhallsPants": self.options.harhalls_pants.value,
            "ChuckleBeans": self.options.chuckle_beans.value,
            "DifficultLogic": self.options.difficult_logic.value,
            "Coins": self.options.coins.value
        }

    def generate_basic(self) -> None:
        item = self.create_item("Mushroom")
        self.multiworld.get_location(LocationName.ShopStartingFlag1, self.player).place_locked_item(item)
        item = self.create_item("Syrup")
        self.multiworld.get_location(LocationName.ShopStartingFlag2, self.player).place_locked_item(item)
        item = self.create_item("1-UP Mushroom")
        self.multiworld.get_location(LocationName.ShopStartingFlag3, self.player).place_locked_item(item)
        item = self.create_item("Hoo Bean")
        self.multiworld.get_location(LocationName.PantsShopStartingFlag1, self.player).place_locked_item(item)
        item = self.create_item("Chuckle Bean")
        self.multiworld.get_location(LocationName.PantsShopStartingFlag2, self.player).place_locked_item(item)
        item = self.create_item("Dragohoho Defeated")
        self.multiworld.get_location("Dragohoho", self.player).place_locked_item(item)
        item = self.create_item("Queen Bean Defeated")
        self.multiworld.get_location("Queen Bean", self.player).place_locked_item(item)
        item = self.create_item("Chuckolator Defeated")
        self.multiworld.get_location("Chuckolator", self.player).place_locked_item(item)
        item = self.create_item("Oasis Access")
        self.multiworld.get_location("Oasis", self.player).place_locked_item(item)
        item = self.create_item("Mom Piranha Defeated")
        self.multiworld.get_location("Mom Piranha", self.player).place_locked_item(item)
        item = self.create_item("Entered Fungitown")
        self.multiworld.get_location("Fungitown", self.player).place_locked_item(item)
        item = self.create_item("Beanstar Complete")
        self.multiworld.get_location("Beanstar", self.player).place_locked_item(item)
        item = self.create_item("Jojora Defeated")
        self.multiworld.get_location("Jojora", self.player).place_locked_item(item)
        item = self.create_item("Birdo Defeated")
        self.multiworld.get_location("Birdo", self.player).place_locked_item(item)

    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = []
        precollected = [item for item in itemList if item in self.multiworld.precollected_items]
        for item in itemList:
            if item.progression != ItemClassification.filler and item.progression != ItemClassification.skip_balancing and item not in precollected:
                freq = item_frequencies.get(item.itemName, 1)
                if freq is None:
                    freq = 1
                if self.options.harhalls_pants and "Harhall's" in item.itemName:
                    continue
                required_items += [item.itemName for _ in range(freq)]

        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        # Then, get a random amount of fillers until we have as many items as we have locations
        filler_items = []
        for item in itemList:
            if item.progression == ItemClassification.skip_balancing:
                continue
            if item.progression == ItemClassification.filler:
                if item.itemName == "5 Coins" and not self.options.coins:
                    continue
                freq = item_frequencies.get(item.itemName)
                if self.options.chuckle_beans == 0:
                    if item.itemName == "Chuckle Bean":
                        continue
                if self.options.chuckle_beans == 1:
                    if item.itemName == "Chuckle Bean":
                        freq -= 59
                if freq is None:
                    freq = 1
                filler_items += [item.itemName for _ in range(freq)]

        remaining = len(all_locations) - len(required_items) - len(event) - 5
        if self.options.castle_skip:
            remaining -= (len(bowsers) + len(bowsersMini) - (5 if self.options.chuckle_beans == 0 else 0))
        if self.options.skip_minecart and self.options.chuckle_beans == 2:
            remaining -= 1
        if self.options.disable_surf:
            remaining -= 1
        if self.options.harhalls_pants:
            remaining -= 1
        if self.options.chuckle_beans == 0:
            remaining -= 192
        if self.options.chuckle_beans == 1:
            remaining -= 59
        if not self.options.coins:
            remaining -= len(coins)
        for i in range(remaining):
            filler_item_name = self.multiworld.random.choice(filler_items)
            item = self.create_item(filler_item_name)
            self.multiworld.itempool.append(item)
            filler_items.remove(filler_item_name)

    def set_rules(self) -> None:
        set_rules(self, self.excluded_locations)
        self.multiworld.completion_condition[self.player] = \
            lambda state: state.can_reach("PostJokes", "Region", self.player)

    def create_item(self, name: str) -> MLSSItem:
        item = item_table[name]
        return MLSSItem(item.itemName, item.progression, item.code, self.player)

    def generate_output(self, output_directory: str) -> None:
        rom = Rom(self)

        for location_name in location_table.keys():
            if (self.options.skip_minecart and "Minecart" in location_name and "After" not in location_name) or (self.options.castle_skip and "Bowser" in location_name) or (self.options.disable_surf and "Surf Minigame" in location_name) or (self.options.harhalls_pants and "Harhall's" in location_name):
                continue
            if (self.options.chuckle_beans == 0 and "Digspot" in location_name) or (self.options.chuckle_beans == 1 and location_table[location_name] in hidden):
                continue
            if not self.options.coins and "Coin" in location_name:
                continue
            location = self.multiworld.get_location(location_name, self.player)
            if location in self.multiworld.get_region("Event", self.player).locations:
                continue
            item = location.item
            address = [address for address in all_locations if address.name == location.name]
            rom.item_inject(location.address, address[0].itemType, item)
            if "Shop" in location_name and "Coffee" not in location_name and item.player != self.player:
                rom.desc_inject(location, item)
        rom.patch_options()

        rom.close(output_directory)
