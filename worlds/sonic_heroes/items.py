from __future__ import annotations

from math import floor
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from worlds.sonic_heroes import SonicHeroesWorld

from BaseClasses import Item, ItemClassification
from .constants import *
from .options import *


class SonicHeroesItem(Item):
    game: str = SONICHEROES


def create_item(world: SonicHeroesWorld, name: str, classification: ItemClassification, amount: int = 1):
    for i in range(amount):
        world.multiworld.itempool.append(SonicHeroesItem(name, classification, world.item_name_to_id[name], world.player))

def create_filler_items(world: SonicHeroesWorld, amount: int):
    filler_list = world.random.choices(list(filler_items_to_weights.keys()), weights=list(filler_items_to_weights.values()), k=amount)

    for name in filler_list:
        create_item(world, name, ItemClassification.filler)

def create_trap_items(world: SonicHeroesWorld, amount: int):
    trap_list = world.random.choices(list(trap_items_to_weights.keys()), weights=list(trap_items_to_weights.values()), k=amount)

    for name in trap_list:
        create_item(world, name, ItemClassification.trap)


def create_items(world: SonicHeroesWorld):
    total_location_count = len(world.multiworld.get_unfilled_locations(world.player))

    trap_items_to_weights[STEALTHTRAP] = world.options.stealth_trap_weight.value
    trap_items_to_weights[FREEZETRAP] = world.options.freeze_trap_weight.value
    trap_items_to_weights[NOSWAPTRAP] = world.options.no_swap_trap_weight.value
    trap_items_to_weights[RINGTRAP] = world.options.ring_trap_weight.value
    trap_items_to_weights[CHARMYTRAP] = world.options.charmy_trap_weight.value



    #create_item(world, EMBLEM, ItemClassification.progression)
    #total_location_count -= 1

    if EMERALDS in world.options.goal_unlock_conditions:
        create_item(world, GREENCHAOSEMERALD, ItemClassification.progression)
        create_item(world, BLUECHAOSEMERALD, ItemClassification.progression)
        create_item(world, YELLOWCHAOSEMERALD, ItemClassification.progression)
        create_item(world, WHITECHAOSEMERALD, ItemClassification.progression)
        create_item(world, CYANCHAOSEMERALD, ItemClassification.progression)
        create_item(world, PURPLECHAOSEMERALD, ItemClassification.progression)
        create_item(world, REDCHAOSEMERALD, ItemClassification.progression)
        total_location_count -= 7


    if world.options.unlock_type == UnlockType.option_legacy_level_gates:
        total_location_count = create_legacy_gate_items(world, total_location_count)

    else:
        total_location_count = create_ability_character_items(world, total_location_count)



    world.extra_items = total_location_count

    #print(f"Extra Items count: {total_location_count}")

    trap_count = round(total_location_count * world.options.trap_fill.value / 100)
    junk_count = total_location_count - trap_count

    #print(f"Junk count: {junk_count}")
    #print(f"Trap count: {trap_count}")

    create_filler_items(world, junk_count)
    create_trap_items(world, trap_count)



def create_legacy_gate_items(world: SonicHeroesWorld, loc_count: int) -> int:

    create_item(world, EMBLEM, ItemClassification.progression, world.emblems_to_create)
    loc_count -= world.emblems_to_create

    return loc_count


def create_ability_character_items(world: SonicHeroesWorld, loc_count: int) -> int:
    if world.options.sonic_story_starting_character != SonicStoryStartingCharacter.option_sonic:
        create_item(world, get_playable_char_item_name(CHARSONIC), ItemClassification.progression)
        loc_count -= 1

    if world.options.sonic_story_starting_character != SonicStoryStartingCharacter.option_knuckles:
        create_item(world, get_playable_char_item_name(CHARKNUCKLES), ItemClassification.progression)
        loc_count -= 1

    if world.options.sonic_story_starting_character != SonicStoryStartingCharacter.option_tails:
        create_item(world, get_playable_char_item_name(CHARTAILS), ItemClassification.progression)
        loc_count -= 1


    if world.options.ability_unlocks == AbilityUnlocks.option_all_regions_separate:
        for region in world.regular_regions:
            for team in world.enabled_teams:
                for ability in get_all_abilities_for_team(team):
                    create_item(world, get_ability_item_name_without_world(team, region, ability), ItemClassification.progression)
                    loc_count -= 1


    elif world.options.ability_unlocks == AbilityUnlocks.option_entire_story:
        for team in world.enabled_teams:
            for ability in get_all_abilities_for_team(team):
                create_item(world, get_ability_item_name_without_world(team, ALLREGIONS, ability), ItemClassification.progression)
                loc_count -= 1


    return loc_count

def change_filler_weights_for_legacy_level_gates(world: SonicHeroesWorld):
    for itemData in itemList:
        if itemData.name == RINGS5:
            itemData.fillerweight = 15
        if itemData.name == RINGS10:
            itemData.fillerweight = 10
        if itemData.name == RINGS20:
            itemData.fillerweight = 5
        if itemData.name == SPEEDLEVELUP or itemData.name == POWERLEVELUP or itemData.name == FLYINGLEVELUP:
            itemData.fillerweight = 25
        if itemData.name == TEAMLEVELUP:
            itemData.fillerweight = 15


itemList: list[ItemData] = \
[
    ItemData(0x93930000, EMBLEM, ItemClassification.progression),
    ItemData(0x93930001, GREENCHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930002, BLUECHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930003, YELLOWCHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930004, WHITECHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930005, CYANCHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930006, PURPLECHAOSEMERALD, ItemClassification.progression),
    ItemData(0x93930007, REDCHAOSEMERALD, ItemClassification.progression),

    ItemData(0x93930008, get_playable_char_item_name(CHARSONIC), ItemClassification.progression),
    ItemData(0x93930009, get_playable_char_item_name(CHARKNUCKLES), ItemClassification.progression),
    ItemData(0x9393000A, get_playable_char_item_name(CHARTAILS), ItemClassification.progression),
    ItemData(0x9393000B, get_playable_char_item_name(CHARSHADOW), ItemClassification.progression),
    ItemData(0x9393000C, get_playable_char_item_name(CHAROMEGA), ItemClassification.progression),
    ItemData(0x9393000D, get_playable_char_item_name(CHARROUGE), ItemClassification.progression),
    ItemData(0x9393000E, get_playable_char_item_name(CHARAMY), ItemClassification.progression),
    ItemData(0x9393000F, get_playable_char_item_name(CHARBIG), ItemClassification.progression),
    ItemData(0x93930010, get_playable_char_item_name(CHARCREAM), ItemClassification.progression),
    ItemData(0x93930011, get_playable_char_item_name(CHARESPIO), ItemClassification.progression),
    ItemData(0x93930012, get_playable_char_item_name(CHARVECTOR), ItemClassification.progression),
    ItemData(0x93930013, get_playable_char_item_name(CHARCHARMY), ItemClassification.progression),
    ItemData(0x93930014, get_playable_char_item_name(CHARSUPERHARDSONIC), ItemClassification.progression),
    ItemData(0x93930015, get_playable_char_item_name(CHARSUPERHARDTAILS), ItemClassification.progression),
    ItemData(0x93930016, get_playable_char_item_name(CHARSUPERHARDKNUCKLES), ItemClassification.progression),


    #ItemData(0x93930200, get_ability_item_name_without_world(ANYTEAM, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930400, get_ability_item_name_without_world(SONIC, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930600, get_ability_item_name_without_world(DARK, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930800, get_ability_item_name_without_world(ROSE, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930A00, get_ability_item_name_without_world(CHAOTIX, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),


    #ItemData(0x93930C00, get_ability_item_name_without_world(SUPERHARD, ALLREGIONS, HOMINGATTACK), ItemClassification.progression),

    #to 0xE00


    #StageOBJS
    #start at 0x1000
    #go to 0x1C00-ish


    #ItemData(0x93931000, get_stage_obj_item_name_without_world(ANYTEAM, ALLREGIONS, ALLSTAGEOBJS), ItemClassification.progression),




    #ItemData(0x93930F00, char_levelup_to_item_name[SONIC][SPEED], ItemClassification.progression),
    #ItemData(0x93930F01, char_levelup_to_item_name[SONIC][FLYING], ItemClassification.progression),
    #ItemData(0x93930F02, char_levelup_to_item_name[SONIC][POWER], ItemClassification.progression),


    ItemData(0x93938000, EXTRALIFE, ItemClassification.filler),
    ItemData(0x93938001, RINGS5, ItemClassification.filler),
    ItemData(0x93938002, RINGS10, ItemClassification.filler),
    ItemData(0x93938003, RINGS20, ItemClassification.filler),
    ItemData(0x93938004, SHIELD, ItemClassification.filler),
    ItemData(0x93938005, INVINCIBILITY, ItemClassification.filler, fillerweight=0),
    ItemData(0x93938006, SPEEDLEVELUP, ItemClassification.filler, fillerweight=0),
    ItemData(0x93938007, POWERLEVELUP, ItemClassification.filler, fillerweight=0),
    ItemData(0x93938008, FLYINGLEVELUP, ItemClassification.filler, fillerweight=0),
    ItemData(0x93938009, TEAMLEVELUP, ItemClassification.filler, fillerweight=0),
    ItemData(0x9393800A, TEAMBLASTREFILL, ItemClassification.filler),
    ItemData(0x93938100, STEALTHTRAP, ItemClassification.trap),
    ItemData(0x93938101, FREEZETRAP, ItemClassification.trap),
    ItemData(0x93938102, NOSWAPTRAP, ItemClassification.trap),
    ItemData(0x93938103, RINGTRAP, ItemClassification.trap),
    ItemData(0x93938104, CHARMYTRAP, ItemClassification.trap),
]


filler_items_to_weights = \
    {item.name: item.fillerweight for item in itemList if item.classification == ItemClassification.filler}

trap_items_to_weights = \
    {item.name: item.fillerweight for item in itemList if item.classification == ItemClassification.trap}


item_groups: dict[str, set[str]] = \
{
    #FILLER: {item.name for item in itemList if item.classification == ItemClassification.filler},
    FILLER: {x for x in filler_items_to_weights.keys()},
    #TRAP: {item.name for item in itemList if item.classification == ItemClassification.trap},
    TRAP: {x for x in trap_items_to_weights.keys()},
    EMERALD: set(emeralds),
    CHARACTER: {get_playable_char_item_name(x) for y in team_char_names.keys() for x in
                team_char_names[y]},
    ABILITY: set(),
    STAGEOBJECT: set(),
}
"""
This is for item groups
"""





item_id = 0x939301F0

for item_team in item_teams:
    hex_mod = item_id % 512
    item_id += (512 - hex_mod)

    for item_region in item_regions:
        for item_ability in item_abilities:
            #team_name = [k for k, v in locals().items() if v == team][0]
            #region_name = [k for k, v in locals().items() if v == region][0]
            #ability_name = [k for k, v in locals().items() if v == ability][0]
            #data.append(
            #    {
            #        "Entry": f"ItemData({hex(item_id).upper().replace("X", "x")}, get_ability_item_name_without_world({team_name}, {region_name}, {ability_name}), ItemClassification.progression),"
            #    })

            itemList.append(ItemData(item_id, get_ability_item_name_without_world(item_team, item_region, item_ability), ItemClassification.progression))
            item_groups[ABILITY].add(get_ability_item_name_without_world(item_team, item_region, item_ability))
            item_id += 1

        hex_mod = item_id % 16
        item_id += (16 - hex_mod)


""""""
item_id = 0x93930FFF

for item_team in item_teams:
    hex_mod = item_id % 4096
    item_id += (4096 - hex_mod)

    for item_region in item_regions:
        for stage_obj in stage_objs:
            #team_name = [k for k, v in locals().items() if v == team][0]
            #region_name = [k for k, v in locals().items() if v == region][0]
            #ability_name = [k for k, v in locals().items() if v == ability][0]
            #data.append(
            #    {
            #        "Entry": f"ItemData({hex(item_id).upper().replace("X", "x")}, get_ability_item_name_without_world({team_name}, {region_name}, {ability_name}), ItemClassification.progression),"
            #    })

            itemList.append(ItemData(item_id, get_stage_obj_item_name_without_world(item_team, item_region, stage_obj), ItemClassification.progression))
            item_groups[STAGEOBJECT].add(get_stage_obj_item_name_without_world(item_team, item_region, stage_obj))
            item_id += 1

        hex_mod = item_id % 256
        item_id += (256 - hex_mod)
""""""
