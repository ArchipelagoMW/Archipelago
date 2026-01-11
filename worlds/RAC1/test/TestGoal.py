from worlds.RAC1.data.Locations import VELDIN_HALFWAY_GOLD_BOLT
from worlds.RAC1.test import RACTestBase


class TestDrek(RACTestBase):
    options = {}

    def test_goal(self) -> None:
        """Test various states to verify goal is beatable with correct items"""
        self.collect_by_name("Veldin")
        self.assertEqual(self.can_reach_region("Veldin"), True, msg="Veldin region not reached with the infobot")
        self.collect_by_name(["Trespasser", "Hydrodisplacer", "Magneboots", "Thruster Pack"])
        self.assertAccessDependency([VELDIN_HALFWAY_GOLD_BOLT.name],
                                    [["Trespasser", "Hydrodisplacer", "Magneboots", "Thruster Pack", "Veldin"]],
                                    True)
        self.assertBeatable(False)
        self.remove_by_name("Veldin")
        self.assertBeatable(False)
        self.collect_by_name("Swingshot")
        self.assertBeatable(False)
        self.collect_all_but(["Veldin", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("Veldin")
        self.assertBeatable(True)
