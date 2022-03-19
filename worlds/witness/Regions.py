from BaseClasses import MultiWorld, Entrance

def makeLambda(panelHexToSolveSet, player):
    return lambda state: state._has_event_items(panelHexToSolveSet, player)

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
    from .FullLogic import allRegionsByName, checksByHex

    world.regions += [
        create_region(world, player, 'Menu', None, ["The Splashscreen?"]),
    ]
    
    allLocationsAccordingToRegions = set()
    allLocationsAccordingToLocationTable = set(location_table.keys())


    for regionName, region in allRegionsByName.items():        
        locationsForThisRegion = [checksByHex[panel]["checkName"] for panel in region["panels"] if checksByHex[panel]["checkName"] in location_table]
        locationsForThisRegion += [checksByHex[panel]["checkName"] + " Event" for panel in region["panels"] if checksByHex[panel]["checkName"] + " Event" in event_location_table]
        
        allLocationsAccordingToRegions = allLocationsAccordingToRegions | set(locationsForThisRegion)
       
        
        world.regions += [create_region(world, player, regionName, locationsForThisRegion)]
        
    for regionName, region in allRegionsByName.items():
        for connection in region["connections"]:
            if connection[0] == "Entry":
                continue
            connect(world, player, regionName, connection[0], connection[1])
            connect(world, player, connection[0], regionName, connection[1])

    world.get_entrance("The Splashscreen?", player).connect(world.get_region('First Hallway', player))