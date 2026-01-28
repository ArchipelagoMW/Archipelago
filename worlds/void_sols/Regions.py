import typing

from BaseClasses import MultiWorld, Region, Entrance
from .Locations import VoidSolsLocation
from .Names import LocationName, ItemName
from .Rules import can_blow_up_wall
from worlds.generic.Rules import add_rule, set_rule
from worlds.AutoWorld import World


def create_regions(world: World, active_locations):
    """
    Creates all regions for the game and assigns locations to them.
    """
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    # Define region names
    region_names = [
        "Menu",
        "Prison",
        "Prison Yard",
        "Prison Portal Room",
        "Forest",
        "Village",
        "Village Undercroft Forgotten Reliquary",
        "Mountain",
        "Mountain Underpass",
        "Mines Floor 1",
        "Mines Floor 2",
        "Mines Floor 3",
        "Mines Floor 4",
        "Cultist Compound",
        "Supermax Prison West",
        "Supermax Prison East",
        "Factory",
        "Swamp",

        # Apex Split (Massive area broken down by access keys)
        "Apex Outskirts",
        "Apex",
    ]

    # Initialize location buckets
    locations_by_region = {name: [] for name in region_names}

    # Sort locations into regions
    for location_name in active_locations:
        # -- PRISON AREA --
        # These specific checks are not accessible until the player has made it to the village
        if location_name in [
            LocationName.prison_wall_portal_1,
            LocationName.prison_wall_portal_2,
            LocationName.prison_wall_portal_3,
            LocationName.prison_item_pickup_caltrops
        ]:
            locations_by_region["Prison Portal Room"].append(location_name)
        elif location_name.startswith(LocationName.PRISON_YARD_PREFIX):
            locations_by_region["Prison Yard"].append(location_name)
        elif location_name.startswith(LocationName.PRISON_PREFIX):
            locations_by_region["Prison"].append(location_name)

        # -- FOREST AREA --
        elif location_name.startswith(LocationName.FOREST_PREFIX):
            locations_by_region["Forest"].append(location_name)

        # -- VILLAGE AREA --
        elif location_name in [
            LocationName.village_torch_forgotten_reliquary,
            LocationName.village_relics_improved_1,
            LocationName.village_relics_improved_2,
            LocationName.village_relics_improved_3,
            LocationName.village_relics_improved_4,
            LocationName.village_relics_improved_5,
        ]:
            locations_by_region["Village Undercroft Forgotten Reliquary"].append(location_name)
        elif location_name.startswith(LocationName.VILLAGE_PREFIX):
            locations_by_region["Village"].append(location_name)

        # -- MOUNTAIN AREA --
        elif location_name.startswith(LocationName.MOUNTAIN_UNDERPASS_PREFIX):
            locations_by_region["Mountain Underpass"].append(location_name)
        elif location_name.startswith(LocationName.MOUNTAIN_PREFIX):
            locations_by_region["Mountain"].append(location_name)

        # -- MINES AREA --
        elif location_name.startswith(LocationName.MINES_0F_PREFIX) or location_name.startswith(LocationName.MINES_1F_PREFIX):
            locations_by_region["Mines Floor 1"].append(location_name)
        elif location_name.startswith(LocationName.MINES_2F_PREFIX):
            locations_by_region["Mines Floor 2"].append(location_name)
        elif location_name.startswith(LocationName.MINES_3F_PREFIX):
            locations_by_region["Mines Floor 3"].append(location_name)
        elif location_name.startswith(LocationName.MINES_4F_PREFIX):
            locations_by_region["Mines Floor 4"].append(location_name)

        # -- CULTIST AREA --
        elif location_name.startswith(LocationName.CULTIST_PREFIX) or location_name.startswith(LocationName.CULTIST_COMPOUND_PREFIX):
            locations_by_region["Cultist Compound"].append(location_name)

        # -- SUPERMAX AREA --
        elif location_name.startswith(LocationName.SUPERMAX_WEST_PREFIX):
            locations_by_region["Supermax Prison West"].append(location_name)
        elif location_name.startswith(LocationName.SUPERMAX_EAST_PREFIX):
            locations_by_region["Supermax Prison East"].append(location_name)

        # -- FACTORY & SWAMP --
        elif location_name.startswith(LocationName.FACTORY_PREFIX):
            locations_by_region["Factory"].append(location_name)
        elif location_name.startswith(LocationName.SWAMP_PREFIX):
            locations_by_region["Swamp"].append(location_name)

        # -- APEX AREA (Split logic) --
        elif location_name.startswith(LocationName.APEX_OUTSKIRTS_PREFIX):
            locations_by_region["Apex Outskirts"].append(location_name)
        elif location_name.startswith(LocationName.APEX_PREFIX):
            if "Outskirts" in location_name or location_name == LocationName.apex_gatekeeper_defeated_event:
                locations_by_region["Apex Outskirts"].append(location_name)
            elif location_name == LocationName.apex_blow_horn:
                # Apex Blow Horn is in Apex Outskirts, but requires Blizzard Talisman
                locations_by_region["Apex Outskirts"].append(location_name)
            else:
                # Default everything else (Hub, Castle, King, etc.) to the main Hub
                locations_by_region["Apex"].append(location_name)

        else:
            # Fallback (Hidden rooms, etc.)
            locations_by_region["Menu"].append(location_name)

    # Create regions
    regions = []
    for name in region_names:
        regions.append(create_region(multiworld, player, active_locations, name, locations_by_region[name]))

    multiworld.regions += regions


def connect_regions(world: World):
    """
    Connects regions together with entrances and rules.
    """
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    # Basic connections
    connect(world, "Menu", "Prison")
    connect(world, "Prison", "Prison Yard", lambda state: state.has(ItemName.prison_warden_defeated_event, player))

    connect(world, "Prison Yard", "Forest", lambda state: state.has(ItemName.gate_key, player))

    # Forest -> Village (Open, no locks)
    connect(world, "Forest", "Village")
    
    # Village -> Prison Portal Room
    connect(world, "Village", "Prison Portal Room")

    # Village -> Village Undercroft Forgotten Reliquary (Locked by Greater Void Worm Defeated)
    connect(world, "Village", "Village Undercroft Forgotten Reliquary",
            lambda state: state.has(ItemName.greater_void_worm_defeated_event, player))

    # Forest -> Mountain (Locked by Outpost Key)
    connect(world, "Forest", "Mountain", lambda state: state.has(ItemName.mountain_outpost_key, player))
    # Forest -> Mines (Locked by Entrance Lift Key)
    connect(world, "Forest", "Mines Floor 1", lambda state: state.has(ItemName.mine_entrance_lift_key, player))

    # Forest -> Apex Outskirts (Two methods from Forest)
    # 1. Key, 2. Dynamite (or Mine Entrance Lift Key which implies access to mines/explosives)
    connect(world, "Forest", "Apex Outskirts",
            lambda state: state.has(ItemName.apex_outskirts_key, player) or can_blow_up_wall(state, player))
    
    # Mines -> Apex Outskirts (Barrel explosion, accessible if in Mines)
    connect(world, "Mines Floor 1", "Apex Outskirts")

    connect(world, "Mountain", "Mountain Underpass")
    
    connect(world, "Village", "Mines Floor 1", lambda state: state.has(ItemName.mine_entrance_lift_key, player))
    
    # Mines Progression
    # Floor 1 -> Floor 2 (Locked by Minecart Wheel)
    connect(world, "Mines Floor 1", "Mines Floor 2", lambda state: state.has(ItemName.minecart_wheel, player))
    
    # Floor 2 -> Floor 3 (Locked by Lift Key)
    connect(world, "Mines Floor 2", "Mines Floor 3", lambda state: state.has(ItemName.lift_key, player))
    
    # Floor 3 -> Floor 4 (Locked by Pit Catwalk Key)
    connect(world, "Mines Floor 3", "Mines Floor 4", lambda state: state.has(ItemName.pit_catwalk_key, player))

    # Mines 4F -> Mountain Underpass (Locked by Temple of the Deep Key)
    connect(world, "Mines Floor 4", "Mountain Underpass", lambda state: state.has(ItemName.temple_of_the_deep_key, player))

    # Mountain Underpass -> Mountain (Elevator)
    connect(world, "Mountain Underpass", "Mountain")

    # Mountain Underpass -> Cultist Compound
    connect(world, "Mountain Underpass", "Cultist Compound")

    # Forest -> Supermax Prison (Locked by Greater Void Worm Defeated)
    # Require East Wing Key to enter to prevent softlock (one-way entrance)
    # However, since East Wing Key is now placed in Supermax Prison West, we remove the key requirement
    # so the player can enter, get the key, and then proceed.
    connect(world, "Forest", "Supermax Prison West",
            lambda state: state.has(ItemName.greater_void_worm_defeated_event, player))

    # Supermax Prison West -> Supermax Prison East (Locked by East Wing Key)
    connect(world, "Supermax Prison West", "Supermax Prison East", lambda state: state.has(ItemName.east_wing_key, player))

    # Supermax Prison East -> Forest (Exit)
    connect(world, "Supermax Prison East", "Forest")
    
    connect(world, "Village", "Factory", lambda state: state.has(ItemName.forest_poacher_defeated_event, player))
    connect(world, "Factory", "Swamp")

    # Apex Connections
    connect(world, "Apex Outskirts", "Apex", lambda state: state.has(ItemName.apex_gatekeeper_defeated_event, player))
    connect(world, "Apex", "Factory")


def create_region(multiworld: MultiWorld, player: int, active_locations, name: str, locations=None):
    ret = Region(name, player, multiworld)
    if locations:
        for locationName in locations:
            if locationName in active_locations:
                loc_id = active_locations[locationName]
                location = VoidSolsLocation(player, locationName, loc_id, ret)
                ret.locations.append(location)

    return ret

def add_location_to_region(multiworld: MultiWorld, player: int, active_locations, region_name: str, location_name: str,
                           rule: typing.Optional[typing.Callable] = None):
    region = multiworld.get_region(region_name, player)
    if location_name in active_locations:
        loc_id = active_locations[location_name]
        location = VoidSolsLocation(player, location_name, loc_id, region)
        region.locations.append(location)
        if rule:
            add_rule(location, rule)


def connect(world: World, source: str, target: str,
            rule: typing.Optional[typing.Callable] = None):
    source_region: Region = world.get_region(source)
    target_region: Region = world.get_region(target)
    source_region.connect(target_region, rule=rule)
