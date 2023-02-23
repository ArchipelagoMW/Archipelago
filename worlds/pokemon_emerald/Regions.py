from BaseClasses import Region, Entrance
from .Data import get_region_data
from .Warps import get_warp_region_name, get_warp_destination


def create_regions(world, player):
    regions = {}
    region_data = get_region_data()

    connections = []
    for region_name, region_data in region_data.items():
        regions[region_name] = Region(region_name, player, world)

        for warp in region_data.warps:
            destination_region_name = get_warp_region_name(get_warp_destination(warp))
            if (destination_region_name == None):
                continue
            connections.append((warp, region_name, destination_region_name))

        for exit in region_data.exits:
            connections.append((f"{region_name} -> {exit}", region_name, exit))

    for name, source, dest in connections:
        connection = Entrance(player, name, regions[source])
        regions[source].exits.append(connection)
        connection.connect(regions[dest])

    menu = Region("Menu", player, world)
    connection = Entrance(player, "New Game", menu)
    menu.exits.append(connection)
    connection.connect(regions["REGION_LITTLEROOT_TOWN"])
    regions["Menu"] = menu

    world.regions += regions.values()
    world.initialize_regions()
