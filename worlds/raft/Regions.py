import json
import os
from BaseClasses import Entrance

with open(os.path.join(os.path.dirname(__file__), 'regions.json'), 'r') as file:
    regionMap = json.loads(file.read())

def create_regions(world, player: int):
    from . import create_region
    from .Locations import location_table
    
    # Create regions and assign locations to each region
    for region in regionMap:
        world.regions += [create_region(world, player, region, [location["name"] for location in location_table if location["region"] is region], regionMap[region])]
	
#    for region in world.regions:
#        for exitName in regionMap[region.name]:
#            region.exits.append(Entrance(player, exit, region))