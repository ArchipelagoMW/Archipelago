"""Shuffle Wrinkly and T&S Doors based on settings."""

from randomizer.Enums.DoorType import DoorType
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Types import Types
from randomizer.Enums.Settings import DKPortalRando
from randomizer.Lists import Exceptions
from randomizer.Lists.DoorLocations import door_locations
from randomizer.LogicClasses import LocationLogic
from randomizer.Patching.Library.Generic import getHintRequirement

level_list = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
]
level_to_name = {
    Levels.DKIsles: "Isles",
    Levels.JungleJapes: "Japes",
    Levels.AngryAztec: "Aztec",
    Levels.FranticFactory: "Factory",
    Levels.GloomyGalleon: "Galleon",
    Levels.FungiForest: "Forest",
    Levels.CrystalCaves: "Caves",
    Levels.CreepyCastle: "Castle",
}


def GetDoorLocationForKongAndLevel(kong, level):
    """For the Level and Kong enum values, return the generic Blueprint Location enum tied to it."""
    baseOffset = int(Locations.JapesDonkeyDoor)  # Japes/Donkey is the first door location and they're all grouped together
    levelOffset = int(level)
    return Locations(baseOffset + (5 * levelOffset) + int(kong))


def UpdateDoorLevels(spoiler):
    """Ensure that the location for each hint door counts towards the correct level."""
    for region in spoiler.RegionList:
        for location_logic in spoiler.RegionList[region].locations:
            if spoiler.LocationList[location_logic.id].type == Types.Hint:
                spoiler.LocationList[location_logic.id].level = spoiler.RegionList[region].level


def ShuffleDoors(spoiler, vanilla_doors_placed: bool):
    """Shuffle Wrinkly and T&S Doors based on settings."""
    # Handle initial settings
    shuffle_wrinkly = False if vanilla_doors_placed else spoiler.settings.wrinkly_location_rando
    shuffle_tns = False if vanilla_doors_placed else spoiler.settings.tns_location_rando
    shuffle_dkportal = spoiler.settings.dk_portal_location_rando_v2 != DKPortalRando.off
    disable_wrinkly_puzzles = False if vanilla_doors_placed else spoiler.settings.remove_wrinkly_puzzles
    # Prepare data structures that will hold the door info
    human_hint_doors = {
        "Jungle Japes": {},
        "Angry Aztec": {},
        "Frantic Factory": {},
        "Gloomy Galleon": {},
        "Fungi Forest": {},
        "Crystal Caves": {},
        "Creepy Castle": {},
    }
    human_portal_doors = {
        "Jungle Japes": {},
        "Angry Aztec": {},
        "Frantic Factory": {},
        "Gloomy Galleon": {},
        "Fungi Forest": {},
        "Crystal Caves": {},
        "Creepy Castle": {},
    }
    human_entry_doors = {
        "Jungle Japes": "Vanilla",
        "Angry Aztec": "Vanilla",
        "Frantic Factory": "Vanilla",
        "Gloomy Galleon": "Vanilla",
        "Fungi Forest": "Vanilla",
        "Crystal Caves": "Vanilla",
        "Creepy Castle": "Vanilla",
    }
    shuffled_door_data = {
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
    }
    # Reset (unreserved) Doors
    for level in door_locations:
        for door in door_locations[level]:
            if not spoiler.settings.dos_door_rando or not door.dos_door:
                # In Dos' Doors, there are exactly two doors that need to not be undone by this process: the two extra Japes doors
                door.placed = door.default_placed
            if shuffle_wrinkly and not vanilla_doors_placed:
                if door.placed == DoorType.wrinkly:
                    door.placed = DoorType.null
            if shuffle_tns and not vanilla_doors_placed:
                if door.placed == DoorType.boss:
                    door.placed = DoorType.null
            if shuffle_dkportal:
                if door.placed == DoorType.dk_portal:
                    door.placed = DoorType.null
            # Reset door lists
            door.door_type = door.default_door_list.copy()
            door.updateDoorTypeLogic(spoiler)
    # If we already placed vanilla doors, we've already saved some data we need to preserve post-reset
    if vanilla_doors_placed:
        shuffled_door_data = spoiler.shuffled_door_data
        human_hint_doors = spoiler.human_hint_doors
        human_portal_doors = spoiler.human_portal_doors
    # Hint doors have Locations tied to them. If we're about to add new ones, then we must remove the old ones.
    if shuffle_wrinkly:
        ClearHintDoorLogic(spoiler)
    # Assign Doors
    for level in door_locations:
        # Get all door locations that can be given a door
        available_doors = []
        for door_index, door in enumerate(door_locations[level]):
            if door.placed == DoorType.null and (shuffle_wrinkly or shuffle_tns or shuffle_dkportal):
                available_doors.append(door_index)
            elif disable_wrinkly_puzzles and door.default_placed == DoorType.wrinkly:
                available_doors.append(door_index)
        # Prevent plandomized doors from being used as portals
        plando_indexes = []
        if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_wrinkly_doors"] != -1:
            plando_indexes = [x for x in available_doors if door_locations[level][x].name in spoiler.settings.plandomizer_dict["plando_wrinkly_doors"].values()]
            for planned_door in plando_indexes:
                available_doors.remove(planned_door)
        spoiler.settings.random.shuffle(available_doors)
        if shuffle_tns:
            plando_portal_indexes = []
            number_of_portals_in_level = spoiler.settings.random.choice([3, 4, 5])
            allow_multiple_portals_per_group = False
            # Make sure selected locations will be suitable to be a T&S portal
            available_portals = [door for door in available_doors if DoorType.boss in door_locations[level][door].door_type]
            if spoiler.settings.enable_plandomizer and spoiler.settings.plandomizer_dict["plando_tns_portals"] != -1:
                level_to_string = str(level.value)
                if level_to_string in spoiler.settings.plandomizer_dict["plando_tns_portals"].keys():
                    number_of_portals_in_level = min(3, len(spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string]))
                    # Sanitize input, now that we don't need the -1's anymore
                    spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string] = [x for x in spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string] if x != -1]
                    plando_portal_indexes = [x for x in available_portals if door_locations[level][x].name in spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string]]
                    if len(plando_portal_indexes) != len([x for x in spoiler.settings.plandomizer_dict["plando_tns_portals"][level_to_string]]):
                        raise Exceptions.PlandoIncompatibleException(f"Not every selected portal is available in level {level}")
                    for planned_portal in plando_portal_indexes:
                        available_portals.remove(planned_portal)
            for new_portal in range(number_of_portals_in_level):
                if len(available_portals) > 0:  # Should only fail if we don't have enough door locations
                    if len(plando_portal_indexes) > 0:
                        selected_door_index = plando_portal_indexes.pop()
                        allow_multiple_portals_per_group = True
                    elif new_portal > 0:
                        selected_door_index = available_portals.pop()
                    else:
                        # On the first iteration, make sure at least 1 TnS portal is accessible without any moves
                        selected_door_index = spoiler.settings.random.choice([door for door in available_portals if door_locations[level][door].moveless is True])
                        available_portals.remove(selected_door_index)
                    selected_portal = door_locations[level][selected_door_index]
                    if not allow_multiple_portals_per_group:
                        # Only place one T&S portal per group so we don't stack portals too heavily
                        available_portals = [door for door in available_portals if door_locations[level][door].group != selected_portal.group]
                    # update available_doors separately as wrinkly doors should not be affected by the T&S grouping
                    available_doors.remove(selected_door_index)
                    selected_portal.assignPortal(spoiler)
                    human_portal_doors[level_list[level]]["T&S #" + str(new_portal + 1)] = selected_portal.name
                    shuffled_door_data[level].append((selected_door_index, DoorType.boss))
        if shuffle_wrinkly:
            # Place one hint door per kong
            for kong in range(5):  # NOTE: If testing all locations, replace "range(5) with range(len(available_doors))"
                assignee = Kongs(kong % 5)
                if len(available_doors) > 0:  # Should only fail if we don't have enough door locations
                    # Give plandomizer an opportunity to get the final say
                    retry = True
                    location_var = str(GetDoorLocationForKongAndLevel(kong, level).value)
                    if (
                        spoiler.settings.enable_plandomizer
                        and spoiler.settings.plandomizer_dict["plando_wrinkly_doors"] != -1
                        and location_var in spoiler.settings.plandomizer_dict["plando_wrinkly_doors"].keys()
                    ):
                        if spoiler.settings.plandomizer_dict["plando_wrinkly_doors"][location_var] not in ("", -1):
                            selected_door_index = [x for x in plando_indexes if door_locations[level][x].name == spoiler.settings.plandomizer_dict["plando_wrinkly_doors"][location_var]][0]
                            retry = False
                        else:
                            selected_door_index = available_doors.pop()
                    else:
                        selected_door_index = available_doors.pop(0)  # Popping from the top of the list makes it possible to append the selected door back into the list, if it's a bad pick
                    # Make sure that the kong is eligible to be assigned to the selected door, and that the door location is suitable to be a hint door
                    while (assignee not in door_locations[level][selected_door_index].kongs) or (DoorType.wrinkly not in door_locations[level][selected_door_index].door_type):
                        # If testing all locations, add a break here
                        if retry:
                            available_doors.append(selected_door_index)
                            selected_door_index = available_doors.pop(0)
                        else:
                            name = spoiler.settings.plandomizer_dict["plando_wrinkly_doors"][location_var]
                            raise Exceptions.PlandoIncompatibleException(f"Bad door location: {name}.")
                    selected_door = door_locations[level][selected_door_index]
                    selected_door.assignDoor(assignee)  # Clamp to within [0,4], preventing list index errors
                    human_hint_doors[level_list[level]][str(Kongs(kong % 5).name).capitalize()] = selected_door.name
                    shuffled_door_data[level].append((selected_door_index, DoorType.wrinkly, (kong % 5)))
                    # Add logic for the new door location
                    doorLocation = GetDoorLocationForKongAndLevel(kong, level)  # If testing all locations, replace "kong" with "kong % 5"
                    region = spoiler.RegionList[selected_door.logicregion]
                    region.locations.append(LocationLogic(doorLocation, selected_door.logic))
                    spoiler.LocationList[doorLocation].name = f"{level_to_name[level]} Hint Door: {selected_door.name}"
        elif disable_wrinkly_puzzles:
            # place vanilla wrinkly doors
            vanilla_wrinkly_doors = [door for door in available_doors if door_locations[level][door].default_placed == DoorType.wrinkly]
            for kong in range(5):
                if len(vanilla_wrinkly_doors) > 0:  # Should only fail if we don't have enough door locations
                    selected_door_index = vanilla_wrinkly_doors.pop()
                    selected_door = door_locations[level][selected_door_index]
                    assignee = selected_door.default_kong
                    selected_door.assignDoor(assignee)
                    human_hint_doors[level_list[level]][str(assignee).capitalize()] = selected_door.name
                    shuffled_door_data[level].append((selected_door_index, DoorType.wrinkly, int(assignee)))
        if shuffle_dkportal:
            available_entries = [door for door in available_doors if DoorType.dk_portal in door_locations[level][door].door_type]
            if len(available_entries) > 0:  # Should only fail if we don't have enough door locations
                selected_door_index = spoiler.settings.random.choice([door for door in available_entries])
                available_entries.remove(selected_door_index)
                selected_entry = door_locations[level][selected_door_index]
                # update available_doors separately as wrinkly doors should not be affected by the T&S grouping
                available_doors.remove(selected_door_index)
                selected_entry.assignDKPortal(spoiler, level)
                human_entry_doors[level_list[level]] = selected_entry.name
                shuffled_door_data[level].append((selected_door_index, DoorType.dk_portal))

    # Track all touched doors in a variable and put it in the spoiler because changes to the static list do not save
    spoiler.shuffled_door_data = shuffled_door_data
    # Give human text to spoiler log
    if shuffle_wrinkly:
        spoiler.human_hint_doors = human_hint_doors
    if shuffle_tns:
        spoiler.human_portal_doors = human_portal_doors
    if shuffle_dkportal:
        spoiler.human_entry_doors = human_entry_doors


def ShuffleVanillaDoors(spoiler):
    """Shuffle T&S and Wrinkly doors amongst the vanilla locations."""
    ClearHintDoorLogic(spoiler)
    # Prepare data structures that will hold the door info
    human_hint_doors = {
        "Jungle Japes": {},
        "Angry Aztec": {},
        "Frantic Factory": {},
        "Gloomy Galleon": {},
        "Fungi Forest": {},
        "Crystal Caves": {},
        "Creepy Castle": {},
    }
    human_portal_doors = {
        "Jungle Japes": {},
        "Angry Aztec": {},
        "Frantic Factory": {},
        "Gloomy Galleon": {},
        "Fungi Forest": {},
        "Crystal Caves": {},
        "Creepy Castle": {},
    }
    shuffled_door_data = {
        Levels.JungleJapes: [],
        Levels.AngryAztec: [],
        Levels.FranticFactory: [],
        Levels.GloomyGalleon: [],
        Levels.FungiForest: [],
        Levels.CrystalCaves: [],
        Levels.CreepyCastle: [],
    }
    for level in door_locations:
        # Reset the data structures for door shuffling information sharing
        shuffled_door_data[level] = []
        human_hint_doors[level_list[level]] = {}
        human_portal_doors[level_list[level]] = {}
        # Find the vanilla doors that are valid hint locations and clear their door
        # In Dos' Doors, this section finds exactly 6 doors per level
        vanilla_door_indexes = []
        for door_index, door in enumerate(door_locations[level]):
            # This catches all default Wrinkly and T&S locations in addition to the additional doors needed for Dos' Doors as needed
            if (door.default_placed != DoorType.null and door.default_placed != DoorType.dk_portal) or (door.dos_door and spoiler.settings.dos_door_rando):
                # In Dos' Doors, we only need one lobby door, so ignore the rest
                if spoiler.settings.dos_door_rando and door.default_placed == DoorType.wrinkly and not door.dos_door:
                    continue
                door.placed = DoorType.null
                vanilla_door_indexes.append(door_index)
        spoiler.settings.random.shuffle(vanilla_door_indexes)
        # One random vanilla T&S per level is locked to being a T&S - Two non-vanilla Japes locations are eligible in Dos' Doors (hence that DoorType.null eligibility)
        locked_tns_options = [
            idx for idx in vanilla_door_indexes if door_locations[level][idx].default_placed in (DoorType.boss, DoorType.null) and DoorType.boss in door_locations[level][idx].door_type
        ]
        locked_tns_index = spoiler.settings.random.choice(locked_tns_options)
        locked_tns = door_locations[level][locked_tns_index]
        locked_tns.assignPortal(spoiler)
        human_portal_doors[level_list[level]]["T&S #1"] = locked_tns.name
        shuffled_door_data[level].append((locked_tns_index, DoorType.boss))
        vanilla_door_indexes.remove(locked_tns_index)
        # All other locations are fair game for hint doors - place one per kong
        for kong in [0, 3, 4, 2, 1]:  # The order of operations here matters because of our good friend Crystal Caves, which has restricted access to certain T&S locations
            assignee = Kongs(kong % 5)
            if level == Levels.CrystalCaves:
                # Caves must consider the kong_lst for each door - there's one T&S that only Diddy can logically access as well as one only Diddy/Lanky can logically access
                filtered_doors = [idx for idx in vanilla_door_indexes if assignee in door_locations[level][idx].kongs]
                selected_door_index = spoiler.settings.random.choice(filtered_doors)
                vanilla_door_indexes.remove(selected_door_index)
            else:
                # Everywhere else? Pick a door, any door
                selected_door_index = vanilla_door_indexes.pop(0)  # This should never fail
            selected_door = door_locations[level][selected_door_index]
            # Assign it to this Kong
            selected_door.assignDoor(assignee)
            human_hint_doors[level_list[level]][str(assignee.name).capitalize()] = selected_door.name
            shuffled_door_data[level].append((selected_door_index, DoorType.wrinkly, int(assignee)))
            # Add this hint door's location back to the logic
            doorLocation = GetDoorLocationForKongAndLevel(kong, level)
            region = spoiler.RegionList[selected_door.logicregion]
            region.locations.append(LocationLogic(doorLocation, selected_door.logic))
            spoiler.LocationList[doorLocation].name = f"{level_to_name[level]} Hint Door: {selected_door.name}"
        # Any remaining vanilla door that isn't occupied and is a T&S door will get a T&S - the number of doors here will vary based on how many hints were placed in lobby vs level
        placed_tns_count = 1
        for door_index in vanilla_door_indexes:
            vanilla_door = door_locations[level][door_index]
            if vanilla_door.placed == DoorType.null and vanilla_door.default_placed == DoorType.boss and DoorType.boss in vanilla_door.door_type:
                placed_tns_count += 1
                vanilla_door.assignPortal(spoiler)
                human_portal_doors[level_list[level]]["T&S #" + str(placed_tns_count)] = vanilla_door.name
                shuffled_door_data[level].append((door_index, DoorType.boss))

    # Track all touched doors in a variable and put it in the spoiler because changes to the static list do not save
    spoiler.shuffled_door_data = shuffled_door_data
    # Give human text to spoiler log
    if spoiler.settings.wrinkly_location_rando:
        spoiler.human_hint_doors = human_hint_doors
    if spoiler.settings.tns_location_rando:
        spoiler.human_portal_doors = human_portal_doors


def ClearHintDoorLogic(spoiler):
    """Remove existing hint door locations from the logic in preparation for custom door locations to be added."""
    for id, region in spoiler.RegionList.items():
        region.locations = [loclogic for loclogic in region.locations if loclogic.id < Locations.JapesDonkeyDoor or loclogic.id > Locations.CastleChunkyDoor]


def SetProgressiveHintDoorLogic(spoiler):
    """Set up hint door location logic for progressive hints to unlock them with GB amounts."""
    dont_clear_hints = Types.Hint in spoiler.settings.shuffled_location_types and not (spoiler.settings.vanilla_door_rando or spoiler.settings.wrinkly_location_rando)
    # Clear out old hint logic, including any custom logic that may have been placed. Don't need any of it.
    if not dont_clear_hints:
        ClearHintDoorLogic(spoiler)
    hint_count = 35
    hint_costs = []
    for i in range(hint_count):
        door_location = Locations.JapesDonkeyDoor + i  # Hint door locations are ordered in their unlocking
        hint_costs.append(getHintRequirement(i, spoiler.settings.progressive_hint_count))
    # I probably hate this more than you do but lambda functions in python REALLY like to mutate apparently
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_01, lambda l: l.canFulfillProgHint(hint_costs[0])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_02, lambda l: l.canFulfillProgHint(hint_costs[1])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_03, lambda l: l.canFulfillProgHint(hint_costs[2])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_04, lambda l: l.canFulfillProgHint(hint_costs[3])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_05, lambda l: l.canFulfillProgHint(hint_costs[4])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_06, lambda l: l.canFulfillProgHint(hint_costs[5])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_07, lambda l: l.canFulfillProgHint(hint_costs[6])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_08, lambda l: l.canFulfillProgHint(hint_costs[7])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_09, lambda l: l.canFulfillProgHint(hint_costs[8])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_10, lambda l: l.canFulfillProgHint(hint_costs[9])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_11, lambda l: l.canFulfillProgHint(hint_costs[10])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_12, lambda l: l.canFulfillProgHint(hint_costs[11])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_13, lambda l: l.canFulfillProgHint(hint_costs[12])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_14, lambda l: l.canFulfillProgHint(hint_costs[13])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_15, lambda l: l.canFulfillProgHint(hint_costs[14])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_16, lambda l: l.canFulfillProgHint(hint_costs[15])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_17, lambda l: l.canFulfillProgHint(hint_costs[16])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_18, lambda l: l.canFulfillProgHint(hint_costs[17])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_19, lambda l: l.canFulfillProgHint(hint_costs[18])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_20, lambda l: l.canFulfillProgHint(hint_costs[19])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_21, lambda l: l.canFulfillProgHint(hint_costs[20])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_22, lambda l: l.canFulfillProgHint(hint_costs[21])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_23, lambda l: l.canFulfillProgHint(hint_costs[22])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_24, lambda l: l.canFulfillProgHint(hint_costs[23])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_25, lambda l: l.canFulfillProgHint(hint_costs[24])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_26, lambda l: l.canFulfillProgHint(hint_costs[25])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_27, lambda l: l.canFulfillProgHint(hint_costs[26])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_28, lambda l: l.canFulfillProgHint(hint_costs[27])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_29, lambda l: l.canFulfillProgHint(hint_costs[28])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_30, lambda l: l.canFulfillProgHint(hint_costs[29])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_31, lambda l: l.canFulfillProgHint(hint_costs[30])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_32, lambda l: l.canFulfillProgHint(hint_costs[31])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_33, lambda l: l.canFulfillProgHint(hint_costs[32])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_34, lambda l: l.canFulfillProgHint(hint_costs[33])))
    spoiler.RegionList[Regions.GameStart].locations.append(LocationLogic(Locations.ProgressiveHint_35, lambda l: l.canFulfillProgHint(hint_costs[34])))
