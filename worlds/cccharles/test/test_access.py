from worlds.cccharles.test import MyGameTestBase


class TestChestAccess(MyGameTestBase):
    def test_claire_breakers(self) -> None:
        """Test locations that require 4 Breakers"""
        locations = ["Lighthouse Claire Mission End"]
        items = [["Breaker"] * 4]
        # Test locations cannot be accessed without 4 "Breaker", but can be accessed once obtained
        self.assertAccessDependency(locations, items)
