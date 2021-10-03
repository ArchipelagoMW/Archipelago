from typing import Dict, List, Set
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
    data_version = 2

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None)}
    item_name_groups = get_item_names_per_category()

    locked_locations: Dict[int, List[str]] = {}
    pyramid_keys_unlock: Dict[int, str] = {}
    location_cache: Dict[int, List[Location]] = {}

    def generate_early(self):
        self.locked_locations[self.player] = []
        self.location_cache[self.player] = []
        self.pyramid_keys_unlock[self.player] = get_pyramid_keys_unlock(self.world, self.player)


    def create_regions(self):
        create_regions(self.world, self.player, get_locations(self.world, self.player), 
                        self.location_cache[self.player], self.pyramid_keys_unlock[self.player])


    def create_item(self, name: str) -> Item:
        return create_item(name, self.player)


    def set_rules(self):
        setup_events(self.world, self.player, self.locked_locations[self.player])

        self.world.completion_condition[self.player] = lambda state: state.has('Killed Nightmare', self.player)


    def generate_basic(self):
        excluded_items = get_excluded_items_based_on_options(self.world, self.player)

        assign_starter_items(self.world, self.player, excluded_items, self.locked_locations[self.player])

        if not is_option_enabled(self.world, self.player, "QuickSeed") and not is_option_enabled(self.world, self.player, "Inverted"):
            place_first_progression_item(self.world, self.player, excluded_items, self.locked_locations[self.player])

        pool = get_item_pool(self.world, self.player, excluded_items)

        fill_item_pool_with_dummy_items(self.world, self.player, self.locked_locations[self.player], pool)

        self.world.itempool += pool


    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        for option_name in timespinner_options:
            slot_data[option_name] = is_option_enabled(self.world, self.player, option_name)

        slot_data["StinkyMaw"] = True
        slot_data["ProgressiveVerticalMovement"] = False
        slot_data["ProgressiveKeycards"] = False
        slot_data["PyramidKeysGate"] = self.pyramid_keys_unlock[self.player]
        slot_data["PersonalItems"] = get_personal_items(self.player, self.location_cache[self.player])

        return slot_data


def create_item(name: str, player: int) -> Item:
    data = item_table[name]
    return Item(name, data.progression, data.code, player)


def get_excluded_items_based_on_options(world: MultiWorld, player: int) -> List[str]:
    excluded_items: List[str] = []

    if is_option_enabled(world, player, "StartWithJewelryBox"):
        excluded_items.append('Jewelry Box')
    if is_option_enabled(world, player, "StartWithMeyef"):
        excluded_items.append('Meyef')
    if is_option_enabled(world, player, "QuickSeed"):
        excluded_items.append('Talaria Attachment')

    return excluded_items


def assign_starter_items(world: MultiWorld, player: int, excluded_items: List[str], locked_locations: List[str]):
    melee_weapon = world.random.choice(starter_melee_weapons)
    spell = world.random.choice(starter_spells)

    excluded_items.append(melee_weapon)
    excluded_items.append(spell)

    melee_weapon_item = create_item(melee_weapon, player)
    spell_item = create_item(spell, player)

    world.get_location('Yo Momma 1', player).place_locked_item(melee_weapon_item)
    world.get_location('Yo Momma 2', player).place_locked_item(spell_item)

    locked_locations.append('Yo Momma 1')
    locked_locations.append('Yo Momma 2')


def get_item_pool(world: MultiWorld, player: int, excluded_items: List[str]) -> List[Item]:
    pool: List[Item] = []

    for name, data in item_table.items():
        if not name in excluded_items:
            for _ in range(data.count):
                item = update_progressive_state_based_flags(world, player, name, create_item(name, player))
                pool.append(item)

    return pool


def fill_item_pool_with_dummy_items(world: MultiWorld, player: int, locked_locations: List[str], pool: List[Item]):
    for _ in range(len(get_locations(world, player)) - len(locked_locations) - len(pool)):
        item = create_item(world.random.choice(filler_items), player)
        pool.append(item)


def place_first_progression_item(world: MultiWorld, player: int, excluded_items: List[str],
                                 locked_locations: List[str]):
    progression_item = world.random.choice(starter_progression_items)
    location = world.random.choice(starter_progression_locations)

    excluded_items.append(progression_item)
    locked_locations.append(location)

    item = create_item(progression_item, player)

    world.get_location(location, player).place_locked_item(item)


def update_progressive_state_based_flags(world: MultiWorld, player: int, name: str, data: Item) -> Item:
    if not data.advancement:
        return data

    if (name == 'Tablet' or name == 'Library Keycard V') and not is_option_enabled(world, player, "DownloadableItems"):
        data.advancement = False
    if name == 'Oculus Ring' and not is_option_enabled(world, player, "FacebookMode"):
        data.advancement = False

    return data


def setup_events(world: MultiWorld, player: int, locked_locations: List[str]):
    for location in get_locations(world, player):
        if location.code == EventId:
            location = world.get_location(location.name, player)
            item = Item(location.name, True, EventId, player)

            locked_locations.append(location.name)

            location.place_locked_item(item)


def get_personal_items(player: int, locations: List[Location]) -> Dict[int, int]:
    personal_items: Dict[int, int] = {}

    for location in locations:
        if location.address and location.item and location.item.code and location.item.player == player:
            personal_items[location.address] = location.item.code
    
    return personal_items