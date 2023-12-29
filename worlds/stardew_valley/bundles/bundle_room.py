from dataclasses import dataclass
from random import Random
from typing import List

from .bundle import Bundle, BundleTemplate
from ..options import BundlePrice


@dataclass
class BundleRoom:
    name: str
    bundles: List[Bundle]


@dataclass
class BundleRoomTemplate:
    name: str
    bundles: List[BundleTemplate]
    number_bundles: int

    def create_bundle_room(self, bundle_price_option: BundlePrice, random: Random, allow_island_items: bool):
        filtered_bundles = [bundle for bundle in self.bundles if allow_island_items or not bundle.requires_island]
        chosen_bundles = random.sample(filtered_bundles, self.number_bundles)
        return BundleRoom(self.name, [bundle.create_bundle(bundle_price_option, random, allow_island_items) for bundle in chosen_bundles])
