from worlds.AutoWorld import World, WebWorld
from BaseClasses import Tutorial, Item, Location, Region, ItemClassification
from .options import PeaksOfYoreOptions
from .data import full_item_table, full_location_table
from .items import PeaksOfYoreItem
from .locations import get_locations, PeaksOfYoreLocation


class PeaksOfWeb(WebWorld):
    theme = "stone"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Peaks of Yore Mod.",
        "English",
        "setup_en.md",
        "setup/en",
        ["c0der23"]
    )]


class PeaksOfWorld(World):
    """A game about climbing mountains!"""
    game = "Peaks of Yore"
    options_dataclass = PeaksOfYoreOptions
    options: PeaksOfYoreOptions
    web = PeaksOfWeb()
    item_name_to_id = {item["name"]: item["id"] for item in full_item_table}
    location_name_to_id = {location["name"]: location["id"] for location in full_location_table}
    topology_present = True

    def create_item(self, name: str) -> Item:
        return PeaksOfYoreItem(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        fundamentals_region = Region("Fundamentals", self.player, self.multiworld)
        fundamentals_region.add_locations(get_locations(0), PeaksOfYoreLocation)
        self.multiworld.regions.append(fundamentals_region)
        menu_region.connect(fundamentals_region)
        menu_region.add_exits({"Fundamentals": "fundamentals_book"},
                              {"Fundamentals": lambda state: state.has("Fundamentals Book", self.player)})

        intermediate_region = Region("Intermediate", self.player, self.multiworld)
        fundamentals_region.add_locations(get_locations(1), PeaksOfYoreLocation)
        self.multiworld.regions.append(intermediate_region)
        menu_region.connect(intermediate_region)
        menu_region.add_exits({"Intermediate": "intermediate_book"},
                              {"Intermediate": lambda state: state.has("Intermediate Book", self.player)})

        advanced_region = Region("Advanced", self.player, self.multiworld)
        fundamentals_region.add_locations(get_locations(2), PeaksOfYoreLocation)
        self.multiworld.regions.append(advanced_region)
        menu_region.connect(advanced_region)
        menu_region.add_exits({"Advanced": "advanced_book"},
                              {"Advanced": lambda state: state.has("Advanced Book", self.player)})

        expert_region = Region("Expert", self.player, self.multiworld)
        fundamentals_region.add_locations(get_locations(3), PeaksOfYoreLocation)
        self.multiworld.regions.append(expert_region)
        menu_region.connect(expert_region)
        menu_region.add_exits({"Expert": "expert_book"},
                              {"Expert": lambda state: state.has("Expert Book", self.player)})

    def create_items(self) -> None:
        for item in full_item_table:
            self.multiworld.itempool.append(self.create_item(item["name"]))
        self.multiworld.itempool += [self.create_item("Extra Rope") for _ in range(20)]
