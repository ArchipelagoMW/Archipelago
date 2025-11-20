from collections import Counter, defaultdict
from typing import Any, Dict, FrozenSet, List, Optional, Set

from Utils import cache_argsless

from .definition_classes import AreaDefinition, ConnectionDefinition, RegionDefinition, WitnessRule
from .item_definition_classes import (
    CATEGORY_NAME_MAPPINGS,
    DoorItemDefinition,
    ItemCategory,
    ItemDefinition,
    ProgressiveItemDefinition,
    WeightedItemDefinition,
)
from .settings.easter_eggs import EASTER_EGGS
from .utils import (
    define_new_region,
    get_items,
    get_sigma_expert_logic,
    get_sigma_normal_logic,
    get_umbra_variety_logic,
    get_vanilla_logic,
    logical_or_witness_rules,
    parse_witness_rule,
)


class StaticWitnessLogicObj:
    def __init__(self, lines: Optional[List[str]] = None) -> None:
        if lines is None:
            lines = get_sigma_normal_logic()

        # All regions with a list of panels in them and the connections to other regions, before logic adjustments
        self.ALL_REGIONS_BY_NAME: Dict[str, RegionDefinition] = {}
        self.ALL_AREAS_BY_NAME: Dict[str, AreaDefinition] = {}
        self.CONNECTIONS_WITH_DUPLICATES: Dict[str, List[ConnectionDefinition]] = defaultdict(list)
        self.STATIC_CONNECTIONS_BY_REGION_NAME: Dict[str, List[ConnectionDefinition]] = {}

        self.ENTITIES_BY_HEX: Dict[str, Dict[str, Any]] = {}
        self.ENTITIES_BY_NAME: Dict[str, Dict[str, Any]] = {}
        self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX: Dict[str, Dict[str, WitnessRule]] = {}

        self.OBELISK_SIDE_ID_TO_EP_HEXES: Dict[int, Set[int]] = {}

        self.EP_TO_OBELISK_SIDE: Dict[str, str] = {}

        self.ENTITY_ID_TO_NAME: Dict[str, str] = {}

        self.read_logic_file(lines)
        self.reverse_connections()
        self.combine_connections()

    def add_easter_eggs(self) -> None:
        egg_counter = 0
        area_counts: Dict[str, int] = Counter()
        for region_name, entity_amount in EASTER_EGGS.items():
            region_object = self.ALL_REGIONS_BY_NAME[region_name]
            correct_area = region_object.area

            for _ in range(entity_amount):
                location_id = 160200 + egg_counter
                entity_hex = hex(0xEE000 + egg_counter)
                egg_counter += 1

                area_counts[correct_area.name] += 1
                full_entity_name = f"{correct_area.name} Easter Egg {area_counts[correct_area.name]}"

                self.ENTITIES_BY_HEX[entity_hex] = {
                    "checkName": full_entity_name,
                    "entity_hex": entity_hex,
                    "region": region_object,
                    "id": int(location_id),
                    "entityType": "Easter Egg",
                    "locationType": "Easter Egg",
                    "area": correct_area,
                    "order": len(self.ENTITIES_BY_HEX),
                }

                self.ENTITIES_BY_NAME[self.ENTITIES_BY_HEX[entity_hex]["checkName"]] = self.ENTITIES_BY_HEX[entity_hex]

                self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex] = {
                    "entities": frozenset({frozenset({})})
                }
                region_object.logical_entities.append(entity_hex)
                region_object.physical_entities.append(entity_hex)

        easter_egg_region = self.ALL_REGIONS_BY_NAME["Easter Eggs"]
        easter_egg_area = easter_egg_region.area
        for i in range(sum(EASTER_EGGS.values())):
            location_id = 160000 + i
            entity_hex = hex(0xEE200 + i)

            if i == 0:
                continue

            full_entity_name = f"{i + 1} Easter Eggs Collected"

            self.ENTITIES_BY_HEX[entity_hex] = {
                "checkName": full_entity_name,
                "entity_hex": entity_hex,
                "region": easter_egg_region,
                "id": int(location_id),
                "entityType": "Easter Egg Total",
                "locationType": "Easter Egg Total",
                "area": easter_egg_area,
                "order": len(self.ENTITIES_BY_HEX),
            }

            self.ENTITIES_BY_NAME[self.ENTITIES_BY_HEX[entity_hex]["checkName"]] = self.ENTITIES_BY_HEX[entity_hex]

            self.STATIC_DEPENDENT_REQUIREMENTS_BY_HEX[entity_hex] = {
                "entities": frozenset({frozenset({})})
            }
            easter_egg_region.logical_entities.append(entity_hex)
            easter_egg_region.physical_entities.append(entity_hex)

    def read_logic_file(self, lines: List[str]) -> None:
        """
        Reads the logic file and does the initial population of data structures
        """
        current_area = AreaDefinition("Misc")
        current_region = RegionDefinition("Fake", "Fake", current_area)  # Unused, but makes PyCharm & mypy shut up
        self.ALL_AREAS_BY_NAME["Misc"] = current_area

        for line in lines:
            if line == "" or line[0] == "#":
                continue

            if line[-1] == ":":
                new_region_and_connections = define_new_region(line, current_area)
                current_region = new_region_and_connections[0]
                region_name = current_region.name
                self.ALL_REGIONS_BY_NAME[region_name] = current_region
                for connection in new_region_and_connections[1]:
                    self.CONNECTIONS_WITH_DUPLICATES[region_name].append(connection)
                current_area.regions.append(region_name)
                continue

            if line[0] == "=":
                area_name = line[2:-2]
                current_area = AreaDefinition(area_name, [])
                self.ALL_AREAS_BY_NAME[area_name] = current_area
                continue

            line_split = line.split(" - ")

            location_id = line_split.pop(0)

            entity_name_full = line_split.pop(0)

            entity_hex = entity_name_full[0:7]
            entity_name = entity_name_full[9:-1]

            entity_requirement_string = line_split.pop(0)

            full_entity_name = current_region.short_name + " " + entity_name

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
                    "entities": parse_witness_rule(entity_requirement_string)
                }

                # Lasers and Doors exist in a region, but don't have a regional *requirement*
                # If a laser is activated, you don't need to physically walk up to it for it to count
                # As such, logically, they behave more as if they were part of the "Entry" region
                self.ALL_REGIONS_BY_NAME["Entry"].logical_entities.append(entity_hex)
                # However, it will also be important to keep track of their physical location for postgame purposes.
                current_region.physical_entities.append(entity_hex)
                continue

            item_requirement_string = line_split.pop(0)

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

            required_items = parse_witness_rule(item_requirement_string)
            required_entities = parse_witness_rule(entity_requirement_string)

            required_items = frozenset(required_items)

            requirement = {
                "entities": required_entities,
                "items": required_items
            }

            if entity_type == "Obelisk Side":
                eps = set(next(iter(required_entities)))
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

            current_region.logical_entities.append(entity_hex)
            current_region.physical_entities.append(entity_hex)

        self.add_easter_eggs()

    def reverse_connection(self, source_region: str, connection: ConnectionDefinition) -> None:
        # Reverse this connection with all its possibilities, except the ones marked as "OneWay".
        remaining_options: Set[FrozenSet[str]] = set()
        for sub_option in connection.traversal_rule:
            if not any(req == "TrueOneWay" for req in sub_option):
                remaining_options.add(sub_option)

        reversed_connection = ConnectionDefinition(source_region, frozenset(remaining_options))
        if reversed_connection.can_be_traversed:
            self.CONNECTIONS_WITH_DUPLICATES[connection.target_region].append(reversed_connection)

    def reverse_connections(self) -> None:
        # Iterate all connections
        for region_name, connections in list(self.CONNECTIONS_WITH_DUPLICATES.items()):
            for connection in connections:
                self.reverse_connection(region_name, connection)

    def combine_connections(self) -> None:
        # All regions need to be present, and this dict is copied later - Thus, defaultdict is not the correct choice.
        self.STATIC_CONNECTIONS_BY_REGION_NAME = {region_name: [] for region_name in self.ALL_REGIONS_BY_NAME}

        for source, connections in self.CONNECTIONS_WITH_DUPLICATES.items():
            # Organize rules by target region
            traversal_options_by_target_region = defaultdict(list)
            for target_region, traversal_option in connections:
                traversal_options_by_target_region[target_region].append(traversal_option)

            # Combine connections to the same target region into one connection
            for target, traversal_rules in traversal_options_by_target_region.items():
                combined_rule = logical_or_witness_rules(traversal_rules)
                combined_connection = ConnectionDefinition(target, combined_rule)
                self.STATIC_CONNECTIONS_BY_REGION_NAME[source].append(combined_connection)


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
