from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

import csv
from . import Connections, Locations, Regions
from ..options import *
from ..constants import *

location_groups: dict[str, set[str]] = \
{
    LEVEL: set(),
    BOSS: set(),
    EMERALD: set(),
    OBJSANITY: set(),
    KEYSANITY: set(),
    CHECKPOINTSANITY: set(),
}


def get_full_location_list() -> list[LocationCSVData]:
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa

    full_location_list = []

    with files(Locations).joinpath(f"{LOCATIONS}.csv").open() as csv_file:
        reader = csv.DictReader(csv_file)
        for x in reader:
            #full_location_list[f"{x[LEVEL]} {x[TEAM]} {ACT} {x[ACT]} {x[NAME]}".replace(f"{ACT} 0 ", "")] = x[CODE]
            loc = LocationCSVData(x[NAME], int(x[CODE], 16), x[TEAM], x[LEVEL], int(x[ACT]), x[REGION], x[RULE], x[LOCATIONTYPE], x[HINTINFO], x[NOTES])
            location_groups[loc.loc_type].add(loc.name)
            full_location_list.append(loc)

    return full_location_list



def import_location_csv(world: SonicHeroesWorld, team: str):
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa

    for region in world.region_list:
        #print(region)
        pass

    with files(Locations).joinpath(f"{LOCATIONS}.csv").open() as csv_file:
        reader = csv.DictReader(csv_file)
        for x in reader:
            loc = LocationCSVData(x[NAME], int(x[CODE], 16), x[TEAM], x[LEVEL], int(x[ACT]), x[REGION], x[RULE], x[LOCATIONTYPE], x[HINTINFO], x[NOTES])

            #if loc.level in sonic_heroes_extra_names.values():
                #print(f"Location {loc} ", end="")

                #if is_loc_in_world(world, team, loc):
                    #print(f"SHOULD be in rando")

                #else:
                    #print(f"will not be in rando")

            #world.loc_id_to_loc[loc.code] = loc
            if is_loc_in_world(world, team, loc):
                #print(f"Adding Location {loc.name} to Region to Location[{loc.region}]")
                world.region_to_location[loc.region].append(loc)

    if world.secret:
        for level in world.allowed_levels_per_team[team]:
            if is_there_a_secret_csv_file(team, level):
                file_name = get_csv_file_name(team, level, LOCATIONS, True)

                with files(Locations).joinpath(f"{file_name}.csv").open() as csv_file:
                    reader = csv.DictReader(csv_file)
                    for x in reader:
                        loc = LocationCSVData(x[NAME], int(x[CODE], 16), x[TEAM], x[LEVEL], int(x[ACT]), x[REGION],
                                              x[RULE], x[LOCATIONTYPE], x[HINTINFO], x[NOTES])
                        # world.loc_id_to_loc[loc.code] = loc
                        if is_loc_in_world(world, team, loc):
                            #print(f"Adding Location {loc.name} to Region to Location[{loc.region}]")
                            world.region_to_location[loc.region].append(loc)



def import_region_csv(world: SonicHeroesWorld, team: str):
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa


    for level in world.allowed_levels_per_team[team]:
        file_name = get_csv_file_name(team, level, REGIONS, False)
        #print(f"File Name here: {file_name}")

    #for level, v in csv_file_names[team].items():
        #file_name = v[REGION]

        with files(Regions).joinpath(f"{file_name}.csv").open() as csv_file:
            reader = csv.DictReader(csv_file)
            for x in reader:
                if TEAM not in x:
                    #print(x)
                    pass

                reg = RegionCSVData(x[TEAM], x[LEVEL], f"{x[LEVEL]} {x[TEAM]} {x[NAME]}", int(x[OBJCHECKS]))
                world.region_list.append(reg)
                world.region_to_location[reg.name] = []

        if world.secret:
            if is_there_a_secret_csv_file(team, level):
                file_name = get_csv_file_name(team, level, REGIONS, True)

            #if v[SECRETREGION] is not None:
                #file_name = v[SECRETREGION]
                with files(Regions).joinpath(f"{file_name}.csv").open() as csv_file:
                    reader = csv.DictReader(csv_file)
                    for x in reader:
                        reg = RegionCSVData(x[TEAM], x[LEVEL], f"{x[LEVEL]} {x[TEAM]} {x[NAME]}", int(x[OBJCHECKS]))
                        world.region_list.append(reg)
                        world.region_to_location[reg.name] = []

        #print(f"Finished with File Name: {file_name}")




def import_connection_csv(world: SonicHeroesWorld, team: str):
    try:
        from importlib.resources import files
    except ImportError:
        from importlib_resources import files  # type: ignore # noqa

    id = 0
    for level in world.allowed_levels_per_team[team]:
        file_name = get_csv_file_name(team, level, CONNECTIONS, False)
        #print(f"File Name here: {file_name}")

    #for level, v in csv_file_names[team].items():
        #file_name = v[CONNECTION]
        #print(f"File Name here: {file_name}")
        with files(Connections).joinpath(f"{file_name}.csv").open() as csv_file:
            reader = csv.DictReader(csv_file)
            for x in reader:
                rule = x[RULE]
                if "" == x[RULE]:
                    rule = "Nothing"

                source = find_index_of_region(world,f"{x[LEVEL]} {x[TEAM]} {x[SOURCE]}")
                target = find_index_of_region(world,f"{x[LEVEL]} {x[TEAM]} {x[TARGET]}")

                if source < 0:
                    #print(f"{x[LEVEL]} {x[TEAM]} {x[SOURCE]} not in region list")
                    raise ValueError("Source Out of Bounds")
                if target < 0:
                    #print(f"{x[LEVEL]} {x[TEAM]} {x[TARGET]} not in region list")
                    raise ValueError("Target Out of Bounds")

                conn = ConnectionCSVData(f"{source} > {target} with Rule: {rule}", x[TEAM], x[LEVEL], f"{x[LEVEL]} {x[TEAM]} {x[SOURCE]}", f"{x[LEVEL]} {x[TEAM]} {x[TARGET]}", x[RULE])
                id += 1
                world.connection_list.append(conn)

        if world.secret:
            if is_there_a_secret_csv_file(team, level):
                file_name = get_csv_file_name(team, level, CONNECTIONS, True)

            #if v[SECRETCONNECTION] is not None:
                #file_name = v[SECRETCONNECTION]
                with files(Connections).joinpath(f"{file_name}.csv").open() as csv_file:
                    reader = csv.DictReader(csv_file)
                    for x in reader:
                        rule = x[RULE]
                        if "" == x[RULE]:
                            rule = "Nothing"
                        source = find_index_of_region(world, f"{x[LEVEL]} {x[TEAM]} {x[SOURCE]}")
                        target = find_index_of_region(world, f"{x[LEVEL]} {x[TEAM]} {x[TARGET]}")
                        conn = ConnectionCSVData(f"{source} > {target} with Rule: {rule}", x[TEAM], x[LEVEL],
                                                 f"{x[LEVEL]} {x[TEAM]} {x[SOURCE]}",
                                                 f"{x[LEVEL]} {x[TEAM]} {x[TARGET]}", x[RULE])
                        id += 1
                        world.connection_list.append(conn)


def is_loc_in_world(world: SonicHeroesWorld, team: str, loc: LocationCSVData) -> bool:
    codes: list[int] = \
        [
            #0x9393230E,
            #0x939300a4,
            #0x939300a6,
            #0x93931706,
            #0x93931708,
            #0x93931806,
            #0x93931808,
            #0x93931906,
            #0x93931908,
            #0x93932009,
            #0x9393200D,
            #0x93932109,
            #0x9393210D,
            #0x93932209,
            #0x9393220D,
        ]

    if "SUPER SECRET HIDDEN" in loc.name and not world.secret:
        return False

    if loc.name == METALOVERLORD:
        for locCsvData in world.region_to_location[loc.region]:
            if locCsvData.name == METALOVERLORD:
                return False
        #print(f"Adding {loc.name} to {loc.region}")
        return True


    if loc.code in codes:
        #print(f"Loc {loc.name} ID {hex(loc.code)} has a region {loc.region}")
        pass

    if loc.team != team and loc.team != ANYTEAM:
        if loc.code in codes:
            #print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not matching team")
            pass
        return False

    if loc.loc_type == SECRET and not world.secret:
        if loc.code in codes:
            #print(f"Loc {loc.name} ID {hex(loc.code)} failed because of secret type")
            pass
        return False


    if team == SONIC:
        return is_loc_in_world_sonic(world, loc)

    if team == DARK:
        return is_loc_in_world_dark(world, loc)

    if team == ROSE:
        return is_loc_in_world_rose(world, loc)

    if team == CHAOTIX:
        return is_loc_in_world_chaotix(world, loc)

    if team == SUPERHARDMODE:
        return is_loc_in_world_superhard(world, loc)

    print(f"How did we get here (end of is_loc_in_world)? {loc}")
    return True


def find_index_of_region(world, name):
    index = 0
    for reg in world.region_list:
        if reg.name == name:
            return index
        index += 1
    #print(f"Region {name} not found")
    return -1




def is_loc_in_world_sonic(world: SonicHeroesWorld, loc: LocationCSVData):
    if loc.level not in world.allowed_levels_per_team[SONIC] and loc.loc_type != EMERALD and loc.loc_type != BOSS:
        # needs to be allowed first
        #print(f"")
        return False

    if loc.loc_type == LEVEL:
        if SONICACTA in world.options.included_levels_and_sanities and not SONICACTB in world.options.included_levels_and_sanities and loc.act != 1:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when Act 1 only")
            return False

        if not SONICACTA in world.options.included_levels_and_sanities and SONICACTB in world.options.included_levels_and_sanities and loc.act != 2:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when Act 2 only")
            return False

        """
        if world.options.sonic_story == SonicStory.option_mission_a_only and loc.act != 1 and METALOVERLORD not in loc.name:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when Act 1 only")
            return False
        if world.options.sonic_story == SonicStory.option_mission_b_only and loc.act != 2 and METALOVERLORD not in loc.name:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when Act 2 only")
            return False
        if world.options.super_hard_mode and loc.act == 2:
            #Sonic Act 2 while SuperHard is on
            return False
        """

    if loc.loc_type == BOSS:
        if loc.level in world.boss_locations_added:
            return True
        return False

    if loc.loc_type == EMERALD:
        if " ".join(loc.level.split(" ")[:-2]) in world.allowed_levels_per_team[SONIC]:
            if loc.name not in world.emerald_locations_added:
                world.emerald_locations_added.append(loc.name)
                return True
        return False

    if loc.loc_type == OBJSANITY:
        #there are no OBJSANITY locations for Sonic
        return False

    #if loc.loc_type == CHECKPOINTSANITY:
        """
        if world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_disabled:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Checkpoint Sanity Disabled")
            return False
        if world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_only_1_set_normal and loc.act != 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 0 with Checkpoint Sanity only 1 Set")
            return False
        
        if world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_only_super_hard:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of only Super Hard Checkpoint Sanity (when loc is Sonic Checkpoint)")
            return False

        if world.options.sonic_checkpoint_sanity == SonicCheckpointSanity.option_set_for_each_act:
            if loc.act == 0:
                # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Act 0 with Checkpoint Sanity set to each Act")
                return False
            if world.options.sonic_story == SonicStory.option_mission_a_only and loc.act != 1:
                # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when Act 1 only")
                return False
            if world.options.sonic_story == SonicStory.option_mission_b_only and loc.act != 2:
                # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when Act 2 only")
                return False
            if loc.act == 2 and world.options.super_hard_mode:
                #Act 2 checkpoint when Super Hard Mode is on (separate option)
                return False
        """

    # if loc.loc_type == KEYSANITY:
        """
        if world.options.sonic_key_sanity == SonicKeySanity.option_disabled:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Key Sanity Disabled")
            return False
        if world.options.sonic_key_sanity == SonicKeySanity.option_only_1_set and loc.act != 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 0 when only 1 Set")
            return False
    
        if world.options.sonic_key_sanity == SonicKeySanity.option_set_for_each_act:
            if loc.act == 0:
                # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Act 0 when each Act")
                return False
            if world.options.sonic_story == SonicStory.option_mission_a_only and loc.act != 1:
                # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when only Act 1")
                return False
            if world.options.sonic_story == SonicStory.option_mission_b_only and loc.act != 2:
                # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when only Act 2")
                return False
            if loc.act == 2 and world.options.super_hard_mode:
                # Act 2 key when Super Hard Mode is on
                return False
        """


    if loc.loc_type == KEYSANITY or loc.loc_type == CHECKPOINTSANITY:
        if not world.is_this_sanity_enabled(SONIC, loc.loc_type):
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Checkpoint Sanity Disabled")
            return False

        if world.is_this_sanity_enabled(SONIC, loc.loc_type) and not world.is_this_sanity_enabled(SONIC, loc.loc_type, both_acts_required=True) and loc.act != 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 0 with Checkpoint Sanity only 1 Set")
            return False

        if world.is_this_sanity_enabled(SONIC, loc.loc_type, both_acts_required=True) and loc.act == 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Act 0 with Checkpoint Sanity set to each Act")
            return False


    return True


def is_loc_in_world_dark(world: SonicHeroesWorld, loc: LocationCSVData):
    if loc.level not in world.allowed_levels_per_team[DARK] and loc.loc_type != EMERALD and loc.loc_type != BOSS:
        # needs to be allowed first
        # print(f"")
        return False

    if loc.loc_type == LEVEL:
        if DARKACTA in world.options.included_levels_and_sanities and not DARKACTB in world.options.included_levels_and_sanities and loc.act != 1:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when Act 1 only")
            return False

        if not DARKACTA in world.options.included_levels_and_sanities and DARKACTB in world.options.included_levels_and_sanities and loc.act != 2:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when Act 2 only")
            return False

    if loc.loc_type == BOSS:
        if loc.level in world.boss_locations_added:
            return True
        return False

    if loc.loc_type == EMERALD:
        if " ".join(loc.level.split(" ")[:-2]) in world.allowed_levels_per_team[DARK]:
            if loc.name not in world.emerald_locations_added:
                world.emerald_locations_added.append(loc.name)
                return True
        return False

    if loc.loc_type == OBJSANITY:
        if not world.is_this_sanity_enabled(DARK, OBJSANITY):
            return False

        if int(loc.name[loc.name.index(":"):].replace(":", "").replace(" ", "")) % world.options.dark_sanity.value == 0:
            #modulus of check # and sanity value is 0, return true (check # 10 is in if sanity < 20)
            return True

        return False

    if loc.loc_type == KEYSANITY or loc.loc_type == CHECKPOINTSANITY:
        if not world.is_this_sanity_enabled(DARK, loc.loc_type):
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Checkpoint Sanity Disabled")
            return False

        if world.is_this_sanity_enabled(DARK, loc.loc_type) and not world.is_this_sanity_enabled(DARK, loc.loc_type, both_acts_required=True) and loc.act != 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 0 with Checkpoint Sanity only 1 Set")
            return False

        if world.is_this_sanity_enabled(DARK, loc.loc_type, both_acts_required=True) and loc.act == 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Act 0 with Checkpoint Sanity set to each Act")
            return False

    #print(f"Dark Location Passing at end of func. {loc}")
    return True


def is_loc_in_world_rose(world: SonicHeroesWorld, loc: LocationCSVData):
    if loc.level not in world.allowed_levels_per_team[ROSE] and loc.loc_type != EMERALD and loc.loc_type != BOSS:
        # needs to be allowed first
        # print(f"")
        return False

    if loc.loc_type == LEVEL:
        if ROSEACTA in world.options.included_levels_and_sanities and not ROSEACTB in world.options.included_levels_and_sanities and loc.act != 1:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when Act 1 only")
            return False

        if not ROSEACTA in world.options.included_levels_and_sanities and ROSEACTB in world.options.included_levels_and_sanities and loc.act != 2:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when Act 2 only")
            return False

    if loc.loc_type == BOSS:
        if loc.level in world.boss_locations_added:
            return True
        return False

    if loc.loc_type == EMERALD:
        if " ".join(loc.level.split(" ")[:-2]) in world.allowed_levels_per_team[ROSE]:
            if loc.name not in world.emerald_locations_added:
                world.emerald_locations_added.append(loc.name)
                return True
        return False

    if loc.loc_type == OBJSANITY:
        if not world.is_this_sanity_enabled(ROSE, OBJSANITY):
            return False

        if int(loc.name[loc.name.index(":"):].replace(":", "").replace(" ", "")) % world.options.rose_sanity.value == 0:
            # modulus of check # and sanity value is 0, return true (check # 10 is in if sanity < 20)
            return True

        return False

    if loc.loc_type == KEYSANITY or loc.loc_type == CHECKPOINTSANITY:
        if not world.is_this_sanity_enabled(ROSE, loc.loc_type):
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Checkpoint Sanity Disabled")
            return False

        if world.is_this_sanity_enabled(ROSE, loc.loc_type) and not world.is_this_sanity_enabled(ROSE, loc.loc_type, both_acts_required=True) and loc.act != 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 0 with Checkpoint Sanity only 1 Set")
            return False

        if world.is_this_sanity_enabled(ROSE, loc.loc_type, both_acts_required=True) and loc.act == 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Act 0 with Checkpoint Sanity set to each Act")
            return False
    return True


def is_loc_in_world_chaotix(world: SonicHeroesWorld, loc: LocationCSVData):
    if loc.level not in world.allowed_levels_per_team[CHAOTIX] and loc.loc_type != EMERALD and loc.loc_type != BOSS:
        # needs to be allowed first
        # print(f"")
        return False

    if loc.loc_type == LEVEL:
        if CHAOTIXACTA in world.options.included_levels_and_sanities and not CHAOTIXACTB in world.options.included_levels_and_sanities and loc.act != 1:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 1 when Act 1 only")
            return False

        if not CHAOTIXACTA in world.options.included_levels_and_sanities and CHAOTIXACTB in world.options.included_levels_and_sanities and loc.act != 2:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 2 when Act 2 only")
            return False

    if loc.loc_type == BOSS:
        if loc.level in world.boss_locations_added:
            return True
        return False

    if loc.loc_type == EMERALD:
        if " ".join(loc.level.split(" ")[:-2]) in world.allowed_levels_per_team[CHAOTIX]:
            if loc.name not in world.emerald_locations_added:
                world.emerald_locations_added.append(loc.name)
                return True
        return False

    if loc.loc_type == OBJSANITY:
        if not world.is_this_sanity_enabled(CHAOTIX, OBJSANITY):
            return False

        if loc.level != CASINOPARK:
            return True

        if int(loc.name[loc.name.index(":"):].replace(":", "").replace(" ", "")) % world.options.chaotix_sanity.value == 0:
            # modulus of check # and sanity value is 0, return true (check # 10 is in if sanity < 20)
            return True

        return False

    if loc.loc_type == KEYSANITY or loc.loc_type == CHECKPOINTSANITY:
        if not world.is_this_sanity_enabled(CHAOTIX, loc.loc_type):
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Checkpoint Sanity Disabled")
            return False

        if world.is_this_sanity_enabled(CHAOTIX, loc.loc_type) and not world.is_this_sanity_enabled(CHAOTIX, loc.loc_type, both_acts_required=True) and loc.act != 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of not Act 0 with Checkpoint Sanity only 1 Set")
            return False

        if world.is_this_sanity_enabled(CHAOTIX, loc.loc_type, both_acts_required=True) and loc.act == 0:
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Act 0 with Checkpoint Sanity set to each Act")
            return False
    return True


def is_loc_in_world_superhard(world: SonicHeroesWorld, loc: LocationCSVData):
    if loc.level not in world.allowed_levels_per_team[SUPERHARDMODE] and loc.loc_type != EMERALD and loc.loc_type != BOSS:
        # needs to be allowed first
        # print(f"")
        return False

    if loc.loc_type == LEVEL:
        if world.is_this_team_enabled(SUPERHARDMODE):
            return True
        return False

    if loc.loc_type == BOSS:
        if loc.level in world.boss_locations_added:
            return True
        return False

    if loc.loc_type == EMERALD:
        if " ".join(loc.level.split(" ")[:-2]) in world.allowed_levels_per_team[SUPERHARDMODE]:
            if loc.name not in world.emerald_locations_added:
                world.emerald_locations_added.append(loc.name)
                return True
        return False

    if loc.loc_type == OBJSANITY:
        #currently are none
        return False

    if loc.loc_type == CHECKPOINTSANITY:
        if not world.is_this_sanity_enabled(SUPERHARDMODE, CHECKPOINTSANITY):
            # print(f"Loc {loc.name} ID {hex(loc.code)} failed because of Checkpoint Sanity Disabled")
            return False
        return True

    return True

