from typing import Dict, List, NamedTuple, Set
from BaseClasses import MultiWorld, Region, Entrance, ItemClassification
from Options import OptionError
from .Locations import location_data_table, DSTLocation
from .ItemPool import DSTItemPool
from .Options import DSTOptions
from .Constants import REGION, PHASE, SEASON, SEASONS_PASSED, SPECIAL_TAGS, BOSS_PREREQUISITES
from . import Util

class DSTRegionData(NamedTuple):
    connecting_regions: List[str] = []
    locations: List[str] = []

def create_regions(multiworld: MultiWorld, player: int, options:DSTOptions, itempool:DSTItemPool):
    world = multiworld.worlds[player]
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

    # Locations to omit if condition is true
    OMITTED:Dict[str, bool] = {}

    # Omit later bosses on bosses_any goal
    if options.goal.value == options.goal.option_bosses_any:
        for dependent_location, prerequisites in BOSS_PREREQUISITES.items():
            if len(prerequisites.intersection(options.required_bosses.value)):
                OMITTED[dependent_location] = True

        # Change the setting to reflect the change
        options.required_bosses.value.difference_update({bossname for bossname, isomitted in OMITTED.items() if isomitted})

    BOSS_DEFEAT_LOCATIONS:Set[str] = set(
        options.required_bosses.value if (options.goal.value == options.goal.option_bosses_any or options.goal.value == options.goal.option_bosses_all)
        else []
    )
    _DUMMY_FILL_ITEM = "Boss Defeat"
    _boss_fill_item:str = (
        "Extra Damage Against Bosses" if options.boss_fill_items.value == options.boss_fill_items.option_extra_damage_against_bosses
        else "Damage Bonus" if options.boss_fill_items.value == options.boss_fill_items.option_damage_bonus
        else _DUMMY_FILL_ITEM
    )
    BOSS_PREFILLS:Dict[str, str] = {
        # Bosses_any goals get dummy item always; Anything else gets selected fill item
        bossname: _DUMMY_FILL_ITEM if (
            options.goal.value == options.goal.option_bosses_any and bossname in options.required_bosses.value
        ) else _boss_fill_item
        for bossname in (
            # If a fill item is selected, give it to all bosses, just give goal bosses dummies
            BOSS_DEFEAT_LOCATIONS if _boss_fill_item == _DUMMY_FILL_ITEM
            else set(options.required_bosses.valid_keys).difference({"Random"})
        )
    }

    # Build whitelists
    WHITELIST = Util.build_whitelist(options)

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
    location_num_left_to_place:int = len(itempool.nonfiller_itempool) + NUM_JUNK_ITEMS

    # Decide which bosses are required in progression
    _progression_required_bosses = set()
    if options.goal.value == options.goal.option_bosses_any or options.goal.value == options.goal.option_bosses_all:
        _progression_required_bosses.update(options.required_bosses.value)
        for bossname in options.required_bosses.value:
            _progression_required_bosses.update(BOSS_PREREQUISITES.get(bossname, set()))

    is_enabled_in_tag_group = Util.create_tag_group_validation_fn(options)

    # Check if locations are disabled by options
    filtered_location_data_table = {name: data for name, data in location_data_table.items() if not(
        "deprecated" in data.tags # Don't add deprecated locations
        or (not options.creature_locations.value and "creature" in data.tags)
        or (options.creature_locations.value == options.creature_locations.option_peaceful and "creature" in data.tags and not "peaceful" in data.tags)
        or (not options.farming_locations.value and "farming" in data.tags)
        or (options.cooking_locations.current_key == "none" and "cooking" in data.tags)
        or (options.cooking_locations.current_key != "warly_enabled" and "warly" in data.tags)
        or (options.cooking_locations.current_key == "veggie_only" and "meat" in data.tags)
        or (options.cooking_locations.current_key == "meat_only" and "veggie" in data.tags)
        or (
            not name in _progression_required_bosses
            and not (options.creature_locations.value == options.creature_locations.option_peaceful and name == "Antlion")
            and (
                (options.boss_locations.value == options.boss_locations.option_none and "boss" in data.tags)
                or (options.boss_locations.value <= options.boss_locations.option_easy and "raidboss" in data.tags)
            )
        )
        or not is_enabled_in_tag_group(SEASON, data.tags)
        or not is_enabled_in_tag_group(PHASE, data.tags)
        or not is_enabled_in_tag_group(SEASONS_PASSED, data.tags)
        or not is_enabled_in_tag_group(SPECIAL_TAGS, data.tags)
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
        if region_name in WHITELIST:
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

                if not name in BOSS_PREFILLS:
                    # Only lower the counter if it won't be prefilled
                    location_num_left_to_place -= 1

    assert len(RESEARCH_GROUPS["other_locations"]) == 0

    for _, group in RESEARCH_GROUPS.items():
        # Shuffle groups!
        world.random.shuffle(group)

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
    world.random.shuffle(remaining_research)

    # Make locations until there's nothing to place left
    while location_num_left_to_place > 0 and len(remaining_research):
        name = remaining_research.pop()
        region_name = get_region_name_from_tags(location_data_table[name].tags)
        REGION_DATA_TABLE[region_name].locations.append(name)
        location_num_left_to_place -= 1

    # Create regions
    for region_name in REGION_DATA_TABLE.keys():
        if region_name in WHITELIST:
            new_region = Region(region_name, player, multiworld)
            multiworld.regions.append(new_region)

    # Create locations and entrances.
    for region_name, region_data in REGION_DATA_TABLE.items():
        # Check if region is allowed
        if not region_name in WHITELIST:
            continue
        # Fill the region with locations
        region = multiworld.get_region(region_name, player)
        region.add_locations({
            location_name: location_data_table[location_name].address for location_name in region_data.locations
        }, DSTLocation)
        if region_data.connecting_regions:
            for exit_name in region_data.connecting_regions:
                if exit_name in WHITELIST:
                    entrance = Entrance(player, f"{region_name} -> {exit_name}", region)
                    entrance.connect(multiworld.get_region(exit_name, player))
                    region.exits.append(entrance)


    EXISTING_LOCATIONS = [location.name for location in multiworld.get_locations(player)]
    # Verify goal boss is added
    for bossname in BOSS_DEFEAT_LOCATIONS:
        if not bossname in EXISTING_LOCATIONS:
            raise OptionError(f"{world.player_name} (Don't Starve Together): {bossname} does not exist in the regions selected in your yaml! " +\
                (
                    "Not enough conditions possible to befriend Crabby Hermit. Add more seasons and day phases!" if (
                        (bossname == "Crab King" or bossname == "Celestial Champion")
                        and REGION.OCEAN in WHITELIST and not SPECIAL_TAGS.HERMIT_10 in WHITELIST
                    ) else "Make sure you select the correct regions for your goal, or choose auto or full!"
                )
            )
            

    # Fill boss locations with prefill items
    for bossname, fillitem in BOSS_PREFILLS.items():
        if bossname in EXISTING_LOCATIONS:
            world.get_location(bossname).place_locked_item(itempool.create_item(world, fillitem))
