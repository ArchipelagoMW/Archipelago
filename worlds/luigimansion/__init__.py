from typing import Dict, List, Set, Tuple, TextIO

from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .Items import item_table, filler_items, get_item_names_per_category
from .Locations import get_locations, EventId
from .Rules import set_ghost_type
from .Options import luigimansion_options
from .Regions import create_regions, is_option_enabled, get_option_value
from ..AutoWorld import World, WebWorld


# Incomplete, some function removal required


class LuigiMansionWebWorld(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Luigi's Mansion randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["BootsinSoots"]
    )

    tutorials = [setup]


class LuigiMansionWorld(World):
    """
    Luigi\'s Mansion is an adventure game starring everyone's favorite plumber brother Luigi. 
    Luigi has won a strange mansion but on arriving, he discovers it's full of ghosts!
    """

    option_definitions = luigimansion_options
    game = "Luigi's Mansion"
    topology_present = True
    data_version = 0
    web = LuigiMansionWebWorld()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    item_name_groups = get_item_names_per_category()

    locked_locations: List[str]
    location_cache: List[Location]
    # Create list of Region names with randomization, reuse list to filter locations and entrances later.
    ghost_affected_regions = {
        "Anteroom": "No Element",
        "Wardrobe": "No Element",
        "Laundry Room": "No Element",
        "Hidden Room": "Ice",
        "Mirror Room": "No Element",
        "Storage Room": "No Element",
        "Kitchen": "Ice",
        "1F Bathroom": "No Element",
        "Courtyard": "No Element",
        "Tea Room": "No Element",
        "2F Washroom": "Fire",
        "Projection Room": "No Element",
        "Safari Room": "Water",
        "Cellar": "No Element",
        "Roof": "No Element",
        "Sealed Room": "No Element",
        "Armory": "No Element",
        "Pipe Room": "No Element"
    }

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

        self.locked_locations = []
        self.location_cache = []

    def generate_early(self):
        # in generate_early the start_inventory isn't copied over to precollected_items yet, so we can still modify
        # the options directly
        if self.multiworld.Enemizer[self.player] == True:
            set_ghost_type(self.multiworld, self.ghost_affected_regions)

        if self.multiworld.StartWithBooRadar[self.player] == True:
            self.multiworld.precollected_items[self.player].append(self.create_item("Boo Radar"))

    def create_regions(self):
        create_regions(self.multiworld, self.player, get_locations(self.multiworld, self.player), self.location_cache)

    def create_items(self):
        pool: List[Item] = []
        excluded_items = get_excluded_items(self, self.multiworld, self.player)
        for name, data in item_table.items():
            if name not in excluded_items:
                if data.group != "Trap" or "Filler":
                    for _ in range(data.count):
                        item = self.create_item(name)
                        pool.append(item)

        fill_item_pool_with_filler_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache,
                                         pool)

        self.multiworld.itempool += pool

    def create_item(self, name: str) -> Item:
        item_id: int = self.item_name_to_id[name]

        return Item(name,
                    item_table[name].classification,
                    item_id, self.player)

    def set_rules(self) -> None:
        self.completion_condition[self.player] = lambda state: state.has("Mario's Painting", self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice([item_name for item_name in filler_items])

    def generate_basic(self):
        pass


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        for option_name in luigimansion_options:
            slot_data[option_name] = get_option_value(self.multiworld, self.player, option_name)

        slot_data["StinkyMaw"] = True
        slot_data["ProgressiveVerticalMovement"] = False
        slot_data["ProgressiveKeycards"] = False
        slot_data["PersonalItems"] = get_personal_items(self.player, self.location_cache)

        return slot_data


def get_excluded_items(self: LuigiMansionWorld, world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    if world.Boosanity[self.player] == False:
        excluded_items.add('Boo')

    for item in world.precollected_items[player]:
        if item.name not in self.item_name_groups['UseItem']:
            excluded_items.add(item.name)

    return excluded_items


def fill_item_pool_with_filler_items(self: LuigiMansionWorld, world: MultiWorld, player: int,
                                     locked_locations: List[str],
                                     location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = world.create_item(self.get_filler_item_name(), player)
        pool.append(item)

    return item


def get_personal_items(player: int, locations: List[Location]) -> Dict[int, int]:
    personal_items: Dict[int, int] = {}

    for location in locations:
        if location.address and location.item and location.item.code and location.item.player == player:
            personal_items[location.address] = location.item.code

    return personal_items



