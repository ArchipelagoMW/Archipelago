from typing import List, Dict, Tuple
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Locations import LocationData
from .extended_logic import logic_helpers

class SAI2Location(Location):
    game: str = "Super Adventure Island II"

def __init__(self, player: int, name: str = " ", address: int = None, parent=None):
    super().__init__(player, name, address, parent)


def init_areas(world, locations: Tuple[LocationData, ...]):
    multiworld = world.multiworld
    player = world.player
    location_cache = world.location_cache
    logic = logic_helpers(world)

    locations_per_region = get_locations_per_region(locations)

    regions = [
        create_region(multiworld, player, locations_per_region, location_cache, 'Menu'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Southern Sea'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Western Sea'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Northwestern Sea'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Northeastern Sea'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Southeastern Sea'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Eastern Sea'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Poka-Poka Island'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Poka-Poka East'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Boa-Boa Island'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Hiya-Hiya Entrance'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Hiya-Hiya Underside'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Hiya-Hiya Main'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Hiya-Hiya Back'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Puka-Puka Island'),
        create_region(multiworld, player, locations_per_region, location_cache, 'Puka-Puka Switch Room'),
        create_region(multiworld, player, locations_per_region, location_cache, "Curly's Casino"),
        create_region(multiworld, player, locations_per_region, location_cache, "Sala-Sala Island"),
        create_region(multiworld, player, locations_per_region, location_cache, "Sala-Sala Backside"),
        create_region(multiworld, player, locations_per_region, location_cache, "Fuwa-Fuwa Island")

    ]
    multiworld.regions += regions

    multiworld.get_region('Menu', player).add_exits(["Southern Sea"])

    multiworld.get_region('Southern Sea', player).add_exits(['Poka-Poka Island', 'Fuwa-Fuwa Island', 'Western Sea', 'Southeastern Sea'],
                                                        {'Fuwa-Fuwa Island': lambda state: logic.fuwa_access(state), #Fuwa island is in the south sea
                                                        'Western Sea': lambda state: state.has("Light Gate Lowered", player), #Light gate
                                                        'Southeastern Sea': lambda state: state.has("Aqua Gate Lowered", player)}) #Aqua gate
    multiworld.get_region('Poka-Poka Island', player).add_exits(["Poka-Poka East"],{"Poka-Poka East": lambda state: state.has("Silver Sword", player)}) #Breakable rocks leading from the start to the back
    multiworld.get_region('Poka-Poka East', player).add_exits(["Fuwa-Fuwa Island", "Poka-Poka Island"],{"Fuwa-Fuwa Island": lambda state: state.has_all({"Shovel", "Fuwa-Poka Shortcut Open"}, player)}) #Shortcut to Fuwa-Fuwa, poka can be reached always
    multiworld.get_region('Western Sea', player).add_exits(['Boa-Boa Island', 'Northwestern Sea'],
                                                        {'Boa-Boa Island': lambda state: state.has("Sun Ring", player), #Sun ring opens island
                                                        'Northwestern Sea': lambda state: state.has("Sun Gate Lowered", player)}) #Sun Gate

    multiworld.get_region('Boa-Boa Island', player).add_exits(['Western Sea', 'Hiya-Hiya Underside', 'Northwestern Sea', 'Hiya-Hiya Entrance'],
                                                        {'Western Sea': lambda state: state.has("Wand", player), #May not need wand.
                                                        'Hiya-Hiya Underside':  lambda state: state.has_all({"Shovel", "Fire Sword", "Boa-Hiya Shortcut Open"}, player),#Shortcut leads to this but blocked by an ice wall
                                                        'Hiya-Hiya Entrance':  lambda state: state.has_all({"Wand", "Shovel", "Shove", "Boa-Hiya Shortcut Open"}, player),#Same as above, but needs Wand to warp to the start
                                                        'Northwestern Sea':  lambda state: state.has_all({"Wand", "Shovel", "Boa-Hiya Shortcut Open"}, player)})#Same as above but doesn't need shove
    multiworld.get_region('Northwestern Sea', player).add_exits(['Hiya-Hiya Entrance', 'Western Sea', 'Northeastern Sea'],
                                                        {'Hiya-Hiya Entrance': lambda state: state.has_all({"Ice Bell", "Shove"}, player), #Intended access
                                                        'Western Sea': lambda state: state.has("Sun Gate Lowered", player),#Sun Gate
                                                        'Northeastern Sea': lambda state: state.has("Star Gate Lowered", player)})#Star Gate
    multiworld.get_region('Hiya-Hiya Entrance', player).add_exits(['Hiya-Hiya Underside', 'Hiya-Hiya Main', 'Northwestern Sea'],
                                                        {'Northwestern Sea': lambda state: state.has("Wand", player),
                                                        'Hiya-Hiya Underside': lambda state: state.has("Shovel", player),
                                                        'Hiya-Hiya Main': lambda state: state.has("Fire Sword", player)})
    multiworld.get_region('Hiya-Hiya Underside', player).add_exits(['Boa-Boa Island'],
                                                        {'Boa-Boa Island': lambda state: state.has_all({"Boa-Hiya Shortcut Open", "Fire Sword"}, player)})
    multiworld.get_region('Hiya-Hiya Main', player).add_exits(['Hiya-Hiya Entrance', "Sala-Sala Backside", "Sala-Sala Island", "Hiya-Hiya Back", "Northwestern Sea"],#Northwestern sea?
                                                        {'Hiya-Hiya Entrance': lambda state: (state.has("Fire Sword", player)) or (state.has_all({"Wand", "Shove"}, player)),
                                                        'Hiya-Hiya Back': lambda state: state.has("Shove", player),
                                                         "Sala-Sala Backside": lambda state: (state.has_all({"Shove", "Sala-Hiya Shortcut Open", "Down Jab"}, player) and logic.star_switch_on(state) and state.has_group("Swords", player, 1)),
                                                         "Sala-Sala Island": lambda state: (state.has_all({"Shove", "Sala-Hiya Shortcut Open", "Wand", "Down Jab"}, player) and logic.star_switch_on(state) and state.has_group("Swords", player, 1) and logic.has_early_health(state)),
                                                         "Northwestern Sea": lambda state: state.has("Wand", player)})
    multiworld.get_region('Hiya-Hiya Back', player).add_exits(['Hiya-Hiya Main', "Hiya-Hiya Entrance"],
                                                    {'Hiya-Hiya Main': lambda state: state.has("Shove", player),
                                                     'Hiya-Hiya Entrance': lambda state: state.has("Wand", player)})
    multiworld.get_region('Southeastern Sea', player).add_exits(['Southern Sea', 'Eastern Sea', 'Northeastern Sea', "Curly's Casino"],
                                                        {'Southern Sea': lambda state: state.has("Aqua Gate Lowered", player),
                                                        'Northeastern Sea': lambda state: state.has("Moon Gate Lowered", player),
                                                        'Eastern Sea': lambda state: state.has("Moon Gate Lowered", player),
                                                        "Curly's Casino": lambda state: state.has("Power Fan", player)})
    multiworld.get_region("Curly's Casino", player).add_exits(['Southeastern Sea', "Puka-Puka Island"],
                                                {'Puka-Puka Island': lambda state: state.has("Shovel", player)})
    multiworld.get_region("Puka-Puka Island", player).add_exits(["Curly's Casino", "Puka-Puka Switch Room", "Fuwa-Fuwa Island"],
                                                {"Curly's Casino": lambda state: state.has("Shovel", player),
                                                "Puka-Puka Switch Room": lambda state: state.has("Puka-Puka Drained", player),
                                                "Fuwa-Fuwa Island": lambda state: state.has_all({"Fuwa-Puka Shortcut Open", "Puka-Puka Drained"}, player) and ((state.has_group("Swords", player, 1) and state.has("Down Jab", player)) or state.has("Wand", player))})
    multiworld.get_region("Puka-Puka Switch Room", player).add_exits(["Curly's Casino", "Sala-Sala Island", "Puka-Puka Island"],
                                                {"Curly's Casino": lambda state: state.has("Wand", player),
                                                "Sala-Sala Island": lambda state: state.has("Sala-Puka Shortcut Open", player) and logic.has_early_health(state),
                                                "Puka-Puka Island": lambda state: state.has("Puka-Puka Drained", player)})
    multiworld.get_region("Eastern Sea", player).add_exits(['Southeastern Sea', "Sala-Sala Island"],
                                                {'Southeastern Sea': lambda state: state.has("Moon Gate Lowered", player),
                                                 "Sala-Sala Island": lambda state: logic.has_early_health(state)})
    multiworld.get_region("Sala-Sala Island", player).add_exits(['Eastern Sea', "Sala-Sala Backside", "Puka-Puka Switch Room"],
                                                {'Sala-Sala Backside': lambda state: logic.moon_switch_on(state) and state.has_all({"Shovel", "Shove"}, player),
                                                'Pula-Puka Switch Room': lambda state: logic.moon_switch_on(state) and state.has_all({"Shovel", "Shove"}, player)})
    multiworld.get_region("Sala-Sala Backside", player).add_exits(['Sala-Sala Island', "Hiya-Hiya Back"],
                                                {'Hiya-Hiya Back': lambda state: state.has("Sala-Hiya Shortcut Open", player)})
    multiworld.get_region('Fuwa-Fuwa Island', player).add_exits(['Southern Sea', 'Poka-Poka East', "Puka-Puka Island", "Curly's Casino"],
                                                        {'Poka-Poka East': lambda state: state.has_all({"Shovel", "Fuwa-Poka Shortcut Open"}, player), #CHECK THIS!!!! 
                                                        'Puka-Puka Island': lambda state: state.has_all({"Down Jab", "Power Sword", "Fuwa-Puka Shortcut Open", "Puka-Puka Drained"}, player),
                                                        "Curly's Casino": lambda state: state.has_all({"Down Jab", "Power Sword", "Fuwa-Puka Shortcut Open", "Wand"}, player)})
    multiworld.get_region('Northeastern Sea', player).add_exits(['Northwestern Sea', 'Southeastern Sea'], #Irrelevant except with random open gates
                                                        {'Northwestern Sea': lambda state: state.has("Star Gate Lowered", player),
                                                        'Southeastern Sea': lambda state: state.has("Moon Gate Lowered", player)})

def create_location(player: int, location_data: LocationData, region: Region, location_cache: List[Location]) -> Location:
    location = SAI2Location(player, location_data.name, location_data.code, region)
    location.access_rule = location_data.rule

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


def get_locations_per_region(locations: Tuple[LocationData, ...]) -> Dict[str, List[LocationData]]:
    per_region: Dict[str, List[LocationData]] = {}

    for location in locations:
        per_region.setdefault(location.region, []).append(location)

    return per_region
