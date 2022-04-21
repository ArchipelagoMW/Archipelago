"""
Parses the WitnessLogic.txt logic file into useful data structures
"""

import pathlib
import os
from BaseClasses import MultiWorld

from worlds.witness.Options import is_option_enabled
pathlib.Path(__file__).parent.resolve()


class ParsedWitnessLogic():
    """WITNESS LOGIC CLASS"""

    def parse_items(self):
        """
        Parses currently defined items from WitnessItems.txt
        """

        path = os.path.join(os.path.dirname(__file__), "WitnessItems.txt")
        file = open(path, "r", encoding="utf-8")

        current_set = self.ALL_ITEMS

        for line in file.readlines():
            line = line.strip()

            if line == "Progression:":
                current_set = self.ALL_ITEMS
                continue
            if line == "Boosts:":
                current_set = self.ALL_BOOSTS
                continue
            if line == "Traps:":
                current_set = self.ALL_TRAPS
                continue
            if line == "":
                continue

            line_split = line.split(" - ")

            #TODO: Setting
            if line_split[1] == "Squares":
                continue

            current_set.add((line_split[1], int(line_split[0])))

    def reduce_req_within_region(self, check_obj):
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

            for option_panel in option:
                new_items = set()
                dep_obj = self.CHECKS_DEPENDENT_BY_HEX.get(option_panel)
                if option_panel in {"7 Lasers", "11 Lasers"}:
                    new_items = frozenset({frozenset([option_panel])})
                elif dep_obj["region"]["name"] != check_obj["region"]["name"]:
                    new_items = frozenset({frozenset([option_panel])})
                    self.EVENT_PANELS_FROM_PANELS.add(option_panel)
                else:
                    new_items = self.reduce_req_within_region(dep_obj)

                updated_items = set()

                for items_option in dependent_items_for_option:
                    for items_option2 in new_items:
                        updated_items.add(items_option.union(items_option2))

                dependent_items_for_option = updated_items

            for items_option in these_items:
                for dependentItem in dependent_items_for_option:
                    all_options.add(items_option.union(dependentItem))

        return frozenset(all_options)

    def parse_lambda(self, lambda_string):
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

    def make_single_adjustment(self, type, line):
        """Makes a single logic adjustment based on additional logic file"""

        if type == "Event Items":
            line_split = line.split(" - ")
            hex_set = line_split[1].split(",")

            for hex_code in hex_set:
                self.ALWAYS_EVENT_NAMES_BY_HEX[hex_code] = line_split[0]

            """
            Should probably do this differently...
            Events right now depend on a panel.
            That seems bad.
            """

            to_remove = set()

            for hex_code, event_name in self.ALWAYS_EVENT_NAMES_BY_HEX.items():
                if hex_code not in hex_set and event_name == line_split[0]:
                    to_remove.add(hex_code)
                    
            for remove in to_remove:
                del self.ALWAYS_EVENT_NAMES_BY_HEX[remove]

            return
        
        if type == "Requirement Changes":
            line_split = line.split(" - ")
            panel_obj = self.CHECKS_DEPENDENT_BY_HEX[line_split[0]]

            required_items = self.parse_lambda(line_split[2])
            items_actually_in_the_game = {item[0] for item in self.ALL_ITEMS}
            required_items = frozenset(
                subset.intersection(items_actually_in_the_game)
                for subset in required_items
            )

            requirement = {
                "panels": self.parse_lambda(line_split[1]),
                "items": required_items
            }

            panel_obj["requirement"] = requirement

            return

        if type == "Disabled Locations":
            self.COMPLETELY_DISABLED_CHECKS.add(line[:7])

    def define_new_region(self, region_string):
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

            for panel_option in self.parse_lambda(corresponding_lambda):
                for panel_with_option in panel_option:
                    self.EVENT_PANELS_FROM_REGIONS.add(panel_with_option)

            options.add(
                (connected_region, self.parse_lambda(corresponding_lambda))
            )

        region_obj = {
            "name": region_name,
            "shortName": region_name_simple,
            "connections": options,
            "panels": set()
        }
        return region_obj

    def read_logic_file(self):
        """
        Reads the logic file and does the initial population of data structures
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
                current_region = self.define_new_region(line)
                region_name = current_region["name"]
                self.ALL_REGIONS_BY_NAME[region_name] = current_region
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

            required_items = self.parse_lambda(required_item_lambda)
            items_actually_in_the_game = {item[0] for item in self.ALL_ITEMS}
            required_items = frozenset(
                subset.intersection(items_actually_in_the_game)
                for subset in required_items
            )

            requirement = {
                "panels": self.parse_lambda(required_panel_lambda),
                "items": required_items
            }

            self.CHECKS_DEPENDENT_BY_HEX[check_hex] = {
                "checkName": current_region["shortName"] + " " + check_name,
                "checkHex": check_hex,
                "region": current_region,
                "requirement": requirement,
                "idOffset": location_id,
                "panelType": location_type
            }

            current_region["panels"].add(check_hex)

    def make_options_adjustments(self, world, player):
        """Makes logic adjustments based on options"""
        adjustment_files_in_order = []

        if is_option_enabled(world, player, "challenge_victory"):
            self.VICTORY_LOCATION = "0x0356B"
        else:
            self.VICTORY_LOCATION = "0x3D9A9"

        self.COMPLETELY_DISABLED_CHECKS.add(
            self.VICTORY_LOCATION
        )

        if is_option_enabled(world, player, "disable_non_randomized_puzzles"):
            adjustment_files_in_order.append("Disable_Unrandomized.txt")

        for adjustment_file in adjustment_files_in_order:
            path = os.path.join(os.path.dirname(__file__), adjustment_file)
            file = open(path, "r", encoding="utf-8")

            current_adjustment_type = None

            for line in file.readlines():
                line = line.strip()
                
                if len(line) == 0:
                    continue
                
                if line[-1] == ":":
                    current_adjustment_type = line[:-1]
                    continue
                
                self.make_single_adjustment(current_adjustment_type, line)

    def make_dependency_reduced_checklist(self):
        """
        Turns dependent check set into semi-independent check set
        """

        for check_hex, check in self.CHECKS_DEPENDENT_BY_HEX.items():
            indep_requirement = self.reduce_req_within_region(check)

            new_check = {
                "checkName": check["checkName"],
                "checkHex": check["checkHex"],
                "region": check["region"],
                "requirement": indep_requirement,
                "idOffset": check["idOffset"],
                "panelType": check["panelType"]
            }

            self.CHECKS_BY_HEX[check_hex] = new_check
            self.CHECKS_BY_NAME[new_check["checkName"]] = new_check

    def make_event_item_pair(self, panel):
        """
        Makes a pair of an event panel and its event item
        """
        name = self.CHECKS_BY_HEX[panel]["checkName"] + " Solved"
        pair = (name, self.EVENT_ITEM_NAMES[panel])
        return pair

    def make_event_panel_lists(self):
        """
        Special event panel data structures
        """

        self.ALWAYS_EVENT_NAMES_BY_HEX[self.VICTORY_LOCATION] = "Victory"

        self.ORIGINAL_EVENT_PANELS.update(self.EVENT_PANELS_FROM_PANELS)
        self.ORIGINAL_EVENT_PANELS.update(self.EVENT_PANELS_FROM_REGIONS)
        self.NECESSARY_EVENT_PANELS.update(self.EVENT_PANELS_FROM_PANELS)

        for panel in self.EVENT_PANELS_FROM_REGIONS:
            for region_name, region in self.ALL_REGIONS_BY_NAME.items():
                for connection in region["connections"]:
                    connected_r = connection[0]
                    if connected_r not in self.ALL_REGIONS_BY_NAME:
                        continue
                    if region_name == "Boat" or connected_r == "Boat":
                        continue
                    connected_r = self.ALL_REGIONS_BY_NAME[connected_r]
                    if not any([panel in option for option in connection[1]]):
                        continue
                    if panel not in region["panels"] | connected_r["panels"]:
                        self.NECESSARY_EVENT_PANELS.add(panel)

        for always_hex, always_item in self.ALWAYS_EVENT_NAMES_BY_HEX.items():
            self.ALWAYS_EVENT_HEX_CODES.add(always_hex)
            self.NECESSARY_EVENT_PANELS.add(always_hex)
            self.EVENT_ITEM_NAMES[always_hex] = always_item

        for panel in self.NECESSARY_EVENT_PANELS:
            pair = self.make_event_item_pair(panel)
            self.EVENT_ITEM_PAIRS[pair[0]] = pair[1]

    def __init__(self):
        self.ALL_ITEMS = set()
        self.ALL_TRAPS = set()
        self.ALL_BOOSTS = set()
        self.EVENT_PANELS_FROM_REGIONS = set()
        self.EVENT_PANELS_FROM_PANELS = set()
        self.ALL_REGIONS_BY_NAME = dict()
        self.CHECKS_DEPENDENT_BY_HEX = dict()
        self.CHECKS_BY_HEX = dict()
        self.CHECKS_BY_NAME = dict()
        self.ORIGINAL_EVENT_PANELS = set()
        self.NECESSARY_EVENT_PANELS = set()
        self.EVENT_ITEM_PAIRS = dict()
        self.ALWAYS_EVENT_HEX_CODES = set()
        self.COMPLETELY_DISABLED_CHECKS = set()
        self.EVENT_ITEM_NAMES = {
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
            "0x28B39": "Town Tower 4th Door Opens"
        }

        self.ALWAYS_EVENT_NAMES_BY_HEX = {
            "0x0360D": "Symmetry Laser Activation",
            "0x03608": "Desert Laser Activation",
            "0x09F98": "Desert Laser Redirection",
            "0x03612": "Quarry Laser Activation",
            "0x19650": "Shadows Laser Activation",
            "0x0360E": "Keep Laser Hedges Activation",
            "0x03317": "Keep Laser Pressure Plates Activation",
            "0x17CA4": "Monastery Laser Activation",
            "0x032F5": "Town Laser Activation",
            "0x03616": "Jungle Laser Activation",
            "0x09DE0": "Bunker Laser Activation",
            "0x03615": "Swamp Laser Activation",
            "0x03613": "Treehouse Laser Activation",
            "0x03535": "Shipwreck Video Pattern Knowledge",
            "0x03542": "Mountain Video Pattern Knowledge",
            "0x0339E": "Desert Video Pattern Knowledge",
            "0x03481": "Tutorial Video Pattern Knowledge",
            "0x03702": "Jungle Video Pattern Knowledge",
            "0x2FAF6": "Theater Walkway Video Pattern Knowledge",
        }

        self.parse_items()
        self.read_logic_file()

    def adjustments(self, world: MultiWorld, player: int):
        self.make_options_adjustments(world, player)
        self.make_dependency_reduced_checklist()
        self.make_event_panel_lists()
