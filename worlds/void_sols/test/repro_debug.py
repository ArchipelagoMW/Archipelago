import unittest
from worlds.void_sols.test.bases import VoidSolsTestBase
from worlds.void_sols.Names import ItemName, LocationName
from BaseClasses import CollectionState

class TestDebug(VoidSolsTestBase):
    def test_debug_apex_access(self) -> None:
        # Check if Apex Outskirts is reachable without keys
        location = LocationName.apex_outskirts_item_pickup_golden_clover
        items_to_remove = [ItemName.apex_outskirts_key, ItemName.dynamite_x1, ItemName.mine_entrance_lift_key]
        
        state = CollectionState(self.multiworld)
        self.collect_all_but(items_to_remove, state)
        
        print(f"\nHas Mine Entrance Lift Key: {state.has(ItemName.mine_entrance_lift_key, self.player)}")
        print(f"Has Dynamite: {state.has(ItemName.dynamite_x1, self.player)}")
        print(f"Has Apex Outskirts Key: {state.has(ItemName.apex_outskirts_key, self.player)}")
        print(f"Has Prison Warden Defeated Event: {state.has(ItemName.prison_warden_defeated_event, self.player)}")
        print(f"Has Gate Key: {state.has(ItemName.gate_key, self.player)}")
        
        can_reach = state.can_reach(location, "Location", self.player)
        print(f"Can reach {location}: {can_reach}")
        
        regions = ["Prison", "Prison Yard", "Forest", "Mines Floor 1", "Apex Outskirts"]
        for r in regions:
            print(f"Can reach region {r}: {state.can_reach(r, 'Region', self.player)}")

    def test_debug_prison_yard(self) -> None:
        # Check why Prison Yard is reachable
        print("\n--- Debug Prison Yard ---")
        state = CollectionState(self.multiworld)
        # We need to remove the event to test if it's reachable without it
        # But collect_all_but collects everything else.
        # Let's try to see if we can reach it with just the event
        
        # Actually, the issue is that Prison Yard IS reachable in test_region_connections
        # self.assertFalse(self.can_reach_region("Prison Yard")) fails -> means it IS reachable
        
        # Let's check what's in the state
        print(f"Has Prison Warden Defeated Event: {self.multiworld.state.has(ItemName.prison_warden_defeated_event, self.player)}")
        print(f"Can reach Prison: {self.can_reach_region('Prison')}")
        print(f"Can reach Prison Yard: {self.can_reach_region('Prison Yard')}")
