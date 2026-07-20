import hashlib
import json
from pathlib import Path
import unittest

from .. import CMWorld
from ..apmw_projection import (
    FROZEN_CONTRACT_HASH,
    PROTOCOL_VERSION,
    RUNTIME_SEMANTIC_VERSION,
)
from ..apmw_projection.contract import compute_manifest_sha256
from ..contract_resource import UNLOCK_ITEM_ROLES, load_production_contract
from ..items import item_table
from ..locations import (
    BoardStage,
    GEOMETRY_UNLOCKS_BY_STAGE,
    location_names_for_stage,
)


CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CONTRACT_HASH = "f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15"
EXPECTED_RESOURCE_SHA256 = "56eb5e5e8ccfe69babd1fda0820a6e81497f542679a1061ba62488bb0f0518fb"
EXPECTED_MAXIMA = {
    "common": {
        "Play as White": 1,
        "Progressive AI Intelligence Malus": 5,
        "Progressive Pocket": 12,
        "Progressive Pocket Range": 6,
        "Progressive King Promotion": 2,
        "Progressive Consul": 2,
    },
    "legacy": {
        "Progressive Pawn": 60,
        "Progressive Pawn Forwardness": 13,
        "Progressive Minor Piece": 15,
        "Progressive Major Piece": 11,
        "Progressive Major To Queen": 9,
        "Progressive Jack": 9,
    },
    "fundamental": {
        "Chessmen": 107,
        "Material": 321,
        "Castler": 2,
    },
}
EXPECTED_MATERIAL = {
    "weak": 75,
    "pawn": 100,
    "minor": 300,
    "major": 485,
    "castler": 500,
    "jack": 700,
    "queen": 900,
    "amazon": 1300,
    "material_item": 400,
    "play_as_white": 50,
    "pocket": 110,
    "consul": 325,
    "king_promotion": 425,
}
EXPECTED_STAGES = (
    (BoardStage.Board8x8, "8x8", (0, 0), (71, 65, 61)),
    (BoardStage.Board10x8, "10x8", (1, 0), (86, 80, 76)),
    (BoardStage.Board10x10, "10x10", (1, 1), (87, 81, 77)),
    (BoardStage.Board12x10, "12x10", (2, 1), (102, 96, 92)),
    (BoardStage.Board12x12, "12x12", (2, 2), (103, 97, 93)),
)


class TestContractRuntimeConsistency(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_production_contract()

    def test_canonical_contract_snapshot_hash_and_runtime_metadata_are_frozen(self):
        canonical = (
            CHECKSMATE_ROOT
            / "apmw_projection"
            / "data"
            / "apmw_contract_v2.json"
        )
        compatibility_snapshot = (
            CHECKSMATE_ROOT
            / "test"
            / "fixtures"
            / "projection-v2"
            / "baseline.json"
        )
        self.assertFalse(
            (CHECKSMATE_ROOT / "data" / "apmw_contract_v2.json").exists()
        )
        canonical_text = canonical.read_text(encoding="utf-8")
        self.assertEqual(
            canonical_text,
            compatibility_snapshot.read_text(encoding="utf-8"),
        )
        canonical_bytes = canonical_text.encode("utf-8")
        self.assertEqual(
            EXPECTED_RESOURCE_SHA256,
            hashlib.sha256(canonical_bytes).hexdigest(),
        )
        self.assertEqual(
            EXPECTED_CONTRACT_HASH,
            compute_manifest_sha256(canonical_text),
        )
        self.assertEqual(EXPECTED_CONTRACT_HASH, FROZEN_CONTRACT_HASH)
        self.assertEqual(1, PROTOCOL_VERSION)
        self.assertEqual("0.1.0", RUNTIME_SEMANTIC_VERSION)

    def test_required_client_and_world_versions_match_contract(self):
        metadata = json.loads(
            (CHECKSMATE_ROOT / "archipelago.json").read_text(encoding="utf-8")
        )
        self.assertEqual("0.4.0", self.contract.minimum_client_version)
        self.assertEqual("0.4.0", CMWorld.required_chess_client_version)
        self.assertEqual("0.4.0", metadata["world_version"])

    def test_runtime_item_maxima_match_contract_modes(self):
        self.assertEqual(EXPECTED_MAXIMA, self.contract.effective_item_maxima)
        for mode in EXPECTED_MAXIMA.values():
            for name, maximum in mode.items():
                with self.subTest(item=name):
                    self.assertEqual(maximum, item_table[name].quantity)

    def test_runtime_item_material_values_match_contract_semantics(self):
        self.assertEqual(EXPECTED_MATERIAL, self.contract.expected_material)
        expected_runtime = {
            "Play as White": EXPECTED_MATERIAL["play_as_white"],
            "Progressive Pawn": EXPECTED_MATERIAL["pawn"],
            "Progressive Minor Piece": EXPECTED_MATERIAL["minor"],
            "Progressive Major Piece": EXPECTED_MATERIAL["major"],
            "Progressive Major To Queen": (
                EXPECTED_MATERIAL["queen"] - EXPECTED_MATERIAL["major"]
            ),
            "Progressive Jack": EXPECTED_MATERIAL["jack"],
            "Chessmen": EXPECTED_MATERIAL["pawn"],
            "Material": EXPECTED_MATERIAL["material_item"],
            "Progressive Pocket": EXPECTED_MATERIAL["pocket"],
            "Progressive King Promotion": EXPECTED_MATERIAL["king_promotion"],
            "Progressive Consul": EXPECTED_MATERIAL["consul"],
        }
        self.assertEqual(
            expected_runtime,
            {name: item_table[name].material for name in expected_runtime},
        )
        self.assertEqual(EXPECTED_MATERIAL["castler"], self.contract.castler.normalized_material)
        self.assertEqual(0, item_table["Castler"].material)

    def test_board_stage_unlocks_and_location_profiles_match_contract(self):
        self.assertEqual(
            {
                BoardStage.Board8x8: (0, 0),
                BoardStage.Board10x8: (1, 0),
                BoardStage.Board10x10: (1, 1),
                BoardStage.Board12x10: (2, 1),
                BoardStage.Board12x12: (2, 2),
            },
            GEOMETRY_UNLOCKS_BY_STAGE,
        )
        self.assertEqual(
            {
                "Board Files": "board-file-unlock",
                "Board Ranks": "board-rank-unlock",
            },
            UNLOCK_ITEM_ROLES,
        )
        self.assertEqual(2, item_table["Board Files"].quantity)
        self.assertEqual(2, item_table["Board Ranks"].quantity)
        self.assertEqual(
            (
                ("board-file-unlock", 8, 2, 12),
                ("board-rank-unlock", 8, 2, 12),
            ),
            tuple(
                (role.role_id, role.base, role.increment, role.maximum)
                for role in self.contract.geometry_unlocks.roles
            ),
        )

        contract_stages = dict(zip(self.contract.stage_order, self.contract.stages))
        for board_stage, stage_id, unlocks, totals in EXPECTED_STAGES:
            with self.subTest(stage=stage_id):
                stage = contract_stages[stage_id]
                self.assertEqual(unlocks, GEOMETRY_UNLOCKS_BY_STAGE[board_stage])
                self.assertEqual(
                    totals,
                    (
                        stage.all_tactics_locations,
                        stage.turns_locations,
                        stage.no_tactics_locations,
                    ),
                )
                self.assertEqual(
                    totals,
                    tuple(
                        len(location_names_for_stage(board_stage, mode))
                        for mode in ("all", "turns", "none")
                    ),
                )


if __name__ == "__main__":
    unittest.main()
