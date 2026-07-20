import json
from pathlib import Path
import sys
import unittest

if __package__:
    from ..apmw_projection.contract import (
        ApmwContractError,
        compute_manifest_sha256,
        parse_contract,
    )
else:
    CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(CHECKSMATE_ROOT))
    from apmw_projection.contract import (
        ApmwContractError,
        compute_manifest_sha256,
        parse_contract,
    )


EXPECTED_HASH = "f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15"
FIXTURE = Path(__file__).parent / "fixtures" / "projection-v2" / "baseline.json"


def rehash(document: dict) -> str:
    document["manifest_sha256"] = ""
    text = json.dumps(document, indent=2)
    document["manifest_sha256"] = compute_manifest_sha256(text)
    return json.dumps(document, indent=2)


class TestApmwContractV2(unittest.TestCase):
    def setUp(self):
        self.text = FIXTURE.read_text(encoding="utf-8")
        self.document = json.loads(self.text)

    def test_accepts_baseline_and_verifies_frozen_hash(self):
        contract = parse_contract(self.text)

        self.assertEqual((2, 0), (contract.version.major, contract.version.minor))
        self.assertEqual(EXPECTED_HASH, contract.manifest_sha256)
        self.assertEqual(EXPECTED_HASH, compute_manifest_sha256(self.text))
        self.assertEqual(
            ("8x8", "10x8", "10x10", "12x10", "12x12"),
            contract.stage_order,
        )
        self.assertEqual(
            [
                ("8x8", 15, 32, 39, 24),
                ("10x8", 19, 40, 49, 30),
                ("10x10", 39, 60, 69, 50),
                ("12x10", 47, 72, 83, 60),
                ("12x12", 71, 96, 107, 84),
            ],
            [
                (
                    stage.stage_id,
                    stage.non_pawn_capacity,
                    stage.gross_pawn_capacity,
                    stage.combined_non_primary_capacity,
                    stage.forwardness_capacity,
                )
                for stage in contract.stages
            ],
        )
        self.assertEqual(107, contract.effective_item_maxima["fundamental"]["Chessmen"])

    def test_freezes_placement_roles_upgrade_role_preservation_and_mode_semantics(self):
        contract = parse_contract(self.text)
        self.assertEqual(
            (
                "primary-royal",
                "additional-royal",
                "locked-castler",
                "jack-slot",
                "major-slot",
                "minor-slot",
                "pawn-slot",
            ),
            contract.source_roles,
        )
        transitions = {transition.action: transition for transition in contract.upgrade_dag.transitions}
        self.assertEqual("establish-minor-slot", transitions["pawn-to-minor"].source_role_rule)
        self.assertEqual("establish-major-slot", transitions["pawn-to-major"].source_role_rule)
        self.assertEqual(
            ("major-slot", "minor-slot"),
            transitions["major-to-queen"].allowed_source_roles,
        )
        self.assertEqual(
            ("jack-slot", "major-slot", "minor-slot"),
            transitions["queen-to-amazon"].allowed_source_roles,
        )
        self.assertEqual("preserve", transitions["better-pawn"].source_role_rule)
        stable_fundamental = next(
            mode for mode in contract.mode_combinations
            if mode.semantic_id == "stable-fundamental"
        )
        self.assertTrue(stable_fundamental.semantic_snapshot_deterministic)
        self.assertTrue(stable_fundamental.semantic_series_isolated)
        self.assertFalse(stable_fundamental.experiential_prefix_stable)
        self.assertFalse(stable_fundamental.planned_series_prefix_stable)
        stable_legacy = next(
            mode for mode in contract.mode_combinations
            if mode.semantic_id == "stable-legacy"
        )
        self.assertFalse(stable_legacy.experiential_prefix_stable)
        self.assertTrue(stable_legacy.planned_series_prefix_stable)
        self.assertIn(
            "fundamental.omission.{source-role}",
            contract.semantic_series_ids,
        )

    def test_freezes_geometry_unlocks_and_dynamic_pawn_capacity_formula(self):
        contract = parse_contract(self.text)
        self.assertEqual(
            (
                ("board-file-unlock", 8, 2, 12),
                ("board-rank-unlock", 8, 2, 12),
            ),
            tuple(
                (role.role_id, role.base, role.increment, role.maximum)
                for role in contract.geometry_unlocks.roles
            ),
        )
        self.assertEqual(
            "largest-componentwise-unlocked-valid-pair",
            contract.geometry_unlocks.selection_policy,
        )
        formula = contract.pawn_capacity_formula
        self.assertEqual("width-times-ranks-minus-four-v1", formula.gross_pawn_capacity_algorithm)
        self.assertEqual(8, formula.non_pawns_beyond_back(8, 15))
        self.assertEqual(24, formula.active_pawn_capacity(8, 32, 15))
        self.assertEqual(60, formula.non_pawns_beyond_back(12, 71))
        self.assertEqual(36, formula.active_pawn_capacity(12, 96, 71))

    def test_freezes_material_first_activation_and_castler_reclassification(self):
        contract = parse_contract(self.text)
        self.assertEqual(contract.source_roles, contract.overflow_policy.role_priority)
        self.assertEqual(
            (
                "final-expected-material-descending",
                "ap-granted-material-descending",
                "source-ordinal-ascending",
            ),
            contract.overflow_policy.within_role_activation_order,
        )
        self.assertEqual(
            "normalized-ap-granted-material-per-reserve-slot-exactly-once",
            contract.overflow_policy.missing_material_accounting,
        )
        self.assertTrue(contract.overflow_policy.aggregate_semantics_ignore_presentation)
        self.assertEqual("presentation-only", contract.overflow_policy.chaos_nonce_scope)
        self.assertEqual("locked-castler", contract.castler.source_role)
        self.assertTrue(contract.castler.reclassifies_existing_chessman)
        self.assertTrue(contract.castler.source_role_immutable)
        self.assertFalse(contract.castler.adds_chessman)
        self.assertTrue(contract.castler.requires_existing_chessman)
        self.assertTrue(contract.castler.occupies_board_slot)
        self.assertEqual(("major", "jack"), contract.castler.target_families)
        self.assertEqual("jack", contract.castler.upgrade_ceiling)
        self.assertEqual(500, contract.castler.normalized_material)
        self.assertEqual(500, contract.castler.normalized_cost)
        self.assertEqual(2, contract.castler.maximum)

    def test_mirrored_fixture_is_byte_identical_when_both_repositories_are_present(self):
        chessv_fixture = (
            Path(__file__).resolve().parents[4]
            / "chessv"
            / "APMW.Test"
            / "Fixtures"
            / "ProjectionV2"
            / "baseline.json"
        )
        if chessv_fixture.exists():
            self.assertEqual(FIXTURE.read_bytes(), chessv_fixture.read_bytes())

    def test_rejects_unknown_major_and_newer_minor_explicitly(self):
        self.document["version"]["major"] = 3
        with self.assertRaisesRegex(ApmwContractError, "unsupported contract major version 3"):
            parse_contract(json.dumps(self.document))

        self.document["version"]["major"] = 2
        self.document["version"]["minor"] = 1
        with self.assertRaisesRegex(ApmwContractError, "unsupported contract minor version 1"):
            parse_contract(json.dumps(self.document))

    def test_rejects_hash_mismatch(self):
        self.document["minimum_client_version"] = "0.4.1"
        with self.assertRaisesRegex(ApmwContractError, "manifest SHA-256 mismatch"):
            parse_contract(json.dumps(self.document))

    def test_rejects_malformed_geometry_duplicate_stage_and_bad_capacity(self):
        self.document["geometry"]["valid_pairs"][1]["stage_id"] = "10-by-8"
        with self.assertRaisesRegex(ApmwContractError, "stage_id must be canonical"):
            parse_contract(rehash(self.document))

        self.document = json.loads(self.text)
        self.document["geometry"]["valid_pairs"][1] = dict(
            self.document["geometry"]["valid_pairs"][0]
        )
        self.document["geometry"]["valid_pairs"][1]["stage_id"] = "8x8"
        with self.assertRaisesRegex(ApmwContractError, "duplicate geometries"):
            parse_contract(rehash(self.document))

        self.document = json.loads(self.text)
        self.document["geometry"]["valid_pairs"][4]["non_pawn_capacity"] = 70
        with self.assertRaisesRegex(ApmwContractError, "expanded-formation-v2"):
            parse_contract(rehash(self.document))

    def test_rejects_alternative_internally_consistent_geometry_path(self):
        alternative = [(8, 8), (8, 10), (10, 10), (10, 12), (12, 12)]
        self.document["geometry"]["stage_order"] = [
            f"{width}x{height}" for width, height in alternative
        ]
        for index, ((width, height), stage) in enumerate(
            zip(alternative, self.document["geometry"]["valid_pairs"])
        ):
            locations = 7 * width + 15 + index
            stage.update(
                {
                    "stage_id": f"{width}x{height}",
                    "files": width,
                    "ranks": height,
                    "deployment_depth": height - 3,
                    "combined_non_primary_capacity": width * (height - 3) - 1,
                    "gross_pawn_capacity": width * (height - 4),
                    "forwardness_capacity": width * (height - 5),
                    "non_pawn_capacity": width * (height - 6) - 1,
                    "cpu_pawn_count": width,
                    "cpu_non_king_count": width - 1,
                    "all_tactics_locations": locations,
                    "turns_locations": locations - 6,
                    "no_tactics_locations": locations - 10,
                }
            )
        with self.assertRaisesRegex(ApmwContractError, "frozen v2.0 value"):
            parse_contract(rehash(self.document))

    def test_rejects_malformed_upgrade_and_activation_schema(self):
        self.document["upgrade_dag"]["transitions"][7]["source_role_rule"] = "become-queen-slot"
        with self.assertRaisesRegex(ApmwContractError, "frozen v2.0 value"):
            parse_contract(rehash(self.document))

        self.document = json.loads(self.text)
        self.document["overflow_policy"]["within_role_activation_order"][0] = (
            "source-ordinal-descending"
        )
        with self.assertRaisesRegex(ApmwContractError, "frozen v2.0 value"):
            parse_contract(rehash(self.document))

        self.document = json.loads(self.text)
        self.document["castler"]["target_families"] = ["queen"]
        with self.assertRaisesRegex(ApmwContractError, "frozen v2.0 value"):
            parse_contract(rehash(self.document))

    def test_rejects_unknown_identifier_and_duplicate_json_property(self):
        self.document["algorithms"]["projection"] = "surprise-v9"
        with self.assertRaisesRegex(ApmwContractError, "frozen v2.0 value"):
            parse_contract(rehash(self.document))

        duplicate = self.text.replace(
            '"schema": "apmw_contract",',
            '"schema": "apmw_contract", "schema": "apmw_contract",',
            1,
        )
        with self.assertRaisesRegex(ApmwContractError, "duplicate JSON property"):
            parse_contract(duplicate)
