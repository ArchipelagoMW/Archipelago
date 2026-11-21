from BaseClasses import CollectionState

from ..locations import BoardStage
from .bases import CMTestBase


class TestCollectionState(CMTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)

    def fresh_state(self) -> CollectionState:
        return CollectionState(self.multiworld)

    def collect_names(
        self,
        state: CollectionState,
        names: list[str],
    ) -> list[bool]:
        return [
            self.world.collect(state, self.world.create_item(name))
            for name in names
        ]

    def remove_names(
        self,
        state: CollectionState,
        names: list[str],
    ) -> list[bool]:
        return [
            self.world.remove(state, self.world.create_item(name))
            for name in names
        ]

    def counts_snapshot(
        self,
        state: CollectionState,
    ) -> tuple[int, int]:
        return (
            state.count("Progressive Major Piece", self.player),
            state.count("Progressive Major To Queen", self.player),
        )

    def exact_material(self, state: CollectionState) -> int:
        counts = {
            name: state.count(name, self.player)
            for name in (
                "Progressive Major Piece",
                "Progressive Major To Queen",
            )
        }
        return self.world.logic_projection.exact_active_material(
            counts,
            BoardStage.Board8x8,
        )

    def test_parent_child_collection_order_is_projection_invariant(self):
        parent_first = self.fresh_state()
        child_first = self.fresh_state()

        self.assertEqual(
            [True, True],
            self.collect_names(
                parent_first,
                ["Progressive Major Piece", "Progressive Major To Queen"],
            ),
        )
        self.assertEqual(
            [True, True],
            self.collect_names(
                child_first,
                ["Progressive Major To Queen", "Progressive Major Piece"],
            ),
        )

        self.assertEqual((1, 1), self.counts_snapshot(parent_first))
        self.assertEqual(
            self.counts_snapshot(parent_first),
            self.counts_snapshot(child_first),
        )
        self.assertEqual(900, self.exact_material(parent_first))
        self.assertEqual(
            self.exact_material(parent_first),
            self.exact_material(child_first),
        )

    def test_collect_then_remove_is_an_exact_count_inverse(self):
        for collection_order in (
            ["Progressive Major Piece", "Progressive Major To Queen"],
            ["Progressive Major To Queen", "Progressive Major Piece"],
        ):
            with self.subTest(collection_order=collection_order):
                state = self.fresh_state()
                self.collect_names(state, collection_order)

                self.assertEqual(
                    [True, True],
                    self.remove_names(
                        state,
                        list(reversed(collection_order)),
                    ),
                )
                self.assertEqual((0, 0), self.counts_snapshot(state))
                self.assertEqual(0, self.exact_material(state))

    def test_unpaired_upgrades_are_interpreted_by_projection(self):
        state = self.fresh_state()

        self.assertEqual(
            [True, True, True],
            self.collect_names(
                state,
                ["Progressive Major To Queen"] * 3,
            ),
        )
        self.assertEqual((0, 3), self.counts_snapshot(state))
        self.assertEqual(0, self.exact_material(state))

        self.assertTrue(
            self.world.collect(
                state,
                self.world.create_item("Progressive Major Piece"),
            )
        )
        self.assertEqual((1, 3), self.counts_snapshot(state))
        self.assertEqual(900, self.exact_material(state))

        self.assertTrue(
            self.world.remove(
                state,
                self.world.create_item("Progressive Major Piece"),
            )
        )
        self.assertEqual((0, 3), self.counts_snapshot(state))
        self.assertEqual(0, self.exact_material(state))

    def test_fixed_quantity_cap_tracks_linked_or_starting_overcounts(self):
        state = self.fresh_state()
        item_name = "Progressive King Promotion"

        self.assertEqual(
            [True, True, False, False],
            self.collect_names(state, [item_name] * 4),
        )
        self.assertEqual(2, state.count(item_name, self.player))
        self.assertEqual(
            850,
            self.world.logic_projection.metrics(
                state,
                self.player,
                BoardStage.Board8x8,
            ).material,
        )

        self.assertEqual(
            [False, False, True, True],
            self.remove_names(state, [item_name] * 4),
        )
        self.assertEqual(0, state.count(item_name, self.player))
        self.assertEqual(
            0,
            self.world.logic_projection.metrics(
                state,
                self.player,
                BoardStage.Board8x8,
            ).material,
        )

    def test_dynamic_pocket_cap_and_counting_share_one_definition(self):
        state = self.fresh_state()
        self.world.options.pocket_limit_by_pocket.value = 1
        self.world.options.max_pocket.value = 12

        self.assertEqual(
            [True, True, True, False],
            self.collect_names(state, ["Progressive Pocket"] * 4),
        )
        self.assertEqual(3, state.count("Progressive Pocket", self.player))
        metrics = self.world.logic_projection.metrics(
            state,
            self.player,
            BoardStage.Board8x8,
        )
        self.assertEqual(3, metrics.chessmen)
        self.assertEqual(0, metrics.material)

    def test_partial_pocket_counts_use_ceiling_consistently(self):
        state = self.fresh_state()
        self.world.options.pocket_limit_by_pocket.value = 4

        self.collect_names(state, ["Progressive Pocket"])
        self.assertEqual(
            1,
            self.world.logic_projection.metrics(
                state,
                self.player,
                BoardStage.Board8x8,
            ).chessmen,
        )

        self.collect_names(state, ["Progressive Pocket"] * 3)
        self.assertEqual(
            1,
            self.world.logic_projection.metrics(
                state,
                self.player,
                BoardStage.Board8x8,
            ).chessmen,
        )

        self.collect_names(state, ["Progressive Pocket"])
        self.assertEqual(
            2,
            self.world.logic_projection.metrics(
                state,
                self.player,
                BoardStage.Board8x8,
            ).chessmen,
        )
