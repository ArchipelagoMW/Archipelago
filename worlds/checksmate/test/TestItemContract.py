import sys
import unittest

from ..Items import item_table


class TestItemContract(unittest.TestCase):
    def test_current_item_ids_quantities_and_material_values(self):
        expected = {
            "Play as White": (4_901_000, 1, 50),
            "Progressive AI Intelligence Malus": (4_901_001, 5, 0),
            "Progressive Pawn": (4_901_002, 60, 100),
            "Progressive Pawn Forwardness": (4_901_003, 13, 0),
            "Progressive Minor Piece": (4_901_004, 15, 300),
            "Progressive Major Piece": (4_901_005, 11, 485),
            "Progressive Major To Queen": (4_901_006, 9, 415),
            "Progressive Jack": (4_901_007, 9, 700),
            "Chessmen": (4_901_008, 107, 100),
            "Victory": (4_901_009, 1, 0),
            "Super-Size Me": (4_901_010, 0, 0),
            "Material": (4_901_011, 321, 400),
            "Castler": (4_901_012, 2, 0),
            "Board Files": (4_901_013, 2, 0),
            "Board Ranks": (4_901_014, 2, 0),
            "Progressive Pocket": (4_901_020, 12, 110),
            "Progressive Pocket Gems": (4_901_023, sys.maxsize, 0),
            "Progressive Pocket Range": (4_901_024, 6, 0),
            "Progressive King Promotion": (4_901_025, 2, 425),
            "Progressive Consul": (4_901_026, 2, 325),
        }

        actual = {
            name: (data.code, data.quantity, data.material)
            for name, data in item_table.items()
        }

        self.assertEqual(expected, actual)

    def test_current_upgrade_item_identity_and_parent_spelling(self):
        self.assertEqual(
            [["Progressive Major Piece", 1]],
            item_table["Progressive Major To Queen"].parents,
        )
        self.assertNotIn("Progressive Queen", item_table)
