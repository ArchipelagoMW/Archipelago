from BaseClasses import LocationProgressType

from . import GameDevTycoonTestBase

RND = ["R&D: Internet Opportunities", "R&D: Grid", "R&D: Own Convention", "R&D: Sublicense Engines",
       "R&D: Hardware Lab", "R&D: MMO", "R&D: 3D Graphics V6", "R&D: 3D Graphics V7", "R&D: AAA Marketing Campaign",
       "R&D: AAA Custom Hardware"]


class TestRnDProjects(GameDevTycoonTestBase):
    def test_projects_need_the_studio(self) -> None:
        for name in RND:
            self.assertFalse(self.can_reach_location(name), name)
        self.collect_by_name(["Progressive Office Upgrade"] * 3)
        for name in RND:
            self.assertTrue(self.can_reach_location(name), name)


class TestOwnConventionEarlyRetirement(GameDevTycoonTestBase):
    options = {"retirement_year": 20}

    def test_own_convention_is_excluded(self) -> None:
        loc = self.multiworld.get_location("R&D: Own Convention", self.player)
        self.assertEqual(loc.progress_type, LocationProgressType.EXCLUDED)
