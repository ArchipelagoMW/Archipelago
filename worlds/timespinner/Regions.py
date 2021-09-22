from typing import List, Dict, Tuple
from BaseClasses import MultiWorld, Region, Entrance, Location
from .Options import is_option_enabled
from .Locations import LocationData

def create_regions(world: MultiWorld, player: int, pyramid_keys_unlock: str, locations: Dict[str, LocationData]):
    locations_per_region = get_locations_per_region(locations)

    world.regions += [
        create_region(world, player, locations_per_region, 'Menu'),
        create_region(world, player, locations_per_region, 'Tutorial'),
        create_region(world, player, locations_per_region, 'Lake desolation'),
        create_region(world, player, locations_per_region, 'Upper lake desolation'),
        create_region(world, player, locations_per_region, 'Lower lake desolation'),
        create_region(world, player, locations_per_region, 'Libary'),
        create_region(world, player, locations_per_region, 'Libary top'),
        create_region(world, player, locations_per_region, 'Varndagroth tower left'),
        create_region(world, player, locations_per_region, 'Varndagroth tower right (upper)'),
        create_region(world, player, locations_per_region, 'Varndagroth tower right (lower)'),
        create_region(world, player, locations_per_region, 'Varndagroth tower right (elevator)'),
        create_region(world, player, locations_per_region, 'Sealed Caves (Sirens)'),
        create_region(world, player, locations_per_region, 'Militairy Fortress'),
        create_region(world, player, locations_per_region, 'The lab'),
        create_region(world, player, locations_per_region, 'The lab (power off)'),
        create_region(world, player, locations_per_region, 'The lab (upper)'),
        create_region(world, player, locations_per_region, 'Emperors tower'),
        create_region(world, player, locations_per_region, 'Sealed Caves (Xarion)'),
        create_region(world, player, locations_per_region, 'Refugee Camp'),
        create_region(world, player, locations_per_region, 'Forest'),
        create_region(world, player, locations_per_region, 'Left Side forest Caves'),
        create_region(world, player, locations_per_region, 'Upper Lake Sirine'),
        create_region(world, player, locations_per_region, 'Lower Lake Sirine'),
        create_region(world, player, locations_per_region, 'Caves of Banishment (upper)'),
        create_region(world, player, locations_per_region, 'Caves of Banishment (Maw)'),
        create_region(world, player, locations_per_region, 'Caves of Banishment (Sirens)'),
        create_region(world, player, locations_per_region, 'Caste Ramparts'),
        create_region(world, player, locations_per_region, 'Caste Keep'),
        create_region(world, player, locations_per_region, 'Royal towers (lower)'),
        create_region(world, player, locations_per_region, 'Royal towers'),
        create_region(world, player, locations_per_region, 'Royal towers (upper)'),
        create_region(world, player, locations_per_region, 'Ancient Pyramid (left)'),
        create_region(world, player, locations_per_region, 'Ancient Pyramid (right)'),
        create_region(world, player, locations_per_region, 'Space time continuum')
    ]

    connectStartingRegion(world, player)

    connect(world, player, 'Lake desolation', 'Lower lake desolation', lambda state: state._timespinner_has_timestop(world, player or state.has('Talaria Attachment', player))) #TODO | R.GateKittyBoss | R.GateLeftLibrary)
    connect(world, player, 'Lake desolation', 'Upper lake desolation', lambda state: state._timespinner_has_fire(world, player) and state.can_reach('Upper Lake Sirine', 'Region', player))
    connect(world, player, 'Lake desolation', 'Sealed Caves (Xarion)', lambda state: state._timespinner_has_keycard_A(world, player) and state._timespinner_has_doublejump(world, player))
    connect(world, player, 'Lake desolation', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Upper lake desolation', 'Lake desolation')
    connect(world, player, 'Upper lake desolation', 'Lower lake desolation') 
    connect(world, player, 'Lower lake desolation', 'Lake desolation') 
    connect(world, player, 'Lower lake desolation', 'Libary') 
    connect(world, player, 'Lower lake desolation', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Libary', 'Lower lake desolation') 
    connect(world, player, 'Libary', 'Libary top', lambda state: state._timespinner_has_doublejump(world, player) or state.has('Talaria Attachment', player)) 
    connect(world, player, 'Libary', 'Varndagroth tower left', lambda state: state._timespinner_has_keycard_C(world, player))
    connect(world, player, 'Libary', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Libary top', 'Libary')
    connect(world, player, 'Varndagroth tower left', 'Libary')
    connect(world, player, 'Varndagroth tower left', 'Varndagroth tower right (upper)', lambda state: state._timespinner_has_keycard_C(world, player))
    connect(world, player, 'Varndagroth tower left', 'Varndagroth tower right (lower)', lambda state: state._timespinner_has_keycard_B(world, player))
    connect(world, player, 'Varndagroth tower left', 'Sealed Caves (Sirens)', lambda state: state._timespinner_has_keycard_B(world, player) and state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower left', 'Refugee Camp', lambda state: state.has('Timespinner Wheel', player) and state.has('Timespinner Spindle', player))
    connect(world, player, 'Varndagroth tower right (upper)', 'Varndagroth tower left')
    connect(world, player, 'Varndagroth tower right (upper)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (upper)')
    connect(world, player, 'Varndagroth tower right (elevator)', 'Varndagroth tower right (lower)')
    connect(world, player, 'Varndagroth tower right (lower)', 'Varndagroth tower left')
    connect(world, player, 'Varndagroth tower right (lower)', 'Varndagroth tower right (elevator)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower right (lower)', 'Sealed Caves (Sirens)', lambda state: state._timespinner_has_keycard_B(world, player) and state.has('Elevator Keycard', player))
    connect(world, player, 'Varndagroth tower right (lower)', 'Militairy Fortress', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))
    connect(world, player, 'Varndagroth tower right (lower)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Sealed Caves (Sirens)', 'Varndagroth tower left', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Sealed Caves (Sirens)', 'Varndagroth tower right (lower)', lambda state: state.has('Elevator Keycard', player))
    connect(world, player, 'Sealed Caves (Sirens)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Militairy Fortress', 'Varndagroth tower right (lower)', lambda state: state._timespinner_can_kill_all_3_bosses(world, player))
    connect(world, player, 'Militairy Fortress', 'The lab', lambda state: state._timespinner_has_keycard_B(world, player) and state._timespinner_has_doublejump(world, player))
    connect(world, player, 'The lab', 'Militairy Fortress')
    connect(world, player, 'The lab', 'The lab (power off)', lambda state: state._timespinner_has_doublejump_of_npc(world, player))
    connect(world, player, 'The lab (power off)', 'The lab')
    connect(world, player, 'The lab (power off)', 'The lab (upper)', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, 'The lab (upper)', 'The lab (power off)')
    connect(world, player, 'The lab (upper)', 'Emperors tower', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, 'The lab (upper)', 'Ancient Pyramid (left)', lambda state: state.has_all(['Timespinner Wheel', 'Timespinner Spindle', 'Timespinner Gear 1', 'Timespinner Gear 2', 'Timespinner Gear 3'], player))
    connect(world, player, 'Emperors tower', 'The lab (upper)')
    connect(world, player, 'Sealed Caves (Xarion)', 'Lake desolation')
    connect(world, player, 'Sealed Caves (Xarion)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Refugee Camp', 'Forest')
    connect(world, player, 'Refugee Camp', 'Libary', lambda state: is_option_enabled(world, player, "Inverted"))
    connect(world, player, 'Refugee Camp', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Forest', 'Refugee Camp')
    connect(world, player, 'Forest', 'Left Side forest Caves', lambda state: state.has('Talaria Attachment', player) or state._timespinner_has_timestop(world, player))
    connect(world, player, 'Forest', 'Caves of Banishment (Sirens)')
    connect(world, player, 'Forest', 'Caste Ramparts')
    connect(world, player, 'Left Side forest Caves', 'Forest')
    connect(world, player, 'Left Side forest Caves', 'Upper Lake Sirine', lambda state: state._timespinner_has_timestop(world, player))
    connect(world, player, 'Left Side forest Caves', 'Lower Lake Sirine', lambda state: state.has('Water Mask', player))
    connect(world, player, 'Left Side forest Caves', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Upper Lake Sirine', 'Left Side forest Caves')
    connect(world, player, 'Upper Lake Sirine', 'Lower Lake Sirine', lambda state: state.has('Water Mask', player))
    connect(world, player, 'Lower Lake Sirine', 'Upper Lake Sirine')
    connect(world, player, 'Lower Lake Sirine', 'Left Side forest Caves')
    connect(world, player, 'Lower Lake Sirine', 'Caves of Banishment (upper)')
    connect(world, player, 'Caves of Banishment (upper)', 'Upper Lake Sirine', lambda state: state.has('Water Mask', player))
    connect(world, player, 'Caves of Banishment (upper)', 'Caves of Banishment (Maw)')
    connect(world, player, 'Caves of Banishment (upper)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (upper)', lambda state: state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, 'Caves of Banishment (Maw)', 'Caves of Banishment (Sirens)')
    connect(world, player, 'Caves of Banishment (Maw)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Caves of Banishment (Sirens)', 'Forest')
    connect(world, player, 'Caste Ramparts', 'Forest')
    connect(world, player, 'Caste Ramparts', 'Caste Keep')
    connect(world, player, 'Caste Ramparts', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Caste Keep', 'Caste Ramparts')
    connect(world, player, 'Caste Keep', 'Royal towers (lower)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, 'Caste Keep', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Royal towers (lower)', 'Caste Keep')
    connect(world, player, 'Royal towers (lower)', 'Royal towers', lambda state: state.has('Timespinner Wheel', player) or state._timespinner_has_forwarddash_doublejump(world, player))
    connect(world, player, 'Royal towers (lower)', 'Space time continuum', lambda state: state.has('Twin Pyramid Key', player))
    connect(world, player, 'Royal towers', 'Royal towers (lower)')
    connect(world, player, 'Royal towers', 'Royal towers (upper)', lambda state: state._timespinner_has_doublejump(world, player))
    connect(world, player, 'Royal towers (upper)', 'Royal towers')
    connect(world, player, 'Ancient Pyramid (left)', 'The lab (upper)')
    connect(world, player, 'Ancient Pyramid (left)', 'Ancient Pyramid (right)', lambda state: state._timespinner_has_upwarddash(world, player))
    connect(world, player, 'Ancient Pyramid (right)', 'Ancient Pyramid (left)')
    connect(world, player, 'Space time continuum', 'Lake desolation', lambda state: pyramid_keys_unlock == "GateLakeDesolation")
    connect(world, player, 'Space time continuum', 'Lower lake desolation', lambda state: pyramid_keys_unlock == "GateKittyBoss")
    connect(world, player, 'Space time continuum', 'Libary', lambda state: pyramid_keys_unlock == "GateLeftLibrary")
    connect(world, player, 'Space time continuum', 'Varndagroth tower right (lower)', lambda state: pyramid_keys_unlock == "GateMilitairyGate")
    connect(world, player, 'Space time continuum', 'Sealed Caves (Xarion)', lambda state: pyramid_keys_unlock == "GateSealedCaves")
    connect(world, player, 'Space time continuum', 'Sealed Caves (Sirens)', lambda state: pyramid_keys_unlock == "GateSealedSirensCave")
    connect(world, player, 'Space time continuum', 'Left Side forest Caves', lambda state: pyramid_keys_unlock == "GateLakeSirineRight")
    connect(world, player, 'Space time continuum', 'Refugee Camp', lambda state: pyramid_keys_unlock == "GateAccessToPast")
    connect(world, player, 'Space time continuum', 'Caste Ramparts', lambda state: pyramid_keys_unlock == "GateCastleRamparts")
    connect(world, player, 'Space time continuum', 'Caste Keep', lambda state: pyramid_keys_unlock == "GateCastleKeep")
    connect(world, player, 'Space time continuum', 'Royal towers (lower)', lambda state: pyramid_keys_unlock == "GateRoyalTowers")
    connect(world, player, 'Space time continuum', 'Caves of Banishment (Maw)', lambda state: pyramid_keys_unlock == "GateMaw")
    connect(world, player, 'Space time continuum', 'Caves of Banishment (upper)', lambda state: pyramid_keys_unlock == "GateCavesOfBanishment")

class TimespinnerWorldLocation(Location):
    game: str = "Timespinner"

    def __init__(self, player: int, name: str, id, parentRegion, rule):
        super(TimespinnerWorldLocation, self).__init__(player, name, id, parentRegion)
        self.access_rule = rule

        if id is None:
            self.event = True
            self.locked = True

def create_region(world: MultiWorld, player: int, locations_per_region: Dict[str, List[Tuple]], name: str) -> Region:
    region = Region(name, None, name, player)
    region.world = world

    for location, data in locations_per_region[name]:
        if data.region == name:
            location = TimespinnerWorldLocation(player, location, data.code, region, data.rule)
            region.locations.append(location)

    return region

def connectStartingRegion(world: MultiWorld, player: int):
    menu = world.get_region('Menu', player)
    tutorial = world.get_region('Tutorial', player)
    space_time_continuum = world.get_region('Space time continuum', player)

    if is_option_enabled(world, player, "Inverted"):
        starting_region = world.get_region('Refugee Camp', player)
    else:
        starting_region = world.get_region('Lake desolation', player)

    menu_to_tutorial = Entrance(player, 'Tutorial', menu)
    menu_to_tutorial.connect(tutorial)
    menu.exits.append(menu_to_tutorial)

    tutorial_to_start = Entrance(player, 'Start Game', tutorial)
    tutorial_to_start.connect(starting_region)
    tutorial.exits.append(tutorial_to_start)

    teleport_back_to_start = Entrance(player, 'Teleport back to start', space_time_continuum)
    teleport_back_to_start.connect(starting_region)
    space_time_continuum.exits.append(teleport_back_to_start)

def connect(world: MultiWorld, player: int, source: str, target: str, rule=None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)

    connection = Entrance(player, source + ' > ' + target, sourceRegion)

    if rule:
        connection.access_rule = rule

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def get_locations_per_region(locations: Dict[str, LocationData]) -> Dict[str, List[Tuple]]:
    per_region: Dict[str, List[Tuple]]  = {}

    for name, data in locations.items():
        per_region[data.region] = [ ( name, data ) ] if data.region not in per_region else per_region[data.region] + ( name, data )

    return per_region