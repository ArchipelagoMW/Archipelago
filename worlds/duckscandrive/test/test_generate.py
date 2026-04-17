"""Sanity tests for the Ducks Can Drive world.

WorldTestBase.setUp builds a single-player MultiWorld and runs the generation
pipeline through `pre_fill`. Items are still in the pool (Fill has not been
called), so beatability checks must collect items manually.

The inherited `test_all_state_can_reach_everything` already verifies every
location is reachable when every item has been collected; these tests cover
the narrower shape guarantees of this specific world.
"""
from test.bases import WorldTestBase


class TestDucksGenerate(WorldTestBase):
    game = "Ducks Can Drive"

    def test_empty_state_is_not_beatable(self) -> None:
        self.assertBeatable(False)

    def test_collecting_all_progressives_beats_the_game(self) -> None:
        self.collect_by_name([
            "Progressive Speed",
            "Progressive Acceleration",
            "Progressive Offroad",
            "Progressive Boost",
            "Progressive Handling",
        ])
        self.assertBeatable(True)

    def test_location_and_item_counts(self) -> None:
        assert len(self.multiworld.get_locations(self.player)) == 26  # 25 upgrades + victory event
        assert len(self.multiworld.itempool) == 25

    def test_victory_location_holds_victory_event(self) -> None:
        victory = self.multiworld.get_location("Fully Upgraded Car", self.player)
        assert victory.item is not None
        assert victory.item.name == "Victory"

    def test_tier_one_locations_are_always_reachable(self) -> None:
        for stat in ("Speed", "Acceleration", "Offroad", "Boost", "Handling"):
            location = self.multiworld.get_location(f"Upgrade {stat} Tier 1", self.player)
            assert location.can_reach(self.multiworld.state), f"Tier 1 {stat} must be sphere-1"

    def test_tier_five_requires_four_progressives_of_that_stat(self) -> None:
        location = self.multiworld.get_location("Upgrade Speed Tier 5", self.player)
        assert not location.can_reach(self.multiworld.state)
        state = self.multiworld.state.copy()
        progressives = self.get_items_by_name("Progressive Speed")[:4]
        for item in progressives:
            state.collect(item)
        assert location.can_reach(state)
