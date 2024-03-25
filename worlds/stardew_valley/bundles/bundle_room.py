from dataclasses import dataclass
from random import Random
from typing import List

from .bundle import Bundle, BundleTemplate
from ..content import StardewContent
from ..options import BundlePrice, StardewValleyOptions


@dataclass
class BundleRoom:
    name: str
    bundles: List[Bundle]


@dataclass
class BundleRoomTemplate:
    name: str
    bundles: List[BundleTemplate]
    number_bundles: int

    def create_bundle_room(self, bundle_price_option: BundlePrice, random: Random, content: StardewContent, options: StardewValleyOptions):
        filtered_bundles = [bundle for bundle in self.bundles if bundle.can_appear(options)]

        if self.number_bundles > len(filtered_bundles):
            chosen_bundles = random.choices(filtered_bundles, k=self.number_bundles)
        else:
            chosen_bundles = random.sample(filtered_bundles, self.number_bundles)

        return BundleRoom(self.name, [bundle.create_bundle(bundle_price_option, random, content, options) for bundle in chosen_bundles])
