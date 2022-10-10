def create_regions(self, world, player: int):
    from . import create_region
    from BaseClasses import Entrance
    from logic.logic import Logic
    from graph.vanilla.graph_locations import locationsDict

    regions = []
    for accessPoint in Logic.accessPoints:
        if not accessPoint.Escape:
            regions.append(create_region(self, 
                                         world, 
                                         player, 
                                         accessPoint.Name, 
                                         None,
                                         [accessPoint.Name + "->" + key for key in accessPoint.intraTransitions.keys()]))

    world.regions += regions

    # create a region for each location and link each to what the location has access
    # we make them one way so that the filler (and spoiler log) doesnt try to use those region as intermediary path
    # this is required in AP because a location cant have multiple parent regions
    locationRegions = []
    for locationName, value in locationsDict.items():
        locationRegions.append(create_region(   self, 
                                                world, 
                                                player, 
                                                locationName, 
                                                [locationName]))
        for key in value.AccessFrom.keys():
            currentRegion =world.get_region(key, player)
            currentRegion.exits.append(Entrance(player, key + "->"+ locationName, currentRegion))

    world.regions += locationRegions
    #create entrances
    regionConcat = regions + locationRegions
    for region in regionConcat:
        for exit in region.exits:
            exit.connect(world.get_region(exit.name[exit.name.find("->") + 2:], player))

    world.regions += [
        create_region(self, world, player, 'Menu', None, ['StartAP'])
    ]
