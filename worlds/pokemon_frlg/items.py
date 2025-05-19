from typing import TYPE_CHECKING, Dict
from BaseClasses import Item, ItemClassification
from .data import data
from .groups import item_groups

if TYPE_CHECKING:
    from . import PokemonFRLGWorld


class PokemonFRLGItem(Item):
    game: str = "Pokemon FireRed and LeafGreen"

    def __init__(self, name: str, classification: ItemClassification, code: int | None, player: int) -> None:
        super().__init__(name, classification, code, player)


def create_item_name_to_id_map() -> Dict[str, int]:
    """
    Creates a map from item names to their AP item ID (code)
    """
    name_to_id_map: Dict[str, int] = {}
    for item_id, item_data in data.items.items():
        name_to_id_map[item_data.name] = item_id

    return name_to_id_map


def get_item_classification(item_id: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[item_id].classification


def get_random_item(world: "PokemonFRLGWorld", item_classification: ItemClassification = None) -> str:
    if item_classification is None:
        item_classification = ItemClassification.useful if world.random.random() < 0.20 else ItemClassification.filler
    items = [item for item in data.items.values()
             if item.classification == item_classification and item.name not in item_groups["Unique Items"]]
    return world.random.choice(items).name
