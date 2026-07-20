from BaseClasses import CollectionState

from ..items import MATERIAL_TOTAL_KEY
from .bases import CMTestBase


class TestCollectionState(CMTestBase):
    def world_setup(self, *args, **kwargs) -> None:
        super().world_setup(seed=0)

    def fresh_state(self) -> CollectionState:
        return CollectionState(self.multiworld)

    def collect_names(self, state: CollectionState, names: list[str]) -> list[bool]:
        return [
            self.world.collect(state, self.world.create_item(name))
            for name in names
        ]

    def remove_names(self, state: CollectionState, names: list[str]) -> list[bool]:
        return [
            self.world.remove(state, self.world.create_item(name))
            for name in names
        ]

    def snapshot(self, state: CollectionState) -> tuple[int, int, int]:
        return (
            state.count("Progressive Major Piece", self.player),
            state.count("Progressive Major To Queen", self.player),
            state.prog_items[self.player][MATERIAL_TOTAL_KEY],
        )

    def test_parent_child_collection_order_is_invariant(self) -> None:
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

        self.assertEqual((1, 1, 900), self.snapshot(parent_first))
        self.assertEqual(self.snapshot(parent_first), self.snapshot(child_first))

    def test_collect_then_remove_is_an_exact_inverse_in_both_orders(self) -> None:
        for collection_order in (
            ["Progressive Major Piece", "Progressive Major To Queen"],
            ["Progressive Major To Queen", "Progressive Major Piece"],
        ):
            with self.subTest(collection_order=collection_order):
                state = self.fresh_state()
                self.collect_names(state, collection_order)

                self.assertEqual(
                    [True, True],
                    self.remove_names(state, list(reversed(collection_order))),
                )
                self.assertEqual((0, 0, 0), self.snapshot(state))

    def test_unpaired_child_upgrades_only_gain_material_when_parents_arrive(self) -> None:
        state = self.fresh_state()

        self.assertEqual(
            [True, True, True],
            self.collect_names(state, ["Progressive Major To Queen"] * 3),
        )
        self.assertEqual((0, 3, 0), self.snapshot(state))

        self.assertTrue(
            self.world.collect(
                state,
                self.world.create_item("Progressive Major Piece"),
            )
        )
        self.assertEqual((1, 3, 900), self.snapshot(state))

        self.assertTrue(
            self.world.remove(
                state,
                self.world.create_item("Progressive Major Piece"),
            )
        )
        self.assertEqual((0, 3, 0), self.snapshot(state))

    def test_fixed_quantity_cap_tracks_linked_or_starting_overcounts(self) -> None:
        """Extra incoming copies are removed before either effective copy."""
        state = self.fresh_state()
        item_name = "Progressive King Promotion"

        self.assertEqual(
            [True, True, False, False],
            self.collect_names(state, [item_name] * 4),
        )
        self.assertEqual(2, state.count(item_name, self.player))
        self.assertEqual(850, state.prog_items[self.player][MATERIAL_TOTAL_KEY])

        self.assertEqual(
            [False, False, True, True],
            self.remove_names(state, [item_name] * 4),
        )
        self.assertEqual(0, state.count(item_name, self.player))
        self.assertEqual(0, state.prog_items[self.player][MATERIAL_TOTAL_KEY])

    def test_dynamic_pocket_cap_is_three_times_per_pocket_limit(self) -> None:
        state = self.fresh_state()
        self.world.options.pocket_limit_by_pocket.value = 1
        self.world.options.max_pocket.value = 12

        self.assertEqual(
            [True, True, True, False],
            self.collect_names(state, ["Progressive Pocket"] * 4),
        )
        self.assertEqual(3, state.count("Progressive Pocket", self.player))
        self.assertEqual(330, state.prog_items[self.player][MATERIAL_TOTAL_KEY])
