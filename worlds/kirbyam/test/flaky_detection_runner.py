"""Repeat reconnect-sensitive KirbyAM tests to detect intermittent failures.

Usage (local):
  python worlds/kirbyam/test/flaky_detection_runner.py --runs 20

The runner executes the selected pytest targets multiple times, writes per-run
JUnit XML files, and prints an aggregate summary that maps failing test names
to run indices where they failed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path
from typing import Iterable

DEFAULT_TARGETS: tuple[str, ...] = (
    "worlds/kirbyam/test/test_reconnect_chaos.py",
    "worlds/kirbyam/test/test_client.py::test_deliver_items_resyncs_forward_after_reconnect",
    "worlds/kirbyam/test/test_client.py::test_receive_notification_reconnect_replay_dedupes_on_rewind",
    "worlds/kirbyam/test/test_client.py::test_game_watcher_reconnect_entry_resets_transient_state_once",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Repeat reconnect-sensitive tests and report flaky failures.")
    parser.add_argument("--runs", type=int, default=20, help="Number of repeated executions (default: 20).")
    parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        default=None,
        help="Pytest target to run. Repeatable. Defaults to a reconnect-sensitive KirbyAM set.",
    )
    parser.add_argument(
        "--junit-dir",
        default=None,
        help="Directory for per-run JUnit XML files. Defaults to a temporary directory.",
    )
    parser.add_argument(
        "--json-out",
        default=None,
        help="Optional JSON summary output path.",
    )
    parser.add_argument(
        "--pytest-arg",
        action="append",
        dest="pytest_args",
        default=None,
        help="Additional argument to pass through to pytest. Repeatable.",
    )

    ns = parser.parse_args(argv)

    if ns.runs <= 0:
        raise SystemExit("--runs must be >= 1")

    if ns.targets is None or len(ns.targets) == 0:
        ns.targets = list(DEFAULT_TARGETS)

    if ns.pytest_args is None:
        ns.pytest_args = []

    return ns


def _extract_failed_tests_from_junit(junit_xml: Path) -> list[str]:
    if not junit_xml.exists():
        return []

    try:
        root = ET.fromstring(junit_xml.read_text(encoding="utf-8"))
    except ET.ParseError:
        return ["<junit-parse-error>"]

    failed: list[str] = []
    for case in root.findall(".//testcase"):
        has_failure = case.find("failure") is not None or case.find("error") is not None
        if not has_failure:
            continue
        classname = case.attrib.get("classname", "")
        name = case.attrib.get("name", "<unknown>")
        if classname:
            failed.append(f"{classname}::{name}")
        else:
            failed.append(name)
    return failed


def _run_once(run_index: int, targets: Iterable[str], junit_path: Path, pytest_args: list[str]) -> tuple[int, list[str], str]:
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        *targets,
        "--junitxml",
        str(junit_path),
        *pytest_args,
    ]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    failed_tests = _extract_failed_tests_from_junit(junit_path)
    output = proc.stdout or ""

    print(f"[run {run_index}] exit={proc.returncode}")
    if failed_tests:
        print(f"[run {run_index}] failed tests: {', '.join(failed_tests)}")

    return proc.returncode, failed_tests, output


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.junit_dir:
        junit_dir = Path(args.junit_dir)
        junit_dir.mkdir(parents=True, exist_ok=True)
        temp_context = None
    else:
        temp_context = tempfile.TemporaryDirectory(prefix="kirbyam-flaky-junit-")
        junit_dir = Path(temp_context.name)

    print("KirbyAM flaky detection mode")
    print(f"Runs: {args.runs}")
    print(f"Targets: {args.targets}")
    print(f"JUnit dir: {junit_dir}")
    if args.pytest_args:
        print(f"Extra pytest args: {args.pytest_args}")

    failures_by_test: dict[str, list[int]] = defaultdict(list)
    failing_runs: list[int] = []

    try:
        for run_index in range(1, args.runs + 1):
            junit_path = junit_dir / f"run-{run_index}.xml"
            rc, failed_tests, _output = _run_once(run_index, args.targets, junit_path, args.pytest_args)
            if rc != 0:
                failing_runs.append(run_index)
            for test_name in failed_tests:
                failures_by_test[test_name].append(run_index)
    finally:
        if temp_context is not None:
            # Keep temp files only when explicitly requested with --junit-dir.
            temp_context.cleanup()

    summary = {
        "runs": args.runs,
        "targets": args.targets,
        "failing_runs": failing_runs,
        "failures_by_test": {name: runs for name, runs in sorted(failures_by_test.items())},
    }

    print("\n=== Flaky Detection Summary ===")
    if not failing_runs:
        print(f"No failures across {args.runs} runs.")
    else:
        print(f"Failing runs: {failing_runs}")
        if failures_by_test:
            print("Failures by test:")
            for test_name, runs in sorted(failures_by_test.items()):
                print(f"- {test_name}: runs {runs}")

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote JSON summary: {out_path}")

    return 1 if failing_runs else 0


if __name__ == "__main__":
    raise SystemExit(main())
