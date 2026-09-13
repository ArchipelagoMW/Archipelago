"""Module entry point for the APMW projection JSON sidecar."""

from __future__ import annotations

import sys

from .protocol import run_cli


if __name__ == "__main__":
    raise SystemExit(run_cli(sys.stdin, sys.stdout, sys.stderr))
