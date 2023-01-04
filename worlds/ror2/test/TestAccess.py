from . import RoR2TestBase


class RoR2AccessTest(RoR2TestBase):
    options = {
        "total_locations": 250,
    }

    def testGoal(self):
        self.assertBeatable(False)
        self.collect_all_but(["Dio's Best Friend", "Victory"])
        self.assertBeatable(False)
        self.collect_by_name("Dio's Best Friend")
        self.assertBeatable(True)

    def testAccess(self):
        self.assertEqual(self.can_reach_location("ItemPickup50"), False)
        location = ["Victory"]
        item = [["Dio's Best Friend"]]
        self.assertAccessDependency(location, item)


class RoR2LunarticTest(RoR2TestBase):
    options = {
        "total_locations": 250,
        "item_weights": 4,
        "total_revivals": 0,
        "start_with_revive": 0,
    }

    def count(self, item_name: str) -> int:
        found: int = 0
        for item in self.multiworld.get_items():
            if item.name == item_name:
                found += 1
        return found

    def testAllLunarItems(self):
        self.collect_by_name("Lunar Item")
        self.assertEqual(self.count("Lunar Item"), 250)
