
from BaseClasses import CollectionState, Item
from .bases import CMTestBase
from ..items import (
    LEGACY_CHESSMEN_GROUP,
    material_items,
    item_name_groups,
)
from ..locations import BoardStage, location_table
from ..rules import determine_difficulty, effective_rule_stage, has_board_stage
import logging


class TestLocationLogic(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collection_state = CollectionState(self.multiworld)
        self.difficulty = determine_difficulty(self.world.options)
        # Initialize locked_items to empty dict
        self.world.locked_items = {}
        
    def create_test_item(self, name: str) -> Item:
        """Helper to create a test item with the given name"""
        return self.world.create_item(name)

    def collect_item_and_get_material(self, item_name: str) -> int:
        """Helper to collect an item and return the material gained"""
        before = self.world.logic_projection.metrics(
            self.collection_state,
            self.player,
            BoardStage.Board8x8,
        ).material
        item = self.create_test_item(item_name)
        self.world.collect(self.collection_state, item)
        after = self.world.logic_projection.metrics(
            self.collection_state,
            self.player,
            BoardStage.Board8x8,
        ).material
        return after - before

    def get_accessible_locations(self) -> set[str]:
        """Helper to get all currently accessible location names"""
        return {loc.name for loc in self.multiworld.get_reachable_locations(self.collection_state, self.player)}

    def get_current_chessmen(self) -> int:
        """Helper to count current chessmen"""
        return self.world.logic_projection.metrics(
            self.collection_state,
            self.player,
            BoardStage.Board8x8,
        ).chessmen

    def assert_locations_accessible(self, material_threshold: int):
        """Assert that all locations with material requirements <= threshold are accessible"""
        accessible = self.get_accessible_locations()
        current_chessmen = self.get_current_chessmen()
        current_material = self.world.logic_projection.metrics(
            self.collection_state, self.player, BoardStage.Board8x8
        ).material
        
        # Special locations that have rules beyond material/chessmen requirements
        special_rule_locations = {
            # Castle locations have special major piece requirements
            "O-O Castle", "O-O-O Castle",
            # Fork locations require pin mechanics
            "Fork, Sacrificial", "Fork, True", "Fork, Sacrificial Triple",
            "Fork, True Triple", "Fork, Sacrificial Royal", "Fork, True Royal",
            # Threat locations require pin mechanics
            "Threaten Minor", "Threaten Major", "Threaten Queen", "Threaten King",
            # Capture Everything adjusts its material requirements based on the goal
            "Capture Everything"
        }
        
        for loc_name, loc_data in location_table.items():
            # Skip special rule locations
            if loc_name in special_rule_locations:
                continue
                
            # Skip locations that require tactics if they're disabled
            if (loc_data.is_tactic is not None and 
                self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_none):
                continue
                
            # Calculate scaled material requirement
            rule_stage = effective_rule_stage(
                loc_name,
                loc_data.required_stage,
                self.world.options.goal.value
                != self.world.options.goal.option_single,
            )
            expanded = (
                self.world.options.goal.value
                != self.world.options.goal.option_single
            )
            material_requirement = loc_data.material_requirement(
                expanded,
                force_grand=(
                    self.world.options.goal.value
                    == self.world.options.goal.option_super
                ),
            )
            scaled_requirement = (
                None
                if material_requirement is None
                else min(
                    material_requirement * self.difficulty,
                    self.world.logic_projection.maximum_material(rule_stage),
                )
            )
            chessmen_requirement = loc_data.chessmen_requirement(expanded)
            
            # Check if location should be accessible
            should_be_accessible = (
                scaled_requirement is not None and
                scaled_requirement <= current_material and  # Meets material requirement
                chessmen_requirement <= current_chessmen and
                has_board_stage(
                    self.collection_state,
                    self.player,
                    rule_stage,
                )
            )
            
            if should_be_accessible:
                self.assertIn(loc_name, accessible, 
                    f"Location {loc_name} with material requirement {scaled_requirement} "
                    f"(base: {material_requirement}, difficulty: {self.difficulty}) "
                    f"and chessmen requirement {chessmen_requirement} "
                    f"should be accessible with current material {current_material} "
                    f"and chessmen {current_chessmen}")
            else:
                self.assertNotIn(loc_name, accessible,
                    f"Location {loc_name} should not be accessible yet. "
                    f"Required: material={scaled_requirement}, chessmen={chessmen_requirement}. "
                    f"Current: material={current_material}, chessmen={current_chessmen}")

    def test_initial_locations_unreachable(self):
        """Test that locations with material requirements start unreachable"""
        accessible = self.get_accessible_locations()
        logging.debug(f"Initial state - Material: {self.collection_state.prog_items[self.player].get('Material', 0)}, Difficulty: {self.difficulty}")
        
        for loc_name, loc_data in location_table.items():
            material_requirement = loc_data.material_requirement(
                self.world.options.goal.value
                != self.world.options.goal.option_single,
                force_grand=(
                    self.world.options.goal.value
                    == self.world.options.goal.option_super
                ),
            )
            chessmen_requirement = loc_data.chessmen_requirement(
                self.world.options.goal.value
                != self.world.options.goal.option_single
            )
            if (
                (material_requirement is not None and material_requirement > 0)
                or chessmen_requirement > 0
            ):
                if loc_name in accessible:
                    logging.debug(f"Location {loc_name} unexpectedly accessible:")
                    logging.debug(f"  Material expectation: {material_requirement}")
                    logging.debug(f"  Chessmen expectation: {chessmen_requirement}")
                    logging.debug(f"  Current chessmen: {self.get_current_chessmen()}")
                self.assertNotIn(loc_name, accessible,
                    f"Location {loc_name} should not be accessible with 0 material and 0 chessmen")

    def test_progressive_material_access(self):
        """Test that locations become accessible as we gain material"""
        current_material = 0
        
        # Split items into categories and sort by material value
        full_chessmen = []
        partial_chessmen = []
        non_chessmen = []
        
        for name, data in material_items.items():
            if name in item_name_groups[LEGACY_CHESSMEN_GROUP]:
                full_chessmen.append((name, data))
            elif name == "Progressive Pocket":
                partial_chessmen.append((name, data))
            else:
                non_chessmen.append((name, data))
                
        # Sort each category by material value
        full_chessmen.sort(key=lambda x: x[1].material)
        partial_chessmen.sort(key=lambda x: x[1].material)
        non_chessmen.sort(key=lambda x: x[1].material)
        
        # Combine lists with full chessmen first, then partial, then non-chessmen
        material_items_sorted = full_chessmen + partial_chessmen + non_chessmen
        
        # Keep adding items until we have enough material for all locations
        max_material = max(
            requirement * self.difficulty
            for loc in location_table.values()
            if (
                requirement := loc.material_requirement(
                    self.world.options.goal.value
                    != self.world.options.goal.option_single,
                    force_grand=(
                        self.world.options.goal.value
                        == self.world.options.goal.option_super
                    ),
                )
            ) is not None
            and requirement > 0
        )
        max_material = min(
            max_material,
            self.world.logic_projection.maximum_material(BoardStage.Board8x8),
        )
                           
        while current_material < max_material:
            # Find next item to add that gives us the least material gain
            for item_name, item_data in material_items_sorted:
                if item_data.material > 0:  # Skip 0 material items
                    material_gain = self.collect_item_and_get_material(item_name)
                    if material_gain > 0:  # If we actually gained material (didn't hit quantity limit)
                        current_material = self.world.logic_projection.metrics(
                            self.collection_state, self.player, BoardStage.Board8x8
                        ).material
                        self.assert_locations_accessible(current_material)
                        break
            else:
                # If we couldn't find any more items to add, we're done
                break

    def test_king_to_center_pawn_access(self):
        """Test that King to Center is accessible with just a pawn"""
        # Initially unreachable
        self.assertFalse("King to Center" in self.get_accessible_locations(),
            "King to Center should be unreachable initially")
        
        # Collect a pawn
        item = self.create_test_item("Progressive Pawn")
        self.world.collect(self.collection_state, item)
        
        # Should now be accessible
        self.assertTrue("King to Center" in self.get_accessible_locations(),
            "King to Center should be accessible with a pawn") 

    def test_capture_everything_access(self):
        """Test that Capture Everything has correct accessibility rules"""
        # Initially unreachable
        self.assertFalse("Capture Everything" in self.get_accessible_locations(),
            "Capture Everything should be unreachable initially")
        
        # Get base material requirement
        base_material = location_table["Capture Everything"].material_expectations
        grand_material = location_table["Capture Everything"].material_expectations_grand
        
        # In current-schema super-sized mode, it requires the 12x10 stage and grand material.
        if self.world.options.goal.value != self.world.options.goal.option_single:
            # Should still be unreachable without Board Files
            self.assertFalse("Capture Everything" in self.get_accessible_locations(),
                "Capture Everything should be unreachable without Super-Size Me in super-sized mode")
            
            # Add Board Files
            super_size = self.create_test_item("Board Files")
            self.world.collect(self.collection_state, super_size)
            
            # Should still be unreachable without enough material
            self.assertFalse("Capture Everything" in self.get_accessible_locations(),
                "Capture Everything should be unreachable without enough material in super-sized mode")
            
            # Add enough material for grand requirement
            target_material = min(
                grand_material * self.difficulty,
                self.world.logic_projection.maximum_material(
                    BoardStage.Board12x10
                ),
            )
            while self.world.logic_projection.metrics(
                    self.collection_state, self.player, BoardStage.Board12x10
            ).material < target_material:
                self.collect_item_and_get_material("Progressive Pawn")
                self.collect_item_and_get_material("Progressive Major Piece")
            
            # Material alone is insufficient until both file unlocks and the first rank unlock arrive.
            self.assertFalse("Capture Everything" in self.get_accessible_locations(),
                "Capture Everything should remain unreachable before the 12x10 stage")
            self.world.collect(self.collection_state, self.create_test_item("Board Files"))
            self.world.collect(self.collection_state, self.create_test_item("Board Ranks"))

            # Should now be accessible
            self.assertTrue("Capture Everything" in self.get_accessible_locations(),
                "Capture Everything should be accessible at 12x10 with enough material in super-sized mode")
        else:
            # In single mode, it just needs base material
            target_material = min(
                base_material * self.difficulty,
                self.world.logic_projection.maximum_material(
                    BoardStage.Board8x8
                ),
            )
            while self.world.logic_projection.metrics(
                    self.collection_state, self.player, BoardStage.Board8x8
            ).material < target_material:
                self.collect_item_and_get_material("Progressive Pawn")
                self.collect_item_and_get_material("Progressive Major Piece")
            
            # Should now be accessible
            self.assertTrue("Capture Everything" in self.get_accessible_locations(),
                "Capture Everything should be accessible with enough material in single mode") 

    def test_geometry_stage_unlock_requirements(self):
        self.assertTrue(has_board_stage(self.collection_state, self.player, BoardStage.Board8x8))
        for stage in list(BoardStage)[1:]:
            self.assertFalse(has_board_stage(self.collection_state, self.player, stage))

        self.world.collect(self.collection_state, self.create_test_item("Super-Size Me"))
        self.assertTrue(has_board_stage(self.collection_state, self.player, BoardStage.Board10x8))
        self.assertFalse(has_board_stage(self.collection_state, self.player, BoardStage.Board10x10))

        self.world.collect(self.collection_state, self.create_test_item("Board Ranks"))
        self.assertTrue(has_board_stage(self.collection_state, self.player, BoardStage.Board10x10))
        self.assertFalse(has_board_stage(self.collection_state, self.player, BoardStage.Board12x10))

        self.world.collect(self.collection_state, self.create_test_item("Board Files"))
        self.assertTrue(has_board_stage(self.collection_state, self.player, BoardStage.Board12x10))
        self.assertFalse(has_board_stage(self.collection_state, self.player, BoardStage.Board12x12))

        self.world.collect(self.collection_state, self.create_test_item("Board Ranks"))
        self.assertTrue(has_board_stage(self.collection_state, self.player, BoardStage.Board12x12))
