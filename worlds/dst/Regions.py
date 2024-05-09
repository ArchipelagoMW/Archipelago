from typing import Dict, List, NamedTuple
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from .Locations import location_data_table, DSTLocation
from .Items import DSTItem, item_data_table
from .ItemPool import DSTItemPool
from .Options import DSTOptions
from .Constants import DSTAP_EVENTS, BOSS_COMPLETION_GOALS
import random

class DSTRegionData(NamedTuple):
   connecting_regions: List[str] = []
   locations: List[str] = []

def create_regions(multiworld: MultiWorld, player: int, options:DSTOptions, itempool:DSTItemPool):
   REGION_DATA_TABLE: Dict[str, DSTRegionData] = {
      "Menu":     DSTRegionData(["Forest"], []),
      "Forest":   DSTRegionData(["Cave", "Ocean"], []),
      "Cave":     DSTRegionData([], []),
      "Ocean":    DSTRegionData([], []),
   }

   def create_event_item(name: str) -> None:
      item:DSTItem = multiworld.create_item(name, player)
      item.classification = ItemClassification.progression
      return item
   
   def create_event(event_location_name: str, event_item_name: str) -> None:
      region = multiworld.get_region("Forest", player)
      loc = DSTLocation(player, event_location_name, None, region)
      loc.place_locked_item(create_event_item(event_item_name))
      region.locations.append(loc)

   def get_region_name_from_tags(tags: set[str]):
      return "Cave" if "caves" in tags else "Ocean" if "ocean" in tags else "Forest"
   
   # Get number of items that need to be placed, plus make space for junk items and traps
   location_num_left_to_place:int = len(itempool.nonfiller_items) + 20

   # Check if locations are disabled by options
   filtered_location_data_table = {name: data for name, data in location_data_table.items() if not(
      "deprecated" in data.tags # Don't add deprecated locations
      or (not options.creature_locations.value and "creature" in data.tags)
      or (not options.farming_locations.value and "farming" in data.tags)
      or (options.cooking_locations.current_key == "none" and "cooking" in data.tags)
      or (options.cooking_locations.current_key != "warly_enabled" and "warly" in data.tags)
      or (options.cooking_locations.current_key == "veggie_only" and "meat" in data.tags)
      or (options.cooking_locations.current_key == "meat_only" and "veggie" in data.tags)
   )}
   # Place normal locations in regions
   for name, data in filtered_location_data_table.items():

      # Don't add science, magic, or seafaring. We'll do that somewhere else
      if ("research" in data.tags
         # Require other research locations
         and not  ("ancient" in data.tags 
                  or "celestial" in data.tags
                  or "hermitcrab" in data.tags)
         ):
         continue

      REGION_DATA_TABLE[get_region_name_from_tags(data.tags)].locations.append(name)
      location_num_left_to_place -= 1

   # Categories
   RESEARCH_GROUPS = {
      "science_1_locations" : [name for name, data in filtered_location_data_table.items() if "science" in data.tags and "tier_1" in data.tags],
      "science_2_locations" : [name for name, data in filtered_location_data_table.items() if "science" in data.tags and "tier_2" in data.tags],
      "magic_1_locations" : [name for name, data in filtered_location_data_table.items() if "magic" in data.tags and "tier_1" in data.tags],
      "magic_2_locations" : [name for name, data in filtered_location_data_table.items() if "magic" in data.tags and "tier_2" in data.tags],
      "seafaring_locations" : [name for name, data in filtered_location_data_table.items() if "seafaring" in data.tags],
   }
   
   for _, group in RESEARCH_GROUPS.items():
      # Shuffle groups!
      random.shuffle(group)

      # Guarantee 6 of each group
      for _ in range(6):
         if len(group):
            name = group.pop()  
            REGION_DATA_TABLE[get_region_name_from_tags(location_data_table[name].tags)].locations.append(name)
            location_num_left_to_place -= 1
         else: break

   # Now smush the groups together!
   remaining_research = []
   for _, group in RESEARCH_GROUPS.items():
      remaining_research += group

   # And shuffle again!
   random.shuffle(remaining_research)

   # Make locations until there's nothing to place left
   while location_num_left_to_place > 0 and len(remaining_research):
      name = remaining_research.pop()  
      REGION_DATA_TABLE[get_region_name_from_tags(location_data_table[name].tags)].locations.append(name)
      location_num_left_to_place -= 1

   # Create regions
   for region_name in REGION_DATA_TABLE.keys():
      new_region = Region(region_name, player, multiworld)
      multiworld.regions.append(new_region)
      
   # Create locations and entrances.
   for region_name, region_data in REGION_DATA_TABLE.items():
      region = multiworld.get_region(region_name, player)
      region.add_locations({
         location_name: location_data_table[location_name].address for location_name in region_data.locations
      }, DSTLocation)
      if region_data.connecting_regions:
         for exit_name in region_data.connecting_regions:
            entrance = Entrance(player, exit_name, region)
            entrance.connect(multiworld.get_region(exit_name, player))
            region.exits.append(entrance)

   # Create events
   for loc_name, item_name in DSTAP_EVENTS.items(): create_event(loc_name, item_name)

   # Decide win conditions
   victory_events:set = set()
   if options.goal.current_key == "survival":
      victory_events.add("Victory")
      create_event("Survival Goal", "Victory")
   elif options.goal.current_key == "bosses_any" or options.goal.current_key == "bosses_all":
      victory_events.update([BOSS_COMPLETION_GOALS[bossname] for bossname in options.required_bosses.value])

   # Set the win conditions
   if options.goal.current_key == "bosses_any":
      multiworld.completion_condition[player] = lambda state: state.has_any(victory_events, player)
   else:
      multiworld.completion_condition[player] = lambda state: state.has_all(victory_events, player)
   