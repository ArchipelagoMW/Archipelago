from random import Random
from typing import List

from .bundle import Bundle, BundleTemplate


class BundleRoom:
    name: str
    bundles: List[Bundle]

    def __init__(self, name: str, bundles: List[Bundle]):
        self.name = name
        self.bundles = bundles


class BundleRoomTemplate:
    name: str
    bundles: List[BundleTemplate]
    number_bundles: int

    def __init__(self, name: str, bundles: List[BundleTemplate], number_bundles: int):
        self.name = name
        self.bundles = bundles
        self.number_bundles = number_bundles

    def create_bundle_room(self, price_difference: int, random: Random, allow_island_items: bool):
        filtered_bundles = [bundle for bundle in self.bundles if allow_island_items or not bundle.requires_island]
        chosen_bundles = random.sample(filtered_bundles, self.number_bundles)
        return BundleRoom(self.name, [bundle.create_bundle(price_difference, random, allow_island_items) for bundle in chosen_bundles])
