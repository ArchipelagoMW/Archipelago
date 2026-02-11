
import typing
from math import ceil, floor

from BaseClasses import MultiWorld, Region, Entrance, Item, ItemClassification
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from . import Items, Levels, Utils, Weapons, Regions, Vehicle, Options, Locations, Names, Objects, Story

from .Items import ShadowTheHedgehogItem, GetLevelTokenItems
from .Levels import INDIVIDUAL_LEVEL_REGIONS
from .Locations import MissionClearLocations, LocationInfo, BossClearLocations, HasCheckpointZero
from .Names import REGION_INDICES
from .Options import LevelProgression
from .Regions import character_name_to_region, region_name_for_character, weapon_name_to_region, \
    region_name_for_weapon
from . import Utils as ShadowUtils

def GetKeyRule(options, stage, player):

    required_keys = options.keys_required_for_doors

    region_list = []
    region_names = []

    arch_item = None

    if options.key_collection_method in [Options.KeyCollectionMethod.option_local, Options.KeyCollectionMethod.option_both]:
        relevant_keys_base = Objects.GetKeyLocations(stage)
        key_regions = [ k.region for k in relevant_keys_base ]

        region_items = [Names.GetDistributionRegionEventName(stage, k) for k in key_regions]
        region_names = list(set([Levels.stage_id_to_region(stage, k) for k in key_regions]))
        region_list.extend(region_items)

    if options.key_collection_method in [Options.KeyCollectionMethod.option_arch, Options.KeyCollectionMethod.option_both]:
        arch_item = Items.GetStageKeyItem(stage)

    return (lambda state, ri=region_list, a_item=arch_item: (state.count_from_list(ri, player) +
                                          (0 if a_item is None else state.count(a_item, player)) >= required_keys), region_names)

def GetRelevantTokenItem(token: LocationInfo):
    level_token_items = GetLevelTokenItems()

    if token.other == Items.ITEM_TOKEN_TYPE_FINAL:
        level_token_items = [ t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_FINAL ]
    elif token.other == Items.ITEM_TOKEN_TYPE_OBJECTIVE:
        level_token_items = [ t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_OBJECTIVE ]
    elif token.other == Items.ITEM_TOKEN_TYPE_STANDARD:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_STANDARD]
    elif token.other == Items.ITEM_TOKEN_TYPE_ALIGNMENT:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_ALIGNMENT]
        if token.alignmentId == Levels.MISSION_ALIGNMENT_DARK:
            level_token_items = [ t for t in level_token_items if t.alignmentId == Levels.MISSION_ALIGNMENT_DARK]
        elif token.alignmentId == Levels.MISSION_ALIGNMENT_HERO:
            level_token_items = [ t for t in level_token_items if t.alignmentId == Levels.MISSION_ALIGNMENT_HERO]
    elif token.other == Items.ITEM_TOKEN_TYPE_BOSS:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_BOSS]
    elif token.other == Items.ITEM_TOKEN_TYPE_FINAL_BOSS:
        level_token_items = [t for t in level_token_items if t.value == Items.ITEM_TOKEN_TYPE_FINAL_BOSS]

    if len(level_token_items) == 0:
        return None

    return level_token_items[0]

def handle_path_rules(options, player, additional_level_region, path_type, outputs=[]):
    rule = lambda state: True
    indirects = []

    if additional_level_region.hardLogicOnly:
        if options.logic_level != Options.LogicLevel.option_hard:
            #print("Path denied", additional_level_region)
            outputs.append("Impossible")
            rule = lambda state: False
            return rule, indirects

    if additional_level_region.iccLogicOnly:
        if options.chaos_control_logic_level not in [ Options.ChaosControlLogicLevel.option_hard, Options.ChaosControlLogicLevel.option_intermediate]:
            rule = lambda state: False
            return rule, indirects

    if not Levels.IsLogicLevelApplicable(additional_level_region, options, path_type, options.start_inventory):
        outputs.append("Does not apply")
        return rule, indirects

    if Names.REGION_RESTRICTION_TYPES.Impassable in additional_level_region.restrictionTypes:
        # Temp solution
        final_item = Items.GetFinalItem()
        return lambda state: state.has(final_item.name, player), indirects

    if options.chaos_control_logic_level != Options.ChaosControlLogicLevel.option_off \
        and additional_level_region.chaosControlLogicRequiresHeal:

        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.HEAL,
                                                         additional_level_region)

        if additional_level_region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_intermediate and \
                options.chaos_control_logic_level not in \
                [Options.ChaosControlLogicLevel.option_off, Options.ChaosControlLogicLevel.option_easy]:

            return weapon_rule, indirects

        if additional_level_region.chaosControlLogicType == Options.ChaosControlLogicLevel.option_hard and \
                options.chaos_control_logic_level == Options.ChaosControlLogicLevel.option_hard:

            return weapon_rule, indirects

    if Names.REGION_RESTRICTION_TYPES.KeyDoor in additional_level_region.restrictionTypes:
        key_rule, regions = GetKeyRule(options, additional_level_region.stageId, player)
        rule = lambda state,r=rule: key_rule(state) and r(state)
        indirects.extend(regions)

    if Names.REGION_RESTRICTION_TYPES.ShootOrTurret in additional_level_region.restrictionTypes:
        if options.weapon_sanity_unlock and options.vehicle_logic:
            rule_weapon_1 = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region)

            rule_weapon_2 = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LOCKON,
                                                             additional_level_region)

            rule_weapon = lambda state: rule_weapon_1(state) or rule_weapon_2(state)

            rule_vehicle = Vehicle.GetRuleByVehicleRequirement(player, "Gun Turret")

            rule_w_or_v = lambda state: (rule_weapon(state) or rule_vehicle(state))
            rule = lambda state, r=rule: rule_w_or_v(state) and r(state)
            outputs.append("Shoot Or Turret")

    if Names.REGION_RESTRICTION_TYPES.Explosion in additional_level_region.restrictionTypes:
        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.EXPLOSION,
                                                  additional_level_region)

        weapon_available = False
        bombs_available = True
        if weapon_rule is not None:
            weapon_available = True

        bomb_rule = lambda state: state.has("Bombs", player)

        if additional_level_region.stageId == Levels.STAGE_DEATH_RUINS:
            bombs_available = False

        explosion_rule = lambda state: True
        if weapon_available and options.weapon_sanity_unlock and \
            (not bombs_available):
            explosion_rule = weapon_rule
        elif bombs_available and weapon_available and options.weapon_sanity_unlock and \
            options.object_unlocks and options.object_units:
            explosion_rule = lambda state, wr=weapon_rule, br=bomb_rule: wr(state) or br(state)
        elif not weapon_available and options.object_unlocks and options.object_units:
            explosion_rule = bomb_rule

        rule = lambda state,r=rule: explosion_rule(state) and r(state)
        outputs.append("Explosion")

    elif Names.REGION_RESTRICTION_TYPES.Heal in additional_level_region.restrictionTypes:
        weapon_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.HEAL,
                                                         additional_level_region)

        weapon_available = False
        units_available = False
        if weapon_rule is not None:
            weapon_available = True

        unit_rule = lambda state: state.has("Heal Units", player)

        if additional_level_region.stageId == Levels.STAGE_THE_DOOM:
            units_available = True

        heal_rule = lambda state: True
        if weapon_available and \
                (not units_available):
            heal_rule = weapon_rule
        elif units_available and weapon_available and \
                options.object_unlocks and options.object_units:
            heal_rule = lambda state, wr=weapon_rule, ur=unit_rule: wr(state) or ur(state)
        elif not weapon_available and options.object_unlocks and options.object_units:
            heal_rule = unit_rule

        rule = lambda state, r=rule: heal_rule(state) and r(state)
        outputs.append("Heal")

    if Names.REGION_RESTRICTION_TYPES.GoldBeetle in additional_level_region.restrictionTypes:
        outputs.append("Gold Beetle")
        if options.logic_level == Options.LogicLevel.option_easy:
            gb_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region)

            rule = lambda state, r=rule: gb_rule(state) and r(state)


        elif options.logic_level == Options.LogicLevel.option_normal:
            gb_rule = Weapons.GetRuleByWeaponRequirement(player, None, additional_level_region)

            if gb_rule is not None:
                rule = lambda state, r=rule: gb_rule(state) and r(state)

    if options.weapon_sanity_unlock and Levels.IsWeaponsanityRestriction(additional_level_region.restrictionTypes):
        if Names.REGION_RESTRICTION_TYPES.Torch in additional_level_region.restrictionTypes:
            outputs.append("Torch")
            rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.TORCH,
                                                      additional_level_region)

            if rule is None:
                raise Exception("Invalid rules")

        w_rule = lambda state: True
        if Names.REGION_RESTRICTION_TYPES.VacuumOrShot in additional_level_region.restrictionTypes:
            outputs.append("Vacuum or Shot")
            v_or_s_rule = lambda state: True
            ruleA = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region)

            ruleB = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region)

            if ruleA is None and ruleB is None:
                print("Unhandled maybe issue with VacuumOrShot region")
                v_or_s_rule = lambda state: True

            elif ruleA is None:
                v_or_s_rule = ruleB

            elif ruleB is None:
                v_or_s_rule = ruleA
            else:
                v_or_s_rule = lambda state, a=ruleA, b=ruleB: a(state) or b(state)

            w_rule = lambda state, w=w_rule: v_or_s_rule(state) and w(state)

        if Names.REGION_RESTRICTION_TYPES.LongRangeGun in additional_level_region.restrictionTypes:
            outputs.append("Ranged Gun")
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LONG_RANGE,
                                                      additional_level_region)

        if Names.REGION_RESTRICTION_TYPES.Vacuum in additional_level_region.restrictionTypes:
            outputs.append("Vacuum")
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.VACUUM,
                                                      additional_level_region)

        if Names.REGION_RESTRICTION_TYPES.Gun in additional_level_region.restrictionTypes:
            outputs.append("Shot")
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.SHOT,
                                                      additional_level_region)

        if Names.REGION_RESTRICTION_TYPES.AnyStageWeapon in additional_level_region.restrictionTypes:
            outputs.append("AnyStageWeapon")
            w_rule = Weapons.GetRuleByWeaponRequirement(player, None, additional_level_region)

            if w_rule is None:
                w_rule = lambda state: False

        if Names.REGION_RESTRICTION_TYPES.SatelliteGun in additional_level_region.restrictionTypes:
            outputs.append("Satelitte Gun")
            w_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.LOCKON,
                                                      additional_level_region)

        if w_rule is None and rule is None:
            print("Unhandled errors")
            rule = lambda state: False
        elif w_rule is None:
            print("Unknown w_rule here:", additional_level_region)
            rule = lambda state, r=rule: r(state)
        elif rule is None:
            rule = lambda state, w=w_rule: w(state)
        else:
            rule = lambda state, w=w_rule, r=rule: w(state) and r(state)

    if options.vehicle_logic and Names.REGION_RESTRICTION_TYPES.Car in additional_level_region.restrictionTypes:
        c_rule = lambda state: True
        # If used anywhere else, need to change to check accessibility
        ruleCar = Vehicle.GetRuleByVehicleRequirement(player, "Standard Car")
        ruleConv = Vehicle.GetRuleByVehicleRequirement(player, "Convertible")
        c_rule = lambda state, r_car=ruleCar, r_conv=ruleConv: r_car(state) or r_conv(state)

        outputs.append("Car")
        rule = lambda state, r=rule: c_rule(state) and r(state)


    if options.vehicle_logic and Levels.IsVeichleSanityRestriction(additional_level_region.restrictionTypes):
        v_rule = lambda state: True
        if Names.REGION_RESTRICTION_TYPES.BlackArmsTurret in additional_level_region.restrictionTypes:
            outputs.append("Black Turret")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Turret")
        if Names.REGION_RESTRICTION_TYPES.BlackVolt in additional_level_region.restrictionTypes:
            outputs.append("Black Volt")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Volt")
        if Names.REGION_RESTRICTION_TYPES.BlackHawk in additional_level_region.restrictionTypes:
            outputs.append("Black Hawk")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Black Hawk")
        if Names.REGION_RESTRICTION_TYPES.GunJumper in additional_level_region.restrictionTypes:
            outputs.append("Gun Jumper")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Jumper")
        if Names.REGION_RESTRICTION_TYPES.AirSaucer in additional_level_region.restrictionTypes:
            outputs.append("Air Saucer")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Air Saucer")
        if Names.REGION_RESTRICTION_TYPES.GunLift in additional_level_region.restrictionTypes:
            outputs.append("Gun Lift")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Lift")
        if Names.REGION_RESTRICTION_TYPES.GunTurret in additional_level_region.restrictionTypes:
            outputs.append("Gun Turret")
            v_rule = Vehicle.GetRuleByVehicleRequirement(player, "Gun Turret")

        rule = lambda state, r=rule, v=v_rule: v(state) and r(state)

    if Names.REGION_RESTRICTION_TYPES.ShadowRifle in additional_level_region.restrictionTypes:
        sr_rule = Weapons.GetRuleByWeaponRequirement(player, Weapons.WeaponAttributes.SHADOW_RIFLE,
                                                         additional_level_region)
        outputs.append("Shadow Rifle")
        rule = lambda state, r=rule, r2=sr_rule: r2(state) and r(state)


    if options.object_unlocks and Levels.IsObjectRestriction(additional_level_region.restrictionTypes):
        o_rule = lambda state: True
        if Names.REGION_RESTRICTION_TYPES.Zipwire in additional_level_region.restrictionTypes and options.object_ziplines:
            o_rule = lambda state: state.has("Zipwire", player)
            outputs.append("Zipwire")
        if Names.REGION_RESTRICTION_TYPES.LightDash in additional_level_region.restrictionTypes  and options.object_light_dashes:
            o_rule = lambda state: state.has("Air Shoes", player)
            outputs.append("Light Dash")
        if Names.REGION_RESTRICTION_TYPES.WarpHole in additional_level_region.restrictionTypes  and options.object_warp_holes:
            o_rule = lambda state: state.has("Warp Holes", player)
            outputs.append("Warp Holes")
        if Names.REGION_RESTRICTION_TYPES.Rocket in additional_level_region.restrictionTypes  and options.object_rockets:
            o_rule = lambda state: state.has("Rocket", player)
            outputs.append("Rocket")
        if Names.REGION_RESTRICTION_TYPES.Pulley in additional_level_region.restrictionTypes  and options.object_pulleys:
            o_rule = lambda state: state.has("Pulley", player)
            outputs.append("Pulley")

        rule = lambda state, r=rule: o_rule(state) and r(state)

    if (options.logic_level == Options.LogicLevel.option_easy and
            Names.REGION_RESTRICTION_TYPES.NoBacktracking in additional_level_region.restrictionTypes):
        rule = lambda state: False

    for regionAccess in [ a.value for a in additional_level_region.restrictionTypes if a.value > 100]:
        outputs.append("Region")
        required_stage_region = regionAccess - 100

        access_region = [ a for a in INDIVIDUAL_LEVEL_REGIONS if a.stageId == additional_level_region.stageId and \
                           a.regionIndex == required_stage_region ][0]

        if access_region.hardLogicOnly and options.logic_level != Options.LogicLevel.option_hard:
            rule = lambda state: False
        else:
            access_rule = lambda state: state.can_reach_region(
                Levels.stage_id_to_region(additional_level_region.stageId, required_stage_region), player)

            indirects.append(Levels.stage_id_to_region(additional_level_region.stageId, required_stage_region))

            rule = lambda state, r=rule: access_rule(state) and r(state)

    return rule, indirects

def restrict_objects(multiworld, world, player):
    world_locations = [ l.name for l in world.get_locations()]

    for object in [ x for x in Objects.GetObjectChecks() if x.restrictionType != 10 ]:
        location_id, entry_location_name = Names.GetObjectLocationName(object)
        if entry_location_name in world_locations:
            location_with_restriction = world.get_location(entry_location_name)
            dummy_region = Levels.LevelRegion(object.stage, object.region, [object.restrictionType])
            location_with_restriction.access_rule = handle_path_rules(world.options, player, dummy_region,
                                                                      Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic)[0]

def lock_warp_items(multiworld, world, player):

    if world.options.level_progression == Options.LevelProgression.option_select or not world.options.secret_story_progression:
        return

    (clear_locations, mission_locations, end_location,
     enemysanity_locations, checkpointsanity_locations, charactersanity_locations,
     token_locations, keysanity_locations, weaponsanity_locations, boss_locations,
     warp_locations, object_locations) = Locations.GetActiveLocationInfo()

    warpItemInfos = Items.PopulateLevelWarpPoints()

    for warp in warp_locations:
        if warp.stageId in Levels.LAST_STORY_STAGES and not world.options.include_last_way_shuffle:
            continue

        if warp.stageId in Levels.BOSS_STAGES and world.options.level_progression == Options.LevelProgression.option_select:
            continue

        if warp.stageId not in world.available_story_levels:
            continue

        if warp.stageId in Levels.BOSS_STAGES:
            warp_story_region = Regions.boss_stage_id_to_story_region(warp.stageId)
        else:
            default_region_index = Regions.GetDefaultCheckpointRegionForStage(world, warp.stageId)
            warp_story_region = Regions.stage_id_to_story_region(warp.stageId, default_region_index)

        location = multiworld.get_location(warp.name, player)
        i = [ w for w in warpItemInfos if w.stageId == warp.stageId][0]
        mw_token_item = ShadowTheHedgehogItem(i, player)
        new_access_rule = lambda state, r=location.access_rule, s=warp_story_region: r(state) and state.can_reach_region(
            s, player)

        location.access_rule = new_access_rule

        location.place_locked_item(
            mw_token_item)

def CalculateObjectiveValueForGate(value, max_gates, gate_no, gate_density, rate=1):
    perc = pow((gate_no + gate_density), 2) / pow((max_gates+1+gate_density), 2)
    result = value * perc
    expected_result = round(result, 0)
    if expected_result == 0:
        return 1

    return expected_result


def GetGateKeyRule(world, player, gate_no):
    # Add weapon unlocks as gate requirement

    if int(gate_no) == 0:
        return lambda state: True

    gate_density = world.options.gate_density
    reqs = {}
    if gate_no in world.gate_requirements:
        reqs = world.gate_requirements[gate_no]
    else:
        if world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_objective:
            full_reqs = world.objective_requirements.copy()
            reqs = {}

            for o in full_reqs.items():
                key = o[0]
                value = o[1]
                reqs[key] = CalculateObjectiveValueForGate(value, world.options.select_gates_count, gate_no, gate_density)
            world.gate_requirements[gate_no] = reqs
        elif world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_objective_available:
            full_reqs = world.objective_requirements.copy()
            reqs = {}

            gated_stages = []
            for i in world.gates.keys():
                if i < gate_no:
                    gated_stages.extend(world.gates[i])

            previous_gates = {}
            for o in [ a for a in full_reqs.items() if Items.GetItemByName(a[0]).stageId
                                                  in gated_stages ]:
                key = o[0]
                value = o[1]
                gate_value = CalculateObjectiveValueForGate(value, world.options.select_gates_count, gate_no, gate_density)

                for key, value in previous_gates:
                    pass

                reqs[key] = gate_value

            world.gate_requirements[gate_no] = reqs
        elif world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_items:

            reqs = {
                "Gate Key": gate_no
            }

            world.gate_requirements[gate_no] = reqs
        elif world.options.gate_unlock_requirement == Options.GateUnlockRequirement.option_chaos_emeralds:
            if gate_no == 0:
                reqs = {}
            elif gate_no == 1:
                reqs = {
                    "Green Chaos Emerald": 1
                }
            elif gate_no == 2:
                reqs = {
                    "Blue Chaos Emerald": 1
                }
            elif gate_no == 3:
                reqs = {
                    "Yellow Chaos Emerald": 1
                }
            elif gate_no == 4:
                reqs = {
                    "White Chaos Emerald": 1
                }
            elif gate_no == 5:
                reqs = {
                    "Cyan Chaos Emerald": 1
                }
            elif gate_no == 6:
                reqs = {
                    "Purple Chaos Emerald": 1
                }
            elif gate_no == 7:
                reqs = {
                    "Red Chaos Emerald": 1
                }
            else:
                print("Invalid data found for gate/type:", gate_no)
                raise Exception("Invalid gate count for this mode")

            world.gate_requirements[gate_no] = reqs

        else:
            print("Unknown requirements:", reqs)

    return lambda state, o=reqs: state.has_all_counts(o, player)
#
# def CountRegionAccessibility(state, keys, data, ix, player, perc=100, stageId=None):
#     #sum(
#
#     #    [data[r] for r in GetReachableRegions(state, keys) if r in keys]) >= ix)
#
#     # This method uses events but they show up in spoiler log and look bad so use other method
#     # Which uses reachable regions instead of events
#
#     use_event_method = True
#     if use_event_method:
#         keys = list(keys)
#
#         # Which is better, % of total, or % of each region?
#
#         total = 0
#         all = True
#         values = []
#         have = []
#
#         # Keys is the names of the distribution events
#         for key in keys:
#
#             count_in_region = data[key]
#             # print("Does player have", key, count_in_region)
#             if count_in_region > 0:
#                 if state.has(key, player):
#
#                     safe = True
#                     if stageId is None:
#                         print("Invalid stageid")
#                     else:
#                         escapePaths = [ e for e in Levels.ManualEscapePaths if e.stageId == stageId]
#                         if len(escapePaths) == 0:
#                             safe = True
#
#                     if safe:
#                         values.append(count_in_region)
#                         have.append(key)
#                 else:
#                     # print("Doesn't player have", key, count_in_region)
#                     all = False
#
#         for i in values:
#             if all:
#                 total += i
#             else:
#                 total += floor(i * (perc / 100))
#
#         if all:
#             new_total = floor(total * (perc / 100))
#             if new_total == 0 and total > 0:
#                 total = 1
#
#         return total >= ix
#     else:
#         keys = list(keys)
#         all_regions = [ a.name for a in  state.reachable_regions[player]]
#         matching_counts = [ data[r] for r in all_regions if r in keys]
#         total_accessible = sum(matching_counts)
#         return total_accessible >= ix


import datetime
def CountRegionAccessibilityNew(options, state, player, stage_id, ix, stage_regions, count_data,
                                given_keys):

    # Which is better, % of total, or % of each region?

    #x = datetime.datetime.now()

    total = 0
    count_options = {}

    # Keys is the names of the distribution events
    for region in stage_regions:
        count_in_region = count_data[region]
        if count_in_region > 0:
            has_escape_path = HasEscapePath(stage_id, region, options)

            if (stage_id, region) in given_keys:
                required = given_keys[(stage_id, region)]
            else:
                required = Names.GetDistributionRegionEventName(stage_id, region)
            safe = state.has(required, player)

            if safe and has_escape_path:
                if HasInescapablePath(stage_id, region, options):
                    count_options[region] = count_data[region]
                    safe = False
                else:

                    if (stage_id, region) in given_keys:
                        required = given_keys[(stage_id, region, 1)]
                    else:
                        required = Names.GetDistributionEscapeRegionEventName(stage_id, region)

                    safe = state.has(required, player)
                    if not safe:
                        count_options[region] = count_data[region]

            if safe:
                total += count_in_region
                if total > ix:
                    return True

    if len(count_options.keys()) != 0:
        group_options = {}

        for key,value in count_options.items():
            for group_name, group_list in CHECKPOINT_ESCAPE_GROUPS[stage_id].items():
                if key in group_list:
                    if group_name not in group_options:
                        group_options[group_name] = 0
                    group_options[group_name] += value

        # This needs to be able to account for all future accessible parts currently reachable with
        # either no restriction or available restriction
        #print("COUNT OPTIONS ARE", count_options, values)
        total += max(group_options.values())

    #y = datetime.datetime.now()

    return total >= ix

def set_rules(multiworld: MultiWorld, world: World, player: int):

    token_assignments = {}

    if world.options.level_progression != LevelProgression.option_select:
        Regions.connect_by_story_mode(multiworld, world, player, world.shuffled_story_mode)

    for stage in Levels.ALL_STAGES:
        if stage in Levels.BOSS_STAGES:
            continue

        if stage not in world.available_levels:
            continue

        if HasCheckpointZero(stage):
            view_name = Names.GetDistributionRegionEventName(stage, 0)
            event_location = multiworld.get_location(view_name, player)

            event_location.access_rule = lambda state, r=Levels.stage_id_to_region(stage,
                                                                        0): \
                state.can_reach_region(r, player)

            event_location.place_locked_item(Item(view_name,
                                                  ItemClassification.progression_skip_balancing, None, player))


            view_name = Names.GetDistributionEscapeRegionEventName(stage, 0)
            event_location = multiworld.get_location(view_name, player)

            event_location.access_rule = GetEscapePathRule(world.options, player, stage, 0)

            event_location.place_locked_item(Item(view_name,
                                                  ItemClassification.progression_skip_balancing, None, player))


        #default_stage_index = Levels.GetDefaultCheckpointForStage(world, stage)
        #if default_stage_index != 0:
        #    checkpoint_rule = lambda state: True
        #    checkpoint_warp_name = Names.GetCheckpointWarpName(0)
        #    base_region_name = stage_id_to_region(stage, default_stage_index)
        #    start_region_name = stage_id_to_region(stage, 0)
        #    connect(player, checkpoint_warp_name,
        #            world.get_region(base_region_name),
        #            world.get_region(start_region_name),
        #            checkpoint_rule)

    if world.options.checkpoint_shuffle != Options.CheckpointShuffle.option_off:
        for stage in Levels.ALL_STAGES:
            if stage in Levels.BOSS_STAGES:
                continue

            if stage not in world.available_levels:
                continue

            # Temporary code til level is resolved
            #if stage == Levels.STAGE_THE_LAST_WAY:
            #    continue

            default_stage_index = Regions.GetDefaultCheckpointIndexForStage(world, stage)
            if default_stage_index == 0:
                # Always require access to a checkpoint to warp between checkpoints
                default_stage_index = 1

            base_checkpoint_region = Regions.GetCheckpointRegion(stage, default_stage_index)
            base_region_name = Levels.stage_id_to_region(stage, base_checkpoint_region)
            for checkpoint in range(0, [ c.total_count+1 for c in Locations.CheckpointLocations if c.stageId == stage ][0]):
                warp_to_region = Regions.GetCheckpointRegion(stage, checkpoint)
                new_region_name = Levels.stage_id_to_region(stage, warp_to_region)
                checkpoint_warp_name = Names.GetCheckpointWarpName(stage, warp_to_region)
                checkpoint_rule = lambda state, s=stage, c=checkpoint:\
                    state.has(Items.GetCheckpointItemName(s, c), player)
                connect(player, checkpoint_warp_name,
                                    world.get_region(base_region_name),
                                    world.get_region(new_region_name),
                                    checkpoint_rule)


    skip_regions = []
    if world.options.logic_level != Options.LogicLevel.option_hard:
        hard_only = [ r for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.hardLogicOnly]
        skip_regions.extend([ (h.stageId, h.regionIndex) for h in hard_only])

    if world.options.chaos_control_logic_level not in [
        Options.ChaosControlLogicLevel.option_hard, Options.ChaosControlLogicLevel.option_intermediate]:
        icc_only = [ r for r in Levels.INDIVIDUAL_LEVEL_REGIONS if r.iccLogicOnly ]
        skip_regions.extend([ (h.stageId, h.regionIndex) for h in icc_only])

    for additional_level_region in Levels.INDIVIDUAL_LEVEL_REGIONS:
        if additional_level_region.stageId not in world.available_levels:
            continue

        if (additional_level_region.stageId, additional_level_region.regionIndex) in skip_regions:
            continue

        if additional_level_region.regionIndex == 0:
            continue

        from_regions = additional_level_region.fromRegions

        if additional_level_region.stageId in Levels.BOSS_STAGES:
            new_region_name = Levels.boss_stage_id_to_region(additional_level_region.stageId, additional_level_region.regionIndex)
        else:
            new_region_name = Levels.stage_id_to_region(additional_level_region.stageId, additional_level_region.regionIndex)

        for region_from in from_regions:

            if (additional_level_region.stageId, region_from) in skip_regions:
                continue

            if additional_level_region.stageId in Levels.BOSS_STAGES:
                base_region_name = Levels.boss_stage_id_to_region(additional_level_region.stageId, region_from)
            else:
                base_region_name = Levels.stage_id_to_region(additional_level_region.stageId, region_from)

            base_region = world.get_region(base_region_name)
            new_region = world.get_region(new_region_name)

            path_rule, indirects = handle_path_rules(world.options, player, additional_level_region,
                                          Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic)
            if path_rule is not None:
                connection_name = Names.GetRegionEntranceName(base_region_name, new_region_name,
                                                              additional_level_region.restrictionTypes)
                connect(world.player, connection_name,
                    base_region, new_region, path_rule)

                if indirects is not None:
                    for indirect in indirects:
                        multiworld.register_indirect_condition(
                            multiworld.get_region(indirect, player),
                            multiworld.get_entrance(connection_name, player))

            else:
                print("Path rule is None", base_region_name, new_region_name)

        view_name = Names.GetDistributionRegionEventName(additional_level_region.stageId, additional_level_region.regionIndex)

        event_location = multiworld.get_location(view_name, player)

        if additional_level_region.stageId in Levels.BOSS_STAGES:
            required_access = Levels.boss_stage_id_to_region(additional_level_region.stageId,
                                                                        additional_level_region.regionIndex)
        else:
            required_access = Levels.stage_id_to_region(additional_level_region.stageId,
                                                                        additional_level_region.regionIndex)
        event_location.access_rule = lambda state, r=required_access: \
            state.can_reach_region(r, player)

        event_location.place_locked_item(Item(view_name,
                                              ItemClassification.progression_skip_balancing, None, player))

        #if (HasEscapePath(additional_level_region.stageId, additional_level_region.regionIndex, world.options) and not
        #    HasInescapablePath(additional_level_region.stageId, additional_level_region.regionIndex)):

        # Always being made, always need to be filled
        view_name = Names.GetDistributionEscapeRegionEventName(additional_level_region.stageId,
                                                               additional_level_region.regionIndex)
        event_location = multiworld.get_location(view_name, player)

        event_location.access_rule = GetEscapePathRule(world.options, player,
                                                       additional_level_region.stageId, additional_level_region.regionIndex)

        event_location.place_locked_item(Item(view_name,
                                              ItemClassification.progression_skip_balancing, None, player))

    for backtrack_region in Levels.BACKTRACKING_REGIONS:

        if backtrack_region.stageId not in world.available_levels:
            continue

        mock_region_info = (Levels.LevelRegion(backtrack_region.stageId,
                                               backtrack_region.backtrackToRegion,
                                               backtrack_region.restrictionTypes)
                            .setFromRegion(backtrack_region.backtrackFromRegion)
                            .setLogicType(backtrack_region.logicType))

        if backtrack_region.hardLogicOnly:
            mock_region_info.setHardLogicOnly()

        if (mock_region_info.stageId, mock_region_info) in skip_regions:
            continue

        from_region_name = Levels.stage_id_to_region(mock_region_info.stageId, backtrack_region.backtrackFromRegion)
        to_region_name = Levels.stage_id_to_region(mock_region_info.stageId, backtrack_region.backtrackToRegion)

        from_region = world.get_region(from_region_name)
        to_region = world.get_region(to_region_name)

        path_rule, indirects = handle_path_rules(world.options, player, mock_region_info,
                                                 Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic)
        if path_rule is not None:
            connection_name = Names.GetRegionEntranceName(from_region_name, to_region_name,
                                                          mock_region_info.restrictionTypes)
            connect(world.player, connection_name,
                    from_region, to_region, path_rule)

            if indirects is not None:
                for indirect in indirects:
                    multiworld.register_indirect_condition(
                        multiworld.get_region(indirect, player),
                        multiworld.get_entrance(connection_name, player))

        else:
            print("Path rule is None", base_region_name, new_region_name)

    override_settings = world.options.percent_overrides
    lock_warp_items(multiworld, world, world.player)

    restrict_objects(multiworld, world, world.player)

    for clear in MissionClearLocations:

        if clear.stageId not in world.available_levels:
            continue

        id, name = Levels.GetLevelCompletionNames(clear.stageId, clear.alignmentId)
        if True:
            req_rule = lambda state: True
            level_rule = lambda state: True
            character_rule = None
            rule_change = False

            # If not goal ring type, require the character in the stage
            if clear.requirement_count is not None:
                pass
                character_for_mission = clear.character.name
                character_regions = Objects.CharacterToLevel[character_for_mission]
                character_regions_for_level = [ l[1] for l in character_regions if l[0] == clear.stageId ]

                for i in character_regions_for_level:
                    region_required = Levels.stage_id_to_region(clear.stageId, i)
                    if character_rule is None:
                        character_rule = lambda state, rq=region_required: state.can_reach_region(rq, player)
                    else:
                        character_rule = lambda state, rq=region_required, cr=character_rule: state.can_reach_region(rq, player) or cr(state)

            if clear.requirements is not None:
                for req in clear.requirements:
                    lr = Levels.LevelRegion(clear.stageId, None, req)
                    lr.setLogicType(clear.logicType)

                    logic_type = Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic

                    req_rule_a, indirects_a = handle_path_rules(world.options, player, lr,
                                                 logic_type)
                    if req_rule_a is not None:
                        req_rule = lambda state, z=req_rule, a=req_rule_a: \
                            z(state) and a(state)
                        level_rule = lambda state, r_rule=req_rule, l_rule=level_rule: (
                                r_rule(state) and l_rule(state))

                        rule_change = True
            if clear.craft_requirements is not None:
                for req in clear.craft_requirements:
                    lr = Levels.LevelRegion(clear.stageId, None, req)
                    lr.setLogicType(clear.logicType)

                    logic_type = Levels.REGION_RESTRICTION_REFERENCE_TYPES.CraftLogic

                    req_rule_b,indirects_b = handle_path_rules(world.options, player, lr,
                                                 logic_type)
                    if req_rule_b is not None:
                        req_rule = lambda state, z=req_rule, b=req_rule_b: \
                            z(state) and b(state)
                        level_rule = lambda state, r_rule=req_rule, l_rule=level_rule: (
                                r_rule(state) and l_rule(state))
                        rule_change = True

            # This part sets up accessibilty to the locations
            if clear.getDistribution() is not None:

                # This functionality requires access to ALL to complete which is inflating
                # When logically you can find with access to either
                # But this also needs handling for objective-less
                #for region_id in clear.getDistribution().keys():
                #    required_region = Levels.stage_id_to_region(clear.stageId, region_id)
                ##    new_rule = lambda state, r_region=required_region: state.can_reach_region(r_region, player)
                #    level_rule = lambda state, l_rule=level_rule, n_rule=new_rule: n_rule(state) and l_rule(state)
                #    rule_change = True

                if clear.requirement_count is not None and world.options.objective_sanity:

                    location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                                 clear.mission_object_name,
                                                                                 world.options, clear.stageId,
                                                                                 clear.alignmentId,
                                                                                 world.options.percent_overrides)

                    result_sanity = ShadowUtils.GetObjectiveSanityFlag(world.options, location_details)
                    if result_sanity:

                        max_required = ShadowUtils.getMaxRequired(
                            location_details,
                            clear.requirement_count, clear.stageId, clear.alignmentId,
                            override_settings)

                        frequency_required = ShadowUtils.getMaxRequired(
                            ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE_FREQUENCY,
                                                                      clear.mission_object_name, world.options,
                                                                      clear.stageId, clear.alignmentId,
                                                                      world.options.percent_overrides),
                            100, clear.stageId, clear.alignmentId,
                            override_settings)

                        progress_distribution = clear.getDistribution().items()
                        progress_dist_by_name = {}

                        total = 0

                        if world.options.objective_sanity_system == Options.ObjectiveSanitySystem.option_individual:
                            if (clear.stageId, clear.alignmentId) in Objects.STAGE_OBJECT_ITEMS:
                                lookup_info = Objects.STAGE_OBJECT_ITEMS[(clear.stageId, clear.alignmentId)]
                                is_objectable = lookup_info[1]
                                if is_objectable == Objects.WORKS_WITH_INDIVIDUAL:
                                    total = -1
                        if total != -1:
                            for region, count in progress_distribution:
                                progress_dist_by_name[region] = count
                                total += count

                        for l in range(1, total + 1):
                            if l > max_required:
                                break

                            if l % frequency_required != 0 and max_required != l:
                                continue

                            prog_rule = lambda state, ix=l, data=progress_dist_by_name, keys=progress_dist_by_name.keys(),\
                                s=clear.stageId, kl=GetDistributionKeys(clear.stageId)\
                                : CountRegionAccessibilityNew(world.options, state, player, s, ix, keys, data, kl)

                            location_id, objective_location_name = (
                                Levels.GetLevelObjectNames(clear.stageId, clear.alignmentId, clear.mission_object_name,
                                                    l))
                            location = multiworld.get_location(objective_location_name, player)

                            progression_rule = lambda state, p_rule=prog_rule, r_rule=req_rule : \
                                p_rule(state) and r_rule(state)

                            add_rule(location, progression_rule)

                            if l > max_required:
                                break


            if clear.requirement_count is not None:
                location = multiworld.get_location(name, player)
                item_name = Items.GetStageAlignmentObject(clear.stageId, clear.alignmentId)
                max_required = ShadowUtils.getMaxRequired(
                    ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_COMPLETION,
                                                              clear.mission_object_name, world.options,
                                                              clear.stageId, clear.alignmentId,
                                                              world.options.percent_overrides),
                    clear.requirement_count, clear.stageId, clear.alignmentId,
                    override_settings)

                new_rule = lambda state: True

                location_details = ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_OBJECTIVE,
                                                                             clear.mission_object_name,
                                                                             world.options, clear.stageId,
                                                                             clear.alignmentId,
                                                                             world.options.percent_overrides)

                result_sanity = ShadowUtils.GetObjectiveSanityFlag(world.options, location_details)

                if world.options.objective_sanity and world.options.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_base_clear \
                    and result_sanity:
                    new_rule = lambda state, itemname=item_name, count=max_required: state.has(itemname, player, count=count)

                progress_distribution = clear.getDistribution().items()
                progress_dist_by_name = {}

                total = 0

                if total != -1:
                    for region, count in progress_distribution:
                        progress_dist_by_name[region] = count
                        total += count

                finish_count = 1
                if (not world.options.objective_sanity
                        or world.options.objective_sanity_behaviour != Options.ObjectiveSanityBehaviour.option_default) or \
                        not result_sanity:
                    finish_count = max_required
                    if finish_count == 0:
                        finish_count = 1

                # Enemy stage clears don't require completing objectives
                if world.options.enemy_objective_sanity and world.options.objective_sanity_behaviour == Options.ObjectiveSanityBehaviour.option_default and \
                    clear.mission_object_name in ("Soldier", "Artificial Chaos", "Alien"):
                    finish_count = 0

                prog_rule = lambda state, keys=progress_dist_by_name.keys(), data=progress_dist_by_name,\
                                   ix=finish_count, s=clear.stageId, kl=GetDistributionKeys(clear.stageId)\
                    : CountRegionAccessibilityNew(world.options, state, player, s, ix, keys, data, kl)
                    #: CountRegionAccessibility(state, keys, data, ix, player)


                #level_rule = lambda state, lr=level_rule, cr=character_rule: lr(state) and cr(state)

                # Does this work as an AND or an OR?
                level_rule = lambda state, l_rule=level_rule, n_rule=new_rule, p_rule=prog_rule, c_rule=character_rule:\
                    l_rule(state) and n_rule(state) and p_rule(state) and (c_rule is None or c_rule(state))
                add_rule(location, level_rule)
                rule_change = True
            else:

                # if equal to 1 there should only be one, and we need that region to finish
                # e.g. goal ring, core, etc.
                if clear.getDistribution() is not None:

                    # This functionality requires access to ALL to complete which is inflating
                    # When logically you can find with access to either
                    # But this also needs handling for objective-less
                    for region_id in clear.getDistribution().keys():
                        required_region = Levels.stage_id_to_region(clear.stageId, region_id)
                        new_rule = lambda state, r_region=required_region: state.can_reach_region(r_region, player)
                        level_rule = lambda state, l_rule=level_rule, n_rule=new_rule: n_rule(state) and l_rule(state)
                        rule_change = True

                location = multiworld.get_location(name, player)
                if rule_change:
                    add_rule(location, level_rule)

            associated_tokens = [t for t in world.token_locations if
                                 t.alignmentId == clear.alignmentId and
                                 t.stageId == clear.stageId and t.other != Items.ITEM_TOKEN_TYPE_BOSS]

            for token in associated_tokens:
                location = multiworld.get_location(token.name, player)
                if rule_change:
                    add_rule(location, level_rule)
                allocated_item = GetRelevantTokenItem(token)
                if allocated_item is None:
                    print("Could not resolve:", token)
                    continue
                if allocated_item.name not in token_assignments:
                    token_assignments[allocated_item.name] = []
                token_assignments[allocated_item.name].append(location)
                mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
                location.place_locked_item(
                    mw_token_item)

        #except KeyError as e:
        #    # Do nothing for mission locations that do not exist
        #    print("Key error in handling!", e)
        #    pass

    for boss in BossClearLocations:
        if boss.stageId not in world.available_levels:
            continue

        if boss.stageId == Levels.BOSS_DEVIL_DOOM:
            continue

        boss_id, boss_name = Locations.GetBossLocationName(boss.name, boss.stageId)
        location = multiworld.get_location(boss_name, player)

        boss_rule = None
        if boss.requirements is not None:
            if boss.stageId not in world.available_levels:
                continue
            lr = Levels.LevelRegion(boss.stageId, None, boss.requirements)
            lr.setLogicType(boss.logicType)
            req_rule, indirects = handle_path_rules(world.options, player, lr, Levels.REGION_RESTRICTION_REFERENCE_TYPES.BossLogic)
            if req_rule is not None:
                boss_rule = lambda state, r_rule=req_rule: r_rule(state)
                boss_id, boss_name = Locations.GetBossLocationName(boss.name, boss.stageId)
                location = multiworld.get_location(boss_name, player)
                add_rule(location, boss_rule)

        associated_tokens = [t for t in world.token_locations if
                             t.stageId == boss.stageId and
                             (t.other == Items.ITEM_TOKEN_TYPE_BOSS or t.other == Items.ITEM_TOKEN_TYPE_FINAL_BOSS)]
        for token in associated_tokens:
            allocated_item = GetRelevantTokenItem(token)
            if allocated_item.name not in token_assignments:
                token_assignments[allocated_item.name] = []
            token_location = multiworld.get_location(token.name, player)
            if boss_rule is not None:
                add_rule(token_location, boss_rule)
            token_assignments[allocated_item.name].append(location)
            mw_token_item = ShadowTheHedgehogItem(allocated_item, world.player)
            token_location.place_locked_item(
                mw_token_item)

    for character,stages in Objects.CharacterToLevel.items():
        if character in world.available_characters:
            region_name = character_name_to_region(character)
            region = world.get_region(region_name)
            already_added = []
            for stage in stages:
                region_index = 0
                if type(stage) is tuple:
                    region_index = stage[1]
                    stage = stage[0]
                    pass

                if (stage, region_index) in already_added:
                    continue

                if stage not in world.available_levels:
                    continue

                if stage in Levels.BOSS_STAGES:
                    region_stage = world.get_region(Levels.boss_stage_id_to_region(stage))
                else:
                    region_stage = world.get_region(Levels.stage_id_to_region(stage, region_index))

                region_stage.connect(region, region_name_for_character(Levels.LEVEL_ID_TO_LEVEL[stage], character, region_index))
                already_added.append((stage, region_index))


    for weapon in Weapons.WEAPON_INFO:
        if weapon.name in world.available_weapons:
            region_name = weapon_name_to_region(weapon.name)
            region = world.get_region(region_name)
            for stage in weapon.available_stages:
                region_index = 0
                if type(stage) is tuple:
                    region_index = stage[1]
                    stage = stage[0]
                    pass

                if stage not in world.available_levels:
                    continue

                rule = lambda state: True

                if (world.options.weapon_sanity_unlock and
                    world.options.weapon_sanity_hold == Options.WeaponsanityHold.option_unlocked) or \
                    Weapons.WeaponAttributes.SPECIAL in weapon.attributes:
                        rule = Weapons.GetRuleByWeaponRequirement(player, weapon.name, None)

                if stage in Levels.BOSS_STAGES:
                    region_stage = world.get_region(Levels.boss_stage_id_to_region(stage, region_index))
                else:
                    region_stage = world.get_region(Levels.stage_id_to_region(stage, region_index))
                region_stage.connect(region, region_name_for_weapon(Levels.LEVEL_ID_TO_LEVEL[stage], region_index, weapon.name),
                                     rule=rule)

    if world.options.enemy_sanity and world.options.objective_sanity_system != Options.ObjectiveSanitySystem.option_individual:
        for enemy in Locations.GetEnemySanityLocations():

            if enemy.stageId not in world.available_levels:
                continue

            if world.options.exclude_go_mode_items and enemy.stageId == Levels.STAGE_THE_LAST_WAY and \
                    not world.options.include_last_way_shuffle:
                continue

            if not world.options.last_way_enemysanity and enemy.stageId == Levels.STAGE_THE_LAST_WAY:
                continue

            max_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, world.options,
                                                          enemy.stageId, enemy.enemyClass,
                                                          world.options.percent_overrides),
                enemy.total_count, enemy.stageId, enemy.enemyClass,
                override_settings)

            perc_required = ShadowUtils.getPercRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY,
                                                          enemy.mission_object_name, world.options,
                                                          enemy.stageId, enemy.enemyClass,
                                                          world.options.percent_overrides),
                enemy.stageId, enemy.enemyClass,
                override_settings)


            frequency_required = ShadowUtils.getMaxRequired(
                ShadowUtils.getObjectiveTypeAndPercentage(ShadowUtils.TYPE_ID_ENEMY_FREQUENCY,
                                                          enemy.mission_object_name, world.options,
                                                          enemy.stageId, enemy.enemyClass,
                                                          world.options.percent_overrides),
                100, enemy.stageId, enemy.enemyClass,
                override_settings)


            enemy_distribution = enemy.getDistribution().items()
            enemy_dist_by_name = {}

            total = 0
            for region, count in enemy_distribution:
                enemy_dist_by_name[region] = count
                total += count

            for l in range(1, total+1):
                if l > max_required:
                    break

                if l % frequency_required != 0 and max_required != l:
                    continue



                new_rule = lambda state, ix=l, data=enemy_dist_by_name, keys=enemy_dist_by_name.keys(),\
                                  p=perc_required, s=enemy.stageId, kl=GetDistributionKeys(enemy.stageId) \
                    : CountRegionAccessibilityNew(world.options, state, player, s, ix, keys, data, given_keys=kl)
                    #: CountRegionAccessibility(state, keys, data, ix, player, p)
                location_id, objective_location_name = (
                    Locations.GetEnemyLocationName(enemy.stageId, enemy.enemyClass, enemy.mission_object_name,
                                        l))
                location = multiworld.get_location(objective_location_name, player)
                add_rule(location, new_rule)

                if l > max_required:
                    break

    for gate in world.gates.items():
        gate_no = gate[0]
        gate_stages = gate[1]

        if gate_no == 0:
            continue

        menu_region = world.get_region("Menu")

        handled_gate_items = []

        for gate_stage in gate_stages:

            if (gate_no, gate_stage) in handled_gate_items:
                print("As of yet unhandled dupe stages in gates")
                continue

            handled_gate_items.append((gate_no, gate_stage))

            if gate_stage in Levels.BOSS_STAGES:
                base_region_name = Levels.boss_stage_id_to_region(gate_stage)
            else:
                check_x1 = Regions.GetDefaultCheckpointRegionForStage(world, gate_stage)
                base_region_name = Levels.stage_id_to_region(gate_stage, check_x1)

            rule = GetGateKeyRule(world, player, gate_no)
            if gate_stage in Levels.BOSS_STAGES and gate_stage not in Levels.LAST_STORY_STAGES and gate_stage not in Levels.FINAL_BOSSES:
                    boss_stage_requirement = Story.GetVanillaBossStage(gate_stage)
                    if boss_stage_requirement is not None:
                        default_region_index = Regions.GetDefaultCheckpointRegionForStage(world, boss_stage_requirement)
                        boss_base_region_name = Levels.stage_id_to_region(boss_stage_requirement, default_region_index)
                        boss_gate_rule = lambda state, r1=rule, boss_region=boss_base_region_name: r1(state) and \
                                                                                        state.can_reach_region(boss_region, player)

                        bossExit = menu_region.connect(world.get_region(base_region_name),
                                            f"Gate Entrance {gate_no} - {base_region_name}",
                                            rule=boss_gate_rule)

                        multiworld.register_indirect_condition(
                            world.get_region(base_region_name), bossExit)

                        multiworld.register_indirect_condition(
                            world.get_region(boss_base_region_name), bossExit)
            else:
                menu_region.connect(world.get_region(base_region_name),
                                    f"Gate Entrance {gate_no} - {base_region_name}",
                                    rule=rule)


    goal_has = []
    if world.options.goal_chaos_emeralds:
        emeralds = Items.GetEmeraldItems()
        goal_has.extend([ (ce.name,1) for ce in emeralds ])
    if world.options.goal_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardMissionToken, token_assignments, world.options.goal_missions)
        goal_has.append(tokens)
    if world.options.goal_hero_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardHeroToken, token_assignments, world.options.goal_hero_missions)
        goal_has.append(tokens)
    if world.options.goal_dark_missions > 0:
        tokens = get_token_count(world, Items.Progression.StandardDarkToken, token_assignments, world.options.goal_dark_missions)
        goal_has.append(tokens)
    if world.options.goal_final_missions > 0:
        tokens = get_token_count(world, Items.Progression.FinalToken, token_assignments, world.options.goal_final_missions)
        goal_has.append(tokens)
    if world.options.goal_objective_missions > 0:
        tokens = get_token_count(world, Items.Progression.ObjectiveToken, token_assignments, world.options.goal_objective_missions)
        goal_has.append(tokens)
    if world.options.goal_bosses > 0:
        tokens = get_token_count(world, Items.Progression.BossToken, token_assignments, world.options.goal_bosses)
        goal_has.append(tokens)
    if world.options.goal_final_bosses > 0:
        tokens = get_token_count(world, Items.Progression.FinalBossToken, token_assignments, world.options.goal_final_bosses)
        goal_has.append(tokens)

    e_rule = lambda state, g_has=goal_has: check_final_rule(state, player, goal_has)

    if world.options.include_last_way_shuffle and world.options.level_progression != Options.LevelProgression.option_select\
            and world.options.story_shuffle != Options.StoryShuffle.option_off:

        # handle requirement that DD must be found in the level shuffle!
        devil_doom_story_region = Regions.boss_stage_id_to_story_region(Levels.BOSS_DEVIL_DOOM)
        devil_doom_region = multiworld.get_region(devil_doom_story_region, player)

        for entrance in devil_doom_region.entrances:
            entrance.access_rule = lambda state, er=e_rule, b_rule=entrance.access_rule: er(state) and b_rule(state)

    else:
        default_region_index = Regions.GetDefaultCheckpointRegionForStage(world, Levels.STAGE_THE_LAST_WAY)
        last_way_region = multiworld.get_region(Levels.stage_id_to_region(Levels.STAGE_THE_LAST_WAY, default_region_index), player)

        #if not world.options.include_last_way_shuffle:
        lw_entrance = connect(world.player, 'LastStoryToLastWay', multiworld.get_region("Menu", player),
            last_way_region, rule=e_rule)
        multiworld.register_indirect_condition(
            last_way_region, lw_entrance)

        # Ensure TLW is beatable
        tlw_location_id, tlw_location_name = Levels.GetLevelCompletionNames(Levels.STAGE_THE_LAST_WAY, Levels.MISSION_ALIGNMENT_NEUTRAL)
        last_way_rule = lambda state: state.can_reach_location(tlw_location_name, player)
        dd_region = multiworld.get_region(Levels.boss_stage_id_to_region(Levels.BOSS_DEVIL_DOOM), player)
        entrance = connect(world.player, "LastWayToDevilDoom", last_way_region,
                dd_region)

        entrance.access_rule = lambda state, lw_rule=last_way_rule, er=e_rule: er(state) and lw_rule(state)
        multiworld.register_indirect_condition(
            last_way_region,entrance)

        multiworld.register_indirect_condition(
            dd_region, entrance)

        for i in [l for l in Levels.INDIVIDUAL_LEVEL_REGIONS if l.stageId == Levels.STAGE_THE_LAST_WAY]:
            lw_sub_region = multiworld.get_region(Levels.stage_id_to_region(Levels.STAGE_THE_LAST_WAY, i.regionIndex), player)
            multiworld.register_indirect_condition(
                lw_sub_region, entrance)

    final_item = Items.GetFinalItem()
    mw_final_item = ShadowTheHedgehogItem(final_item, world.player)
    multiworld.get_location(Levels.DevilDoom_Name, world.player).place_locked_item(
        mw_final_item)

    if world.options.rifle_components:
        location = multiworld.get_location("Complete Shadow Rifle", player)
        shadow_rifle = Items.GetShadowRifle()
        mw_shadow_rifle = ShadowTheHedgehogItem(shadow_rifle, world.player)
        location.place_locked_item(mw_shadow_rifle)

        rifle_components = Items.GetRifleComponents()
        rifle_rule = lambda state: True

        for component in rifle_components:
            new_rifle_part = lambda state, cn=component.name: state.has(cn, player)
            rifle_rule = lambda state, rr=rifle_rule, nrp=new_rifle_part: rr(state) and nrp(state)

        add_rule(location, rifle_rule)

    multiworld.completion_condition[player] = lambda state: state.has(Items.Progression.GoodbyeForever, player)

def GetDistributionKeys(stageId):
    key_lookup = {
        (stageId, 0): Names.GetDistributionRegionEventName(stageId, 0),
        (stageId, 0, 1): Names.GetDistributionEscapeRegionEventName(stageId, 0)
    }

    for i in [r for r in INDIVIDUAL_LEVEL_REGIONS if r.stageId == stageId]:
        key_lookup[(stageId, i.regionIndex)] = Names.GetDistributionRegionEventName(stageId, i.regionIndex)
        key_lookup[(stageId, i.regionIndex, 1)] = Names.GetDistributionEscapeRegionEventName(stageId,i.regionIndex)

    return key_lookup

def check_final_rule(state, player, goal_has):
    have = ([x for x in goal_has if state.has(x[0], player, count=x[1])])
    return len(have) == len(goal_has)

def get_token_count(world, type, token_assignments, goal_value):
    if type not in token_assignments:
        return (type, 0)
    count = len(token_assignments[type])
    goal_req = Utils.getRequiredCount(count, goal_value, ceil)
    world.required_tokens[type] = goal_req
    return (type, goal_req)


def connect(player: int, name: str,
            source_region: Region, target_region: Region,
            rule: typing.Optional[typing.Callable] = None):
    connection = Entrance(player, name, source_region)

    if rule is not None:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    return connection


def GetEscapePathRule(options, player, stage_id, region_id):

    if not HasEscapePath(stage_id, region_id, options):
        return lambda state: True

    if HasInescapablePath(stage_id, region_id, options):
        # Do not use this one
        return lambda state: True

    return lambda state: True

    results = GetCheckpointEscapesWithCache(options)
    simplified_regions = results[stage_id][2][region_id]

    rule_options = []
    escape_regions = [ region for region in Levels.INDIVIDUAL_LEVEL_REGIONS
                       if region.stageId == stage_id and region.regionIndex in simplified_regions]
    full_rule = []

    if len(escape_regions) == 0:
        return lambda state: True

    for region in escape_regions:
        output_test = []
        rule, indirects = handle_path_rules(options, player, region, Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic,
                                 outputs=output_test)

        full_rule.append(rule)

    rule = lambda state: True
    for part_rule in full_rule:
        rule = lambda state, b=rule, r=part_rule: b(state) and r(state)

    rule_options.append(rule)

    if len(rule_options) == 0:
        return lambda state: False

    result_rule = None
    for rule in rule_options:
        if result_rule is None:
            result_rule = rule
        else:
            result_rule = lambda state, b=result_rule, r=rule: b(state) or r(state)

    return result_rule

def GetAllCheckpointEscapes(options):
    results = {}
    for level in Levels.ALL_STAGES:
        if level in Levels.BOSS_STAGES:
            continue

        simplified, stucks, inescapes = GetCheckpointEscapes(options, level)
        results[level] = (stucks, inescapes, simplified)

    return results

def GetCheckpointEscapes(options, level):
    escapes = Levels.RegionEscapes
    escape_for_level = escapes[level]

    level_data = {}
    region_simplified = {}
    for e in escape_for_level.keys():
        paths = escape_for_level[e]

        region_simplified[e] = []
        # This should factor in options, not just the combination of

        all_paths_result = []
        for path in paths:
            path_result = {}
            skip_please = []
            for path_item in path:

                if path_item in skip_please:
                    continue

                if path_item == e:
                    continue

                if str(path_item).endswith("d"):
                    skip_please.append(int(path_item[0:-1]))
                    continue

                if str(path_item).endswith("b"):
                    regionTo = int(path_item[0:-1].split("/")[0])
                    regionFrom = int(path_item[0:-1].split("/")[1])
                    skip_please.append(regionTo)
                    bt_region = [l for l in Levels.BACKTRACKING_REGIONS if
                                 l.stageId == level and l.backtrackFromRegion == regionFrom and l.backtrackToRegion == regionTo]

                    if len(bt_region) == 0:
                        print("Could not find BT region:", path_item)
                        continue

                    bt_region = bt_region[0]

                    mock_region_info = (Levels.LevelRegion(bt_region.stageId,
                                                           bt_region.backtrackToRegion,
                                                           bt_region.restrictionTypes)
                                        .setFromRegion(bt_region.backtrackFromRegion)
                                        .setLogicType(bt_region.logicType))

                    if bt_region.hardLogicOnly:
                        mock_region_info.setHardLogicOnly()
                    region = mock_region_info
                else:
                    region = [l for l in INDIVIDUAL_LEVEL_REGIONS if l.stageId == level and l.regionIndex == path_item]
                    if len(region) != 1:
                        print("Unknown, continue", e)
                        continue

                    region = region[0]

                output = []

                result = handle_path_rules(options, 0, region,
                                                 Levels.REGION_RESTRICTION_REFERENCE_TYPES.BaseLogic, outputs=output)

                if "Does not apply" not in output:
                    region_simplified[e].append(region.regionIndex)

                path_result[region.regionIndex] = output

            all_paths_result.append(path_result)

        level_data[e] = all_paths_result

    stuck_regions = []
    unstickable_regions = []

    for item in level_data.keys():
        results = level_data[item]

        if type(results) is not list:
            print("Unknown result type", item, result)
            continue

        if len(results) == 0:
            unstickable_regions.append(item)
            continue

        fully_stuck_on = True
        fully_impassable = True
        for result in results:
            if type(result) is not dict:
                print("Unhandled result type 3", item, result)
                continue

            if len(result.keys()) == 0:
                fully_stuck_on = False
                fully_impassable = False
                continue

            stuck_on = False
            impassable = False
            for j in result.values():
                if type(j) is not list:
                    print("Unhandled result type 4", item, result, j)
                    continue

                if 'Impossible' in j:
                    impassable = True

                important = [x for x in j if x != 'Does not apply']
                if len(important) != 0:
                    stuck_on = True

            if not stuck_on:
                fully_stuck_on = False

            if not impassable:
                fully_impassable = False

        if fully_impassable:
            unstickable_regions.append(item)

        elif fully_stuck_on:
            stuck_regions.append(item)

    return region_simplified, stuck_regions, unstickable_regions

STORED_CHECKPOINT_ESCAPES = None

def GetCheckpointEscapesWithCache(options):
    global STORED_CHECKPOINT_ESCAPES
    if STORED_CHECKPOINT_ESCAPES is None:
        print("Generate CEWC")
        STORED_CHECKPOINT_ESCAPES = GetAllCheckpointEscapes(options)

    return STORED_CHECKPOINT_ESCAPES

def HasEscapePath(level, region, options):
    check_data = GetCheckpointEscapesWithCache(options)
    if level in check_data:
        escapes, inescapes, simplified = check_data[level]
        if len(escapes) > 0:
            if region in escapes:
                return True

        if len(inescapes) > 0:
            if region in inescapes:
                return True

    return False

def HasInescapablePath(level, region, options):
    check_data = GetCheckpointEscapesWithCache(options)
    if level in check_data:
        escapes, inescapes, simplified = check_data[level]
        if len(inescapes) > 0:
            if region in inescapes:
                return True

    return False

CHECKPOINT_ESCAPE_GROUPS = {
    Levels.STAGE_LETHAL_HIGHWAY: {
        "A": [REGION_INDICES.LETHAL_HIGHWAY_TWO_FALL,
              REGION_INDICES.LETHAL_HIGHWAY_KEY_DOOR],
        "B": [REGION_INDICES.LETHAL_HIGHWAY_FIVE_BOMB,
              REGION_INDICES.LETHAL_HIGHWAY_FIVE_ROCKET,
              REGION_INDICES.LETHAL_HIGHWAY_FIVE_FALL]
    },

    Levels.STAGE_CRYPTIC_CASTLE: {
        "A": [REGION_INDICES.CRYPTIC_CASTLE_TWO_BALLOON,
              REGION_INDICES.CRYPTIC_CASTLE_BOMB_EASY_1,
              REGION_INDICES.CRYPTIC_CASTLE_TWO_LOWER],
        "B": [REGION_INDICES.CRYPTIC_CASTLE_TOP_PATH],
        "C": [REGION_INDICES.CRYPTIC_CASTLE_FIVE_BALLOON,
              REGION_INDICES.CRYPTIC_CASTLE_KEY_DOOR,
              REGION_INDICES.CRYPTIC_CASTLE_BOMB_EASY_2],
        "D": [REGION_INDICES.CRYPTIC_CASTLE_DARK_LIGHT_DASH]
    },

    Levels.STAGE_CIRCUS_PARK: {
        "A": [REGION_INDICES.CIRCUS_PARK_PULLEY]
    },

    Levels.STAGE_SKY_TROOPS: {
        "A": [REGION_INDICES.SKY_TROOPS_LIGHT_DASH,
              REGION_INDICES.SKY_TROOPS_GUN_JUMPER],
        "B": [REGION_INDICES.SKY_TROOPS_THREE_LOWER,
              REGION_INDICES.SKY_TROOPS_THREE_TURRET,
              REGION_INDICES.SKY_TROOPS_GUN_JUMPER_2],
        "C": [REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_EASY_1,
              REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_EASY_2,
              REGION_INDICES.SKY_TROOPS_BLACK_HAWK_CC_HARD,
              REGION_INDICES.SKY_TROOPS_HAWK_OR_VOLT]
    },

    Levels.STAGE_AIR_FLEET: {
        "A": [REGION_INDICES.AIR_FLEET_CHECKPOINT_ZERO,
              REGION_INDICES.AIR_FLEET_KEY_DOOR,
              REGION_INDICES.AIR_FLEET_AIR_SAUCER,
              REGION_INDICES.AIR_FLEET_RAILS,
              REGION_INDICES.AIR_FLEET_SECRET_1],
    },

    Levels.STAGE_IRON_JUNGLE: {
        "A": [REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_ONE,
              REGION_INDICES.IRON_JUNGLE_KEY_DOOR,
              REGION_INDICES.IRON_JUNGLE_PULLEY_NORMAL],
        "B": [REGION_INDICES.IRON_JUNGLE_LIGHT_DASH_LOWER,
              REGION_INDICES.IRON_JUNGLE_GUN_JUMPER,
              REGION_INDICES.IRON_JUNGLE_JUMPER_OR_LIGHT_DASH],
        "C": [REGION_INDICES.IRON_JUNGLE_ANDROID_HOLE_THREE,
              REGION_INDICES.IRON_JUNGLE_HERO_PULLEY]
    },

    Levels.STAGE_SPACE_GADGET:
    {
        "A": [REGION_INDICES.SPACE_GADGET_ZIPWIRE,
              REGION_INDICES.SPACE_GADGET_POST_ZIP],
        "B": [REGION_INDICES.SPACE_GADGET_LAST_DARK_ROOM]
    },

    Levels.STAGE_GUN_FORTRESS: {
        "A": [REGION_INDICES.GUN_FORTRESS_TURRET_OR_FIRE,
              REGION_INDICES.GUN_FORTRESS_ZIPWIRE_NORMAL],
        "B": [REGION_INDICES.GUN_FORTRESS_ZIP_1A,
              REGION_INDICES.GUN_FORTRESS_ZIP_1B,
              REGION_INDICES.GUN_FORTRESS_ZIP_2,
              REGION_INDICES.GUN_FORTRESS_ZIPWIRE_BASE]
    },

    Levels.STAGE_BLACK_COMET: {
        "A": [REGION_INDICES.BLACK_COMET_TWO_AIR_SAUCER,
              REGION_INDICES.BLACK_COMET_TWO_WORMS,
              REGION_INDICES.BLACK_COMET_TWO_TRIANGLE_JUMP,
              REGION_INDICES.BLACK_COMET_TWO_UP,
              REGION_INDICES.BLACK_COMET_LATER_AIR_SAUCER,
              REGION_INDICES.BLACK_COMET_LATER_WORMS,
              REGION_INDICES.BLACK_COMET_FIRST_WARP_HOLE_AREA,
              REGION_INDICES.BLACK_COMET_FIRST_WARP_FLOATERS],
        "B": [REGION_INDICES.BLACK_COMET_FOUR_AIR_SAUCER,
              REGION_INDICES.BLACK_COMET_FOUR_WORMS,
              REGION_INDICES.BLACK_COMET_FOUR_GUN_PATH,
              REGION_INDICES.BLACK_COMET_BLACK_TURRET_2],
        "C": [REGION_INDICES.BLACK_COMET_FIVE_WEAPON_FRONT,
              REGION_INDICES.BLACK_COMET_FIVE_WEAPON_BACK,
              REGION_INDICES.BLACK_COMET_FIVE_WEAPON,
              REGION_INDICES.BLACK_COMET_FIVE_PIT,
              REGION_INDICES.BLACK_COMET_ONSLAUGHT_LOWER,
              REGION_INDICES.BLACK_COMET_ONSLAUGHT_FLOATERS,
              REGION_INDICES.BLACK_COMET_HIGHER_CREATURES,
              REGION_INDICES.BLACK_COMET_FLOATERS_FROM_ABOVE,
              REGION_INDICES.BLACK_COMET_ONSLAUGHT_END],
        "D": [REGION_INDICES.BLACK_COMET_SIX_LOWER,
              REGION_INDICES.BLACK_COMET_SIX_AIR_SAUCER,
              REGION_INDICES.BLACK_COMET_SIX_WORMS],
        "E": [REGION_INDICES.BLACK_COMET_SEVEN_DROP,
              REGION_INDICES.BLACK_COMET_SEVEN_ENEMY_FAR]
    },

    Levels.STAGE_LAVA_SHELTER:
    {
        "A": [REGION_INDICES.LAVA_SHELTER_DEFENSE_FOUR,
              REGION_INDICES.LAVA_SHELTER_LIGHT_DASH_DARK]
    },

    Levels.STAGE_COSMIC_FALL:
    {
        "A": [REGION_INDICES.COSMIC_FALL_CHECKPOINT_ZERO],
        "B": [REGION_INDICES.COSMIC_FALL_ONE_AWAY],
        "C": [REGION_INDICES.COSMIC_FALL_TWO_AWAY,
              REGION_INDICES.COSMIC_FALL_PULLEY_CORE],
        "D": [REGION_INDICES.COSMIC_FALL_FOUR_AWAY],
        "E": [REGION_INDICES.COSMIC_FALL_LIGHT_DASH,
              REGION_INDICES.COSMIC_FALL_GUN_JUMPER,
              REGION_INDICES.COSMIC_FALL_GUN_JUMPER_PULLEY_HARD,
              REGION_INDICES.COSMIC_FALL_LD_OR_JUMPER]
    },

    Levels.STAGE_FINAL_HAUNT: {
        "A": [REGION_INDICES.FINAL_HAUNT_SHIELD_ONE],
        "F": [REGION_INDICES.FINAL_HAUNT_HERO_SPLIT],
        "B": [REGION_INDICES.FINAL_HAUNT_BEFORE_ROCKET],
        "C": [REGION_INDICES.FINAL_HAUNT_SHIELD_TWO],
        "G": [REGION_INDICES.FINAL_HAUNT_FOUR_LOWER],
        "D": [REGION_INDICES.FINAL_HAUNT_FIVE_VACUUM,
              REGION_INDICES.FINAL_HAUNT_BLACK_VOLT_2,
              REGION_INDICES.FINAL_HAUNT_DARK_TURRET,
              REGION_INDICES.FINAL_HAUNT_KEY_DOOR,
              REGION_INDICES.FINAL_HAUNT_SECRET_TURRET,
              REGION_INDICES.FINAL_HAUNT_VOLT_OR_FIVE],
        "E": [REGION_INDICES.FINAL_HAUNT_SHIELD_THREE]
    }
}