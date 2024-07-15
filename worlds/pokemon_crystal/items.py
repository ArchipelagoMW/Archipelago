from typing import Dict, FrozenSet, Optional

from BaseClasses import Item, ItemClassification
from .data import data


class PokemonCrystalItem(Item):
    game: str = "Pokemon Crystal"
    tags: FrozenSet[str]

    def __init__(self, name: str, classification: ItemClassification, code: Optional[int], player: int) -> None:
        super().__init__(name, classification, code, player)

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            self.tags = data.items[code].tags


def create_item_label_to_code_map() -> Dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    label_to_code_map: Dict[str, int] = {}
    for item_value, attributes in data.items.items():
        label_to_code_map[attributes.label] = item_value

    return label_to_code_map


def get_item_classification(item_code: int) -> ItemClassification:
    """
    Returns the item classification for a given AP item id (code)
    """
    return data.items[item_code].classification


def item_const_name_to_id(const_name):
    ids = [item_id for item_id, item_data in data.items.items() if item_data.item_const == const_name]
    if len(ids):
        return ids[0] if ids[0] < 256 else ids[0] - 256
    return 0


def item_const_name_to_label(const_name):
    labels = [item_data.label for _item_id, item_data in data.items.items() if item_data.item_const == const_name]
    if len(labels):
        return labels[0]
    return "Poke Ball"


ITEM_GROUPS = {
    "Badges": {
        "Zephyr Badge",
        "Hive Badge",
        "Plain Badge",
        "Fog Badge",
        "Mineral Badge",
        "Storm Badge",
        "Glacier Badge",
        "Rising Badge",

        "Boulder Badge",
        "Cascade Badge",
        "Thunder Badge",
        "Rainbow Badge",
        "Soul Badge",
        "Marsh Badge",
        "Volcano Badge",
        "Earth Badge"
    },
    "Johto Badges": {
        "Zephyr Badge",
        "Hive Badge",
        "Plain Badge",
        "Fog Badge",
        "Mineral Badge",
        "Storm Badge",
        "Glacier Badge",
        "Rising Badge"
    },
    "Kanto Badges": {
        "Boulder Badge",
        "Cascade Badge",
        "Thunder Badge",
        "Rainbow Badge",
        "Soul Badge",
        "Marsh Badge",
        "Volcano Badge",
        "Earth Badge"
    },
    "HMs": {
        "HM01 Cut",
        "HM02 Fly",
        "HM03 Surf",
        "HM04 Strength",
        "HM05 Flash",
        "HM06 Whirlpool",
        "HM07 Waterfall"
    },
    "Gear": {
        "Pokegear",
        "Radio Card",
        "EXPN Card",
        "Map Card"
    },
    "Traps": {
        "Phone Trap",
        "Sleep Trap",
        "Poison Trap",
        "Burn Trap",
        "Freeze Trap",
        "Paralysis Trap"
    },
    "HM01": {"HM01 Cut"},
    "HM02": {"HM02 Fly"},
    "HM03": {"HM03 Surf"},
    "HM04": {"HM04 Strength"},
    "HM05": {"HM05 Flash"},
    "HM06": {"HM06 Whirlpool"},
    "HM07": {"HM07 Waterfall"},
    "TM08": {"TM08 Rock Smash"}
}
