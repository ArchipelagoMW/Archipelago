import typing

from BaseClasses import LocationProgressType
from test.param import classvar_matrix

from .bases import HKTestBase


class ExcludeBase:
    run_default_tests = False

    def is_default(self, location_name: str) -> bool:
        return self.world.get_location(location_name).progress_type == LocationProgressType.DEFAULT

    def is_excluded(self, location_name: str) -> bool:
        return self.world.get_location(location_name).progress_type == LocationProgressType.EXCLUDED

    def assert_excluded(self, location_name: str, expected: bool) -> None:
        test = self.is_excluded if expected else self.is_default
        with self.subTest(name=location_name, excluded=expected):
            self.assertTrue(test(location_name))

    def test_fragment(self):
        if not self.world.options.RandomizeCharms:
            self.assertTrue(self.world.get_location("King_Fragment").item.name == "King_Fragment")

        elif self.world.options.WhitePalace == "exclude":
            self.assertTrue(self.is_excluded("King_Fragment"))
        else:
            self.assertTrue(self.is_default("King_Fragment"))

    def test_lore(self):
        if not self.world.options.RandomizeLoreTablets:
            return
        tablets = (
            "Lore_Tablet-Palace_Workshop",
            "Lore_Tablet-Palace_Throne",
        )
        expected = self.world.options.WhitePalace in ("exclude", "kingfragment")
        for loc in tablets:
            self.assert_excluded(loc, expected)

    def test_totems(self):
        if not self.world.options.RandomizeSoulTotems:
            return
        totems = (
            "Soul_Totem-White_Palace_Entrance",
            "Soul_Totem-White_Palace_Hub",
            "Soul_Totem-White_Palace_Left",
            "Soul_Totem-White_Palace_Final",
            "Soul_Totem-White_Palace_Right",
        )
        expected = self.world.options.WhitePalace in ("exclude", "kingfragment")
        for loc in totems:
            self.assert_excluded(loc, expected)

    def test_pop(self):
        totems = (
            "Soul_Totem-Path_of_Pain_Below_Lever",
            "Soul_Totem-Path_of_Pain_Left_of_Lever",
            "Soul_Totem-Path_of_Pain_Entrance",
            "Soul_Totem-Path_of_Pain_Second",
            "Soul_Totem-Path_of_Pain_Hidden",
            "Soul_Totem-Path_of_Pain_Below_Thornskip",
            "Soul_Totem-Path_of_Pain_Final",
        )
        expected = self.world.options.WhitePalace in ("exclude", "kingfragment", "nopathofpain",)
        if self.world.options.RandomizeLoreTablets:
            self.assert_excluded("Lore_Tablet-Path_of_Pain_Entrance", expected)
        if self.world.options.RandomizeJournalEntries:
            self.assert_excluded("Journal_Entry-Seal_of_Binding", expected)
        if self.world.options.RandomizeSoulTotems:
            for loc in totems:
                self.assert_excluded(loc, expected)


@classvar_matrix(exclude=("exclude", "kingfragment", "nopathofpain", "include",))
class TestExclusions(ExcludeBase, HKTestBase):
    options: typing.ClassVar[dict[str, typing.Any]] = {
        "RandomizeCharms": "True",
        "RandomizeSoulTotems": "True",
        "RandomizeLoreTablets": "True",
        "RandomizeJournalEntries": "True",
        "WhitePalace": "",
    }

    def setUp(self):
        self.options["WhitePalace"] = self.exclude
        super().setUp()
