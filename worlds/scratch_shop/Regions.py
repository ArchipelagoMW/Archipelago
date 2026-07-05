from BaseClasses import Region, Entrance
from .Locations import TemplateLocation, location_data

def create_regions(multiworld, player):
    # Create the starting Region
    menu_region = Region("Menu", player, multiworld)
    overworld_region = Region("Overworld", player, multiworld)

    # Put locations into the Overworld region
    for loc_name, loc_id in location_data.items():
        loc = TemplateLocation(player, loc_name, loc_id, overworld_region)
        overworld_region.locations.append(loc)

    # Connect Menu to Overworld
    connection = Entrance(player, "Start Game", menu_region)
    menu_region.exits.append(connection)
    connection.connect(overworld_region)

    # Add to multiworld
    multiworld.regions.append(menu_region)
    multiworld.regions.append(overworld_region)