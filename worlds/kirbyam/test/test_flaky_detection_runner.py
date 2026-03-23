"""Tests for the KirbyAM flaky detection runner (Issue #310)."""

from __future__ import annotations

import importlib.util
from pathlib import Path


RUNNER_PATH = Path(__file__).resolve().parent / "flaky_detection_runner.py"
RUNNER_SPEC = importlib.util.spec_from_file_location("kirbyam_flaky_runner", RUNNER_PATH)
if RUNNER_SPEC is None or RUNNER_SPEC.loader is None:
    raise RuntimeError(f"Failed to load flaky detection runner from {RUNNER_PATH}")
runner = importlib.util.module_from_spec(RUNNER_SPEC)
RUNNER_SPEC.loader.exec_module(runner)


def test_parse_args_rejects_non_positive_runs() -> None:
    try:
        runner.parse_args(["--runs", "0"])
        assert False, "Expected SystemExit for --runs 0"
    except SystemExit as exc:
        assert "--runs must be >= 1" in str(exc)


def test_parse_args_uses_default_targets() -> None:
    args = runner.parse_args(["--runs", "2"])
    assert args.targets == list(runner.DEFAULT_TARGETS)


def test_extract_failed_tests_from_junit(tmp_path: Path) -> None:
    xml_path = tmp_path / "run.xml"
    xml_path.write_text(
        """
<testsuite tests=\"2\" failures=\"1\"> 
  <testcase classname=\"worlds.kirbyam.test.test_reconnect_chaos\" name=\"test_a\">
    <failure message=\"boom\">trace</failure>
  </testcase>
  <testcase classname=\"worlds.kirbyam.test.test_reconnect_chaos\" name=\"test_b\" />
</testsuite>
""".strip(),
        encoding="utf-8",
    )

    failed = runner._extract_failed_tests_from_junit(xml_path)
    assert failed == ["worlds.kirbyam.test.test_reconnect_chaos::test_a"]


def test_extract_failed_tests_handles_parse_error(tmp_path: Path) -> None:
    xml_path = tmp_path / "broken.xml"
    xml_path.write_text("<testsuite><testcase>", encoding="utf-8")
    failed = runner._extract_failed_tests_from_junit(xml_path)
    assert failed == ["<junit-parse-error>"]
