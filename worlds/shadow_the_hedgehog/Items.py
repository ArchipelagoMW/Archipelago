#from __future__ import annotations
import copy
import logging
import typing
from dataclasses import dataclass
from math import floor, ceil
from typing import List, Optional

from BaseClasses import Item, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World
from . import Weapons, Vehicle, Utils as ShadowUtils, Options, Levels, Objects, ObjectTypes
from .Levels import LEVEL_ID_TO_LEVEL, ALL_STAGES, MISSION_ALIGNMENT_DARK, \
    MISSION_ALIGNMENT_HERO, MISSION_ALIGNMENT_NEUTRAL, ITEM_TOKEN_TYPE_STANDARD, ITEM_TOKEN_TYPE_FINAL, \
    ITEM_TOKEN_TYPE_OBJECTIVE, ITEM_TOKEN_TYPE_ALIGNMENT, ITEM_TOKEN_TYPE_BOSS, \
    ITEM_TOKEN_TYPE_FINAL_BOSS
from .Locations import MissionClearLocations, GetAlignmentsForStage, count_locations, count_last_way_locations

BASE_ID = 1743800000
ITEM_ID_START_AT_WEAPONS = 2000
ITEM_ID_START_AT_VEHICLES = 2500
ITEM_ID_START_AT_RIFLE = 2600
ITEM_ID_START_AT_OBJECTS = 2700
ITEM_ID_START_AT_JUNK = 3000
ITEM_ID_START_AT_MISSION = 1000
ITEM_ID_START_AT_IMPORTANT = 10
ITEM_ID_START_AT_LEVEL = 100
ITEM_ID_START_AT_WARP = 150
ITEM_ID_START_AT_KEY = 200
ID_START_AT_OTHER = 0
ITEM_ID_START_AT_TOKEN = 5000


@dataclass
class ItemInfo:
    itemId: int
    name: str
    classification: ItemClassification
    stageId: Optional[int]
    alignmentId: Optional[int]
    type: str
    value: Optional[int]


class Progression:
    GoodbyeForever = "Goodbye Forever"
    WhiteEmerald = "White Chaos Emerald"
    RedEmerald = "Red Chaos Emerald"
    CyanEmerald = "Cyan Chaos Emerald"
    PurpleEmerald = "Purple Chaos Emerald"
    GreenEmerald = "Green Chaos Emerald"
    YellowEmerald = "Yellow Chaos Emerald"
    BlueEmerald = "Blue Chaos Emerald"

    StandardHeroToken = "Hero Token"
    StandardDarkToken = "Dark Token"
    StandardMissionToken = "Mission Token"
    FinalToken = "Final Token"
    ObjectiveToken = "Objective Token"
    BossToken = "Boss Token"
    FinalBossToken = "Final Boss Token"

    #FinalHeroToken = "Final Hero Token"
    #FinalDarkToken = "Final Dark Token"
    #ObjectiveDarkToken = "Objective Dark Token"
    #ObjectiveHeroToken = "Objective Hero Token"


class ShadowRifleComponents:
    ShadowRifleBarrel = "Shadow Rifle Barrel"
    ShadowRifleAction = "Shadow Rifle Action"
    ShadowRifleStock = "Shadow Rifle Stock"
    ShadowRifleReceiver = "Shadow Rifle Receiver"
    ShadowRifleMagazine = "Shadow Rifle Magazine"


TOKENS = [
    Progression.StandardHeroToken, Progression.StandardDarkToken, Progression.StandardMissionToken,
    #Progression.FinalHeroToken, Progression.ObjectiveDarkToken,
    #Progression.FinalDarkToken, Progression.ObjectiveHeroToken,
    Progression.FinalToken, Progression.ObjectiveToken, Progression.BossToken, Progression.FinalBossToken
]

class Junk:
    NothingJunk = "Nothing Junk"


#GaugeAmounts = [1, 1000, 2000, 5000, 10000, 15000, 20000, 30000]
#RingAmounts = [1, 2, 5, 10, 20]

GaugeAmounts = \
    {
        100: 5,
        500: 10,
        1000: 20,
        2000: 20,
        5000: 10,
        10000: 10,
        15000: 5,
        20000: 2,
        30000: 1
    }

RingAmounts = \
    {
        5: 20,
        10: 15,
        20: 10
    }


def GetLevelTokenItems():
    id_iterator = ITEM_ID_START_AT_TOKEN
    level_token_items = []
    for token in TOKENS:
        alignment = MISSION_ALIGNMENT_NEUTRAL

        type = ITEM_TOKEN_TYPE_STANDARD
        if "Boss" in token:
            type = ITEM_TOKEN_TYPE_BOSS

        if "Final Boss" in token:
            type = ITEM_TOKEN_TYPE_FINAL_BOSS

        if "Final" in token and "Final Boss" not in token:
            type = ITEM_TOKEN_TYPE_FINAL
        if "Objective" in token:
            type = ITEM_TOKEN_TYPE_OBJECTIVE
        if "Dark" in token:
            type = ITEM_TOKEN_TYPE_ALIGNMENT
            alignment = MISSION_ALIGNMENT_DARK
        elif "Hero" in token:
            type = ITEM_TOKEN_TYPE_ALIGNMENT
            alignment = MISSION_ALIGNMENT_HERO

        i = ItemInfo(id_iterator, token, ItemClassification.progression_skip_balancing, None, alignment, "Token", type)
        id_iterator += 1
        level_token_items.append(i)

    return level_token_items


def PopulateLevelUnlockItems():
    level_unlock_items = []
    count = ITEM_ID_START_AT_LEVEL
    for stageId in ALL_STAGES:
        #if stageId in BOSS_STAGES or stageId in LAST_STORY_STAGES:
        #    continue

        if stageId in Levels.LAST_STORY_STAGES:
            continue

        item = ItemInfo(count, GetStageUnlockItem(stageId), ItemClassification.progression, stageId=stageId,
                        alignmentId=None, type="level_unlock", value=None)
        count += 1
        level_unlock_items.append(item)

    return level_unlock_items


def PopulateKeyItems():
    key_items = []
    count = ITEM_ID_START_AT_KEY
    for stage in Levels.ALL_STAGES:
        if stage in Levels.BOSS_STAGES:
            continue

        item = ItemInfo(count, GetStageKeyItem(stage), ItemClassification.progression,
                        stageId=stage,
                        alignmentId=None, type="key", value=None)
        count += 1
        key_items.append(item)

    key_items.append(ItemInfo(count, "Gate Key", ItemClassification.progression,
                        stageId=None,
                        alignmentId=None, type="gatekey", value=None))

    return key_items



# Upon entering a level, provide the player with a key
def PopulateLevelWarpPoints():
    level_warp_points = []
    count = ITEM_ID_START_AT_WARP
    for stageId in ALL_STAGES:
        item = ItemInfo(count, GetStageWarpItem(stageId), ItemClassification.progression_skip_balancing,
                        stageId=stageId,
                        alignmentId=None, type="level_warp", value=None)
        count += 1
        level_warp_points.append(item)

    return level_warp_points


def PopulateLevelObjectItems():
    level_object_items = []
    count = ITEM_ID_START_AT_MISSION
    for stageId in ALL_STAGES:
        alignment_ids = GetAlignmentsForStage(stageId)
        for alignment in alignment_ids:
            alignment_object = GetStageAlignmentObject(stageId, alignment)
            if alignment_object is None:
                continue
            item = ItemInfo(count, alignment_object, ItemClassification.progression,
                            stageId=stageId, alignmentId=alignment, type="level_object", value=None)
            count += 1
            level_object_items.append(item)

    return level_object_items


def GetStageAlignmentObject(stageId, alignmentId):
    i = [m for m in MissionClearLocations if m.stageId == stageId and m.alignmentId == alignmentId]
    if len(i) == 0:
        return None

    item = i[0]
    if item.mission_object_name is None:
        return None

    return LEVEL_ID_TO_LEVEL[stageId] + " " + item.mission_object_name


def GetStageUnlockItem(stageId):
    return "Stage:" + LEVEL_ID_TO_LEVEL[stageId]


def GetStageWarpItem(stageId):
    return "Warp:" + LEVEL_ID_TO_LEVEL[stageId]

def GetStageKeyItem(stageId):
    return LEVEL_ID_TO_LEVEL[stageId] + " Key"


class ShadowTheHedgehogItem(Item):
    game: str = "Shadow The Hedgehog"

    def __init__(self, item: ItemInfo, player):
        #item = item_name_to_info[name]
        super().__init__(item.name, item.classification, item.itemId + BASE_ID, player)


def GetFinalItem():
    info = ItemInfo(ITEM_ID_START_AT_IMPORTANT, Progression.GoodbyeForever,
                    ItemClassification.progression, None, None, type="final", value=None)
    return info


def GetEmeraldItems():
    emeralds: List[ItemInfo] = [
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 1, Progression.WhiteEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 2, Progression.CyanEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 3, Progression.RedEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 4, Progression.GreenEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 5, Progression.BlueEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 6, Progression.PurpleEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None),
        ItemInfo(ITEM_ID_START_AT_IMPORTANT + 7, Progression.YellowEmerald, ItemClassification.progression,
                 None, None, type="emerald", value=None)
    ]

    return emeralds


def GetItemDict():
    all_items = GetAllItemInfo()

    result = {}
    for item_type in all_items:
        for item in item_type:
            result[item.name] = item.itemId + BASE_ID

    return result


def GetItemLookupDict():
    all_items = GetAllItemInfo()

    result = {}
    for item_type in all_items:
        for item in item_type:
            result[item.itemId + BASE_ID] = item

    return result


def GetItemByName(name):
    d = GetItemLookupDict()
    name_map = {v.name: v for k, v in d.items()}
    return name_map[name]


def GetGaugeItems():
    id_s = ITEM_ID_START_AT_JUNK + 1
    infos = []
    alignments = ["Hero", "Dark"]
    for alignment in alignments:
        for gauge in GaugeAmounts.keys():
            infos.append(ItemInfo(id_s, "Gauge:" + alignment + "-" + str(gauge), ItemClassification.filler,
                                  None, MISSION_ALIGNMENT_DARK if alignment == "Dark"
                                  else MISSION_ALIGNMENT_HERO, "gauge", gauge))
            id_s += 1

    return infos


def GetRingItems():
    id_s = ITEM_ID_START_AT_JUNK + 50
    infos = []
    for ring in RingAmounts.keys():
        infos.append(ItemInfo(id_s, str(ring) + " Ring" + ("" if ring == 1 else "s"), ItemClassification.filler,
                              None, None, "rings", ring))
        id_s += 1

    return infos

def GetAmmoBoostItems():
    id_s = ITEM_ID_START_AT_JUNK + 75
    info = []
    for weapon in Weapons.WEAPON_INFO:
        info.append(ItemInfo(id_s, weapon.name + " Ammo Boost",  ItemClassification.filler,
                              None, None, "ammoboost", weapon.game_id))
        id_s += 1

    return info


def GetTraps():
    id_t = ITEM_ID_START_AT_JUNK + 70

    infos = []
    infos.append(ItemInfo(id_t, "Ammo Trap", ItemClassification.trap,
                          None, None, "ammotrap", None))
    id_t+=1

    infos.append(ItemInfo(id_t, "Poison Trap", ItemClassification.trap,
                          None, None, "poisontrap", None))
    id_t+=1

    infos.append(ItemInfo(id_t, "Checkpoint Trap", ItemClassification.trap,
                          None, None, "checkpointtrap", None))
    id_t+=1

    return infos


# The order here matters
def GetSpecialWeapons():
    id_s = ITEM_ID_START_AT_WEAPONS
    weapons = []

    weapons.append(
        ItemInfo(id_s + 3, "Samurai Blade", ItemClassification.progression,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 2, "Satellite Gun", ItemClassification.progression,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 1, "Egg Vacuum", ItemClassification.progression,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 4, "Omochao Gun", ItemClassification.progression,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 5, "Heal Cannon", ItemClassification.progression,
                 None, None, "SpecialWeapon", None)
    )

    weapons.append(
        ItemInfo(id_s + 6, "Shadow Rifle", ItemClassification.progression,
                 None, None, "SpecialWeapon", None)
    )

    return weapons


def GetWeapons():
    id_s = ITEM_ID_START_AT_WEAPONS
    weapons = []
    for weapon in Weapons.WEAPON_INFO:
        weapons.append(
            ItemInfo(id_s + len(weapons), weapon.name, ItemClassification.progression,
                     None, None, "Weapon", weapon.game_id)
        )

    return weapons


def GetWeaponGroups():
    weapons_count = len(GetWeapons())
    id_s = ITEM_ID_START_AT_WEAPONS + weapons_count
    weapon_groups = []

    for weapon_group in Weapons.WeaponGroups.keys():
        weapon_groups.append(
            ItemInfo(id_s + len(weapon_groups), weapon_group, ItemClassification.progression,
                     None, None, "WeaponGroup", None)
        )

    return weapon_groups


def GetVehicles():
    id_s = ITEM_ID_START_AT_VEHICLES
    vehicles = []
    for vehicle in Vehicle.VEHICLE_INFO:
        vehicles.append(
            ItemInfo(id_s + len(vehicles), vehicle.name, ItemClassification.progression,
                     None, None, "Vehicle", vehicle.game_id)
        )

    return vehicles


def GetRifleComponents():
    id_s = ITEM_ID_START_AT_RIFLE
    rifle_components = []
    for rifle_name in ShadowRifleComponents.__dict__.keys():
        if "ShadowRifle" in rifle_name:
            rifle_components.append(ItemInfo(id_s + len(rifle_components), ShadowRifleComponents.__dict__[rifle_name],
                                             ItemClassification.progression,
                                             None, None, "Rifle Component", None)
                                    )

    return rifle_components


def GetJunkItemInfo():
    junk_items = []

    nothing = ItemInfo(ITEM_ID_START_AT_JUNK, Junk.NothingJunk, ItemClassification.filler, None, None, "Junk", None)
    junk_items.append(nothing)

    gauge_items = GetGaugeItems()
    junk_items.extend(gauge_items)

    ring_items = GetRingItems()
    junk_items.extend(ring_items)

    ammo_boost_items = GetAmmoBoostItems()
    junk_items.extend(ammo_boost_items)

    return junk_items


def GetAllItemInfo():
    level_unlocks_item_table: List[ItemInfo] = PopulateLevelUnlockItems()
    level_warp_item_table = PopulateLevelWarpPoints()

    key_items = PopulateKeyItems()

    stage_progression_item_table: List[ItemInfo] = PopulateLevelObjectItems()

    emerald_items = GetEmeraldItems()
    required_items = [GetFinalItem()]

    level_unlock_items = []
    for unlock in level_unlocks_item_table:
        level_unlock_items.append(unlock)

    level_warp_items = []
    for warp in level_warp_item_table:
        level_warp_items.append(warp)

    stage_objective_items = stage_progression_item_table
    junk_items = GetJunkItemInfo()
    trap_items = GetTraps()
    token_items = GetLevelTokenItems()
    weapon_items = GetWeapons()
    weapon_group_items = GetWeaponGroups()
    vehicle_items = GetVehicles()

    rifle_components = GetRifleComponents()
    object_items = GetObjectItems()

    return (emerald_items, required_items, level_unlock_items, stage_objective_items, junk_items,
            token_items, weapon_items, vehicle_items, level_warp_items, rifle_components,
            weapon_group_items, object_items, key_items, trap_items)




useful_to_count = {
    "Egg Vacuum": 2,
    "Satellite Gun": 2,
    "Samurai Blade": 2,
    "Omochao Gun": 2,
    "Heal Cannon": 2,
    "Shadow Rifle": 1
}

def GetTrapDensity(option):
    if option == Options.AmmoTraps.option_low:
        return 1
    if option == Options.AmmoTraps.option_medium:
        return 2
    if option == Options.AmmoTraps.option_high:
        return 4

    return 0

def ChooseJunkItems(random, junk, traps, options, junk_count, available_weapons):
    junk_distribution = {}
    trap_distribution = {}
    junk_items = []
    trap_items = []

    total = 0
    trap_total = 0

    trap_percentage = options.trap_fill_percentage
    trap_count = 0

    if options.enable_traps:
        trap_count = int(junk_count / 100 * trap_percentage)
        filler_count = int(junk_count - trap_count)

        if options.poison_trap_enabled != Options.PoisonTraps.option_off:
            poison_item = \
                [j for j in traps if j.type == "poisontrap"][0]
            trap_items.append(poison_item)
            trap_distribution[trap_total] = GetTrapDensity(options.poison_trap_enabled)
            trap_total += 1

        if options.ammo_trap_enabled:
            ammo_item = \
                [j for j in traps if j.type == "ammotrap"][0]
            trap_items.append(ammo_item)
            trap_distribution[trap_total] = GetTrapDensity(options.ammo_trap_enabled)
            trap_total += 1

        if options.checkpoint_trap_enabled:
            trap_item = \
                [j for j in traps if j.type == "checkpointtrap"][0]
            trap_items.append(trap_item)
            trap_distribution[trap_total] = GetTrapDensity(options.checkpoint_trap_enabled)
            trap_total += 1

    else:
        filler_count = junk_count

    if options.enable_gauge_items:
        for g, c in GaugeAmounts.items():
            g_item_dark = \
            [j for j in junk if j.type == "gauge" and j.value == g and j.alignmentId == MISSION_ALIGNMENT_DARK][0]
            g_item_hero = \
            [j for j in junk if j.type == "gauge" and j.value == g and j.alignmentId == MISSION_ALIGNMENT_HERO][0]
            junk_items.append(g_item_dark)
            junk_items.append(g_item_hero)
            junk_distribution[total] = c
            junk_distribution[total + 1] = c
            total += 2

    if options.enable_ring_items:
        for r, c in RingAmounts.items():
            r_item = [j for j in junk if j.type == "rings" and j.value == r][0]
            junk_distribution[total] = c
            junk_items.append(r_item)
            total += 1

    if options.enable_ammo_boost_items:
        weapons = Weapons.WEAPON_INFO
        r_items = [j for j in junk if j.type == "ammoboost"]
        for r in r_items:
            weapon_info = [ w for w in weapons if w.game_id == r.value][0]
            if weapon_info.name not in available_weapons:
                continue
            weight = 0.5
            if weapon_info.power is None:
                weight = 2
            elif weapon_info.power > 15:
                weight = 0.1
            elif weapon_info.power == 2 and weapon_info.base_ammo == 4:
                weight = 0
            elif weapon_info.power < 2:
                weight = 4
            elif weapon_info.base_ammo < 10:
                weight = 3
            elif weapon_info.power < 8:
                weight = 1

            junk_distribution[total] = weight
            junk_items.append(r)
            total += 1

    NothingJunk = [j for j in junk if j.type == "Junk"][0]
    junk_items.append(NothingJunk)
    junk_distribution[total] = 1
    total += 1

    randomised_indicies = random.choices(list(junk_distribution.keys()), k=filler_count,
                                         weights=list(junk_distribution.values()))

    if trap_count > 0:
        randomised_traps = random.choices(list(trap_distribution.keys()), k=trap_count,
                                         weights=list(trap_distribution.values()))
        traps = [trap_items[k] for k in randomised_traps]
    else:
        traps = []

    junk =  [junk_items[k] for k in randomised_indicies]

    junk.extend(traps)
    return junk


def AddItemsToStartInventory(world, count):
    base_plando_items = []
    plando_items = ShadowUtils.GetPlandoItems(world)

    multiworld_itempool_self = [ i for i in world.multiworld.itempool if i.player == world.player ]

    valid_removals = [ i for i in multiworld_itempool_self if i.name not in base_plando_items
                       and i.classification == ItemClassification.progression and i.name not in plando_items]

    if len(valid_removals) < count:
        raise OptionError(f"Unable to remove {count} items from valid list of {len(valid_removals)}")

    startings = world.random.sample(valid_removals, k=count)
    for s in startings:
        world.multiworld.itempool.remove(s)
        logging.info(f"Add {s} to starting inventory")
        world.push_precollected(s)


def CountItems(world: World):
    (emerald_items, required_items, level_unlock_items, stage_objective_items_x,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items, object_items, key_items, trap_items) = GetAllItemInfo()

    if (not world.options.objective_sanity or
            world.options.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear):
        stage_objective_items_x = []

    if not world.options.rifle_components:
        rifle_components = []

    stage_objective_items_full = [s for s in stage_objective_items_x if s.stageId in world.available_levels]
    using_stage_objective_items = []

    for item in stage_objective_items_full:
        lookup = [x for x in MissionClearLocations
                  if x.stageId == item.stageId and x.alignmentId == item.alignmentId][0]

        location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                  lookup.mission_object_name,
                                                  world.options, lookup.stageId, lookup.alignmentId,
                                                  world.options.percent_overrides)

        result_sanity = ShadowUtils.GetObjectiveSanityFlag(world.options, location_details)
        if not result_sanity:
            continue

        max_available = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                      lookup.mission_object_name,
                                                      world.options, lookup.stageId, lookup.alignmentId,
                                                      world.options.percent_overrides),
            lookup.requirement_count, lookup.stageId, lookup.alignmentId, world.options.percent_overrides)

        items = [item] * max_available
        using_stage_objective_items.extend(items)

    use_level_unlock_items = [l for l in level_unlock_items if l.stageId not in world.first_regions and
                              l.stageId in world.available_levels
                              and l.stageId not in Levels.LAST_STORY_STAGES
                              and (l.stageId not in Levels.BOSS_STAGES or world.options.select_bosses)
                              and world.options.level_progression != Options.LevelProgression.option_story]

    select_stage_count = 0
    if len(use_level_unlock_items) > 0:
        unlock_items = [l for l in use_level_unlock_items if l.stageId in world.available_select_stages and
                        l.stageId not in world.first_regions]
        select_stage_count = len(unlock_items)

    item_count = increment_item_count(0, select_stage_count)
    item_count = increment_item_count(item_count, using_stage_objective_items)
    if world.options.goal_chaos_emeralds or world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_chaos_emeralds:
        item_count = increment_item_count(item_count, emerald_items)

    weapon_dict = Weapons.GetWeaponDict()
    special_weapon_extras = [w for w in weapon_items if
                             Weapons.WeaponAttributes.SPECIAL in weapon_dict[w.name].attributes and
                             w.name != 'Shadow Rifle' and w.name != 'Weapon:Shadow Rifle']


    weapon_items = [w for w in weapon_items if
                    w.name != "Weapon:Shadow Rifle" and
                    w.name != "Shadow Rifle"]

    weapon_items.extend(special_weapon_extras)

    available_weapons = [w for w in weapon_items if w.name in world.available_weapons]
    HandleAllWeaponsGroups(world.options, available_weapons, weapon_group_items)

    mw_weapon_items = [ShadowTheHedgehogItem(w, world.player) for w in available_weapons]

    mw_weapon_special_only = [ShadowTheHedgehogItem(w, world.player) for w in special_weapon_extras]
    mw_weapon_special_only_dupes = [ShadowTheHedgehogItem(w, world.player) for w in special_weapon_extras]
    mw_weapon_special_only.extend(mw_weapon_special_only_dupes)

    shadow_rifle = GetShadowRifle()
    if not world.options.rifle_components:
        mw_weapon_special_only.append(ShadowTheHedgehogItem(shadow_rifle, world.player))
        mw_weapon_items.append(ShadowTheHedgehogItem(shadow_rifle, world.player))
    else:
        mw_weapon_special_only.extend([ShadowTheHedgehogItem(w, world.player) for w in rifle_components])
        mw_weapon_items.extend([ShadowTheHedgehogItem(w, world.player) for w in rifle_components])

    if world.options.weapon_sanity_unlock:
        item_count = increment_item_count(item_count, mw_weapon_items)
    else:
        item_count = increment_item_count(item_count, mw_weapon_special_only)

    if world.options.vehicle_logic:
        available_vehicle_items = Objects.GetAvailableVehicles(world)
        item_count = increment_item_count(item_count, len(available_vehicle_items))

    if world.options.object_unlocks:
        available_objects = Objects.GetAvailableObjects(world)
        if world.options.object_pulleys and ObjectTypes.ObjectType.STANDARD_PULLEY in available_objects:
            item_count = increment_item_count(item_count, 1)
        if world.options.object_ziplines and (ObjectTypes.ObjectType.GUN_ZIPWIRE in available_objects
            or ObjectTypes.ObjectType.SPACE_ZIPWIRE in available_objects or ObjectTypes.ObjectType.GUN_ZIPWIRE in available_objects or
            ObjectTypes.ObjectType.BALLOON_ZIPWIRE in available_objects):
            item_count = increment_item_count(item_count, 1)
        if world.options.object_units:
            if ObjectTypes.ObjectType.BOMB in available_objects or ObjectTypes.ObjectType.BOMB_SERVER in available_objects:
                item_count = increment_item_count(item_count, 1)
            if ObjectTypes.ObjectType.HEAL_UNIT in available_objects or ObjectTypes.ObjectType.HEAL_SERVER in available_objects:
                item_count = increment_item_count(item_count, 1)
        if world.options.object_rockets and ObjectTypes.ObjectType.ROCKET in available_objects:
            item_count = increment_item_count(item_count, 1)
        if world.options.object_light_dashes and ObjectTypes.ObjectType.LIGHT_DASH_TRAIL in available_objects:
            item_count = increment_item_count(item_count, 1)
        if world.options.object_warp_holes and ObjectTypes.ObjectType.WARP_HOLE in available_objects:
            item_count = increment_item_count(item_count, 1)

    return item_count


def GetStageItems(world, stage_objective_items=None):
    override_settings = world.options.percent_overrides
    mw_temp_stage_objective_items = []

    world.objective_requirements = {}

    if stage_objective_items is None:
        (emerald_items, required_items, level_unlock_items, stage_objective_items,
         junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
         weapon_group_items, object_items, key_items, trap_items) = GetAllItemInfo()

    if (not world.options.objective_sanity or
            world.options.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_base_clear):
        return []

    for item in stage_objective_items:
        if item.stageId not in world.available_levels:
            continue

        lookup = [x for x in MissionClearLocations
                  if x.stageId == item.stageId and x.alignmentId == item.alignmentId][0]

        location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                     lookup.mission_object_name,
                                                                     world.options, lookup.stageId, lookup.alignmentId,
                                                                     world.options.percent_overrides)

        result_sanity = ShadowUtils.GetObjectiveSanityFlag(world.options, location_details)
        if not result_sanity:
            continue

        relevant_objective_complete = ShadowUtils.getMaxRequired(ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                  lookup.mission_object_name, world.options,
                                                                       item.stageId, item.alignmentId,
                                                                       world.options.percent_overrides), lookup.requirement_count, item.stageId, item.alignmentId,
            override_settings)

        world.objective_requirements[item.name] = relevant_objective_complete


        relevant_objective = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                  lookup.mission_object_name, world.options,
                                                                       item.stageId, item.alignmentId,
                                                                       world.options.percent_overrides)

        # None if returned if relevant objective is disabled (e.g. objective/enemy sanity off)
        if relevant_objective is None:
            continue

        required_available = ShadowUtils.getMaxRequired(
            relevant_objective,
            lookup.requirement_count, item.stageId, item.alignmentId,
            override_settings)

        assert relevant_objective_complete <=  required_available

        mw_temp_stage_objective_items.extend([item] * required_available)

    mw_stage_items = [ShadowTheHedgehogItem(s, world.player) for s in mw_temp_stage_objective_items]
    return mw_stage_items


def GetPotentialDowngradeItems(world, mw_stage_items=None):
    potential_downgrade = []
    to_remove = []

    if mw_stage_items is None:
        mw_stage_items = GetStageItems(world)

    override_settings = world.options.percent_overrides
    itemdict = GetItemLookupDict()

    indexer = {}
    for item in mw_stage_items:
        item_lookup = itemdict[item.code]
        lookup = [x for x in MissionClearLocations
                  if x.stageId == item_lookup.stageId and x.alignmentId == item_lookup.alignmentId][0]
        if item_lookup.name not in indexer:
            indexer[item_lookup.name] = 0

        indexer[item_lookup.name] += 1

        max_required_complete = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION, lookup.mission_object_name,
                                                      world.options, lookup.stageId, lookup.alignmentId,world.options.percent_overrides),
            lookup.requirement_count, lookup.stageId, lookup.alignmentId,
            override_settings)

        max_available = ShadowUtils.getMaxRequired(
            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_AVAILABLE,
                                                      lookup.mission_object_name,
                                                      world.options, lookup.stageId, lookup.alignmentId,
                                                      world.options.percent_overrides),
            lookup.requirement_count, lookup.stageId, lookup.alignmentId,
            override_settings)

        if indexer[item_lookup.name] > max_available:
            to_remove.append(item)
        elif indexer[item_lookup.name] > max_required_complete:
            potential_downgrade.append(item)


    return potential_downgrade, to_remove


def GetShadowRifle():
    (emerald_items, required_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items, object_items, key_items, trap_items) = GetAllItemInfo()

    return [w for w in weapon_items if w.name == 'Shadow Rifle' or w.name == 'Weapon:Shadow Rifle'][0]

def HandleWeaponDuplicates(world, available_weapons):
    new_weapons = []

    weapon_min = world.options.weapon_sanity_min_available
    weapon_max = world.options.weapon_sanity_max_available

    weapon_dict = Weapons.GetWeaponDict()
    for w in available_weapons:
        if w.name in weapon_dict and Weapons.WeaponAttributes.SPECIAL in weapon_dict[w.name].attributes:
            new_weapons.extend([w]*1)
        elif weapon_min == weapon_max:
            new_weapons.extend([w]*weapon_min)
        else:
            weapon_maximum = weapon_max if weapon_max > weapon_min else weapon_min
            weapon_minimum = weapon_max if weapon_max < weapon_min else weapon_min
            r = world.random.randrange(weapon_minimum, weapon_maximum)
            new_weapons.extend([w]*r)

    return new_weapons


def HandleAllWeaponsGroups(options, items, group_items):
    if not options.weapon_sanity_unlock:
        return

    weapons_to_remove = []
    for group in Weapons.WeaponGroups.keys():
        if group in options.weapon_groups:
            HandleWeaponGroup(items, group_items, group, weapons_to_remove)

    for weapon in weapons_to_remove:
        if weapon in items:
            items.remove(weapon)


def HandleWeaponGroup(items, group_items, weapon_group_name, weapons_to_remove):
    melee_group = Weapons.WeaponGroups[weapon_group_name]
    weapon_items_to_remove = [w for w in items if w.value in melee_group]

    if len(weapon_items_to_remove) == 0:
        # If no items in the group are available, don't add the group
        return

    weapons_to_remove.extend(weapon_items_to_remove)
    group_item = [w for w in group_items if w.name == weapon_group_name]
    items.extend(group_item)


def increment_item_count(count, items):
    plus = 0
    printString = ""
    if type(items) is list:
        plus += len(items)
        printString = [x.name for x in items]
    if type(items) is int:
        plus += items
        printString = str(plus)

    return count + plus


def GetObjectItems():
    id_s = ITEM_ID_START_AT_OBJECTS
    object_items = [

        ItemInfo(id_s,     "Pulley",    ItemClassification.progression, None, None, "Object", None),
        ItemInfo(id_s + 1, "Air Shoes", ItemClassification.progression, None, None, "Object", None),
        ItemInfo(id_s + 2, "Rocket",    ItemClassification.progression, None, None, "Object", None),
        ItemInfo(id_s + 3, "Zipwire",   ItemClassification.progression, None, None, "Object", None),
        ItemInfo(id_s + 4, "Heal Units", ItemClassification.progression, None, None, "Object", None),
        ItemInfo(id_s + 5, "Bombs",     ItemClassification.progression, None, None, "Object", None),
        ItemInfo(id_s + 6, "Warp Holes", ItemClassification.progression, None, None, "Object", None)

    ]

    return object_items


def PopulateItemPool(world: World):
    (emerald_items, required_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items, object_items, key_items, trap_items) = GetAllItemInfo()

    use_level_unlock_items = []
    if world.options.level_progression != Options.LevelProgression.option_story and \
        world.options.select_gates == Options.SelectGates.option_off:
            use_level_unlock_items = [l for l in level_unlock_items if l.stageId not in world.first_regions and
                                      l.stageId in world.available_levels
                                      # and (l.stageId not in Levels.FINAL_BOSSES
                                      and l.stageId not in Levels.LAST_STORY_STAGES
                                      and (l.stageId not in Levels.BOSS_STAGES or world.options.select_bosses)
                                      ]

    # Convert to multiworld items
    mw_em_items = [ShadowTheHedgehogItem(e, world.player) for e in emerald_items]

    unlock_items = [l for l in use_level_unlock_items if l.stageId in world.available_select_stages and
                    l.stageId not in world.first_regions]
    level_unlock_item_selections = [ l for l in unlock_items ]

    mw_level_unlock_items = [ShadowTheHedgehogItem(l, world.player) for l in level_unlock_item_selections]

    mw_stage_items = GetStageItems(world, stage_objective_items)

    potential_downgrade, to_remove = GetPotentialDowngradeItems(world, mw_stage_items)
    if world.excess_item_count > 0 and len(potential_downgrade) > 0:
        t_size = len(to_remove)
        size = world.excess_item_count - t_size
        size = min(size, len(potential_downgrade))
        new_remove = world.random.sample(potential_downgrade, k=size)
        potential_downgrade = [ p for p in potential_downgrade if p not in new_remove]
        to_remove.extend(new_remove)

    if world.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_always:
        for downgrade in potential_downgrade:
            downgrade.classification = ItemClassification.useful

    elif world.options.exceeding_items_filler == Options.ExceedingItemsFiller.option_chance:
        chance = world.options.exceeding_items_filler_random
        sample = [item for item in potential_downgrade if world.random.randrange(0, 100) < chance]
        for downgrade in sample:
            downgrade.classification = ItemClassification.useful

    for remove in to_remove:
        logging.debug("Remove excess item: %s", remove)
        mw_stage_items.remove(remove)

    weapon_dict = Weapons.GetWeaponDict()
    special_weapons_weaponsanity_extras = [copy.copy(w) for w in weapon_items if
                             Weapons.WeaponAttributes.SPECIAL in weapon_dict[w.name].attributes and
                             w.name != 'Shadow Rifle' and w.name != 'Weapon:Shadow Rifle']

    weapon_items = [w for w in weapon_items if
                    w.name != "Weapon:Shadow Rifle" and
                    w.name != "Shadow Rifle"]

    weapon_items.extend(special_weapons_weaponsanity_extras)

    available_weapons = [w for w in weapon_items if w.name in world.available_weapons]
    for w in available_weapons:
        # If changed already, then ignore
        if w.classification == ItemClassification.progression:
            weapon_classification = Weapons.GetWeaponClassification(world, weapon_dict[w.name])
            if weapon_classification is not None:
                w.classification = weapon_classification

    HandleAllWeaponsGroups(world.options, available_weapons, weapon_group_items)
    available_weapons = HandleWeaponDuplicates(world, available_weapons)

    mw_weapon_items = [ShadowTheHedgehogItem(w, world.player) for w in available_weapons]

    mw_weapon_special_only = [ShadowTheHedgehogItem(w, world.player) for w in special_weapons_weaponsanity_extras]

    # Not sure how much this helps
    #for weapon in special_weapons_weaponsanity_extras:
    #    print("Change weapon to Useful", weapon.name)
    #    weapon.classification = ItemClassification.useful

    mw_weapon_special_only_dupes = [ShadowTheHedgehogItem(w, world.player) for w in special_weapons_weaponsanity_extras]
    mw_weapon_special_only.extend(mw_weapon_special_only_dupes)

    shadow_rifle = GetShadowRifle()
    if not world.options.rifle_components:
        mw_weapon_special_only.append(ShadowTheHedgehogItem(shadow_rifle, world.player))
        mw_weapon_items.append(ShadowTheHedgehogItem(shadow_rifle, world.player))
    else:
        mw_weapon_special_only.extend([ShadowTheHedgehogItem(w, world.player) for w in rifle_components])
        mw_weapon_items.extend([ShadowTheHedgehogItem(w, world.player) for w in rifle_components])

    available_vehicle_items = Objects.GetAvailableVehicles(world)
    mw_vehicle_items = [ShadowTheHedgehogItem(w, world.player) for w in vehicle_items if w.value in available_vehicle_items ]

    item_count = increment_item_count(0, mw_level_unlock_items)
    item_count = increment_item_count(item_count, mw_stage_items)
    if world.options.goal_chaos_emeralds or world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_chaos_emeralds:
        item_count = increment_item_count(item_count, mw_em_items)

    if world.options.weapon_sanity_unlock:
        item_count = increment_item_count(item_count, mw_weapon_items)
    else:
        item_count = increment_item_count(item_count, mw_weapon_special_only)

    if world.options.vehicle_logic:
        item_count = increment_item_count(item_count, mw_vehicle_items)

    mw_object_items = []
    available_objects = Objects.GetAvailableObjects(world)
    if world.options.object_unlocks:
        if world.options.object_pulleys and ObjectTypes.ObjectType.STANDARD_PULLEY in available_objects and "Pulley" not in world.starting_items:
            mw_object_items.append(ShadowTheHedgehogItem
                                   ([o for o in object_items if o.name == "Pulley"]
                                    [0], world.player))
            item_count = increment_item_count(item_count, 1)
        if world.options.object_ziplines and (ObjectTypes.ObjectType.GUN_ZIPWIRE in available_objects
            or ObjectTypes.ObjectType.SPACE_ZIPWIRE in available_objects or ObjectTypes.ObjectType.GUN_ZIPWIRE in available_objects or
            ObjectTypes.ObjectType.BALLOON_ZIPWIRE in available_objects or
            ObjectTypes.ObjectType.CIRCUS_ZIPWIRE in available_objects) and "Zipwire" not in world.starting_items:
            mw_object_items.append(ShadowTheHedgehogItem
                                   ([o for o in object_items if o.name == "Zipwire"]
                                    [0], world.player))
            item_count = increment_item_count(item_count, 1)
        if world.options.object_units:
            if ObjectTypes.ObjectType.BOMB in available_objects or ObjectTypes.ObjectType.BOMB_SERVER in available_objects\
                    and "Bombs" not in world.starting_items:
                mw_object_items.append(ShadowTheHedgehogItem
                                       ([o for o in object_items if o.name == "Bombs"]
                                        [0], world.player))
                item_count = increment_item_count(item_count, 1)
            if ObjectTypes.ObjectType.HEAL_UNIT in available_objects or ObjectTypes.ObjectType.HEAL_SERVER in available_objects\
                    and "Heal Units" not in world.starting_items:
                mw_object_items.append(ShadowTheHedgehogItem
                                   ([o for o in object_items if o.name == "Heal Units"]
                                    [0], world.player))
                item_count = increment_item_count(item_count, 1)

        if world.options.object_rockets and ObjectTypes.ObjectType.ROCKET in available_objects and "Rocket" not in world.starting_items:
            mw_object_items.append(ShadowTheHedgehogItem
                                   ([o for o in object_items if o.name == "Rocket"]
                                    [0], world.player))
            item_count = increment_item_count(item_count, 1)
        if world.options.object_light_dashes and ObjectTypes.ObjectType.LIGHT_DASH_TRAIL in available_objects \
                and "Air Shoes" not in world.starting_items:
            mw_object_items.append(ShadowTheHedgehogItem
                                   ([o for o in object_items if o.name == "Air Shoes"]
                                    [0], world.player))
            item_count = increment_item_count(item_count, 1)
        if world.options.object_warp_holes and ObjectTypes.ObjectType.WARP_HOLE in available_objects and "Warp Holes" not in world.starting_items:
            mw_object_items.append(ShadowTheHedgehogItem
                                   ([o for o in object_items if o.name == "Warp Holes"]
                                    [0], world.player))
            item_count = increment_item_count(item_count, 1)

    location_count = count_locations(world)

    mw_useful_items = []
    junk_but_useful = [j for j in junk_items if j.classification == ItemClassification.useful]
    for item in junk_but_useful:
        if item.name in useful_to_count:
            mw_useful_items.extend(
                [ShadowTheHedgehogItem(item, world.player) for _ in range(0, useful_to_count[item.name])])

    if world.options.goal_chaos_emeralds or world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_chaos_emeralds:
        world.multiworld.itempool += mw_em_items

    world.multiworld.itempool += mw_level_unlock_items
    world.multiworld.itempool += mw_stage_items
    world.multiworld.itempool += mw_useful_items

    if world.options.weapon_sanity_unlock:
        world.multiworld.itempool += mw_weapon_items
    else:
        world.multiworld.itempool += mw_weapon_special_only

    if world.options.vehicle_logic:
        world.multiworld.itempool += mw_vehicle_items

    if world.options.object_unlocks:
        world.multiworld.itempool += mw_object_items

    if world.options.key_collection_method in [Options.KeyCollectionMethod.option_arch, Options.KeyCollectionMethod.option_both]:
        choice_key_items = [ x for x in key_items if x.stageId is not None and x.stageId in world.available_levels]
        choice_key_items *= world.options.keys_required_for_doors
        mw_key_items = [ShadowTheHedgehogItem(i, world.player) for i in choice_key_items]
        world.multiworld.itempool += mw_key_items

        item_count = increment_item_count(item_count, mw_key_items)

    if world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_items:
        gate_key_item = [ l for l in key_items if l.type == 'gatekey'][0]
        gate_count = world.options.select_gates_count
        mw_prep_items = [ gate_key_item ] * gate_count
        mw_gate_keys = [ ShadowTheHedgehogItem(i, world.player) for i in mw_prep_items ]
        item_count = increment_item_count(item_count, mw_gate_keys)
        world.multiworld.itempool += mw_gate_keys

    # Add checks here for checks locked by The Last Way when this is the final part
    # If required, replace all TLW checks with junk items in the pool, start inventory will get amended

    junk_count = (location_count - item_count - len(mw_useful_items))
    #print("Junk count is", location_count, junk_count)
    reverse_count = 0

    if junk_count < 0:
        reverse_count = -junk_count
        junk_count = 0

    if not world.options.include_last_way_shuffle:
        if not world.options.exclude_go_mode_items:
            tlw_locations = count_last_way_locations(world)
        else:
            tlw_locations = 1
        if junk_count < tlw_locations:
            reverse_count += tlw_locations
            junk_count += tlw_locations

    if junk_count > 0:
        mw_junk_items = [ShadowTheHedgehogItem(i, world.player) for i in
                         ChooseJunkItems(world.random, junk_items, trap_items, world.options, junk_count, world.available_weapons)]
        world.multiworld.itempool += mw_junk_items

    if reverse_count > 0:
        AddItemsToStartInventory(world, reverse_count)

def get_item_groups():
    (emerald_items, required_items, level_unlock_items, stage_objective_items,
     junk_items, token_items, weapon_items, vehicle_items, warp_items, rifle_components,
     weapon_group_items, object_items, key_items, trap_items) = GetAllItemInfo()

    item_groups: typing.Dict[str, list] = {
        "Chaos Emeralds": [e.name for e in emerald_items],
        "Unlocks": [e.name for e in level_unlock_items],
        "Weapons": [e.name for e in weapon_items],
        "Vehicles": [e.name for e in vehicle_items],
        "Vacuums": [w.name for w in weapon_items if "Vacuum" in w.name],
        "Rifles": [w.name for w in rifle_components],
        "Junk": [w.name for w in junk_items]
    }

    return item_groups
