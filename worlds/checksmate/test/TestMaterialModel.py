from .CMMockTestCase import CMMockTestCase
from ..MaterialModel import MaterialModel

class TestMaterialModel(CMMockTestCase):
    def setUp(self):
        super().setUp()
        self.material_model = MaterialModel(self.world)
        self.material_model.items_used = {self.world.player: {}}

    def test_calculate_current_material(self):
        """Test that current material is calculated correctly"""
        # Add some items
        self.material_model.items_used[self.world.player] = {
            "Progressive Pawn": 2,  # 2 * 100 = 200
            "Progressive Minor Piece": 1,  # 1 * 300 = 300
            "Progressive Major Piece": 1  # 1 * 485 = 485
        }
        
        self.assertEqual(self.material_model.calculate_current_material(), 985)

    def test_calculate_remaining_material(self):
        """Test that remaining material from locked items is calculated correctly"""
        locked_items = {
            "Progressive Pawn": 2,  # 2 * 100 = 200
            "Progressive Minor Piece": 1,  # 1 * 300 = 300
            "Progressive Major To Queen": 1  # 1 * 415 = 415
        }
        
        self.assertEqual(self.material_model.calculate_remaining_material(locked_items), 915)

    def test_material_requirements_scaling(self):
        """Test that material requirements scale correctly with board size"""
        min_mat, max_mat = self.material_model.calculate_material_requirements(super_sized=False)
        min_mat_super, max_mat_super = self.material_model.calculate_material_requirements(super_sized=True)
        
        self.assertGreater(min_mat_super, min_mat)
        self.assertGreater(max_mat_super, max_mat)

    def test_unupgraded_majors_in_pool(self):
        """Test counting of unupgraded major pieces"""
        # Create test items
        items = [
            type('CMItem', (), {'name': 'Progressive Major Piece'})(),
            type('CMItem', (), {'name': 'Progressive Major Piece'})(),
            type('CMItem', (), {'name': 'Progressive Major To Queen'})()
        ]
        
        # Test with no locked items
        self.assertEqual(
            self.material_model.unupgraded_majors_in_pool(items, {}),
            1  # 2 majors - 1 upgrade = 1 unupgraded
        )
        
        # Test with locked items
        locked_items = {
            "Progressive Major Piece": 2,
            "Progressive Major To Queen": 1
        }
        self.assertEqual(
            self.material_model.unupgraded_majors_in_pool(items, locked_items),
            2  # (2+2) majors - (1+1) upgrades = 2 unupgraded
        )