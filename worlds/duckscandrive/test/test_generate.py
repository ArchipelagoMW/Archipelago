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
        # Default (banana off): 25 upgrades + 8 books + 12 TT (no Finish Banana) + 1 victory
        assert len(self.multiworld.get_locations(self.player)) == 46
        # 25 progressives + 6 track unlocks (no Banana Unlock) + 14 rubber ducks
        assert len(self.multiworld.itempool) == 45

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
        # 8 books + 13 TT locations - 7 track-unlock items = 14 rubber ducks
        rubber_ducks = [item for item in self.multiworld.itempool if item.name == "Rubber Duck"]
        assert len(rubber_ducks) == 14

    def test_six_track_unlock_items_exist_once_each_by_default(self) -> None:
        # Banana Unlock is excluded when include_banana is off.
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach"):
            matches = [item for item in self.multiworld.itempool if item.name == f"{display} Unlock"]
            assert len(matches) == 1, f"expected exactly one '{display} Unlock', got {len(matches)}"
        banana = [item for item in self.multiworld.itempool if item.name == "Banana Unlock"]
        assert len(banana) == 0, "Banana Unlock must not be in the pool with include_banana off"

    def test_time_trial_finishes_require_matching_unlock(self) -> None:
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach"):
            location = self.multiworld.get_location(f"Finish {display}", self.player)
            assert not location.can_reach(self.multiworld.state), f"Finish {display} must require unlock"

            state = self.multiworld.state.copy()
            state.collect(self.get_item_by_name(f"{display} Unlock"))
            assert location.can_reach(state), f"Finish {display} must unlock after its item"

    def test_banana_locations_absent_by_default(self) -> None:
        import pytest
        with pytest.raises(KeyError):
            self.multiworld.get_location("Finish Banana", self.player)
        with pytest.raises(KeyError):
            self.multiworld.get_location("Beat par on Banana", self.player)

    def test_par_locations_require_matching_unlock(self) -> None:
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach"):
            location = self.multiworld.get_location(f"Beat par on {display}", self.player)
            assert not location.can_reach(self.multiworld.state)

            state = self.multiworld.state.copy()
            state.collect(self.get_item_by_name(f"{display} Unlock"))
            assert location.can_reach(state)

    def test_fill_slot_data_emits_starting_money(self) -> None:
        data = self.world.fill_slot_data()
        assert data["starting_money"] == 12_500  # matches StartingMoney.default

    def test_fill_slot_data_defaults(self) -> None:
        data = self.world.fill_slot_data()
        assert data["include_banana"] is False
        assert data["include_par_times"] is True


class TestDucksGenerateWithBanana(WorldTestBase):
    game = "Ducks Can Drive"
    options = {"include_banana": True}

    def test_banana_locations_and_unlock_present(self) -> None:
        assert self.multiworld.get_location("Finish Banana", self.player) is not None
        bananas = [item for item in self.multiworld.itempool if item.name == "Banana Unlock"]
        assert len(bananas) == 1

    def test_location_and_item_counts_with_banana(self) -> None:
        # 25 upgrades + 8 books + 13 TT + 1 victory = 47 locations
        assert len(self.multiworld.get_locations(self.player)) == 47
        assert len(self.multiworld.itempool) == 46

    def test_fill_slot_data_flags_include_banana(self) -> None:
        assert self.world.fill_slot_data()["include_banana"] is True


class TestDucksGenerateNoPars(WorldTestBase):
    game = "Ducks Can Drive"
    options = {"include_par_times": False}

    def test_par_locations_absent(self) -> None:
        import pytest
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach"):
            with pytest.raises(KeyError):
                self.multiworld.get_location(f"Beat par on {display}", self.player)

    def test_finishes_still_present(self) -> None:
        for display in ("Duck Circuit", "Lake Loop", "Quack Crossing", "Wing Circuit",
                        "Blackbill Ship", "Bill Beach"):
            assert self.multiworld.get_location(f"Finish {display}", self.player) is not None

    def test_location_and_item_counts_no_pars(self) -> None:
        # 25 upgrades + 8 books + 6 finishes (no pars, no banana) + 1 victory = 40
        assert len(self.multiworld.get_locations(self.player)) == 40
        # 25 progressives + 6 unlocks + 8 rubber ducks = 39
        assert len(self.multiworld.itempool) == 39
        ducks = [item for item in self.multiworld.itempool if item.name == "Rubber Duck"]
        assert len(ducks) == 8

    def test_fill_slot_data_flags_pars_off(self) -> None:
        assert self.world.fill_slot_data()["include_par_times"] is False

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
