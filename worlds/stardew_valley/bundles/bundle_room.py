from dataclasses import dataclass
from random import Random
from typing import List

from .bundle import Bundle, BundleTemplate
from ..content import StardewContent
from ..options import StardewValleyOptions


@dataclass
class BundleRoom:
    name: str
    bundles: List[Bundle]

    def special_behavior(self, world):
        for bundle in self.bundles:
            bundle.special_behavior(world)


def simplify_name(name: str) -> str:
    return name.lower().replace(" ", "").replace("-", "").replace("_", "").replace(".", "")


# In the context of meme bundles, some of the bundles are directly references to specific people, mostly content creators.
# This ensures that they roll their own bundle as part of their community center.
def is_bundle_related_to_player(bundle: BundleTemplate, player_name: str) -> bool:
    if player_name == "":
        return False
    simple_bundle = simplify_name(bundle.name)
    simple_player = simplify_name(player_name)
    return simple_player in simple_bundle or simple_bundle in simple_player


@dataclass
class BundleRoomTemplate:
    name: str
    bundles: List[BundleTemplate]
    number_bundles: int

    def create_bundle_room(self, random: Random, content: StardewContent, options: StardewValleyOptions, player_name: str = "", is_entire_cc: bool = False):
        filtered_bundles = [bundle for bundle in self.bundles if bundle.can_appear(options)]

        priority_bundles = []
        unpriority_bundles = []
        for bundle in filtered_bundles:
            if options.bundle_plando.prioritizes(bundle.name) or is_bundle_related_to_player(bundle, player_name):
                priority_bundles.append(bundle)
            else:
                unpriority_bundles.append(bundle)

        modifier = options.bundle_per_room.value
        if is_entire_cc:
            modifier *= 6
        number_bundles = self.number_bundles + modifier
        bundles_cap = max(len(filtered_bundles), self.number_bundles)
        number_bundles = max(1, min(bundles_cap, number_bundles))
        if number_bundles <= len(priority_bundles):
            chosen_bundles = random.sample(priority_bundles, number_bundles)
        else:
            chosen_bundles = priority_bundles
            num_remaining_bundles = number_bundles - len(priority_bundles)
            if num_remaining_bundles > len(unpriority_bundles):
                chosen_bundles.extend(random.choices(unpriority_bundles, k=num_remaining_bundles))
            else:
                chosen_bundles.extend(random.sample(unpriority_bundles, num_remaining_bundles))

        return BundleRoom(self.name, [bundle.create_bundle(random, content, options) for bundle in chosen_bundles])
