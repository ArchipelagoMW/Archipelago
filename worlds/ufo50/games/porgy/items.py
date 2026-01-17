from typing import TYPE_CHECKING, Dict, NamedTuple, List, Set, Optional
from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id
from ...options import PorgyRadar

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int
    group: Optional[str] = None


item_table: Dict[str, ItemInfo] = {
    "Torpedo Upgrade": ItemInfo(300, IC.progression, 20),
    "Fuel Tank": ItemInfo(301, IC.progression, 20),
    "Fish Gratitude": ItemInfo(302, IC.progression, 20),
    # modules
    "Missile System Module": ItemInfo(191, IC.progression, 1, "Modules"),
    "Radar System Module": ItemInfo(291, IC.progression, 1, "Modules"),
    "Buster Torpedoes Module": ItemInfo(90, IC.progression, 1, "Modules"),
    "Depth Charge Module": ItemInfo(92, IC.progression, 1, "Modules"),
    "Efficient Fuel Module": ItemInfo(290, IC.progression, 1, "Modules"),
    "Armor Plating Module": ItemInfo(292, IC.useful, 1, "Modules"),
    "Super Booster Module": ItemInfo(93, IC.useful, 1, "Modules"),
    "Spotlight Module": ItemInfo(192, IC.progression, 1, "Modules"),
    "Drill Module": ItemInfo(91, IC.progression, 1, "Modules"),
    "Targeting System Module": ItemInfo(190, IC.useful, 1, "Modules"),

    # the mcguffins
    "Strange Light": ItemInfo(303, IC.progression_skip_balancing, 5),
}


# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> Dict[str, int]:
    return {f"Porgy - {name}": data.id_offset + get_game_base_id("Porgy") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
def get_item_groups() -> Dict[str, Set[str]]:
    item_groups: Dict[str, Set[str]] = {"Porgy": {f"Porgy - {item_name}" for item_name in item_table.keys()}}
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Porgy")
    if item_name.startswith("Porgy - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Porgy - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
def create_items(world: "UFO50World") -> List[Item]:
    items_to_create: Dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    porgy_items: List[Item] = []
    if world.options.porgy_radar == PorgyRadar.option_always_on:
        items_to_create["Radar System Module"] = 0
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            porgy_items.append(create_item(item_name, world))
    return porgy_items


filler_items = ["Porgy - Fuel Tank", "Porgy - Torpedo Upgrade"]


def get_filler_item_name(world: "UFO50World") -> str:
    return world.random.choice(filler_items)
