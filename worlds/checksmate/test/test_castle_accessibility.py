from BaseClasses import CollectionState

from ..rules import set_rules
from .bases import CMTestBase


CASTLE_LOCATIONS = ("O-O Castle", "O-O-O Castle")


class TestCastleAccessibility(CMTestBase):
    options = {
        "difficulty": "grandmaster",
        "progression_itemization": "legacy",
    }

    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)

    def fresh_state(self) -> CollectionState:
        return CollectionState(self.multiworld)

    def collect_copies(
        self,
        state: CollectionState,
        name: str,
        count: int = 1,
    ) -> None:
        for _ in range(count):
            self.assertTrue(self.world.collect(state, self.world.create_item(name)))

    def assert_castles_reachable(
        self,
        state: CollectionState,
        expected: bool,
    ) -> None:
        for name in CASTLE_LOCATIONS:
            with self.subTest(location=name):
                self.assertEqual(
                    expected,
                    self.multiworld.get_location(name, self.player).can_reach(state),
                )

    def test_normal_world_castling_requirement_is_monotonic(self) -> None:
        state = self.fresh_state()
        self.collect_copies(state, "Progressive Major Piece", 2)
        self.assert_castles_reachable(state, True)

        self.collect_copies(state, "Progressive Major To Queen", 3)
        self.assert_castles_reachable(state, True)

    def test_tracker_reconstruction_preserves_legacy_non_monotonic_bug(self) -> None:
        """Legacy tracker rules get harder when a queen upgrade is collected."""
        self.multiworld.generation_is_fake = True
        for name in CASTLE_LOCATIONS:
            self.multiworld.get_location(name, self.player).access_rule = lambda state: True
        set_rules(self.world)

        state = self.fresh_state()
        self.collect_copies(state, "Progressive Major Piece", 2)
        self.assert_castles_reachable(state, True)

        self.collect_copies(state, "Progressive Major To Queen")
        self.assert_castles_reachable(state, False)

        self.collect_copies(state, "Progressive Major Piece")
        self.assert_castles_reachable(state, True)
