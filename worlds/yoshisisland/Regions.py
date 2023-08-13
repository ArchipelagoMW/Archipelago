from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import LocationData
from .LogicExtensions import YoshiLogic
from .Options import get_option_value
from .SetupBosses import BossReqs

def create_regions(world: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location], gamevar, boss_order: list, level_location_list: list, luigi_pieces: int):
    logic = YoshiLogic(world, player, boss_order, luigi_pieces)

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(world, player, locations_per_region, location_cache, 'Menu'),
        create_region(world, player, locations_per_region, location_cache, 'Overworld'),
        create_region(world, player, locations_per_region, location_cache, 'World 1'),
        create_region(world, player, locations_per_region, location_cache, 'World 2'),
        create_region(world, player, locations_per_region, location_cache, 'World 3'),
        create_region(world, player, locations_per_region, location_cache, 'World 4'),
        create_region(world, player, locations_per_region, location_cache, 'World 5'),
        create_region(world, player, locations_per_region, location_cache, 'World 6'),

        create_region(world, player, locations_per_region, location_cache, 'Make Eggs, Throw Eggs'),
        create_region(world, player, locations_per_region, location_cache, 'Watch Out Below!'),
        create_region(world, player, locations_per_region, location_cache, 'The Cave Of Chomp Rock'),
        create_region(world, player, locations_per_region, location_cache, "Burt The Bashful's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Burt The Bashful's Boss Room"),
        create_region(world, player, locations_per_region, location_cache, 'Hop! Hop! Donut Lifts'),
        create_region(world, player, locations_per_region, location_cache, 'Shy-Guys On Stilts'),
        create_region(world, player, locations_per_region, location_cache, 'Touch Fuzzy Get Dizzy'),
        create_region(world, player, locations_per_region, location_cache, "Salvo The Slime's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Salvo The Slime's Boss Room"),

        create_region(world, player, locations_per_region, location_cache, "Visit Koopa And Para-Koopa"),
        create_region(world, player, locations_per_region, location_cache, "The Baseball Boys"),
        create_region(world, player, locations_per_region, location_cache, "What's Gusty Taste Like?"),
        create_region(world, player, locations_per_region, location_cache, "Bigger Boo's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Bigger Boo's Boss Room"),
        create_region(world, player, locations_per_region, location_cache, "Watch Out For Lakitu"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of The Mystery Maze"),
        create_region(world, player, locations_per_region, location_cache, "Lakitu's Wall"),
        create_region(world, player, locations_per_region, location_cache, "The Potted Ghost's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Roger The Ghost's Boss Room"),

        create_region(world, player, locations_per_region, location_cache, "Welcome To Monkey World!"),
        create_region(world, player, locations_per_region, location_cache, "Jungle Rhythm..."),
        create_region(world, player, locations_per_region, location_cache, "Nep-Enuts' Domain"),
        create_region(world, player, locations_per_region, location_cache, "Prince Froggy's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Prince Froggy's Boss Room"),
        create_region(world, player, locations_per_region, location_cache, "Jammin' Through The Trees"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of Harry Hedgehog"),
        create_region(world, player, locations_per_region, location_cache, "Monkeys' Favorite Lake"),
        create_region(world, player, locations_per_region, location_cache, "Naval Piranha's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Naval Piranha's Boss Room"),

        create_region(world, player, locations_per_region, location_cache, "GO! GO! MARIO!!"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of The Lakitus"),
        create_region(world, player, locations_per_region, location_cache, "Don't Look Back!"),
        create_region(world, player, locations_per_region, location_cache, "Marching Milde's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Marching Milde's Boss Room"),
        create_region(world, player, locations_per_region, location_cache, "Chomp Rock Zone"),
        create_region(world, player, locations_per_region, location_cache, "Lake Shore Paradise"),
        create_region(world, player, locations_per_region, location_cache, "Ride Like The Wind"),
        create_region(world, player, locations_per_region, location_cache, "Hookbill The Koopa's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Hookbill The Koopa's Boss Room"),

        create_region(world, player, locations_per_region, location_cache, "BLIZZARD!!!"),
        create_region(world, player, locations_per_region, location_cache, "Ride The Ski Lifts"),
        create_region(world, player, locations_per_region, location_cache, "Danger - Icy Conditions Ahead"),
        create_region(world, player, locations_per_region, location_cache, "Sluggy The Unshaven's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Sluggy The Unshaven's Boss Room"),
        create_region(world, player, locations_per_region, location_cache, "Goonie Rides!"),
        create_region(world, player, locations_per_region, location_cache, "Welcome To Cloud World"),
        create_region(world, player, locations_per_region, location_cache, "Shifting Platforms Ahead"),
        create_region(world, player, locations_per_region, location_cache, "Raphael The Raven's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Raphael The Raven's Boss Room"),

        create_region(world, player, locations_per_region, location_cache, "Scary Skeleton Goonies!"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of The Bandits"),
        create_region(world, player, locations_per_region, location_cache, "Beware The Spinning Logs"),
        create_region(world, player, locations_per_region, location_cache, "Tap-Tap The Red Nose's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Tap-Tap The Red Nose's Boss Room"),
        create_region(world, player, locations_per_region, location_cache, "The Very Loooooong Cave"),
        create_region(world, player, locations_per_region, location_cache, "The Deep, Underground Maze"),
        create_region(world, player, locations_per_region, location_cache, "KEEP MOVING!!!!"),
        create_region(world, player, locations_per_region, location_cache, "King Bowser's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Bowser's Room"),

    ]
    if get_option_value(world, player, "extras_enabled") == 1:
        regions.insert(72, create_region(world, player, locations_per_region, location_cache, "Castles - Masterpiece Set")),
        regions.insert(62, create_region(world, player, locations_per_region, location_cache, "Kamek's Revenge")),
        regions.insert(51, create_region(world, player, locations_per_region, location_cache, "The Impossible? Maze")),
        regions.insert(40, create_region(world, player, locations_per_region, location_cache, "More Monkey Madness")),
        regions.insert(30, create_region(world, player, locations_per_region, location_cache, "Hit That Switch!!")),
        regions.insert(18, create_region(world, player, locations_per_region, location_cache, "Poochy Ain't Stupid"))

    if get_option_value(world, player, "minigame_checks") >= 2:
        regions.insert(74, create_region(world, player, locations_per_region, location_cache, "Slot Machine")),
        regions.insert(60, create_region(world, player, locations_per_region, location_cache, "Roulette")),
        regions.insert(51, create_region(world, player, locations_per_region, location_cache, "Match Cards")),
        regions.insert(40, create_region(world, player, locations_per_region, location_cache, "Drawing Lots")),
        regions.insert(30, create_region(world, player, locations_per_region, location_cache, "Scratch And Match")),
        regions.insert(18, create_region(world, player, locations_per_region, location_cache, "Flip Cards"))
    world.regions += regions

    connectStartingRegion(world, player)

    bosses = BossReqs(world, player)

    names: Dict[str, int] = {}

    connect(world, player, names, 'Overworld', 'World 1', lambda state: state.has('World 1 Gate', player)),
    connect(world, player, names, 'Overworld', 'World 2', lambda state: state.has('World 2 Gate', player)),
    connect(world, player, names, 'Overworld', 'World 3', lambda state: state.has('World 3 Gate', player)),
    connect(world, player, names, 'Overworld', 'World 4', lambda state: state.has('World 4 Gate', player)),
    connect(world, player, names, 'Overworld', 'World 5', lambda state: state.has('World 5 Gate', player)),
    connect(world, player, names, 'Overworld', 'World 6', lambda state: state.has('World 6 Gate', player)),

    connect(world, player, names, 'World 1', gamevar.level_location_list[0]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[1]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[2]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[3]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[4]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[5]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[6]),
    connect(world, player, names, 'World 1', gamevar.level_location_list[7]),
    connect(world, player, names, "Burt The Bashful's Fort", gamevar.boss_order[0], lambda state: logic._14Clear(state)),
    connect(world, player, names, "Salvo The Slime's Castle", gamevar.boss_order[1], lambda state: logic._18Clear(state)),

    connect(world, player, names, 'World 2', gamevar.level_location_list[8]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[9]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[10]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[11]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[12]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[13]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[14]),
    connect(world, player, names, 'World 2', gamevar.level_location_list[15]),
    connect(world, player, names, "Bigger Boo's Fort", gamevar.boss_order[2], lambda state: logic._24Clear(state)),
    connect(world, player, names, "The Potted Ghost's Castle", gamevar.boss_order[3], lambda state: logic._28Clear(state)),

    connect(world, player, names, 'World 3', gamevar.level_location_list[16]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[17]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[18]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[19]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[20]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[21]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[22]),
    connect(world, player, names, 'World 3', gamevar.level_location_list[23]),
    connect(world, player, names, "Prince Froggy's Fort", gamevar.boss_order[4], lambda state: logic._34Clear(state)),
    connect(world, player, names, "Naval Piranha's Castle", gamevar.boss_order[5], lambda state: logic._38Clear(state)),

    connect(world, player, names, 'World 4', gamevar.level_location_list[24]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[25]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[26]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[27]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[28]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[29]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[30]),
    connect(world, player, names, 'World 4', gamevar.level_location_list[31]),
    connect(world, player, names, "Marching Milde's Fort", gamevar.boss_order[6], lambda state: logic._44Clear(state)),
    connect(world, player, names, "Hookbill The Koopa's Castle", gamevar.boss_order[7], lambda state: logic._48Clear(state)),

    connect(world, player, names, 'World 5', gamevar.level_location_list[32]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[33]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[34]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[35]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[36]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[37]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[38]),
    connect(world, player, names, 'World 5', gamevar.level_location_list[39]),
    connect(world, player, names, "Sluggy The Unshaven's Fort", gamevar.boss_order[8], lambda state: logic._54Clear(state)),
    connect(world, player, names, "Raphael The Raven's Castle", gamevar.boss_order[9], lambda state: logic._58Clear(state)),

    connect(world, player, names, 'World 6', gamevar.level_location_list[40]),
    connect(world, player, names, 'World 6', gamevar.level_location_list[41]),
    connect(world, player, names, 'World 6', gamevar.level_location_list[42]),
    connect(world, player, names, 'World 6', gamevar.level_location_list[43]),
    connect(world, player, names, 'World 6', gamevar.level_location_list[44]),
    connect(world, player, names, 'World 6', gamevar.level_location_list[45]),
    connect(world, player, names, 'World 6', gamevar.level_location_list[46]),
    connect(world, player, names, 'World 6', "King Bowser's Castle", lambda state: bosses.castle_access(state)),
    connect(world, player, names, "King Bowser's Castle", "Bowser's Room", lambda state: bosses.castle_clear(state)),
    connect(world, player, names, "Tap-Tap The Red Nose's Fort", gamevar.boss_order[10], lambda state: logic._64Clear(state))

    if get_option_value(world, player, "extras_enabled") == 1:
        connect(world, player, names, 'World 1', "Poochy Ain't Stupid", lambda state: state.has('Extra Panels', player) or state.has('Extra 1', player)),
        connect(world, player, names, 'World 2', "Hit That Switch!!", lambda state: state.has('Extra Panels', player) or state.has('Extra 2', player)),
        connect(world, player, names, 'World 3', "More Monkey Madness", lambda state: state.has('Extra Panels', player) or state.has('Extra 3', player)),
        connect(world, player, names, 'World 4', "The Impossible? Maze", lambda state: state.has('Extra Panels', player) or state.has('Extra 4', player)),
        connect(world, player, names, 'World 5', "Kamek's Revenge", lambda state: state.has('Extra Panels', player) or state.has('Extra 5', player)),
        connect(world, player, names, 'World 6', "Castles - Masterpiece Set", lambda state: state.has('Extra Panels', player) or state.has('Extra 6', player))

    if get_option_value(world, player, "minigame_checks") >= 2:
        connect(world, player, names, 'World 1', "Flip Cards", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 1', player)),
        connect(world, player, names, 'World 2', "Scratch And Match", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 2', player)),
        connect(world, player, names, 'World 3', "Drawing Lots", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 3', player)),
        connect(world, player, names, 'World 4', "Match Cards", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 4', player)),
        connect(world, player, names, 'World 5', "Roulette", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 5', player)),
        connect(world, player, names, 'World 6', "Slot Machine", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 6', player)),

def create_location(player: int, location_data: LocationData, region: Region, location_cache: List[Location]) -> Location:
    location = Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location

def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, world)
    region.world = world

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region

def connectStartingRegion(world: MultiWorld, player: int):
    menu = world.get_region('Menu', player)
    world_main = world.get_region('Overworld', player)

    if get_option_value(world, player, "starting_world") == 0:
        starting_region = world.get_region('World 1', player)
    elif get_option_value(world, player, "starting_world") == 1:
        starting_region = world.get_region('World 2', player)
    elif get_option_value(world, player, "starting_world") == 2:
        starting_region = world.get_region('World 3', player)
    elif get_option_value(world, player, "starting_world") == 3:
        starting_region = world.get_region('World 4', player)
    elif get_option_value(world, player, "starting_world") == 4:
        starting_region = world.get_region('World 5', player)
    elif get_option_value(world, player, "starting_world") == 5:
        starting_region = world.get_region('World 6', player)

    load_file = Entrance(player, 'Overworld', menu)
    load_file.connect(world_main)
    menu.exits.append(load_file)

    starting_world = Entrance(player, 'Overworld', world_main)
    starting_world.connect(starting_region)
    world_main.exits.append(starting_world)

def connect(world: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str, rule: Optional[Callable] = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (' ' * used_names[target])

    connection = Entrance(player, name, sourceRegion)

    if rule:
        connection.access_rule = rule
        
    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region