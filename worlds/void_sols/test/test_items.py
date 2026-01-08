from worlds.void_sols.test.bases import VoidSolsTestBase
from worlds.void_sols.Names import ItemName

class TestItems(VoidSolsTestBase):
    def test_item_classification(self) -> None:
        """Test that key items are classified correctly as progression"""
        progression_items = [
            ItemName.prison_key,
            ItemName.gate_key,
            ItemName.forest_bridge_key,
            ItemName.mine_entrance_lift_key,
            ItemName.minecart_wheel,
            ItemName.lift_key,
            ItemName.pit_catwalk_key,
            ItemName.temple_of_the_deep_key,
            ItemName.east_wing_key,
            ItemName.apex_outskirts_key,
            ItemName.fishing_rod,
            ItemName.flaming_torch_x1,
            ItemName.dynamite_x1,
            ItemName.strange_curio,
        ]
        
        for item_name in progression_items:
            item = self.world.create_item(item_name)
            self.assertTrue(item.advancement, f"Item {item_name} should be progression")

    def test_filler_items(self) -> None:
        """Test that filler items are classified correctly"""
        filler_items = [
            ItemName.glitterstone_x1,
            ItemName.snare_trap_x2,
            ItemName.harsh_pepper_x1,
            ItemName.ritual_needle_x2,
            ItemName.verdant_berry_x2,
            ItemName.chewy_seaweed_x2,
            ItemName.purifying_needle_x2,
            ItemName.bursting_bubble_x1,
            ItemName.caltrops_x2,
            ItemName.stale_bread_x1,
            ItemName.pocket_barrel_x1,
            ItemName.pet_worm_x3,
            ItemName.minor_sol_shard,
            ItemName.major_sol_shard,
        ]
        
        for item_name in filler_items:
            item = self.world.create_item(item_name)
            self.assertFalse(item.advancement, f"Item {item_name} should not be progression")
            self.assertFalse(item.useful, f"Item {item_name} should not be useful")
