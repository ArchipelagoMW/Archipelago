import os
import pkgutil
import typing
import settings
from BaseClasses import Tutorial, ItemClassification
from worlds.AutoWorld import WebWorld, World
from typing import Set, Dict, Any
from .Locations import all_locations, location_table, bowsers, bowsersMini, hidden, coins
from .Options import MLSSOptions
from .Items import MLSSItem, itemList, item_frequencies, item_table
from .Names.LocationName import LocationName
from .Client import MLSSClient
from .Regions import create_regions, connect_regions
from .Rom import MLSSProcedurePatch, write_tokens
from .Rules import set_rules


class MLSSWebWorld(WebWorld):
    theme = "partyTime"
    bug_report_page = "https://github.com/jamesbrq/ArchipelagoMLSS/issues"
    tutorials = [
        Tutorial(
            tutorial_name="Setup Guide",
            description="A guide to setting up Mario & Luigi: Superstar Saga for Archipelago.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["jamesbrq"],
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
    to stop the evil Cackletta and retrieve the Beanstar.
    """

    game = "Mario & Luigi Superstar Saga"
    web = MLSSWebWorld()
    options_dataclass = MLSSOptions
    options: MLSSOptions
    settings: typing.ClassVar[MLSSSettings]
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {loc_data.name: loc_data.id for loc_data in all_locations}
    required_client_version = (0, 5, 0)

    disabled_locations: Set[str]

    def generate_early(self) -> None:
        self.disabled_locations = set()
        if self.options.skip_minecart:
            self.disabled_locations.update([LocationName.HoohooMountainBaseMinecartCaveDigspot])
        if self.options.disable_surf:
            self.disabled_locations.update([LocationName.SurfMinigame])
        if self.options.disable_harhalls_pants:
            self.disabled_locations.update([LocationName.HarhallsPants])
        if self.options.chuckle_beans == 0:
            self.disabled_locations.update([location.name for location in all_locations if "Digspot" in location.name])
        if self.options.chuckle_beans == 1:
            self.disabled_locations.update([location.name for location in all_locations if location.id in hidden])
        if self.options.castle_skip:
            self.disabled_locations.update([location.name for location in bowsers + bowsersMini])
        if not self.options.coins:
            self.disabled_locations.update([location.name for location in coins])

    def create_regions(self) -> None:
        create_regions(self)
        connect_regions(self)

        item = self.create_item("Mushroom")
        self.get_location(LocationName.ShopStartingFlag1).place_locked_item(item)
        item = self.create_item("Syrup")
        self.get_location(LocationName.ShopStartingFlag2).place_locked_item(item)
        item = self.create_item("1-UP Mushroom")
        self.get_location(LocationName.ShopStartingFlag3).place_locked_item(item)
        item = self.create_item("Hoo Bean")
        self.get_location(LocationName.PantsShopStartingFlag1).place_locked_item(item)
        item = self.create_item("Chuckle Bean")
        self.get_location(LocationName.PantsShopStartingFlag2).place_locked_item(item)
        item = MLSSItem("Victory", ItemClassification.progression, None, self.player)
        self.get_location("Cackletta's Soul").place_locked_item(item)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            "CastleSkip": self.options.castle_skip.value,
            "SkipMinecart": self.options.skip_minecart.value,
            "DisableSurf": self.options.disable_surf.value,
            "HarhallsPants": self.options.disable_harhalls_pants.value,
            "ChuckleBeans": self.options.chuckle_beans.value,
            "DifficultLogic": self.options.difficult_logic.value,
            "Coins": self.options.coins.value,
        }

    def create_items(self) -> None:
        # First add in all progression and useful items
        required_items = []
        precollected = [item for item in itemList if item in self.multiworld.precollected_items]
        for item in itemList:
            if item.classification != ItemClassification.filler and item.classification != ItemClassification.skip_balancing:
                freq = item_frequencies.get(item.itemName, 1)
                if item in precollected:
                    freq = max(freq - precollected.count(item), 0)
                if self.options.disable_harhalls_pants and "Harhall's" in item.itemName:
                    continue
                required_items += [item.itemName for _ in range(freq)]

        for itemName in required_items:
            self.multiworld.itempool.append(self.create_item(itemName))

        # Then, create our list of filler items
        filler_items = []
        for item in itemList:
            if item.classification != ItemClassification.filler:
                continue
            if item.itemName == "5 Coins" and not self.options.coins:
                continue
            freq = item_frequencies.get(item.itemName, 1)
            if self.options.chuckle_beans == 0:
                if item.itemName == "Chuckle Bean":
                    continue
            if self.options.chuckle_beans == 1:
                if item.itemName == "Chuckle Bean":
                    freq -= 59
            filler_items += [item.itemName for _ in range(freq)]

        # And finally take as many fillers as we need to have the same amount of items and locations.
        remaining = len(all_locations) - len(required_items) - len(self.disabled_locations) - 5

        self.multiworld.itempool += [
            self.create_item(filler_item_name) for filler_item_name in self.random.sample(filler_items, remaining)
        ]

    def set_rules(self) -> None:
        set_rules(self, self.disabled_locations)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

    def create_item(self, name: str) -> MLSSItem:
        item = item_table[name]
        return MLSSItem(item.itemName, item.classification, item.code, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(filter(lambda item: item.classification == ItemClassification.filler, itemList))).itemName

    def generate_output(self, output_directory: str) -> None:
        patch = MLSSProcedurePatch(player=self.player, player_name=self.multiworld.player_name[self.player])
        patch.write_file("base_patch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff"))
        write_tokens(self, patch)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}" f"{patch.patch_file_ending}"
        )
        patch.write(rom_path)
