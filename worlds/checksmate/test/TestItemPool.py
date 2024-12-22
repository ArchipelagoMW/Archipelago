import unittest
from typing import Dict, List
from BaseClasses import MultiWorld, CollectionState
from Options import DefaultOnToggle, Accessibility, ItemSet
from .. import CMWorld
from ..Items import progression_items, useful_items, filler_items
from ..Options import (CMOptions, MinorPieceLimitByType, MajorPieceLimitByType, 
                      QueenPieceLimitByType, QueenPieceLimit, PocketLimitByPocket,
                      Goal, Difficulty,
                      EnableTactics, PieceLocations, PieceTypes, FairyChessPieces,
                      FairyChessArmy, FairyChessPawns)
from ..ItemPool import CMItemPool


class TestItemPool(unittest.TestCase):
    def setUp(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "ChecksMate"
        self.world = CMWorld(self.multiworld, 1)
        
        # Initialize options with proper option classes
        progression_balancing = DefaultOnToggle(True)
        accessibility = Accessibility.option_full
        local_items = ItemSet({})
        non_local_items = ItemSet({})
        goal = Goal.option_single
        difficulty = Difficulty.option_daily
        enable_tactics = EnableTactics.option_all
        piece_locations = PieceLocations.option_chaos
        piece_types = PieceTypes.option_stable
        fairy_chess_pieces = FairyChessPieces.option_full
        fairy_chess_army = FairyChessArmy.option_stable
        fairy_chess_pawns = FairyChessPawns.option_vanilla
        
        self.world.options = CMOptions(
            progression_balancing,
            accessibility,
            local_items,
            non_local_items,
            [],  # start_inventory
            [],  # start_hints
            [],  # start_location_hints
            set(),  # exclude_locations
            set(),  # priority_locations
            [],  # item_links
            goal,
            difficulty,
            enable_tactics,
            piece_locations,
            piece_types,
            0,  # early_material
            5,  # max_engine_penalties
            12,  # max_pocket
            3,  # max_kings
            2,  # fairy_kings
            fairy_chess_pieces,
            fairy_chess_pieces,  # fairy_chess_pieces_configure
            fairy_chess_army,
            fairy_chess_pawns,
            MinorPieceLimitByType.range_end,
            MajorPieceLimitByType.range_end,
            QueenPieceLimitByType.range_end,
            QueenPieceLimit.range_end,
            PocketLimitByPocket.range_end,
            {},  # locked_items
            False  # death_link
        )
        
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
        self.world.options.enable_tactics.value = self.world.options.enable_tactics.option_none
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

    def test_progression_item_creation(self):
        """Test that progression items are created within material limits"""
        min_mat, max_mat = 10, 20
        items = self.item_pool.create_progression_items(min_mat, max_mat)
        
        total_material = sum(progression_items[item.name].material for item in items)
        self.assertGreaterEqual(total_material, min_mat)
        self.assertLessEqual(total_material, max_mat)

    def test_filler_item_creation(self):
        """Test that filler items respect pocket requirements"""
        # Test without pocket
        items_no_pocket = self.item_pool.create_filler_items(has_pocket=False)
        self.assertTrue(all("Pocket" not in item.name for item in items_no_pocket))
        
        # Test with pocket
        items_with_pocket = self.item_pool.create_filler_items(has_pocket=True)
        has_pocket_items = any("Pocket" in item.name for item in items_with_pocket)
        self.assertTrue(has_pocket_items)

    def test_excluded_items_handling(self):
        """Test that excluded items are handled correctly"""
        excluded = {"Progressive Pawn": 2, "Progressive Minor Piece": 1}
        starter_items = self.item_pool.handle_excluded_items(excluded)
        
        self.assertEqual(len(starter_items), 3)  # 2 pawns + 1 minor piece
        self.assertEqual(self.item_pool.items_used[self.world.player]["Progressive Pawn"], 2)
        self.assertEqual(self.item_pool.items_used[self.world.player]["Progressive Minor Piece"], 1)


if __name__ == '__main__':
    unittest.main() 