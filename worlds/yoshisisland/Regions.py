from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import LocationData
from .LevelLogic import YoshiLogic
from .Options import get_option_value
from .SetupBosses import BossReqs

class YILocation(Location):
    game: str = "Yoshi's Island"
    LevelID: int

def __init__(self, player: int, name: str = " ", address: int = None, parent=None, LevelID: int = None):
    super().__init__(player, name, address, parent)
    self.LevelID = LevelID


def create_regions(multiworld: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location], gamevar, boss_order: list, level_location_list: list, luigi_pieces: int):
    logic = YoshiLogic(multiworld, player, boss_order, luigi_pieces)

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(multiworld, player, locations_per_region, location_cache, 'Menu'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Overworld'),
        create_region(multiworld, player, locations_per_region, location_cache, 'World 1'),
        create_region(multiworld, player, locations_per_region, location_cache, 'World 2'),
        create_region(multiworld, player, locations_per_region, location_cache, 'World 3'),
        create_region(multiworld, player, locations_per_region, location_cache, 'World 4'),
        create_region(multiworld, player, locations_per_region, location_cache, 'World 5'),
        create_region(multiworld, player, locations_per_region, location_cache, 'World 6'),

        create_region(multiworld, player, locations_per_region, location_cache, '1-1'),
        create_region(multiworld, player, locations_per_region, location_cache, '1-2'),
        create_region(multiworld, player, locations_per_region, location_cache, '1-3'),
        create_region(multiworld, player, locations_per_region, location_cache, "1-4"),
        create_region(multiworld, player, locations_per_region, location_cache, "Burt The Bashful's Boss Room"),
        create_region(multiworld, player, locations_per_region, location_cache, '1-5'),
        create_region(multiworld, player, locations_per_region, location_cache, '1-6'),
        create_region(multiworld, player, locations_per_region, location_cache, '1-7'),
        create_region(multiworld, player, locations_per_region, location_cache, "1-8"),
        create_region(multiworld, player, locations_per_region, location_cache, "Salvo The Slime's Boss Room"),

        create_region(multiworld, player, locations_per_region, location_cache, "2-1"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-2"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-3"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-4"),
        create_region(multiworld, player, locations_per_region, location_cache, "Bigger Boo's Boss Room"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-5"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-6"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-7"),
        create_region(multiworld, player, locations_per_region, location_cache, "2-8"),
        create_region(multiworld, player, locations_per_region, location_cache, "Roger The Ghost's Boss Room"),

        create_region(multiworld, player, locations_per_region, location_cache, "3-1"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-2"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-3"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-4"),
        create_region(multiworld, player, locations_per_region, location_cache, "Prince Froggy's Boss Room"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-5"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-6"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-7"),
        create_region(multiworld, player, locations_per_region, location_cache, "3-8"),
        create_region(multiworld, player, locations_per_region, location_cache, "Naval Piranha's Boss Room"),

        create_region(multiworld, player, locations_per_region, location_cache, "4-1"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-2"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-3"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-4"),
        create_region(multiworld, player, locations_per_region, location_cache, "Marching Milde's Boss Room"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-5"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-6"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-7"),
        create_region(multiworld, player, locations_per_region, location_cache, "4-8"),
        create_region(multiworld, player, locations_per_region, location_cache, "Hookbill The Koopa's Boss Room"),

        create_region(multiworld, player, locations_per_region, location_cache, "5-1"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-2"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-3"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-4"),
        create_region(multiworld, player, locations_per_region, location_cache, "Sluggy The Unshaven's Boss Room"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-5"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-6"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-7"),
        create_region(multiworld, player, locations_per_region, location_cache, "5-8"),
        create_region(multiworld, player, locations_per_region, location_cache, "Raphael The Raven's Boss Room"),

        create_region(multiworld, player, locations_per_region, location_cache, "6-1"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-2"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-3"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-4"),
        create_region(multiworld, player, locations_per_region, location_cache, "Tap-Tap The Red Nose's Boss Room"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-5"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-6"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-7"),
        create_region(multiworld, player, locations_per_region, location_cache, "6-8"),
        create_region(multiworld, player, locations_per_region, location_cache, "Bowser's Room"),

    ]
    if get_option_value(multiworld, player, "extras_enabled") == 1:
        regions.insert(68, create_region(multiworld, player, locations_per_region, location_cache, "6-Extra")),
        regions.insert(58, create_region(multiworld, player, locations_per_region, location_cache, "5-Extra")),
        regions.insert(48, create_region(multiworld, player, locations_per_region, location_cache, "4-Extra")),
        regions.insert(38, create_region(multiworld, player, locations_per_region, location_cache, "3-Extra")),
        regions.insert(28, create_region(multiworld, player, locations_per_region, location_cache, "2-Extra")),
        regions.insert(18, create_region(multiworld, player, locations_per_region, location_cache, "1-Extra"))

    if get_option_value(multiworld, player, "minigame_checks") >= 2:
        regions.insert(74, create_region(multiworld, player, locations_per_region, location_cache, "6-Bonus")),
        regions.insert(63, create_region(multiworld, player, locations_per_region, location_cache, "5-Bonus")),
        regions.insert(52, create_region(multiworld, player, locations_per_region, location_cache, "4-Bonus")),
        regions.insert(41, create_region(multiworld, player, locations_per_region, location_cache, "3-Bonus")),
        regions.insert(29, create_region(multiworld, player, locations_per_region, location_cache, "2-Bonus")),
        regions.insert(19, create_region(multiworld, player, locations_per_region, location_cache, "1-Bonus"))
    multiworld.regions += regions

    connectStartingRegion(multiworld, player)

    bosses = BossReqs(multiworld, player)

    names: Dict[str, int] = {}

    multiworld.get_region('Overworld', player).add_exits(['World 1', 'World 2', 'World 3', 'World 4', 'World 5', 'World 6'],
                                                        {'World 1': lambda state: state.has('World 1 Gate', player),
                                                        'World 2': lambda state: state.has('World 2 Gate', player),
                                                        'World 3': lambda state: state.has('World 3 Gate', player),
                                                        'World 4': lambda state: state.has('World 4 Gate', player),
                                                        'World 5': lambda state: state.has('World 5 Gate', player),
                                                        'World 6': lambda state: state.has('World 6 Gate', player)})
    CurWorld = 1
    CurLev = 0
    for i in range(47):
        multiworld.get_region(f'World {CurWorld}', player).add_exits([gamevar.level_location_list[i]])
        if CurLev >= 8:
            CurLev = 1
            CurWorld += 1
        else: CurLev += 1

    connect(multiworld, player, names, "1-4", gamevar.boss_order[0], lambda state: logic._14Clear(state)),
    connect(multiworld, player, names, "1-8", gamevar.boss_order[1], lambda state: logic._18Clear(state)),

    connect(multiworld, player, names, "2-4", gamevar.boss_order[2], lambda state: logic._24Clear(state)),
    connect(multiworld, player, names, "2-8", gamevar.boss_order[3], lambda state: logic._28Clear(state)),

    connect(multiworld, player, names, "3-4", gamevar.boss_order[4], lambda state: logic._34Clear(state)),
    connect(multiworld, player, names, "3-8", gamevar.boss_order[5], lambda state: logic._38Clear(state)),

    connect(multiworld, player, names, "4-4", gamevar.boss_order[6], lambda state: logic._44Clear(state)),
    connect(multiworld, player, names, "4-8", gamevar.boss_order[7], lambda state: logic._48Clear(state)),

    connect(multiworld, player, names, "5-4", gamevar.boss_order[8], lambda state: logic._54Clear(state)),
    connect(multiworld, player, names, "5-8", gamevar.boss_order[9], lambda state: logic._58Clear(state)),
    connect(multiworld, player, names, 'World 6', "6-8", lambda state: bosses.castle_access(state)),
    connect(multiworld, player, names, "6-8", "Bowser's Room", lambda state: bosses.castle_clear(state)),
    connect(multiworld, player, names, "6-4", gamevar.boss_order[10], lambda state: logic._64Clear(state))

    if get_option_value(multiworld, player, "extras_enabled") == 1:
        for i in range(6):
            multiworld.get_region(f'World {i + 1}', player).add_exits([f'{i + 1}-Extra'],
                                                                {f'{i+1}-Extra': lambda state: state.has('Extra Panels', player) or state.has(f'Extra {i + 1}', player)})

    if get_option_value(multiworld, player, "minigame_checks") >= 2:
        for i in range(6):
            multiworld.get_region(f'World {i + 1}', player).add_exits([f'{i + 1}-Bonus'],
                                                                {f'{i+1}-Bonus': lambda state: state.has('Bonus Panels', player) or state.has(f'Bonus {i + 1}', player)})

    



def create_location(player: int, location_data: LocationData, region: Region, location_cache: List[Location]) -> Location:
    location = YILocation(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule
    location.LevelID = location_data.LevelID

    if id is None:
        location.event = True
        location.locked = True

    location_cache.append(location)

    return location

def create_region(multiworld: MultiWorld, player: int, locations_per_region: Dict[str, List[LocationData]], location_cache: List[Location], name: str) -> Region:
    region = Region(name, player, multiworld)
    region.world = multiworld

    if name in locations_per_region:
        for location_data in locations_per_region[name]:
            location = create_location(player, location_data, region, location_cache)
            region.locations.append(location)

    return region

def connectStartingRegion(multiworld: MultiWorld, player: int):
    menu = multiworld.get_region('Menu', player)
    world_main = multiworld.get_region('Overworld', player)

    starting_region = multiworld.get_region(f'World {multiworld.starting_world[player].value + 1}', player)

    load_file = Entrance(player, 'Overworld', menu)
    load_file.connect(world_main)
    menu.connect(world_main, "Start Game")

    starting_world = Entrance(player, 'Overworld', world_main)
    starting_world.connect(starting_region)
    world_main.connect(starting_region, "Overworld")

def connect(multiworld: MultiWorld, player: int, used_names: Dict[str, int], source: str, target: str, rule: Optional[Callable] = None):
    sourceRegion = multiworld.get_region(source, player)
    targetRegion = multiworld.get_region(target, player)

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