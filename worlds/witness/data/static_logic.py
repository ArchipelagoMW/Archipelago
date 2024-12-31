from collections import defaultdict
from typing import Any, Dict, List, Optional, Set, Tuple

from Utils import cache_argsless

from .item_definition_classes import (
    CATEGORY_NAME_MAPPINGS,
    DoorItemDefinition,
    ItemCategory,
    ItemDefinition,
    ProgressiveItemDefinition,
    WeightedItemDefinition,
)
from .utils import (
    WitnessRule,
    define_new_region,
    get_items,
    get_sigma_expert_logic,
    get_sigma_normal_logic,
    get_umbra_variety_logic,
    get_vanilla_logic,
    logical_or_witness_rules,
    parse_lambda,
)


class StaticWitnessLogicObj:
    def __init__(self, lines: Optional[List[str]] = None) -> None:
        if lines is None:
            lines = get_sigma_normal_logic()

        # All regions with a list of panels in them and the connections to other regions, before logic adjustments
        self.ALL_REGIONS_BY_NAME: Dict[str, Dict[str, Any]] = {}
        self.ALL_AREAS_BY_NAME: Dict[str, Dict[str, Any]] = {}
        self.CONNECTIONS_WITH_DUPLICATES: Dict[str, Dict[str, Set[WitnessRule]]] = defaultdict(lambda: defaultdict(set))
        self.STATIC_CONNECTIONS_BY_REGION_NAME: Dict[str, Set[Tuple[str, WitnessRule]]] = {}

        self.ENTITIES_BY_HEX: Dict[str, Dict[str, Any]] = {}
        self.ENTITIES_BY_NAME: Dict[str, Dict[str, Any]] = {}
        self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX: Dict[str, Dict[str, WitnessRule]] = {}

        self.OBELISK_SIDE_ID_TO_EP_HEXES: Dict[int, Set[int]] = {}

        self.EP_TO_OBELISK_SIDE: Dict[str, str] = {}

        self.ENTITY_ID_TO_NAME: Dict[str, str] = {}

        self.read_logic_file(lines)
        self.reverse_connections()
        self.combine_connections()

    def read_logic_file(self, lines: List[str]) -> None:
        """
        Reads the logic file and does the initial population of data structures
        """

        current_region = {}
        current_area: Dict[str, Any] = {
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
                for connection in new_region_and_connections[1]:
                    self.CONNECTIONS_WITH_DUPLICATES[region_name][connection[0]].add(connection[1])
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
                    "locationType": None,
                    "area": current_area,
                    "order": len(self.ENTITIES_BY_HEX),
                }

                self.ENTITIES_BY_NAME[self.ENTITIES_BY_HEX[entity_hex]["checkName"]] = self.ENTITIES_BY_HEX[entity_hex]

                self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex] = {
                    "entities": parse_lambda(required_panel_lambda)
                }

                # Lasers and Doors exist in a region, but don't have a regional *requirement*
                # If a laser is activated, you don't need to physically walk up to it for it to count
                # As such, logically, they behave more as if they were part of the "Entry" region
                self.ALL_REGIONS_BY_NAME["Entry"]["entities"].append(entity_hex)
                # However, it will also be important to keep track of their physical location for postgame purposes.
                current_region["physical_entities"].append(entity_hex)
                continue

            required_item_lambda = line_split.pop(0)

            laser_names = {
                "Laser",
                "Laser Hedges",
                "Laser Pressure Plates",
            }

            if "Discard" in entity_name:
                entity_type = "Panel"
                location_type = "Discard"
            elif "Vault" in entity_name:
                entity_type = "Panel"
                location_type = "Vault"
            elif entity_name in laser_names:
                entity_type = "Laser"
                location_type = None
            elif "Obelisk Side" in entity_name:
                entity_type = "Obelisk Side"
                location_type = "Obelisk Side"
            elif "Obelisk" in entity_name:
                entity_type = "Obelisk"
                location_type = None
            elif "EP" in entity_name:
                entity_type = "EP"
                location_type = "EP"
            elif "Pet the Dog" in entity_name:
                entity_type = "Event"
                location_type = "Good Boi"
            elif entity_hex.startswith("0xFF"):
                entity_type = "Event"
                location_type = None
            else:
                entity_type = "Panel"
                location_type = "General"

            required_items = parse_lambda(required_item_lambda)
            required_panels = parse_lambda(required_panel_lambda)

            required_items = frozenset(required_items)

            requirement = {
                "entities": required_panels,
                "items": required_items
            }

            if entity_type == "Obelisk Side":
                eps = set(next(iter(required_panels)))
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
                "entityType": entity_type,
                "locationType": location_type,
                "area": current_area,
                "order": len(self.ENTITIES_BY_HEX),
            }

            self.ENTITY_ID_TO_NAME[entity_hex] = full_entity_name

            self.ENTITIES_BY_NAME[self.ENTITIES_BY_HEX[entity_hex]["checkName"]] = self.ENTITIES_BY_HEX[entity_hex]
            self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex] = requirement

            current_region["entities"].append(entity_hex)
            current_region["physical_entities"].append(entity_hex)

    def reverse_connection(self, source_region: str, connection: Tuple[str, Set[WitnessRule]]) -> None:
        target = connection[0]
        traversal_options = connection[1]

        # Reverse this connection with all its possibilities, except the ones marked as "OneWay".
        for requirement in traversal_options:
            remaining_options = set()
            for option in requirement:
                if not any(req == "TrueOneWay" for req in option):
                    remaining_options.add(option)

            if remaining_options:
                self.CONNECTIONS_WITH_DUPLICATES[target][source_region].add(frozenset(remaining_options))

    def reverse_connections(self) -> None:
        # Iterate all connections
        for region_name, connections in list(self.CONNECTIONS_WITH_DUPLICATES.items()):
            for connection in connections.items():
                self.reverse_connection(region_name, connection)

    def combine_connections(self) -> None:
        # All regions need to be present, and this dict is copied later - Thus, defaultdict is not the correct choice.
        self.STATIC_CONNECTIONS_BY_REGION_NAME = {region_name: set() for region_name in self.ALL_REGIONS_BY_NAME}

        for source, connections in self.CONNECTIONS_WITH_DUPLICATES.items():
            for target, requirement in connections.items():
                combined_req = logical_or_witness_rules(requirement)
                self.STATIC_CONNECTIONS_BY_REGION_NAME[source].add((target, combined_req))


# Item data parsed from WitnessItems.txt
ALL_ITEMS: Dict[str, ItemDefinition] = {}
_progressive_lookup: Dict[str, str] = {}


def parse_items() -> None:
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
            ALL_ITEMS[item_name] = DoorItemDefinition(item_code, current_category, arguments)
        elif current_category == ItemCategory.TRAP or current_category == ItemCategory.FILLER:
            # Read filler weights.
            weight = int(arguments[0]) if len(arguments) >= 1 else 1
            ALL_ITEMS[item_name] = WeightedItemDefinition(item_code, current_category, weight)
        elif arguments:
            # Progressive items.
            ALL_ITEMS[item_name] = ProgressiveItemDefinition(item_code, current_category, arguments)
            for child_item in arguments:
                _progressive_lookup[child_item] = item_name
        else:
            ALL_ITEMS[item_name] = ItemDefinition(item_code, current_category)


def get_parent_progressive_item(item_name: str) -> str:
    """
    Returns the name of the item's progressive parent, if there is one, or the item's name if not.
    """
    return _progressive_lookup.get(item_name, item_name)


@cache_argsless
def get_vanilla() -> StaticWitnessLogicObj:
    return StaticWitnessLogicObj(get_vanilla_logic())


@cache_argsless
def get_sigma_normal() -> StaticWitnessLogicObj:
    return StaticWitnessLogicObj(get_sigma_normal_logic())


@cache_argsless
def get_sigma_expert() -> StaticWitnessLogicObj:
    return StaticWitnessLogicObj(get_sigma_expert_logic())


@cache_argsless
def get_umbra_variety() -> StaticWitnessLogicObj:
    return StaticWitnessLogicObj(get_umbra_variety_logic())


def __getattr__(name: str) -> StaticWitnessLogicObj:
    if name == "vanilla":
        return get_vanilla()
    if name == "sigma_normal":
        return get_sigma_normal()
    if name == "sigma_expert":
        return get_sigma_expert()
    if name == "umbra_variety":
        return get_umbra_variety()
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


parse_items()

ALL_REGIONS_BY_NAME = get_sigma_normal().ALL_REGIONS_BY_NAME
ALL_AREAS_BY_NAME = get_sigma_normal().ALL_AREAS_BY_NAME
STATIC_CONNECTIONS_BY_REGION_NAME = get_sigma_normal().STATIC_CONNECTIONS_BY_REGION_NAME

ENTITIES_BY_HEX = get_sigma_normal().ENTITIES_BY_HEX
ENTITIES_BY_NAME = get_sigma_normal().ENTITIES_BY_NAME
STATIC_DEPENDENT_REQUIREMENTS_BY_HEX = get_sigma_normal().STATIC_DEPENDENT_REQUIREMENTS_BY_HEX

OBELISK_SIDE_ID_TO_EP_HEXES = get_sigma_normal().OBELISK_SIDE_ID_TO_EP_HEXES

EP_TO_OBELISK_SIDE = get_sigma_normal().EP_TO_OBELISK_SIDE

ENTITY_ID_TO_NAME = get_sigma_normal().ENTITY_ID_TO_NAME
