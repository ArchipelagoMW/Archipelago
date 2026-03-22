#!/usr/bin/env python3
"""Parse machine-checkable manual testing result blocks from issue comments."""

from __future__ import annotations

import argparse
import json
import re
from typing import Any, Iterable

BLOCK_PATTERN = re.compile(
    r"<!--\s*MANUAL_TEST_RESULT:START\s*-->(.*?)<!--\s*MANUAL_TEST_RESULT:END\s*-->",
    flags=re.DOTALL,
)
LINE_PATTERN = re.compile(r"^([A-Z_]+):\s*(.*)$")
REQUIRED_FIELDS = (
    "RESULT_SCHEMA_VERSION",
    "TEST_CASE_ID",
    "STATUS",
    "BUILD_REF",
    "PLATFORM",
    "BIZHAWK_VERSION",
    "ROM_REGION",
    "EXPECTED_RESULT",
    "OBSERVED_RESULT",
    "EVIDENCE",
    "NOTES",
)
VALID_STATUS = {"PASS", "FAIL", "BLOCKED"}


def _parse_block(block_text: str) -> dict[str, str]:
    parsed: dict[str, str] = {}
    for raw_line in block_text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = LINE_PATTERN.match(line)
        if not match:
            continue
        key, value = match.group(1), match.group(2)
        parsed[key] = value

    missing = [field for field in REQUIRED_FIELDS if field not in parsed]
    if missing:
        raise ValueError(f"Manual test result block missing required fields: {missing}")

    status = parsed["STATUS"].upper()
    if status not in VALID_STATUS:
        raise ValueError(
            f"Invalid STATUS value '{parsed['STATUS']}'. Expected one of: {sorted(VALID_STATUS)}"
        )
    parsed["STATUS"] = status
    return parsed


def parse_manual_test_results(comment_bodies: Iterable[str]) -> list[dict[str, str]]:
    """Return structured result entries parsed from issue comment bodies."""
    results: list[dict[str, str]] = []
    for index, body in enumerate(comment_bodies):
        for block in BLOCK_PATTERN.findall(body):
            parsed = _parse_block(block)
            parsed["COMMENT_INDEX"] = str(index)
            results.append(parsed)
    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Parse MANUAL_TEST_RESULT blocks from text and output JSON. "
            "Use --input for a file or omit to read stdin."
        )
    )
    parser.add_argument("--input", help="Path to input text containing one or more result blocks")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print output JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.input:
        with open(args.input, "r", encoding="utf-8") as handle:
            text = handle.read()
    else:
        import sys

        text = sys.stdin.read()

    parsed = parse_manual_test_results([text])
    if args.pretty:
        print(json.dumps(parsed, indent=2, sort_keys=True))
    else:
        print(json.dumps(parsed, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
