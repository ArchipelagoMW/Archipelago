from .base_adjustment_classes import AddedItem, DisabledEntity, AddedEvent, RequirementChange, RemoveItem, \
    AddToStartInventory, AddedConnection
from . import static_items as static_witness_items
from . import static_logic as static_witness_logic
from .special_disablings import \
    LONGBOX_POSTGAME_EXCEPT_PATH_TO_CHALLENGE, UNRANDOMIZED_ENTITIES


def build_added_item_adjustment(source_list: list[str]) -> list[AddedItem]:
    return [AddedItem(item_name) for item_name in source_list]


def build_disabled_locations_adjustment(source_list: list[str]) -> list[DisabledEntity]:
    return [DisabledEntity(location_name) for location_name in source_list]


SYMBOL_SHUFFLE = build_added_item_adjustment(static_witness_items.SYMBOL_ITEMS)
LASER_SHUFFLE = build_added_item_adjustment(static_witness_items.LASER_ITEMS)
OBELISK_KEY_SHUFFLE = build_added_item_adjustment(static_witness_items.OBELISK_KEYS)
SHUFFLE_BOAT = build_added_item_adjustment(static_witness_items.BOAT)

INDIVIDUAL_PANEL_SHUFFLE = [
    *build_added_item_adjustment(static_witness_items.INDIVIDUAL_DOOR_PANELS),
    *build_added_item_adjustment(static_witness_items.INDIVIDUAL_CONTROL_PANELS),
]
INDIVIDUAL_DOOR_SHUFFLE = build_added_item_adjustment(static_witness_items.INDIVIDUAL_DOORS)
INDIVIDUAL_MIXED_SHUFFLE = [
    *build_added_item_adjustment(static_witness_items.INDIVIDUAL_DOORS),
    *build_added_item_adjustment(static_witness_items.INDIVIDUAL_CONTROL_PANELS),
]
REGIONAL_PANEL_SHUFFLE = build_added_item_adjustment(static_witness_items.REGIONAL_PANELS)
REGIONAL_DOOR_SHUFFLE = build_added_item_adjustment(static_witness_items.REGIONAL_DOORS)
REGIONAL_MIXED_SHUFFLE = [
    *build_added_item_adjustment(static_witness_items.REGIONAL_DOORS),
    *build_added_item_adjustment(static_witness_items.REGIONAL_CONTROL_PANELS)
]

DISABLE_ECLIPSE = build_disabled_locations_adjustment(["Theater Eclipse EP"])
DISABLE_TEDIOUS_EPS = build_disabled_locations_adjustment([
    "Theater Eclipse EP",
    "Mountainside Cloud Cycle EP",
    "Shipwreck Couch EP",
    "Tunnels Theater Flowers EP",
    "Windmill Second Blade EP",
    "Windmill Third Blade EP",
    "Boat Shipwreck Green EP",
    "Boat Shipwreck CCW Underside EP",
    "Boat Shipwreck CW Underside EP",
    "Boat Tutorial EP",
    "Boat Tutorial Reflection EP",
    "Swamp Rotating Bridge CCW EP",
    "Swamp Rotating Bridge CW EP",
    "Mountain Floor 2 Pink Bridge EP",
    "Mountain Bottom Floor Blue Bridge EP",
    "Mountain Bottom Floor Yellow Bridge EP",
    "Treehouse Beach Both Orange Bridges EP",
])
DISABLE_ALL_EPS = build_disabled_locations_adjustment(
    [name for name, entity in static_witness_logic.ENTITIES_BY_NAME.items() if entity["entityType"] == "EP"]
)
DISABLE_OBELISK_SIDES = build_disabled_locations_adjustment(
    [name for name, entity in static_witness_logic.ENTITIES_BY_NAME.items() if entity["entityType"] == "Obelisk Side"]
)

DISABLE_NON_RANDOMIZED_ENTITIES = ([
    *build_disabled_locations_adjustment(UNRANDOMIZED_ENTITIES),
    AddedEvent("Monastery Laser Activation", "Monastery Laser", ["Symmetry Island Laser Yellow", "Desert Discard", "Treehouse Green Bridge Discard"]),
    AddedEvent("Bunker Laser Activation", "Bunker Laser", ["Outside Tutorial Shed Row 5", "Town Cargo Box Discard", "Mountainside Discard"]),
    AddedEvent("Shadows Laser Activation", "Shadows Laser", ["Outside Tutorial Tree Row 9", "Shipwreck Discard", "Town Rooftop Discard"]),
    AddedEvent("Town Tower 4th Door Opens", "Town Tower 4th Door", ["Outside Tutorial Outpost Discard", "Glass Factory Discard", "Theater Discard"]),
    AddedEvent("Jungle Popup Wall Lifts", "Jungle Popup Wall", ["Treehouse Laser Discard", "Keep Discard", "Jungle Discard", "Jungle Popup Wall Control"]),
    RequirementChange("0x17C65", "0x00A5B | 0x17CE7 | 0x17FA9", None),
    RequirementChange("0x0C2B2", "0x00061 | 0x17D01 | 0x17C42", None),
    RequirementChange("0x181B3",  "0x00021 | 0x17D28 | 0x17C71", None),
    RequirementChange("0x17CAB", "True", None),
    RequirementChange("0x17CA4", "True", None),
    RequirementChange("0x1475B", "0x17FA0 | 0x17D27 | 0x17F9B | 0x17CAB", None),
    RequirementChange("0x2779A", "0x17CFB | 0x3C12B | 0x17CF7", None),
])

DISABLE_REGULAR_DISCARDS = build_disabled_locations_adjustment([
    name for name, entity in static_witness_logic.ENTITIES_BY_NAME.items()
    if entity["locationType"] == "Discard" and entity["checkName"] != "Mountain Bottom Floor Discard"
])
DISABLE_MOUNTAIN_BOTTOM_FLOOR_DISCARD = build_disabled_locations_adjustment(["Mountain Bottom Floor Discard"])

DISABLE_VAULTS = build_disabled_locations_adjustment([
    *[name for name, entity in static_witness_logic.ENTITIES_BY_NAME.items() if entity["locationType"] == "Vault"],
    "Theater Video Input"
])

DISABLE_CAVES_EXCEPT_PATH_TO_CHALLENGE = build_disabled_locations_adjustment(LONGBOX_POSTGAME_EXCEPT_PATH_TO_CHALLENGE)

EARLY_CAVES_ADD_TO_POOL = [
    AddedItem("Caves Shortcuts"),
]

EARLY_CAVES_START_INVENTORY = [
    AddedItem("Caves Shortcuts"),
    AddToStartInventory("Caves Shortcuts"),
    RemoveItem("Caves Mountain Shortcut (Door)"),
    RemoveItem("Caves Swamp Shortcut (Door)"),
]

ENTITY_HUNT = [
    RequirementChange("0x03629", "Entity Hunt", "True"),
    RequirementChange("0x03505", "0x03629", "True"),
    AddedConnection("Tutorial", "Outside Tutorial", "True"),
]

ROTATED_BOX = [
    RequirementChange("0xFFF00", "11 Lasers", "True"),
]

QUARRY_ELEVATOR_COMES_TO_YOU = [
    AddedConnection("Quarry", "Quarry Elevator", "TrueOneWay"),
    AddedConnection("Outside Quarry", "Quarry Elevator", "TruoeOneWay"),
]

BUNKER_ELEVATOR_COMES_TO_YOU = [
    AddedConnection("Outside Bunker", "Bunker Elevator", "TrueOneWay"),
]

SWAMP_LONG_BRIDGE_COMES_TO_YOU = [
    AddedConnection("Outside Swamp", "Swamp Long Bridge", "TrueOneWay"),
    AddedConnection("Swamp Near Boat", "Swamp Long Bridge", "TrueOneWay"),
    RequirementChange("0x035DE", "0x17E2B", "True"), # Swamp Purple Sand Bottom EP
]

TOWN_MAZE_BRIDGE_COMES_TO_YOU = [
    AddedConnection("Town Red Rooftop", "Town Maze Rooftop", "TrueOneWay"),
]
