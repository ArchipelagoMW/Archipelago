from collections import deque

from .definitions_types import (
    AutopelagoAllRequirement,
    AutopelagoAnyRequirement,
    AutopelagoAnyTwoRequirement,
    AutopelagoGameRequirement,
    AutopelagoItemRequirement,
    AutopelagoNonProgressionItemType,
    AutopelagoRegionDefinition,
)
from .items import item_key_to_name, item_name_groups, item_name_to_rat_count
from .util import defs, gen_ids

autopelago_regions: dict[str, AutopelagoRegionDefinition] = {}
location_name_to_progression_item_name: dict[str, str] = {}
location_name_to_nonprogression_item: dict[str, AutopelagoNonProgressionItemType] = {}
location_name_to_requirement: dict[str, AutopelagoGameRequirement] = {}
location_name_to_id: dict[str, int] = {}
_location_id_gen = gen_ids()

# build regions for landmarks
for k, curr_region in defs["regions"]["landmarks"].items():
    _name = curr_region["name"]
    location_name_to_id[_name] = next(_location_id_gen)
    location_name_to_progression_item_name[_name] = item_key_to_name[curr_region["unrandomized_item"]]
    location_name_to_requirement[_name] = curr_region["requires"]
    exits: list[str] = curr_region["exits"] if "exits" in curr_region else []
    autopelago_regions[k] = AutopelagoRegionDefinition(k, exits, [_name], curr_region["requires"], True)

# build regions for fillers. these don't have any special requirements beyond region connections.
_no_requirement: AutopelagoAllRequirement = {"all": []}
for rk, curr_region in defs["regions"]["fillers"].items():
    _locations: list[str] = []
    _cur = 1
    region_items = curr_region["unrandomized_items"]
    for k in region_items["key"] if "key" in region_items else []:
        if isinstance(k, str):
            # key:
            #   - pizza_rat
            _name = curr_region["name_template"].replace("{n}", f"{_cur}")
            location_name_to_id[_name] = next(_location_id_gen)
            location_name_to_progression_item_name[_name] = item_key_to_name[k]
            _locations.append(_name)
            _cur += 1
        else:
            # key:
            #   - item: pack_rat
            #     count: 5
            for _ in range(k["count"]):
                _name = curr_region["name_template"].replace("{n}", f"{_cur}")
                location_name_to_id[_name] = next(_location_id_gen)
                location_name_to_progression_item_name[_name] = item_key_to_name[k["item"]]
                _locations.append(_name)
                _cur += 1
    for _ in range(region_items["useful_nonprogression"]) if "useful_nonprogression" in region_items else []:
        _name = curr_region["name_template"].replace("{n}", f"{_cur}")
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = "useful_nonprogression"
        _locations.append(_name)
        _cur += 1
    for _ in range(region_items["filler"]) if "filler" in region_items else []:
        _name = curr_region["name_template"].replace("{n}", f"{_cur}")
        location_name_to_id[_name] = next(_location_id_gen)
        location_name_to_nonprogression_item[_name] = "filler"
        _locations.append(_name)
        _cur += 1
    autopelago_regions[rk] = AutopelagoRegionDefinition(rk, curr_region["exits"], _locations, _no_requirement, False)


def _get_required_rat_count(req: AutopelagoGameRequirement):
    if "all" in req:
        return max(_get_required_rat_count(sub_req) for sub_req in req["all"]) if req["all"] else 0
    if "any" in req:
        return min(_get_required_rat_count(sub_req) for sub_req in req["any"])
    if "rat_count" in req:
        return req["rat_count"]
    return 0


max_required_rat_count = max(
    _get_required_rat_count(req) for req in
        [location_name_to_requirement.values()] +
        [r.requires for r in autopelago_regions.values()]
)
total_available_rat_count = sum(
    item_name_to_rat_count[i] for i in
    location_name_to_progression_item_name.values()
        if i in item_name_to_rat_count
)

location_name_groups: dict[str, set[str]] = {
    "Landmarks": set(),
    "Fillers": set(),
    "Zone Bosses": set(),
    "Sewer Landmarks": set(),
    "Sewer Fillers": set(),
    "Cool World Landmarks": set(),
    "Cool World Fillers": set(),
    "Space Landmarks": set(),
    "Space Fillers": set(),
    "Optional Bosses": set(),
    "Optional Fillers": set(),
}

def _visit_for_items(group_name: str, req: AutopelagoGameRequirement):
    if "item" in req:
        req: AutopelagoItemRequirement
        item_name_groups[group_name].add(item_key_to_name[req["item"]])
    elif "all" in req:
        req: AutopelagoAllRequirement
        for sub_req in req["all"]:
            _visit_for_items(group_name, sub_req)
    elif "any" in req:
        req: AutopelagoAnyRequirement
        for sub_req in req["any"]:
            _visit_for_items(group_name, sub_req)
    elif "any_two" in req:
        req: AutopelagoAnyTwoRequirement
        for sub_req in req["any_two"]:
            _visit_for_items(group_name, sub_req)


q: deque[tuple[str, AutopelagoRegionDefinition | None, AutopelagoRegionDefinition]] = deque()
q.append(("Sewer", None, autopelago_regions["before_basketball"]))
while q:
    prev_region_from_q: AutopelagoRegionDefinition
    curr_region_from_q: AutopelagoRegionDefinition
    zone, prev_region_from_q, curr_region_from_q = q.popleft()
    _visit_for_items(f"{zone} Progression", curr_region_from_q.requires)
    region_type = "Landmarks" if curr_region_from_q.landmark else "Fillers"
    if curr_region_from_q.key == "captured_goldfish":
        region_type = "Zone Bosses"
        next_zone = "Cool World"
    elif curr_region_from_q.key == "secret_cache":
        region_type = "Zone Bosses"
        next_zone = "Space"
    elif curr_region_from_q.key == "snakes_on_a_planet":
        # nothing else needed beyond here
        continue
    else:
        next_zone = zone

    next_regions = [autopelago_regions[e] for e in curr_region_from_q.exits]
    for loc in curr_region_from_q.locations:
        location_name_groups[region_type].add(loc)
        if region_type != "Zone Bosses":
            location_name_groups[f"{zone} {region_type}"].add(loc)

        if not next_regions:
            location_name_groups["Optional Bosses"].add(loc)
            for prev_loc in prev_region_from_q.locations:
                location_name_groups["Optional Fillers"].add(prev_loc)

    if next_zone:
        for next_region in next_regions:
            q.append((next_zone, curr_region_from_q, next_region))
