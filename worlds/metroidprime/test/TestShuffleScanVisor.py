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
        self.assertFalse(self.can_reach_location("Tallon Overworld: Alcove"))

    def test_do_not_start_with_scan_visor(self):
        self.assertNotIn(
            SuitUpgrade.Scan_Visor.value,
            [item.name for item in self.multiworld.precollected_items[self.player]],
        )

    def test_scan_visor_in_item_pool(self):
        self.assertIn(
            SuitUpgrade.Scan_Visor.value,
            [item.name for item in self.multiworld.itempool],
        )


class TestScanVisorNotShuffled(MetroidPrimeTestBase):
    run_default_tests = False  # type: ignore
    options = {
        "trick_difficulty": TrickDifficulty.Easy.value,
        "shuffle_scan_visor": False,
    }

    def test_can_reach_alcove_with_tricks_enabled(self):
        self.assertTrue(self.can_reach_location("Tallon Overworld: Alcove"))

    def test_start_with_scan_visor(self):
        self.assertIn(
            SuitUpgrade.Scan_Visor.value,
            [item.name for item in self.multiworld.precollected_items[self.player]],
        )

    def test_scan_visor_not_in_item_pool(self):
        self.assertNotIn(
            SuitUpgrade.Scan_Visor.value,
            [item.name for item in self.multiworld.itempool],
        )


class TestScanVisorNotRequiredForPreScannedElevators(MetroidPrimeTestBase):
    options = {"pre_scan_elevators": True, "shuffle_scan_visor": True}

    def test_starting_room_is_landing_site(self):
        self.assertEqual(self.world.starting_room_name, RoomName.Landing_Site.value)

    def test_scan_visor_not_required_for_elevator(self):
        state = self.multiworld.state
        self.assertTrue(state.can_reach_region(RoomName.Main_Plaza.value, self.player))
