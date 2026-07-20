"""Standalone entry point for the frozen APMW semantic projection sidecar."""

from __future__ import annotations

from pathlib import Path
import sys


if not getattr(sys, "frozen", False):
    CHECKSMATE_ROOT = Path(__file__).resolve().parent / "worlds" / "checksmate"
    sys.path.insert(0, str(CHECKSMATE_ROOT))

from apmw_projection.protocol import run_cli


def main() -> int:
    return run_cli(sys.stdin, sys.stdout, sys.stderr)


if __name__ == "__main__":
    raise SystemExit(main())
