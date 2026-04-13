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

import os
import sys

# When this script is executed from worlds/kirbyam, Python prepends that folder
# to sys.path. That folder contains types.py, which can shadow stdlib types.
_SCRIPT_DIR = os.path.realpath(os.path.dirname(__file__))
if sys.path and os.path.realpath(sys.path[0]) == _SCRIPT_DIR:
    sys.path.pop(0)

import argparse
import json
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Any

DEFAULT_WORLD_NAME = "kirbyam"
DEFAULT_APCONTAINER_VERSION = 7


def _augment_toolchain_path(base_env: dict[str, str]) -> dict[str, str]:
    """Return a child-process env with common Windows toolchain paths prepended."""
    env = dict(base_env)
    existing_path = env.get("PATH") or env.get("Path") or ""

    user_home = Path.home()
    path_candidates = [
        # User-local make install path used in this workspace.
        user_home / "tools" / "make-4.4.1-without-guile-w32-bin" / "bin",
        # User-local Arm GNU toolchain path used in this workspace.
        user_home / "tools" / "arm-gnu-toolchain-14.2.rel1" / "bin",
        # Winget app links (contains make shim for per-user install).
        Path(env.get("LOCALAPPDATA", str(user_home / "AppData" / "Local"))) / "Microsoft" / "WinGet" / "Links",
        # Common devkitPro install locations.
        Path("C:/devkitPro/msys2/usr/bin"),
        Path("C:/devkitPro/devkitARM/bin"),
    ]

    prepended = [str(p) for p in path_candidates if p.exists()]
    if prepended:
        env["PATH"] = ";".join(prepended + ([existing_path] if existing_path else []))
    return env


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
    # For --source-type file, patch_rom.py reads rom_path.tmp and writes to a fixed
    # output path under worlds/kirbyam/data/. Passing [patch] in this mode is ignored.

    try:
        child_env = _augment_toolchain_path(os.environ)
        proc = subprocess.run(
            cmd,
            cwd=str(payload_dir),
            env=child_env,
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


def get_default_install_path(world_name: str) -> Path | None:
    if os.name != "nt":
        return None

    program_data = Path(os.environ.get("ProgramData", r"C:\ProgramData"))
    return program_data / "Archipelago" / "custom_worlds" / f"{world_name}.apworld"


def install_apworld(apworld_path: Path, install_path: Path) -> None:
    install_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(apworld_path, install_path)


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
    p.add_argument(
        "--install-path",
        default=None,
        help="Path to install the built .apworld after packaging. Defaults to %%ProgramData%%\\Archipelago\\custom_worlds\\<world>.apworld on Windows.",
    )
    p.add_argument(
        "--skip-install",
        action="store_true",
        help="Skip copying the built .apworld into the Archipelago custom_worlds directory.",
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help="Disable interactive prompts; fail fast when required inputs are missing.",
    )
    return p.parse_args()


def _can_prompt(non_interactive: bool) -> bool:
    if non_interactive:
        return False

    stdin = getattr(sys, "stdin", None)
    stdout = getattr(sys, "stdout", None)
    return bool(
        stdin is not None
        and stdout is not None
        and stdin.isatty()
        and stdout.isatty()
    )


def _prompt_yes_no(prompt: str, *, default: bool) -> bool:
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please enter 'y' or 'n'.")


def _prompt_existing_file(prompt: str) -> str:
    while True:
        raw = input(prompt).strip().strip("'\"")
        if not raw:
            print("A file path is required.")
            continue

        candidate = Path(raw).expanduser()
        if candidate.is_file():
            return str(candidate.resolve())

        print(f"File not found: {candidate}")


def _prepare_args_for_patch(args: argparse.Namespace, world_root: Path) -> argparse.Namespace:
    if args.skip_patch:
        return args

    can_prompt = _can_prompt(bool(args.non_interactive))

    if args.source_type == "arg":
        if args.rom:
            rom_candidate = Path(args.rom).expanduser()
            if not rom_candidate.is_file():
                if not can_prompt:
                    raise SystemExit(
                        "--rom must point to an existing base ROM file when using --source-type arg."
                    )
                print(f"Provided ROM path does not exist: {rom_candidate}")
                args.rom = _prompt_existing_file("Enter path to the base ROM (.gba): ")
            else:
                args.rom = str(rom_candidate.resolve())
        else:
            if not can_prompt:
                raise SystemExit(
                    "You selected --source-type arg but did not provide --rom <path>. "
                    "Run interactively to be prompted, or pass --rom explicitly."
                )
            print("--source-type arg requires a base ROM path.")
            args.rom = _prompt_existing_file("Enter path to the base ROM (.gba): ")

    elif args.source_type == "file":
        rom_path_tmp = world_root / "kirby_ap_payload" / "rom_path.tmp"
        rom_path_text = ""
        if rom_path_tmp.exists():
            try:
                rom_path_text = rom_path_tmp.read_text(encoding="utf-8").strip().strip("'\"")
            except OSError:
                rom_path_text = ""

        rom_path_ok = False
        if rom_path_text:
            rom_candidate = Path(rom_path_text).expanduser()
            if not rom_candidate.is_absolute():
                rom_candidate = rom_path_tmp.parent / rom_candidate
            rom_path_ok = rom_candidate.is_file()

        if not rom_path_ok:
            guidance = (
                "--source-type file requires kirby_ap_payload/rom_path.tmp to contain a valid ROM path. "
                "Use --source-type arg --rom <path> instead."
            )
            if not can_prompt:
                # Keep existing non-interactive behavior for automation and tests:
                # patch_rom.py remains the source of truth for file-source failures.
                return args

            print(
                "Could not find a valid ROM path in kirby_ap_payload/rom_path.tmp."
            )
            if _prompt_yes_no("Switch to --source-type arg and enter a ROM path now?", default=True):
                args.source_type = "arg"
                args.rom = _prompt_existing_file("Enter path to the base ROM (.gba): ")
            else:
                print(guidance)

    return args


def main() -> None:
    args = parse_args()
    world_name = args.world

    if world_name.lower() != world_name:
        raise SystemExit("World name must be lowercase.")

    world_root = Path(__file__).resolve().parent
    args = _prepare_args_for_patch(args, world_root)

    if Path.cwd().resolve() != world_root:
        print(f"Using world root from script location: {world_root}")

    manifest_path = world_root / "archipelago.json"
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest: {manifest_path}")

    # 1) Ensure manifest includes APContainer fields
    inject_apcontainer_fields(manifest_path, int(args.apcontainer_version))

    # 2) Run patch_rom.py (build payload + generate base_patch.bsdiff4)
    if not args.skip_patch:
        patch_out = world_root / "data" / "base_patch.bsdiff4"
        try:
            run_patch_rom(world_root, source_type=args.source_type, rom_arg=args.rom)
        except SystemExit as e:
            message = str(e)
            toolchain_missing = (
                "'make' was not found on PATH" in message
                or "required tool 'arm-none-eabi" in message
            )

            # Allow packaging/install to continue when patch regeneration is unavailable
            # but an existing base patch is already present in data/.
            if toolchain_missing and patch_out.exists():
                print(
                    "Warning: payload toolchain unavailable; using existing "
                    f"base patch at {patch_out} and continuing packaging/install."
                )
                print("Hint: install GNU make + devkitARM to regenerate base_patch.bsdiff4.")
            else:
                raise
    else:
        print("Skipping patch_rom.py (--skip-patch)")

    # 3) Build .apworld in-place
    apworld_path = build_apworld_in_place(world_root, world_name)

    install_path: Path | None
    if args.install_path:
        install_path = Path(args.install_path)
    else:
        install_path = get_default_install_path(world_name)

    if args.skip_install:
        print("Skipping .apworld install (--skip-install)")
    elif install_path is None:
        print("No default .apworld install path for this platform; built archive left in world folder.")
    else:
        install_apworld(apworld_path, install_path)
        print(f"Installed: {install_path}")

    print("")
    print(f"Built: {apworld_path}")
    print("")
    print("Next steps:")
    if args.skip_install or install_path is None:
        print("1) Copy this .apworld into your Archipelago custom_worlds directory, if needed.")
        print("2) Restart ArchipelagoLauncher.exe")
        print("3) Click 'Generate Template Settings' and look for: Kirby & The Amazing Mirror")
    else:
        print("1) Restart ArchipelagoLauncher.exe")
        print("2) Click 'Generate Template Settings' and look for: Kirby & The Amazing Mirror")


if __name__ == "__main__":
    main()
