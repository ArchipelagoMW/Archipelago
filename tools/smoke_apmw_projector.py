"""Smoke-test a frozen APMW projector with one five-geometry request."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import subprocess
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
CHECKSMATE_ROOT = REPOSITORY_ROOT / "worlds" / "checksmate"
CASES_FIXTURE = (
    CHECKSMATE_ROOT / "test" / "fixtures" / "projection-v2" / "cases.json"
)
GEOMETRIES = ("8x8", "10x8", "10x10", "12x10", "12x12")


def smoke(executable: Path) -> None:
    executable = executable.resolve()
    if not executable.is_file():
        raise ValueError(f"projector executable is not a file: {executable}")

    checksmate_path = str(CHECKSMATE_ROOT)
    if checksmate_path not in sys.path:
        sys.path.insert(0, checksmate_path)
    from apmw_projection import FROZEN_CONTRACT_HASH, PROTOCOL_VERSION
    from apmw_projection.protocol import canonical_json, handle_batch_request

    cases = json.loads(CASES_FIXTURE.read_text(encoding="utf-8"))["cases"]
    base_input = next(
        case["input"] for case in cases if case["id"] == "geometry-8x8"
    )
    request = {
        "protocol_version": PROTOCOL_VERSION,
        "request_id": "frozen-release-smoke",
        "contract_hash": FROZEN_CONTRACT_HASH,
        "input": {
            field: copy.deepcopy(base_input[field])
            for field in ("itemization", "ordering", "seeds", "item_counts")
        },
        "geometries": list(GEOMETRIES),
    }
    expected = canonical_json(handle_batch_request(request))
    completed = subprocess.run(
        [str(executable)],
        input=canonical_json(request),
        capture_output=True,
        encoding="utf-8",
        check=False,
        timeout=30,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"projector exited with {completed.returncode}: {completed.stderr.strip()}"
        )
    if completed.stderr:
        raise RuntimeError(f"projector wrote unexpected stderr: {completed.stderr.strip()}")
    if completed.stdout.strip() != expected:
        raise RuntimeError("projector output does not match the canonical package")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--executable", required=True, type=Path)
    arguments = parser.parse_args(argv)
    try:
        smoke(arguments.executable)
    except (OSError, RuntimeError, ValueError, subprocess.TimeoutExpired) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
