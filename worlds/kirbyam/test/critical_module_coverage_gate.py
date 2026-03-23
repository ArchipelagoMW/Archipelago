"""Enforce per-module coverage thresholds for critical KirbyAM modules."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def _load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as e:
        raise SystemExit(f"Missing JSON file: {path}") from e
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON file: {path}\n{e}") from e


def _normalize_path(path_str: str) -> str:
    return path_str.replace("\\", "/")


def enforce_thresholds(coverage_json: Path, thresholds_json: Path) -> tuple[bool, list[str]]:
    coverage = _load_json(coverage_json)
    thresholds_raw = _load_json(thresholds_json)

    files = coverage.get("files")
    if not isinstance(files, dict):
        raise SystemExit(f"Coverage JSON does not contain 'files' object: {coverage_json}")

    threshold_items: dict[str, float] = {}
    for module_path, threshold in thresholds_raw.items():
        if not isinstance(module_path, str):
            raise SystemExit("Threshold keys must be module path strings")
        if not isinstance(threshold, (int, float)):
            raise SystemExit(f"Threshold for {module_path} must be numeric")
        threshold_items[_normalize_path(module_path)] = float(threshold)

    covered_by_norm_path: dict[str, float] = {}
    for raw_path, payload in files.items():
        normalized = _normalize_path(raw_path)
        summary = payload.get("summary", {}) if isinstance(payload, dict) else {}
        percent = summary.get("percent_covered")
        if isinstance(percent, (int, float)):
            covered_by_norm_path[normalized] = float(percent)

    failures: list[str] = []
    details: list[str] = []

    for module_path, threshold in threshold_items.items():
        actual = covered_by_norm_path.get(module_path)
        if actual is None:
            failures.append(f"{module_path}: missing from coverage report (required >= {threshold:.1f}%)")
            continue

        details.append(f"{module_path}: {actual:.1f}% (required >= {threshold:.1f}%)")
        if actual + 1e-9 < threshold:
            failures.append(f"{module_path}: {actual:.1f}% < {threshold:.1f}%")

    if failures:
        return False, details + ["", "Coverage gate failures:", *failures]
    return True, details + ["", "All critical module coverage thresholds passed."]


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate critical-module coverage thresholds.")
    parser.add_argument("--coverage-json", required=True, help="Path to coverage JSON report.")
    parser.add_argument("--thresholds-json", required=True, help="Path to thresholds JSON file.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    ok, lines = enforce_thresholds(Path(args.coverage_json), Path(args.thresholds_json))
    for line in lines:
        print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
