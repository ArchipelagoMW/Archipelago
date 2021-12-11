from typing import Dict, List, Set, TextIO
from BaseClasses import Item, MultiWorld, Location
from ..AutoWorld import World
from .LogicMixin import TimespinnerLogic
from .Items import get_item_names_per_category, item_table, starter_melee_weapons, starter_spells, starter_progression_items, filler_items
from .Locations import get_locations, starter_progression_locations, EventId
from .Regions import create_regions
from .Options import is_option_enabled, timespinner_options
from .PyramidKeys import get_pyramid_keys_unlock

class TimespinnerWorld(World):
    """
    Timespinner is a beautiful metroidvania inspired by classic 90s action-platformers.
    Travel back in time to change fate itself. Join timekeeper Lunais on her quest for revenge against the empire that killed her family.
    """

    options = timespinner_options
    game = "Timespinner"
    topology_present = True
    remote_items = False
    data_version = 4

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    item_name_groups = get_item_names_per_category()

    locked_locations: List[str]
    pyramid_keys_unlock: str
    location_cache: List[Location]

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

        self.locked_locations = []
        self.location_cache = []
        self.pyramid_keys_unlock = get_pyramid_keys_unlock(world, player)

    # for item in self.world.precollected_items[self.player]:
    # if item.name in self.remove_from_start_inventory:

    def generate_early(self):
        if self.world.start_inventory[self.player].value.pop('Meyef', 0) > 0:
            self.world.StartWithMeyef[self.player].value = self.world.StartWithMeyef[self.player].option_true
        if self.world.start_inventory[self.player].value.pop('Talaria Attachment', 0) > 0:
            self.world.QuickSeed[self.player].value = self.world.QuickSeed[self.player].option_true
        if self.world.start_inventory[self.player].value.pop('Jewelry Box', 0) > 0:
            self.world.StartWithJewelryBox[self.player].value = self.world.StartWithJewelryBox[self.player].option_true


    def create_regions(self):
        create_regions(self.world, self.player, get_locations(self.world, self.player), 
                        self.location_cache, self.pyramid_keys_unlock)


    def create_item(self, name: str) -> Item:
        return create_item_with_correct_settings(self.world, self.player, name)


    def set_rules(self):
        setup_events(self.world, self.player, self.locked_locations, self.location_cache)

        self.world.completion_condition[self.player] = lambda state: state.has('Killed Nightmare', self.player)


    def generate_basic(self):
        excluded_items = get_excluded_items_based_on_options(self.world, self.player)

        assign_starter_items(self.world, self.player, excluded_items, self.locked_locations)

        if not is_option_enabled(self.world, self.player, "QuickSeed") and not is_option_enabled(self.world, self.player, "Inverted"):
            place_first_progression_item(self.world, self.player, excluded_items, self.locked_locations)

        pool = get_item_pool(self.world, self.player, excluded_items)

        fill_item_pool_with_dummy_items(self.world, self.player, self.locked_locations, self.location_cache, pool)

        self.world.itempool += pool


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        for option_name in timespinner_options:
            slot_data[option_name] = is_option_enabled(self.world, self.player, option_name)

        slot_data["StinkyMaw"] = True
        slot_data["ProgressiveVerticalMovement"] = False
        slot_data["ProgressiveKeycards"] = False
        slot_data["PyramidKeysGate"] = self.pyramid_keys_unlock
        slot_data["PersonalItems"] = get_personal_items(self.player, self.location_cache)

        return slot_data
        

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write('Twin Pyramid Keys unlock:        %s\n' % (self.pyramid_keys_unlock))


def get_excluded_items_based_on_options(world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    if is_option_enabled(world, player, "StartWithJewelryBox"):
        excluded_items.add('Jewelry Box')
    if is_option_enabled(world, player, "StartWithMeyef"):
        excluded_items.add('Meyef')
    if is_option_enabled(world, player, "QuickSeed"):
        excluded_items.add('Talaria Attachment')
    
    return excluded_items


def assign_starter_items(world: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]):
    melee_weapon = world.random.choice(starter_melee_weapons)
    spell = world.random.choice(starter_spells)

    excluded_items.add(melee_weapon)
    excluded_items.add(spell)

    melee_weapon_item = create_item_with_correct_settings(world, player, melee_weapon)
    spell_item = create_item_with_correct_settings(world, player, spell)

    world.get_location('Yo Momma 1', player).place_locked_item(melee_weapon_item)
    world.get_location('Yo Momma 2', player).place_locked_item(spell_item)

    locked_locations.append('Yo Momma 1')
    locked_locations.append('Yo Momma 2')


def get_item_pool(world: MultiWorld, player: int, excluded_items: Set[str]) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        if not name in excluded_items:
            for _ in range(data.count):
                item = create_item_with_correct_settings(world, player, name)
                pool.append(item)

    return pool


def fill_item_pool_with_dummy_items(world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(world, player, world.random.choice(filler_items))
        pool.append(item)


def place_first_progression_item(world: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]):
    progression_item = world.random.choice(starter_progression_items)
    location = world.random.choice(starter_progression_locations)

    excluded_items.add(progression_item)
    locked_locations.append(location)

    item = create_item_with_correct_settings(world, player, progression_item)

    world.get_location(location, player).place_locked_item(item)


def create_item_with_correct_settings(world: MultiWorld, player: int, name: str) -> Item:
    data = item_table[name]

    item = Item(name, data.progression, data.code, player)
    item.never_exclude = data.never_exclude

    if not item.advancement:
        return item

    if (name == 'Tablet' or name == 'Library Keycard V') and not is_option_enabled(world, player, "DownloadableItems"):
        item.advancement = False
    elif name == 'Oculus Ring' and not is_option_enabled(world, player, "FacebookMode"):
        item.advancement = False
    elif (name == 'Kobo' or name == 'Merchant Crow') and not is_option_enabled(world, player, "GyreArchives"):
        item.advancement = False

    return item


def setup_events(world: MultiWorld, player: int, locked_locations: List[str], location_cache: List[Location]):
    for location in location_cache:
        if location.address == EventId:
            item = Item(location.name, True, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_personal_items(player: int, locations: List[Location]) -> Dict[int, int]:
    personal_items: Dict[int, int] = {}

    for location in locations:
        if location.address and location.item and location.item.code and location.item.player == player:
            personal_items[location.address] = location.item.code
    
    return personal_items