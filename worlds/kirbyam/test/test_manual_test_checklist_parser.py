"""Tests for machine-checkable manual testing result parsing (Issue #312)."""

from __future__ import annotations

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys

import pytest


SCRIPT_PATH = Path(__file__).resolve().parents[3] / ".github" / "scripts" / "manual_test_checklist_parser.py"
SPEC = spec_from_file_location("manual_test_checklist_parser", SCRIPT_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Unable to load manual test parser from {SCRIPT_PATH}")
MODULE = module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


VALID_BLOCK = """\
Some comment text.

<!-- MANUAL_TEST_RESULT:START -->
RESULT_SCHEMA_VERSION: 1
TEST_CASE_ID: case-001
STATUS: pass
BUILD_REF: pr-123
PLATFORM: windows
BIZHAWK_VERSION: 2.10
ROM_REGION: USA
EXPECTED_RESULT: one deathlink apply
OBSERVED_RESULT: one deathlink apply
EVIDENCE: screenshot.png
NOTES: none
<!-- MANUAL_TEST_RESULT:END -->
"""


def test_parse_manual_test_results_single_block() -> None:
    parsed = MODULE.parse_manual_test_results([VALID_BLOCK])

    assert len(parsed) == 1
    assert parsed[0]["TEST_CASE_ID"] == "case-001"
    assert parsed[0]["STATUS"] == "PASS"
    assert parsed[0]["COMMENT_INDEX"] == "0"


def test_parse_manual_test_results_multiple_comments() -> None:
    comment_a = VALID_BLOCK.replace("case-001", "case-001a")
    comment_b = VALID_BLOCK.replace("case-001", "case-001b").replace("STATUS: pass", "STATUS: FAIL")

    parsed = MODULE.parse_manual_test_results([comment_a, comment_b])

    assert [entry["TEST_CASE_ID"] for entry in parsed] == ["case-001a", "case-001b"]
    assert [entry["STATUS"] for entry in parsed] == ["PASS", "FAIL"]
    assert [entry["COMMENT_INDEX"] for entry in parsed] == ["0", "1"]


def test_parse_manual_test_results_ignores_non_template_text() -> None:
    parsed = MODULE.parse_manual_test_results(["plain comment with no result block"])
    assert parsed == []


def test_parse_manual_test_results_rejects_missing_fields() -> None:
    bad_block = VALID_BLOCK.replace("EVIDENCE: screenshot.png\n", "")

    with pytest.raises(ValueError, match="missing required fields"):
        MODULE.parse_manual_test_results([bad_block])


def test_parse_manual_test_results_rejects_invalid_status() -> None:
    bad_block = VALID_BLOCK.replace("STATUS: pass", "STATUS: MAYBE")

    with pytest.raises(ValueError, match="Invalid STATUS value"):
        MODULE.parse_manual_test_results([bad_block])
