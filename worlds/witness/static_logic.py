import os

from .utils import define_new_region, parse_lambda


class StaticWitnessLogic:
    ALL_SYMBOL_ITEMS = set()
    ALL_DOOR_ITEMS = set()
    ALL_DOOR_ITEMS_AS_DICT = dict()
    ALL_USEFULS = set()
    ALL_TRAPS = set()
    ALL_BOOSTS = set()
    CONNECTIONS_TO_SEVER_BY_DOOR_HEX = dict()

    EVENT_PANELS_FROM_REGIONS = set()

    # All regions with a list of panels in them and the connections to other regions, before logic adjustments
    ALL_REGIONS_BY_NAME = dict()
    STATIC_CONNECTIONS_BY_REGION_NAME = dict()

    CHECKS_BY_HEX = dict()
    CHECKS_BY_NAME = dict()
    STATIC_DEPENDENT_REQUIREMENTS_BY_HEX = dict()

    def parse_items(self):
        """
        Parses currently defined items from WitnessItems.txt
        """

        path = os.path.join(os.path.dirname(__file__), "WitnessItems.txt")
        with open(path, "r", encoding="utf-8") as file:
            current_set = self.ALL_SYMBOL_ITEMS

            for line in file.readlines():
                line = line.strip()

                if line == "Progression:":
                    current_set = self.ALL_SYMBOL_ITEMS
                    continue
                if line == "Boosts:":
                    current_set = self.ALL_BOOSTS
                    continue
                if line == "Traps:":
                    current_set = self.ALL_TRAPS
                    continue
                if line == "Usefuls:":
                    current_set = self.ALL_USEFULS
                    continue
                if line == "Doors:":
                    current_set = self.ALL_DOOR_ITEMS
                    continue
                if line == "":
                    continue

                line_split = line.split(" - ")

                if current_set is self.ALL_USEFULS:
                    current_set.add((line_split[1], int(line_split[0]), line_split[2] == "True"))
                elif current_set is self.ALL_DOOR_ITEMS:
                    new_door = (line_split[1], int(line_split[0]), frozenset(line_split[2].split(",")))
                    current_set.add(new_door)
                    self.ALL_DOOR_ITEMS_AS_DICT[line_split[1]] = new_door
                else:
                    current_set.add((line_split[1], int(line_split[0])))

    def read_logic_file(self):
        """
        Reads the logic file and does the initial population of data structures
        """
        path = os.path.join(os.path.dirname(__file__), "WitnessLogic.txt")
        with open(path, "r", encoding="utf-8") as file:
            current_region = dict()

            counter = 0

            for line in file.readlines():
                line = line.strip()

                if line == "":
                    continue

                if line[-1] == ":":
                    new_region_and_connections = define_new_region(line)
                    current_region = new_region_and_connections[0]
                    region_name = current_region["name"]
                    self.ALL_REGIONS_BY_NAME[region_name] = current_region
                    self.STATIC_CONNECTIONS_BY_REGION_NAME[region_name] = new_region_and_connections[1]
                    continue

                line_split = line.split(" - ")

                location_id = line_split.pop(0)

                check_name_full = line_split.pop(0)

                check_hex = check_name_full[0:7]
                check_name = check_name_full[9:-1]

                required_panel_lambda = line_split.pop(0)

                if location_id == "Door" or location_id == "Laser":
                    self.CHECKS_BY_HEX[check_hex] = {
                        "checkName": current_region["shortName"] + " " + check_name,
                        "checkHex": check_hex,
                        "region": current_region,
                        "id": None,
                        "panelType": location_id
                    }

                    self.CHECKS_BY_NAME[self.CHECKS_BY_HEX[check_hex]["checkName"]] = self.CHECKS_BY_HEX[check_hex]

                    self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[check_hex] = {
                        "panels": parse_lambda(required_panel_lambda)
                    }

                    current_region["panels"].add(check_hex)
                    continue

                required_item_lambda = line_split.pop(0)

                laser_names = {
                    "Laser",
                    "Laser Hedges",
                    "Laser Pressure Plates",
                    "Desert Laser Redirect"
                }
                is_vault_or_video = "Vault" in check_name or "Video" in check_name

                if "Discard" in check_name:
                    location_type = "Discard"
                elif is_vault_or_video or check_name == "Tutorial Gate Close":
                    location_type = "Vault"
                elif check_name in laser_names:
                    location_type = "Laser"
                else:
                    location_type = "General"

                required_items = parse_lambda(required_item_lambda)

                required_items = frozenset(required_items)

                requirement = {
                    "panels": parse_lambda(required_panel_lambda),
                    "items": required_items
                }

                self.CHECKS_BY_HEX[check_hex] = {
                    "checkName": current_region["shortName"] + " " + check_name,
                    "checkHex": check_hex,
                    "region": current_region,
                    "id": int(location_id),
                    "panelType": location_type
                }

                self.CHECKS_BY_NAME[self.CHECKS_BY_HEX[check_hex]["checkName"]] = self.CHECKS_BY_HEX[check_hex]
                self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[check_hex] = requirement

                current_region["panels"].add(check_hex)

    def __init__(self):
        self.parse_items()
        self.read_logic_file()
