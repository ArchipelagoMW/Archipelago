

import importlib
import os
import pkgutil
import sys
import time

from BaseClasses import MultiWorld
from . import Levels, Names, ShTHClient, Objects, ShtHWorld, Options, Rules
from .Items import GetAllItemInfo
from .Levels import INDIVIDUAL_LEVEL_REGIONS, BACKTRACKING_REGIONS
from .Locations import GetAllLocationInfo
from .Names import REGION_INDICES, REGION_RESTRICTION_TYPES
from .Objects import DESIRABLE_OBJECTS
from .Objects_AirFleet import DESIRABLE_OBJECTS_AIR_FLEET
from .Objects_GlyphicCanyon import DESIRABLE_OBJECTS_GLYPHIC_CANYON
from .Objects_PrisonIsland import DESIRABLE_OBJECTS_PRISON_ISLAND
from .Options import ShadowTheHedgehogOptions


def TestA():
    dir = "C:\\Users\\Alex\\Downloads\\SHADOWTEST"

    inis = {}

    files = os.listdir(dir)
    for f in files:
        f2 = open(dir+"/"+f)
        data = f2.readlines()
        dic = {

        }

        section = "SectionError"
        for line in data:
            line = line.strip()
            if line.startswith("["):
                section = line
            else:
                s = line.split("=")
                if len(s) > 1:
                    dic[section+ "-" + s[0]] = s[1]

        inis[f] = dic

        f2.close()

    base = "Choatix.ini"

    mine = inis[base]
    for key in mine:
        my_value = mine[key]
        for i in inis.keys():
            if i == base:
                continue

            d = inis[i]

            if key not in d:
                print("Missing key from base:", key, i)
            else:
                their_value = d[key]
                if their_value != my_value:
                    print("Different key from base", i, key, my_value, their_value)


#TestA()
#sys.exit(1)


def LoadSetSummary():
    file = "C:/Users/Alex/Documents/SetSummary.txt"

    f = open(file)
    data = f.readlines()
    f.close()

    unknown_types = []
    info_for_unknown_types = []
    current_level = None
    for line in data:
        s = line.strip()
        if len(s) == 0:
            continue

        if line.startswith("SET has changed"):
            #SET has changed: index=152, type=Weapon Box: Weapon:Semi Automatic Rifle, old=None, new=1, behind 6

            line = line.replace("SET has changed: ", "")
            split = line.split(",")
            index_data = split[0]
            index_split = index_data.split("=")
            index_value = index_split[1]

            type_data = split[1]
            type_string = type_data[6:]
            secondary_type_string = None

            if type_string.startswith("Weapon Box: Weapon:"):
                secondary_type_string = type_string[19:]
                type_string = "Weapon Box"
            elif type_string.startswith("Weapon Wood Box : Weapon:"):
                secondary_type_string = type_string[25:]
                type_string = "Wooden Weapon Box"
            elif type_string.startswith("Weapon Metal Box : Weapon:"):
                secondary_type_string = type_string[26:]
                type_string = "Metal Weapon Box"
            elif type_string == "Environment Weapon":
                secondary_type_string = "STAGE ITEM"
                type_string = "Environment Weapon"
            elif type_string == "Weapon":
                type_string = "Weapon"
                secondary_type_string = "Unknown"
            else:
                print("Unhandled info at this time", type_string)
                if type_string not in unknown_types:
                    unknown_types.append(type_string)

                info_for_unknown_types.append(line)
                continue
                #time.sleep(5)

            old_data = split[2]
            new_data = split[3]

            if len(split) > 4:
                other_data = split[4]
            else:
                other_data = None

            new_split = new_data.split("=")
            if len(new_split[1]) > 1:
                other_data = new_split[1][1:].strip()

            if type_string == "Weapon":
                type_string = "FLOOR_WEAPON"
                secondary_type_string = secondary_type_string.upper().replace(" ", "_")
            elif type_string == "Weapon Box":
                type_string = "WEAPON_BOX"
                secondary_type_string = secondary_type_string.upper().replace(" ", "_")
            elif type_string == "Metal Weapon Box":
                type_string = "WEAPON_METAL_BOX"
                secondary_type_string = secondary_type_string.upper().replace(" ", "_")
            elif type_string == "Wooden Weapon Box":
                type_string = "WEAPON_WOODEN_BOX"
                secondary_type_string = secondary_type_string.upper().replace(" ", "_")
            elif type_string == "Environment Weapon":
                type_string = "ENVIRONMENT_WEAPON"
                secondary_type_string = secondary_type_string.upper().replace(" ", "_")
            #else:
            #    print("Not yet handled", type_string)
            #    #time.sleep(2)

            current_level_lookup = current_level.replace("BOSS", "").replace("STAGE", "")
            inverted = {v.upper().replace(' ','_').replace('STAGE_', '').replace('BOSS_', ''): k for k, v in Levels.LEVEL_ID_TO_LEVEL.items()}
            if current_level.endswith("_LS"):
                current_level_lookup = current_level.replace("_LS", "_LAVA_SHELTER")
            if current_level.endswith("_LH"):
                current_level_lookup = current_level.replace("_LH", "_LETHAL_HIGHWAY")
            if current_level.endswith("_DR"):
                current_level_lookup = current_level.replace("_DR", "_DEATH_RUINS")
            if current_level.endswith("IJ"):
                current_level_lookup = current_level.replace("_IJ", "_IRON_JUNGLE")
            if current_level.endswith("_MM"):
                current_level_lookup = current_level.replace("_MM", "_MAD_MATRIX")
            if current_level.endswith("_CC"):
                current_level_lookup = current_level.replace("_CC", "_CRYPTIC_CASTLE")
            if current_level.endswith("_GF"):
                current_level_lookup = current_level.replace("_GF", "_GUN_FORTRESS")
            if current_level.endswith("_BC"):
                current_level_lookup = current_level.replace("_BC", "_BLACK_COMET")
            if current_level.endswith("_CF"):
                current_level_lookup = current_level.replace("_CF", "_COSMIC_FALL")
            if current_level.endswith("_FH"):
                current_level_lookup = current_level.replace("_FH", "_FINAL_HAUNT")
            #print(inverted)
            if current_level_lookup in inverted:
                level_id = inverted[current_level_lookup]
                found = [ x for x in DESIRABLE_OBJECTS if x.stage == level_id and int(index_value) == x.index ]

                other_data_to_show = other_data.strip().replace(' ', '_').upper()
                other_data_to_show = other_data_to_show.replace("1", "ONE")
                other_data_to_show = other_data_to_show.replace("2", "two")
                other_data_to_show = other_data_to_show.replace("3", "three")
                other_data_to_show = other_data_to_show.replace("4", "four")
                other_data_to_show = other_data_to_show.replace("5", "fivE")
                other_data_to_show = other_data_to_show.replace("6", "siz")
                other_data_to_show = other_data_to_show.replace("7", "seven")
                other_data_to_show = other_data_to_show.replace("8", "eigh")
                other_data_to_show = other_data_to_show.replace("9", "ninE")
                other_data_to_show = other_data_to_show.replace("0", "zero")

                if len(found) == 0:
                    s = (f"SETObject(ObjectType.{type_string}, Levels.STAGE_{current_level}, {index_value}, \'{index_value}\', "
                         f"\r\n\tregion=REGION_INDICES.{other_data_to_show}, weapon=WEAPONS.{secondary_type_string}),")
                    print(s)
            else:
                print("No key for:", current_level, current_level_lookup, inverted)

            #print("SETTY is", "index", index_value, "type", type_string, "secondary type", secondary_type_string, "region info", other_data)
        else:
            print("Data for line is", line)
            current_level = line.replace(" ", "_").upper().strip()

    print(unknown_types)

    #for l in info_for_unknown_types:
    #    print(l)


def TestCheckpointPathing():
    escapes = Levels.RegionEscapes

    errors = 0

    options = ShadowTheHedgehogOptions.__new__(ShadowTheHedgehogOptions)
    options.logic_level = Options.LogicLevel.option_normal
    options.start_inventory = {}
    options.object_unlocks = True
    options.object_pulleys = True
    options.object_ziplines = True
    options.object_units = True
    options.object_rockets = True
    options.object_light_dashes = True
    options.object_warp_holes = True

    options.weapon_sanity_unlock = True
    options.vehicle_logic = True
    options.keys_required_for_doors = 5
    options.key_collection_method = Options.KeyCollectionMethod.option_arch
    options.chaos_control_logic_level = Options.ChaosControlLogicLevel.option_off

    all_results = Rules.GetAllCheckpointEscapes(options)
    print(all_results)

    CheckRules = Rules.CHECKPOINT_ESCAPE_GROUPS

    for stage,results in all_results.items():
        stuck_regions = results[0]
        inescapable_regions = results[1]

        if stage not in CheckRules:
            if len(stuck_regions) + len(inescapable_regions) > 0 :
                print("Stage not found in groups", stage, stuck_regions, inescapable_regions)
                errors += 1
        else:
            groups = CheckRules[stage]
            known_groups = []

            for g in groups.values():
                known_groups.extend(g)

            for item in stuck_regions:
                if item not in known_groups:
                    print("Region not found in groups", stage,item)
                    errors += 1

            for item in inescapable_regions:
                if item not in known_groups:
                    print("Region not found in groups", stage, item)
                    errors += 1


    return errors


def TestRegionIndicies():
    regions = INDIVIDUAL_LEVEL_REGIONS

    errors = 0

    previous = None
    previousStage = None
    print(len(regions))
    for region in regions:

        if previous is not None and previousStage is not None:
            if previousStage != region.stageId:
                pass
                #print("Change to level", region.stageId, region.regionIndex)
            else:
                if region.regionIndex < previous:
                    print("Error with", region.stageId, region.regionIndex)
                    errors += 1

        previous = region.regionIndex
        previousStage = region.stageId

    return errors


def TestItemIds():
    items = GetAllItemInfo()

    result = {}
    error_count = 0
    for i_set in items:
        for item in i_set:
            if item.itemId in result:
                print("Duplicate item ID", result[item.itemId].name, item.name, item.itemId)
                error_count += 1
            else:
                result[item.itemId] = item

    return error_count


def TestLocationStageReference():
    locations = GetAllLocationInfo()
    error_count = 0
    for l_set in locations:
        for location in l_set:
            if location.stageId is not None:
                if Levels.LEVEL_ID_TO_LEVEL[location.stageId] not in location.name:
                    print("Suspicious name for ", location.name, "for stage", Levels.LEVEL_ID_TO_LEVEL[location.stageId])

    return error_count

def TestLocationIds():
    locations = GetAllLocationInfo()
    result = {}
    error_count = 0
    for l_set in locations:
        for location in l_set:
            if location.locationId in result:
                print("Duplicate location ID", result[location.locationId].name, location.name, location.locationId)
                error_count += 1
            else:
                result[location.locationId] = location

            if location.stageId is not None:
                if Levels.LEVEL_ID_TO_LEVEL[location.stageId] not in location.name:
                    print("Suspicious name for ", location.name, "for stage", Levels.LEVEL_ID_TO_LEVEL[location.stageId])

    return error_count


previous_stage = None
enemy_for_stage = None
last_was_enemy = False
for item in DESIRABLE_OBJECTS:
    if previous_stage is None:
        previous_stage = item.stage
        last_was_enemy = False
        enemy_for_stage = None
    elif previous_stage != item.stage:
        previous_stage = item.stage
        last_was_enemy = False
        enemy_for_stage = None

    if item.object_type in Objects.GetStandardEnemyTypes():
        if enemy_for_stage is None:
            enemy_for_stage = True
        elif not enemy_for_stage:
            print("Order error with:", item.stage, item.index)

        last_was_enemy = True
    else:
        if enemy_for_stage:
            enemy_for_stage = False


def TestSlotData():
    mw = MultiWorld(1)
    world = ShtHWorld(mw, 1)

    o = ShadowTheHedgehogOptions.__dict__
    print(o)

    slot_data = ShtHWorld.fill_slot_data(world)


    for option in world.options.__dict__:
        print(option)


#for item in DESIRABLE_OBJECTS_PRISON_ISLAND:
#    o = ShTHClient.EnemyToCodeString(item)
#    print(o)

errors = 0

#errors = TestSlotData()
errors += TestCheckpointPathing()

errors +=  TestItemIds()
errors += TestLocationIds()
errors += TestLocationStageReference()
errors += TestRegionIndicies()


print("ERROR count is", errors)

if errors > 0:
    sys.exit(1)


