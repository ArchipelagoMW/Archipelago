from BaseClasses import CollectionState, Item, ItemClassification
from ..Items import item_table
from . import CMTestBase

class TestCollectionState(CMTestBase):
    def setUp(self):
        super().setUp()
        self.collection_state = CollectionState(self.multiworld)
        self.cm_collection_state = self.world._collection_state
        
    def create_test_item(self, name: str) -> Item:
        """Helper to create a test item with the given name"""
        return Item(name, ItemClassification.progression, self.world.player, item_table[name])
        
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
