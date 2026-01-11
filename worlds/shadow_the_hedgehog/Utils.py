from math import ceil, floor
from typing import Tuple

from . import Levels, Locations

VERSION: Tuple[int, int, int] = (0, 3, 3)

TYPE_ID_ENEMY = 0
TYPE_ID_OBJECTIVE = 1
TYPE_ID_COMPLETION = 2
TYPE_ID_OBJECTIVE_AVAILABLE = 3
TYPE_ID_OBJECTIVE_ENEMY = 4
TYPE_ID_OBJECTIVE_ENEMY_COMPLETION = 5
TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE = 6
TYPE_ID_OBJECTIVE_FREQUENCY = 7
TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY = 8
TYPE_ID_ENEMY_FREQUENCY = 9

def GetVersionString():
    return f"{VERSION[0]}.{VERSION[1]}.{VERSION[2]}"
def getRequiredCount(total, percentage,
                     round_method=ceil,
                     override=None):

    if override is not None:
        percentage = override

    required_count = round_method(total * percentage / 100)
    if required_count == 0 and percentage != 0:
        required_count += 1

    return int(required_count)

def getRequiredPercentage(percentage,
                     round_method=ceil,
                     override=None):

    if override is not None:
        percentage = override

    return percentage

def GetOverrideKey(typeId, alignmentId):
    type_name = None
    if typeId == TYPE_ID_ENEMY:
        if alignmentId == Locations.ENEMY_CLASS_ALIEN:
            type_name = "EA"
        elif alignmentId == Locations.ENEMY_CLASS_GUN:
            type_name = "EG"
        elif alignmentId == Locations.ENEMY_CLASS_EGG:
            type_name = "EE"
    elif typeId == TYPE_ID_OBJECTIVE:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OH"
    elif typeId == TYPE_ID_COMPLETION:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "CD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "CH"
    elif typeId == TYPE_ID_OBJECTIVE_AVAILABLE:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "AD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "AH"
    elif typeId == TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "AED"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "AEH"
    elif typeId == TYPE_ID_OBJECTIVE_ENEMY:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OED"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OEH"
    elif typeId == TYPE_ID_OBJECTIVE_ENEMY_COMPLETION:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OECD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OECH"

    elif typeId == TYPE_ID_OBJECTIVE_FREQUENCY:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OFD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OFH"

    elif typeId == TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY:
        if alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            type_name = "OEFD"
        elif alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            type_name = "OEFH"

    elif typeId == TYPE_ID_ENEMY_FREQUENCY:
        if alignmentId == Locations.ENEMY_CLASS_EGG:
            type_name = "EFE"
        if alignmentId == Locations.ENEMY_CLASS_GUN:
            type_name = "EFG"
        if alignmentId == Locations.ENEMY_CLASS_ALIEN:
            type_name = "EFH"

    return type_name



def GetValidOverrideKeys():
    valid_keys = []
    for missionClear in Locations.MissionClearLocations:
        if missionClear.mission_object_name is None:
            print("Skip", missionClear.stageId, missionClear.alignmentId)
            continue
        objective_key_type, objective_key_x, \
        objective_key_y = getObjectiveTypeAndPercentage(TYPE_ID_OBJECTIVE,
                                                      missionClear.mission_object_name, None,
                                                      missionClear.stageId, missionClear.alignmentId,
                                                      None)
        key_part = GetOverrideKey(objective_key_type, missionClear.alignmentId)
        key = key_part + "."+ Levels.LEVEL_ID_TO_LEVEL[missionClear.stageId]
        valid_keys.append(key)

        objective_key_type, objective_key_x, \
            objective_key_y = getObjectiveTypeAndPercentage(TYPE_ID_COMPLETION,
                                                            missionClear.mission_object_name, None,
                                                            missionClear.stageId, missionClear.alignmentId,
                                                            None)
        key_part = GetOverrideKey(objective_key_type, missionClear.alignmentId)
        key = key_part + "." + Levels.LEVEL_ID_TO_LEVEL[missionClear.stageId]
        valid_keys.append(key)

        objective_key_type, objective_key_x, \
            objective_key_y = getObjectiveTypeAndPercentage(TYPE_ID_OBJECTIVE_AVAILABLE,
                                                            missionClear.mission_object_name, None,
                                                            missionClear.stageId, missionClear.alignmentId,
                                                            None)
        key_part = GetOverrideKey(objective_key_type, missionClear.alignmentId)
        if key_part is not None:
            key = key_part + "." + Levels.LEVEL_ID_TO_LEVEL[missionClear.stageId]
            valid_keys.append(key)

        objective_key_type, objective_key_x, \
            objective_key_y = getObjectiveTypeAndPercentage(TYPE_ID_OBJECTIVE_FREQUENCY,
                                                            missionClear.mission_object_name, None,
                                                            missionClear.stageId, missionClear.alignmentId,
                                                            None)
        key_part = GetOverrideKey(objective_key_type, missionClear.alignmentId)
        if key_part is not None:
            key = key_part + "." + Levels.LEVEL_ID_TO_LEVEL[missionClear.stageId]
            valid_keys.append(key)

    for enemy in Locations.GetEnemySanityLocations():
        objective_key_type, objective_key_x, objective_key_y = getObjectiveTypeAndPercentage(TYPE_ID_ENEMY,
                                                        enemy.mission_object_name, None,
                                                        enemy.stageId, enemy.enemyClass,
                                                        None)
        key_part = GetOverrideKey(objective_key_type, enemy.enemyClass)
        if key_part is not None:
            key = key_part + "." + Levels.LEVEL_ID_TO_LEVEL[enemy.stageId]
            valid_keys.append(key)

        objective_key_type, objective_key_x, objective_key_y = getObjectiveTypeAndPercentage(TYPE_ID_ENEMY_FREQUENCY,
                                                                                             enemy.mission_object_name, None,
                                                                                             enemy.stageId,
                                                                                             enemy.enemyClass,
                                                                                             None)
        key_part = GetOverrideKey(objective_key_type, enemy.enemyClass)
        if key_part is not None:
            key = key_part + "." + Levels.LEVEL_ID_TO_LEVEL[enemy.stageId]
            valid_keys.append(key)

    i = 0
    while i < len(valid_keys):
        print(valid_keys[i:i+4])
        i += 4
    return valid_keys


def getOverwriteRequiredCount(override_settings, stageId, alignmentId, typeId):
    key = "{type}.{stageName}"

    type_name = GetOverrideKey(typeId, alignmentId)

    level_name = Levels.LEVEL_ID_TO_LEVEL[stageId]
    key_lookup = key.format(type=type_name, stageName=level_name)

    if key_lookup in override_settings:
        return override_settings[key_lookup]

    return None

def isEnemyObjectiveLocation(name):
    if "Soldier" in name or "Alien" in name or "Artificial Chaos" in name:
        return True

    return False

# TODO: Needs to work with percentage as well...
def getObjectiveTypeAndPercentage(base_objective_type, item_name, options,
                                  stage, alignment, overrides):

    if options is not None and not options.objective_sanity:
        if base_objective_type in (TYPE_ID_OBJECTIVE_AVAILABLE, TYPE_ID_OBJECTIVE,
                                   TYPE_ID_OBJECTIVE_ENEMY,
                                   TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE, TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY,
                                   TYPE_ID_OBJECTIVE_FREQUENCY):
            return None

    percentage = None
    round_method = None
    required_for_completion = None
    if base_objective_type == TYPE_ID_OBJECTIVE:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY
            percentage = options.objective_enemy_percentage if options is not None else None
            round_method = floor
        else:
            percentage = options.objective_percentage if options is not None else None
            round_method = ceil
    if base_objective_type == TYPE_ID_COMPLETION:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY_COMPLETION
            percentage = options.objective_completion_enemy_percentage if options is not None else None
            round_method = floor
        else:
            percentage = options.objective_completion_percentage if options is not None else None
            round_method = floor

    if base_objective_type == TYPE_ID_OBJECTIVE_AVAILABLE:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE
            if options is not None:
                # Available needs to do a lookup on completion inc. overrides

                #percentage = options.objective_enemy_available_percentage if options is not None else None
                required_for_completion = getPercRequired(
                    getObjectiveTypeAndPercentage(TYPE_ID_COMPLETION,item_name, options, stage, alignment, overrides),
                    stage,alignment,overrides)

                percentage = options.objective_item_enemy_percentage_available if options is not None else None
                round_method = ceil
        else:
            if options is not None:
                required_for_completion = getPercRequired(
                    getObjectiveTypeAndPercentage(TYPE_ID_COMPLETION, item_name, options, stage, alignment, overrides),
                    stage, alignment, overrides)

                percentage = options.objective_item_percentage_available if options is not None else None

                #percentage = (required_for_completion *\
                #              ((100 + options.objective_item_percentage_available)/100)) if options is not None else None
                round_method = ceil

    if base_objective_type in (TYPE_ID_OBJECTIVE_AVAILABLE, TYPE_ID_OBJECTIVE,
                               TYPE_ID_OBJECTIVE_ENEMY,
                               TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE,
                               TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY, TYPE_ID_OBJECTIVE_FREQUENCY):
        if isEnemyObjectiveLocation(item_name):
            if options is not None and not options.enemy_objective_sanity:
                return base_objective_type, 0, floor, required_for_completion


    if base_objective_type == TYPE_ID_ENEMY:
        percentage = options.enemy_sanity_percentage if options is not None else None
        round_method = floor

    if base_objective_type == TYPE_ID_ENEMY_FREQUENCY:
        percentage = (100 / options.enemy_frequency) if options is not None else None
        round_method = floor

    if base_objective_type == TYPE_ID_OBJECTIVE_FREQUENCY:
        if isEnemyObjectiveLocation(item_name):
            base_objective_type = TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY
            percentage = (100 / options.enemy_objective_frequency) if options is not None else None
            round_method = floor
        else:
            percentage = (100 / options.objective_frequency)  if options is not None else None
            round_method = floor

    return base_objective_type, percentage, round_method,required_for_completion


def FrequencyPercentageToIncrementer(perc, round_method):
    if perc == 0:
        return None

    base = 100 / perc
    rounded = round_method(base)
    if rounded == 0:
        return 1

    return rounded

def getMaxRequired(type_default_percentage, total:int, stageId:int, alignmentId:int, override_settings):
    if type_default_percentage is None:
        #print("Type percentage is None: Return 100%")
        return total

    type_value = type_default_percentage[0]
    default_percentage = type_default_percentage[1]
    round_method = type_default_percentage[2]
    extra = type_default_percentage[3]

    override_total = getOverwriteRequiredCount(override_settings, stageId, alignmentId, type_value)
    #if override_total is not None and type_value in (TYPE_ID_OBJECTIVE_AVAILABLE, TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE):
    #    override_total = (override_total * default_percentage) / 100

    if type_value in [ TYPE_ID_OBJECTIVE_AVAILABLE, TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE]:
        if override_total is not None:
            override_total = extra * ((100 + override_total)/100)
        else:
            override_total = extra * ((100 + default_percentage)/100)

    #print("ot=", override_settings, override_total)
    max_required = getRequiredCount(total, default_percentage, override=override_total, round_method=round_method)

    if max_required == 0 and type_value in (TYPE_ID_COMPLETION, TYPE_ID_OBJECTIVE_ENEMY_COMPLETION):
        max_required = 1

    if type_value in [ TYPE_ID_ENEMY_FREQUENCY, TYPE_ID_OBJECTIVE_FREQUENCY, TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY]:
        return FrequencyPercentageToIncrementer(max_required, round_method)

    return max_required

def getPercRequired(type_default_percentage, stageId:int, alignmentId:int, override_settings):
    if type_default_percentage is None:
        return 100

    type_value = type_default_percentage[0]
    default_percentage = type_default_percentage[1]
    round_method = type_default_percentage[2]

    override_total = getOverwriteRequiredCount(override_settings, stageId, alignmentId, type_value)
    max_perc_required = getRequiredPercentage(default_percentage, override=override_total, round_method=round_method)

    return max_perc_required


class ShadowPlando:
    item_name: str

def GetPlandoItems(world):
    results = []
    if hasattr(world.options, "plando_items"):
       plando_items = world.options.plando_items
       relevant_plando_items = [ p.items for p in plando_items if p.from_pool and p.force]
       for item_list in relevant_plando_items:
           for item in item_list:
               results.append(item)
    else:
        plando_items = world.multiworld.plando_items[world.player]
        base_plando_items = [i["item"] for i in plando_items if i["from_pool"] and i["force"]]
        for item in base_plando_items:
            results.append(item)

    return results

TYPE_ID_ENEMY = 0
TYPE_ID_OBJECTIVE = 1
TYPE_ID_COMPLETION = 2
TYPE_ID_OBJECTIVE_AVAILABLE = 3
TYPE_ID_OBJECTIVE_ENEMY = 4
TYPE_ID_OBJECTIVE_ENEMY_COMPLETION = 5
TYPE_ID_OBJECTIVE_ENEMY_AVAILABLE = 6
TYPE_ID_OBJECTIVE_FREQUENCY = 7
TYPE_ID_OBJECTIVE_ENEMY_FREQUENCY = 8
TYPE_ID_ENEMY_FREQUENCY = 9

def GetObjectiveSanityFlag(details, level_info):
    if level_info is None:
        return False

    if level_info[0] == TYPE_ID_OBJECTIVE_ENEMY:
        return details.enemy_objective_sanity

    return details.objective_sanity