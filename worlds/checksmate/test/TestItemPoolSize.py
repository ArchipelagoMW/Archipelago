from .CMMockTestCase import CMMockTestCase
from ..ItemPool import CMItemPool
from ..Options import Goal, EnableTactics, FairyChessPieces, FairyChessArmy


class TestItemPoolSize(CMMockTestCase):
    event_count = 1
    ordered_event_count = 2
    tactics_all_item_count = 10
    tactics_turns_item_count = 4
    # All "Capture Pawn" locations (A through H) - 8 locations
    # All "Capture Piece" locations (Queen's Rook through King's Rook) - 7 locations
    # "Checkmate Minima" - 1 location, but not counted
    # All "King to..." locations - 5 locations
    # All "Capture 2 Pawns" through "Capture 8 Pawns" - 7 locations
    # All "Capture 2 Pieces" through "Capture 7 Pieces" - 6 locations
    # All "Capture 2 Of Each" through "Capture 7 Of Each" - 6 locations
    # "Capture Everything" - 1 location
    # All "Capture Any 2" through "Capture Any 14" - 13 locations
    # All "Current Objective: Survive..." locations - 4 locations
    # All "Threaten..." locations - 5 locations
    # All "Fork..." locations - 6 locations
    # Both Castle locations - 2 locations
    single_location_count = 71
    single_item_count = single_location_count - event_count
    # 'Capture Pawn I' and 'Capture Pawn J'(+2)
    # 'Checkmate Maxima'(+1) - 1 location, but not counted
    # "Capture Piece Queen's Attendant" and "Capture Piece King's Attendant"(+2)
    # 'Capture 9 Pawns' and 'Capture 10 Pawns'(+2)
    # 'Capture 8 Pieces' and 'Capture 9 Pieces'(+2)
    # 'Capture 8 Of Each' and 'Capture 9 Of Each'(+2)
    # 'Capture Any 15' through 'Capture Any 18'(+4)
    # Total additional locations: 15
    super_location_count = 86
    super_item_count = super_location_count - event_count

    def setUp(self):
        super().setUp()
        self.item_pool = CMItemPool(self.world)
        self.item_pool.initialize_item_tracking()

    def get_event_item_count(self) -> int:
        """Calculate the number of event items based on current game options."""
        count = 1  # Play as White is always added
        if self.world.options.goal.value != self.world.options.goal.option_single:
            count += 1  # Super-Size Me for non-single modes
        count += 1  # Victory item
        return count

    def test_item_pool_matches_location_count(self):
        """Test that the item pool size matches the number of valid locations"""
        items = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(False)
        self.assertEqual(len(items), max_items - self.event_count,
            f"Expected {max_items} location items plus {self.event_count} event items")

    def test_item_pool_with_tactics(self):
        """Test that enabling tactics increases the item pool size"""
        # Test with all tactics enabled
        self.world.options.enable_tactics.value = self.world.options.enable_tactics.option_all
        items_all = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(False)
        self.assertEqual(len(items_all), max_items - self.event_count,
            f"Expected {max_items} location items plus {self.event_count} event items with all tactics")

        # Test with no tactics
        self.world.options.enable_tactics.value = self.world.options.enable_tactics.option_none
        items_none = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(False)
        self.assertEqual(len(items_none), max_items - self.event_count,
            f"Expected {max_items} location items plus {self.event_count} event items with no tactics")

        # Verify that enabling tactics increases the pool size
        self.assertGreater(len(items_all), len(items_none),
            "Enabling tactics should increase the item pool size")

    def test_item_pool_with_shuffled_progressive(self):
        """Test that enabling fairy pieces increases the item pool size"""
        # Test with goal shuffled into item pool
        self.world.options.goal.value = self.world.options.goal.option_progressive
        items_shuffled = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(True)
        self.assertEqual(len(items_shuffled), max_items - self.event_count,
            f"Expected {max_items} location items plus {self.event_count} event items with shuffled progressive")

        # Test with goal set to an event location
        self.world.options.goal.value = self.world.options.goal.option_ordered_progressive
        items_ordered = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(True)
        self.assertEqual(len(items_ordered), max_items - self.ordered_event_count,
            f"Expected {max_items} location items plus {self.ordered_event_count} event items with full fairy pieces")

        # Verify that changing an event location to an item location increases the pool size
        self.assertLess(len(items_ordered), len(items_shuffled),
            "Enabling fairy pieces should increase the item pool size")

    def test_item_pool_with_single(self):
        """Test that single mode has the correct item pool size"""
        self.world.options.goal.value = self.world.options.goal.option_single
        items_single = self.item_pool.create_items()
        max_items_single = self.item_pool.get_max_items(False)
        self.assertEqual(len(items_single), max_items_single - self.event_count,
            f"Expected {max_items_single} location items plus {self.event_count} event items in single mode")

    def test_item_pool_with_super_sized(self):
        """Test that super-sized mode has the correct item pool size"""
        self.world.options.goal.value = self.world.options.goal.option_super
        items_super = self.item_pool.create_items()
        max_items_super = self.item_pool.get_max_items(True)
        self.assertEqual(len(items_super), max_items_super - self.event_count,
            f"Expected {max_items_super} location items plus {self.event_count} event items in super-sized mode")
