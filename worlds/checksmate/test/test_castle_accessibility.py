from BaseClasses import CollectionState

from ..rules import set_rules
from .bases import CMTestBase


CASTLE_LOCATIONS = ("O-O Castle", "O-O-O Castle")


class TestCastleAccessibility(CMTestBase):
    options = {
        "difficulty": "grandmaster",
        "progression_itemization": "legacy",
        "locked_items": {"Progressive Major To Queen": 1},
        "queen_piece_limit": 1,
        "queen_piece_limit_by_type": 1,
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
        self.assert_castles_reachable(state, False)

        self.collect_copies(state, "Progressive Major Piece")
        self.assert_castles_reachable(state, True)

        self.collect_copies(state, "Progressive Major To Queen")
        self.assert_castles_reachable(state, True)

    def test_tracker_reconstruction_uses_same_monotonic_requirement(self) -> None:
        slot_data = self.world.fill_slot_data()
        self.multiworld.generation_is_fake = True
        self.multiworld.re_gen_passthrough = {
            self.world.game: self.world.interpret_slot_data(slot_data)
        }
        self.world._logic_projection = None
        self.world._set_logic_obtainable_counts(
            {"Progressive Major Piece": 3}
        )
        for name in CASTLE_LOCATIONS:
            self.multiworld.get_location(name, self.player).access_rule = lambda state: True
        set_rules(self.world)

        state = self.fresh_state()
        self.collect_copies(state, "Progressive Major Piece", 2)
        self.assert_castles_reachable(state, False)

        self.collect_copies(state, "Progressive Major Piece")
        self.assert_castles_reachable(state, True)
        self.collect_copies(state, "Progressive Major To Queen")
        self.assert_castles_reachable(state, True)


class TestFundamentalTrackerProjection(CMTestBase):
    options = {
        "progression_itemization": "fundamental",
    }

    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)

    def test_tracker_ignores_legacy_queen_total(self) -> None:
        slot_data = self.world.fill_slot_data()
        original_seeds = self.world.logic_projection.seeds
        self.multiworld.generation_is_fake = True
        self.multiworld.re_gen_passthrough = {
            self.world.game: self.world.interpret_slot_data(slot_data)
        }
        self.world.random.seed(999)
        self.world._semantic_seed_values = None
        self.world._logic_projection = None

        self.assertNotIn(
            "Progressive Major To Queen",
            self.world.logic_projection.axes,
        )
        self.assertEqual(original_seeds, self.world.logic_projection.seeds)
        self.assertEqual(
            slot_data["logic_obtainable_counts"],
            self.world.logic_projection.obtainable_counts(),
        )
