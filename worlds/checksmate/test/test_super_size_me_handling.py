from .cm_mock_test_case import CMMockTestCase
from ..item_pool import CMItemPool
from ..item_utils import collection_item_maximum
from ..options import MinBoardSize


class TestSuperSizeMeHandling(CMMockTestCase):
    """Geometry is event-locked while the legacy marker remains decodable."""

    def test_default_series_uses_only_fixed_geometry_events(self):
        items = CMItemPool(self.world).create_items()

        self.assertFalse(
            any(
                item.name in {"Board Files", "Board Ranks", "Super-Size Me"}
                for item in items
            )
        )
        self.assertEqual(
            {
                "Checkmate Minima": "Board Files",
                "Checkmate Maxima": "Board Ranks",
                "Checkmate 10x10": "Board Files",
            },
            {
                name: self.world.multiworld.get_location(
                    name, self.world.player
                ).item.name
                for name in (
                    "Checkmate Minima",
                    "Checkmate Maxima",
                    "Checkmate 10x10",
                )
            },
        )
        self.assertEqual(
            [],
            self.world.multiworld.precollected_items[self.world.player],
        )

    def test_six_by_eight_start_adds_the_absolute_file_step_as_an_event(self):
        self.world.options.min_board_size = MinBoardSize.from_any("6x8")
        items = CMItemPool(self.world).create_items()

        self.assertFalse(any(item.name == "Board Files" for item in items))
        self.assertEqual(
            "Board Files",
            self.world.multiworld.get_location(
                "Checkmate 6x8", self.world.player
            ).item.name,
        )

    def test_legacy_super_size_marker_remains_one_file_unlock(self):
        item = self.world.create_item("Super-Size Me")
        self.assertEqual("Super-Size Me", item.name)
        self.assertEqual(
            1,
            collection_item_maximum(
                self.world.options,
                "Super-Size Me",
            ),
        )
