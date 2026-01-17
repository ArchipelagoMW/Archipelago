from typing import TYPE_CHECKING, Dict, NamedTuple, List, Set
from BaseClasses import ItemClassification as IC, Item

from ...constants import get_game_base_id

if TYPE_CHECKING:
    from ... import UFO50World


class ItemInfo(NamedTuple):
    id_offset: int
    classification: IC
    quantity: int


item_table: Dict[str, ItemInfo] = {
    "$50": ItemInfo(0, IC.progression, 5),
    "$100": ItemInfo(1, IC.progression, 5),
    "Umbrella": ItemInfo(2, IC.progression, 1),
    "Necklace": ItemInfo(3, IC.progression, 1),
    "Pin": ItemInfo(4, IC.progression | IC.useful, 1),
    "Candy": ItemInfo(5, IC.progression, 1),
    "Wand": ItemInfo(6, IC.progression | IC.useful, 1),
    "Blood Sword": ItemInfo(7, IC.progression, 1),
    "Key": ItemInfo(8, IC.progression, 1),
    "Bat Orb": ItemInfo(9, IC.progression, 1),
    "Trash": ItemInfo(10, IC.filler, 1),
    "Egg": ItemInfo(11, IC.progression, 2),
    "A Broken Wall": ItemInfo(12, IC.progression, 1),
}


# this is for filling out item_name_to_id, it should be static regardless of yaml options
def get_items() -> Dict[str, int]:
    return {f"Barbuta - {name}": data.id_offset + get_game_base_id("Barbuta") for name, data in item_table.items()}


# this should return the item groups for this game, independent of yaml options
# you should include a group that contains all items for this game that is called the same thing as the game
def get_item_groups() -> Dict[str, Set[str]]:
    item_groups: Dict[str, Set[str]] = {"Barbuta": {f"Barbuta - {item_name}" for item_name in item_table.keys()}}
    return item_groups


# for when the world needs to create an item at random (like with random filler items)
# the first argument must be the item name. It must be able to handle the world giving it an actual item name
# the second argument must be the world class
# the third argument is an item classification, `item_class: ItemClassification = None`
# you must put the third argument in, but you are not required to use it
def create_item(item_name: str, world: "UFO50World", item_class: IC = None) -> Item:
    base_id = get_game_base_id("Barbuta")
    if item_name.startswith("Barbuta - "):
        item_name = item_name.split(" - ", 1)[1]
    item_data = item_table[item_name]
    return Item(f"Barbuta - {item_name}", item_class or item_data.classification,
                base_id + item_data.id_offset, world.player)


# for when the world is getting the items to place into the multiworld's item pool
# you must pass in the world class as the argument
def create_items(world: "UFO50World") -> List[Item]:
    items_to_create: Dict[str, int] = {item_name: data.quantity for item_name, data in item_table.items()}
    barbuta_items: List[Item] = []
    for item_name, quantity in items_to_create.items():
        for _ in range(quantity):
            barbuta_items.append(create_item(item_name, world))
    return barbuta_items


def get_filler_item_name(world: "UFO50World") -> str:
    return "Barbuta - Egg"
