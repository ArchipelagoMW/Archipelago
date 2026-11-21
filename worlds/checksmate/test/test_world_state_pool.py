import unittest

from test.general import setup_multiworld

from .. import CMWorld


class TestWorldPoolState(unittest.TestCase):
    def setUp(self) -> None:
        multiworld = setup_multiworld([CMWorld, CMWorld], steps=(), seed=0)
        self.first = multiworld.worlds[1]
        self.second = multiworld.worlds[2]

    def test_world_instances_do_not_share_generation_state(self) -> None:
        self.first.pool_accounting.add_used("Progressive Pawn", 2)
        self.first.pool_accounting.set_remaining("Progressive Pawn", 58)
        self.first.army_ids.append(0)
        self.first.locked_locations.append("Checkmate Minima")

        self.assertEqual({"Progressive Pawn": 2}, self.first.pool_accounting.used)
        self.assertEqual({}, self.second.pool_accounting.used)
        self.assertEqual({}, self.second.pool_accounting.remaining)
        self.assertEqual([], self.second.army_ids)
        self.assertEqual([], self.second.locked_locations)

        self.first.items_used[self.first.player]["Progressive Minor Piece"] = 1
        self.assertEqual(
            1,
            self.first.pool_accounting.used["Progressive Minor Piece"],
        )
        self.assertNotIn(
            "Progressive Minor Piece",
            self.second.pool_accounting.used,
        )

    def test_world_has_one_authoritative_pool_service_graph(self) -> None:
        first_pool = self.first._item_pool
        second_pool = self.second._item_pool

        self.assertIs(first_pool.accounting, self.first.pool_accounting)
        self.assertIs(first_pool.piece_model.accounting, first_pool.accounting)
        self.assertIs(first_pool.material_model.accounting, first_pool.accounting)
        self.assertIs(
            first_pool.removal_rules.piece_model,
            first_pool.piece_model,
        )

        self.assertIsNot(first_pool, second_pool)
        self.assertIsNot(first_pool.accounting, second_pool.accounting)
        self.assertIsNot(first_pool.piece_model, second_pool.piece_model)
        self.assertIsNot(first_pool.material_model, second_pool.material_model)
        self.assertNotIn("_piece_model", self.first.__dict__)
        self.assertNotIn("_material_model", self.first.__dict__)
