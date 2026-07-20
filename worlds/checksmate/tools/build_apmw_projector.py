"""Build the standalone APMW projector without running the Archipelago setup.

Run a frozen sidecar smoke build with:
    python worlds/checksmate/tools/build_apmw_projector.py --output build/apmw-projector-smoke
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any


CHECKSMATE_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = CHECKSMATE_ROOT.parents[1]
ENTRY_SCRIPT = Path(__file__).resolve().with_name("apmw_projector.py")
CONTRACT_DATA = (
    CHECKSMATE_ROOT / "apmw_projection" / "data" / "apmw_contract_v2.json"
)
MANIFEST_NAME = "apmw-projector-manifest.json"
CX_FREEZE_VERSION = "8.0.0"
BUILD_MANIFEST_SCHEMA = "apmw_projector_build_manifest"
BUILD_MANIFEST_VERSION = 1


def projector_executable_name(system: str | None = None) -> str:
    return (
        "ApmwProjector.exe"
        if normalize_platform(system) == "windows"
        else "ApmwProjector"
    )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def normalize_platform(system: str | None = None) -> str:
    platforms = {
        "windows": "windows",
        "linux": "linux",
        "darwin": "macos",
        "macos": "macos",
    }
    value = (system or platform.system()).lower()
    try:
        return platforms[value]
    except KeyError as error:
        raise ValueError(f"unsupported projector platform: {value}") from error


def normalize_architecture(machine: str | None = None) -> str:
    architectures = {
        "x86": "x86",
        "i386": "x86",
        "i486": "x86",
        "i586": "x86",
        "i686": "x86",
        "x64": "x64",
        "amd64": "x64",
        "x86_64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
    }
    value = (machine or platform.machine()).lower()
    try:
        return architectures[value]
    except KeyError as error:
        raise ValueError(f"unsupported projector architecture: {value}") from error


def projector_metadata() -> dict[str, Any]:
    _ensure_checksmate_import_path()
    from apmw_projection import (
        FROZEN_CONTRACT_HASH,
        PROTOCOL_VERSION,
        RUNTIME_SEMANTIC_VERSION,
    )

    return {
        "runtime_semantic_version": RUNTIME_SEMANTIC_VERSION,
        "protocol_version": PROTOCOL_VERSION,
        "contract_hash": FROZEN_CONTRACT_HASH,
    }


def build_manifest(executable: Path, output_dir: Path) -> dict[str, Any]:
    executable = executable.resolve()
    output_dir = output_dir.resolve()
    return {
        "schema": BUILD_MANIFEST_SCHEMA,
        "version": BUILD_MANIFEST_VERSION,
        **projector_metadata(),
        "target_platform": normalize_platform(),
        "target_architecture": normalize_architecture(),
        "executable_relative_path": executable.relative_to(output_dir).as_posix(),
        "executable_sha256": sha256_file(executable),
    }


def write_manifest(executable: Path, output_dir: Path) -> Path:
    manifest_path = output_dir / MANIFEST_NAME
    manifest_path.write_text(
        json.dumps(
            build_manifest(executable, output_dir),
            sort_keys=True,
            separators=(",", ":"),
        )
        + "\n",
        encoding="ascii",
    )
    return manifest_path


def build_projector(output_dir: Path) -> Path:
    """Freeze only the ChecksMate projector entry and return its manifest path."""
    cx_freeze = _load_cx_freeze()
    output_dir = output_dir.resolve()
    if output_dir.exists() and any(output_dir.iterdir()):
        raise ValueError(f"output directory is not empty: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    _ensure_checksmate_import_path()

    executable_name = projector_executable_name()
    metadata = projector_metadata()
    cx_freeze.setup(
        name="ApmwProjector",
        version=metadata["runtime_semantic_version"],
        description="Standalone APMW semantic projection sidecar",
        options={
            "build_exe": {
                "packages": ["apmw_projection"],
                "include_files": [
                    (
                        str(CONTRACT_DATA),
                        "data/apmw_contract_v2.json",
                    )
                ],
            }
        },
        executables=[
            cx_freeze.Executable(
                script=str(ENTRY_SCRIPT),
                target_name=executable_name,
            )
        ],
        script_args=["build_exe", "--build-exe", str(output_dir)],
    )
    executable = output_dir / executable_name
    if not executable.is_file():
        raise RuntimeError(f"cx_Freeze did not create projector executable: {executable}")
    return write_manifest(executable, output_dir)


def _ensure_checksmate_import_path() -> None:
    path = str(CHECKSMATE_ROOT)
    if path not in sys.path:
        sys.path.insert(0, path)


def _load_cx_freeze() -> Any:
    try:
        import cx_Freeze
    except ImportError as error:
        raise RuntimeError(
            f"cx_Freeze {CX_FREEZE_VERSION} is required; "
            "install the pinned dependency before building"
        ) from error
    if getattr(cx_Freeze, "__version__", None) != CX_FREEZE_VERSION:
        raise RuntimeError(
            f"cx_Freeze {CX_FREEZE_VERSION} is required; found {cx_Freeze.__version__}"
        )
    return cx_Freeze


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="empty directory that will receive the standalone projector",
    )
    arguments = parser.parse_args(argv)
    try:
        manifest = build_projector(arguments.output)
    except (RuntimeError, ValueError) as error:
        parser.error(str(error))
    print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
