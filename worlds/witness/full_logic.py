"""
Parses the WitnessLogic.txt logic file into useful data structures
"""

import pathlib
import os
pathlib.Path(__file__).parent.resolve()


ALL_ITEMS = set()
ALL_TRAPS = set()
ALL_BOOSTS = set()
EVENT_PANELS_FROM_REGIONS = set()
EVENT_PANELS_FROM_PANELS = set()
ALL_REGIONS_BY_NAME = dict()
CHECKS_DEPENDENT_BY_HEX = dict()
CHECKS_BY_HEX = dict()
CHECKS_BY_NAME = dict()
ORIGINAL_EVENT_PANELS = set()
NECESSARY_EVENT_PANELS = set()
EVENT_ITEM_PAIRS = dict()
ALWAYS_EVENT_HEX_CODES = set()
EVENT_ITEM_NAMES = {
    "0x01A0F": "Keep Laser Panel (Hedge Mazes) Activates",
    "0x09D9B": "Monastery Overhead Doors Open",
    "0x193A6": "Monastery Laser Panel Activates",
    "0x00037": "Monastery Branch Panels Activate",
    "0x0A079": "Access to Bunker Laser",
    "0x0A3B5": "Door to Tutorial Discard Opens",
    "0x01D3F": "Keep Laser Panel (Pressure Plates) Activates",
    "0x09F7F": "Mountain Access",
    "0x0367C": "Quarry Laser Mill Requirement Met",
    "0x009A1": "Swamp Rotating Bridge Near Side",
    "0x00006": "Swamp Cyan Water Drains",
    "0x00990": "Swamp Broken Shapers 1 Activates",
    "0x0A8DC": "Lower Avoid 6 Activates",
    "0x0000A": "Swamp More Rotated Shapers 1 Access",
    "0x09ED8": "Inside Mountain Second Layer Both Light Bridges Solved",
    "0x0A3D0": "Quarry Laser Boathouse Requirement Met",
    "0x00596": "Swamp Red Water Drains",
}


ALWAYS_EVENTS_BY_NAME = {
    "Symmetry Laser Activation": "0x0360D",
    "Desert Laser Activation": "0x03608",
    "Desert Laser Redirection": "0x09F98",
    "Quarry Laser Activation": "0x03612",
    "Shadows Laser Activation": "0x19650",
    "Keep Laser Hedges Activation": "0x0360E",
    "Keep Laser Pressure Plates Activation": "0x03317",
    "Monastery Laser Activation": "0x17CA4",
    "Town Laser Activation": "0x032F5",
    "Jungle Laser Activation": "0x03616",
    "Bunker Laser Activation": "0x09DE0",
    "Swamp Laser Activation": "0x03615",
    "Treehouse Laser Activation": "0x03613",
    "Shipwreck Video Pattern Knowledge": "0x03535",
    "Mountain Video Pattern Knowledge": "0x03542",
    "Desert Video Pattern Knowledge": "0x0339E",
    "Tutorial Video Pattern Knowledge": "0x03481",
    "Jungle Video Pattern Knowledge": "0x03702",
    "Theater Walkway Video Pattern Knowledge": "0x2FAF6"
}


def parse_items():
    """
    Parses currently defined items from WitnessItems.txt
    """

    path = os.path.join(os.path.dirname(__file__), "WitnessItems.txt")
    file = open(path, "r", encoding="utf-8")

    current_set = ALL_ITEMS

    for line in file.readlines():
        line = line.strip()

        if line == "Progression:":
            current_set = ALL_ITEMS
            continue
        if line == "Boosts:":
            current_set = ALL_BOOSTS
            continue
        if line == "Traps:":
            current_set = ALL_TRAPS
            continue
        if line == "":
            continue

        line_split = line.split(" - ")

        current_set.add((line_split[1], int(line_split[0])))



def reduce_requirement_within_region(check_obj):
    """
    Panels in this game often only turn on when other panels are solved.
    Those other panels may have different item requirements.
    It would be slow to recursively check solvability each time.
    This is why we reduce the item dependencies within the region.
    Panels outside of the same region will still be checked manually.
    """

    if check_obj["requirement"]["panels"] == frozenset({frozenset()}):
        return check_obj["requirement"]["items"]

    all_options = set()

    these_items = check_obj["requirement"]["items"]

    for option in check_obj["requirement"]["panels"]:
        dependent_items_for_option = frozenset({frozenset()})

        for panel_within_option in option:
            new_items = set()
            depend_obj = CHECKS_DEPENDENT_BY_HEX.get(panel_within_option)
            if panel_within_option in {"7 Lasers", "11 Lasers"}:
                new_items = frozenset({frozenset([panel_within_option])})
            elif depend_obj["region"]["name"] != check_obj["region"]["name"]:
                new_items = frozenset({frozenset([panel_within_option])})
                EVENT_PANELS_FROM_PANELS.add(panel_within_option)
            else:
                new_items = reduce_requirement_within_region(depend_obj)

            updated_items = set()

            for items_option in dependent_items_for_option:
                for items_option2 in new_items:
                    updated_items.add(items_option.union(items_option2))

            dependent_items_for_option = updated_items

        for items_option in these_items:
            for dependentItem in dependent_items_for_option:
                all_options.add(items_option.union(dependentItem))

    return frozenset(all_options)


def parse_lambda(lambda_string):
    """
    Turns a lambda String literal like this: a | b & c
    into a set of sets like this: {{a}, {b, c}}
    The lambda has to be in DNF.
    """
    if lambda_string == "True":
        return frozenset([frozenset()])
    split_ands = set(lambda_string.split(" | "))
    lambda_set = frozenset({frozenset(a.split(" & ")) for a in split_ands})

    return lambda_set


def define_new_region(region_string):
    """
    Returns a region object by parsing a line in the logic file
    """

    region_string = region_string[:-1]
    line_split = region_string.split(" - ")

    region_name_full = line_split.pop(0)

    region_name_split = region_name_full.split(" (")

    region_name = region_name_split[0]
    region_name_simple = region_name_split[1][:-1]

    options = set()

    for _ in range(len(line_split) // 2):
        connected_region = line_split.pop(0)
        corresponding_lambda = line_split.pop(0)

        for panel_option in parse_lambda(corresponding_lambda):
            for panel_with_option in panel_option:
                EVENT_PANELS_FROM_REGIONS.add(panel_with_option)

        options.add((connected_region, parse_lambda(corresponding_lambda)))

    region_obj = {
        "name": region_name,
        "shortName": region_name_simple,
        "connections": options,
        "panels": set()
    }
    return region_obj


def read_logic_file():
    """
    Reads the logic file and does the initial population of data structures.
    """
    path = os.path.join(os.path.dirname(__file__), "WitnessLogic.txt")
    file = open(path, "r", encoding="utf-8")

    current_region = ""

    discard_ids = 0
    normal_panel_ids = 0
    vault_ids = 0
    laser_ids = 0

    for line in file.readlines():
        line = line.strip()

        if line == "":
            continue

        if line[0] != "0":
            current_region = define_new_region(line)
            ALL_REGIONS_BY_NAME[current_region["name"]] = current_region
            continue

        line_split = line.split(" - ")

        check_name_full = line_split.pop(0)

        check_hex = check_name_full[0:7]
        check_name = check_name_full[9:-1]

        required_panel_lambda = line_split.pop(0)
        required_item_lambda = line_split.pop(0)

        location_id = 0
        location_type = ""

        laser_names = {
            "Laser",
            "Laser Hedges",
            "Laser Pressure Plates",
            "Desert Laser Redirect"
        }
        is_vault_or_video = "Vault" in check_name or "Video" in check_name

        if "Discard" in check_name:
            location_type = "Discard"
            location_id = discard_ids
            discard_ids += 1
        elif is_vault_or_video or check_name == "Tutorial Gate Close":
            location_type = "Vault"
            location_id = vault_ids
            vault_ids += 1
        elif check_name in laser_names:
            location_type = "Laser"
            location_id = laser_ids
            laser_ids += 1
        else:
            location_type = "General"
            location_id = normal_panel_ids
            normal_panel_ids += 1

        required_items = parse_lambda(required_item_lambda)
        items_actually_in_the_game = {item[0] for item in ALL_ITEMS}
        required_items = frozenset(
            subset.intersection(items_actually_in_the_game) for subset in required_items
        )

        requirement = {
            "panels": parse_lambda(required_panel_lambda),
            "items": required_items
        }

        CHECKS_DEPENDENT_BY_HEX[check_hex] = {
            "checkName": current_region["shortName"] + " " + check_name,
            "checkHex": check_hex,
            "region": current_region,
            "requirement": requirement,
            "idOffset": location_id,
            "panelType": location_type
        }

        current_region["panels"].add(check_hex)


def make_dependency_reduced_checklist():
    """
    Turns dependent check set into semi-independent check set
    """

    for check_hex, check in CHECKS_DEPENDENT_BY_HEX.items():
        independent_requirement = reduce_requirement_within_region(check)

        new_check = {
            "checkName": check["checkName"],
            "checkHex": check["checkHex"],
            "region": check["region"],
            "requirement": independent_requirement,
            "idOffset": check["idOffset"],
            "panelType": check["panelType"]
        }

        CHECKS_BY_HEX[check_hex] = new_check
        CHECKS_BY_NAME[new_check["checkName"]] = new_check


def make_event_item_pair(panel):
    """
    Makes a pair of an event panel and its event item
    """
    name = CHECKS_BY_HEX[panel]["checkName"] + " Solved"
    pair = (name, EVENT_ITEM_NAMES[panel])
    return pair


def make_event_panel_lists():
    """
    Special event panel data structures
    """

    ORIGINAL_EVENT_PANELS.update(EVENT_PANELS_FROM_PANELS)
    ORIGINAL_EVENT_PANELS.update(EVENT_PANELS_FROM_REGIONS)
    NECESSARY_EVENT_PANELS.update(EVENT_PANELS_FROM_PANELS)

    for panel in EVENT_PANELS_FROM_REGIONS:
        for region_name, region in ALL_REGIONS_BY_NAME.items():
            for connection in region["connections"]:
                connected_region_name = connection[0]
                if connected_region_name not in ALL_REGIONS_BY_NAME:
                    continue
                if region_name == "Boat" or connected_region_name == "Boat":
                    continue
                connected_region = ALL_REGIONS_BY_NAME[connected_region_name]
                if not any([panel in option for option in connection[1]]):
                    continue
                if panel not in region["panels"] | connected_region["panels"]:
                    NECESSARY_EVENT_PANELS.add(panel)

    for always_event_item, always_event_hex in ALWAYS_EVENTS_BY_NAME.items():
        ALWAYS_EVENT_HEX_CODES.add(always_event_hex)
        NECESSARY_EVENT_PANELS.add(always_event_hex)
        EVENT_ITEM_NAMES[always_event_hex] = always_event_item

    for panel in NECESSARY_EVENT_PANELS:
        pair = make_event_item_pair(panel)
        EVENT_ITEM_PAIRS[pair[0]] = pair[1]

parse_items()
read_logic_file()
make_dependency_reduced_checklist()
make_event_panel_lists()
