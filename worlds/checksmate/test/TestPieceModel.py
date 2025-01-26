from .CMMockTestCase import CMMockTestCase
from ..PieceModel import PieceModel, PieceLimitCascade

class TestPieceModel(CMMockTestCase):
    def setUp(self):
        super().setUp()
        self.piece_model = PieceModel(self.world)
        self.piece_model.items_used = {self.world.player: {}}

    def test_has_prereqs_root_item(self):
        """Test that root items (like pieces) have no prerequisites"""
        root_items = ["Progressive Pawn", "Progressive Minor Piece", "Progressive Major Piece"]
        for item in root_items:
            self.assertTrue(self.piece_model.has_prereqs(item))

    def test_has_prereqs_upgrade_item(self):
        """Test that upgrade items require their prerequisites"""
        # Test queen promotion without major piece
        self.assertFalse(self.piece_model.has_prereqs("Progressive Major To Queen"))
        
        # Add major piece and test again
        self.piece_model.items_used[self.world.player]["Progressive Major Piece"] = 1
        self.assertTrue(self.piece_model.has_prereqs("Progressive Major To Queen"))

    def test_can_add_more_respects_limits(self):
        """Test that can_add_more respects piece type limits"""
        # Should be able to add first two
        self.assertTrue(self.piece_model.can_add_more("Progressive Minor Piece"))
        self.piece_model.items_used[self.world.player]["Progressive Minor Piece"] = 1
        self.assertTrue(self.piece_model.can_add_more("Progressive Minor Piece"))
        
        # Should not be able to add third
        self.piece_model.items_used[self.world.player]["Progressive Minor Piece"] = 99999
        self.assertFalse(self.piece_model.can_add_more("Progressive Minor Piece"))

    def test_piece_limit_cascading(self):
        """Test that piece limits properly cascade to children"""
        # Set up a scenario where we have a major piece that could be upgraded to queen
        self.piece_model.items_used[self.world.player]["Progressive Major To Queen"] = 1
        
        # Test different cascade levels
        no_children = self.piece_model.find_piece_limit(
            "Progressive Major Piece", 
            PieceLimitCascade.NO_CHILDREN
        )
        with_children = self.piece_model.find_piece_limit(
            "Progressive Major Piece",
            PieceLimitCascade.ACTUAL_CHILDREN
        )
        potential = self.piece_model.find_piece_limit(
            "Progressive Major Piece",
            PieceLimitCascade.POTENTIAL_CHILDREN
        )
        
        self.assertLess(no_children, with_children)
        self.assertLess(with_children, potential)