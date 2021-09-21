import typing

from BaseClasses import Item, MultiWorld, Region, Location, Entrance
from ..AutoWorld import World
from .Items import ItemData, item_table, starter_melee_weapons, starter_spells, starter_progression_items, filler_items
from .Locations import location_table, downloadable_items, starter_progression_locations
from .Regions import create_regions
from .Rules import set_rules, present_teleportation_gates, past_teleportation_gates
from .Options import timespinner_options, is_option_enabled

class TimespinnerWorld(World):
    options = timespinner_options
    game = "Timespinner"
    topology_present = False
    data_version = 1

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.code for name, data in { **location_table, **downloadable_items }.items()} 

    def _get_slot_data(self):
        return {
            "StartWithJewelryBox": self.world.StartWithJewelryBox[self.player],
            "DownloadableItems": self.world.DownloadableItems[self.player],
            "FacebookMode": self.world.FacebookMode[self.player],
            "StartWithMeyef": self.world.StartWithMeyef[self.player],
            "QuickSeed": self.world.QuickSeed[self.player],
            "SpecificKeycards": self.world.SpecificKeycards[self.player],
            "Inverted": self.world.Inverted[self.player]
        }
   
    def generate_early(self):
        self.world.timespinner_pyramid_keys_unlock = get_pyramid_unlock(self.world, self.player)
        self.item_name_groups = get_item_name_groups()

    def generate_basic(self):
        excluded_items = get_excluded_items_based_on_options(self.world, self.player)
        locked_locations = []

        assign_starter_items(self.world, self.player, excluded_items, locked_locations)

        if not is_option_enabled(self.world, self.player, "QuickSeed") or not is_option_enabled(self.world, self.player, "Inverted"):
            place_first_progression_item(self.world, self.player, excluded_items, locked_locations)

        pool = get_item_pool(self.world, self.player, excluded_items)
        pool = fill_item_pool_with_dummy_items(self.world, self.player, locked_locations, pool)

        self.world.itempool += pool

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        return Item(name, item_data.progression, item_data.code, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self) -> typing.Dict:
        slot_data = self._get_slot_data()

        for option_name in timespinner_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = int(option.value)

        slot_data["StinkyMaw"] = 1
        slot_data["ProgressiveVerticalMovement"] = 0
        slot_data["ProgressiveKeycards"] = 0
        slot_data["PyramidKeysGate"] = self.world.timespinner_pyramid_keys_unlock

        return slot_data

class TimespinnerWorldLocation(Location):
    game: str = "Timespinner"

    def __init__(self, player: int, name: str, id=None, parentRegion=None):
        super(TimespinnerWorldLocation, self).__init__(player, name, id, parentRegion)
        if id is None:
            self.event = True
            self.locked = True

class TimespinnerWorldItem(Item):
    game = "Timespinner"

    def __init__(self, name: str, player: int = None):
        item_data = item_table[name]
        super(TimespinnerWorldItem, self).__init__(name, item_data.progression, item_data.code, player)

def get_excluded_items_based_on_options(world: MultiWorld, player: int) -> typing.List[str]:
    excluded_items = []

    if is_option_enabled(world, player, "StartWithJewelryBox"):
        excluded_items.append('Jewelry Box')
    if is_option_enabled(world, player, "StartWithMeyef"):
        excluded_items.append('Meyef')
    if is_option_enabled(world, player, "QuickSeed"):
        excluded_items.append('Talaria Attachment')
    
    return excluded_items

def assign_starter_items(world: MultiWorld, player: int, excluded_items: typing.List[str], locked_locations: typing.List[str]):
    world.random.shuffle(starter_melee_weapons)
    world.random.shuffle(starter_spells)

    melee_weapon = starter_melee_weapons.pop()
    spell = starter_spells.pop()

    excluded_items.append(melee_weapon)
    excluded_items.append(spell)

    melee_weapon_item = TimespinnerWorldItem(melee_weapon, player)
    spell_item = TimespinnerWorldItem(spell, player)
    
    world.get_location('Yo Momma 1', player).place_locked_item(melee_weapon_item)
    world.get_location('Yo Momma 2', player).place_locked_item(spell_item)

    locked_locations.append('Yo Momma 1')
    locked_locations.append('Yo Momma 2')

def get_item_pool(world: MultiWorld, player: int, excluded_items: typing.List[str]) -> typing.List[TimespinnerWorldItem]:
    pool = []

    for name, data in item_table.items():
        if not name in excluded_items:
            for _ in range(data.count):
                item = update_progressive_state_based_flags(world, player, name, TimespinnerWorldItem(name, player))
                pool.append(item)

    return pool

def fill_item_pool_with_dummy_items(world: MultiWorld, player: int, locked_locations: typing.List[str], pool: typing.List[TimespinnerWorldItem]) -> typing.List[TimespinnerWorldItem]:
    for _ in range(get_number_of_locations(world, player) - len(locked_locations) - len(pool)):
        world.random.shuffle(filler_items)

        item_name = filler_items.pop()
        filler_items.append(item_name)

        item = TimespinnerWorldItem(item_name, player)
        pool.append(item)

    return pool

def place_first_progression_item(world: MultiWorld, player: int, excluded_items: typing.List[str], locked_locations: typing.List[str]):
    world.random.shuffle(starter_progression_items)
    world.random.shuffle(starter_progression_locations)

    progression_item = starter_progression_items.pop()
    location = starter_progression_locations.pop()

    excluded_items.append(progression_item)
    locked_locations.append(location)
    
    item = TimespinnerWorldItem(progression_item, player)

    world.get_location(location, player).place_locked_item(item)
 
def update_progressive_state_based_flags(world: MultiWorld, player: int, name: str, data: TimespinnerWorldItem) -> TimespinnerWorldItem:
    if not data.advancement:
        return data

    if (name == 'Tablet' or name == 'Library Keycard V') and not is_option_enabled(world, player, "DownloadableItems"):
        data.advancement = False
    if name == 'Oculus Ring' and not is_option_enabled(world, player, "FacebookMode"):
        data.advancement = False

    return data

def get_number_of_locations(world: MultiWorld, player: int) -> int:
    if is_option_enabled(world, player, "DownloadableItems"):
        return len({**location_table, **downloadable_items })
    else:
        return len(location_table)

def get_pyramid_unlock(world: MultiWorld, player: int) -> str:
    gates = []

    if is_option_enabled(world, player, "Inverted"):
        gates = present_teleportation_gates
    else:
        gates = [*past_teleportation_gates, *present_teleportation_gates]

    world.random.shuffle(gates)

    return gates.pop()

def create_region(world: MultiWorld, player: int, name: str, exits=None) -> Region:
    region = Region(name, None, name, player)
    region.world = world

    for location, data in location_table.items():
        if data.region == name:
            location = TimespinnerWorldLocation(player, location, data.code, region)
            region.locations.append(location)

    if exits:
        for exit in exits:
            region.exits.append(Entrance(player, exit, region))

    return region

def get_item_name_groups() -> typing.Dict[str, typing.List[str]]:
    groups: typing.Dict[str, typing.List[str]] = {}

    for name, data in item_table.items():
        if not data.category in groups:
            groups[data.category] = []

        groups[data.category].append(name)

    return groups