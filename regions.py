from __future__ import annotations

import itertools
from typing import Iterable, Sequence, Set, TYPE_CHECKING

from BaseClasses import Region, Entrance

from . import rules
from .locations import WL4Location, get_level_location_data
from .types import AccessRule, Passage
from .options import Difficulty, OpenDoors

if TYPE_CHECKING:
    from . import WL4World

# itertools.pairwise from Python 3.10
def pairwise(iterable):
    try:
        return itertools.pairwise(iterable)
    except AttributeError:
        # https://docs.python.org/3.9/library/itertools.html#itertools-recipes
        a, b = itertools.tee(iterable)
        next(b, None)
        return zip(a, b)


class WL4Region(Region):
    clear_rule: AccessRule

    def __init__(self, name: str, world: WL4World):
        super().__init__(name, world.player, world.multiworld)
        self.clear_rule = None


def basic_region_creator(world: WL4World, location_table: Set[str]):
    def basic_region(name, locations=()):
        return create_region(world, location_table, name, locations)
    return basic_region


def create_regions(world: WL4World, location_table: Set[str]):
    create_main_regions(world, location_table)
    create_level_regions(world, location_table)


def create_main_regions(world: WL4World, location_table: Set[str]):
    basic_region = basic_region_creator(world, location_table)

    def passage_region(passage: Passage):
        return basic_region(passage.long_name())

    def minigame_shop(passage: Passage):
        return basic_region(f'{passage.short_name()} Minigame Shop')

    def boss_region(passage: Passage, boss_name: str):
        return basic_region(f'{passage.long_name()} Boss', [boss_name])

    menu_region = basic_region('Menu')

    passage_regions = (passage_region(passage) for passage in Passage)
    minigame_shops = (minigame_shop(passage) for passage in Passage)

    spoiled_rotten = boss_region(Passage.ENTRY, 'Spoiled Rotten')
    cractus = boss_region(Passage.EMERALD, 'Cractus')
    cuckoo_condor = boss_region(Passage.RUBY, 'Cuckoo Condor')
    aerodent = boss_region(Passage.TOPAZ, 'Aerodent')
    catbat = boss_region(Passage.SAPPHIRE, 'Catbat')
    golden_diva = boss_region(Passage.GOLDEN, 'Golden Diva')

    world.multiworld.regions += [
        menu_region,
        *passage_regions,
        *minigame_shops,
        spoiled_rotten,
        cractus,
        cuckoo_condor,
        aerodent,
        catbat,
        golden_diva,
    ]


# Eventually I'll want to make trees out of the regions in the levels for
# diamond shuffle, but sequences will work for now
regions_in_levels = {
    'Hall of Hieroglyphs':   None,

    'Palm Tree Paradise':    None,
    'Wildflower Fields':     ['Before Sunflower', 'After Sunflower'],
    'Mystic Lake':           ['Shore', 'Shallows', 'Depths'],
    'Monsoon Jungle':        ['Upper', 'Lower'],

    'The Curious Factory':   None,
    'The Toxic Landfill':    None,
    '40 Below Fridge':       None,
    'Pinball Zone':          ['Early Rooms', 'Jungle Room', 'Late Rooms', 'Escape'],

    'Toy Block Tower':       None,
    'The Big Board':         None,
    'Doodle Woods':          None,
    'Domino Row':            ['Before Lake', 'After Lake'],

    'Crescent Moon Village': ['Upper', 'Lower'],
    'Arabian Night':         ['Town', 'Sewer'],
    'Fiery Cavern':          ['Flaming', 'Frozen'],
    'Hotel Horror':          ['Hotel', 'Switch Room'],

    'Golden Passage':        ['Passage', 'Keyzer Area'],
}


def get_region_names(level_name: str, merge: bool = False) -> Sequence[str]:
    entrance = f'{level_name} (entrance)'
    regions = regions_in_levels[level_name]
    if regions and not merge:
        regions = (f'{level_name} - {region}' for region in regions)
    else:
        regions = (level_name,)
    return entrance, *regions


def create_level_regions(world: WL4World, location_table: Set[str]):
    basic_region = basic_region_creator(world, location_table)

    def level_regions(name: str, passage: Passage, level: int):
        portal_setting = world.options.portal.value
        region_names = get_region_names(name)
        regions = {region: basic_region(region) for region in region_names}
        for loc_name, location in get_level_location_data(passage, level):
            if not portal_setting:
                region_name = rules.get_frog_switch_region(name)
            elif location.region_in_level is not None:
                region_name = f'{name} - {location.region_in_level}'
            else:
                region_name = name
            if loc_name in location_table:
                location = WL4Location.from_name(world.player, loc_name, regions[region_name])
                regions[region_name].locations.append(location)
        return regions.values()

    hall_of_hieroglyphs = level_regions('Hall of Hieroglyphs', Passage.ENTRY, 0)

    palm_tree_paradise = level_regions('Palm Tree Paradise', Passage.EMERALD, 0)
    wildflower_fields = level_regions('Wildflower Fields', Passage.EMERALD, 1)
    mystic_lake = level_regions('Mystic Lake', Passage.EMERALD, 2)
    monsoon_jungle = level_regions('Monsoon Jungle', Passage.EMERALD, 3)

    curious_factory = level_regions('The Curious Factory', Passage.RUBY, 0)
    toxic_landfill = level_regions('The Toxic Landfill', Passage.RUBY, 1)
    forty_below_fridge = level_regions('40 Below Fridge', Passage.RUBY, 2)
    pinball_zone = level_regions('Pinball Zone', Passage.RUBY, 3)

    toy_block_tower = level_regions('Toy Block Tower', Passage.TOPAZ, 0)
    big_board = level_regions('The Big Board', Passage.TOPAZ, 1)
    doodle_woods = level_regions('Doodle Woods', Passage.TOPAZ, 2)
    domino_row = level_regions('Domino Row', Passage.TOPAZ, 3)

    crescent_moon_village = level_regions('Crescent Moon Village', Passage.SAPPHIRE, 0)
    arabian_night = level_regions('Arabian Night', Passage.SAPPHIRE, 1)
    fiery_cavern = level_regions('Fiery Cavern', Passage.SAPPHIRE, 2)
    hotel_horror = level_regions('Hotel Horror', Passage.SAPPHIRE, 3)

    golden_passage = level_regions('Golden Passage', Passage.GOLDEN, 0)

    world.multiworld.regions += [
        *hall_of_hieroglyphs,
        *palm_tree_paradise,
        *wildflower_fields,
        *mystic_lake,
        *monsoon_jungle,
        *curious_factory,
        *toxic_landfill,
        *forty_below_fridge,
        *pinball_zone,
        *toy_block_tower,
        *big_board,
        *doodle_woods,
        *domino_row,
        *crescent_moon_village,
        *arabian_night,
        *fiery_cavern,
        *hotel_horror,
        *golden_passage,
    ]


def connect_regions(world: WL4World):
    portal_setting = world.options.portal.value

    def connect_level(level_name):
        regions = get_region_names(level_name)
        for source, dest in pairwise(regions):
            access_rule = rules.get_access_rule(world, dest)
            connect_entrance(world, dest, source, dest, access_rule)

    connect_level('Hall of Hieroglyphs')
    connect_level('Palm Tree Paradise')
    connect_level('Wildflower Fields')
    connect_level('Mystic Lake')
    connect_level('Monsoon Jungle')
    connect_level('The Curious Factory')
    connect_level('The Toxic Landfill')
    connect_level('40 Below Fridge')
    connect_level('Pinball Zone')
    connect_level('Toy Block Tower')
    connect_level('The Big Board')
    connect_level('Doodle Woods')
    connect_level('Domino Row')
    connect_level('Crescent Moon Village')
    connect_level('Arabian Night')
    connect_level('Fiery Cavern')
    connect_level('Hotel Horror')
    connect_level('Golden Passage')

    def connect_with_name(source, destination, name, rule: AccessRule = None):
        connect_entrance(world, name, source, destination, rule)

    def connect(source, destination, rule: AccessRule = None):
        connect_with_name(source, destination, f'{source} -> {destination}', rule)

    def connect_level_exit(level, destination, rule: AccessRule = None):
        # No Keyzer means you can just walk past the actual entrance to the next level
        open_doors = world.options.open_doors
        if (open_doors == OpenDoors.option_open
            or (open_doors == OpenDoors.option_closed_diva and level != 'Golden Passage')
           ):
            region = f'{level} (entrance)'
        elif portal_setting:
            region = rules.get_keyzer_region(level)
        else:
            region = get_region_names(level)[-1]
        connect_with_name(region, destination, f'{level} Gate', rule)

    required_jewels = world.options.required_jewels.value
    required_jewels_entry = min(1, required_jewels)

    connect('Menu', 'Entry Passage')
    connect('Entry Passage', 'Hall of Hieroglyphs (entrance)')
    connect_level_exit('Hall of Hieroglyphs', 'Entry Minigame Shop')
    connect('Entry Minigame Shop', 'Entry Passage Boss',
            rules.make_boss_access_rule(world, Passage.ENTRY, required_jewels_entry))

    connect('Menu', 'Emerald Passage')
    connect('Emerald Passage', 'Palm Tree Paradise (entrance)')
    connect_level_exit('Palm Tree Paradise', 'Wildflower Fields (entrance)')
    connect_level_exit('Wildflower Fields', 'Mystic Lake (entrance)')
    connect_level_exit('Mystic Lake', 'Monsoon Jungle (entrance)')
    connect_level_exit('Monsoon Jungle', 'Emerald Minigame Shop')
    connect('Emerald Minigame Shop', 'Emerald Passage Boss',
            rules.make_boss_access_rule(world, Passage.EMERALD, required_jewels))

    connect('Menu', 'Ruby Passage')
    connect('Ruby Passage', 'The Curious Factory (entrance)')
    connect_level_exit('The Curious Factory', 'The Toxic Landfill (entrance)')
    connect_level_exit('The Toxic Landfill', '40 Below Fridge (entrance)')
    connect_level_exit('40 Below Fridge', 'Pinball Zone (entrance)')
    connect_level_exit('Pinball Zone', 'Ruby Minigame Shop')
    connect('Ruby Minigame Shop', 'Ruby Passage Boss',
            rules.make_boss_access_rule(world, Passage.RUBY, required_jewels))

    connect('Menu', 'Topaz Passage')
    connect('Topaz Passage', 'Toy Block Tower (entrance)')
    connect_level_exit('Toy Block Tower', 'The Big Board (entrance)')
    connect_level_exit('The Big Board', 'Doodle Woods (entrance)')
    connect_level_exit('Doodle Woods', 'Domino Row (entrance)')
    connect_level_exit('Domino Row', 'Topaz Minigame Shop')
    connect('Topaz Minigame Shop', 'Topaz Passage Boss',
            rules.make_boss_access_rule(world, Passage.TOPAZ, required_jewels))

    connect('Menu', 'Sapphire Passage')
    connect('Sapphire Passage', 'Crescent Moon Village (entrance)')
    connect_level_exit('Crescent Moon Village', 'Arabian Night (entrance)')
    connect_level_exit('Arabian Night', 'Fiery Cavern (entrance)')
    connect_level_exit('Fiery Cavern', 'Hotel Horror (entrance)')
    connect_level_exit('Hotel Horror', 'Sapphire Minigame Shop')
    connect('Sapphire Minigame Shop', 'Sapphire Passage Boss',
            rules.make_boss_access_rule(world, Passage.SAPPHIRE, required_jewels))

    connect('Menu', 'Golden Pyramid',
            lambda state: state.has_all({'Emerald Passage Clear', 'Ruby Passage Clear',
                                     'Topaz Passage Clear', 'Sapphire Passage Clear'}, world.player))
    connect('Golden Pyramid', 'Golden Passage (entrance)')
    connect_level_exit('Golden Passage', 'Golden Minigame Shop')
    connect('Golden Minigame Shop', 'Golden Pyramid Boss',
            rules.make_boss_access_rule(world, Passage.GOLDEN, required_jewels_entry))


def create_region(world: WL4World, location_table: Set[str], name: str,
                  locations: Iterable[str] = ()) -> WL4Region:
    region = WL4Region(name, world)
    for location in locations:
        if location in location_table:
            region.locations.append(WL4Location.from_name(world.player, location, region))
    return region


def connect_entrance(world: WL4World, name: str, source: str, target: str, rule: AccessRule = None):
    multiworld, player = world.multiworld, world.player
    source_region = multiworld.get_region(source, player)
    target_region = multiworld.get_region(target, player)

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
