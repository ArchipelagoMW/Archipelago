import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import VoidSolsLocation
from .Names import LocationName, ItemName
from worlds.generic.Rules import add_rule, set_rule
from worlds.AutoWorld import World


def create_regions(world: World, active_locations):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    # Define region names
    region_names = [
        "Menu",
        "Prison",
        "Prison Yard",
        "Forest",
        "Village",
        "Mountain",
        "Mountain Underpass",
        "Mines",
        "Cultist Compound",
        "Supermax Prison",
        "Factory",
        "Swamp",
        "Apex"
    ]

    # Initialize location buckets
    locations_by_region = {name: [] for name in region_names}

    # Sort locations into regions
    for location_name in active_locations:
        if location_name.startswith("Prison Yard - "):
            locations_by_region["Prison Yard"].append(location_name)
        elif location_name.startswith("Prison - "):
            locations_by_region["Prison"].append(location_name)
        elif location_name.startswith("Forest - "):
            locations_by_region["Forest"].append(location_name)
        elif location_name.startswith("Village - "):
            locations_by_region["Village"].append(location_name)
        elif location_name.startswith("Mountain Underpass - "):
            locations_by_region["Mountain Underpass"].append(location_name)
        elif location_name.startswith("Mountain - "):
            locations_by_region["Mountain"].append(location_name)
        elif location_name.startswith("Mines - "):
            locations_by_region["Mines"].append(location_name)
        elif location_name.startswith("Cultist - ") or location_name.startswith("Cultist Compound - "):
            locations_by_region["Cultist Compound"].append(location_name)
        elif location_name.startswith("Supermax Prison - "):
            locations_by_region["Supermax Prison"].append(location_name)
        elif location_name.startswith("Factory - "):
            locations_by_region["Factory"].append(location_name)
        elif location_name.startswith("Swamp - "):
            locations_by_region["Swamp"].append(location_name)
        elif location_name.startswith("Apex - "):
            locations_by_region["Apex"].append(location_name)
        else:
            # Fallback for any unclassified locations
            pass

    # Create regions
    regions = []
    for name in region_names:
        regions.append(create_region(multiworld, player, active_locations, name, locations_by_region[name]))

    multiworld.regions += regions


def connect_regions(world: World):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    # Basic connections
    connect(world, "Menu", "Prison")
    connect(world, "Prison", "Prison Yard")

    connect(world, "Prison Yard", "Forest", lambda state: state.has(ItemName.gate_key, player))

    connect(world, "Forest", "Village", lambda state: state.has(ItemName.forest_bridge_key, player))

    connect(world, "Village", "Mountain", lambda state: state.has(ItemName.mountain_outpost_key, player))
    connect(world, "Mountain", "Mountain Underpass")
    
    connect(world, "Village", "Mines", lambda state: state.has(ItemName.mine_entrance_lift_key, player))
    connect(world, "Mines", "Cultist Compound")
    connect(world, "Cultist Compound", "Supermax Prison")
    
    connect(world, "Village", "Swamp")
    connect(world, "Village", "Factory")
    
    connect(world, "Forest", "Apex")
    connect(world, "Factory", "Apex", lambda state: state.has(ItemName.apex_outskirts_key, player))


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            loc_id = active_locations.get(locationName, 0)
            if loc_id:
                location = VoidSolsLocation(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret

def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str,
                           rule: typing.Optional[typing.Callable] = None):
    region = multiworld.get_region(region_name, player)
    loc_id = active_locations.get(location_name, 0)
    if loc_id:
        location = VoidSolsLocation(player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)


def connect(world: World, source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region: Region = world.get_region(source)
    target_region: Region = world.get_region(target)
    source_region.connect(target_region, rule=rule)
