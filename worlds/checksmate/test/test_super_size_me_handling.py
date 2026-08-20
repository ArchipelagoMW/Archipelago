
from .cm_mock_test_case import CMMockTestCase
from ..item_pool import CMItemPool


class TestSuperSizeMeHandling(CMMockTestCase):
    """Test current v2 geometry items while retaining the legacy marker."""
    def setUp(self):
        super().setUp()
        self.player = self.world.player
        self.multiworld = self.world.multiworld
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
        """Test that Board Files is in the pool in progressive mode."""
        self.world.options.goal.value = self.world.options.goal.option_progressive
        items = self.item_pool.create_items()
        
        self.assertEqual(2, sum(item.name == "Board Files" for item in items))
        self.assertEqual(2, sum(item.name == "Board Ranks" for item in items))
        self.assertFalse(any(item.name == "Super-Size Me" for item in items))
        
        # Verify it's not in starting inventory
        self.assertNotIn("Super-Size Me",
            [item.name for item in self.multiworld.precollected_items[self.player]],
            "Super-Size Me should not be in starting inventory in progressive mode")

    def test_ordered_progressive_mode(self):
        """Test that all four geometry unlocks are locked in stage order."""
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
        
        self.assertEqual(
            {
                "Checkmate Minima": "Board Files",
                "Checkmate Maxima": "Board Ranks",
                "Checkmate 10x10": "Board Files",
                "Checkmate 12x10": "Board Ranks",
            },
            {
                location: self.multiworld.get_location(location, self.player).item.name
                for location in (
                    "Checkmate Minima",
                    "Checkmate Maxima",
                    "Checkmate 10x10",
                    "Checkmate 12x10",
                )
            },
        )
        self.assertEqual(0, sum(item.name == "Board Files" for item in items))
        self.assertEqual(0, sum(item.name == "Board Ranks" for item in items))

    def test_super_mode(self):
        """Test that the first Board Files unlock is in starting inventory in super mode."""
        self.world.options.goal.value = self.world.options.goal.option_super
        items = self.item_pool.create_items()
        
        # Verify Super-Size Me is not in the pool
        super_size_items = [item for item in items if item.name == "Super-Size Me"]
        self.assertEqual(len(super_size_items), 0,
            "Super-Size Me should not be in the pool in super mode")
        
        # Verify it's in starting inventory
        self.assertIn("Board Files",
            [item.name for item in self.multiworld.precollected_items[self.player]],
            "Board Files should be in starting inventory in super mode")
        self.assertEqual(1, sum(item.name == "Board Files" for item in items))
        self.assertEqual(2, sum(item.name == "Board Ranks" for item in items))

    def test_legacy_super_size_marker_remains_decodable(self):
        item = self.world.create_item("Super-Size Me")
        self.assertEqual("Super-Size Me", item.name)
