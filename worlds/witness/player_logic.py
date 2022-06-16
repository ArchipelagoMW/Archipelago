"""
Parses the WitnessLogic.txt logic file into useful data structures.
This is the heart of the randomization.

In WitnessLogic.txt we have regions defined with their connections:

Region Name (Short name) - Connected Region 1 - Connection Requirement 1 - Connected Region 2...

And then panels in that region with the hex code used in the game
previous panels that are required to turn them on, as well as the symbols they require:

0x##### (Panel Name) - Required Panels - Required Items

On __init__, the base logic is read and all panels are given Location IDs.
When the world has parsed its options, a second function is called to finalize the logic.
"""

import copy
from BaseClasses import MultiWorld
from .static_logic import StaticWitnessLogic
from .utils import define_new_region, get_disable_unrandomized_list, parse_lambda, get_early_utm_list
from .Options import is_option_enabled, get_option_value, the_witness_options


class WitnessPlayerLogic:
    """WITNESS LOGIC CLASS"""

    def update_door_dict(self, panel_hex):
        item_id = StaticWitnessLogic.ALL_DOOR_ITEM_IDS_BY_HEX.get(panel_hex)

        if item_id is None:
            return

        self.DOOR_DICT_FOR_CLIENT[panel_hex] = item_id
        self.DOOR_CONNECTIONS_TO_SEVER.update(StaticWitnessLogic.CONNECTIONS_TO_SEVER_BY_DOOR_HEX[panel_hex])

    def reduce_req_within_region(self, panel_hex):
        """
        Panels in this game often only turn on when other panels are solved.
        Those other panels may have different item requirements.
        It would be slow to recursively check solvability each time.
        This is why we reduce the item dependencies within the region.
        Panels outside of the same region will still be checked manually.
        """

        these_items = self.DEPENDENT_REQUIREMENTS_BY_HEX[panel_hex]["items"]

        real_items = {item[0] for item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME}

        these_items = frozenset({
            subset.intersection(real_items)
            for subset in these_items
        })

        these_panels = self.DEPENDENT_REQUIREMENTS_BY_HEX[panel_hex]["panels"]

        if StaticWitnessLogic.DOOR_NAMES_BY_HEX.get(panel_hex) in real_items:
            self.update_door_dict(panel_hex)

            these_panels = frozenset({frozenset()})

        if these_panels == frozenset({frozenset()}):
            return these_items

        all_options = set()

        check_obj = StaticWitnessLogic.CHECKS_BY_HEX[panel_hex]

        for option in these_panels:
            dependent_items_for_option = frozenset({frozenset()})

            for option_panel in option:
                new_items = set()
                dep_obj = StaticWitnessLogic.CHECKS_BY_HEX.get(option_panel)
                if option_panel in {"7 Lasers", "11 Lasers"}:
                    new_items = frozenset({frozenset([option_panel])})
                # If a panel turns on when a panel in a different region turns on,
                # the latter panel will be an "event panel", unless it ends up being
                # a location itself. This prevents generation failures.
                elif dep_obj["region"]["name"] != check_obj["region"]["name"]:
                    new_items = frozenset({frozenset([option_panel])})
                    self.EVENT_PANELS_FROM_PANELS.add(option_panel)
                elif option_panel in self.ALWAYS_EVENT_NAMES_BY_HEX.keys():
                    new_items = frozenset({frozenset([option_panel])})
                    self.EVENT_PANELS_FROM_PANELS.add(option_panel)
                else:
                    new_items = self.reduce_req_within_region(option_panel)

                updated_items = set()

                for items_option in dependent_items_for_option:
                    for items_option2 in new_items:
                        updated_items.add(items_option.union(items_option2))

                dependent_items_for_option = updated_items

            for items_option in these_items:
                for dependentItem in dependent_items_for_option:
                    all_options.add(items_option.union(dependentItem))

        return frozenset(all_options)

    def make_single_adjustment(self, adj_type, line):
        """Makes a single logic adjustment based on additional logic file"""

        if adj_type == "Event Items":
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

        if adj_type == "Requirement Changes":
            line_split = line.split(" - ")

            required_items = parse_lambda(line_split[2])
            items_actually_in_the_game = {item[0] for item in StaticWitnessLogic.ALL_SYMBOL_ITEMS}
            required_items = frozenset(
                subset.intersection(items_actually_in_the_game)
                for subset in required_items
            )

            requirement = {
                "panels": parse_lambda(line_split[1]),
                "items": required_items
            }

            self.DEPENDENT_REQUIREMENTS_BY_HEX[line_split[0]] = requirement

            return

        if adj_type == "Disabled Locations":
            panel_hex = line[:7]

            self.COMPLETELY_DISABLED_CHECKS.add(panel_hex)

            self.PROG_ITEMS_ACTUALLY_IN_THE_GAME = {
                item for item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME
                if item[0] != StaticWitnessLogic.DOOR_NAMES_BY_HEX.get(panel_hex)
            }

            return

        if adj_type == "Region Changes":
            new_region_and_options = define_new_region(line + ":")
            
            self.CONNECTIONS_BY_REGION_NAME[new_region_and_options[0]["name"]] = new_region_and_options[1]

            return

        if adj_type == "Added Locations":
            self.ADDED_CHECKS.add(line)

    def make_options_adjustments(self, world, player):
        """Makes logic adjustments based on options"""
        adjustment_linesets_in_order = []

        if get_option_value(world, player, "victory_condition") == 0:
            self.VICTORY_LOCATION = "0x3D9A9"
        elif get_option_value(world, player, "victory_condition") == 1:
            self.VICTORY_LOCATION = "0x0356B"
        elif get_option_value(world, player, "victory_condition") == 2:
            self.VICTORY_LOCATION = "0x09F7F"
        elif get_option_value(world, player, "victory_condition") == 3:
            self.VICTORY_LOCATION = "0xFFF00"

        self.COMPLETELY_DISABLED_CHECKS.add(
            self.VICTORY_LOCATION
        )

        if is_option_enabled(world, player, "disable_non_randomized_puzzles"):
            adjustment_linesets_in_order.append(get_disable_unrandomized_list())

        if is_option_enabled(world, player, "shuffle_symbols") or "shuffle_symbols" not in the_witness_options.keys():
            self.PROG_ITEMS_ACTUALLY_IN_THE_GAME.update(StaticWitnessLogic.ALL_SYMBOL_ITEMS)

        if is_option_enabled(world, player, "shuffle_doors"):
            self.PROG_ITEMS_ACTUALLY_IN_THE_GAME.update(StaticWitnessLogic.ALL_DOOR_ITEMS)

        if is_option_enabled(world, player, "early_secret_area"):
            adjustment_linesets_in_order.append(get_early_utm_list())
        else:
            self.PROG_ITEMS_ACTUALLY_IN_THE_GAME = {
                item for item in self.PROG_ITEMS_ACTUALLY_IN_THE_GAME
                if item[0] != "Mountaintop River Shape Power On"
            }

        for adjustment_lineset in adjustment_linesets_in_order:
            current_adjustment_type = None

            for line in adjustment_lineset:
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

        for check_hex in self.DEPENDENT_REQUIREMENTS_BY_HEX.keys():
            indep_requirement = self.reduce_req_within_region(check_hex)

            self.REQUIREMENTS_BY_HEX[check_hex] = indep_requirement

    def make_event_item_pair(self, panel):
        """
        Makes a pair of an event panel and its event item
        """
        name = StaticWitnessLogic.CHECKS_BY_HEX[panel]["checkName"] + " Solved"
        pair = (name, self.EVENT_ITEM_NAMES[panel])
        return pair

    def _regions_are_adjacent(self, region1, region2):
        for connection in self.CONNECTIONS_BY_REGION_NAME[region1]:
            if connection[0] == region2:
                return True

        for connection in self.CONNECTIONS_BY_REGION_NAME[region2]:
            if connection[0] == region1:
                return True

        return False

    def make_event_panel_lists(self):
        """
        Special event panel data structures
        """

        for region_conn in self.CONNECTIONS_BY_REGION_NAME.values():
            for region_and_option in region_conn:
                for panelset in region_and_option[1]:
                    for panel in panelset:
                        self.EVENT_PANELS_FROM_REGIONS.add(panel)

        self.ALWAYS_EVENT_NAMES_BY_HEX[self.VICTORY_LOCATION] = "Victory"

        self.ORIGINAL_EVENT_PANELS.update(self.EVENT_PANELS_FROM_PANELS)
        self.ORIGINAL_EVENT_PANELS.update(self.EVENT_PANELS_FROM_REGIONS)

        for panel in self.EVENT_PANELS_FROM_REGIONS:
            for region_name, region in StaticWitnessLogic.ALL_REGIONS_BY_NAME.items():
                for connection in self.CONNECTIONS_BY_REGION_NAME[region_name]:
                    connected_r = connection[0]
                    if connected_r not in StaticWitnessLogic.ALL_REGIONS_BY_NAME:
                        continue
                    if region_name == "Boat" or connected_r == "Boat":
                        continue
                    connected_r = StaticWitnessLogic.ALL_REGIONS_BY_NAME[connected_r]
                    if not any([panel in option for option in connection[1]]):
                        continue
                    if panel not in region["panels"] | connected_r["panels"]:
                        self.NECESSARY_EVENT_PANELS.add(panel)

        for event_panel in self.EVENT_PANELS_FROM_PANELS:
            for panel, panel_req in self.REQUIREMENTS_BY_HEX.items():
                if any([event_panel in item_set for item_set in panel_req]):
                    region1 = StaticWitnessLogic.CHECKS_BY_HEX[panel]["region"]["name"]
                    region2 = StaticWitnessLogic.CHECKS_BY_HEX[event_panel]["region"]["name"]

                    if not self._regions_are_adjacent(region1, region2):
                        self.NECESSARY_EVENT_PANELS.add(event_panel)

        for always_hex, always_item in self.ALWAYS_EVENT_NAMES_BY_HEX.items():
            self.ALWAYS_EVENT_HEX_CODES.add(always_hex)
            self.NECESSARY_EVENT_PANELS.add(always_hex)
            self.EVENT_ITEM_NAMES[always_hex] = always_item

        for panel in self.NECESSARY_EVENT_PANELS:
            pair = self.make_event_item_pair(panel)
            self.EVENT_ITEM_PAIRS[pair[0]] = pair[1]

    def __init__(self, world: MultiWorld, player: int):
        self.EVENT_PANELS_FROM_PANELS = set()
        self.EVENT_PANELS_FROM_REGIONS = set()

        self.PROG_ITEMS_ACTUALLY_IN_THE_GAME = set()
        self.DOOR_DICT_FOR_CLIENT = dict()
        self.DOOR_CONNECTIONS_TO_SEVER = set()

        self.CONNECTIONS_BY_REGION_NAME = copy.copy(StaticWitnessLogic.STATIC_CONNECTIONS_BY_REGION_NAME)
        self.DEPENDENT_REQUIREMENTS_BY_HEX = copy.copy(StaticWitnessLogic.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX)
        self.REQUIREMENTS_BY_HEX = dict()

        # Determining which panels need to be events is a difficult process.
        # At the end, we will have EVENT_ITEM_PAIRS for all the necessary ones.
        self.ORIGINAL_EVENT_PANELS = set()
        self.NECESSARY_EVENT_PANELS = set()
        self.EVENT_ITEM_PAIRS = dict()
        self.ALWAYS_EVENT_HEX_CODES = set()
        self.COMPLETELY_DISABLED_CHECKS = set()
        self.ADDED_CHECKS = set()
        self.VICTORY_LOCATION = "0x0356B"
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
            "0x28B39": "Town Tower 4th Door Opens",
            "0x0343A": "Door to Symmetry Island Powers On",
            "0xFFF00": "Inside Mountain Bottom Layer Discard Turns On"
        }

        self.ALWAYS_EVENT_NAMES_BY_HEX = {
            "0x0360D": "Symmetry Laser Activation",
            "0x03608": "Desert Laser Activation",
            "0x09F98": "Desert Laser Redirection",
            "0x03612": "Quarry Laser Activation",
            "0x19650": "Shadows Laser Activation",
            "0x0360E": "Keep Laser Activation",
            "0x03317": "Keep Laser Activation",
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
            "0x09F7F": "Mountaintop Trap Door Turns On",
            "0x17C34": "Mountain Access",
        }

        self.make_options_adjustments(world, player)
        self.make_dependency_reduced_checklist()
        self.make_event_panel_lists()
