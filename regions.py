from typing import Callable, Dict, Iterable, Optional

from BaseClasses import MultiWorld, Region, Entrance

from .locations import WL4Location, get_level_locations
from .types import Passage


def create_regions(world: MultiWorld, player: int, location_table: dict):
    def basic_region(name, locations=()):
        return create_region(world, player, location_table, name, locations)

    def passage_region(passage: Passage):
        return basic_region(passage.long_name())

    def level_region(name, passage, level):
        return basic_region(name, get_level_locations(passage, level))

    def boss_region(passage: Passage, boss_name):
        return basic_region(f'{passage.long_name()} Boss', [boss_name])

    menu_region = basic_region('Menu')

    entry_passage = passage_region(Passage.ENTRY)
    hall_of_hieroglyphs = level_region('Hall of Hieroglyphs', Passage.ENTRY, 0)
    spoiled_rotten = boss_region(Passage.ENTRY, 'Spoiled Rotten')

    emerald_passage = passage_region(Passage.EMERALD)
    palm_tree_paradise = level_region('Palm Tree Paradise', Passage.EMERALD, 0)
    wildflower_fields = level_region('Wildflower Fields', Passage.EMERALD, 1)
    mystic_lake = level_region('Mystic Lake', Passage.EMERALD, 2)
    monsoon_jungle = level_region('Monsoon Jungle', Passage.EMERALD, 3)
    cractus = boss_region(Passage.EMERALD, 'Cractus')

    ruby_passage = passage_region(Passage.RUBY)
    curious_factory = level_region('The Curious Factory', Passage.RUBY, 0)
    toxic_landfill = level_region('The Toxic Landfill', Passage.RUBY, 1)
    forty_below_fridge = level_region('40 Below Fridge', Passage.RUBY, 2)
    pinball_zone = level_region('Pinball Zone', Passage.RUBY, 3)
    cuckoo_condor = boss_region(Passage.RUBY, 'Cuckoo Condor')

    topaz_passage = passage_region(Passage.TOPAZ)
    toy_block_tower = level_region('Toy Block Tower', Passage.TOPAZ, 0)
    big_board = level_region('The Big Board', Passage.TOPAZ, 1)
    doodle_woods = level_region('Doodle Woods', Passage.TOPAZ, 2)
    domino_row = level_region('Domino Row', Passage.TOPAZ, 3)
    aerodent = boss_region(Passage.TOPAZ, 'Aerodent')

    sapphire_passage = passage_region(Passage.SAPPHIRE)
    crescent_moon_village = level_region('Crescent Moon Village', Passage.SAPPHIRE, 0)
    arabian_night = level_region('Arabian Night', Passage.SAPPHIRE, 1)
    fiery_cavern = level_region('Fiery Cavern', Passage.SAPPHIRE, 2)
    hotel_horror = level_region('Hotel Horror', Passage.SAPPHIRE, 3)
    catbat = boss_region(Passage.SAPPHIRE, 'Catbat')

    golden_pyramid = passage_region(Passage.GOLDEN)
    golden_passage = level_region('Golden Passage', Passage.GOLDEN, 0)
    golden_diva = boss_region(Passage.GOLDEN, 'Golden Diva')

    world.regions += [
        menu_region,
        entry_passage,
        hall_of_hieroglyphs,
        spoiled_rotten,
        emerald_passage,
        palm_tree_paradise,
        wildflower_fields,
        mystic_lake,
        monsoon_jungle,
        cractus,
        ruby_passage,
        curious_factory,
        toxic_landfill,
        forty_below_fridge,
        pinball_zone,
        cuckoo_condor,
        topaz_passage,
        toy_block_tower,
        big_board,
        doodle_woods,
        domino_row,
        aerodent,
        sapphire_passage,
        crescent_moon_village,
        arabian_night,
        fiery_cavern,
        hotel_horror,
        catbat,
        golden_pyramid,
        golden_passage,
        golden_diva,
    ]


def connect_regions(world, player):
    names: Dict[str, int] = {}

    connect(world, player, names, 'Menu', 'Entry Passage')
    connect(world, player, names, 'Entry Passage', 'Hall of Hieroglyphs')
    connect(world, player, names, 'Hall of Hieroglyphs', 'Entry Passage Boss',
            lambda state: state.wl4_has_full_jewels(player, Passage.ENTRY, 1))

    connect(world, player, names, 'Menu', 'Emerald Passage',
            lambda state: state.has('Entry Passage Clear', player))
    connect(world, player, names, 'Emerald Passage', 'Palm Tree Paradise')
    connect(world, player, names, 'Palm Tree Paradise', 'Wildflower Fields')
    connect(world, player, names, 'Wildflower Fields', 'Mystic Lake')
    connect(world, player, names, 'Mystic Lake', 'Monsoon Jungle')
    connect(world, player, names, 'Monsoon Jungle', 'Emerald Passage Boss',
        lambda state: state.wl4_has_full_jewels(player, Passage.EMERALD, 4))

    connect(world, player, names, 'Menu', 'Ruby Passage',
            lambda state: state.has('Entry Passage Clear', player))
    connect(world, player, names, 'Ruby Passage', 'The Curious Factory')
    connect(world, player, names, 'The Curious Factory', 'The Toxic Landfill')
    connect(world, player, names, 'The Toxic Landfill', '40 Below Fridge')
    connect(world, player, names, '40 Below Fridge', 'Pinball Zone')
    connect(world, player, names, 'Pinball Zone', 'Ruby Passage Boss',
        lambda state: state.wl4_has_full_jewels(player, Passage.RUBY, 4))

    connect(world, player, names, 'Menu', 'Topaz Passage',
            lambda state: state.has('Entry Passage Clear', player))
    connect(world, player, names, 'Topaz Passage', 'Toy Block Tower')
    connect(world, player, names, 'Toy Block Tower', 'The Big Board')
    connect(world, player, names, 'The Big Board', 'Doodle Woods')
    connect(world, player, names, 'Doodle Woods', 'Domino Row')
    connect(world, player, names, 'Domino Row', 'Topaz Passage Boss',
        lambda state: state.wl4_has_full_jewels(player, Passage.TOPAZ, 4))

    connect(world, player, names, 'Menu', 'Sapphire Passage',
            lambda state: state.has('Entry Passage Clear', player))
    connect(world, player, names, 'Sapphire Passage', 'Crescent Moon Village')
    connect(world, player, names, 'Crescent Moon Village', 'Arabian Night')
    connect(world, player, names, 'Arabian Night', 'Fiery Cavern')
    connect(world, player, names, 'Fiery Cavern', 'Hotel Horror')
    connect(world, player, names, 'Hotel Horror', 'Sapphire Passage Boss',
        lambda state: state.wl4_has_full_jewels(player, Passage.SAPPHIRE, 4))

    connect(world, player, names, 'Menu', 'Golden Pyramid',
        lambda state: (state.has_all({'Emerald Passage Clear', 'Ruby Passage Clear',
                                      'Topaz Passage Clear', 'Sapphire Passage Clear'}, player)))
    connect(world, player, names, 'Golden Pyramid', 'Golden Passage')
    connect(world, player, names, 'Golden Passage', 'Golden Pyramid Boss',
        lambda state: state.wl4_has_full_jewels(player, Passage.GOLDEN, 1))


def create_region(world: MultiWorld, player: int, location_table: dict,
                  name: str, locations: Iterable[str] = ()):
    region = Region(name, player, world)
    for location in locations:
        if location in location_table:
            region.locations.append(WL4Location.from_name(player, location, region))
    return region


def connect(
    world: MultiWorld,
    player: int,
    used_names: Dict[str, int],
    source: str,
    target: str,
    rule: Optional[Callable] = None,
):
    source_region = world.get_region(source, player)
    target_region = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, source_region)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
