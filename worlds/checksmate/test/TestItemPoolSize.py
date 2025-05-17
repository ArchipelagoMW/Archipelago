from .CMMockTestCase import CMMockTestCase
from ..ItemPool import CMItemPool
from ..Options import Goal, EnableTactics, FairyChessPieces, FairyChessArmy


class TestItemPoolSize(CMMockTestCase):
    # All "Capture Pawn" locations (A through H) - 8 locations
    # All "Capture Piece" locations (Queen's Rook through King's Rook) - 7 locations
    # "Checkmate Minima" - 1 location
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
    single_event_count = 1
    single_item_count = single_location_count - single_event_count
    # 'Capture Pawn I' and 'Capture Pawn J'(+2)
    # 'Checkmate Maxima'(+1)
    # "Capture Piece Queen's Attendant" and "Capture Piece King's Attendant"(+2)
    # 'Capture 9 Pawns' and 'Capture 10 Pawns'(+2)
    # 'Capture 8 Pieces' and 'Capture 9 Pieces'(+2)
    # 'Capture 8 Of Each' and 'Capture 9 Of Each'(+2)
    # 'Capture Any 15' through 'Capture Any 18'(+4)
    # Total additional locations: 15
    super_location_count = 86
    super_event_count = 2
    super_item_count = super_location_count - super_event_count
    tactics_all_item_count = 10
    tactics_turns_item_count = 4

    def setUp(self):
        super().setUp()
        self.item_pool = CMItemPool(self.world)
        self.item_pool.initialize_item_tracking()

    def test_item_pool_matches_location_count(self):
        """Test that the total number of items matches the number of locations"""
        # Create items
        items = self.item_pool.create_items()
        
        # Get max items (based on locations)
        max_items = self.item_pool.get_max_items(
            super_sized=self.world.options.goal.value != self.world.options.goal.option_single
        )

        # Verify super sized items are equal to actual super sized locations
        self.assertEqual(max_items, self.single_item_count)
        # Verify total items don't exceed locations
        self.assertLessEqual(len(items), max_items)

    def test_item_pool_with_fairy_pieces(self):
        """Test item pool size with fairy pieces enabled"""
        # Enable fairy pieces
        self.world.options.fairy_chess_pieces = FairyChessPieces(FairyChessPieces.option_full)
        self.world.options.fairy_chess_army = FairyChessArmy(FairyChessArmy.option_chaos)
        
        # Create items
        items = self.item_pool.create_items()
        
        # Get max items
        max_items = self.item_pool.get_max_items(
            super_sized=self.world.options.goal.value != self.world.options.goal.option_single
        )

        # Verify super sized items are equal to actual super sized locations
        self.assertEqual(max_items, self.single_item_count)
        # Verify total items don't exceed locations
        self.assertLessEqual(len(items), max_items)

    def test_item_pool_with_tactics(self):
        """Test item pool size with different tactics settings"""
        # Test with all tactics
        self.world.options.enable_tactics = EnableTactics(EnableTactics.option_all)
        items_all = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(
            super_sized=self.world.options.goal.value != self.world.options.goal.option_single
        )
        self.assertLessEqual(len(items_all), max_items)
        # Verify super sized items are equal to actual super sized locations
        self.assertEqual(max_items, self.single_item_count)
        
        # Test with no tactics
        self.world.options.enable_tactics = EnableTactics(EnableTactics.option_none)
        items_none = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(
            super_sized=self.world.options.goal.value != self.world.options.goal.option_single
        )
        self.assertLessEqual(len(items_none), max_items)
        # Verify super sized items are equal to actual super sized locations
        self.assertEqual(max_items, self.single_item_count - self.tactics_all_item_count)

        # Verify that no tactics has fewer items than all tactics
        self.assertLess(len(items_none), len(items_all))

    def test_item_pool_with_super_sized(self):
        """Test item pool size with super-sized mode"""
        # Test with single mode
        self.world.options.goal = Goal(Goal.option_single)
        items_single = self.item_pool.create_items()
        max_items_single = self.item_pool.get_max_items(super_sized=False)
        self.assertLessEqual(len(items_single), max_items_single)

        # Test with super-sized mode
        self.world.options.goal = Goal(Goal.option_super)
        items_super = self.item_pool.create_items()
        max_items_super = self.item_pool.get_max_items(super_sized=True)
        self.assertLessEqual(len(items_super), max_items_super)

        # Verify that super-sized has more items than single
        self.assertGreater(len(items_super), len(items_single)) 