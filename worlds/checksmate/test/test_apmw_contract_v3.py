import json
from pathlib import Path
import sys
import unittest

if __package__:
    from ..apmw_projection.contract import (
        ApmwContractV3,
        compute_manifest_sha256,
        parse_contract,
    )
    from ..apmw_projection.models import projection_input_from_dict
    from ..apmw_projection.resource import (
        CONTRACT_RESOURCE,
        load_frozen_contract,
        mode_item_maxima,
    )
    from ..apmw_projection.semantic import ProjectionError, project_semantic_roster
else:
    CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(CHECKSMATE_ROOT))
    from apmw_projection.contract import (
        ApmwContractV3,
        compute_manifest_sha256,
        parse_contract,
    )
    from apmw_projection.models import projection_input_from_dict
    from apmw_projection.resource import (
        CONTRACT_RESOURCE,
        load_frozen_contract,
        mode_item_maxima,
    )
    from apmw_projection.semantic import ProjectionError, project_semantic_roster


V2_FIXTURE = Path(__file__).parent / "fixtures" / "projection-v2" / "baseline.json"


def v3_contract_text() -> str:
    document = json.loads(V2_FIXTURE.read_text(encoding="utf-8"))
    document["version"]["major"] = 3
    geometry = document["geometry"]
    geometry["base"]["files"] = 6
    geometry["file_ladder"] = [6, 8, 10, 12]
    geometry["stage_order"].insert(0, "6x8")
    geometry["valid_pairs"].insert(
        0,
        {
            "stage_id": "6x8",
            "files": 6,
            "ranks": 8,
            "deployment_depth": 5,
            "combined_non_primary_capacity": 29,
            "forwardness_capacity": 18,
            "non_pawn_capacity": 11,
            "cpu_pawn_count": 6,
            "cpu_non_king_count": 5,
            "all_tactics_locations": 57,
            "turns_locations": 51,
            "no_tactics_locations": 47,
            "gross_pawn_capacity": 24,
        },
    )
    geometry["unlocks"]["roles"][0]["base"] = 6
    document["manifest_sha256"] = ""
    text = json.dumps(document, indent=2)
    document["manifest_sha256"] = compute_manifest_sha256(text)
    return json.dumps(document, indent=2)


class TestApmwContractV3(unittest.TestCase):
    def test_frozen_runtime_uses_v3_while_v2_fixture_remains_decodable(self):
        frozen = load_frozen_contract()
        legacy = parse_contract(V2_FIXTURE.read_text(encoding="utf-8"))

        self.assertEqual("data/apmw_contract_v3.json", CONTRACT_RESOURCE)
        self.assertEqual((3, 0), (frozen.version.major, frozen.version.minor))
        self.assertEqual("6x8", frozen.stage_order[0])
        self.assertEqual("12x12", frozen.stage_order[-1])
        self.assertEqual((2, 0), (legacy.version.major, legacy.version.minor))

    def test_runtime_maxima_expose_three_file_and_two_rank_unlocks(self):
        maxima = mode_item_maxima("legacy")

        self.assertEqual(3, maxima["Board Files"])
        self.assertEqual(2, maxima["Board Ranks"])

    def test_accepts_6x8_prologue_without_changing_existing_stage_ids(self):
        contract = parse_contract(v3_contract_text())

        self.assertIsInstance(contract, ApmwContractV3)
        self.assertEqual((3, 0), (contract.version.major, contract.version.minor))
        self.assertEqual((6, 8), (contract.base_geometry.files, contract.base_geometry.ranks))
        self.assertEqual((6, 8, 10, 12), contract.file_ladder)
        self.assertEqual((8, 10, 12), contract.rank_ladder)
        self.assertEqual(
            ("6x8", "8x8", "10x8", "10x10", "12x10", "12x12"),
            contract.stage_order,
        )
        self.assertEqual(
            [
                ("6x8", 6, 8, 29, 24, 18, 11, 57, 51, 47),
                ("8x8", 8, 8, 39, 32, 24, 15, 71, 65, 61),
                ("10x8", 10, 8, 49, 40, 30, 19, 86, 80, 76),
                ("10x10", 10, 10, 69, 60, 50, 39, 87, 81, 77),
                ("12x10", 12, 10, 83, 72, 60, 47, 102, 96, 92),
                ("12x12", 12, 12, 107, 96, 84, 71, 103, 97, 93),
            ],
            [
                (
                    stage.stage_id,
                    stage.files,
                    stage.ranks,
                    stage.combined_non_primary_capacity,
                    stage.gross_pawn_capacity,
                    stage.forwardness_capacity,
                    stage.non_pawn_capacity,
                    stage.all_tactics_locations,
                    stage.turns_locations,
                    stage.no_tactics_locations,
                )
                for stage in contract.stages
            ],
        )
        self.assertEqual(
            (
                ("board-file-unlock", 6, 2, 12),
                ("board-rank-unlock", 8, 2, 12),
            ),
            tuple(
                (role.role_id, role.base, role.increment, role.maximum)
                for role in contract.geometry_unlocks.roles
            ),
        )

    def test_geometry_selection_applies_unlocks_to_supplied_start_baseline(self):
        contract = parse_contract(v3_contract_text())

        cases = (
            (None, {}, "6x8"),
            ({"files": 8, "ranks": 8}, {}, "8x8"),
            ({"files": 8, "ranks": 8}, {"board-file-unlock": 1}, "10x8"),
            ({"files": 10, "ranks": 8}, {"board-rank-unlock": 1}, "10x10"),
            ({"files": 10, "ranks": 10}, {"board-file-unlock": 1}, "12x10"),
            ({"files": 12, "ranks": 10}, {"board-rank-unlock": 1}, "12x12"),
        )
        for baseline, unlock_counts, expected_stage in cases:
            with self.subTest(baseline=baseline, unlock_counts=unlock_counts):
                input_data = {
                    "itemization": "legacy",
                    "ordering": "stable",
                    "unlock_counts": unlock_counts,
                }
                if baseline is not None:
                    input_data["geometry_baseline"] = baseline
                projection = project_semantic_roster(
                    contract,
                    projection_input_from_dict(input_data),
                )
                self.assertEqual(expected_stage, projection.geometry_stage)

        capped = project_semantic_roster(
            contract,
            projection_input_from_dict(
                {
                    "itemization": "legacy",
                    "ordering": "stable",
                    "geometry_baseline": {"files": 10, "ranks": 10},
                    "unlock_counts": {"board-file-unlock": 3},
                }
            ),
        )
        self.assertEqual("12x10", capped.geometry_stage)
        self.assertEqual(1, capped.effective_counts.unlocks[0].count)
        self.assertEqual(2, capped.effective_counts.unlock_overcounts[0].count)

        with self.assertRaisesRegex(
            ProjectionError,
            "geometry baseline 6x10 is not a valid contract stage",
        ):
            project_semantic_roster(
                contract,
                projection_input_from_dict(
                    {
                        "itemization": "legacy",
                        "ordering": "stable",
                        "geometry_baseline": {"files": 6, "ranks": 10},
                    }
                ),
            )


if __name__ == "__main__":
    unittest.main()
