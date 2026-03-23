"""Tests for critical-module coverage gate enforcement (Issue #308)."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


GATE_PATH = Path(__file__).resolve().parent / "critical_module_coverage_gate.py"
GATE_SPEC = importlib.util.spec_from_file_location("kirbyam_cov_gate", GATE_PATH)
if GATE_SPEC is None or GATE_SPEC.loader is None:
    raise RuntimeError(f"Failed to load coverage gate module from {GATE_PATH}")
gate = importlib.util.module_from_spec(GATE_SPEC)
GATE_SPEC.loader.exec_module(gate)


def _write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_enforce_thresholds_passes_when_all_modules_meet_target(tmp_path: Path) -> None:
    cov = tmp_path / "coverage.json"
    thr = tmp_path / "thresholds.json"

    _write_json(
        cov,
        {
            "files": {
                "worlds/kirbyam/client.py": {"summary": {"percent_covered": 90.0}},
                "worlds/kirbyam/rules.py": {"summary": {"percent_covered": 95.0}},
            }
        },
    )
    _write_json(
        thr,
        {
            "worlds/kirbyam/client.py": 88.0,
            "worlds/kirbyam/rules.py": 90.0,
        },
    )

    ok, lines = gate.enforce_thresholds(cov, thr)
    assert ok
    assert any("All critical module coverage thresholds passed." in line for line in lines)


def test_enforce_thresholds_fails_for_low_coverage(tmp_path: Path) -> None:
    cov = tmp_path / "coverage.json"
    thr = tmp_path / "thresholds.json"

    _write_json(
        cov,
        {
            "files": {
                "worlds/kirbyam/client.py": {"summary": {"percent_covered": 80.0}},
            }
        },
    )
    _write_json(thr, {"worlds/kirbyam/client.py": 88.0})

    ok, lines = gate.enforce_thresholds(cov, thr)
    assert not ok
    assert any("80.0% < 88.0%" in line for line in lines)


def test_enforce_thresholds_fails_when_required_module_missing(tmp_path: Path) -> None:
    cov = tmp_path / "coverage.json"
    thr = tmp_path / "thresholds.json"

    _write_json(cov, {"files": {}})
    _write_json(thr, {"worlds/kirbyam/client.py": 88.0})

    ok, lines = gate.enforce_thresholds(cov, thr)
    assert not ok
    assert any("missing from coverage report" in line for line in lines)
