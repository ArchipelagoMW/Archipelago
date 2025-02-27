from ..data.RoomNames import RoomName
from ..Items import SuitUpgrade
from ..data.Tricks import TrickDifficulty
from . import MetroidPrimeTestBase


class TestScanVisorShuffled(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "trick_difficulty": TrickDifficulty.Easy.value,
        "shuffle_scan_visor": True,
    }

    def test_cannot_reach_alcove_with_tricks_enabled(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == False

    def test_do_not_start_with_scan_visor(self):
        assert SuitUpgrade.Scan_Visor.value not in [
            item.name for item in self.multiworld.precollected_items[self.player]
        ]

    def test_scan_visor_in_item_pool(self):
        assert SuitUpgrade.Scan_Visor.value in [
            item.name for item in self.multiworld.itempool
        ]


class TestScanVisorNotShuffled(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "trick_difficulty": TrickDifficulty.Easy.value,
        "shuffle_scan_visor": False,
    }

    def test_can_reach_alcove_with_tricks_enabled(self):
        assert self.can_reach_location("Tallon Overworld: Alcove") == True

    def test_start_with_scan_visor(self):
        assert SuitUpgrade.Scan_Visor.value in [
            item.name for item in self.multiworld.precollected_items[self.player]
        ]

    def test_scan_visor_not_in_item_pool(self):
        assert SuitUpgrade.Scan_Visor.value not in [
            item.name for item in self.multiworld.itempool
        ]


class TestScanVisorRequiredForNonPreScannedElevators(MetroidPrimeTestBase):
    options = {"pre_scan_elevators": False, "shuffle_scan_visor": True}

    def test_starting_room_switches_to_save_1(self):
        self.assertTrue(self.world.starting_room_name == RoomName.Save_Station_1.value)

    def test_scan_visor_required_for_elevator(self):
        state = self.multiworld.state
        self.assertFalse(
            state.can_reach_region(RoomName.Landing_Site.value, self.player)
        )
        self.collect_by_name(SuitUpgrade.Scan_Visor.value)
        self.assertTrue(state.can_reach_region(RoomName.Main_Plaza.value, self.player))


class TestScanVisorNotRequiredForPreScannedElevators(MetroidPrimeTestBase):
    options = {"pre_scan_elevators": True, "shuffle_scan_visor": True}

    def test_starting_room_is_landing_site(self):
        self.assertTrue(self.world.starting_room_name == RoomName.Landing_Site.value)

    def test_scan_visor_not_required_for_elevator(self):
        state = self.multiworld.state
        self.assertTrue(state.can_reach_region(RoomName.Main_Plaza.value, self.player))
