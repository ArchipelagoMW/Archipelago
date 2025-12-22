import json
import pkgutil
import typing
from typing import Any, NamedTuple

from BaseClasses import CollectionState, Location, Region
from Utils import restricted_loads
from worlds.generic.Rules import CollectionRule, set_rule
from .options import FirstRootNode, LogicDifficulty, NineSolsGameOptions
from .should_generate import should_generate

if typing.TYPE_CHECKING:
    from . import NineSolsWorld


class NineSolsLocation(Location):
    game = "Nine Sols"


class NineSolsLocationData(NamedTuple):
    region: str
    address: int | None = None
    category: str | None = None


class NineSolsRegionData(NamedTuple):
    connecting_regions: list[str] = []


pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
unpickled_data = restricted_loads(pickled_data)
locations_data = unpickled_data["LOCATIONS"]
connections_data = unpickled_data["CONNECTIONS"]


location_data_table: dict[str, NineSolsLocationData] = {}
for location_datum in locations_data:
    location_data_table[location_datum["name"]] = NineSolsLocationData(
        address=location_datum["address"],
        region=(location_datum["region"] if "region" in location_datum else None),
        category=(location_datum["category"] if "category" in location_datum else None),
    )

all_non_event_locations_table = {name: data.address for name, data
                                 in location_data_table.items() if data.address is not None}

location_names: set[str] = set(entry["name"] for entry in locations_data)

afm = set(n for n in location_names if n.startswith("AF (Monitoring): "))
afe = set(n for n in location_names if n.startswith("AF (Elevator): "))
afd = set(n for n in location_names if n.startswith("AF (Depths): "))
ch = set(n for n in location_names if n.startswith("Central Hall: "))
fsp = set(n for n in location_names if n.startswith("FSP: "))
cc = set(n for n in location_names if n.startswith("Cortex Center: "))
cth = set(n for n in location_names if n.startswith("CTH: "))
pre = set(n for n in location_names if n.startswith("PR (East): "))
prc = set(n for n in location_names if n.startswith("PR (Central): "))
prw = set(n for n in location_names if n.startswith("PR (West)"))
lyr = set(n for n in location_names if n.startswith("LYR: "))
gh = set(n for n in location_names if n.startswith("Greenhouse: "))
wos = set(n for n in location_names if n.startswith("W&OS: "))
yc = set(n for n in location_names if n.startswith("Yinglong Canal: "))
fgh = set(n for n in location_names if n.startswith("Factory (GH): "))
fu = set(n for n in location_names if n.startswith("Factory (U): "))
prison = set(n for n in location_names if n.startswith("Prison: "))
fmr = set(n for n in location_names if n.startswith("Factory (MR): "))
fpa = set(n for n in location_names if n.startswith("Factory (PA): "))
am = set(n for n in location_names if n.startswith("AM: "))
uc = set(n for n in location_names if n.startswith("UC: "))
gd = set(n for n in location_names if n.startswith("Galactic Dock: "))
ow = set(n for n in location_names if n.startswith("OW: "))
iw = set(n for n in location_names if n.startswith("IW: "))
br = set(n for n in location_names if n.startswith("BR: "))
gos_y = set(n for n in location_names if n.startswith("GoS (Entry): "))
gos_e = set(n for n in location_names if n.startswith("GoS (East): "))
gos_w = set(n for n in location_names if n.startswith("GoS (West): "))
st = set(n for n in location_names if n.startswith("Sky Tower: "))
edp = set(n for n in location_names if n.startswith("ED (Passages): "))
edla = set(n for n in location_names if n.startswith("ED (Living Area): "))
eds = set(n for n in location_names if n.startswith("ED (Sanctum): "))
trc = set(n for n in location_names if n.startswith("TRC: "))

location_name_groups = {
    # Auto-generated groups
    # We don't need an "Everywhere" group because AP makes that for us
    "AFM": afm, "AF (Monitoring)": afm, "Apeman Facility (Monitoring)": afm,
    "AFE": afe, "AF (Elevator)": afe, "Apeman Facility (Elevator)": afe,
    "AFD": afd, "AF (Depths)": afd, "Apeman Facility (Depths)": afd,
    "CH": ch, "Central Hall": ch,
    "FSP": fsp, "Four Seasons Pavilion": fsp,
    "CC": cc, "Cortex Center": cc,
    "CTH": cth, "Central Transport Hub": cth,
    "PRE": pre, "PR (East)": pre, "Power Reservoir (East)": pre,
    "PRC": prc, "PR (Central)": prc, "Power Reservoir (Central)": prc,
    "PRW": prw, "PR (West)": prw, "Power Reservoir (West)": prw,
    "LYR": lyr, "Lake Yaochi Ruins": lyr,
    "GH": gh, "Greenhouse": gh,
    "W&OS": wos, "Water & Oxygen Synthesis": wos,
    "YC": yc, "Yinglong Canal": yc,
    "FGH": fgh, "Factory (GH)": fgh, "Factory (Great Hall)": fgh,
    "FU": fu, "Factory (U)": fu, "Factory (Underground)": fu,
    "P": prison, "Prison": prison,
    "FMR": fmr, "Factory (MR)": fmr, "Factory (Machine Room)": fmr,
    "FPA": fpa, "Factory (PA)": fpa, "Factory (Production Area)": fpa,
    "AM": am, "Abandoned Mines": am,
    "UC": uc, "Underground Cave": uc,
    "GD": gd, "Galactic Dock": gd,
    "OW": ow, "Outer Warehouse": ow,
    "IW": iw, "Inner Warehouse": iw,
    "BR": br, "Boundless Repository": br,
    "GoSY": gos_y, "GoS (Entry)": gos_y, "Grotto of Scriptures (Entry)": gos_y,
    "GoSE": gos_e, "GoS (East)": gos_e, "Grotto of Scriptures (East)": gos_e,
    "GoSW": gos_w, "GoS (West)": gos_w, "Grotto of Scriptures (West)": gos_w,
    "ST": st, "Sky Tower": st,
    "EDP": edp, "ED (Passages)": edp, "Empyrean District (Passages)": edp,
    "EDLA": edla, "ED (Living Area)": edla, "Empyrean District (Living Area)": edla,
    "EDS": eds, "ED (Sanctum)": eds, "Empyrean District (Sanctum)": eds,
    "TRC": trc, "Tiandao Research Center": trc,

    # Manually curated groups
    "Sol Seal Locations": {
        "Kuafu's Vital Sanctum",
        "Goumang's Vital Sanctum",
        "Yanlao's Vital Sanctum",
        "Jiequan's Vital Sanctum",
        "Cortex Center: Defeat Lady Ethereal",
        "Ji's Vital Sanctum",
        "ED (Living Area): Fuxi's Vital Sanctum",
        "Nuwa's Vital Sanctum",
    },
    "Sol Fight Rewards": {
        "Kuafu's Vital Sanctum", "Defeat General Yingzhao",
        "Goumang's Vital Sanctum", "Chest After Goumang (1st Reward)", "Chest After Goumang (2nd Reward)",
        "Yanlao's Vital Sanctum", "Yanlao's Tianhuo Flower", "BR: Vault 1st Chest", "BR: Vault 2nd Chest",
        "BR: Examine Vault Scroll", "BR: Vault 3rd Chest", "BR: Vault 4th Chest",
        "Jiequan's Vital Sanctum", "Jiequan's Tianhuo Flower", "Chest After Jiequan",
        "Cortex Center: Defeat Lady Ethereal", "Cortex Center: Tianhuo Flower After Soulscape",
        "Cortex Center: Retrieve Chip From Shanhai 9000",
        "Nuwa's Vital Sanctum", "Chest After Fengs", "Nuwa's Tianhuo Flower",
        "Examine Ji", "Ji's Vital Sanctum", "Retrieve Chip From Shanhai 1000",
    }
}


region_data_table: dict[str, NineSolsRegionData] = {}


def create_regions(world: "NineSolsWorld") -> None:
    mw = world.multiworld
    p = world.player
    options = world.options

    # start by ensuring every region is a key in region_data_table
    locations_to_create = {k: v for k, v in location_data_table.items()
                           if should_generate(v.category, world)}

    for ld in locations_to_create.values():
        region_name = ld.region
        if region_name not in region_data_table:
            region_data_table[region_name] = NineSolsRegionData()

    connections_to_create = [c for c in connections_data
                             if should_generate(c["category"] if "category" in c else None, world)]

    for cd in connections_to_create:
        if cd["from"] not in region_data_table:
            region_data_table[cd["from"]] = NineSolsRegionData()
        if cd["to"] not in region_data_table:
            region_data_table[cd["to"]] = NineSolsRegionData()

    # actually create the Regions, initially all empty
    for region_name in region_data_table.keys():
        mw.regions.append(Region(region_name, p, mw))

    # add locations and connections to each region
    for region_name, region_data in region_data_table.items():
        region = mw.get_region(region_name, p)
        region.add_locations({
            location_name: location_data.address for location_name, location_data in locations_to_create.items()
            if location_data.region == region_name
        }, NineSolsLocation)

        exit_connections = [cd for cd in connections_to_create if cd["from"] == region_name]
        for connection in exit_connections:
            rule, indirect_region_names = get_combined_access_rule(connection, world)
            entrance = region.connect(mw.get_region(connection["to"], p), None, rule)
            for indirect_region_name in indirect_region_names:
                mw.register_indirect_condition(mw.get_region(indirect_region_name, p), entrance)

    # add access rules to the created locations
    for ld in locations_data:
        if ld["name"] in locations_to_create:
            rule, _ = get_combined_access_rule(ld, world)
            set_rule(mw.get_location(ld["name"], p), rule)

    world.origin_region_name = "FSP - Root Node"
    if options.first_root_node == FirstRootNode.option_apeman_facility_monitoring:
        first_node_region = "AFM - Root Node"
    elif options.first_root_node == FirstRootNode.option_galactic_dock:
        first_node_region = "GD - Root Node & Right Exit"
    elif options.first_root_node == FirstRootNode.option_power_reservoir_east:
        first_node_region = "PRE - Root Node"
    elif options.first_root_node == FirstRootNode.option_lake_yaochi_ruins:
        first_node_region = "LYR - Root Node"
    elif options.first_root_node == FirstRootNode.option_yinglong_canal:
        first_node_region = "YC - Root Node"
    elif options.first_root_node == FirstRootNode.option_factory_great_hall:
        first_node_region = "FGH - Lower Levels & Root Node"
    elif options.first_root_node == FirstRootNode.option_outer_warehouse:
        first_node_region = "OW - Root Node & Middle Exits"
    elif options.first_root_node == FirstRootNode.option_grotto_of_scriptures_entry:
        first_node_region = "GoSY - Root Node"
    elif options.first_root_node == FirstRootNode.option_grotto_of_scriptures_east:
        first_node_region = "GoSE - Root Node"
    elif options.first_root_node == FirstRootNode.option_grotto_of_scriptures_west:
        first_node_region = "GoSW - Root Node"
    elif options.first_root_node == FirstRootNode.option_agrarian_hall:
        first_node_region = "AH - Root Node"
    elif options.first_root_node == FirstRootNode.option_radiant_pagoda:
        first_node_region = "RP - Root Node"
    elif options.first_root_node == FirstRootNode.option_apeman_facility_depths:
        first_node_region = "AFD - Root Node"
    elif options.first_root_node == FirstRootNode.option_central_transport_hub:
        first_node_region = "CTH - Root Node"
    elif options.first_root_node == FirstRootNode.option_factory_underground:
        first_node_region = "FU - Root Node & Lower Elevator"
    elif options.first_root_node == FirstRootNode.option_inner_warehouse:
        first_node_region = "IW - Root Node"
    elif options.first_root_node == FirstRootNode.option_power_reservoir_west:
        first_node_region = "PRW - Root Node"
    else:
        raise Exception("Unrecognized first_root_node")

    mw.get_region(world.origin_region_name, p).add_exits([first_node_region])

# `logic` can be a location or a connection
def get_combined_access_rule(logic: Any, world: "NineSolsWorld") -> tuple[CollectionRule, list[str]]:
    vanilla_requires = logic["requires"] if "requires" in logic else None

    medium_requires = None
    if "medium_requires" in logic:
        if world.options.logic_difficulty >= LogicDifficulty.option_medium:
            medium_requires = logic["medium_requires"]
        elif world.using_ut and world.options.logic_difficulty == LogicDifficulty.option_vanilla:
            medium_requires = [{"item": world.glitches_item_name}] + logic["medium_requires"]

    ls_requires = None
    if "ls_requires" in logic:
        if world.options.logic_difficulty >= LogicDifficulty.option_ledge_storage:
            ls_requires = logic["ls_requires"]
        elif world.using_ut and world.options.logic_difficulty == LogicDifficulty.option_medium:
            ls_requires = [{"item": world.glitches_item_name}] + logic["ls_requires"]

    all_requires_levels = [x for x in [vanilla_requires, medium_requires, ls_requires] if x is not None]
    if len(all_requires_levels) == 0:
        return lambda state: False, []
    elif all(len(r) == 0 for r in all_requires_levels):
        return lambda state: True, []
    else:
        requires = all_requires_levels[0] if len(all_requires_levels) == 1 else [{"anyOf": all_requires_levels}]
        requires = pre_eval_option_criteria_in_rule(world.options, requires)
        return (
            lambda state, r=requires: eval_rule(state, world.player, world.options, r),  # noqa
            regions_referenced_by_rule(requires)
        )


# In the .jsonc files we use, a location or region connection's "access rule" is defined
# by a "requires" key, whose value is an array of "criteria" strings or objects.
# These rules are designed to be evaluated by both this Python code and
# (in the future) the game mod's C# code for the in-game tracker.

# In particular: this eval_rule() function is the main piece of code which will have to
# be implemented in both languages, so it's important we keep the implementations in sync
def eval_rule(state: CollectionState, p: int, options: NineSolsGameOptions, rule: list[Any]) -> bool:
    return all(eval_criterion(state, p, options, criterion) for criterion in rule)


def eval_criterion(state: CollectionState, p: int, options: NineSolsGameOptions, criterion: Any) -> bool:
    if isinstance(criterion, list):
        return all(eval_criterion(state, p, options, sub_criterion) for sub_criterion in criterion)

    if isinstance(criterion, dict):
        # we can ignore "option" criteria here, because those should have been "pre-eval"ed already
        key, value = next(iter(criterion.items()))
        if (key == "item" or key == "item_group") and isinstance(value, str):
            count = 1
            if "count" in criterion:
                count = criterion["count"]
            if "count_option" in criterion:
                count = getattr(options, criterion["count_option"]).value

            if key == "item_group":
                return state.has_group(value, p, count)
            return state.has(value, p, count)
        elif key == "count":
            raise ValueError("Apparently dict iteration can hit 'count' first?: " + json.dumps(criterion))
        elif key == "anyOf" and isinstance(value, list):
            return any(eval_criterion(state, p, options, sub_criterion) for sub_criterion in value)
        elif key == "location" and isinstance(value, str):
            return state.can_reach(value, "Location", p)
        elif key == "region" and isinstance(value, str):
            return state.can_reach(value, "Region", p)

    raise ValueError("Unable to evaluate rule criterion: " + json.dumps(criterion))


def pre_eval_option_criteria_in_rule(options: NineSolsGameOptions, rule: list[Any]) -> list[Any]:
    return [pre_eval_option_criterion(options, c) for c in rule]


def pre_eval_option_criterion(options: NineSolsGameOptions, criterion: Any) -> Any:
    if isinstance(criterion, list):
        return pre_eval_option_criteria_in_rule(options, criterion)

    if isinstance(criterion, dict):
        if "option" in criterion:
            option_name = criterion["option"]
            option_str_value = getattr(options, option_name).current_key
            return pre_eval_option_criterion(options, criterion[option_str_value])
        else:
            return criterion

    raise ValueError("Unable to pre-evaluate rule criterion: " + json.dumps(criterion))


# Per AP docs:
# "When using state.can_reach within an entrance access condition,
# you must also use multiworld.register_indirect_condition."
# And to call register_indirect_condition, we need to know what regions a rule is referencing.
# Figuring out the regions referenced by a rule ends up being very similar to evaluating that rule.
def regions_referenced_by_rule(rule: list[Any]) -> list[str]:
    return [region for criterion in rule for region in regions_referenced_by_criterion(criterion)]


def regions_referenced_by_criterion(criterion: Any) -> list[str]:
    # see eval_criterion comments
    if isinstance(criterion, list):
        return [region for sub_criterion in criterion for region in regions_referenced_by_criterion(sub_criterion)]

    if isinstance(criterion, dict):
        # we can ignore "option" criteria here, because those should have been "pre-eval"ed already
        key, value = next(iter(criterion.items()))
        if key == "item" or key == "item_group" or key == "count":
            return []
        elif key == "anyOf":
            return [region for sub_criterion in value for region in regions_referenced_by_criterion(sub_criterion)]
        elif key == "location":
            return [location_data_table[value].region]
        elif key == "region":
            return [value]

    raise ValueError("Invalid rule criterion: " + json.dumps(criterion))
