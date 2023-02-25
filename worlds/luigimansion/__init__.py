from typing import Dict, List, Set, Tuple, TextIO

from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .Items import item_table
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

    locked_locations: List[str]
    location_cache: List[Location]
    # Create list of Regions with randomization, reuse list to filter locations and entrances later. str
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
        "Telephone Room": "No Element",
        "Roof": "No Element",
        "Sealed Room": "No Element",
        "Armory": "No Element",
        "Pipe Room": "No Element"
    }

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

        self.locked_locations = []
        self.location_cache = []
        self.room_to_ghost_table: {}

    def generate_early(self):
        # in generate_early the start_inventory isn't copied over to precollected_items yet, so we can still modify
        # the options directly
        if self.multiworld.Enemizer[self.player]:
            set_ghost_type(self.multiworld, self.ghost_affected_regions)

    def create_regions(self):
        create_regions(self.multiworld, self.player, get_locations(self.multiworld, self.player), self.location_cache)

    def create_item(self, name: str) -> Item:
        item_id: int = self.item_name_to_id[name]

        return Item(name,
                              item_table[name].classification,
                              item_id, player=self.player)

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(filler_items)

    def set_rules(self):
        if self.multiworld.Enemizer[self.player]:
            set_ghost_rules(self.location_cache)

        setup_events(self.player, self.locked_locations, self.location_cache)

    def generate_basic(self):
        excluded_items = get_excluded_items(self, self.multiworld, self.player)

        pool = get_item_pool(self.multiworld, self.player, excluded_items)

        fill_item_pool_with_filler_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache,
                                         pool)

        self.multiworld.itempool += pool

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        for option_name in luigimansion_options:
            slot_data[option_name] = get_option_value(self.multiworld, self.player, option_name)

        slot_data["StinkyMaw"] = True
        slot_data["ProgressiveVerticalMovement"] = False
        slot_data["ProgressiveKeycards"] = False
        slot_data["PersonalItems"] = get_personal_items(self.player, self.location_cache)

        return slot_data

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write('Twin Pyramid Keys unlock:        %s\n' % (self.pyramid_keys_unlock))


def get_excluded_items(self: LuigiMansionWorld, world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    if is_option_enabled(world, player, "StartWithJewelryBox"):
        excluded_items.add('Jewelry Box')
    if is_option_enabled(world, player, "StartWithMeyef"):
        excluded_items.add('Meyef')
    if is_option_enabled(world, player, "QuickSeed"):
        excluded_items.add('Talaria Attachment')

    for item in world.precollected_items[player]:
        if item.name not in self.item_name_groups['UseItem']:
            excluded_items.add(item.name)

    return excluded_items

def assign_starter_item(world: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str],
        location: str, item_list: Tuple[str, ...]):

    item_name = world.random.choice(item_list)

    excluded_items.add(item_name)

    item = create_item_with_correct_settings(world, player, item_name)

    world.get_location(location, player).place_locked_item(item)

    locked_locations.append(location)


def get_item_pool(world: MultiWorld, player: int, excluded_items: Set[str]) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        if name not in excluded_items:
            for _ in range(data.count):
                item = create_item_with_correct_settings(world, player, name)
                pool.append(item)

    return pool


def fill_item_pool_with_filler_items(self: LuigiMansionWorld, world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):

    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = world.create_item(world, player, filler.random.choice())
        pool.append(item)



    if (name == 'Tablet' or name == 'Library Keycard V') and not is_option_enabled(world, player, "DownloadableItems"):
        item.classification = ItemClassification.filler
    elif name == 'Oculus Ring' and not is_option_enabled(world, player, "EyeSpy"):
        item.classification = ItemClassification.filler
    elif (name == 'Kobo' or name == 'Merchant Crow') and not is_option_enabled(world, player, "GyreArchives"):
        item.classification = ItemClassification.filler

    return item


def setup_events(player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address == EventId:
            item = Item(location.name, ItemClassification.progression, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_personal_items(player: int, locations: List[Location]) -> Dict[int, int]:
    personal_items: Dict[int, int] = {}

    for location in locations:
        if location.address and location.item and location.item.code and location.item.player == player:
            personal_items[location.address] = location.item.code

    return personal_items

class LMItem(Item):
    game = "Luigi's Mansion"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(LMItem, self).__init__(
            name,
            item_data.classification,
            item_data.code, player
        )