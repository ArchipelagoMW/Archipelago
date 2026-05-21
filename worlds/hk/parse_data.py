from collections import defaultdict
from typing import Any, cast

from .data import ids, item_effects, location_data, option_data, region_structure, trando_data

__all__ = [
    "datapackage_item_groups",
    "datapackage_items",
    "datapackage_location_groups",
    "datapackage_locations",
    "effects_items_by_term",
    "effects_non_prog",
    "effects_prog_lookup",
    "effects_terms_by_item",
    "hk_locations",
    "hk_regions",
    "metadata_location_areas",
    "metadata_location_multi",
    "options_logic_mappings",
    "options_pool_mappings",
    "shop_locations",
    "structure_locations",
    "structure_regions",
    "structure_transition_to_region_map",
    "trando_starts",
    "trando_transitions",
    "vanilla_location_costs",
    "vanilla_shop_costs",
]

datapackage_items = ids.item_name_to_id
datapackage_locations = ids.location_name_to_id

effects_terms_by_item = item_effects.affected_terms_by_item
effects_items_by_term = item_effects.affecting_items_by_term
effects_non_prog = item_effects.non_progression_items
effects_prog_lookup = item_effects.progression_effect_lookup

metadata_location_areas = location_data.locations
metadata_location_multi = location_data.multi_locations

options_logic_mappings = option_data.logic_options
options_pool_mappings = option_data.pool_options

structure_locations = region_structure.locations
structure_regions = region_structure.regions
structure_transition_to_region_map = region_structure.transition_to_region_map

trando_starts = trando_data.starts
trando_transitions = trando_data.transitions

# TODO: loop through additional sources

shop_locations = metadata_location_multi
event_locations = [location["name"] for location in structure_locations if location["is_event"]
                   and location["name"] not in ("Can_Warp_To_DG_Bench", "Can_Warp_To_Bench")]
vanilla_cost_data = [pair for option in options_pool_mappings.values() for pair in option["vanilla"] if pair["costs"]]
vanilla_location_costs = {
    pair["location"]: {cost["term"]: cost["amount"] for cost in pair["costs"]}
    for pair in vanilla_cost_data
    if pair["location"] not in metadata_location_multi
    }
vanilla_shop_costs = defaultdict(list)
for i in vanilla_cost_data:
    if i["location"] not in metadata_location_multi:
        continue
    costs = {cost["term"]: cost["amount"] for cost in i["costs"]}
    vanilla_shop_costs[(i["location"], i["item"])].append(costs)

hk_regions = [
    region for region in cast(list[dict[str, Any]], structure_regions)
    if not region["name"].startswith("$") and not region["name"] == "Bench-Godhome_Roof"
]
hk_locations = cast(list[dict[str, Any]], list(structure_locations))


# Datapackage Groups

# strip "Randomize" from pool options and use their names as group names
datapackage_item_groups = {
    key[9:]: set(value["randomized"]["items"])
    for key, value in options_pool_mappings.items()

    # TODO dynamically exclude these if possible
    if key not in ("RandomizeSwim", "RandomizeFocus")
    }

# override to remove world sense
datapackage_item_groups["Dreamers"] = set(effects_items_by_term["DREAMER"])

datapackage_item_groups["CDash"] = set(effects_items_by_term["LEFTSUPERDASH"] + effects_items_by_term["RIGHTSUPERDASH"])
datapackage_item_groups["Claw"] = set(effects_items_by_term["LEFTCLAW"] + effects_items_by_term["RIGHTCLAW"])
datapackage_item_groups["Cloak"] = set(effects_items_by_term["LEFTDASH"] + effects_items_by_term["RIGHTDASH"])
datapackage_item_groups["Dive"] = set(effects_items_by_term["QUAKE"])
datapackage_item_groups["Fireball"] = set(effects_items_by_term["FIREBALL"])
datapackage_item_groups["Scream"] = set(effects_items_by_term["SCREAM"])
datapackage_item_groups["Grimmchild"] = set(effects_items_by_term["Grimmchild"])
datapackage_item_groups["Charms"] |= datapackage_item_groups["Grimmchild"]
# Grimmchild1 isn't in the options_pool_mappings for charms
datapackage_item_groups["WhiteFragments"] = set(effects_items_by_term["WHITEFRAGMENT"])
datapackage_item_groups["DreamNails"] = set(effects_items_by_term["DREAMNAIL"])

# TODO
# datapackage_item_groups["PalaceLore"] = set(effects_items_by_term["DREAMER"])
# datapackage_item_groups["PalaceTotem"] = set(effects_items_by_term["DREAMER"])

datapackage_item_groups["Horizontal"] = datapackage_item_groups["Cloak"] | datapackage_item_groups["CDash"]
datapackage_item_groups["Vertical"] = datapackage_item_groups["Claw"] | {"Monarch_Wings"}
# add split movement to skills
datapackage_item_groups["Skills"] |= datapackage_item_groups["Vertical"] | datapackage_item_groups["Horizontal"]

datapackage_item_groups["SoulTotems"].add("Soul_Refill")

datapackage_location_groups = defaultdict(set)

for name, location in metadata_location_areas.items():
    if name in shop_locations:
        for i in range(1, 17):
            shop_name = f"{name}_{i}"
            datapackage_location_groups[location["map_area"]].add(shop_name)
            datapackage_location_groups[location["titled_area"]].add(shop_name)
        continue

    datapackage_location_groups[location["map_area"]].add(name)
    datapackage_location_groups[location["titled_area"]].add(name)
