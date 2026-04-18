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
        # 25 upgrades + 8 books + 13 time-trial + 1 victory event
        assert len(self.multiworld.get_locations(self.player)) == 47
        # 25 progressives + 21 rubber ducks; victory is placed, not pooled
        assert len(self.multiworld.itempool) == 46

    def test_victory_location_holds_victory_event(self) -> None:
        victory = self.multiworld.get_location("Fully Upgraded Car", self.player)
        assert victory.item is not None
        assert victory.item.name == "Victory"

    def test_upgrade_tier_one_requires_one_progressive(self) -> None:
        # Strict rule: not sphere-1 from empty state; becomes reachable once a
        # matching progressive is collected.
        for stat in ("Speed", "Acceleration", "Offroad", "Boost", "Handling"):
            location = self.multiworld.get_location(f"Upgrade {stat} Tier 1", self.player)
            assert not location.can_reach(self.multiworld.state), f"Tier 1 {stat} must require a progressive"

            state = self.multiworld.state.copy()
            state.collect(self.get_item_by_name(f"Progressive {stat}"))
            assert location.can_reach(state), f"Tier 1 {stat} must be reachable after one Progressive {stat}"

    def test_all_eight_books_exist_and_are_free_sphere_one(self) -> None:
        for n in range(1, 9):
            location = self.multiworld.get_location(f"Book {n}", self.player)
            assert location.can_reach(self.multiworld.state), f"Book {n} must be sphere-1"

    def test_rubber_duck_count_matches_non_upgrade_locations(self) -> None:
        # 8 books + 13 TT locations = 21 rubber ducks
        rubber_ducks = [item for item in self.multiworld.itempool if item.name == "Rubber Duck"]
        assert len(rubber_ducks) == 21

    def test_all_seven_time_trial_finishes_exist_and_are_free(self) -> None:
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach", "Banana"):
            location = self.multiworld.get_location(f"Finish {display}", self.player)
            assert location.can_reach(self.multiworld.state), f"Finish {display} must be sphere-1"

    def test_banana_has_no_par_location(self) -> None:
        import pytest
        with pytest.raises(KeyError):
            self.multiworld.get_location("Beat par on Banana", self.player)

    def test_six_par_locations_exist(self) -> None:
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach"):
            location = self.multiworld.get_location(f"Beat par on {display}", self.player)
            assert location.can_reach(self.multiworld.state)

    def test_fill_slot_data_emits_starting_money(self) -> None:
        data = self.world.fill_slot_data()
        assert data["starting_money"] == 12_500  # matches StartingMoney.default

    def test_tier_five_requires_five_progressives_of_that_stat(self) -> None:
        location = self.multiworld.get_location("Upgrade Speed Tier 5", self.player)
        assert not location.can_reach(self.multiworld.state)
        state = self.multiworld.state.copy()
        progressives = self.get_items_by_name("Progressive Speed")[:4]
        for item in progressives:
            state.collect(item)
        assert not location.can_reach(state), "four progressives must not yet unlock tier 5"
        state.collect(self.get_items_by_name("Progressive Speed")[4])
        assert location.can_reach(state)
