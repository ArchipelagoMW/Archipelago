from typing import Dict, Any, Set, List

from BaseClasses import Item, Location, Region, Entrance, ItemClassification, Tutorial, RegionType
from Options import Accessibility
from worlds.AutoWorld import World, WebWorld
from .Constants import NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS, JUNK, ALWAYS_LOCATIONS, SEALS, ALL_ITEMS
from .Options import messenger_options
from .Regions import REGIONS, REGION_CONNECTIONS
from .Rules import MessengerRules


class MessengerWeb(WebWorld):
    theme = "ocean"

    bug_report_page = "https://github.com/minous27/TheMessengerRandomizerMod/issues"

    tut_en = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up The Messenger randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["alwaysintreble"]
    )

    tutorials = [tut_en]


class MessengerWorld(World):
    game = "The Messenger"

    item_name_groups = {
        "Notes": NOTES,
        "Keys": NOTES,
        "Crest": {"Sun Crest", "Moon Crest"},
        "Phobe": PHOBEKINS,
        "Phobekin": PHOBEKINS,
        "Shuriken": {"Windmill Shuriken"},
    }

    option_definitions = messenger_options

    base_offset = 0xADD_000
    item_name_to_id = {item: item_id
                       for item_id, item in enumerate(ALL_ITEMS, base_offset)}
    location_name_to_id = {location: location_id
                           for location_id, location in enumerate([*ALWAYS_LOCATIONS, *SEALS], base_offset)}

    data_version = 0

    web = MessengerWeb()

    rules: MessengerRules

    def generate_early(self) -> None:
        self.rules = MessengerRules(self.player)

    def create_regions(self) -> None:
        class MessengerRegion(Region):
            def __init__(self, name: str, world: MessengerWorld):
                super().__init__(name, RegionType.Generic, name, world.player, world.multiworld)
                self.world = world
                self.add_locations()
                world.multiworld.regions.append(self)

            def add_locations(self) -> None:
                for loc in REGIONS[self.name]:
                    self.locations.append(self.world.create_location(loc, self))
                if self.multiworld.shuffle_seals[self.player]:
                    seal_locs = {loc for loc in SEALS if loc.startswith(self.name)}
                    for seal_loc in seal_locs:
                        self.locations.append(self.world.create_location(seal_loc, self))

            def add_exits(self, exits: Set[str]) -> None:
                for exit in exits:
                    ret = Entrance(self.player, exit, self)
                    if exit in self.world.rules.region_rules:
                        ret.access_rule = self.world.rules.region_rules[exit]
                    self.exits.append(ret)
                    ret.connect(self.multiworld.get_region(exit, self.player))

        for region in REGIONS:
            MessengerRegion(region, self)

        for reg_name, exits in REGION_CONNECTIONS.items():
            region = self.multiworld.get_region(reg_name, self.player)
            if type(region) is not MessengerRegion:
                raise KeyError(f"Tried to get {region} for player {self.player} but isn't of type {MessengerRegion}")
            region.add_exits(exits)

    def create_items(self) -> None:
        itempool = []
        for item in self.item_name_to_id:
            if item != "Time Shard":  # if we create this with power seal shuffling off we'll have too many items
                itempool.append(self.create_item(item))
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self) -> None:
        if self.multiworld.enable_logic[self.player]:
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Rescue Phantom", self.player)
        else:
            self.multiworld.accessibility[self.player].value = Accessibility.option_minimal

    def fill_slot_data(self) -> Dict[str, Any]:
        locations: Dict[int, List[str]] = {}
        for loc in self.multiworld.get_filled_locations(self.player):
            if loc.item.code:
                locations[loc.address] = [loc.item.name, self.multiworld.player_name[loc.item.player]]

        return {
            "deathlink": bool(self.multiworld.death_link[self.player].value),
            "locations": locations,
            "settings": {"Difficulty": "Basic" if not self.multiworld.shuffle_seals[self.player] else "Advanced"}
        }

    def get_filler_item_name(self) -> str:
        return "Time Shard"

    def create_item(self, name: str) -> "Item":
        class MessengerItem(Item):
            game = "The Messenger"

            def __init__(self, name: str, world: MessengerWorld):
                item_class = ItemClassification.filler
                if name in {*NOTES, *PROG_ITEMS, *PHOBEKINS}:
                    item_class = ItemClassification.progression
                elif name in USEFUL_ITEMS:
                    item_class = ItemClassification.useful
                item_id = world.item_name_to_id[name] if name in world.item_name_to_id else None
                if item_id is None:
                    item_class = ItemClassification.progression
                super().__init__(name, item_class, item_id, world.player)

        return MessengerItem(name, self)

    def create_region(self, name: str) -> Region:
        current_region = Region(name, RegionType.Generic, name, self.player, self.multiworld)
        for loc in REGIONS[name]:
            current_region.locations.append(self.create_location(loc, current_region))
        return current_region

    def create_location(self, name: str, parent: Region) -> "Location":
        class MessengerLocation(Location):
            game = "The Messenger"

        loc_id = self.location_name_to_id[name] if name in self.location_name_to_id else None
        loc = MessengerLocation(self.player, name, loc_id, parent)
        if name in self.rules.location_rules:
            loc.access_rule = self.rules.location_rules[name]
        if loc_id is None:
            loc.place_locked_item(self.create_item(name))
        return loc

