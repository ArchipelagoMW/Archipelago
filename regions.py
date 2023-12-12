from typing import Iterable, Set

from BaseClasses import MultiWorld, Region, Entrance

from . import rules
from .locations import WL4Location, get_level_locations
from .types import AccessRule, Passage


class WL4Region(Region):
    clear_rule: AccessRule

    def __init__(self, name: str, player: int, multiworld: MultiWorld):
        super().__init__(name, player, multiworld)
        self.clear_rule = None


def create_regions(world: MultiWorld, player: int, location_table: Set[str]):
    def basic_region(name, locations=()):
        return create_region(world, player, location_table, name, locations)

    def passage_region(passage: Passage):
        return basic_region(passage.long_name())

    def level_regions(name: str, passage: Passage, level: int):
        entrance = basic_region(f'{name} (entrance)')
        boxes = basic_region(name, get_level_locations(passage, level))
        return entrance, boxes

    def minigame_shop(passage: Passage):
        return basic_region(f'{passage.short_name()} Minigame Shop')

    def boss_region(passage: Passage, boss_name: str):
        return basic_region(f'{passage.long_name()} Boss', [boss_name])

    menu_region = basic_region('Menu')

    passage_regions = (passage_region(passage) for passage in Passage)
    minigame_shops = (minigame_shop(passage) for passage in Passage)

    hall_of_hieroglyphs = level_regions('Hall of Hieroglyphs', Passage.ENTRY, 0)
    spoiled_rotten = boss_region(Passage.ENTRY, 'Spoiled Rotten')

    palm_tree_paradise = level_regions('Palm Tree Paradise', Passage.EMERALD, 0)
    wildflower_fields = level_regions('Wildflower Fields', Passage.EMERALD, 1)
    mystic_lake = level_regions('Mystic Lake', Passage.EMERALD, 2)
    monsoon_jungle = level_regions('Monsoon Jungle', Passage.EMERALD, 3)
    cractus = boss_region(Passage.EMERALD, 'Cractus')

    curious_factory = level_regions('The Curious Factory', Passage.RUBY, 0)
    toxic_landfill = level_regions('The Toxic Landfill', Passage.RUBY, 1)
    forty_below_fridge = level_regions('40 Below Fridge', Passage.RUBY, 2)
    pinball_zone = level_regions('Pinball Zone', Passage.RUBY, 3)
    cuckoo_condor = boss_region(Passage.RUBY, 'Cuckoo Condor')

    toy_block_tower = level_regions('Toy Block Tower', Passage.TOPAZ, 0)
    big_board = level_regions('The Big Board', Passage.TOPAZ, 1)
    doodle_woods = level_regions('Doodle Woods', Passage.TOPAZ, 2)
    domino_row = level_regions('Domino Row', Passage.TOPAZ, 3)
    aerodent = boss_region(Passage.TOPAZ, 'Aerodent')

    crescent_moon_village = level_regions('Crescent Moon Village', Passage.SAPPHIRE, 0)
    arabian_night = level_regions('Arabian Night', Passage.SAPPHIRE, 1)
    fiery_cavern = level_regions('Fiery Cavern', Passage.SAPPHIRE, 2)
    hotel_horror = level_regions('Hotel Horror', Passage.SAPPHIRE, 3)
    catbat = boss_region(Passage.SAPPHIRE, 'Catbat')

    golden_passage = level_regions('Golden Passage', Passage.GOLDEN, 0)
    golden_diva = boss_region(Passage.GOLDEN, 'Golden Diva')

    world.regions += [
        menu_region,
        *passage_regions,
        *minigame_shops,
        *hall_of_hieroglyphs,
        spoiled_rotten,
        *palm_tree_paradise,
        *wildflower_fields,
        *mystic_lake,
        *monsoon_jungle,
        cractus,
        *curious_factory,
        *toxic_landfill,
        *forty_below_fridge,
        *pinball_zone,
        cuckoo_condor,
        *toy_block_tower,
        *big_board,
        *doodle_woods,
        *domino_row,
        aerodent,
        *crescent_moon_village,
        *arabian_night,
        *fiery_cavern,
        *hotel_horror,
        catbat,
        *golden_passage,
        golden_diva,
    ]


def connect_regions(world: MultiWorld, player: int):
    def connect_level(level_name):
        if level_name == 'Hotel Horror' and world.difficulty[player].value == 2:
            rule = None
        else:
            rule = rules.get_access_rule(player, level_name)
        connect_entrance(world, player, level_name, f'{level_name} (entrance)', level_name, rule)

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
        connect_entrance(world, player, name, source, destination, rule)

    def connect(source, destination, rule: AccessRule = None):
        connect_with_name(source, destination, f'{source} -> {destination}', rule)

    def connect_level_exit(source, destination, rule: AccessRule = None):
        level = source
        # No Keyzer means you can just walk past the actual entrance to the next level
        open_doors = world.open_doors[player].value
        if open_doors == 2 or (open_doors == 1 and level != 'Golden Passage'):
            source += ' (entrance)'
        connect_with_name(source, destination, f'{level} Gate', rule)

    required_jewels = world.required_jewels[player].value
    required_jewels_entry = min(1, required_jewels)

    connect('Menu', 'Entry Passage')
    connect('Entry Passage', 'Hall of Hieroglyphs (entrance)')
    connect_level_exit('Hall of Hieroglyphs', 'Entry Minigame Shop')
    connect('Entry Minigame Shop', 'Entry Passage Boss',
            rules.make_boss_access_rule(player, Passage.ENTRY, required_jewels_entry))

    connect('Menu', 'Emerald Passage')
    connect('Emerald Passage', 'Palm Tree Paradise (entrance)')
    connect_level_exit('Palm Tree Paradise', 'Wildflower Fields (entrance)')
    connect_level_exit('Wildflower Fields', 'Mystic Lake (entrance)')
    connect_level_exit('Mystic Lake', 'Monsoon Jungle (entrance)')
    connect_level_exit('Monsoon Jungle', 'Emerald Minigame Shop')
    connect('Emerald Minigame Shop', 'Emerald Passage Boss',
            rules.make_boss_access_rule(player, Passage.EMERALD, required_jewels))

    connect('Menu', 'Ruby Passage')
    connect('Ruby Passage', 'The Curious Factory (entrance)')
    connect_level_exit('The Curious Factory', 'The Toxic Landfill (entrance)')
    connect_level_exit('The Toxic Landfill', '40 Below Fridge (entrance)')
    connect_level_exit('40 Below Fridge', 'Pinball Zone (entrance)')
    connect_level_exit('Pinball Zone', 'Ruby Minigame Shop')
    connect('Ruby Minigame Shop', 'Ruby Passage Boss',
            rules.make_boss_access_rule(player, Passage.RUBY, required_jewels))

    connect('Menu', 'Topaz Passage')
    connect('Topaz Passage', 'Toy Block Tower (entrance)')
    connect_level_exit('Toy Block Tower', 'The Big Board (entrance)')
    connect_level_exit('The Big Board', 'Doodle Woods (entrance)')
    connect_level_exit('Doodle Woods', 'Domino Row (entrance)')
    connect_level_exit('Domino Row', 'Topaz Minigame Shop')
    connect('Topaz Minigame Shop', 'Topaz Passage Boss',
            rules.make_boss_access_rule(player, Passage.TOPAZ, required_jewels))

    connect('Menu', 'Sapphire Passage')
    connect('Sapphire Passage', 'Crescent Moon Village (entrance)')
    connect_level_exit('Crescent Moon Village', 'Arabian Night (entrance)')
    connect_level_exit('Arabian Night', 'Fiery Cavern (entrance)')
    connect_level_exit('Fiery Cavern', 'Hotel Horror (entrance)')
    connect_level_exit('Hotel Horror', 'Sapphire Minigame Shop')
    connect('Sapphire Minigame Shop', 'Sapphire Passage Boss',
            rules.make_boss_access_rule(player, Passage.SAPPHIRE, required_jewels))

    connect('Menu', 'Golden Pyramid',
            lambda state: state.has_all({'Emerald Passage Clear', 'Ruby Passage Clear',
                                     'Topaz Passage Clear', 'Sapphire Passage Clear'}, player))
    connect('Golden Pyramid', 'Golden Passage (entrance)')
    # Golden Passage is the only level where escaping has different requirements from getting Keyzer
    connect_level_exit('Golden Passage', 'Golden Minigame Shop',
            lambda state: world.open_doors[player].value == 2 or
                          (state.has('Progressive Grab', player) and
                           state.has('Progressive Ground Pound', player)))
    connect('Golden Minigame Shop', 'Golden Pyramid Boss',
            rules.make_boss_access_rule(player, Passage.GOLDEN, required_jewels_entry))


def create_region(world: MultiWorld, player: int, location_table: Set[str],
                  name: str, locations: Iterable[str] = ()) -> WL4Region:
    region = WL4Region(name, player, world)
    for location in locations:
        if location in location_table:
            region.locations.append(WL4Location.from_name(player, location, region))
    return region


def connect_entrance(world: MultiWorld, player: int, name: str,
            source: str, target: str, rule: AccessRule = None):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
