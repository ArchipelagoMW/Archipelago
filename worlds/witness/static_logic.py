import os

from .utils import define_new_region, parse_lambda


class StaticWitnessLogic:
    ALL_SYMBOL_ITEMS = set()
    ALL_USEFULS = set()
    ALL_TRAPS = set()
    ALL_BOOSTS = set()
    ALL_DOOR_ITEM_IDS_BY_HEX = dict()
    DOOR_NAMES_BY_HEX = dict()
    ALL_DOOR_ITEMS = set()
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
                if line == "":
                    continue

                line_split = line.split(" - ")

                current_set.add((line_split[1], int(line_split[0])))

        path = os.path.join(os.path.dirname(__file__), "Door_Shuffle.txt")
        with open(path, "r", encoding="utf-8") as file:
            for line in file.readlines():
                line = line.strip()

                line_split = line.split(" - ")

                hex_set_split = line_split[1].split(",")

                sever_list = line_split[2].split(",")
                sever_set = {sever_panel for sever_panel in sever_list if sever_panel != "None"}

                for door_hex in hex_set_split:
                    self.ALL_DOOR_ITEM_IDS_BY_HEX[door_hex] = int(line_split[0])
                    self.CONNECTIONS_TO_SEVER_BY_DOOR_HEX[door_hex] = sever_set

                    if len(line_split) > 3:
                        self.DOOR_NAMES_BY_HEX[door_hex] = line_split[3]
        
    def read_logic_file(self):
        """
        Reads the logic file and does the initial population of data structures
        """
        path = os.path.join(os.path.dirname(__file__), "WitnessLogic.txt")
        with open(path, "r", encoding="utf-8") as file:
            current_region = dict()

            discard_ids = 0
            normal_panel_ids = 0
            vault_ids = 0
            laser_ids = 0

            for line in file.readlines():
                line = line.strip()

                if line == "":
                    continue

                if line[0] != "0":
                    new_region_and_connections = define_new_region(line)
                    current_region = new_region_and_connections[0]
                    region_name = current_region["name"]
                    self.ALL_REGIONS_BY_NAME[region_name] = current_region
                    self.STATIC_CONNECTIONS_BY_REGION_NAME[region_name] = new_region_and_connections[1]
                    continue

                line_split = line.split(" - ")

                check_name_full = line_split.pop(0)

                check_hex = check_name_full[0:7]
                check_name = check_name_full[9:-1]

                required_panel_lambda = line_split.pop(0)
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

                    if check_hex == "0x012D7":  # Compatibility
                        normal_panel_ids += 1

                    if check_hex == "0x17E07":  # Compatibility
                        location_id = 112

                    elif check_hex == "0xFFF00":
                        location_id = 800

                    else:
                        location_id = normal_panel_ids
                        normal_panel_ids += 1

                required_items = parse_lambda(required_item_lambda)
                items_actually_in_the_game = {item[0] for item in self.ALL_SYMBOL_ITEMS}
                required_items = set(
                    subset.intersection(items_actually_in_the_game)
                    for subset in required_items
                )

                doors_in_the_game = self.ALL_DOOR_ITEM_IDS_BY_HEX.keys()
                if check_hex in doors_in_the_game:
                    door_name = current_region["shortName"] + " " + check_name + " Power On"
                    if check_hex in self.DOOR_NAMES_BY_HEX.keys():
                        door_name = self.DOOR_NAMES_BY_HEX[check_hex]

                    required_items = set(
                        subset.union(frozenset({door_name}))
                        for subset in required_items
                    )

                    self.ALL_DOOR_ITEMS.add(
                        (door_name, self.ALL_DOOR_ITEM_IDS_BY_HEX[check_hex])
                    )

                required_items = frozenset(required_items)

                requirement = {
                    "panels": parse_lambda(required_panel_lambda),
                    "items": required_items
                }

                self.CHECKS_BY_HEX[check_hex] = {
                    "checkName": current_region["shortName"] + " " + check_name,
                    "checkHex": check_hex,
                    "region": current_region,
                    "idOffset": location_id,
                    "panelType": location_type
                }

                self.CHECKS_BY_NAME[self.CHECKS_BY_HEX[check_hex]["checkName"]] = self.CHECKS_BY_HEX[check_hex]
                self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[check_hex] = requirement

                current_region["panels"].add(check_hex)

    def __init__(self):
        self.parse_items()
        self.read_logic_file()
