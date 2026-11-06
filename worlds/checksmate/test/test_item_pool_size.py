from .cm_mock_test_case import CMMockTestCase
from ..item_pool import CMItemPool
from ..options import EnableTactics, MaxBoardSize, MinBoardSize


class TestItemPoolSize(CMMockTestCase):
    def setUp(self):
        super().setUp()
        self.item_pool = CMItemPool(self.world)

    def test_item_pool_reserves_victory_and_fixed_transitions(self):
        items = self.item_pool.create_items()
        progression = self.world.geometry_progression
        self.assertEqual(
            self.item_pool.get_max_items()
            - 1
            - len(progression.transitions),
            len(items),
        )
        self.assertFalse(
            any(item.name in {"Board Files", "Board Ranks"} for item in items)
        )

    def test_enabling_tactics_increases_pool_capacity(self):
        self.world.options.enable_tactics = EnableTactics(
            EnableTactics.option_all
        )
        items_all = CMItemPool(self.world).create_items()

        self.world.options.enable_tactics = EnableTactics(
            EnableTactics.option_none
        )
        items_none = CMItemPool(self.world).create_items()

        self.assertGreater(len(items_all), len(items_none))

    def test_selected_series_capacity_matrix(self):
        expected = {
            ("8x8", "10x8", "all"): (86, 84),
            ("8x8", "10x10", "all"): (87, 84),
            ("8x8", "12x10", "all"): (102, 98),
            ("6x8", "10x8", "all"): (87, 84),
            ("8x8", "12x10", "turns"): (96, 92),
            ("8x8", "12x10", "none"): (92, 88),
        }

        for (start, end, tactics), (location_count, item_count) in expected.items():
            with self.subTest(start=start, end=end, tactics=tactics):
                world = self.create_mock_world()
                world.options.min_board_size = MinBoardSize.from_any(start)
                world.options.max_board_size = MaxBoardSize.from_any(end)
                world.options.enable_tactics = EnableTactics.from_any(tactics)
                item_pool = CMItemPool(world)

                self.assertEqual(location_count, item_pool.get_max_items())
                self.assertEqual(item_count, len(item_pool.create_items()))
