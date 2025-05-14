import json
import pkgutil
import typing
from typing import Any, NamedTuple

from BaseClasses import CollectionState, Location, Region
from Utils import restricted_loads
from worlds.generic.Rules import set_rule
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
}


region_data_table: dict[str, NineSolsRegionData] = {}


def create_regions(world: "NineSolsWorld") -> None:
    mw = world.multiworld
    p = world.player
    options = world.options

    # start by ensuring every region is a key in region_data_table
    locations_to_create = {k: v for k, v in location_data_table.items()
                           if should_generate(v.category, options)}

    for ld in locations_to_create.values():
        region_name = ld.region
        if region_name not in region_data_table:
            region_data_table[region_name] = NineSolsRegionData()

    connections_to_create = [c for c in connections_data
                             if should_generate(c["category"] if "category" in c else None, options)]

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
            to = connection["to"]
            requires = connection["requires"]
            # we'll replace this with a generic "requires": { "option": ... } syntax when we get to trick logic
            if (region_name == "CC - Root Node" and to == "CC - Root Node After Boss"
                    and options.skip_soulscape_platforming):
                requires = [  # no TCK, only the platforming required that
                    {"item": "Event - Lady Ethereal Soulscape Unlocked"},
                    {"item": "Air Dash"}
                ]
            rule = None if len(requires) == 0 else lambda state, r=requires: eval_rule(state, p, r)  # noqa
            entrance = region.connect(mw.get_region(to, p), None, rule)
            indirect_region_names = regions_referenced_by_rule(requires)
            for indirect_region_name in indirect_region_names:
                mw.register_indirect_condition(mw.get_region(indirect_region_name, p), entrance)

    # add access rules to the created locations
    for ld in locations_data:
        if ld["name"] in locations_to_create and len(ld["requires"]) > 0:
            set_rule(mw.get_location(ld["name"], p),
                     lambda state, r=ld["requires"]: eval_rule(state, p, r))  # noqa

    world.origin_region_name = "FSP - Root Node"
    # add dynamic logic, i.e. connections based on player options
    first_node_region = "AFM - Root Node"
    mw.get_region(world.origin_region_name, p).add_exits([first_node_region])


# In the .jsonc files we use, a location or region connection's "access rule" is defined
# by a "requires" key, whose value is an array of "criteria" strings or objects.
# These rules are designed to be evaluated by both this Python code and
# (in the future) the game mod's C# code for the in-game tracker.

# In particular: this eval_rule() function is the main piece of code which will have to
# be implemented in both languages, so it's important we keep the implementations in sync
def eval_rule(state: CollectionState, p: int, rule: list[Any]) -> bool:
    return all(eval_criterion(state, p, criterion) for criterion in rule)


def eval_criterion(state: CollectionState, p: int, criterion: Any) -> bool:
    if isinstance(criterion, list):
        return all(eval_criterion(state, p, sub_criterion) for sub_criterion in criterion)

    if isinstance(criterion, dict):
        key, value = next(iter(criterion.items()))

        # { "item": "..." } and { "anyOf": [ ... ] } and { "location": "foo" } and { "region": "bar" }
        # mean exactly what they sound like, and those are the only kinds of criteria.
        if key == "item" and isinstance(value, str):
            if "count" in criterion:
                return state.has(value, p, criterion["count"])
            return state.has(value, p)
        elif key == "item_group" and isinstance(value, str):
            if "count" in criterion:
                return state.has_group(value, p, criterion["count"])
            return state.has_group(value, p)
        elif key == "count":
            raise ValueError("Apparently dict iteration can hit 'count' first?: " + json.dumps(criterion))
        elif key == "anyOf" and isinstance(value, list):
            return any(eval_criterion(state, p, sub_criterion) for sub_criterion in value)
        elif key == "location" and isinstance(value, str):
            return state.can_reach(value, "Location", p)
        elif key == "region" and isinstance(value, str):
            return state.can_reach(value, "Region", p)

    raise ValueError("Unable to evaluate rule criterion: " + json.dumps(criterion))


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
