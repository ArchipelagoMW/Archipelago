from worlds.cccharles.test import MyGameTestBase


class TestChestAccess(MyGameTestBase):
    def test_claire_breakers(self) -> None:
        """Test locations that require 4 Breakers"""
        locations = ["lighthouse_claire_mission_end"]
        items = [["Breaker"], ["Breaker"], ["Breaker"], ["Breaker"]]
        # This will test that each location can't be accessed without 4 "Breaker", but can be accessed once obtained
        self.assertAccessDependency(locations, items)
