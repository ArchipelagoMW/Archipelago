from typing import List, Set, Dict, Tuple, Optional, Callable
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import LocationData
from .Options import get_option_value
from .SetupBosses import BossReqs

def create_regions(world: MultiWorld, player: int, locations: Tuple[LocationData, ...], location_cache: List[Location]):
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
        create_region(world, player, locations_per_region, location_cache, 'Hop! Hop! Donut Lifts'),
        create_region(world, player, locations_per_region, location_cache, 'Shy-Guys On Stilts'),
        create_region(world, player, locations_per_region, location_cache, 'Touch Fuzzy Get Dizzy'),
        create_region(world, player, locations_per_region, location_cache, "Salvo The Slime's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Poochy Ain't Stupid"),
        create_region(world, player, locations_per_region, location_cache, "Flip Cards"),

        create_region(world, player, locations_per_region, location_cache, "Visit Koopa And Para-Koopa"),
        create_region(world, player, locations_per_region, location_cache, "The Baseball Boys"),
        create_region(world, player, locations_per_region, location_cache, "What's Gusty Taste Like?"),
        create_region(world, player, locations_per_region, location_cache, "Bigger Boo's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Watch Out For Lakitu"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of The Mystery Maze"),
        create_region(world, player, locations_per_region, location_cache, "Lakitu's Wall"),
        create_region(world, player, locations_per_region, location_cache, "The Potted Ghost's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Hit That Switch!!"),
        create_region(world, player, locations_per_region, location_cache, "Scratch And Match"),

        create_region(world, player, locations_per_region, location_cache, "Welcome To Monkey World!"),
        create_region(world, player, locations_per_region, location_cache, "Jungle Rhythm..."),
        create_region(world, player, locations_per_region, location_cache, "Nep-Enuts' Domain"),
        create_region(world, player, locations_per_region, location_cache, "Prince Froggy's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Jammin' Through The Trees"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of Harry Hedgehog"),
        create_region(world, player, locations_per_region, location_cache, "Monkeys' Favorite Lake"),
        create_region(world, player, locations_per_region, location_cache, "Naval Piranha's Castle"),
        create_region(world, player, locations_per_region, location_cache, "More Monkey Madness"),
        create_region(world, player, locations_per_region, location_cache, "Drawing Lots"),

        create_region(world, player, locations_per_region, location_cache, "GO! GO! MARIO!!"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of The Lakitus"),
        create_region(world, player, locations_per_region, location_cache, "Don't Look Back!"),
        create_region(world, player, locations_per_region, location_cache, "Marching Milde's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Chomp Rock Zone"),
        create_region(world, player, locations_per_region, location_cache, "Lake Shore Paradise"),
        create_region(world, player, locations_per_region, location_cache, "Ride Like The Wind"),
        create_region(world, player, locations_per_region, location_cache, "Hookbill The Koopa's Castle"),
        create_region(world, player, locations_per_region, location_cache, "The Impossible? Maze"),
        create_region(world, player, locations_per_region, location_cache, "Match Cards"),

        create_region(world, player, locations_per_region, location_cache, "BLIZZARD!!!"),
        create_region(world, player, locations_per_region, location_cache, "Ride The Ski Lifts"),
        create_region(world, player, locations_per_region, location_cache, "Danger - Icy Conditions Ahead"),
        create_region(world, player, locations_per_region, location_cache, "Sluggy The Unshaven's Fort"),
        create_region(world, player, locations_per_region, location_cache, "Goonie Rides!"),
        create_region(world, player, locations_per_region, location_cache, "Welcome To Cloud World"),
        create_region(world, player, locations_per_region, location_cache, "Shifting Platforms Ahead"),
        create_region(world, player, locations_per_region, location_cache, "Raphael The Raven's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Kamek's Revenge"),
        create_region(world, player, locations_per_region, location_cache, "Roulette"),

        create_region(world, player, locations_per_region, location_cache, "Scary Skeleton Goonies!"),
        create_region(world, player, locations_per_region, location_cache, "The Cave Of The Bandits"),
        create_region(world, player, locations_per_region, location_cache, "Beware The Spinning Logs"),
        create_region(world, player, locations_per_region, location_cache, "Tap-Tap The Red Nose's Fort"),
        create_region(world, player, locations_per_region, location_cache, "The Very Loooooong Cave"),
        create_region(world, player, locations_per_region, location_cache, "The Deep, Underground Maze"),
        create_region(world, player, locations_per_region, location_cache, "KEEP MOVING!!!!"),
        create_region(world, player, locations_per_region, location_cache, "King Bowser's Castle"),
        create_region(world, player, locations_per_region, location_cache, "Bowser's Room"),
        create_region(world, player, locations_per_region, location_cache, "Castles - Masterpiece Set"),
        create_region(world, player, locations_per_region, location_cache, "Slot Machine")


    ]

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

    connect(world, player, names, 'World 1', 'Make Eggs, Throw Eggs'),
    connect(world, player, names, 'World 1', 'Watch Out Below!'),
    connect(world, player, names, 'World 1', 'The Cave Of Chomp Rock'),
    connect(world, player, names, 'World 1', "Burt The Bashful's Fort"),
    connect(world, player, names, 'World 1', "Hop! Hop! Donut Lifts"),
    connect(world, player, names, 'World 1', "Shy-Guys On Stilts"),
    connect(world, player, names, 'World 1', "Touch Fuzzy Get Dizzy"),
    connect(world, player, names, 'World 1', "Salvo The Slime's Castle"),
    connect(world, player, names, 'World 1', "Poochy Ain't Stupid", lambda state: state.has('Extra Panels', player) or state.has('Extra 1', player)),
    connect(world, player, names, 'World 1', "Flip Cards", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 1', player)),

    connect(world, player, names, 'World 2', "Visit Koopa And Para-Koopa"),
    connect(world, player, names, 'World 2', "The Baseball Boys"),
    connect(world, player, names, 'World 2', "What's Gusty Taste Like?"),
    connect(world, player, names, 'World 2', "Bigger Boo's Fort"),
    connect(world, player, names, 'World 2', "Watch Out For Lakitu"),
    connect(world, player, names, 'World 2', "The Cave Of The Mystery Maze"),
    connect(world, player, names, 'World 2', "Lakitu's Wall"),
    connect(world, player, names, 'World 2', "The Potted Ghost's Castle"),
    connect(world, player, names, 'World 2', "Hit That Switch!!", lambda state: state.has('Extra Panels', player) or state.has('Extra 2', player)),
    connect(world, player, names, 'World 2', "Scratch And Match", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 2', player)),

    connect(world, player, names, 'World 3', "Welcome To Monkey World!"),
    connect(world, player, names, 'World 3', "Jungle Rhythm..."),
    connect(world, player, names, 'World 3', "Nep-Enuts' Domain"),
    connect(world, player, names, 'World 3', "Prince Froggy's Fort"),
    connect(world, player, names, 'World 3', "Jammin' Through The Trees"),
    connect(world, player, names, 'World 3', "The Cave Of Harry Hedgehog"),
    connect(world, player, names, 'World 3', "Monkeys' Favorite Lake"),
    connect(world, player, names, 'World 3', "Naval Piranha's Castle"),
    connect(world, player, names, 'World 3', "More Monkey Madness", lambda state: state.has('Extra Panels', player) or state.has('Extra 3', player)),
    connect(world, player, names, 'World 3', "Drawing Lots", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 3', player)),

    connect(world, player, names, 'World 4', "GO! GO! MARIO!!"),
    connect(world, player, names, 'World 4', "The Cave Of The Lakitus"),
    connect(world, player, names, 'World 4', "Don't Look Back!"),
    connect(world, player, names, 'World 4', "Marching Milde's Fort"),
    connect(world, player, names, 'World 4', "Chomp Rock Zone"),
    connect(world, player, names, 'World 4', "Lake Shore Paradise"),
    connect(world, player, names, 'World 4', "Ride Like The Wind"),
    connect(world, player, names, 'World 4', "Hookbill The Koopa's Castle"),
    connect(world, player, names, 'World 4', "The Impossible? Maze", lambda state: state.has('Extra Panels', player) or state.has('Extra 4', player)),
    connect(world, player, names, 'World 4', "Match Cards", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 4', player)),

    connect(world, player, names, 'World 5', "BLIZZARD!!!"),
    connect(world, player, names, 'World 5', "Ride The Ski Lifts"),
    connect(world, player, names, 'World 5', "Danger - Icy Conditions Ahead"),
    connect(world, player, names, 'World 5', "Sluggy The Unshaven's Fort"),
    connect(world, player, names, 'World 5', "Goonie Rides!"),
    connect(world, player, names, 'World 5', "Welcome To Cloud World"),
    connect(world, player, names, 'World 5', "Shifting Platforms Ahead"),
    connect(world, player, names, 'World 5', "Raphael The Raven's Castle"),
    connect(world, player, names, 'World 5', "Kamek's Revenge", lambda state: state.has('Extra Panels', player) or state.has('Extra 5', player)),
    connect(world, player, names, 'World 5', "Roulette", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 5', player)),

    connect(world, player, names, 'World 6', "Scary Skeleton Goonies!"),
    connect(world, player, names, 'World 6', "The Cave Of The Bandits"),
    connect(world, player, names, 'World 6', "Beware The Spinning Logs"),
    connect(world, player, names, 'World 6', "Tap-Tap The Red Nose's Fort"),
    connect(world, player, names, 'World 6', "The Very Loooooong Cave"),
    connect(world, player, names, 'World 6', "The Deep, Underground Maze"),
    connect(world, player, names, 'World 6', "KEEP MOVING!!!!"),
    connect(world, player, names, 'World 6', "King Bowser's Castle", lambda state: bosses.castle_access(state)),
    connect(world, player, names, "King Bowser's Castle", "Bowser's Room", lambda state: bosses.castle_clear(state)),
    connect(world, player, names, 'World 6', "Castles - Masterpiece Set", lambda state: state.has('Extra Panels', player) or state.has('Extra 6', player)),
    connect(world, player, names, 'World 6', "Slot Machine", lambda state: state.has('Bonus Panels', player) or state.has('Bonus 6', player))

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