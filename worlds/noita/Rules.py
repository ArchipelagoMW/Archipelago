from BaseClasses import MultiWorld
from typing import List, Set

from ..generic import Rules as GenericRules
from . import Locations, Items, Regions


holy_mountain_regions: List[str] = [
    "Holy Mountain 1 (To Coal Pits)",
    "Holy Mountain 2 (To Snowy Depths)",
    "Holy Mountain 3 (To Hiisi Base)",
    "Holy Mountain 4 (To Underground Jungle)",
    "Holy Mountain 5 (To The Vault)",
    "Holy Mountain 6 (To Temple of the Art)",
    "Holy Mountain 7 (To The Laboratory)",
]

wand_tiers: List[str] = [
    "Wand (Tier 1)",
    "Wand (Tier 2)",
    "Wand (Tier 3)",
    "Wand (Tier 4)",
    "Wand (Tier 5)",
    "Wand (Tier 6)",
]

items_hidden_from_shops: Set[str] = {"Gold (10)", "Gold (50)", "Gold (200)", "Gold (1000)", "Potion", "Random Potion",
                                     "Secret Potion", "Chaos Die", "Greed Die", "Kammi", "Refreshing Gourd", "Sadekivi",
                                     "Broken Wand", "Powder Pouch"}


def forbid_items_at_location(world: MultiWorld, location_name: str, items: Set[str], player: int):
    location = world.get_location(location_name, player)
    GenericRules.forbid_items_for_player(location, items, player)
