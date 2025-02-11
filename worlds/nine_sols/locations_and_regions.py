import json
import pkgutil
import typing
from typing import Any, Dict, List, NamedTuple, Optional, Set

from BaseClasses import CollectionState, Location, Region
from Utils import restricted_loads
from worlds.generic.Rules import set_rule
from .options import Spawn
from .should_generate import should_generate

if typing.TYPE_CHECKING:
    from . import NineSolsWorld


class NineSolsLocation(Location):
    game = "Nine Sols"


class NineSolsLocationData(NamedTuple):
    region: str
    address: Optional[int] = None
    category: Optional[str] = None


class NineSolsRegionData(NamedTuple):
    connecting_regions: List[str] = []


pickled_data = pkgutil.get_data(__name__, "shared_static_logic/static_logic.pickle")
unpickled_data = restricted_loads(pickled_data)
locations_data = unpickled_data["LOCATIONS"]
connections_data = unpickled_data["CONNECTIONS"]


location_data_table: Dict[str, NineSolsLocationData] = {}
for location_datum in locations_data:
    location_data_table[location_datum["name"]] = NineSolsLocationData(
        address=location_datum["address"],
        region=(location_datum["region"] if "region" in location_datum else None),
        category=(location_datum["category"] if "category" in location_datum else None),
    )

all_non_event_locations_table = {name: data.address for name, data
                                 in location_data_table.items() if data.address is not None}

location_names: Set[str] = set(entry["name"] for entry in locations_data)
location_name_groups = {
    # Auto-generated groups
    # We don't need an "Everywhere" group because AP makes that for us

    "Signals": set(n for n in location_names if n.endswith(" Signal")),

    "Ember Twin": set(n for n in location_names if n.startswith("ET: ") or n.startswith("ET Ship Log: ")),
    "Ash Twin": set(n for n in location_names if n.startswith("AT: ") or n.startswith("AT Ship Log: ")),
    "Hourglass Twins": set(n for n in location_names if
                           n.startswith("ET: ") or n.startswith("ET Ship Log: ") or
                           n.startswith("AT: ") or n.startswith("AT Ship Log: ")),
    "Timber Hearth": set(n for n in location_names if n.startswith("TH: ") or n.startswith("TH Ship Log: ")),
    "Attlerock": set(n for n in location_names if n.startswith("AR: ") or n.startswith("AR Ship Log: ")),
    "Brittle Hollow": set(n for n in location_names if n.startswith("BH: ") or n.startswith("BH Ship Log: ")),
    "Giant's Deep": set(n for n in location_names if n.startswith("GD: ") or n.startswith("GD Ship Log: ")),
    "Dark Bramble": set(n for n in location_names if n.startswith("DB: ") or n.startswith("DB Ship Log: ")),
    "Quantum Moon": set(n for n in location_names if n.startswith("QM: ") or n.startswith("QM Ship Log: ")),
    "Interloper": set(n for n in location_names if n == "Ruptured Core (Text Wheel)" or "Ship Log: Ruptured Core" in n),
    "Sun Station": set(n for n in location_names if n == "Sun Station (Projection Stone Text)" or "Ship Log: Sun Station" in n),
    "WHS": set(n for n in location_names if n == "WHS (Text Wall)" or "Ship Log: WHS" in n),
    "The Stranger": set(n for n in location_names if n.startswith("EotE: ") or n.startswith("EotE Ship Log: ")),
    "Dreamworld": set(n for n in location_names if n.startswith("DW: ") or n.startswith("DW Ship Log: ")),

    "Ship Logs": set(n for n in location_names if "Ship Log: " in n),
}


region_data_table: Dict[str, NineSolsRegionData] = {}


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
            rule = None if len(requires) == 0 else lambda state, r=requires: eval_rule(state, p, r)
            entrance = region.connect(mw.get_region(to, p), None, rule)
            indirect_region_names = regions_referenced_by_rule(requires)
            for indirect_region_name in indirect_region_names:
                mw.register_indirect_condition(mw.get_region(indirect_region_name, p), entrance)

    # add access rules to the created locations
    for ld in locations_data:
        if ld["name"] in locations_to_create and len(ld["requires"]) > 0:
            set_rule(mw.get_location(ld["name"], p),
                     lambda state, r=ld["requires"]: eval_rule(state, p, r))

    # add dynamic logic, i.e. connections based on player options
    menu = mw.get_region("Menu", p)
    # TODO: alternate spawns
    menu.add_exits(["Four Seasons Pavilion"])
    menu.add_exits(["Apeman Facility (Monitoring)"])


# In the .jsonc files we use, a location or region connection's "access rule" is defined
# by a "requires" key, whose value is an array of "criteria" strings or objects.
# These rules are designed to be evaluated by both this Python code and
# (in the future) the game mod's C# code for the in-game tracker.

# In particular: this eval_rule() function is the main piece of code which will have to
# be implemented in both languages, so it's important we keep the implementations in sync
def eval_rule(state: CollectionState, p: int, rule: List[Any]) -> bool:
    return all(eval_criterion(state, p, criterion) for criterion in rule)


def eval_criterion(state: CollectionState, p: int, criterion: Any) -> bool:
    # all valid criteria are dicts
    if isinstance(criterion, dict):
        # we're only using JSON objects / Python dicts here as discriminated unions,
        # so there should always be exactly one key-value pair
        if len(criterion.items()) != 1:
            return False
        key, value = next(iter(criterion.items()))

        # { "item": "..." } and { "anyOf": [ ... ] } and { "location": "foo" } and { "region": "bar" }
        # mean exactly what they sound like, and those are the only kinds of criteria.
        if key == "item" and isinstance(value, str):
            return state.has(value, p)
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
def regions_referenced_by_rule(rule: List[Any]) -> List[str]:
    return [region for criterion in rule for region in regions_referenced_by_criterion(criterion)]


def regions_referenced_by_criterion(criterion: Any) -> List[str]:
    # see eval_criterion comments
    if isinstance(criterion, dict):
        if len(criterion.items()) != 1:
            raise ValueError("Invalid rule criterion: " + json.dumps(criterion))
        key, value = next(iter(criterion.items()))
        if key == "item":
            return []
        elif key == "anyOf":
            return [region for sub_criterion in value for region in regions_referenced_by_criterion(sub_criterion)]
        elif key == "location":
            return [location_data_table[value].region]
        elif key == "region":
            return [value]

    raise ValueError("Invalid rule criterion: " + json.dumps(criterion))
