
from .bases import CMTestBase
from ..ItemPool import CMItemPool


class TestSuperSizeMeHandling(CMTestBase):
    """Test that Super-Size Me is handled correctly across different game goals."""
    def setUp(self):
        super().setUp()
        self.item_pool = CMItemPool(self.world)
        self.item_pool.initialize_item_tracking()

    def test_single_mode(self):
        """Test that Super-Size Me is not in the pool in single mode."""
        self.world.options.goal.value = self.world.options.goal.option_single
        items = self.item_pool.create_items()
        
        # Verify Super-Size Me is not in the pool
        super_size_items = [item for item in items if item.name == "Super-Size Me"]
        self.assertEqual(len(super_size_items), 0, 
            "Super-Size Me should not be in the pool in single mode")
        
        # Verify it's not in starting inventory
        self.assertNotIn("Super-Size Me", 
            [item.name for item in self.multiworld.precollected_items[self.player]],
            "Super-Size Me should not be in starting inventory in single mode")

    def test_progressive_mode(self):
        """Test that Super-Size Me is in the pool in progressive mode."""
        self.world.options.goal.value = self.world.options.goal.option_progressive
        items = self.item_pool.create_items()
        
        # Verify Super-Size Me is in the pool
        super_size_items = [item for item in items if item.name == "Super-Size Me"]
        self.assertEqual(len(super_size_items), 1,
            "Super-Size Me should be in the pool in progressive mode")
        
        # Verify it's not in starting inventory
        self.assertNotIn("Super-Size Me",
            [item.name for item in self.multiworld.precollected_items[self.player]],
            "Super-Size Me should not be in starting inventory in progressive mode")

    def test_ordered_progressive_mode(self):
        """Test that Super-Size Me is locked at Checkmate Minima in ordered progressive mode."""
        self.world.options.goal.value = self.world.options.goal.option_ordered_progressive
        
        # Clear any existing items at Checkmate Minima
        checkmate_minima = self.multiworld.get_location("Checkmate Minima", self.player)
        if checkmate_minima.item is not None:
            checkmate_minima.item = None
        
        items = self.item_pool.create_items()
        
        # Verify Super-Size Me is not in the regular pool
        super_size_items = [item for item in items if item.name == "Super-Size Me"]
        self.assertEqual(len(super_size_items), 0,
            "Super-Size Me should not be in the regular pool in ordered progressive mode")
        
        # Verify it's locked at Checkmate Minima
        checkmate_minima = self.multiworld.get_location("Checkmate Minima", self.player)
        self.assertIsNotNone(checkmate_minima.item,
            "Checkmate Minima should have a locked item")
        self.assertEqual(checkmate_minima.item.name, "Super-Size Me",
            "Super-Size Me should be locked at Checkmate Minima in ordered progressive mode")

    def test_super_mode(self):
        """Test that Super-Size Me is in starting inventory in super mode."""
        self.world.options.goal.value = self.world.options.goal.option_super
        items = self.item_pool.create_items()
        
        # Verify Super-Size Me is not in the pool
        super_size_items = [item for item in items if item.name == "Super-Size Me"]
        self.assertEqual(len(super_size_items), 0,
            "Super-Size Me should not be in the pool in super mode")
        
        # Verify it's in starting inventory
        self.assertIn("Super-Size Me",
            [item.name for item in self.multiworld.precollected_items[self.player]],
            "Super-Size Me should be in starting inventory in super mode")
