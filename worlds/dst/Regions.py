from typing import Dict, List, NamedTuple, Set
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from .Locations import location_data_table, DSTLocation
from .ItemPool import DSTItemPool
from .Options import DSTOptions
from .Constants import REGION

class DSTRegionData(NamedTuple):
   connecting_regions: List[str] = []
   locations: List[str] = []

def create_regions(multiworld: MultiWorld, player: int, options:DSTOptions, itempool:DSTItemPool):
   REGION_DATA_TABLE: Dict[str, DSTRegionData] = {
      REGION.MENU:         DSTRegionData([REGION.FOREST], []),
      REGION.FOREST:       DSTRegionData([REGION.CAVE, REGION.OCEAN], []),
      REGION.CAVE:         DSTRegionData([REGION.ARCHIVE, REGION.RUINS, REGION.DUALREGION], []),
      REGION.ARCHIVE:      DSTRegionData([], []),
      REGION.RUINS:        DSTRegionData([], []), 
      REGION.OCEAN:        DSTRegionData([REGION.MOONQUAY, REGION.MOONSTORM, REGION.DUALREGION], []),
      REGION.MOONQUAY:     DSTRegionData([], []),
      REGION.MOONSTORM:    DSTRegionData([], []),
      REGION.DUALREGION:   DSTRegionData([REGION.BOTHREGIONS], []),
      REGION.BOTHREGIONS:  DSTRegionData([], []),
   }   
   NUM_JUNK_ITEMS:int = options.junk_item_amount.value
   BOSS_DEFEAT_LOCATIONS:Set = set(
      options.required_bosses.value if (options.goal.value == options.goal.option_bosses_any or options.goal.value == options.goal.option_bosses_all)
      else []
   )

   # Locations to omit if condition is true TODO: Change these when mcguffin items are added
   OMITTED:Dict[str, bool] = {
      "Ancient Fuelweaver": "Ancient Guardian" in options.required_bosses.value,
      "Celestial Champion": "Crab King" in options.required_bosses.value,
      "Scrappy Werepig": "Nightmare Werepig" in options.required_bosses.value,
   } if options.goal.value == options.goal.option_bosses_any else {}

   # Build region whitelist
   REGION_WHITELIST = set([REGION.MENU, REGION.FOREST])
   if options.cave_regions.value >= options.cave_regions.option_light: REGION_WHITELIST.update([REGION.CAVE])
   if options.cave_regions.value >= options.cave_regions.option_full: REGION_WHITELIST.update([REGION.RUINS, REGION.ARCHIVE])
   if options.ocean_regions.value >= options.ocean_regions.option_light: REGION_WHITELIST.update([REGION.OCEAN, REGION.MOONQUAY])
   if options.ocean_regions.value >= options.ocean_regions.option_full: REGION_WHITELIST.update([REGION.MOONSTORM])
   if REGION.CAVE in REGION_WHITELIST or REGION.OCEAN in REGION_WHITELIST: REGION_WHITELIST.update([REGION.DUALREGION])
   if REGION.CAVE in REGION_WHITELIST and REGION.OCEAN in REGION_WHITELIST: REGION_WHITELIST.update([REGION.BOTHREGIONS])

   def get_region_name_from_tags(tags: Set[str]):
      return (
         REGION.FOREST if "nounlock" in tags and options.shuffle_no_unlock_recipes.value
         else REGION.BOTHREGIONS if "bothregions" in tags
         else REGION.DUALREGION if "dualregion" in tags
         else REGION.MOONSTORM if "moonstorm" in tags
         else REGION.MOONQUAY if "moonquay" in tags
         else REGION.OCEAN if "ocean" in tags or "seafaring" in tags
         else REGION.ARCHIVE if "archive" in tags
         else REGION.RUINS if "ruins" in tags
         else REGION.CAVE if "cave" in tags
         else REGION.FOREST
      )
   
   # Get number of items that need to be placed
   location_num_left_to_place:int = len(itempool.nonfiller_itempool) + NUM_JUNK_ITEMS + len(BOSS_DEFEAT_LOCATIONS)

   # Check if locations are disabled by options
   filtered_location_data_table = {name: data for name, data in location_data_table.items() if not(
      "deprecated" in data.tags # Don't add deprecated locations
      or (not options.creature_locations.value and "creature" in data.tags)
      or (not options.farming_locations.value and "farming" in data.tags)
      or (options.cooking_locations.current_key == "none" and "cooking" in data.tags)
      or (options.cooking_locations.current_key != "warly_enabled" and "warly" in data.tags)
      or (options.cooking_locations.current_key == "veggie_only" and "meat" in data.tags)
      or (options.cooking_locations.current_key == "meat_only" and "veggie" in data.tags)
      or (OMITTED.get(name, False))
   )}
   
   # Categories
   RESEARCH_GROUPS = {
      "veggie_locations": [],
      "science_1_locations": [],
      "science_2_locations": [],
      "critter_locations": [],
      "magic_1_locations": [],
      "magic_2_locations": [],
      "seafaring_locations": [],
      "other_locations": []
   }

   # Fill categories with locations
   for name, data in filtered_location_data_table.items():
      region_name = get_region_name_from_tags(data.tags)
      if region_name in REGION_WHITELIST:
         if ("research" in data.tags
            and not (
               # These won't be randomized
               "ancient" in data.tags 
               or "celestial" in data.tags
               or "hermitcrab" in data.tags
            )
         ):
            (
               RESEARCH_GROUPS["veggie_locations"] if "veggie_research" in data.tags
               else RESEARCH_GROUPS["critter_locations"] if "critter_research" in data.tags
               else RESEARCH_GROUPS["science_1_locations"] if "science" in data.tags and "tier_1" in data.tags
               else RESEARCH_GROUPS["science_2_locations"] if "science" in data.tags and "tier_2" in data.tags
               else RESEARCH_GROUPS["magic_1_locations"] if "magic" in data.tags and "tier_1" in data.tags
               else RESEARCH_GROUPS["magic_2_locations"] if "magic" in data.tags and "tier_2" in data.tags
               else RESEARCH_GROUPS["seafaring_locations"] if "seafaring" in data.tags 
               else RESEARCH_GROUPS["other_locations"] # There shouldn't be anything here, but just to be safe
            ).append(name)

         else:
            # Add all other locations to regions
            REGION_DATA_TABLE[region_name].locations.append(name)
            location_num_left_to_place -= 1

   assert len(RESEARCH_GROUPS["other_locations"]) == 0
   
   for _, group in RESEARCH_GROUPS.items():
      # Shuffle groups!
      multiworld.random.shuffle(group)

      # Guarantee 4 of each group
      for _ in range(4):
         if len(group):
            name = group.pop()
            region_name = get_region_name_from_tags(location_data_table[name].tags)
            REGION_DATA_TABLE[region_name].locations.append(name)
            location_num_left_to_place -= 1
         else: break

   # Now smush the groups together!
   remaining_research = []
   for _, group in RESEARCH_GROUPS.items():
      remaining_research += group

   # And shuffle again!
   multiworld.random.shuffle(remaining_research)

   # Make locations until there's nothing to place left
   while location_num_left_to_place > 0 and len(remaining_research):
      name = remaining_research.pop()
      region_name = get_region_name_from_tags(location_data_table[name].tags)
      REGION_DATA_TABLE[region_name].locations.append(name)
      location_num_left_to_place -= 1

   # Create regions
   for region_name in REGION_DATA_TABLE.keys():
      if region_name in REGION_WHITELIST:
         new_region = Region(region_name, player, multiworld)
         multiworld.regions.append(new_region)
      
   # Create locations and entrances.
   for region_name, region_data in REGION_DATA_TABLE.items():
      # Check if region is allowed
      if not region_name in REGION_WHITELIST:
         continue
      # Fill the region with locations
      region = multiworld.get_region(region_name, player)
      region.add_locations({
         location_name: location_data_table[location_name].address for location_name in region_data.locations
      }, DSTLocation)
      if region_data.connecting_regions:
         for exit_name in region_data.connecting_regions:
            if exit_name in REGION_WHITELIST:
               entrance = Entrance(player, exit_name, region)
               entrance.connect(multiworld.get_region(exit_name, player))
               region.exits.append(entrance)

   # Fill boss locations with "Boss Defeat" items
   EXISTING_LOCATIONS = [location.name for location in multiworld.get_locations(player)]
   for bossname in BOSS_DEFEAT_LOCATIONS:
      assert bossname in EXISTING_LOCATIONS, \
         f"{multiworld.get_player_name(player)} (Don't Starve Together): {bossname} does not exist in the regions selected in your yaml! " \
         "Make sure you select the correct regions for your goal, or choose auto or full!"
      multiworld.get_location(bossname, player).place_locked_item(multiworld.create_item("Boss Defeat", player))
   