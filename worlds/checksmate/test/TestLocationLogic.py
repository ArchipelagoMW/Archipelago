from typing import List, Dict, Set, Tuple
from BaseClasses import CollectionState, Item, ItemClassification
from . import CMTestBase
from ..Items import item_table, material_items, item_name_groups
from ..Locations import location_table
from ..Rules import determine_difficulty
import logging


class TestLocationLogic(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collection_state = CollectionState(self.multiworld)
        self.difficulty = determine_difficulty(self.world.options)
        
    def create_test_item(self, name: str) -> Item:
        """Helper to create a test item with the given name"""
        return Item(name, ItemClassification.progression, self.player, item_table[name])

    def collect_item_and_get_material(self, item_name: str) -> int:
        """Helper to collect an item and return the material gained"""
        item = self.create_test_item(item_name)
        # Only collect through world to ensure proper state updates
        material_gain = self.world._collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        return material_gain

    def get_accessible_locations(self) -> Set[str]:
        """Helper to get all currently accessible location names"""
        return {loc.name for loc in self.multiworld.get_reachable_locations(self.collection_state, self.player)}

    def get_current_chessmen(self) -> int:
        """Helper to count current chessmen"""
        chessmen = 0
        for item_name in item_name_groups["Chessmen"]:
            chessmen += self.collection_state.prog_items[self.player].get(item_name, 0)
        # Pockets count as partial chessmen (0.5 each)
        pocket_count = self.collection_state.prog_items[self.player].get("Progressive Pocket", 0)
        chessmen += pocket_count // 2
        return chessmen

    def assert_locations_accessible(self, material_threshold: int):
        """Assert that all locations with material requirements <= threshold are accessible"""
        accessible = self.get_accessible_locations()
        current_chessmen = self.get_current_chessmen()
        current_material = self.collection_state.prog_items[self.player].get("Material", 0)
        
        # Special locations that have rules beyond material/chessmen requirements
        special_rule_locations = {
            # Castle locations have special major piece requirements
            "O-O Castle", "O-O-O Castle",
            # Fork locations require pin mechanics
            "Fork, Sacrificial", "Fork, True", "Fork, Sacrificial Triple",
            "Fork, True Triple", "Fork, Sacrificial Royal", "Fork, True Royal",
            # Threat locations require pin mechanics
            "Threaten Minor", "Threaten Major", "Threaten Queen", "Threaten King"
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
            scaled_requirement = loc_data.material_expectations * self.difficulty
            
            # Check if location should be accessible
            should_be_accessible = (
                loc_data.material_expectations != -1 and  # Not a super-size only location
                scaled_requirement <= current_material and  # Meets material requirement
                loc_data.chessmen_expectations <= current_chessmen  # Meets chessmen requirement
            )
            
            if should_be_accessible:
                self.assertIn(loc_name, accessible, 
                    f"Location {loc_name} with material requirement {scaled_requirement} "
                    f"(base: {loc_data.material_expectations}, difficulty: {self.difficulty}) "
                    f"and chessmen requirement {loc_data.chessmen_expectations} "
                    f"should be accessible with current material {current_material} "
                    f"and chessmen {current_chessmen}")
            else:
                self.assertNotIn(loc_name, accessible,
                    f"Location {loc_name} should not be accessible yet. "
                    f"Required: material={scaled_requirement}, chessmen={loc_data.chessmen_expectations}. "
                    f"Current: material={current_material}, chessmen={current_chessmen}")

    def test_initial_locations_unreachable(self):
        """Test that locations with material requirements start unreachable"""
        accessible = self.get_accessible_locations()
        logging.debug(f"Initial state - Material: {self.collection_state.prog_items[self.player].get('Material', 0)}, Difficulty: {self.difficulty}")
        
        for loc_name, loc_data in location_table.items():
            if (loc_data.material_expectations > 0 or 
                  loc_data.chessmen_expectations > 0):
                if loc_name in accessible:
                    logging.debug(f"Location {loc_name} unexpectedly accessible:")
                    logging.debug(f"  Material expectation: {loc_data.material_expectations}")
                    logging.debug(f"  Scaled requirement: {loc_data.material_expectations * self.difficulty}")
                    logging.debug(f"  Chessmen expectation: {loc_data.chessmen_expectations}")
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
            if name in item_name_groups["Chessmen"]:
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
        max_material = max(loc.material_expectations * self.difficulty
                           for loc in location_table.values() 
                           if loc.material_expectations > 0)
                           
        while current_material < max_material:
            # Find next item to add that gives us the least material gain
            for item_name, item_data in material_items_sorted:
                if item_data.material > 0:  # Skip 0 material items
                    material_gain = self.collect_item_and_get_material(item_name)
                    if material_gain > 0:  # If we actually gained material (didn't hit quantity limit)
                        current_material = self.collection_state.prog_items[self.player].get("Material", 0)
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
