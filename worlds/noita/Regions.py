# Regions are areas in your game that you travel to.
import itertools
from Typing import Dict, List
from BaseClasses import Region, Entrance, LocationProgressType


# Creates a new Region with the locations found in `location_region_mapping`
# and adds them to the world.
def create_region(world, player: int, region_name: str):
  new_region = Region(region_name, RegionType.Generic, region_name, player, world)

  # Here we create and assign locations to the region
  for location_name, location_id in Locations.location_region_mapping.get(region_name, {}).items():
    location = Locations.NoitaLocation(player, location_name, location_id, new_region)

    # If it's not the region with all the shitty chests, increases the priority of important items.
    # This way people know they can find their items by checking fixed locations instead of
    # leaving it up to chance.
    if region_name != "Forest": 
      location.progress_type = LocationProgressType.PRIORITY

    new_region.locations.append(location)

  world.regions.append(new_region)
  return new_region


# Creates connections based on our access mapping in `noita_connections`.
def create_connections(player, regions):
  for source, destinations in noita_connections.items():
    new_entrances = []

    for destination in destinations:
      # An "Entrance" is really just a connection between two regions
      entrance = Entrance(player, f"From {source} To {destination}", regions[source])
      entrance.connect(regions[destination])
      new_entrances.append(entrance)

    created_regions[source].exits = new_entrances


# Creates all regions and connections. Called from NoitaWorld.
def create_all_regions(world, player: int):
  created_regions = { name: create_region(world, player, name) for name in noita_regions }
  create_connections(player, created_regions)


noita_regions = {
  "Menu", "Forest",
  
  "Mines", "Collapsed Mines", "Lava Lake", "Dark Cave", "Shaft",

  "Coal Pits", "Fungal Caverns",

  "Snowy Depths",

  "Hiisi Base", "Secret Shop",

  "Underground Jungle", "Dragoncave",

  "The Vault",

  "Temple of the Art",

  "The Laboratory", "The Work",

  "Holy Mountain 1 (To Coal Pits)",
  "Holy Mountain 2 (To Snowy Depths)",
  "Holy Mountain 3 (To Hiisi Base)",
  "Holy Mountain 4 (To Underground Jungle)",
  "Holy Mountain 5 (To The Vault)",
}

noita_connections: Dict[str, List[str]] = {
  "Menu": ["Forest"],
  "Forest": ["Mines", "Collapsed Mines"],

  "Mines": ["Collapsed Mines", "Holy Mountain 1 (To Coal Pits)", "Lava Lake", "Forest"],
  "Collapsed Mines": ["Mines", "Holy Mountain 1 (To Coal Pits)", "Dark Cave"],
  "Lava Lake": ["Mines", "Shaft"],
  "Shaft": ["Lava Lake", "Snowy Depths"],

  ###
  "Holy Mountain 1 (To Coal Pits)": ["Coal Pits"],
  "Coal Pits": ["Holy Mountain 1 (To Coal Pits)", "Fungal Caverns", "Holy Mountain 2 (To Snowy Depths)"],
  "Fungal Caverns": ["Coal Pits"],

  ###
  "Holy Mountain 2 (To Snowy Depths)": ["Snowy Depths"],
  "Snowy Depths": ["Shaft", "Holy Mountain 2 (To Snowy Depths)", "Holy Mountain 3 (To Hiisi Base)"],
  
  ###
  "Holy Mountain 3 (To Hiisi Base)": ["Hiisi Base"],
  "Hiisi Base": ["Holy Mountain 3 (To Hiisi Base)", "Secret Shop", "Holy Mountain 4 (To Underground Jungle)"],

  ###
  "Holy Mountain 4 (To Underground Jungle)": ["Underground Jungle"],
  "Dragoncave": ["Underground Jungle"],
  "Underground Jungle": ["Holy Mountain 4 (To Underground Jungle)", "Dragoncave", "Holy Mountain 5 (To The Vault)"],
  
  ###
  "Holy Mountain 5 (To The Vault)": ["The Vault"],
  "The Vault": ["Holy Mountain 5 (To The Vault)", "Holy Mountain 6 (To Temple of the Art)"],
  
  ###
  "Holy Mountain 6 (To Temple of the Art)": ["Temple of the Art"],
  "Temple of the Art": ["Holy Mountain 6 (To Temple of the Art)", "Holy Mountain 7 (To The Laboratory)"],

  ###
  "Holy Mountain 7 (To The Laboratory)": ["The Laboratory"],
  "The Laboratory": ["Holy Mountain 7 (To The Laboratory)", "The Work"],
}
