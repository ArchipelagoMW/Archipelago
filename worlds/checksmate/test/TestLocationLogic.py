from typing import List, Dict, Set, Tuple
from BaseClasses import CollectionState, Item, ItemClassification
from . import CMTestBase
from ..Items import item_table, material_items, item_name_groups
from ..Locations import location_table
from ..Rules import determine_difficulty


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
        self.world.collect(self.collection_state, item)
        return item_table[item_name].material if item_name in item_table else 0

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
        
        for loc_name, loc_data in location_table.items():
            # Skip locations that require tactics if they're disabled
            if (loc_data.is_tactic is not None and 
                self.world.options.enable_tactics.value == self.world.options.enable_tactics.option_none):
                continue
                
            # Calculate scaled material requirement
            scaled_requirement = loc_data.material_expectations_grand * self.difficulty
            
            # Check if location should be accessible
            should_be_accessible = (
                loc_data.material_expectations != -1 and  # Not a super-size only location
                scaled_requirement <= current_material and  # Meets material requirement
                loc_data.chessmen_expectations <= current_chessmen  # Meets chessmen requirement
            )
            
            if should_be_accessible:
                self.assertIn(loc_name, accessible, 
                    f"Location {loc_name} with material requirement {scaled_requirement} "
                    f"(base: {loc_data.material_expectations_grand}, difficulty: {self.difficulty}) "
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
        for loc_name, loc_data in location_table.items():
            if (loc_data.material_expectations_grand > 0 or 
                loc_data.chessmen_expectations > 0):
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
        max_material = max(loc.material_expectations_grand * self.difficulty
                           for loc in location_table.values() 
                           if loc.material_expectations_grand > 0)
                           
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