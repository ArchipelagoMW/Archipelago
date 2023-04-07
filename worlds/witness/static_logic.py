import os

from .utils import define_new_region, parse_lambda, lazy


class StaticWitnessLogicObj:
    def read_logic_file(self, file_path="WitnessLogic.txt"):
        """
        Reads the logic file and does the initial population of data structures
        """
        path = os.path.join(os.path.dirname(__file__), file_path)

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

                full_check_name = current_region["shortName"] + " " + check_name

                if location_id == "Door" or location_id == "Laser":
                    self.CHECKS_BY_HEX[check_hex] = {
                        "checkName": full_check_name,
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
                elif "Obelisk Side" in check_name:
                    location_type = "Obelisk Side"
                    full_check_name = check_name
                elif "EP" in check_name:
                    location_type = "EP"
                else:
                    location_type = "General"

                required_items = parse_lambda(required_item_lambda)
                required_panels = parse_lambda(required_panel_lambda)

                required_items = frozenset(required_items)

                requirement = {
                    "panels": required_panels,
                    "items": required_items
                }

                if location_type == "Obelisk Side":
                    eps = set(list(required_panels)[0])
                    eps -= {"Theater to Tunnels"}

                    eps_ints = {int(h, 16) for h in eps}

                    self.OBELISK_SIDE_ID_TO_EP_HEXES[int(check_hex, 16)] = eps_ints
                    for ep_hex in eps:
                        self.EP_TO_OBELISK_SIDE[ep_hex] = check_hex

                self.CHECKS_BY_HEX[check_hex] = {
                    "checkName": full_check_name,
                    "checkHex": check_hex,
                    "region": current_region,
                    "id": int(location_id),
                    "panelType": location_type
                }

                self.ENTITY_ID_TO_NAME[check_hex] = full_check_name

                self.CHECKS_BY_NAME[self.CHECKS_BY_HEX[check_hex]["checkName"]] = self.CHECKS_BY_HEX[check_hex]
                self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[check_hex] = requirement

                current_region["panels"].add(check_hex)

    def __init__(self, file_path="WitnessLogic.txt"):
        # All regions with a list of panels in them and the connections to other regions, before logic adjustments
        self.ALL_REGIONS_BY_NAME = dict()
        self.STATIC_CONNECTIONS_BY_REGION_NAME = dict()

        self.CHECKS_BY_HEX = dict()
        self.CHECKS_BY_NAME = dict()
        self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX = dict()

        self.OBELISK_SIDE_ID_TO_EP_HEXES = dict()

        self.EP_TO_OBELISK_SIDE = dict()

        self.ENTITY_ID_TO_NAME = dict()

        self.read_logic_file(file_path)


class StaticWitnessLogic:
    ALL_SYMBOL_ITEMS = set()
    ITEMS_TO_PROGRESSIVE = dict()
    PROGRESSIVE_TO_ITEMS = dict()
    ALL_DOOR_ITEMS = set()
    ALL_DOOR_ITEMS_AS_DICT = dict()
    ALL_USEFULS = set()
    ALL_TRAPS = set()
    ALL_BOOSTS = set()
    CONNECTIONS_TO_SEVER_BY_DOOR_HEX = dict()

    ALL_REGIONS_BY_NAME = dict()
    STATIC_CONNECTIONS_BY_REGION_NAME = dict()

    OBELISK_SIDE_ID_TO_EP_HEXES = dict()

    CHECKS_BY_HEX = dict()
    CHECKS_BY_NAME = dict()
    STATIC_DEPENDENT_REQUIREMENTS_BY_HEX = dict()

    EP_TO_OBELISK_SIDE = dict()

    ENTITY_ID_TO_NAME = dict()

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
                    if len(line_split) > 2:
                        progressive_items = line_split[2].split(",")
                        for i, value in enumerate(progressive_items):
                            self.ITEMS_TO_PROGRESSIVE[value] = line_split[1]
                        self.PROGRESSIVE_TO_ITEMS[line_split[1]] = progressive_items
                        current_set.add((line_split[1], int(line_split[0])))
                        continue
                    current_set.add((line_split[1], int(line_split[0])))

    @lazy
    def sigma_expert(self) -> StaticWitnessLogicObj:
        return StaticWitnessLogicObj("WitnessLogicExpert.txt")

    @lazy
    def sigma_normal(self) -> StaticWitnessLogicObj:
        return StaticWitnessLogicObj("WitnessLogic.txt")

    @lazy
    def vanilla(self) -> StaticWitnessLogicObj:
        return StaticWitnessLogicObj("WitnessLogicVanilla.txt")

    def __init__(self):
        self.parse_items()

        self.ALL_REGIONS_BY_NAME.update(self.sigma_normal.ALL_REGIONS_BY_NAME)
        self.STATIC_CONNECTIONS_BY_REGION_NAME.update(self.sigma_normal.STATIC_CONNECTIONS_BY_REGION_NAME)

        self.CHECKS_BY_HEX.update(self.sigma_normal.CHECKS_BY_HEX)
        self.CHECKS_BY_NAME.update(self.sigma_normal.CHECKS_BY_NAME)
        self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX.update(self.sigma_normal.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX)

        self.OBELISK_SIDE_ID_TO_EP_HEXES.update(self.sigma_normal.OBELISK_SIDE_ID_TO_EP_HEXES)

        self.EP_TO_OBELISK_SIDE.update(self.sigma_normal.EP_TO_OBELISK_SIDE)

        self.ENTITY_ID_TO_NAME.update(self.sigma_normal.ENTITY_ID_TO_NAME)