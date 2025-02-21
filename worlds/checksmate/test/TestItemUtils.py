import unittest
from ..ItemUtils import get_parents, get_children
from ..Items import item_table


class TestItemUtils(unittest.TestCase):
    def test_get_parents_root_item(self):
        """Test that root items (like pieces) have no parents"""
        root_items = ["Progressive Pawn", "Progressive Minor Piece", "Progressive Major Piece"]
        for item in root_items:
            parents = get_parents(item)
            self.assertEqual(len(parents), 0, f"{item} should have no parents")

    def test_get_parents_upgrade_item(self):
        """Test that upgrade items have correct parents"""
        # Test queen promotion
        queen_parents = get_parents("Progressive Major To Queen")
        self.assertTrue(any(parent[0] == "Progressive Major Piece" for parent in queen_parents))

    def test_get_children_leaf_item(self):
        """Test that leaf items (like final upgrades) have no children"""
        leaf_items = ["Progressive Major To Queen"]  # Add more leaf items as needed
        for item in leaf_items:
            children = get_children(item)
            self.assertEqual(len(children), 0, f"{item} should have no children")

    def test_get_children_parent_item(self):
        """Test that parent items have correct children"""
        # Test major piece children
        major_children = get_children("Progressive Major Piece")
        self.assertIn("Progressive Major To Queen", major_children)

    def test_parent_child_relationship(self):
        """Test that parent-child relationships are consistent"""
        for item_name in item_table:
            parents = get_parents(item_name)
            for parent_name, _ in parents:
                # If A is a parent of B, then B should be in A's children
                children = get_children(parent_name)
                self.assertIn(item_name, children,
                            f"{parent_name} is a parent of {item_name} but {item_name} is not in its children")


if __name__ == '__main__':
    unittest.main() 