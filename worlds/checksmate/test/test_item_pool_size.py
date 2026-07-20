from .cm_mock_test_case import CMMockTestCase
from ..item_pool import CMItemPool
from ..options import Goal, EnableTactics, FairyChessPieces, FairyChessArmy


class TestItemPoolSize(CMMockTestCase):
    victory_reserved_count = 1
    ordered_reserved_count = 5
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
    single_item_count = single_location_count - victory_reserved_count
    # 'Capture Pawn I' and 'Capture Pawn J'(+2)
    # 'Checkmate Maxima'(+1) - 1 location, but not counted
    # "Capture Piece Queen's Attendant" and "Capture Piece King's Attendant"(+2)
    # 'Capture 9 Pawns' and 'Capture 10 Pawns'(+2)
    # 'Capture 8 Pieces' and 'Capture 9 Pieces'(+2)
    # 'Capture 8 Of Each' and 'Capture 9 Of Each'(+2)
    # 'Capture Any 15' through 'Capture Any 18'(+4)
    # Total additional locations: 15
    super_location_count = 103
    super_item_count = super_location_count - victory_reserved_count

    def setUp(self):
        super().setUp()
        self.item_pool = CMItemPool(self.world)
        self.item_pool.initialize_item_tracking()

    def test_item_pool_matches_location_count(self):
        """Test that the item pool size matches the number of valid locations"""
        items = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(False)
        self.assertEqual(
            len(items),
            max_items - self.victory_reserved_count,
            "Victory should reserve one location outside the randomized pool",
        )

    def test_item_pool_with_tactics(self):
        """Test that enabling tactics increases the item pool size"""
        # Test with all tactics enabled
        self.world.options.enable_tactics.value = self.world.options.enable_tactics.option_all
        items_all = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(False)
        self.assertEqual(
            len(items_all),
            max_items - self.victory_reserved_count,
        )

        # Test with no tactics
        self.world.options.enable_tactics.value = self.world.options.enable_tactics.option_none
        items_none = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(False)
        self.assertEqual(
            len(items_none),
            max_items - self.victory_reserved_count,
        )

        # Verify that enabling tactics increases the pool size
        self.assertGreater(len(items_all), len(items_none),
            "Enabling tactics should increase the item pool size")

    def test_item_pool_with_shuffled_progressive(self):
        """Test that enabling fairy pieces increases the item pool size"""
        # Test with goal shuffled into item pool
        self.world.options.goal.value = self.world.options.goal.option_progressive
        items_shuffled = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(True)
        self.assertEqual(
            len(items_shuffled),
            max_items - self.victory_reserved_count,
        )

        # Test with goal set to an event location
        self.world.options.goal.value = self.world.options.goal.option_ordered_progressive
        items_ordered = self.item_pool.create_items()
        max_items = self.item_pool.get_max_items(True)
        self.assertEqual(
            len(items_ordered),
            max_items - self.ordered_reserved_count,
        )

        # Verify that changing an event location to an item location increases the pool size
        self.assertLess(len(items_ordered), len(items_shuffled),
            "Enabling fairy pieces should increase the item pool size")

    def test_item_pool_with_single(self):
        """Test that single mode has the correct item pool size"""
        self.world.options.goal.value = self.world.options.goal.option_single
        items_single = self.item_pool.create_items()
        max_items_single = self.item_pool.get_max_items(False)
        self.assertEqual(
            len(items_single),
            max_items_single - self.victory_reserved_count,
        )

    def test_item_pool_with_super_sized(self):
        """Test that super-sized mode has the correct item pool size"""
        self.world.options.goal.value = self.world.options.goal.option_super
        items_super = self.item_pool.create_items()
        max_items_super = self.item_pool.get_max_items(True)
        self.assertEqual(
            len(items_super),
            max_items_super - self.victory_reserved_count,
        )

    def test_current_location_and_item_pool_count_matrix(self):
        expected = {
            ("single", "all"): (71, 70),
            ("single", "turns"): (65, 64),
            ("single", "none"): (61, 60),
            ("ordered_progressive", "all"): (103, 98),
            ("ordered_progressive", "turns"): (97, 92),
            ("ordered_progressive", "none"): (93, 88),
            ("progressive", "all"): (103, 102),
            ("progressive", "turns"): (97, 96),
            ("progressive", "none"): (93, 92),
            ("super", "all"): (103, 102),
            ("super", "turns"): (97, 96),
            ("super", "none"): (93, 92),
        }

        for (goal_name, tactics_name), (location_count, item_count) in expected.items():
            with self.subTest(goal=goal_name, tactics=tactics_name):
                world = self.create_mock_world()
                world.options.goal = Goal(getattr(Goal, f"option_{goal_name}"))
                world.options.enable_tactics = EnableTactics(getattr(EnableTactics, f"option_{tactics_name}"))
                item_pool = CMItemPool(world)

                self.assertEqual(
                    location_count,
                    item_pool.get_max_items(goal_name != "single"),
                )
                self.assertEqual(item_count, len(item_pool.create_items()))
