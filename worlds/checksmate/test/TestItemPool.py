import functools

from .CMMockTestCase import CMMockTestCase
from ..ItemPool import CMItemPool
from ..Items import progression_items
from ..Options import EnableTactics


class TestItemPool(CMMockTestCase):
    def setUp(self):
        super().setUp()
        self.item_pool = CMItemPool(self.world)
        self.item_pool.initialize_item_tracking()
        
    def test_material_requirements(self):
        """Test that material requirements are calculated correctly for both board sizes"""
        min_mat, max_mat = self.item_pool.calculate_material_requirements(super_sized=False)
        self.assertGreater(max_mat, min_mat)
        
        min_mat_super, max_mat_super = self.item_pool.calculate_material_requirements(super_sized=True)
        self.assertGreater(min_mat_super, min_mat)
        self.assertGreater(max_mat_super, max_mat)

    def test_progression_item_pool_preparation(self):
        """Test that the progression item pool is prepared with correct frequencies"""
        pool = self.item_pool.prepare_progression_item_pool()
        
        # Check Victory is removed
        self.assertNotIn("Victory", pool)

    def test_option_limits(self):
        """Test that option limits are correctly applied"""
        self.item_pool.handle_option_limits()
        
        # Check king limits
        self.assertLessEqual(
            self.item_pool.items_used[self.world.player]["Progressive Consul"],
            3 - self.world.options.max_kings.value
        )
        
        # Check fairy king limits
        self.assertLessEqual(
            self.item_pool.items_used[self.world.player]["Progressive King Promotion"],
            2 - self.world.options.fairy_kings.value
        )
        
        # Check engine penalty limits
        self.assertLessEqual(
            self.item_pool.items_used[self.world.player]["Progressive Engine ELO Lobotomy"],
            5 - self.world.options.max_engine_penalties.value
        )

    def test_max_items_calculation(self):
        """Test that max items are calculated correctly based on options"""
        base_max = self.item_pool.get_max_items(super_sized=False)
        super_max = self.item_pool.get_max_items(super_sized=True)
        self.assertGreater(super_max, base_max)
        
        # Test with tactics disabled
        self.world.options.enable_tactics = EnableTactics(EnableTactics.option_none)
        no_tactics_max = self.item_pool.get_max_items(super_sized=False)
        self.assertLess(no_tactics_max, base_max)

    def test_item_consumption_tracking(self):
        """Test that item consumption is tracked correctly"""
        test_item = next(iter(progression_items.keys()))
        initial_quantity = progression_items[test_item].quantity
        
        self.item_pool.consume_item(test_item, {})
        
        self.assertEqual(self.item_pool.items_used[self.world.player][test_item], 1)
        self.assertEqual(
            self.item_pool.items_remaining[self.world.player][test_item],
            initial_quantity - 1
        )

    def test_pocket_limit(self):
        """Test that pocket limits are correctly applied"""
        min_mat, max_mat = 4100, 4600
        max_items = 100
        locked_items = {}
        items = self.item_pool.create_progression_items(
            max_items=max_items,
            min_material=min_mat,
            max_material=max_mat,
            locked_items=locked_items
        )
        if self.world.options.pocket_limit_by_pocket.value > 0:
            self.assertLessEqual(
                functools.reduce(lambda x, y: x + 1, [item for item in items if item.name == "Progressive Pocket"], 0),
                self.world.options.pocket_limit_by_pocket.value * 3
            )
        if self.world.options.max_pocket.value > 0:
            self.assertLessEqual(
                functools.reduce(lambda x, y: x + 1, [item for item in items if item.name == "Progressive Pocket"], 0),
                self.world.options.max_pocket.value
            )

    def test_progression_item_creation(self):
        """Test that progression items are created within material limits"""
        min_mat, max_mat = 4100, 4600
        max_items = 100
        locked_items = {}
        items = self.item_pool.create_progression_items(
            max_items=max_items,
            min_material=min_mat,
            max_material=max_mat,
            locked_items=locked_items
        )
        
        added_material = sum(progression_items[item.name].material for item in items)
        locked_material = sum(progression_items[item_name].material * count 
                            for item_name, count in locked_items.items())
        total_material = added_material + locked_material
        
        self.assertGreaterEqual(total_material, min_mat)
        self.assertLessEqual(total_material, max_mat)
        
        # Also verify we don't exceed max_items
        self.assertLessEqual(len(items), max_items)

    def test_filler_item_creation_respects_pocket(self):
        """Test that filler items respect pocket requirements"""
        max_items = 100
        # Test without pocket
        items_no_pocket = self.item_pool.create_filler_items(has_pocket=False, max_items=max_items)
        # Allow Progressive Pocket Gems as it's effectively a do-nothing item
        self.assertTrue(all(("Pocket" not in item.name) or (item.name == "Progressive Pocket Gems") for item in items_no_pocket))
        
        # Test with pocket
        items_with_pocket = self.item_pool.create_filler_items(has_pocket=True, max_items=max_items)
        has_pocket_items = any("Pocket" in item.name for item in items_with_pocket)
        self.assertTrue(has_pocket_items)

    def test_filler_item_creation_with_pocket(self):
        """Test that filler item creation handles pocket gems as fallback"""
        max_items = 100
        user_location_count = 5  # Simulate some existing locations
        locked_items = {"Progressive Major Piece": 2}  # Simulate some locked items
        
        # Test with pocket
        items_with_pocket = self.item_pool.create_filler_items(
            has_pocket=True,
            max_items=max_items,
            user_location_count=user_location_count,
            locked_items=locked_items
        )
        total_count = len(items_with_pocket) + user_location_count + sum(locked_items.values())
        self.assertLessEqual(total_count, max_items)
        
    def test_filler_item_creation_no_pocket(self):
        """Test that filler item creation handles no pocket gems"""
        max_items = 100
        user_location_count = 5  # Simulate some existing locations
        locked_items = {"Progressive Major Piece": 2}  # Simulate some locked items
        
        # Test without pocket
        items_no_pocket = self.item_pool.create_filler_items(
            has_pocket=False, max_items=max_items,
            user_location_count=user_location_count,
            locked_items=locked_items
        )
        total_count = len(items_no_pocket) + user_location_count + sum(locked_items.values())
        self.assertLessEqual(total_count, max_items)

    def test_excluded_items_handling(self):
        """Test that excluded items are handled correctly"""
        excluded = {"Progressive Pawn": 2, "Progressive Minor Piece": 1}
        starter_items = self.item_pool.handle_excluded_items(excluded)
        
        self.assertEqual(len(starter_items), 3)  # 2 pawns + 1 minor piece
        self.assertEqual(self.item_pool.items_used[self.world.player]["Progressive Pawn"], 2)
        self.assertEqual(self.item_pool.items_used[self.world.player]["Progressive Minor Piece"], 1)
