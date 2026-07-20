r"""Projection compatibility snapshot provenance.

Source: ``..\chessv\APMW.Test\Fixtures\ProjectionV2``.
Regenerate from this repository root with:
``Copy-Item ..\chessv\APMW.Test\Fixtures\ProjectionV2\*.json worlds\checksmate\test\fixtures\projection-v2\``.
"""

import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import unittest

if __package__:
    from ..apmw_projection.contract import load_contract
    from ..apmw_projection.semantic import (
        CounterBasedSeedSeries,
        ProjectionError,
        SemanticSeeds,
        UpgradePreference,
        characterize_fundamental_owned_plan,
        expected_normalized_grant_material,
        projection_input_from_dict,
        projection_to_dict,
        project_exact_active_material,
        project_exact_active_non_primary_count,
        project_semantic_roster,
    )
else:
    CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(CHECKSMATE_ROOT))
    from apmw_projection.contract import load_contract
    from apmw_projection.semantic import (
        CounterBasedSeedSeries,
        ProjectionError,
        SemanticSeeds,
        UpgradePreference,
        characterize_fundamental_owned_plan,
        expected_normalized_grant_material,
        projection_input_from_dict,
        projection_to_dict,
        project_exact_active_material,
        project_exact_active_non_primary_count,
        project_semantic_roster,
    )


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "projection-v2"
CONTRACT_FIXTURE = FIXTURE_DIR / "baseline.json"
CASES_FIXTURE = FIXTURE_DIR / "cases.json"
EXPECTED_CONTRACT_HASH = "f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15"
EXPECTED_CASES_HASH = "8d644bee7d7565f45b572d1e93c8f6e544a1efdb8b1a8f198172c8f528e8e98c"
SNAPSHOT_SOURCE = Path("..") / "chessv" / "APMW.Test" / "Fixtures" / "ProjectionV2"
REGENERATION_COMMAND = (
    r"Copy-Item ..\chessv\APMW.Test\Fixtures\ProjectionV2\*.json "
    "worlds\\checksmate\\test\\fixtures\\projection-v2\\"
)


def _single_non_primary_summary(output):
    piece = next(
        piece
        for piece in output["owned_slots"]
        if piece["source_role"] != "primary-royal"
    )
    return piece["final_family"], piece["granted_material"], output["dormant_material"]


class TestSemanticProjectionV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = load_contract(CONTRACT_FIXTURE)
        cls.fixture_text = CASES_FIXTURE.read_text(encoding="utf-8")
        cls.document = json.loads(cls.fixture_text)
        cls.cases = {case["id"]: case for case in cls.document["cases"]}

    def test_fixture_hash_contract_hash_and_required_coverage_are_frozen(self):
        self.assertEqual(
            EXPECTED_CASES_HASH,
            hashlib.sha256(self.fixture_text.encode("utf-8")).hexdigest(),
        )
        self.assertEqual("apmw_projection_cases", self.document["schema"])
        self.assertEqual(2, self.document["version"])
        self.assertEqual(EXPECTED_CONTRACT_HASH, self.document["contract_sha256"])
        self.assertEqual(EXPECTED_CONTRACT_HASH, self.contract.manifest_sha256)

        covered = {
            tag
            for case in self.document["cases"]
            for tag in case["covers"]
        }
        self.assertTrue(
            {
                "every-geometry",
                "exact-capacity-overflow-per-role",
                "mixed-band-pawn-reduction",
                "lowest-material-omission",
                "source-ordinal-ties",
                "upgrade-role-preservation",
                "parentless-upgrades",
                "castlers-additional-royal-priority",
                "legacy-stable-chaos-equality",
                "fundamental-zero-full-overflow",
                "known-chessmen-dilution",
                "normalization",
                "missing-material-conservation",
                "invalid-unlock-combination",
                "same-family-actions",
                "castler-to-jack-ceiling",
                "role-local-ordinals",
                "expanded-geometry-forwardness",
                "reserve-promotion-families",
                "complete-legacy-actions",
                "legacy-amazon-contract-boundary",
                "promotion-entitlement-history",
                "same-file-forwardness-blockers",
                "csharp-coordinate-characterization",
                "fundamental-pawn-entitlement",
                "pawn-creation-action-compatibility",
            }.issubset(covered)
        )

    def test_compatibility_snapshot_source_and_regeneration_command_are_frozen(self):
        self.assertEqual(
            r"..\chessv\APMW.Test\Fixtures\ProjectionV2",
            str(SNAPSHOT_SOURCE),
        )
        self.assertEqual(
            r"Copy-Item ..\chessv\APMW.Test\Fixtures\ProjectionV2\*.json "
            "worlds\\checksmate\\test\\fixtures\\projection-v2\\",
            REGENERATION_COMMAND,
        )
        source = (
            Path(__file__).resolve().parents[4]
            / "chessv"
            / "APMW.Test"
            / "Fixtures"
            / "ProjectionV2"
        )
        if source.is_dir():
            for filename in ("baseline.json", "cases.json"):
                with self.subTest(filename=filename):
                    self.assertEqual(
                        json.loads(
                            (FIXTURE_DIR / filename).read_text(encoding="utf-8")
                        ),
                        json.loads(
                            (source / filename).read_text(encoding="utf-8")
                        ),
                    )

    def test_seed_root_legacy_and_fundamental_projection_vectors_are_frozen(self):
        seeds = {
            "pocket_seed": "101",
            "pawn_seed": "202",
            "minor_seed": "303",
            "major_seed": "404",
            "queen_seed": "505",
        }
        self.assertEqual("101|202|303|404|505", SemanticSeeds(**seeds).stable_root)

        legacy = projection_to_dict(
            project_semantic_roster(
                self.contract,
                projection_input_from_dict(
                    {
                        "itemization": "legacy",
                        "ordering": "stable",
                        "seeds": seeds,
                        "item_counts": {
                            "Progressive Major Piece": 1,
                            "Progressive Jack": 1,
                        },
                        "upgrade_preferences": [
                            {"action": "major-to-jack", "priority": 10}
                        ],
                    }
                ),
            )
        )
        self.assertEqual(
            [
                ("primary-royal:000000", 4, 0),
                ("major-slot:000000", 6, 0),
            ],
            [
                (entry["slot_id"], entry["file"], entry["relative_rank"])
                for entry in legacy["active_placements"]
            ],
        )
        self.assertEqual(
            [("active:major-slot:000000", "major-slot:000000", 700)],
            [
                (entry["entry_id"], entry["slot_id"], entry["amount"])
                for entry in legacy["active_material_ledger"]
            ],
        )

        fundamental = projection_to_dict(
            project_semantic_roster(
                self.contract,
                projection_input_from_dict(
                    {
                        "itemization": "fundamental",
                        "ordering": "stable",
                        "seeds": seeds,
                        "item_counts": {"Chessmen": 5, "Material": 12},
                        "upgrade_preferences": [
                            {"action": "pawn-to-minor", "priority": 7},
                            {"action": "minor-to-major", "priority": 6},
                            {"action": "major-to-jack", "priority": 5},
                            {"action": "minor-to-jack", "priority": 4},
                            {"action": "major-to-queen", "priority": 3},
                            {"action": "jack-to-queen", "priority": 2},
                            {"action": "queen-to-amazon", "priority": 1},
                        ],
                    }
                ),
            )
        )
        self.assertEqual(
            [
                ("chessman:000003", "queen", 900),
                ("chessman:000004", "amazon", 1300),
                ("chessman:000001", "queen", 900),
                ("chessman:000002", "amazon", 1300),
                ("chessman:000000", "queen", 900),
            ],
            [
                (entry["slot_id"], entry["final_family"], entry["granted_material"])
                for entry in fundamental["owned_slots"]
                if entry["source_role"] != "primary-royal"
            ],
        )
        self.assertEqual(
            [
                ("chessman:000003", 5, 0),
                ("chessman:000004", 3, 0),
                ("chessman:000001", 7, 0),
                ("chessman:000002", 0, 0),
                ("chessman:000000", 1, 0),
            ],
            [
                (entry["slot_id"], entry["file"], entry["relative_rank"])
                for entry in fundamental["active_placements"]
                if entry["slot_id"] != "primary-royal:000000"
            ],
        )
        self.assertEqual(5300, fundamental["total_accounted_material"])

    def test_all_canonical_cases_match_byte_model(self):
        for case in self.document["cases"]:
            with self.subTest(case=case["id"]):
                projection_input = projection_input_from_dict(case["input"])
                if "error" in case:
                    with self.assertRaisesRegex(
                        ProjectionError,
                        "^" + re.escape(case["error"]) + "$",
                    ):
                        project_semantic_roster(self.contract, projection_input)
                else:
                    actual = projection_to_dict(
                        project_semantic_roster(self.contract, projection_input)
                    )
                    self.assertEqual(case["output"], actual)

    def test_fast_exact_material_projection_matches_full_projection(self):
        for case in self.document["cases"]:
            if "output" not in case:
                continue
            with self.subTest(case=case["id"]):
                projection_input = projection_input_from_dict(case["input"])
                self.assertEqual(
                    project_semantic_roster(
                        self.contract, projection_input
                    ).exact_active_material,
                    project_exact_active_material(
                        self.contract, projection_input
                    ),
                )
                output = project_semantic_roster(
                    self.contract, projection_input
                )
                self.assertEqual(
                    sum(
                        piece.source_role != "primary-royal"
                        for piece in output.active_slots
                    ),
                    project_exact_active_non_primary_count(
                        self.contract, projection_input
                    ),
                )

    def test_projection_ledgers_and_capacity_invariants(self):
        for case in self.document["cases"]:
            if "output" not in case:
                continue
            with self.subTest(case=case["id"]):
                output = case["output"]
                active_ids = {piece["slot_id"] for piece in output["active_slots"]}
                reserve_ids = {piece["slot_id"] for piece in output["reserve_slots"]}
                owned_ids = {piece["slot_id"] for piece in output["owned_slots"]}
                self.assertFalse(active_ids & reserve_ids)
                self.assertEqual(owned_ids, active_ids | reserve_ids)
                self.assertEqual(
                    output["owned_expected_material"],
                    sum(
                        piece["final_expected_material"]
                        for piece in output["owned_slots"]
                        if piece["source_role"] != "primary-royal"
                    ),
                )
                self.assertEqual(
                    output["available_promotion_families"],
                    [
                        family
                        for family in (
                            "royal", "pawn", "minor", "major", "jack", "queen", "amazon"
                        )
                        if any(
                            family in piece["promotion_entitlement_families"]
                            for piece in output["active_slots"]
                        )
                    ],
                )
                self.assertEqual(
                    output["reserve_promotion_families"],
                    [
                        family
                        for family in (
                            "royal", "pawn", "minor", "major", "jack", "queen", "amazon"
                        )
                        if any(
                            family in piece["promotion_entitlement_families"]
                            for piece in output["reserve_slots"]
                        )
                    ],
                )
                placements = output["active_placements"]
                self.assertEqual(len(output["active_slots"]), len(placements))
                self.assertEqual(
                    len(placements),
                    len(
                        {
                            (placement["file"], placement["relative_rank"])
                            for placement in placements
                        }
                    ),
                )

                active_ledger = sum(
                    entry["amount"] for entry in output["active_material_ledger"]
                )
                reserve_ledger = sum(
                    entry["amount"] for entry in output["reserve_material_ledger"]
                )
                dormant_ledger = sum(
                    entry["amount"] for entry in output["dormant_material_ledger"]
                )
                unallocated_ledger = sum(
                    entry["amount"] for entry in output["unallocated_material_ledger"]
                )
                self.assertEqual(output["active_granted_material"], active_ledger)
                self.assertEqual(output["missing_material"], reserve_ledger)
                self.assertEqual(output["dormant_material"], dormant_ledger)
                self.assertEqual(output["unallocated_material"], unallocated_ledger)
                self.assertEqual(
                    output["total_accounted_material"],
                    active_ledger
                    + reserve_ledger
                    + dormant_ledger
                    + unallocated_ledger,
                )
                projection_input = projection_input_from_dict(case["input"])
                expected_grant = expected_normalized_grant_material(
                    self.contract, projection_input
                )
                self.assertEqual(
                    expected_grant,
                    output["normalized_grant_material"],
                )
                self.assertEqual(
                    expected_grant,
                    output["total_accounted_material"],
                )

                region = output["region_usage"]
                active_non_primary = sum(
                    1
                    for piece in output["active_slots"]
                    if piece["source_role"]
                    in {
                        "additional-royal",
                        "locked-castler",
                        "jack-slot",
                        "major-slot",
                        "minor-slot",
                    }
                )
                active_pawns = sum(
                    1
                    for piece in output["active_slots"]
                    if piece["source_role"] == "pawn-slot"
                )
                self.assertLessEqual(active_non_primary, region["non_pawn_capacity"])
                self.assertLessEqual(active_pawns, region["active_pawn_capacity"])

    def test_geometry_selection_uses_largest_componentwise_valid_pair(self):
        stages = [
            self.cases[f"geometry-{stage}"]["output"]["geometry_stage"]
            for stage in ("8x8", "10x8", "10x10", "12x10", "12x12")
        ]
        self.assertEqual(
            ["8x8", "10x8", "10x10", "12x10", "12x12"],
            stages,
        )

        rank_only = projection_input_from_dict(
            {
                "itemization": "legacy",
                "ordering": "stable",
                "seed": "rank-only",
                "unlock_counts": {"board-rank-unlock": 2},
            }
        )
        self.assertEqual(
            "8x8",
            project_semantic_roster(self.contract, rank_only).geometry_stage,
        )

    def test_material_first_omission_role_priority_and_ties(self):
        overflow = self.cases["role-overflow-material-first"]["output"]
        active_by_role = {
            entry["source_role"]: entry["count"]
            for entry in overflow["active_counts"]
        }
        self.assertEqual(2, active_by_role["additional-royal"])
        self.assertEqual(9, active_by_role["jack-slot"])
        self.assertEqual(4, active_by_role["major-slot"])
        self.assertNotIn("minor-slot", active_by_role)
        self.assertEqual(24, overflow["region_usage"]["active_pawn_capacity"])
        self.assertTrue(
            all(
                piece["final_family"] == "queen"
                for piece in overflow["active_slots"]
                if piece["source_role"] == "major-slot"
            )
        )

        ties = self.cases["omission-full-tie-source-ordinal"]["output"]
        active_major_ordinals = [
            piece["source_ordinal"]
            for piece in ties["active_slots"]
            if piece["source_role"] == "major-slot"
        ]
        self.assertEqual([0, 1, 2, 3], active_major_ordinals)
        reserve_major_ordinals = [
            piece["source_ordinal"]
            for piece in ties["reserve_slots"]
            if piece["source_role"] == "major-slot"
        ]
        self.assertEqual([10, 9, 8, 7, 6, 5, 4], reserve_major_ordinals)
        self.assertEqual(
            [f"reserve:major-slot:{ordinal:06d}" for ordinal in reserve_major_ordinals],
            [
                entry["entry_id"]
                for entry in ties["reserve_material_ledger"]
                if entry["slot_id"].startswith("major-slot:")
            ],
        )

    def test_upgrade_roles_parentless_upgrades_and_castlers(self):
        role_case = self.cases["upgrade-role-preservation"]["output"]
        upgraded = next(
            piece
            for piece in role_case["owned_slots"]
            if piece["slot_id"] == "minor-slot:000000"
        )
        self.assertEqual("minor-slot", upgraded["source_role"])
        self.assertEqual("major", upgraded["final_family"])
        self.assertEqual(["minor-to-major"], upgraded["upgrade_path"])
        self.assertEqual(
            ["minor", "major"],
            upgraded["promotion_entitlement_families"],
        )

        parentless = self.cases["parentless-upgrades-dormant"]["output"]
        self.assertEqual(1245, parentless["dormant_material"])
        self.assertEqual(0, parentless["missing_material"])

        castle = self.cases["castlers-additional-royal-priority"]["output"]
        self.assertEqual(2, len(castle["active_castlers"]))
        self.assertTrue(
            set(castle["active_castlers"]).issubset(
                castle["castling_eligible_slots"]
            )
        )
        self.assertEqual(7, castle["region_usage"]["back_non_primary"])
        self.assertEqual(
            2,
            sum(
                entry["count"]
                for entry in castle["active_counts"]
                if entry["source_role"] == "additional-royal"
            ),
        )

        ceiling = self.cases["castler-to-jack-ceiling"]["output"]
        locked = [
            piece
            for piece in ceiling["owned_slots"]
            if piece["source_role"] == "locked-castler"
        ]
        self.assertEqual([0, 1], [piece["source_ordinal"] for piece in locked])
        self.assertTrue(
            all(
                piece["final_family"] == "jack"
                and piece["upgrade_path"] == ["castler", "major-to-jack"]
                and piece["granted_material"] == 800
                and piece["final_expected_material"] == 700
                for piece in locked
            )
        )
        self.assertFalse(
            any(
                family in {"queen", "amazon"}
                for family in (piece["final_family"] for piece in locked)
            )
        )

    def test_legacy_stable_and_chaos_have_equal_aggregate_semantics(self):
        stable = copy.deepcopy(self.cases["legacy-stable-equality"]["output"])
        chaos = copy.deepcopy(self.cases["legacy-chaos-equality"]["output"])
        stable.pop("ordering")
        chaos.pop("ordering")
        self.assertEqual(stable, chaos)

    def test_fundamental_shared_wave_dilution_and_normalization(self):
        small = self.cases["fundamental-dilution-small"]["output"]
        large = self.cases["fundamental-dilution-large"]["output"]

        def families(output):
            return {
                entry["final_family"]: entry["count"]
                for entry in output["active_counts"]
                if entry["source_role"] != "primary-royal"
            }

        self.assertEqual({"queen": 3, "amazon": 2}, families(small))
        self.assertEqual({"major": 3, "jack": 6}, families(large))

        normalized = self.cases["fundamental-overflow-normalized"]["output"]
        effective = {
            entry["name"]: entry["count"]
            for entry in normalized["effective_counts"]["items"]
        }
        self.assertEqual(107, effective["Chessmen"])
        self.assertEqual(321, effective["Material"])
        self.assertEqual(2, effective["Castler"])
        self.assertEqual("12x12", normalized["geometry_stage"])

    def test_same_family_pawn_actions_terminate_without_wave_repetition(self):
        for case_id in (
            "legacy-better-pawn-finite",
            "legacy-pool-pawn-finite",
            "fundamental-better-pawn-finite",
            "fundamental-pool-pawn-finite",
        ):
            with self.subTest(case=case_id):
                output = self.cases[case_id]["output"]
                pawns = [
                    piece
                    for piece in output["owned_slots"]
                    if piece["source_role"] == "pawn-slot"
                ]
                self.assertEqual(4, len(pawns))
                self.assertTrue(
                    all(
                        piece["final_family"] == "pawn"
                        and piece["upgrade_path"] == []
                        for piece in pawns
                    )
                )
                expected = 400 if case_id.startswith("legacy-") else 1200
                self.assertEqual(expected, output["normalized_grant_material"])
                self.assertEqual(expected, output["total_accounted_material"])

    def test_reserve_promotion_families_are_reported_but_not_available(self):
        output = self.cases["reserve-promotion-families"]["output"]
        self.assertEqual(
            ["royal", "major", "jack"],
            output["available_promotion_families"],
        )
        self.assertEqual(
            ["minor", "major"],
            output["reserve_promotion_families"],
        )
        self.assertNotIn("minor", output["available_promotion_families"])

        history = self.cases["reserve-upgrade-entitlement-history"]["output"]
        reserve = history["reserve_slots"]
        self.assertEqual(1, len(reserve))
        self.assertEqual(
            ("minor-slot", "major", ["minor", "major"]),
            (
                reserve[0]["source_role"],
                reserve[0]["final_family"],
                reserve[0]["promotion_entitlement_families"],
            ),
        )
        self.assertEqual(
            ["minor", "major"],
            history["reserve_promotion_families"],
        )
        self.assertNotIn("minor", history["available_promotion_families"])

    def test_complete_accepted_legacy_action_and_parentless_matrix(self):
        expectations = {
            "upgrade-role-preservation": ("minor-slot", "major", ["minor-to-major"], 485),
            "legacy-action-major-to-jack": ("major-slot", "jack", ["major-to-jack"], 700),
            "legacy-action-minor-to-jack": ("minor-slot", "jack", ["minor-to-jack"], 700),
            "legacy-action-major-to-queen": ("major-slot", "queen", ["major-to-queen"], 900),
            "legacy-action-jack-to-queen": ("jack-slot", "queen", ["jack-to-queen"], 900),
        }
        for case_id, (role, family, path, material) in expectations.items():
            with self.subTest(case=case_id):
                output = self.cases[case_id]["output"]
                piece = next(
                    piece
                    for piece in output["owned_slots"]
                    if piece["source_role"] != "primary-royal"
                )
                self.assertEqual((role, family, path, material), (
                    piece["source_role"],
                    piece["final_family"],
                    piece["upgrade_path"],
                    piece["granted_material"],
                ))

        amazon_boundary = self.cases[
            "legacy-queen-to-amazon-contract-boundary"
        ]["output"]
        self.assertEqual(
            ["major", "queen"],
            amazon_boundary["available_promotion_families"],
        )
        self.assertFalse(
            any(
                piece["final_family"] == "amazon"
                for piece in amazon_boundary["owned_slots"]
            ),
            "accepted Legacy maxima contain no Amazon entitlement, so the action must not invent one",
        )
        self.assertEqual(
            1245,
            self.cases["parentless-upgrades-dormant"]["output"]["dormant_material"],
        )
        self.assertEqual(
            ("major", 485, 0),
            _single_non_primary_summary(
                self.cases["legacy-parentless-major-remains-direct"]["output"]
            ),
        )
        self.assertEqual(
            ("jack", 700, 0),
            _single_non_primary_summary(
                self.cases["legacy-parentless-jack-remains-direct"]["output"]
            ),
        )

    def test_counter_based_seed_series_vectors_match_corrected_csharp_wire(self):
        for vector in self.document["series_vectors"]:
            with self.subTest(series=vector["series_id"]):
                series = CounterBasedSeedSeries(
                    vector["root"], vector["series_id"]
                )
                counter = vector["counter"]
                self.assertEqual(int(vector["value"]), series.value(counter))
                self.assertEqual(
                    vector["index"],
                    series.index(counter, vector["count"]),
                )
                self.assertEqual(
                    vector["unit"],
                    format(series.unit(counter), ".17g"),
                )

    def test_fundamental_plan_vectors_match_csharp_dilution_characterization(self):
        for vector in self.document["fundamental_plan_vectors"]:
            with self.subTest(vector=vector["id"]):
                plan = characterize_fundamental_owned_plan(
                    self.contract,
                    vector["chessmen"],
                    vector["material_budget"],
                    vector["castlers"],
                    SemanticSeeds(**vector["seeds"]),
                    tuple(
                        UpgradePreference(
                            entry["action"],
                            entry["priority"],
                            entry.get("proportion_numerator", 1),
                            entry.get("proportion_denominator", 1),
                        )
                        for entry in vector["upgrade_preferences"]
                    ),
                )
                self.assertEqual(
                    vector["tier_counts"],
                    dict(plan.tier_counts),
                )
                self.assertEqual(
                    vector["spare_material"],
                    plan.spare_material,
                )

    def test_gateway_roles_receive_independent_role_local_ordinals(self):
        output = self.cases["gateway-role-local-ordinals"]["output"]
        for role in ("minor-slot", "major-slot"):
            ordinals = [
                piece["source_ordinal"]
                for piece in output["owned_slots"]
                if piece["source_role"] == role
            ]
            self.assertEqual(list(range(len(ordinals))), ordinals)
        self.assertTrue(
            all(
                piece["slot_id"].startswith("chessman:")
                for piece in output["owned_slots"]
                if piece["source_role"] in {"minor-slot", "major-slot"}
            )
        )

    def test_forwardness_is_applied_after_projection(self):
        active = self.cases["forwardness-active-only"]["output"]
        blocked = self.cases["pawn-overflow-forwardness-blocked"]["output"]
        self.assertEqual((13, 0), (
            active["applied_forwardness"],
            active["unspent_forwardness"],
        ))
        self.assertEqual((0, 13), (
            blocked["applied_forwardness"],
            blocked["unspent_forwardness"],
        ))
        expanded = self.cases["expanded-forwardness-12x12"]["output"]
        self.assertEqual("12x12", expanded["geometry_stage"])
        self.assertEqual((13, 0), (
            expanded["applied_forwardness"],
            expanded["unspent_forwardness"],
        ))

        blockers = self.cases["forwardness-same-file-blockers-csharp"]["output"]
        self.assertEqual((9, 4), (
            blockers["applied_forwardness"],
            blockers["unspent_forwardness"],
        ))
        pawn_coordinates = [
            (
                placement["slot_id"],
                placement["file"],
                placement["relative_rank"],
            )
            for placement in blockers["active_placements"]
            if placement["slot_id"].startswith("pawn-slot:")
        ]
        self.assertEqual(
            [
                ("pawn-slot:000000", 0, 2),
                ("pawn-slot:000001", 3, 1),
                ("pawn-slot:000002", 6, 1),
                ("pawn-slot:000003", 5, 1),
                ("pawn-slot:000004", 3, 2),
                ("pawn-slot:000005", 2, 3),
                ("pawn-slot:000006", 0, 3),
                ("pawn-slot:000007", 4, 3),
                ("pawn-slot:000008", 6, 2),
                ("pawn-slot:000009", 7, 3),
                ("pawn-slot:000010", 1, 2),
                ("pawn-slot:000011", 5, 2),
                ("pawn-slot:000012", 0, 4),
                ("pawn-slot:000013", 7, 4),
                ("pawn-slot:000014", 2, 4),
                ("pawn-slot:000015", 6, 3),
                ("pawn-slot:000016", 1, 3),
                ("pawn-slot:000017", 3, 3),
                ("pawn-slot:000018", 4, 4),
                ("pawn-slot:000019", 5, 3),
                ("pawn-slot:000020", 3, 4),
                ("pawn-slot:000021", 1, 4),
                ("pawn-slot:000022", 6, 4),
                ("pawn-slot:000023", 5, 4),
            ],
            pawn_coordinates,
        )

    def test_primary_king_base_is_zero_and_promotions_are_normalized_grants(self):
        zero = self.cases["fundamental-zero"]["output"]
        primary = next(
            piece
            for piece in zero["owned_slots"]
            if piece["source_role"] == "primary-royal"
        )
        self.assertEqual((0, 0), (
            primary["granted_material"],
            primary["final_expected_material"],
        ))

        normalized = self.cases["legacy-normalization-all-ledgers"]["output"]
        promoted = next(
            piece
            for piece in normalized["owned_slots"]
            if piece["source_role"] == "primary-royal"
        )
        self.assertEqual(850, promoted["granted_material"])
        self.assertEqual(["king-promotion", "king-promotion"], promoted["upgrade_path"])

    def test_surviving_fundamental_pawns_gain_active_and_reserve_entitlements(self):
        zero_upgrade = self.cases["fundamental-no-upgrades-unallocated"]["output"]
        pawns = [
            piece
            for piece in zero_upgrade["owned_slots"]
            if piece["final_family"] == "pawn"
        ]
        self.assertTrue(pawns)
        self.assertTrue(
            all(
                piece["promotion_entitlement_families"] == ["pawn"]
                for piece in pawns
            )
        )
        self.assertEqual(["pawn"], zero_upgrade["available_promotion_families"])

        overflow = self.cases["fundamental-pawn-reserve-overflow"]["output"]
        reserve_pawns = [
            piece
            for piece in overflow["reserve_slots"]
            if piece["final_family"] == "pawn"
        ]
        self.assertEqual(75, len(reserve_pawns))
        self.assertTrue(
            all(
                piece["promotion_entitlement_families"] == ["pawn"]
                for piece in reserve_pawns
            )
        )
        self.assertEqual(["pawn"], overflow["reserve_promotion_families"])

    def test_creation_actions_are_accepted_but_do_not_enter_transition_waves(self):
        creation_actions = {"new-pawn", "more-pawn"}
        for case_id in (
            "legacy-configure-creation-actions",
            "fundamental-configure-creation-actions",
        ):
            with self.subTest(case=case_id):
                case = self.cases[case_id]
                configured = case["output"]
                control_input = copy.deepcopy(case["input"])
                control_input["upgrade_preferences"] = [
                    preference
                    for preference in control_input["upgrade_preferences"]
                    if preference["action"] not in creation_actions
                ]
                control = projection_to_dict(
                    project_semantic_roster(
                        self.contract,
                        projection_input_from_dict(control_input),
                    )
                )
                self.assertEqual(control, configured)
