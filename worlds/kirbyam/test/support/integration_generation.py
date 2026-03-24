"""Helpers for KirbyAM integration tests that need generated multiworld archives."""

from __future__ import annotations

import shutil
import sys
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from MultiServer import Context as MultiServerContext


def generate_archive_from_fixture(fixture_yaml: Path, output_dir: Path, seed: int = 367) -> Path:
    """Generate a single-player archive from a fixture yaml and return the output zip path."""
    import Generate
    import Main

    output_dir.mkdir(parents=True, exist_ok=True)
    original_argv = list(sys.argv)
    try:
        with TemporaryDirectory(prefix="kirbyam_issue367_players_") as players_dir:
            player_yaml = Path(players_dir) / "1.yaml"
            shutil.copy2(fixture_yaml, player_yaml)

            sys.argv = [
                sys.argv[0],
                "--seed",
                str(seed),
                "--player_files_path",
                str(players_dir),
                "--outputpath",
                str(output_dir),
            ]
            Main.main(*Generate.main())
    finally:
        sys.argv = original_argv

    archives = sorted(output_dir.glob("*.zip"), key=lambda p: p.stat().st_mtime, reverse=True)
    if len(archives) != 1:
        raise AssertionError(f"Expected exactly one generated archive in {output_dir}, found {len(archives)}")
    return archives[0]


def load_multidata_from_archive(archive_path: Path) -> dict[str, Any]:
    """Read and decode the .archipelago payload from a generated zip archive."""
    with zipfile.ZipFile(archive_path) as zf:
        archipelago_entries = [name for name in zf.namelist() if name.endswith(".archipelago")]
        if len(archipelago_entries) != 1:
            raise AssertionError(
                f"Expected exactly one .archipelago entry in {archive_path}, found {len(archipelago_entries)}"
            )
        data = zf.read(archipelago_entries[0])

    decoded = MultiServerContext.decompress(data)
    if not isinstance(decoded, dict):
        raise AssertionError("Decoded multidata payload is not a dictionary")
    return decoded
