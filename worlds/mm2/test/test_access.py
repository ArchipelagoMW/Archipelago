from . import MM2TestBase
from ..locations import (quick_man_locations, heat_man_locations, wily_1_locations, wily_2_locations,
                         wily_3_locations, wily_4_locations, wily_5_locations, wily_6_locations,
                         energy_pickups, etank_1ups)
from ..names import *


class TestAccess(MM2TestBase):
    options = {
        "consumables": "all"
    }

    def test_time_stopper(self) -> None:
        """Optional based on Enable Lasers setting, confirm these are the locations affected"""
        locations = [*quick_man_locations, *energy_pickups["Quick Man Stage"], *etank_1ups["Quick Man Stage"]]
        items = [["Time Stopper"]]
        self.assertAccessDependency(locations, items)

    def test_item_2(self) -> None:
        """Optional based on Yoku Block setting, confirm these are the locations affected"""
        locations = [*heat_man_locations, *etank_1ups["Heat Man Stage"]]
        items = [["Item 2 - Rocket"]]
        self.assertAccessDependency(locations, items, True)

    def test_any_item(self) -> None:
        locations = [flash_man_c2, quick_man_c1, crash_man_c3]
        items = [["Item 1 - Propeller"], ["Item 2 - Rocket"], ["Item 3 - Bouncy"]]
        self.assertAccessDependency(locations, items, True)
        locations = [metal_man_c2, metal_man_c3]
        items = [["Item 1 - Propeller"], ["Item 2 - Rocket"]]
        self.assertAccessDependency(locations, items, True)

    def test_all_items(self) -> None:
        locations = [flash_man_c2, quick_man_c1, crash_man_c3, metal_man_c2, metal_man_c3, *heat_man_locations,
                     *etank_1ups["Heat Man Stage"], *wily_1_locations, *wily_2_locations, *wily_3_locations,
                     *wily_4_locations, *wily_5_locations, *wily_6_locations, *etank_1ups["Wily Stage 1"],
                     *etank_1ups["Wily Stage 2"], *etank_1ups["Wily Stage 3"], *etank_1ups["Wily Stage 4"],
                     *energy_pickups["Wily Stage 1"], *energy_pickups["Wily Stage 2"], *energy_pickups["Wily Stage 3"],
                     *energy_pickups["Wily Stage 4"]]
        items = [["Item 1 - Propeller", "Item 2 - Rocket", "Item 3 - Bouncy"]]
        self.assertAccessDependency(locations, items)

    def test_crash_bomber(self) -> None:
        locations = [flash_man_c3, flash_man_c4, wily_2_c5, wily_2_c6, wily_3_c1, wily_3_c2,
                     wily_4, wily_stage_4]
        items = [["Crash Bomber"]]
        self.assertAccessDependency(locations, items)
