from BaseClasses import CollectionState
from .bases import CCCharlesTestBase


class TestAccess(CCCharlesTestBase):
    def test_claire_breakers(self) -> None:
        """Test locations that require 4 Breakers"""
        lighthouse_claire_mission_end = self.world.get_location("Lighthouse Claire Mission End")

        state = CollectionState(self.multiworld)
        self.collect_all_but("Breaker")

        breakers_in_pool = self.get_items_by_name("Breaker")
        self.assertGreaterEqual(len(breakers_in_pool), 4) # Check at least 4 Breakers are in the item pool

        for breaker in breakers_in_pool[:3]:
            state.collect(breaker) # Collect 3 Breakers into state
        self.assertFalse(
            lighthouse_claire_mission_end.can_reach(state),
            "Lighthouse Claire Mission End should not be reachable with only three Breakers"
        )

        state.collect(breakers_in_pool[3]) # Collect 4th breaker into state
        self.assertTrue(
            lighthouse_claire_mission_end.can_reach(state),
            "Lighthouse Claire Mission End should have been reachable with four Breakers"
        )
