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
    region_rules: Dict[str, Callable[[CollectionState], bool]]

    def __init__(self, world: InscryptionWorld) -> None:
        self.player = world.player
        self.world = world
        self.location_rules = {
            "Act 1 Wardrobe Drawer 1": self.has_wardrobe_key,
            "Act 1 Wardrobe Drawer 2": self.has_wardrobe_key,
            "Act 1 Wardrobe Drawer 3": self.has_wardrobe_key,
            "Act 1 Wardrobe Drawer 4": self.has_wardrobe_key,
            "Act 1 Dagger": self.has_caged_wolf,
            "Act 1 Magnificus Eye": self.has_dagger,
            "Act 1 Cabin Clock Main Compartment": self.has_magnificus_eye
        }
        self.region_rules = {
            "Act 2": self.has_act2_requirements,
            "Act 3": self.has_act3_requirements,
            "Epilogue": self.has_epilogue_requirements
        }

    def has_wardrobe_key(self, state: CollectionState) -> bool:
        return state.has("Wardrobe Key", self.player)

    def has_caged_wolf(self, state: CollectionState) -> bool:
        return state.has("Caged Wolf Card", self.player)

    def has_dagger(self, state: CollectionState) -> bool:
        return state.has("Dagger", self.player)

    def has_magnificus_eye(self, state: CollectionState) -> bool:
        return state.has("Magnificus Eye", self.player)

    def has_act2_requirements(self, state: CollectionState) -> bool:
        return state.has("Film Roll", self.player)

    def has_act3_requirements(self, state: CollectionState) -> bool:
        return self.has_act2_requirements(state) and state.has("Epitaph Piece 1", self.player) and \
            state.has("Epitaph Piece 2", self.player) and state.has("Epitaph Piece 3", self.player) and \
            state.has("Epitaph Piece 4", self.player) and state.has("Epitaph Piece 5", self.player) and \
            state.has("Epitaph Piece 6", self.player) and state.has("Epitaph Piece 7", self.player) and \
            state.has("Epitaph Piece 8", self.player) and state.has("Epitaph Piece 9", self.player)

    def has_epilogue_requirements(self, state: CollectionState) -> bool:
        # TODO Had the missing checks
        return self.has_act2_requirements(state) and self.has_act3_requirements(state)

    def set_all_rules(self) -> None:
        multiworld = self.world.multiworld
        #TODO Change this to the real completion check
        multiworld.completion_condition[self.player] = self.has_epilogue_requirements
        for region in multiworld.get_regions(self.player):
            if region in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]

