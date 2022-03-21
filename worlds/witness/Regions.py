from BaseClasses import MultiWorld, Entrance

def makeLambda(panelHexToSolveSet, player):
    return lambda state: state._can_solve_panels(panelHexToSolveSet, player)

def connect(world: MultiWorld, player: int, source: str, target: str, panelHexToSolveSet = None):
    sourceRegion = world.get_region(source, player)
    targetRegion = world.get_region(target, player)
   
    
    connection = Entrance(player, source + " to " + target + " via " + str(panelHexToSolveSet), sourceRegion)

    connection.access_rule = makeLambda(panelHexToSolveSet, player)

    sourceRegion.exits.append(connection)
    connection.connect(targetRegion)

def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table, event_location_table
    from .full_logic import ALL_REGIONS_BY_NAME, CHECKS_BY_HEX

    world.regions += [
        create_region(world, player, 'Menu', None, ["The Splashscreen?"]),
    ]
    
    allLocationsAccordingToRegions = set()
    allLocationsAccordingToLocationTable = set(location_table.keys())


    for regionName, region in ALL_REGIONS_BY_NAME.items():        
        locationsForThisRegion = [CHECKS_BY_HEX[panel]["checkName"] for panel in region["panels"] if CHECKS_BY_HEX[panel]["checkName"] in location_table]
        locationsForThisRegion += [CHECKS_BY_HEX[panel]["checkName"] + " Solved" for panel in region["panels"] if CHECKS_BY_HEX[panel]["checkName"] + " Solved" in event_location_table]
        
        
        allLocationsAccordingToRegions = allLocationsAccordingToRegions | set(locationsForThisRegion)
       
        
        world.regions += [create_region(world, player, regionName, locationsForThisRegion)]
        
    for regionName, region in ALL_REGIONS_BY_NAME.items():
        for connection in region["connections"]:
            if connection[0] == "Entry":
                continue
            connect(world, player, regionName, connection[0], connection[1])
            connect(world, player, connection[0], regionName, connection[1])

    world.get_entrance("The Splashscreen?", player).connect(world.get_region('First Hallway', player))