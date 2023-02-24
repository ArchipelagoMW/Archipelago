from BaseClasses import Region, Entrance, ItemClassification
from .Data import get_region_data
from .Items import PokemonEmeraldItem
from .Locations import PokemonEmeraldLocation
from .Warps import get_warp_region_name, get_warp_destination


def create_regions(world, player):
    regions = {}
    region_data = get_region_data()

    connections = []
    for region_name, region_data in region_data.items():
        new_region = Region(region_name, player, world)

        for event_data in region_data.events:
            event = PokemonEmeraldLocation(player, event_data.name, None, new_region)
            event.place_locked_item(PokemonEmeraldItem(event_data.name, ItemClassification.progression, None, player))
            new_region.locations.append(event)

        for exit in region_data.exits:
            connections.append((f"{region_name} -> {exit}", region_name, exit))

        for warp in region_data.warps:
            destination_region_name = get_warp_region_name(get_warp_destination(warp))
            if (destination_region_name == None):
                continue
            connections.append((warp, region_name, destination_region_name))

        regions[region_name] = new_region

    for name, source, dest in connections:
        connection = Entrance(player, name, regions[source])
        regions[source].exits.append(connection)
        connection.connect(regions[dest])

    menu = Region("Menu", player, world)
    connection = Entrance(player, "New Game", menu)
    menu.exits.append(connection)
    connection.connect(regions["REGION_LITTLEROOT_TOWN/MAIN"])
    regions["Menu"] = menu

    world.regions += regions.values()
    world.initialize_regions()
