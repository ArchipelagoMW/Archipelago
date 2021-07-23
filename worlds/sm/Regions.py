def create_regions(self, world, player: int):
    from . import create_region
    from .Locations import lookup_name_to_id as location_lookup_name_to_id
    from BaseClasses import Entrance

    from variaRandomizer.logic.logic import Logic
    from variaRandomizer.graph.vanilla.graph_locations import locationsDict
    from variaRandomizer.graph.graph_utils import vanillaTransitions, vanillaBossesTransitions

    import logging
    regions = []
    #create exits
    for accessPoint in Logic.accessPoints:
        #if accessPoint.Internal == True or accessPoint.Boss == True:
        #    continue
        regions.append(create_region(self, world, player, accessPoint.Name, [key for key, value in locationsDict.items() if accessPoint.Name in value.AccessFrom], [accessPoint.Name + "|" + key for key in accessPoint.intraTransitions.keys()]))

    world.regions += regions
    #create entrances
    for accessPoint in Logic.accessPoints:
        for exit in world.get_region(accessPoint.Name, player).exits:
            exit.connect(world.get_region(exit.name.split("|")[1], player))

    for src, dest in vanillaTransitions:
        src_region = world.get_region(src, player)
        dest_region = world.get_region(dest, player)
        src_region.exits.append(Entrance(player, src + "|" + dest, src_region))
        srcDestEntrance = world.get_entrance(src + "|" + dest, player)
        srcDestEntrance.connect(dest_region)

    for dest, src in vanillaTransitions:
        src_region = world.get_region(src, player)
        dest_region = world.get_region(dest, player)
        src_region.exits.append(Entrance(player, src + "|" + dest, src_region))
        srcDestEntrance = world.get_entrance(src + "|" + dest, player)
        srcDestEntrance.connect(dest_region)

    for src, dest in vanillaBossesTransitions:
        src_region = world.get_region(src, player)
        dest_region = world.get_region(dest, player)
        src_region.exits.append(Entrance(player, src + "|" + dest, src_region))
        srcDestEntrance = world.get_entrance(src + "|" + dest, player)
        srcDestEntrance.connect(dest_region)

    for dest, src in vanillaBossesTransitions:
        src_region = world.get_region(src, player)
        dest_region = world.get_region(dest, player)
        src_region.exits.append(Entrance(player, src + "|" + dest, src_region))
        srcDestEntrance = world.get_entrance(src + "|" + dest, player)
        srcDestEntrance.connect(dest_region)


    world.regions += [
        create_region(self, world, player, 'Menu', None, ['Ship'])
        #create_region(world, player, 'Zebes', [location for location in location_lookup_name_to_id])
    ]

    shipEntrance = world.get_entrance('Ship', player)
    shipEntrance.connect(world.get_region('Landing Site', player))
    #startAP = world.get_region('Landing Site', player)
   # entrance = world.get_entrance('Ship', player)         
    #startAP.exits.append(entrance)
   # entrance.connect(startAP)