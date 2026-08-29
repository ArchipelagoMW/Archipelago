"""
Logic Extractor designed for "Randomizer 4".
Place a Randomizer 4 compatible "Resources" folder next to this script, then run the script, to create AP data.
"""
import os
import json
import typing
import ast

import jinja2

from ast import unparse

from Utils import get_text_between


def put_digits_at_end(text: str) -> str:
    for x in range(len(text)):
        if text[0].isdigit():
            text = text[1:] + text[0]
        else:
            break
    return text


def hk_loads(file: str) -> typing.Any:
    with open(file, encoding="utf-8-sig") as f:
        data = f.read()
    new_data = []
    for row in data.split("\n"):
        if not row.strip().startswith(r"//"):
            new_data.append(row)
    return json.loads("\n".join(new_data))


def hk_convert(text: str) -> str:
    parts = text.replace("(", "( ").replace(")", " )").replace(">", " > ").replace("=", "==").split()
    new_parts = []
    for part in parts:
        part = put_digits_at_end(part)

        if part in items or part in effect_names or part in event_names or part in connectors:
            new_parts.append(f"\"{part}\"")
        else:
            new_parts.append(part)
    text = " ".join(new_parts)
    result = ""
    parts = text.split("$StartLocation[")
    for i, part in enumerate(parts[:-1]):
        result += part + "StartLocation[\""
        parts[i+1] = parts[i+1].replace("]", "\"]", 1)

    text = result + parts[-1]

    result = ""
    parts = text.split("COMBAT[")
    for i, part in enumerate(parts[:-1]):
        result += part + "COMBAT[\""
        parts[i+1] = parts[i+1].replace("]", "\"]", 1)

    text = result + parts[-1]
    return text.replace("+", "and").replace("|", "or").replace("$", "").strip()


class Absorber(ast.NodeTransformer):
    additional_truths = set()
    additional_falses = set()

    def __init__(self, truth_values, false_values):
        self.truth_values = truth_values
        self.truth_values |= {"True", "None", "ANY", "ITEMRANDO"}
        self.false_values = false_values
        self.false_values |= {"False", "NONE"}

        super(Absorber, self).__init__()

    def generic_visit(self, node: ast.AST) -> ast.AST:
        # Need to call super() in any case to visit child nodes of the current one.
        node = super().generic_visit(node)
        return node

    def visit_BoolOp(self, node: ast.BoolOp) -> ast.AST:
        if type(node.op) == ast.And:
            if self.is_always_true(node.values[0]):
                return self.visit(node.values[1])
            if self.is_always_true(node.values[1]):
                return self.visit(node.values[0])
            if self.is_always_false(node.values[0]) or self.is_always_false(node.values[1]):
                return ast.Constant(False, ctx=ast.Load())
        elif type(node.op) == ast.Or:
            if self.is_always_true(node.values[0]) or self.is_always_true(node.values[1]):
                return ast.Constant(True, ctx=ast.Load())
            if self.is_always_false(node.values[0]):
                return self.visit(node.values[1])
            if self.is_always_false(node.values[1]):
                return self.visit(node.values[0])
        return self.generic_visit(node)

    def visit_Name(self, node: ast.Name) -> ast.AST:
        if node.id in self.truth_values:
            return ast.Constant(True, ctx=node.ctx)
        if node.id in self.false_values:
            return ast.Constant(False, ctx=node.ctx)
        if node.id in logic_options:
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()), attr='_hk_option', ctx=ast.Load()),
                args=[ast.Name(id="player", ctx=ast.Load()), ast.Constant(value=logic_options[node.id])], keywords=[])
        if node.id in macros:
            return macros[node.id].body
        if node.id in region_names:
            raise Exception(f"Should be event {node.id}")
        # You'd think this means reach Scene/Region of that name, but is actually waypoint/event
        # if node.id in region_names:
        #     return ast.Call(
        #         func=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()), attr='can_reach', ctx=ast.Load()),
        #         args=[ast.Constant(value=node.id),
        #               ast.Constant(value="Region"),
        #               ast.Name(id="player", ctx=ast.Load())],
        #         keywords=[])
        return self.generic_visit(node)

    def visit_Constant(self, node: ast.Constant) -> ast.AST:
        if type(node.value) == str:
            logic_items.add(node.value)
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()), attr='count', ctx=ast.Load()),
                args=[ast.Constant(value=node.value), ast.Name(id="player", ctx=ast.Load())], keywords=[])

        return node

    def visit_Subscript(self, node: ast.Subscript) -> ast.AST:
        if node.value.id == "NotchCost":
            notches = [ast.Constant(value=notch.value - 1) for notch in node.slice.elts]  # apparently 1-indexed
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()), attr='_hk_notches', ctx=ast.Load()),
                args=[ast.Name(id="player", ctx=ast.Load())] + notches, keywords=[])
        elif node.value.id == "StartLocation":
            node.slice.value = node.slice.value.replace(" ", "_").lower()
            if node.slice.value in removed_starts:
                return ast.Constant(False, ctx=node.ctx)
            return ast.Call(
                func=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()), attr='_hk_start', ctx=ast.Load()),
                args=[ast.Name(id="player", ctx=ast.Load()), node.slice], keywords=[])
        elif node.value.id == "COMBAT":
            return macros[unparse(node)].body
        else:
            name = unparse(node)
            if name in self.additional_truths:
                return ast.Constant(True, ctx=ast.Load())
            elif name in self.additional_falses:
                return ast.Constant(False, ctx=ast.Load())
            elif name in macros:
                # macro such as "COMBAT[White_Palace_Arenas]"
                return macros[name].body
            else:
                # assume Entrance
                entrance = unparse(node)
                assert entrance in connectors, entrance
                return ast.Call(
                    func=ast.Attribute(value=ast.Name(id='state', ctx=ast.Load()), attr='can_reach', ctx=ast.Load()),
                    args=[ast.Constant(value=entrance),
                          ast.Constant(value="Entrance"),
                          ast.Name(id="player", ctx=ast.Load())],
                    keywords=[])
        return node

    def is_always_true(self, node):
        if isinstance(node, ast.Name) and (node.id in self.truth_values or node.id in self.additional_truths):
            return True
        if isinstance(node, ast.Subscript) and unparse(node) in self.additional_truths:
            return True

    def is_always_false(self, node):
        if isinstance(node, ast.Name) and (node.id in self.false_values or node.id in self.additional_falses):
            return True
        if isinstance(node, ast.Subscript) and unparse(node) in self.additional_falses:
            return True


def get_parser(truths: typing.Set[str] = frozenset(), falses: typing.Set[str] = frozenset()):
    return Absorber(truths, falses)


def ast_parse(parser, rule_text, truths: typing.Set[str] = frozenset(), falses: typing.Set[str] = frozenset()):
    tree = ast.parse(hk_convert(rule_text), mode='eval')
    parser.additional_truths = truths
    parser.additional_falses = falses
    new_tree = parser.visit(tree)
    parser.additional_truths = set()
    parser.additional_truths = set()
    return new_tree


world_folder = os.path.dirname(__file__)

resources_source = os.path.join(world_folder, "Resources")
data_folder = os.path.join(resources_source, "Data")
logic_folder = os.path.join(resources_source, "Logic")
logic_options: typing.Dict[str, str] = hk_loads(os.path.join(data_folder, "logic_settings.json"))
for logic_key, logic_value in logic_options.items():
    logic_options[logic_key] = logic_value.split(".", 1)[-1]

vanilla_cost_data: typing.Dict[str, typing.Dict[str, typing.Any]] = hk_loads(os.path.join(data_folder, "costs.json"))
vanilla_location_costs = {
    key: {
        value["term"]: int(value["amount"])
    }
    for key, value in vanilla_cost_data.items()
    if value["amount"] > 0 and value["term"] == "GEO"
}

salubra_geo_costs_by_charm_count = {
    5: 120,
    10: 500,
    18: 900,
    25: 1400,
    40: 800
}

# Can't extract this data, so supply it ourselves.  Source: the wiki
vanilla_shop_costs = {
    ('Sly', 'Simple_Key'): [{'GEO': 950}],
    ('Sly', 'Rancid_Egg'): [{'GEO': 60}],
    ('Sly', 'Lumafly_Lantern'): [{'GEO': 1800}],
    ('Sly', 'Gathering_Swarm'): [{'GEO': 300}],
    ('Sly', 'Stalwart_Shell'): [{'GEO': 200}],
    ('Sly', 'Mask_Shard'): [
        {'GEO': 150},
        {'GEO': 500},
    ],
    ('Sly', 'Vessel_Fragment'): [{'GEO': 550}],
    ('Sly_(Key)', 'Heavy_Blow'): [{'GEO': 350}],
    ('Sly_(Key)', 'Elegant_Key'): [{'GEO': 800}],
    ('Sly_(Key)', 'Mask_Shard'): [
        {'GEO': 800},
        {'GEO': 1500},
    ],
    ('Sly_(Key)', 'Vessel_Fragment'): [{'GEO': 900}],
    ('Sly_(Key)', 'Sprintmaster'): [{'GEO': 400}],

    ('Iselda', 'Wayward_Compass'): [{'GEO': 220}],
    ('Iselda', 'Quill'): [{'GEO': 120}],

    ('Salubra', 'Lifeblood_Heart'): [{'GEO': 250}],
    ('Salubra', 'Longnail'): [{'GEO': 300}],
    ('Salubra', 'Steady_Body'): [{'GEO': 120}],
    ('Salubra', 'Shaman_Stone'): [{'GEO': 220}],
    ('Salubra', 'Quick_Focus'): [{'GEO': 800}],

    ('Leg_Eater', 'Fragile_Heart'): [{'GEO': 350}],
    ('Leg_Eater', 'Fragile_Greed'): [{'GEO': 250}],
    ('Leg_Eater', 'Fragile_Strength'): [{'GEO': 600}],
}
extra_pool_options: typing.List[typing.Dict[str, typing.Any]] = hk_loads(os.path.join(data_folder, "pools.json"))
pool_options: typing.Dict[str, typing.Tuple[typing.List[str], typing.List[str]]] = {}
for option in extra_pool_options:
    if option["Path"] != "False":
        items: typing.List[str] = []
        locations: typing.List[str] = []
        for pairing in option["Vanilla"]:
            items.append(pairing["item"])
            location_name = pairing["location"]
            item_costs = pairing.get("costs", [])
            if item_costs:
                if any(cost_entry["term"] == "CHARMS" for cost_entry in item_costs):
                    location_name += "_(Requires_Charms)"
                #vanilla_shop_costs[pairing["location"], pairing["item"]] = \
                cost = {
                    entry["term"]: int(entry["amount"]) for entry in item_costs
                }
                # Rando4 doesn't include vanilla geo costs for Salubra charms, so dirty hardcode here.
                if 'CHARMS' in cost:
                    geo = salubra_geo_costs_by_charm_count.get(cost['CHARMS'])
                    if geo:
                        cost['GEO'] = geo

                key = (pairing["location"], pairing["item"])
                vanilla_shop_costs.setdefault(key, []).append(cost)

            locations.append(location_name)
        if option["Path"]:
            # basename carries over from prior entry if no Path given
            basename = option["Path"].split(".", 1)[-1]
        if not basename.startswith("Randomize"):
            basename = "Randomize" + basename
        assert len(items) == len(locations)
        if items:  # skip empty pools
            if basename in pool_options:
                pool_options[basename] = pool_options[basename][0]+items, pool_options[basename][1]+locations
            else:
                pool_options[basename] = items, locations
del extra_pool_options

# reverse all the vanilla shop costs (really, this is just for Salubra).
# When we use these later, we pop off the end of the list so this ensures they are still sorted.
vanilla_shop_costs = {
    k: list(reversed(v)) for k, v in vanilla_shop_costs.items()
}

# items
items: typing.Dict[str, typing.Dict] = hk_loads(os.path.join(data_folder, "items.json"))
logic_items: typing.Set[str] = set()
for item_name in sorted(items):
    item = items[item_name]
    items[item_name] = item["Pool"]
items: typing.Dict[str, str]

extra_item_data: typing.List[typing.Dict[str, typing.Any]] = hk_loads(os.path.join(logic_folder, "items.json"))
item_effects: typing.Dict[str, typing.Dict[str, int]] = {}
effect_names: typing.Set[str] = set()
for item_data in extra_item_data:
    if "FalseItem" in item_data:
        item_data = item_data["FalseItem"]
    effects = []
    if "Effect" in item_data:
        effects = [item_data["Effect"]]
    elif "Effects" in item_data:
        effects = item_data["Effects"]
    for effect in effects:
        effect_names.add(effect["Term"])
    effects = {effect["Term"]: effect["Value"] for effect in effects if
               effect["Term"] != item_data["Name"] and effect["Term"] not in {"GEO",
                                                                              "HALLOWNESTSEALS",
                                                                              "WANDERERSJOURNALS",
                                                                              'HALLOWNESTSEALS',
                                                                              "KINGSIDOLS",
                                                                              'ARCANEEGGS',
                                                                              'MAPS'
                                                                              }}

    if effects:
        item_effects[item_data["Name"]] = effects

del extra_item_data

# locations
original_locations: typing.Dict[str, typing.Dict[str, typing.Any]] = hk_loads(os.path.join(data_folder, "locations.json"))
del(original_locations["Start"])  # Starting Inventory works different in AP

locations: typing.List[str] = []
locations_in_regions: typing.Dict[str, typing.List[str]] = {}
location_to_region_lookup: typing.Dict[str, str] = {}
multi_locations: typing.Dict[str, typing.List[str]] = {}
for location_name, location_data in original_locations.items():
    region_name = location_data["SceneName"]
    if location_data["FlexibleCount"]:
        location_names = [f"{location_name}_{count}" for count in range(1, 17)]
        multi_locations[location_name] = location_names
    else:
        location_names = [location_name]

    location_to_region_lookup.update({name: region_name for name in location_names})
    locations_in_regions.setdefault(region_name, []).extend(location_names)
    locations.extend(location_names)
del original_locations

# regions
region_names: typing.Set[str] = set(hk_loads(os.path.join(data_folder, "rooms.json")))
connectors_data: typing.Dict[str, typing.Dict[str, typing.Any]] = hk_loads(os.path.join(data_folder, "transitions.json"))
connectors_logic: typing.List[typing.Dict[str, typing.Any]] = hk_loads(os.path.join(logic_folder, "transitions.json"))
exits: typing.Dict[str, typing.List[str]] = {}
connectors: typing.Dict[str, str] = {}
one_ways: typing.Set[str] = set()
for connector_name, connector_data in connectors_data.items():
    exits.setdefault(connector_data["SceneName"], []).append(connector_name)
    connectors[connector_name] = connector_data["VanillaTarget"]
    if connector_data["Sides"] != "Both":
        one_ways.add(connector_name)
del connectors_data

# starts
starts: typing.Dict[str, typing.Dict[str, typing.Any]] = hk_loads(os.path.join(data_folder, "starts.json"))

# only allow always valid starts for now
removed_starts: typing.Set[str] = {name.replace(" ", "_").lower() for name, data in starts.items() if
                                   name != "King's Pass"}

starts: typing.Dict[str, str] = {
    name.replace(" ", "_").lower(): data["sceneName"] for name, data in starts.items() if name == "King's Pass"}

# logic
falses = {"MAPAREARANDO", "FULLAREARANDO"}
macros: typing.Dict[str, ast.AST] = {
}
parser = get_parser(set(), falses)
extra_macros: typing.Dict[str, str] = hk_loads(os.path.join(logic_folder, "macros.json"))
raw_location_rules: typing.List[typing.Dict[str, str]] = hk_loads(os.path.join(logic_folder, "locations.json"))
events: typing.List[typing.Dict[str, typing.Any]] = hk_loads(os.path.join(logic_folder, "waypoints.json"))

event_names: typing.Set[str] = {event["name"] for event in events}

for macro_name, rule in extra_macros.items():
    if macro_name not in macros:
        macro_name = put_digits_at_end(macro_name)
        if macro_name in items or macro_name in effect_names:
            continue
        assert macro_name not in events
        rule = ast_parse(parser, rule)
        macros[macro_name] = rule
        if macro_name.startswith("COMBAT["):
            name = get_text_between(macro_name, "COMBAT[", "]")
            if not "'" in name:
                macros[f"COMBAT['{name}']"] = rule
            macros[f'COMBAT["{name}"]'] = rule

location_rules: typing.Dict[str, str] = {}
for loc_obj in raw_location_rules:
    loc_name = loc_obj["name"]
    rule = loc_obj["logic"]
    if rule != "ANY":
        rule = ast_parse(parser, rule)
        location_rules[loc_name] = unparse(rule)
location_rules["Salubra_(Requires_Charms)"] = location_rules["Salubra"]

connectors_rules: typing.Dict[str, str] = {}
for connector_obj in connectors_logic:
    name = connector_obj["Name"]
    rule = connector_obj["logic"]
    rule = ast_parse(parser, rule)
    rule = unparse(rule)
    if rule != "True":
        connectors_rules[name] = rule

event_rules: typing.Dict[str, str] = {}
for event in events:
    rule = ast_parse(parser, event["logic"])
    rule = unparse(rule)
    if rule != "True":
        event_rules[event["name"]] = rule


event_rules.update(connectors_rules)
connectors_rules = {}


# Apply some final fixes
item_effects.update({
    'Left_Mothwing_Cloak': {'LEFTDASH': 1},
    'Right_Mothwing_Cloak': {'RIGHTDASH': 1},
})
names = sorted({"logic_options", "starts", "pool_options", "locations", "multi_locations", "location_to_region_lookup",
                "event_names", "item_effects", "items", "logic_items", "region_names",
                "exits", "connectors", "one_ways", "vanilla_shop_costs", "vanilla_location_costs"})
warning = "# This module is written by Extractor.py, do not edit manually!.\n\n"
with open(os.path.join(os.path.dirname(__file__), "ExtractedData.py"), "wt") as py:
    py.write(warning)
    for name in names:
        var = globals()[name]
        if type(var) == set:
            # sort so a regen doesn't cause a file change every time
            var = sorted(var)
            var = "{"+str(var)[1:-1]+"}"
        py.write(f"{name} = {var}\n")


template_env: jinja2.Environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader([os.path.join(os.path.dirname(__file__), "templates")]))
rules_template = template_env.get_template("RulesTemplate.pyt")
rules = rules_template.render(location_rules=location_rules, one_ways=one_ways, connectors_rules=connectors_rules,
                              event_rules=event_rules)

with open("GeneratedRules.py", "wt") as py:
    py.write(warning)
    py.write(rules)
