from BaseClasses import CollectionState, Item, ItemClassification
from ..Items import item_table
from . import CMTestBase
import random

class TestCollectionState(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collection_state = CollectionState(self.multiworld)
        self.cm_collection_state = self.world._collection_state
        
    def create_test_item(self, name: str) -> Item:
        """Helper to create a test item with the given name"""
        return Item(name, ItemClassification.progression, self.player, item_table[name])
        
    def get_expected_material_loss(self, item_name: str) -> int:
        """Calculate expected material loss based on current state and upgrades"""
        if item_name == "Progressive Major Piece":
            # If we have a queen upgrade, removing the major piece actually removes a queen
            queens = self.collection_state.prog_items[self.player].get("Progressive Major To Queen", 0)
            majors = self.collection_state.prog_items[self.player].get("Progressive Major Piece", 0)
            if queens > 0 and majors <= queens:
                # This major piece was upgraded to a queen
                return item_table["Progressive Major To Queen"].material + item_table["Progressive Major Piece"].material
            return item_table[item_name].material
        elif item_name == "Progressive Major To Queen":
            # Queen upgrade has no value without a major piece to upgrade
            majors = self.collection_state.prog_items[self.player].get("Progressive Major Piece", 0)
            queens = self.collection_state.prog_items[self.player].get("Progressive Major To Queen", 0)
            if majors < queens:  # If we have more queen upgrades than pieces to upgrade
                return 0  # This upgrade isn't being used
            return item_table[item_name].material
        return item_table[item_name].material
        
    def test_collect_beyond_quantity(self):
        """Test that collecting items beyond their quantity limit doesn't affect material"""
        # Test with Progressive King Promotion which has quantity=2
        item = self.create_test_item("Progressive King Promotion")
        
        # First collection should count
        material1 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertGreater(material1, 0)
        
        # Second collection should count
        material2 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertGreater(material2, 0)
        
        # Third collection should not count due to quantity limit
        material3 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertEqual(material3, 0)
        
    def test_remove_beyond_quantity(self):
        """Test that removing items beyond their quantity limit doesn't affect material"""
        # Set up initial state with 3 Progressive King Promotions
        item = self.create_test_item("Progressive King Promotion")
        
        # Add 3 items first
        self.cm_collection_state.collect(self.collection_state, item)
        self.cm_collection_state.collect(self.collection_state, item)
        self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        
        # First removal should not count (going from 3->2)
        material1 = self.cm_collection_state.remove(self.collection_state, item)
        self.world.remove(self.collection_state, item)
        self.assertEqual(material1, 0)
        
        # Second removal should count (going from 2->1)
        material2 = self.cm_collection_state.remove(self.collection_state, item)
        self.world.remove(self.collection_state, item)
        self.assertGreater(material2, 0)
        
        # Third removal should count (going from 1->0)
        material3 = self.cm_collection_state.remove(self.collection_state, item)
        self.world.remove(self.collection_state, item)
        self.assertGreater(material3, 0)
        
    def test_pocket_limit_interaction(self):
        """Test that Progressive Pocket respects pocket limit"""
        # Set up a world with pocket_limit_by_pocket = 1 and max_pocket = 3
        self.world.options.pocket_limit_by_pocket.value = 1
        self.world.options.max_pocket.value = 3
        item = self.create_test_item("Progressive Pocket")
        
        # First collection should count
        material1 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertGreater(material1, 0)
        
        # Second collection should count
        material2 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertGreater(material2, 0)

        # Third collection should count
        material3 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertGreater(material3, 0)

        # Fourth collection should not count due to pocket limit
        material4 = self.cm_collection_state.collect(self.collection_state, item)
        self.world.collect(self.collection_state, item)
        self.assertEqual(material4, 0)

    def test_random_collect_remove(self):
        """Test collecting and removing items in random order to verify state consistency"""
        # Create list of all items that have material value
        material_items = {name: data for name, data in item_table.items() if data.material > 0}
        material_items_list = list(material_items.items())
        
        # Track what we expect to have
        expected_material = 0
        collected_items = []
        
        # First collect items in random order
        random.shuffle(material_items_list)
        for item_name, item_data in material_items_list:
            # Collect the item
            item = self.create_test_item(item_name)
            material_gain = self.cm_collection_state.collect(self.collection_state, item)
            self.world.collect(self.collection_state, item)
            
            if material_gain > 0:  # If we actually gained material (didn't hit quantity limit)
                expected_material += material_gain
                collected_items.append(item_name)
                
            # Verify material matches expectations
            actual_material = self.collection_state.prog_items[self.player].get("Material", 0)
            self.assertEqual(expected_material, actual_material,
                f"Material mismatch after collecting {item_name}. "
                f"Expected {expected_material}, got {actual_material}")
        
        # Now remove items in random order
        random.shuffle(collected_items)
        for item_name in collected_items:
            # Remove the item
            item = self.create_test_item(item_name)
            expected_loss = self.get_expected_material_loss(item_name)
            material_loss = self.cm_collection_state.remove(self.collection_state, item)
            self.world.remove(self.collection_state, item)
            
            # Material loss should match what we expect based on current state
            self.assertEqual(material_loss, expected_loss,
                f"Material loss {material_loss} doesn't match expected loss {expected_loss} "
                f"when removing {item_name}")
            
            expected_material -= material_loss
            
            # Verify material matches expectations
            actual_material = self.collection_state.prog_items[self.player].get("Material", 0)
            self.assertEqual(expected_material, actual_material,
                f"Material mismatch after removing {item_name}. "
                f"Expected {expected_material}, got {actual_material}")
        
        # Verify we're back to 0 material
        self.assertEqual(0, self.collection_state.prog_items[self.player].get("Material", 0),
            "Material should be 0 after removing all items")
