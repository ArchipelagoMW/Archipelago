"""Bootstrap a local Archipelago MultiServer for KirbyAM integration testing."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def _find_latest_archive(output_dir: Path) -> Path:
    candidates = sorted(
        [
            p for p in output_dir.glob("**/*")
            if p.is_file() and p.suffix.lower() in {".zip", ".archipelago"}
        ],
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError(
            f"No generated multiworld archive found in {output_dir}. "
            "Run Generate.py first."
        )
    return candidates[0]


def _run(cmd: Sequence[str], cwd: Path) -> int:
    process = subprocess.run(cmd, cwd=str(cwd))
    return process.returncode


def main() -> int:
    repo_root = Path(__file__).resolve().parents[4]

    parser = argparse.ArgumentParser(
        description="Start local MultiServer for KirbyAM test archive.",
    )
    parser.add_argument(
        "--archive",
        help="Path to generated archive (.zip/.archipelago). If omitted, newest file in --output-dir is used.",
        default=None,
    )
    parser.add_argument(
        "--output-dir",
        default=str(repo_root / "output"),
        help="Directory to scan for generated archive when --archive is not provided.",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("KIRBYAM_TEST_SERVER_HOST", "0.0.0.0"),
        help="Host interface for MultiServer.",
    )
    parser.add_argument(
        "--port",
        default=os.getenv("KIRBYAM_TEST_SERVER_PORT", "38281"),
        help="Port for MultiServer.",
    )
    args = parser.parse_args()

    archive_path = Path(args.archive).resolve() if args.archive else _find_latest_archive(Path(args.output_dir))
    if not archive_path.exists():
        raise FileNotFoundError(f"Archive not found: {archive_path}")

    cmd = [
        sys.executable,
        "MultiServer.py",
        "--host",
        str(args.host),
        "--port",
        str(args.port),
        str(archive_path),
    ]
    print(f"Starting MultiServer with archive: {archive_path}")
    return _run(cmd, cwd=repo_root)


if __name__ == "__main__":
    raise SystemExit(main())
