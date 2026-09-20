from .bases import MM3TestBase
from ..locations import get_boss_locations, get_oneup_locations, get_energy_locations
from ..names import *


class TestAccess(MM3TestBase):
    options = {
        "consumables": "all"
    }

    def test_rush_jet(self) -> None:
        locations = [wily_2_boss, wily_stage_2, needle_man_c2, gemini_man_c1, doc_needle_c2, doc_needle_c3,
                     wily_2_c5, wily_2_c6, wily_2_c7, wily_2_c8, wily_2_c9, wily_2_c10, wily_2_c11,
                     wily_2_c12, wily_2_c13]
        # while it also locks every stage past wily 2, checking for Wily Stage 2 is sufficient for coverage
        items = [[rush_jet]]
        self.assertAccessDependency(locations, items, True)

    def test_any_rush(self) -> None:
        locations = [gemini_man, get_gemini_laser, gemini_man_c6, gemini_man_c7,
                     gemini_man_c8, gemini_man_c9, gemini_man_c10,]
        items = [[rush_jet], [rush_coil], [rush_marine]]
        self.assertAccessDependency(locations, items, True)

    def test_rush_vertical(self):
        locations = [hard_man, get_hard_knuckle, wily_1_boss,
                     wily_stage_1, *get_boss_locations("Doc Robot (Needle) - Air"),
                     *get_energy_locations("Doc Robot (Needle) - Air"),
                     *get_boss_locations("Doc Robot (Spark) - Metal"),
                     *get_energy_locations("Doc Robot (Spark) - Metal"),
                     *get_oneup_locations("Doc Robot (Spark) - Metal"),
                     *get_boss_locations("Doc Robot (Gemini) - Bubble"),
                     *get_oneup_locations("Doc Robot (Gemini) - Bubble"),
                     *get_energy_locations("Doc Robot (Gemini) - Bubble"),
                     gemini_man_c2, gemini_man_c3, gemini_man_c4, gemini_man_c5,
                     hard_man_c2, hard_man_c3, hard_man_c4, hard_man_c5, hard_man_c6,
                     hard_man_c7, top_man_c2, top_man_c3, top_man_c4, top_man_c6,
                     top_man_c7, spark_man_c1, spark_man_c2, doc_gemini_c1, doc_gemini_c2,
                     wily_1_c6, wily_1_c7, wily_1_c8, wily_1_c11, wily_1_c12]
        items = [[rush_jet], [rush_coil]]
        self.assertAccessDependency(locations, items, True)

    def test_long_water(self) -> None:
        locations = [*get_boss_locations("Doc Robot (Gemini) - Bubble"),
                     *get_oneup_locations("Doc Robot (Gemini) - Bubble"),
                     *get_energy_locations("Doc Robot (Gemini) - Bubble"),]
        items = [[rush_jet], [rush_marine]]
        self.assertAccessDependency(locations, items, True)

    def test_hard_knuckle(self) -> None:
        locations = [wily_1_c4, wily_1_c5, wily_1_c6, wily_1_c7, wily_1_c8, ]
        items = [[hard_knuckle]]
        self.assertAccessDependency(locations, items, True)

    def test_vertical_attack(self) -> None:
        locations = [*get_boss_locations("Doc Robot (Spark) - Metal"),
                     *get_oneup_locations("Doc Robot (Spark) - Metal"),
                     *get_energy_locations("Doc Robot (Spark) - Metal"),
                     gemini_man_c3]
        items = [[shadow_blade], [gemini_laser]]
        self.assertAccessDependency(locations, items, True)
