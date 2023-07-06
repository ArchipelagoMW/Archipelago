from typing import Dict, List, Callable, TYPE_CHECKING
from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import InscryptionWorld
else:
    InscryptionWorld = object


# Based on The Messenger's implementation
class InscryptionRules:
    player: int
    world: InscryptionWorld
    location_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: InscryptionWorld) -> None:
        self.player = world.player
        self.world = world
        self.location_rules = {
            "Wardrobe Drawer 1": self.has_wardrobe_key,
            "Wardrobe Drawer 2": self.has_wardrobe_key,
            "Wardrobe Drawer 3": self.has_wardrobe_key,
            "Wardrobe Drawer 4": self.has_wardrobe_key,
            "Dagger": self.has_caged_wolf,
            "Magnificus Eye": self.has_dagger,
            "Cabin Clock Main Compartment": self.has_magnificus_eye
        }

    def has_wardrobe_key(self, state: CollectionState) -> bool:
        return state.has("Wardrobe Key", self.player)

    def has_caged_wolf(self, state: CollectionState) -> bool:
        return state.has("Caged Wolf Card", self.player)

    def has_dagger(self, state: CollectionState) -> bool:
        return state.has("Dagger", self.player)

    def has_magnificus_eye(self, state: CollectionState) -> bool:
        return state.has("Magnificus Eye", self.player)

    def set_location_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]
