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

    def create_bundle_room(self, random: Random, content: StardewContent, options: StardewValleyOptions):
        filtered_bundles = [bundle for bundle in self.bundles if bundle.can_appear(options)]

        priority_bundles = []
        unpriority_bundles = []
        for bundle in filtered_bundles:
            if bundle.name in options.bundle_plando:
                priority_bundles.append(bundle)
            else:
                unpriority_bundles.append(bundle)

        if self.number_bundles <= len(priority_bundles):
            chosen_bundles = random.sample(priority_bundles, self.number_bundles)
        else:
            chosen_bundles = priority_bundles
            num_remaining_bundles = self.number_bundles - len(priority_bundles)
            if num_remaining_bundles > len(unpriority_bundles):
                chosen_bundles.extend(random.choices(unpriority_bundles, k=num_remaining_bundles))
            else:
                chosen_bundles.extend(random.sample(unpriority_bundles, num_remaining_bundles))

        return BundleRoom(self.name, [bundle.create_bundle(random, content, options) for bundle in chosen_bundles])
