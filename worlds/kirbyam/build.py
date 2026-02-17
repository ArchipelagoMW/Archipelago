#!/usr/bin/env python3
"""
build_kirbyam_apworld.py

Runs the Kirby AM patch build (calls kirby_ap_payload/patch_rom.py), then packages this
world folder into kirbyam.apworld in-place (inside worlds/kirbyam).

Key requirements:
- Do NOT create any new folders (no staging dir).
- The build script is run from repo_root/worlds/kirbyam/
- patch_rom.py is at repo_root/worlds/kirbyam/kirby_ap_payload/
- Output .apworld should be created inside worlds/kirbyam/
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any

DEFAULT_WORLD_NAME = "kirbyam"
DEFAULT_APCONTAINER_VERSION = 7


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise SystemExit(
            f"Missing manifest: {path}\n"
            f"Create archipelago.json in this world folder first."
        ) from e
    except json.JSONDecodeError as e:
        raise SystemExit(f"Invalid JSON in manifest: {path}\n{e}") from e


def write_pretty_json(path: Path, obj: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def inject_apcontainer_fields(manifest_path: Path, apcontainer_version: int) -> None:
    manifest = load_json(manifest_path)
    changed = False

    if "version" not in manifest:
        manifest["version"] = apcontainer_version
        changed = True
    if "compatible_version" not in manifest:
        manifest["compatible_version"] = apcontainer_version
        changed = True

    if changed:
        write_pretty_json(manifest_path, manifest)


def run_patch_rom(world_root: Path, source_type: str, rom_arg: str | None) -> None:
    """
    Calls patch_rom.py from kirby_ap_payload/ and runs it with cwd set to kirby_ap_payload/
    so it can find Makefile/payload.bin as expected.

    patch_rom.py (new behavior):
      - Default --source-type file: reads base ROM from rom_path.tmp
      - If --source-type arg: takes <in.gba> as a positional
      - Always takes optional [patch_path] positional
      - Creates an intermediary .gba internally and deletes it after generating the patch.
    """
    payload_dir = world_root / "kirby_ap_payload"
    patch_script = payload_dir / "patch_rom.py"

    if not patch_script.exists():
        raise SystemExit(f"patch_rom.py not found: {patch_script}")

    # IMPORTANT: This does not create folders; it expects data/ already exists.
    patch_out = world_root / "data" / "base_patch.bsdiff4"

    if not patch_out.parent.exists():
        raise SystemExit(
            f"Missing data folder: {patch_out.parent}\n"
            "Create worlds/kirbyam/data/ (folder) manually; this build script will not create folders."
        )

    print("Running patch_rom.py:")
    print(f"  CWD:        {payload_dir}")
    print(f"  Patch out:  {patch_out}")
    print(f"  Source:     {source_type}")

    cmd: list[str] = [sys.executable, str(patch_script), "--source-type", source_type]

    if source_type == "arg":
        if not rom_arg:
            raise SystemExit(
                "You selected --source-type arg but did not provide --rom <path>."
            )
        print(f"  Input ROM:  {rom_arg}")
        # patch_rom.py expects: --source-type arg <in.gba> [patch]
        cmd += [rom_arg, str(patch_out)]
    else:
        # patch_rom.py expects: [patch] (default source-type file)
        # We pass patch_out as the single optional positional.
        cmd += [str(patch_out)]

    try:
        proc = subprocess.run(
            cmd,
            cwd=str(payload_dir),
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if proc.stdout:
            print(proc.stdout.rstrip())
    except subprocess.CalledProcessError as e:
        output = (e.stdout or "").rstrip()
        raise SystemExit(
            "patch_rom.py failed.\n"
            f"Command: {' '.join(cmd)}\n"
            f"{output}"
        ) from e

    if not patch_out.exists():
        raise SystemExit(
            f"patch_rom.py completed but patch file was not created:\n  {patch_out}\n"
            "Confirm patch_rom.py is writing to the path provided as its [patch] argument."
        )


def should_exclude(rel_posix: str) -> bool:
    parts = rel_posix.split("/")
    name = parts[-1]

    # Skip bytecode/cache
    if "__pycache__" in parts:
        return True
    if name.endswith(".pyc") or name.endswith(".pyo"):
        return True

    # Skip build outputs / local-only items
    if name.endswith(".apworld") or name.endswith(".zip") or name.endswith(".gba"):
        return True
    if name in {".DS_Store", "Thumbs.db"}:
        return True

    return False


def build_apworld_in_place(world_root: Path, world_name: str) -> Path:
    """
    Creates <world_root>/<world_name>.apworld containing a top-level folder named <world_name>.
    No staging folder is created.
    """
    out_path = world_root / f"{world_name}.apworld"
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for p in world_root.rglob("*"):
            if p.is_dir():
                continue

            rel = p.relative_to(world_root)
            rel_posix = rel.as_posix()

            if should_exclude(rel_posix):
                continue

            arcname = f"{world_name}/{rel_posix}"
            zf.write(p, arcname)

    return out_path


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Build kirbyam.apworld in-place inside worlds/kirbyam/")
    p.add_argument("--world", default=DEFAULT_WORLD_NAME, help="World folder name (must be lowercase).")
    p.add_argument(
        "--apcontainer-version",
        type=int,
        default=DEFAULT_APCONTAINER_VERSION,
        help="APContainer manifest version/compatible_version to inject if missing.",
    )
    p.add_argument("--skip-patch", action="store_true", help="Skip calling kirby_ap_payload/patch_rom.py first.")
    p.add_argument(
        "--source-type",
        choices=("file", "arg"),
        default="file",
        help="How to locate the base ROM for patch creation: file reads rom_path.tmp; arg uses --rom.",
    )
    p.add_argument(
        "--rom",
        default=None,
        help="Path to base ROM when using --source-type arg. Ignored for --source-type file.",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    world_name = args.world

    if world_name.lower() != world_name:
        raise SystemExit("World name must be lowercase.")

    # This build script runs at repo_root/worlds/kirbyam/
    world_root = Path.cwd().resolve()

    if world_root.name != world_name:
        print(f"Warning: current directory is {world_root}, expected to be .../worlds/{world_name}")
        print("Proceeding anyway, but ensure you're running from the world folder.")

    manifest_path = world_root / "archipelago.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {manifest_path}")

    # 1) Ensure manifest includes APContainer fields
    inject_apcontainer_fields(manifest_path, int(args.apcontainer_version))

    # 2) Run patch_rom.py (build payload + generate base_patch.bsdiff4)
    if not args.skip_patch:
        run_patch_rom(world_root, source_type=args.source_type, rom_arg=args.rom)
    else:
        print("Skipping patch_rom.py (--skip-patch)")

    # 3) Build .apworld in-place
    apworld_path = build_apworld_in_place(world_root, world_name)

    print("")
    print(f"Built: {apworld_path}")
    print("")
    print("Next steps:")
    print("1) Copy this .apworld into your Archipelago custom_worlds directory, if needed.")
    print("2) Restart ArchipelagoLauncher.exe")
    print("3) Click 'Generate Template Settings' and look for: Kirby & The Amazing Mirror")


if __name__ == "__main__":
    main()
