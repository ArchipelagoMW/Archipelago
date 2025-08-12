from typing import Dict, Callable, TYPE_CHECKING
from BaseClasses import CollectionState, LocationProgressType
from .Options import Goal, PaintingChecksBalancing

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
            "Act 2 - Mycologists Holo Key": self.has_tower_requirements,  # Could need money
            "Act 2 - Ancient Obol": self.has_tower_requirements,  # Need money for the pieces? Use the tower mannequin.
            "Act 3 - Boss Photographer": self.has_inspectometer_battery,
            "Act 3 - Boss Archivist": self.has_battery_and_quill,
            "Act 3 - Boss Unfinished": self.has_gems_and_battery,
            "Act 3 - Boss G0lly": self.has_gems_and_battery,
            "Act 3 - Extra Battery": self.has_inspectometer_battery,  # Hard to miss but soft lock still possible.
            "Act 3 - Nano Armor Generator": self.has_gems_and_battery,  # Costs money, so can need multiple battles.
            "Act 3 - Shop Holo Pelt": self.has_gems_and_battery,  # Costs money, so can need multiple battles.
            "Act 3 - Middle Holo Pelt": self.has_inspectometer_battery,  # Can be reached without but possible soft lock
            "Act 3 - Forest Holo Pelt": self.has_inspectometer_battery,
            "Act 3 - Crypt Holo Pelt": self.has_inspectometer_battery,
            "Act 3 - Tower Holo Pelt": self.has_gems_and_battery,
            "Act 3 - Trader 1": self.has_pelts(1),
            "Act 3 - Trader 2": self.has_pelts(2),
            "Act 3 - Trader 3": self.has_pelts(3),
            "Act 3 - Trader 4": self.has_pelts(4),
            "Act 3 - Trader 5": self.has_pelts(5),
            "Act 3 - Goobert's Painting": self.has_gems_and_battery,
            "Act 3 - The Great Transcendence": self.has_transcendence_requirements,
            "Act 3 - Boss Mycologists": self.has_mycologists_boss_requirements,
            "Act 3 - Bone Lord Room": self.has_bone_lord_room_requirements,
            "Act 3 - Luke's File Entry 1": self.has_battery_and_quill,
            "Act 3 - Luke's File Entry 2": self.has_battery_and_quill,
            "Act 3 - Luke's File Entry 3": self.has_battery_and_quill,
            "Act 3 - Luke's File Entry 4": self.has_transcendence_requirements,
            "Act 3 - Well": self.has_inspectometer_battery,
            "Act 3 - Gems Drone": self.has_inspectometer_battery,
            "Act 3 - Clock": self.has_gems_and_battery,  # Can be brute-forced, but the solution needs those items.
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

    def has_useful_act1_items(self, state: CollectionState) -> bool:
        return state.has_all(("Oil Painting's Clover Plant", "Squirrel Totem Head"), self.player)

    def has_all_epitaph_pieces(self, state: CollectionState) -> bool:
        return state.has(self.world.required_epitaph_pieces_name, self.player, self.world.required_epitaph_pieces_count)

    def has_camera_and_meat(self, state: CollectionState) -> bool:
        return state.has_all(("Camera Replica", "Pile Of Meat"), self.player)

    def has_monocle(self, state: CollectionState) -> bool:
        return state.has("Monocle", self.player)

    def has_obol(self, state: CollectionState) -> bool:
        return state.has("Ancient Obol", self.player)

    def has_epitaphs_and_forest_items(self, state: CollectionState) -> bool:
        return self.has_camera_and_meat(state) and self.has_all_epitaph_pieces(state)

    def has_act2_bridge_requirements(self, state: CollectionState) -> bool:
        return self.has_camera_and_meat(state) or self.has_all_epitaph_pieces(state)

    def has_tower_requirements(self, state: CollectionState) -> bool:
        return self.has_monocle(state) and self.has_act2_bridge_requirements(state)

    def has_inspectometer_battery(self, state: CollectionState) -> bool:
        return state.has("Inspectometer Battery", self.player)

    def has_gems_and_battery(self, state: CollectionState) -> bool:
        return state.has("Gems Module", self.player) and self.has_inspectometer_battery(state)

    def has_pelts(self, count: int) -> Callable[[CollectionState], bool]:
        return lambda state: state.has("Holo Pelt", self.player, count) and self.has_gems_and_battery(state)

    def has_mycologists_boss_requirements(self, state: CollectionState) -> bool:
        return state.has("Mycologists Holo Key", self.player) and self.has_transcendence_requirements(state)

    def has_bone_lord_room_requirements(self, state: CollectionState) -> bool:
        return state.has("Bone Lord Holo Key", self.player) and self.has_inspectometer_battery(state)

    def has_battery_and_quill(self, state: CollectionState) -> bool:
        return state.has("Quill", self.player) and self.has_inspectometer_battery(state)

    def has_transcendence_requirements(self, state: CollectionState) -> bool:
        return state.has("Quill", self.player) and self.has_gems_and_battery(state)

    def has_act2_requirements(self, state: CollectionState) -> bool:
        return state.has("Film Roll", self.player)

    def has_act3_requirements(self, state: CollectionState) -> bool:
        return self.has_act2_requirements(state) and self.has_all_epitaph_pieces(state) and \
            self.has_camera_and_meat(state) and self.has_monocle(state)

    def has_epilogue_requirements(self, state: CollectionState) -> bool:
        return self.has_act3_requirements(state) and self.has_transcendence_requirements(state)

    def set_all_rules(self) -> None:
        multiworld = self.world.multiworld
        if self.world.options.goal != Goal.option_first_act:
            multiworld.completion_condition[self.player] = self.has_epilogue_requirements
        else:
            multiworld.completion_condition[self.player] = self.has_act2_requirements
        for region in multiworld.get_regions(self.player):
            if self.world.options.goal == Goal.option_full_story_in_order:
                if region.name in self.region_rules:
                    for entrance in region.entrances:
                        entrance.access_rule = self.region_rules[region.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]

        if self.world.options.painting_checks_balancing == PaintingChecksBalancing.option_balanced:
            self.world.get_location("Act 1 - Painting 2").access_rule = self.has_useful_act1_items
            self.world.get_location("Act 1 - Painting 3").access_rule = self.has_useful_act1_items
        elif self.world.options.painting_checks_balancing == PaintingChecksBalancing.option_force_filler:
            self.world.get_location("Act 1 - Painting 2").progress_type = LocationProgressType.EXCLUDED
            self.world.get_location("Act 1 - Painting 3").progress_type = LocationProgressType.EXCLUDED
