from . import MM2TestBase
from ..locations import (get_oneup_locations, get_boss_locations, get_energy_locations, mm2_regions)
from ..names import *


class TestAccess(MM2TestBase):
    options = {
        "consumables": "all",
        "yoku_jumps": False,
        "enable_lasers": False,
    }

    def test_time_stopper(self) -> None:
        """Optional based on Enable Lasers setting, confirm these are the locations affected"""
        locations = list(mm2_regions["Quick Man Stage"].locations.keys())
        items = [["Time Stopper"]]
        self.assertAccessDependency(locations, items)

    def test_item_2(self) -> None:
        """Optional based on Yoku Block setting, confirm these are the locations affected"""
        locations = list(mm2_regions["Heat Man Stage"].locations.keys())
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
        locations = [flash_man_c2, quick_man_c1, crash_man_c3, metal_man_c2, metal_man_c3,
                     *list(mm2_regions["Heat Man Stage"].locations.keys()),
                     *list(mm2_regions["Wily Stage 1"].locations.keys()),
                     *list(mm2_regions["Wily Stage 2"].locations.keys()),
                     *list(mm2_regions["Wily Stage 3"].locations.keys()),
                     *list(mm2_regions["Wily Stage 4"].locations.keys()),
                     *list(mm2_regions["Wily Stage 5"].locations.keys()),
                     *list(mm2_regions["Wily Stage 6"].locations.keys()),
                     ]
        items = [["Item 1 - Propeller", "Item 2 - Rocket", "Item 3 - Bouncy"]]
        self.assertAccessDependency(locations, items)

    def test_crash_bomber(self) -> None:
        locations = [flash_man_c3, flash_man_c4, wily_2_c5, wily_2_c6, wily_3_c1, wily_3_c2,
                     wily_4, wily_stage_4]
        items = [["Crash Bomber"]]
        self.assertAccessDependency(locations, items)
