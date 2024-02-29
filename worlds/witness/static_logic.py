from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from .utils import define_new_region, parse_lambda, lazy, get_items, get_sigma_normal_logic, get_sigma_expert_logic,\
    get_vanilla_logic


class ItemCategory(Enum):
    SYMBOL = 0
    DOOR = 1
    LASER = 2
    USEFUL = 3
    FILLER = 4
    TRAP = 5
    JOKE = 6
    EVENT = 7


CATEGORY_NAME_MAPPINGS: Dict[str, ItemCategory] = {
    "Symbols:": ItemCategory.SYMBOL,
    "Doors:": ItemCategory.DOOR,
    "Lasers:": ItemCategory.LASER,
    "Useful:": ItemCategory.USEFUL,
    "Filler:": ItemCategory.FILLER,
    "Traps:": ItemCategory.TRAP,
    "Jokes:": ItemCategory.JOKE
}


@dataclass(frozen=True)
class ItemDefinition:
    local_code: int
    category: ItemCategory


@dataclass(frozen=True)
class ProgressiveItemDefinition(ItemDefinition):
    child_item_names: List[str]


@dataclass(frozen=True)
class DoorItemDefinition(ItemDefinition):
    panel_id_hexes: List[str]


@dataclass(frozen=True)
class WeightedItemDefinition(ItemDefinition):
    weight: int


class StaticWitnessLogicObj:
    def read_logic_file(self, lines):
        """
        Reads the logic file and does the initial population of data structures
        """

        current_region = dict()
        current_area = {
            "name": "Misc",
            "regions": [],
        }
        self.ALL_AREAS_BY_NAME["Misc"] = current_area

        for line in lines:
            if line == "" or line[0] == "#":
                continue

            if line[-1] == ":":
                new_region_and_connections = define_new_region(line)
                current_region = new_region_and_connections[0]
                region_name = current_region["name"]
                self.ALL_REGIONS_BY_NAME[region_name] = current_region
                self.STATIC_CONNECTIONS_BY_REGION_NAME[region_name] = new_region_and_connections[1]
                current_area["regions"].append(region_name)
                continue

            if line[0] == "=":
                area_name = line[2:-2]
                current_area = {
                    "name": area_name,
                    "regions": [],
                }
                self.ALL_AREAS_BY_NAME[area_name] = current_area
                continue

            line_split = line.split(" - ")

            location_id = line_split.pop(0)

            entity_name_full = line_split.pop(0)

            entity_hex = entity_name_full[0:7]
            entity_name = entity_name_full[9:-1]

            required_panel_lambda = line_split.pop(0)

            full_entity_name = current_region["shortName"] + " " + entity_name

            if location_id == "Door" or location_id == "Laser":
                self.ENTITIES_BY_HEX[entity_hex] = {
                    "checkName": full_entity_name,
                    "entity_hex": entity_hex,
                    "region": None,
                    "id": None,
                    "entityType": location_id,
                    "area": current_area,
                }

                self.ENTITIES_BY_NAME[self.ENTITIES_BY_HEX[entity_hex]["checkName"]] = self.ENTITIES_BY_HEX[entity_hex]

                self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex] = {
                    "panels": parse_lambda(required_panel_lambda)
                }

                # Lasers and Doors exist in a region, but don't have a regional *requirement*
                # If a laser is activated, you don't need to physically walk up to it for it to count
                # As such, logically, they behave more as if they were part of the "Entry" region
                self.ALL_REGIONS_BY_NAME["Entry"]["panels"].append(entity_hex)
                continue

            required_item_lambda = line_split.pop(0)

            laser_names = {
                "Laser",
                "Laser Hedges",
                "Laser Pressure Plates",
            }
            is_vault_or_video = "Vault" in entity_name or "Video" in entity_name

            if "Discard" in entity_name:
                location_type = "Discard"
            elif is_vault_or_video or entity_name == "Tutorial Gate Close":
                location_type = "Vault"
            elif entity_name in laser_names:
                location_type = "Laser"
            elif "Obelisk Side" in entity_name:
                location_type = "Obelisk Side"
            elif "EP" in entity_name:
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

                self.OBELISK_SIDE_ID_TO_EP_HEXES[int(entity_hex, 16)] = eps_ints
                for ep_hex in eps:
                    self.EP_TO_OBELISK_SIDE[ep_hex] = entity_hex

            self.ENTITIES_BY_HEX[entity_hex] = {
                "checkName": full_entity_name,
                "entity_hex": entity_hex,
                "region": current_region,
                "id": int(location_id),
                "entityType": location_type,
                "area": current_area,
            }

            self.ENTITY_ID_TO_NAME[entity_hex] = full_entity_name

            self.ENTITIES_BY_NAME[self.ENTITIES_BY_HEX[entity_hex]["checkName"]] = self.ENTITIES_BY_HEX[entity_hex]
            self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex] = requirement

            current_region["panels"].append(entity_hex)

    def __init__(self, lines=None):
        if lines is None:
            lines = get_sigma_normal_logic()

        # All regions with a list of panels in them and the connections to other regions, before logic adjustments
        self.ALL_REGIONS_BY_NAME = dict()
        self.ALL_AREAS_BY_NAME = dict()
        self.STATIC_CONNECTIONS_BY_REGION_NAME = dict()

        self.ENTITIES_BY_HEX = dict()
        self.ENTITIES_BY_NAME = dict()
        self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX = dict()

        self.OBELISK_SIDE_ID_TO_EP_HEXES = dict()

        self.EP_TO_OBELISK_SIDE = dict()

        self.ENTITY_ID_TO_NAME = dict()

        self.read_logic_file(lines)


class StaticWitnessLogic:
    # Item data parsed from WitnessItems.txt
    all_items: Dict[str, ItemDefinition] = {}
    _progressive_lookup: Dict[str, str] = {}

    ALL_REGIONS_BY_NAME = dict()
    ALL_AREAS_BY_NAME = dict()
    STATIC_CONNECTIONS_BY_REGION_NAME = dict()

    OBELISK_SIDE_ID_TO_EP_HEXES = dict()

    ENTITIES_BY_HEX = dict()
    ENTITIES_BY_NAME = dict()
    STATIC_DEPENDENT_REQUIREMENTS_BY_HEX = dict()

    EP_TO_OBELISK_SIDE = dict()

    ENTITY_ID_TO_NAME = dict()

    @staticmethod
    def parse_items():
        """
        Parses currently defined items from WitnessItems.txt
        """

        lines: List[str] = get_items()
        current_category: ItemCategory = ItemCategory.SYMBOL

        for line in lines:
            # Skip empty lines and comments.
            if line == "" or line[0] == "#":
                continue

            # If this line is a category header, update our cached category.
            if line in CATEGORY_NAME_MAPPINGS.keys():
                current_category = CATEGORY_NAME_MAPPINGS[line]
                continue

            line_split = line.split(" - ")

            item_code = int(line_split[0])
            item_name = line_split[1]
            arguments: List[str] = line_split[2].split(",") if len(line_split) >= 3 else []

            if current_category in [ItemCategory.DOOR, ItemCategory.LASER]:
                # Map doors to IDs.
                StaticWitnessLogic.all_items[item_name] = DoorItemDefinition(item_code, current_category,
                                                                             arguments)
            elif current_category == ItemCategory.TRAP or current_category == ItemCategory.FILLER:
                # Read filler weights.
                weight = int(arguments[0]) if len(arguments) >= 1 else 1
                StaticWitnessLogic.all_items[item_name] = WeightedItemDefinition(item_code, current_category, weight)
            elif arguments:
                # Progressive items.
                StaticWitnessLogic.all_items[item_name] = ProgressiveItemDefinition(item_code, current_category,
                                                                                    arguments)
                for child_item in arguments:
                    StaticWitnessLogic._progressive_lookup[child_item] = item_name
            else:
                StaticWitnessLogic.all_items[item_name] = ItemDefinition(item_code, current_category)

    @staticmethod
    def get_parent_progressive_item(item_name: str):
        """
        Returns the name of the item's progressive parent, if there is one, or the item's name if not.
        """
        return StaticWitnessLogic._progressive_lookup.get(item_name, item_name)

    @lazy
    def sigma_expert(self) -> StaticWitnessLogicObj:
        return StaticWitnessLogicObj(get_sigma_expert_logic())

    @lazy
    def sigma_normal(self) -> StaticWitnessLogicObj:
        return StaticWitnessLogicObj(get_sigma_normal_logic())

    @lazy
    def vanilla(self) -> StaticWitnessLogicObj:
        return StaticWitnessLogicObj(get_vanilla_logic())

    def __init__(self):
        self.parse_items()

        self.ALL_REGIONS_BY_NAME.update(self.sigma_normal.ALL_REGIONS_BY_NAME)
        self.ALL_AREAS_BY_NAME.update(self.sigma_normal.ALL_AREAS_BY_NAME)
        self.STATIC_CONNECTIONS_BY_REGION_NAME.update(self.sigma_normal.STATIC_CONNECTIONS_BY_REGION_NAME)

        self.ENTITIES_BY_HEX.update(self.sigma_normal.ENTITIES_BY_HEX)
        self.ENTITIES_BY_NAME.update(self.sigma_normal.ENTITIES_BY_NAME)
        self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX.update(self.sigma_normal.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX)

        self.OBELISK_SIDE_ID_TO_EP_HEXES.update(self.sigma_normal.OBELISK_SIDE_ID_TO_EP_HEXES)

        self.EP_TO_OBELISK_SIDE.update(self.sigma_normal.EP_TO_OBELISK_SIDE)

        self.ENTITY_ID_TO_NAME.update(self.sigma_normal.ENTITY_ID_TO_NAME)


StaticWitnessLogic()
