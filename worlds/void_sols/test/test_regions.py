from worlds.void_sols.test.bases import VoidSolsTestBase
from worlds.void_sols.Names import ItemName, LocationName
from BaseClasses import CollectionState

class TestRegions(VoidSolsTestBase):
    def collect_event(self, event_name: str) -> None:
        item = self.get_item_by_name(event_name)
        self.collect(item)

    def test_region_connections(self) -> None:
        """Test basic region connections"""
        self.multiworld.state = CollectionState(self.multiworld)
        
        # Menu -> Prison
        self.assertTrue(self.can_reach_region("Prison"))
        
        # Prison -> Prison Yard (Requires Warden Defeated Event)
        self.assertFalse(self.can_reach_region("Prison Yard"))
        self.collect_event(ItemName.prison_warden_defeated_event)
        self.assertTrue(self.can_reach_region("Prison Yard"))
        
        # Prison Yard -> Forest (Requires Gate Key)
        self.assertFalse(self.can_reach_region("Forest"))
        self.collect_by_name(ItemName.gate_key)
        self.assertTrue(self.can_reach_region("Forest"))
        
        # Forest -> Village (Open)
        self.assertTrue(self.can_reach_region("Village"))

    def test_mines_progression(self) -> None:
        """Test progression through the mines floors"""
        self.multiworld.state = CollectionState(self.multiworld)
        
        # Need to reach Forest first
        self.collect_event(ItemName.prison_warden_defeated_event)
        self.collect_by_name(ItemName.gate_key)
        
        # Forest -> Mines Floor 1 (Requires Mine Entrance Lift Key)
        self.assertFalse(self.can_reach_region("Mines Floor 1"))
        self.collect_by_name(ItemName.mine_entrance_lift_key)
        self.assertTrue(self.can_reach_region("Mines Floor 1"))
        
        # Mines Floor 1 -> Mines Floor 2 (Requires Minecart Wheel)
        self.assertFalse(self.can_reach_region("Mines Floor 2"))
        self.collect_by_name(ItemName.minecart_wheel)
        self.assertTrue(self.can_reach_region("Mines Floor 2"))
        
        # Mines Floor 2 -> Mines Floor 3 (Requires Lift Key)
        self.assertFalse(self.can_reach_region("Mines Floor 3"))
        self.collect_by_name(ItemName.lift_key)
        self.assertTrue(self.can_reach_region("Mines Floor 3"))
        
        # Mines Floor 3 -> Mines Floor 4 (Requires Pit Catwalk Key)
        self.assertFalse(self.can_reach_region("Mines Floor 4"))
        self.collect_by_name(ItemName.pit_catwalk_key)
        self.assertTrue(self.can_reach_region("Mines Floor 4"))

    def test_apex_access(self) -> None:
        """Test access to Apex regions"""
        self.multiworld.state = CollectionState(self.multiworld)

        # Need to reach Forest first
        self.collect_event(ItemName.prison_warden_defeated_event)
        self.collect_by_name(ItemName.gate_key)

        # Forest -> Apex Outskirts (Requires Apex Outskirts Key OR Dynamite)
        # Use dynamite to reach outskirts without getting the key (which would trigger the event)
        self.assertFalse(self.can_reach_region("Apex Outskirts"))
        self.collect_by_name(ItemName.dynamite_x1)
        self.assertTrue(self.can_reach_region("Apex Outskirts"))
        
        # Apex Outskirts -> Apex (Requires Gatekeeper Defeated Event)
        self.collect_event(ItemName.apex_gatekeeper_defeated_event)
        self.assertTrue(self.can_reach_region("Apex"))
