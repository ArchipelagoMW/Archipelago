from .bases import SM64TestBase
from .. import Options
from ..Regions import sm64_entrances_to_level, sm64_level_to_entrances

# Access to Locations/Areas/Entrances by Power Star count in star_cost
class StarCostAccessTestBase(SM64TestBase):
    run_default_tests = False
    options = {
        # Test for access would mean access to entrance/painting,
        # not level itself for the sake of entrance rando.
        "area_rando": Options.AreaRandomizer.option_Courses_and_Secrets,
        "progressive_keys": Options.ProgressiveKeys.option_false
    }

    def test_BoB_entrance_access(self):
        # Always accessible, no stars needed.
        bob_level_id = sm64_entrances_to_level["Bob-omb Battlefield"]
        bob_entrance_id = self.world.area_connections[bob_level_id]
        bob_entrance = sm64_level_to_entrances[bob_entrance_id]
        self.assertTrue(self.can_reach_region(bob_entrance))

    def test_MIPS1_access(self):
        # Requires Basement Key and Power Stars calculated in star_costs["MIPS1Cost"]
        self.assertFalse(self.can_reach_location("MIPS 1"))
        self.collect([self.get_item_by_name("Basement Key")])
        self.assertFalse(self.can_reach_location("MIPS 1"))
        mips1_cost = self.world.star_costs["MIPS1Cost"]
        self.collect([self.get_item_by_name("Power Star")] * mips1_cost)
        self.assertTrue(self.can_reach_location("MIPS 1"))

    def test_MIPS2_access(self):
        # Requires Basement Key and Power Stars calculated in star_costs["MIPS2Cost"]
        self.assertFalse(self.can_reach_location("MIPS 2"))
        self.collect([self.get_item_by_name("Basement Key")])
        self.assertFalse(self.can_reach_location("MIPS 2"))
        mips2_cost = self.world.star_costs["MIPS2Cost"]
        self.collect([self.get_item_by_name("Power Star")] * mips2_cost)
        self.assertTrue(self.can_reach_location("MIPS 2"))

    def test_BitDW_entrance_access(self):
        # Requires Power Stars calculated in star_costs["FirstBowserDoorCost"]
        bitdw_level_id = sm64_entrances_to_level["Bowser in the Dark World"]
        bitdw_entrance_id = self.world.area_connections[bitdw_level_id]
        bitdw_entrance = sm64_level_to_entrances[bitdw_entrance_id]
        self.assertFalse(self.can_reach_region(bitdw_entrance))
        bitdw_cost = self.world.star_costs["FirstBowserDoorCost"]
        self.collect([self.get_item_by_name("Power Star")] * bitdw_cost)
        self.assertTrue(self.can_reach_region(bitdw_entrance))

    # Since BitFS is locked behind "DDD: Board Bowser's Sub", we just need to test DDD.
    def test_DDD_entrance_access(self):
        # Requires Basement Key and Power Stars calculated in star_costs["BasementDoorCost"]
        ddd_level_id = sm64_entrances_to_level["Dire, Dire Docks"]
        ddd_entrance_id = self.world.area_connections[ddd_level_id]
        ddd_entrance = sm64_level_to_entrances[ddd_entrance_id]
        self.assertFalse(self.can_reach_region(ddd_entrance))
        self.collect([self.get_item_by_name("Basement Key")])
        self.assertFalse(self.can_reach_region(ddd_entrance))
        bitfs_cost = self.world.star_costs["BasementDoorCost"]
        self.collect([self.get_item_by_name("Power Star")] * bitfs_cost)
        self.assertTrue(self.can_reach_region(ddd_entrance))

    def test_Floor3_access(self):
        # Requires Second Floor Key and Power Stars calculated in star_costs["SecondFloorDoorCost"]
        self.assertFalse(self.can_reach_region("Third Floor"))
        self.collect([self.get_item_by_name("Second Floor Key")])
        self.assertFalse(self.can_reach_region("Third Floor"))
        floor3_cost = self.world.star_costs["StarsToFinish"]
        self.collect([self.get_item_by_name("Power Star")] * floor3_cost)
        self.assertTrue(self.can_reach_region("Third Floor"))

    def test_BitS_entrance_access(self):
        # Requires Second Floor Key and Power Stars calculated in star_costs["StarsToFinish"]
        self.assertFalse(self.can_reach_region("Bowser in the Sky"))
        self.collect([self.get_item_by_name("Second Floor Key")])
        self.assertFalse(self.can_reach_region("Bowser in the Sky"))
        bits_cost = self.world.star_costs["StarsToFinish"]
        self.collect([self.get_item_by_name("Power Star")] * bits_cost)
        self.assertTrue(self.can_reach_region("Third Floor"))
        self.assertTrue(self.can_reach_region("Bowser in the Sky"))
