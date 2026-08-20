import ast
import copy
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest

if __package__:
    from ..apmw_projection import (
        CONTRACT_MISMATCH,
        FROZEN_CONTRACT_HASH,
        INVALID_JSON,
        INVALID_PROTOCOL,
        INVALID_REQUEST,
        PROJECTION_ERROR,
        PROTOCOL_VERSION,
        RUNTIME_SEMANTIC_VERSION,
        UNKNOWN_GEOMETRY,
        ProtocolError,
        handle_batch_request,
        handle_json_request,
    )
    from ..apmw_projection.protocol import canonical_json, run_cli
    from ..apmw_projection.resource import load_frozen_contract
else:
    CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(CHECKSMATE_ROOT))
    from apmw_projection import (
        CONTRACT_MISMATCH,
        FROZEN_CONTRACT_HASH,
        INVALID_JSON,
        INVALID_PROTOCOL,
        INVALID_REQUEST,
        PROJECTION_ERROR,
        PROTOCOL_VERSION,
        RUNTIME_SEMANTIC_VERSION,
        UNKNOWN_GEOMETRY,
        ProtocolError,
        handle_batch_request,
        handle_json_request,
    )
    from apmw_projection.protocol import canonical_json, run_cli
    from apmw_projection.resource import load_frozen_contract


FIXTURE_DIR = Path(__file__).parent / "fixtures" / "projection-v2"
CASES_FIXTURE = FIXTURE_DIR / "cases.json"
REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PROJECTOR_ENTRY = REPOSITORY_ROOT / "worlds" / "checksmate" / "tools" / "apmw_projector.py"
EXPECTED_CONTRACT_HASH = "f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15"
EXPECTED_PROTOCOL_VERSION = 1
EXPECTED_RUNTIME_SEMANTIC_VERSION = "0.1.0"


class TestApmwProjectionProtocol(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cases = json.loads(CASES_FIXTURE.read_text(encoding="utf-8"))["cases"]
        cls.geometry_cases = {
            case["id"].removeprefix("geometry-"): case
            for case in cases
            if case["id"].startswith("geometry-")
        }
        base_input = cls.geometry_cases["8x8"]["input"]
        cls.request = {
            "protocol_version": PROTOCOL_VERSION,
            "request_id": "projection-test",
            "contract_hash": load_frozen_contract().manifest_sha256,
            "input": {
                field: copy.deepcopy(base_input[field])
                for field in ("itemization", "ordering", "seeds", "item_counts")
            },
            "geometries": ["8x8", "10x8", "10x10", "12x10", "12x12"],
        }

    def test_all_geometries_use_frozen_contract_and_fixture_projection(self):
        response = handle_batch_request(self.request)

        self.assertEqual(FROZEN_CONTRACT_HASH, self.request["contract_hash"])
        self.assertEqual(PROTOCOL_VERSION, response["protocol_version"])
        self.assertEqual("projection-test", response["request_id"])
        self.assertEqual(RUNTIME_SEMANTIC_VERSION, response["runtime_semantic_version"])
        self.assertEqual(
            self.request["geometries"],
            [result["geometry_stage"] for result in response["results"]],
        )
        for result in response["results"]:
            self.assertEqual(
                self.geometry_cases[result["geometry_stage"]]["output"],
                result["projection"],
            )

    def test_canonical_output_and_result_order_are_stable(self):
        request = copy.deepcopy(self.request)
        request["geometries"] = ["12x12", "8x8", "10x10"]

        first = handle_batch_request(request)
        self.assertEqual(canonical_json(first), canonical_json(handle_batch_request(request)))
        self.assertEqual(
            request["geometries"],
            [result["geometry_stage"] for result in first["results"]],
        )

    def test_request_and_response_wire_serialization_is_frozen(self):
        request = copy.deepcopy(self.request)
        request["request_id"] = "characterization"
        request["geometries"] = ["8x8"]
        expected_request = (
            '{"contract_hash":"f1456e916285bf79dd4be6f4c8c6e5798ed7bb1eebd2f6e1f81075f39e8ffc15",'
            '"geometries":["8x8"],"input":{"item_counts":{"Progressive Pawn":8},'
            '"itemization":"legacy","ordering":"stable","seeds":{"major_seed":"404",'
            '"minor_seed":"303","pawn_seed":"202","pocket_seed":"101","queen_seed":"505"}},'
            '"protocol_version":1,"request_id":"characterization"}'
        )

        self.assertEqual(expected_request, canonical_json(request))
        response_text = canonical_json(handle_json_request(expected_request))
        self.assertEqual(
            "9e207c4907cf93c1a4f44ba4d22605107664ffa0aeb5447c3b5c095ec8bbc728",
            hashlib.sha256(response_text.encode("ascii")).hexdigest(),
        )
        response = json.loads(response_text)
        self.assertEqual(
            {
                "contract_hash": EXPECTED_CONTRACT_HASH,
                "protocol_version": EXPECTED_PROTOCOL_VERSION,
                "request_id": "characterization",
                "runtime_semantic_version": EXPECTED_RUNTIME_SEMANTIC_VERSION,
            },
            {key: response[key] for key in response if key != "results"},
        )

    def test_structured_failures(self):
        failures = (
            (
                INVALID_JSON,
                "request is not valid JSON",
                lambda: handle_json_request("{"),
            ),
            (
                INVALID_PROTOCOL,
                "unsupported protocol version",
                lambda: handle_batch_request(
                    {**self.request, "protocol_version": PROTOCOL_VERSION + 1}
                ),
            ),
            (
                CONTRACT_MISMATCH,
                "contract hash does not match frozen v2 contract",
                lambda: handle_batch_request(
                    {**self.request, "contract_hash": "not-the-frozen-contract"}
                ),
            ),
            (
                INVALID_REQUEST,
                "geometries must not contain duplicates",
                lambda: handle_batch_request(
                    {**self.request, "geometries": ["8x8", "8x8"]}
                ),
            ),
            (
                UNKNOWN_GEOMETRY,
                "geometry is not defined by frozen v2 contract",
                lambda: handle_batch_request(
                    {**self.request, "geometries": ["9x9"]}
                ),
            ),
            (
                PROJECTION_ERROR,
                "item count for Progressive Pawn must not be negative",
                lambda: handle_batch_request(
                    {
                        **self.request,
                        "input": {
                            **self.request["input"],
                            "item_counts": {"Progressive Pawn": -1},
                        },
                    }
                ),
            ),
        )
        for code, message, operation in failures:
            with self.subTest(code=code):
                with self.assertRaises(ProtocolError) as raised:
                    operation()
                self.assertEqual(code, raised.exception.code)
                self.assertEqual(
                    {"error": {"code": code, "message": message}},
                    raised.exception.to_dict(),
                )
                self.assertEqual(
                    canonical_json({"error": {"code": code, "message": message}}),
                    canonical_json(raised.exception.to_dict()),
                )

    def test_projection_errors_keep_actionable_details_without_tracebacks(self):
        request = copy.deepcopy(self.request)
        request["input"]["item_counts"] = {"Progressive Pawn": -1}

        with self.assertRaises(ProtocolError) as raised:
            handle_batch_request(request)

        self.assertEqual(PROJECTION_ERROR, raised.exception.code)
        self.assertIn("must not be negative", raised.exception.message)
        self.assertNotIn("Traceback", raised.exception.message)

    def test_standalone_entrypoint_matches_direct_api(self):
        expected = handle_batch_request(self.request)
        completed = subprocess.run(
            [sys.executable, str(PROJECTOR_ENTRY)],
            cwd=REPOSITORY_ROOT,
            input=canonical_json(self.request),
            capture_output=True,
            encoding="utf-8",
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual(canonical_json(expected), completed.stdout.strip())
        self.assertEqual("", completed.stderr)

    def test_standalone_entrypoint_imports_no_archipelago_runtime_modules(self):
        request = canonical_json(self.request)
        probe = f"""
import io
import json
import runpy
import sys

sys.stdin = io.StringIO({request!r})
sys.stdout = io.StringIO()
try:
    runpy.run_path({str(PROJECTOR_ENTRY)!r}, run_name="__main__")
except SystemExit as error:
    exit_code = error.code
else:
    exit_code = None
forbidden = [
    name
    for name in sys.modules
    if name == "worlds"
    or name.startswith("worlds.")
    or name == "BaseClasses"
    or name == "Options"
]
sys.__stdout__.write(json.dumps({{"exit_code": exit_code, "forbidden": forbidden}}))
"""
        completed = subprocess.run(
            [sys.executable, "-c", probe],
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            encoding="utf-8",
            check=False,
        )

        self.assertEqual(0, completed.returncode, completed.stderr)
        self.assertEqual({"exit_code": 0, "forbidden": []}, json.loads(completed.stdout))

    def test_cli_writes_structured_errors_and_diagnostics(self):
        stdout = io.StringIO()
        stderr = io.StringIO()

        exit_code = run_cli(io.StringIO("{"), stdout, stderr)

        self.assertEqual(1, exit_code)
        self.assertEqual(
            {"error": {"code": INVALID_JSON, "message": "request is not valid JSON"}},
            json.loads(stdout.getvalue()),
        )
        self.assertIn(INVALID_JSON, stderr.getvalue())

    def test_canonical_package_has_no_archipelago_runtime_imports(self):
        package_dir = Path(__file__).parents[1] / "apmw_projection"
        forbidden = {"BaseClasses", "Options", "worlds", "worlds.AutoWorld"}
        imports = set()
        for path in package_dir.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="ascii"))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.update(alias.name for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and not node.level:
                    imports.add(node.module)
        self.assertFalse(imports & forbidden)


if __name__ == "__main__":
    unittest.main()
