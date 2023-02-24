from typing import Dict, List, Set, Tuple, TextIO
from BaseClasses import Item, MultiWorld, Location, Tutorial, ItemClassification
from .Items import get_item_names_per_category, item_table, starter_melee_weapons, starter_spells, filler_items
from .Locations import get_locations, EventId
from .Options import is_option_enabled, get_option_value, timespinner_options
from .PreCalculatedWeights import PreCalculatedWeights
from .Regions import create_regions
from worlds.AutoWorld import World, WebWorld

class TimespinnerWebWorld(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Timespinner randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Jarno"]
    )

    setup_de = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["Grrmo", "Fynxes", "Blaze0168"]
    )

    tutorials = [setup, setup_de]


class TimespinnerWorld(World):
    """
    Timespinner is a beautiful metroidvania inspired by classic 90s action-platformers.
    Travel back in time to change fate itself. Join timekeeper Lunais on her quest for revenge against the empire that killed her family.
    """

    option_definitions = timespinner_options
    game = "Timespinner"
    topology_present = True
    data_version = 11
    web = TimespinnerWebWorld()
    required_client_version = (0, 3, 7)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {location.name: location.code for location in get_locations(None, None, None)}
    item_name_groups = get_item_names_per_category()

    locked_locations: List[str]
    location_cache: List[Location]
    precalculated_weights: PreCalculatedWeights

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)

        self.locked_locations = []
        self.location_cache = []
        self.precalculated_weights = PreCalculatedWeights(world, player)

    def generate_early(self):
        # in generate_early the start_inventory isnt copied over to precollected_items yet, so we can still modify the options directly
        if self.multiworld.start_inventory[self.player].value.pop('Meyef', 0) > 0:
            self.multiworld.StartWithMeyef[self.player].value = self.multiworld.StartWithMeyef[self.player].option_true
        if self.multiworld.start_inventory[self.player].value.pop('Talaria Attachment', 0) > 0:
            self.multiworld.QuickSeed[self.player].value = self.multiworld.QuickSeed[self.player].option_true
        if self.multiworld.start_inventory[self.player].value.pop('Jewelry Box', 0) > 0:
            self.multiworld.StartWithJewelryBox[self.player].value = self.multiworld.StartWithJewelryBox[self.player].option_true

    def create_regions(self):
        locations = get_locations(self.multiworld, self.player, self.precalculated_weights)
        create_regions(self.multiworld, self.player, locations, self.location_cache, self.precalculated_weights)

    def create_item(self, name: str) -> Item:
        return create_item_with_correct_settings(self.multiworld, self.player, name)

    def get_filler_item_name(self) -> str:
        trap_chance: int = get_option_value(self.multiworld, self.player, "TrapChance")
        enabled_traps: List[str] = get_option_value(self.multiworld, self.player, "Traps")

        if self.multiworld.random.random() < (trap_chance / 100) and enabled_traps:
            return self.multiworld.random.choice(enabled_traps)
        else:
            return self.multiworld.random.choice(filler_items) 

    def set_rules(self):
        setup_events(self.player, self.locked_locations, self.location_cache)

        final_boss: str
        if is_option_enabled(self.multiworld, self.player, "DadPercent"):
            final_boss = "Killed Emperor"
        else:
            final_boss = "Killed Nightmare"

        self.multiworld.completion_condition[self.player] = lambda state: state.has(final_boss, self.player) 

    def generate_basic(self):
        excluded_items: Set[str] = get_excluded_items(self, self.multiworld, self.player)

        assign_starter_items(self.multiworld, self.player, excluded_items, self.locked_locations)

        pool = get_item_pool(self.multiworld, self.player, excluded_items)

        fill_item_pool_with_dummy_items(self, self.multiworld, self.player, self.locked_locations, self.location_cache, pool)

        self.multiworld.itempool += pool

    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}

        ap_specific_settings: Set[str] = {"RisingTidesOverrides", "TrapChance"}

        for option_name in timespinner_options:
            if (option_name not in ap_specific_settings):
                slot_data[option_name] = get_option_value(self.multiworld, self.player, option_name)

        slot_data["StinkyMaw"] = True
        slot_data["ProgressiveVerticalMovement"] = False
        slot_data["ProgressiveKeycards"] = False
        slot_data["PersonalItems"] = get_personal_items(self.player, self.location_cache)
        slot_data["PyramidKeysGate"] = self.precalculated_weights.pyramid_keys_unlock
        slot_data["PresentGate"] = self.precalculated_weights.present_key_unlock
        slot_data["PastGate"] = self.precalculated_weights.past_key_unlock
        slot_data["TimeGate"] = self.precalculated_weights.time_key_unlock
        slot_data["Basement"] = int(self.precalculated_weights.flood_basement) + \
                                int(self.precalculated_weights.flood_basement_high)
        slot_data["Xarion"] = self.precalculated_weights.flood_xarion
        slot_data["Maw"] = self.precalculated_weights.flood_maw
        slot_data["PyramidShaft"] = self.precalculated_weights.flood_pyramid_shaft
        slot_data["BackPyramid"] = self.precalculated_weights.flood_pyramid_back
        slot_data["CastleMoat"] = self.precalculated_weights.flood_moat
        slot_data["CastleCourtyard"] = self.precalculated_weights.flood_courtyard
        slot_data["LakeDesolation"] = self.precalculated_weights.flood_lake_desolation
        slot_data["DryLakeSerene"] = self.precalculated_weights.dry_lake_serene

        return slot_data

    def write_spoiler_header(self, spoiler_handle: TextIO):
        if is_option_enabled(self.multiworld, self.player, "UnchainedKeys"):
            spoiler_handle.write(f'Modern Warp Beacon unlock:       {self.precalculated_weights.present_key_unlock}\n')
            spoiler_handle.write(f'Timeworn Warp Beacon unlock:     {self.precalculated_weights.past_key_unlock}\n')

            if is_option_enabled(self.multiworld, self.player, "EnterSandman"):
                spoiler_handle.write(f'Mysterious Warp Beacon unlock:   {self.precalculated_weights.time_key_unlock}\n')
        else:
            spoiler_handle.write(f'Twin Pyramid Keys unlock:        {self.precalculated_weights.pyramid_keys_unlock}\n')
       
        if is_option_enabled(self.multiworld, self.player, "RisingTides"):
            flooded_areas: List[str] = []

            if self.precalculated_weights.flood_basement:
                if self.precalculated_weights.flood_basement_high:
                    flooded_areas.append("Castle Basement")
                else:
                    flooded_areas.append("Castle Basement (Savepoint available)")
            if self.precalculated_weights.flood_xarion:
                flooded_areas.append("Xarion (boss)")
            if self.precalculated_weights.flood_maw:
                flooded_areas.append("Maw (caves + boss)")
            if self.precalculated_weights.flood_pyramid_shaft:
                flooded_areas.append("Ancient Pyramid Shaft")
            if self.precalculated_weights.flood_pyramid_back:
                flooded_areas.append("Sandman\\Nightmare (boss)")
            if self.precalculated_weights.flood_moat:
                flooded_areas.append("Castle Ramparts Moat")
            if self.precalculated_weights.flood_courtyard:
                flooded_areas.append("Castle Courtyard")
            if self.precalculated_weights.flood_lake_desolation:
                flooded_areas.append("Lake Desolation")
            if self.precalculated_weights.dry_lake_serene:
                flooded_areas.append("Dry Lake Serene")

            if len(flooded_areas) == 0:
                flooded_areas_string: str = "None"
            else:
                flooded_areas_string: str = ", ".join(flooded_areas)

            spoiler_handle.write(f'Flooded Areas:                   {flooded_areas_string}\n')


def get_excluded_items(self: TimespinnerWorld, world: MultiWorld, player: int) -> Set[str]:
    excluded_items: Set[str] = set()

    if is_option_enabled(world, player, "StartWithJewelryBox"):
        excluded_items.add('Jewelry Box')
    if is_option_enabled(world, player, "StartWithMeyef"):
        excluded_items.add('Meyef')
    if is_option_enabled(world, player, "QuickSeed"):
        excluded_items.add('Talaria Attachment')

    if is_option_enabled(world, player, "UnchainedKeys"):
        excluded_items.add('Twin Pyramid Key')

        if not is_option_enabled(world, player, "EnterSandman"):
            excluded_items.add('Mysterious Warp Beacon')
    else:
        excluded_items.add('Timeworn Warp Beacon')
        excluded_items.add('Modern Warp Beacon')
        excluded_items.add('Mysterious Warp Beacon')

    for item in world.precollected_items[player]:
        if item.name not in self.item_name_groups['UseItem']:
            excluded_items.add(item.name)

    return excluded_items


def assign_starter_items(world: MultiWorld, player: int, excluded_items: Set[str], locked_locations: List[str]):
    non_local_items = world.non_local_items[player].value

    local_starter_melee_weapons = tuple(item for item in starter_melee_weapons if item not in non_local_items)
    if not local_starter_melee_weapons:
        if 'Plasma Orb' in non_local_items:
            raise Exception("Atleast one melee orb must be local")
        else:
            local_starter_melee_weapons = ('Plasma Orb',)

    local_starter_spells = tuple(item for item in starter_spells if item not in non_local_items)
    if not local_starter_spells:
        if 'Lightwall' in non_local_items:
            raise Exception("Atleast one spell must be local")
        else:
            local_starter_spells = ('Lightwall',)

    assign_starter_item(world, player, excluded_items, locked_locations, 'Tutorial: Yo Momma 1', local_starter_melee_weapons)
    assign_starter_item(world, player, excluded_items, locked_locations, 'Tutorial: Yo Momma 2', local_starter_spells)


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


def fill_item_pool_with_dummy_items(self: TimespinnerWorld, world: MultiWorld, player: int, locked_locations: List[str],
                                    location_cache: List[Location], pool: List[Item]):
    for _ in range(len(location_cache) - len(locked_locations) - len(pool)):
        item = create_item_with_correct_settings(world, player, self.get_filler_item_name())
        pool.append(item)


def create_item_with_correct_settings(world: MultiWorld, player: int, name: str) -> Item:
    data = item_table[name]

    if data.useful:
        classification = ItemClassification.useful
    elif data.progression:
        classification = ItemClassification.progression
    elif data.trap:
        classification = ItemClassification.trap
    else:
        classification = ItemClassification.filler
        
    item = Item(name, classification, data.code, player)

    if not item.advancement:
        return item

    if (name == 'Tablet' or name == 'Library Keycard V') and not is_option_enabled(world, player, "DownloadableItems"):
        item.classification = ItemClassification.filler
    elif name == 'Oculus Ring' and not is_option_enabled(world, player, "EyeSpy"):
        item.classification = ItemClassification.filler
    elif (name == 'Kobo' or name == 'Merchant Crow') and not is_option_enabled(world, player, "GyreArchives"):
        item.classification = ItemClassification.filler
    elif name in {"Timeworn Warp Beacon", "Modern Warp Beacon", "Mysterious Warp Beacon"} \
            and not is_option_enabled(world, player, "UnchainedKeys"):
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
