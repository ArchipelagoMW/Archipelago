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
            "Act 1 - Wardrobe Drawer 1": self.has_wardrobe_key,
            "Act 1 - Wardrobe Drawer 2": self.has_wardrobe_key,
            "Act 1 - Wardrobe Drawer 3": self.has_wardrobe_key,
            "Act 1 - Wardrobe Drawer 4": self.has_wardrobe_key,
            "Act 1 - Dagger": self.has_caged_wolf,
            "Act 1 - Magnificus Eye": self.has_dagger,
            "Act 1 - Clock Main Compartment": self.has_magnificus_eye,
            "Act 2 - Battle Prospector": self.has_camera_and_meat,
            "Act 2 - Battle Angler": self.has_camera_and_meat,
            "Act 2 - Battle Trapper": self.has_camera_and_meat,
            "Act 2 - Battle Pike Mage": self.has_tower_requirements,
            "Act 2 - Battle Goobert": self.has_tower_requirements,
            "Act 2 - Battle Lonely Wizard": self.has_tower_requirements,
            "Act 2 - Battle Inspector": self.has_act2_bridge_requirements,
            "Act 2 - Battle Melter": self.has_act2_bridge_requirements,
            "Act 2 - Battle Dredger": self.has_act2_bridge_requirements,
            "Act 2 - Forest Meadow Chest": self.has_camera_and_meat,
            "Act 2 - Tower Chest 1": self.has_act2_bridge_requirements,
            "Act 2 - Tower Chest 2": self.has_tower_requirements,
            "Act 2 - Tower Chest 3": self.has_tower_requirements,
            "Act 2 - Tentacle": self.has_tower_requirements,
            "Act 2 - Factory Trash Can": self.has_act2_bridge_requirements,
            "Act 2 - Factory Drawer 1": self.has_act2_bridge_requirements,
            "Act 2 - Factory Drawer 2": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 1": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 2": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 3": self.has_act2_bridge_requirements,
            "Act 2 - Factory Chest 4": self.has_act2_bridge_requirements,
            "Act 2 - Monocle": self.has_act2_bridge_requirements,
            "Act 2 - Boss Grimora": self.has_all_epitaph_pieces,
            "Act 2 - Boss Leshy": self.has_camera_and_meat,
            "Act 2 - Boss Magnificus": self.has_tower_requirements,
            "Act 2 - Boss P03": self.has_act2_bridge_requirements,
            "Act 2 - Bone Lord Femur": self.has_obol,
            "Act 2 - Bone Lord Horn": self.has_obol,
            "Act 2 - Bone Lord Holo Key": self.has_obol,
            "Act 2 - Mycologists Holo Key": self.has_epitaphs_and_forest_items,
            "Act 2 - Ancient Obol": self.has_tower_requirements,
            "Act 3 - Boss Photographer": self.has_inspectometer_battery,
            "Act 3 - Boss Archivist": self.has_inspectometer_battery,
            "Act 3 - Boss Unfinished": self.has_drone_and_battery,
            "Act 3 - Boss G0lly": self.has_drone_and_battery,
            "Act 3 - Trader 1": self.has_one_pelt,
            "Act 3 - Trader 2": self.has_two_pelt,
            "Act 3 - Trader 3": self.has_three_pelt,
            "Act 3 - Trader 4": self.has_four_pelt,
            "Act 3 - Trader 5": self.has_five_pelt,
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

    def has_all_epitaph_pieces(self, state: CollectionState) -> bool:
        return state.has("Epitaph Piece 1", self.player) and \
            state.has("Epitaph Piece 2", self.player) and state.has("Epitaph Piece 3", self.player) and \
            state.has("Epitaph Piece 4", self.player) and state.has("Epitaph Piece 5", self.player) and \
            state.has("Epitaph Piece 6", self.player) and state.has("Epitaph Piece 7", self.player) and \
            state.has("Epitaph Piece 8", self.player) and state.has("Epitaph Piece 9", self.player)

    def has_camera_and_meat(self, state: CollectionState) -> bool:
        return state.has("Camera Replica", self.player) and state.has("Pile Of Meat", self.player)

    def has_monocle(self, state: CollectionState) -> bool:
        return state.has("Monocle", self.player)

    def has_obol(self, state: CollectionState) -> bool:
        return state.has("Ancient Obol", self.player)

    def has_epitaphs_and_forest_items(self, state: CollectionState) -> bool:
        return self.has_camera_and_meat(state) and self.has_all_epitaph_pieces(state)

    def has_act2_bridge_requirements(self, state: CollectionState) -> bool:
        return self.has_camera_and_meat(state) or self.has_all_epitaph_pieces(state)

    def has_tower_requirements(self, state: CollectionState) -> bool:
        return self.has_act2_bridge_requirements(state) and self.has_monocle(state)

    def has_inspectometer_battery(self, state: CollectionState) -> bool:
        return state.has("Inspectometer Battery", self.player)

    def has_drone_and_battery(self, state: CollectionState) -> bool:
        return state.has("Gem Drone", self.player) and self.has_inspectometer_battery(state)

    def has_pelts(self, state: CollectionState, count: int) -> bool:
        return state.has("Holo Pelt", self.player, count)

    def has_one_pelt(self, state: CollectionState) -> bool:
        return self.has_pelts(state, 1)

    def has_two_pelt(self, state: CollectionState) -> bool:
        return self.has_pelts(state, 2)

    def has_three_pelt(self, state: CollectionState) -> bool:
        return self.has_pelts(state, 3)

    def has_four_pelt(self, state: CollectionState) -> bool:
        return self.has_pelts(state, 4)

    def has_five_pelt(self, state: CollectionState) -> bool:
        return self.has_pelts(state, 5)

    def has_act2_requirements(self, state: CollectionState) -> bool:
        return state.has("Film Roll", self.player)

    def has_act3_requirements(self, state: CollectionState) -> bool:
        return self.has_act2_requirements(state) and self.has_all_epitaph_pieces(state) and \
            self.has_camera_and_meat(state) and self.has_monocle(state)

    def has_epilogue_requirements(self, state: CollectionState) -> bool:
        # TODO Add the missing checks
        return self.has_act3_requirements(state) and self.has_drone_and_battery(state)

    def set_all_rules(self) -> None:
        multiworld = self.world.multiworld
        multiworld.completion_condition[self.player] = self.has_epilogue_requirements
        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]

