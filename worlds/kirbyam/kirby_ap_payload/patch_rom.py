import argparse
import hashlib
import importlib.util
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PAYLOAD_OFFSET = 0x0015E000
HOOK_OFFSET    = 0x00152696

# Thumb BL to 0x0815E000 from 0x08152696 (already computed)
BL_BYTES = bytes.fromhex("0B F0 B3 FC")

ROM_PATH_TMP = "rom_path.tmp"
INTERMEDIARY_ROM = "baseline_patched.tmp.gba"


# ----------------------------
# Logging (tee stdout/stderr)
# ----------------------------
class Tee:
    def __init__(self, *streams):
        self.streams = streams

    def write(self, data):
        for s in self.streams:
            s.write(data)
            s.flush()

    def flush(self):
        for s in self.streams:
            s.flush()

def get_fixed_patch_out() -> Path:
    # patch_rom.py is in .../worlds/kirbyam/kirby_ap_payload/
    # world root is .../worlds/kirbyam
    world_root = Path(__file__).resolve().parent.parent
    return world_root / "data" / "base_patch.bsdiff4"


def get_log_path() -> Path:
    # Create the log file next to this script (same directory)
    script_dir = Path(__file__).resolve().parent
    return script_dir / "patch_rom.log"


def setup_logging() -> Path:
    log_path = get_log_path()
    # Append to preserve prior runs
    log_f = log_path.open("a", encoding="utf-8", newline="\n")
    header = (
        "\n"
        "============================================================\n"
        f"patch_rom.py run: {datetime.now().isoformat(timespec='seconds')}\n"
        f"Working dir: {Path.cwd()}\n"
        f"Args: {sys.argv}\n"
        "============================================================\n"
    )
    log_f.write(header)
    log_f.flush()

    # Tee both stdout and stderr to the same log file
    sys.stdout = Tee(sys.__stdout__, log_f)  # type: ignore[assignment]
    sys.stderr = Tee(sys.__stderr__, log_f)  # type: ignore[assignment]

    # Store handle so it stays open for duration
    return log_path


def run_make():
    """Run `make clean` then `make` in the current working directory."""
    for cmd in (["make", "clean"], ["make"]):
        print("Running:", " ".join(cmd))
        try:
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )
            if result.stdout:
                print(result.stdout.rstrip())
        except FileNotFoundError as e:
            raise SystemExit(
                "Error: 'make' was not found on PATH.\n"
                "Install build tools (e.g., GNU Make) or run this script in an environment where `make` is available."
            ) from e
        except subprocess.CalledProcessError as e:
            output = (e.stdout or "").rstrip()
            raise SystemExit(
                f"Error: command failed: {' '.join(cmd)}\n"
                f"{output}"
            ) from e


def require_bsdiff4():
    try:
        import bsdiff4  # noqa: F401
        return bsdiff4
    except ModuleNotFoundError as e:
        raise SystemExit(
            "Error: Python package 'bsdiff4' is not installed.\n"
            "Install it in the SAME environment you run this script with:\n"
            "  python -m pip install bsdiff4\n"
        ) from e


def read_rom_path_from_tmp(tmp_path: str) -> str:
    try:
        with open(tmp_path, "r", encoding="utf-8") as f:
            for line in f:
                candidate = line.strip()
                if candidate:
                    candidate = candidate.strip('"').strip("'").strip()
                    return candidate
    except FileNotFoundError as e:
        raise SystemExit(
            f"Error: '{tmp_path}' not found.\n"
            f"Create '{tmp_path}' with a single line pointing to your clean base ROM."
        ) from e

    raise SystemExit(
        f"Error: '{tmp_path}' exists but contains no usable ROM path.\n"
        "Put the full path to the ROM on the first line."
    )


def safe_unlink(path: str) -> None:
    try:
        os.remove(path)
        print("Deleted intermediary ROM:", path)
    except FileNotFoundError:
        return
    except Exception as e:
        print(f"Warning: failed to delete intermediary ROM '{path}': {e}")


def md5_file(path: str, chunk_size: int = 1024 * 1024) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk_size)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def load_expected_rom_md5_from_rom_py() -> str:
    """
    Load expected base ROM MD5 from worlds/kirbyam/rom.py as a package import so
    relative imports inside rom.py work.

    Assumptions:
      - patch_rom.py is at .../worlds/kirbyam/kirby_ap_payload/patch_rom.py
      - repo root is 3 parents up from this script (contains 'worlds/')
      - expected hash lives at KirbyAmProcedurePatch.hash
    """
    script_path = Path(__file__).resolve()
    repo_root = script_path.parents[3]  # repo root containing 'worlds/'

    repo_root_str = str(repo_root)
    added = False
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)
        added = True

    try:
        # Import as a proper package module so rom.py's relative imports work.
        import importlib

        mod = importlib.import_module("worlds.kirbyam.rom")

        if not hasattr(mod, "KirbyAmProcedurePatch"):
            raise SystemExit("--hash-debug: worlds.kirbyam.rom does not define KirbyAmProcedurePatch")

        cls = getattr(mod, "KirbyAmProcedurePatch")
        if not hasattr(cls, "hash"):
            raise SystemExit("--hash-debug: KirbyAmProcedurePatch has no attribute 'hash'")

        expected = getattr(cls, "hash")
        if not isinstance(expected, str) or not expected:
            raise SystemExit("--hash-debug: KirbyAmProcedurePatch.hash is not a non-empty string")

        expected = expected.strip().lower()
        if any(c not in "0123456789abcdef" for c in expected) or len(expected) != 32:
            raise SystemExit(
                "--hash-debug: KirbyAmProcedurePatch.hash does not look like an MD5 hex digest.\n"
                f"Value: {expected!r}"
            )

        return expected
    except ModuleNotFoundError as e:
        raise SystemExit(
            "--hash-debug: Failed to import worlds.kirbyam.rom.\n"
            f"Repo root used: {repo_root_str}\n"
            f"Original error: {e}"
        ) from e
    finally:
        # Optional rollback to keep environment clean
        if added:
            try:
                sys.path.remove(repo_root_str)
            except ValueError:
                pass


def hash_debug_report(in_path: str, source_type: str) -> None:
    print("")
    print("=== HASH DEBUG (BASE ROM) ===")
    print("Source type:", source_type)
    print("Base ROM path:", in_path)

    if source_type == "file":
        tmp = Path(ROM_PATH_TMP).resolve()
        print("rom_path.tmp:", str(tmp))
        if tmp.exists():
            try:
                line0 = tmp.read_text(encoding="utf-8", errors="replace").splitlines()[:1]
                if line0:
                    print("rom_path.tmp first line:", line0[0])
            except Exception as e:
                print(f"Warning: could not read rom_path.tmp for display: {e}")
        else:
            print("rom_path.tmp exists: False")

    p = Path(in_path)
    print("Exists:", p.exists())
    if not p.exists():
        print("=== HASH DEBUG END (ROM MISSING) ===")
        print("")
        return

    try:
        size = p.stat().st_size
        print("Size (bytes):", size)
    except Exception as e:
        print(f"Warning: could not stat ROM file: {e}")

    # Compute MD5 of base ROM
    actual = md5_file(in_path)

    # Load expected MD5 from rom.py
    expected = load_expected_rom_md5_from_rom_py()

    # Adjacent lines, explicitly labeled
    print(f"Expected MD5 (rom.py KirbyAmProcedurePatch.hash): {expected}")
    print(f"Computed MD5 (selected base ROM):               {actual}")

    if actual.lower() == expected.lower():
        print("Result: MATCH (base ROM MD5 matches expected).")
    else:
        print("Result: MISMATCH (base ROM MD5 does NOT match expected).")
        print("Action: verify you're using the correct (clean, unmodified) USA ROM file.")

    print("=== HASH DEBUG END ===")
    print("")


def parse_args(argv):
    fixed_patch = str(get_fixed_patch_out())

    # Legacy mode: <in> <out> [patch] and no flags
    if len(argv) in (3, 4) and not any(a.startswith("-") for a in argv[1:]):
        in_path = argv[1]
        ignored_out = argv[2]
        if len(argv) == 4:
            print(f"Warning: ignoring user-supplied patch output path '{argv[3]}'")
            print(f"         Patch will always be written to: {fixed_patch}")
        return {
            "source_type": "arg",
            "in_path": in_path,
            "patch_path": fixed_patch,
            "legacy_ignored_out": ignored_out,
            "hash_debug": False,
        }

    parser = argparse.ArgumentParser(
        prog=os.path.basename(argv[0]),
        description="Build payload, patch ROM, and generate a bsdiff4 patch.",
    )
    parser.add_argument(
        "--source-type",
        choices=("file", "arg"),
        default="file",
        help="Where to get the base ROM path: 'file' reads rom_path.tmp, 'arg' uses positional IN_ROM.",
    )
    parser.add_argument(
        "--hash-debug",
        action="store_true",
        help="Compute and print MD5 of selected base ROM and compare to KirbyAmProcedurePatch.hash from rom.py.",
    )
    # Keep accepting optional PATH args for backwards compatibility, but they are ignored for patch output.
    parser.add_argument(
        "paths",
        nargs="*",
        help="Legacy/compat only. Any provided patch output path will be ignored.",
    )

    ns = parser.parse_args(argv[1:])

    legacy_ignored_out = None

    if ns.source_type == "file":
        # Accept 0 or 1 positional for backward compatibility, but ignore it.
        if len(ns.paths) > 1:
            raise SystemExit(
                "Usage:\n"
                "  python patch_rom.py [ignored_patch_path]\n"
                "  python patch_rom.py --source-type file [ignored_patch_path]\n"
                f"Patch will always be written to: {fixed_patch}"
            )
        if len(ns.paths) == 1:
            print(f"Warning: ignoring user-supplied patch output path '{ns.paths[0]}'")
            print(f"         Patch will always be written to: {fixed_patch}")
        in_path = read_rom_path_from_tmp(ROM_PATH_TMP)

    else:
        # Expect: IN_ROM [ignored_patch_path]
        if len(ns.paths) not in (1, 2):
            raise SystemExit(
                "Usage with --source-type arg:\n"
                "  python patch_rom.py --source-type arg <in.gba> [ignored_patch_path]\n"
                f"Patch will always be written to: {fixed_patch}"
            )
        in_path = ns.paths[0]
        if len(ns.paths) == 2:
            print(f"Warning: ignoring user-supplied patch output path '{ns.paths[1]}'")
            print(f"         Patch will always be written to: {fixed_patch}")

    return {
        "source_type": ns.source_type,
        "in_path": in_path,
        "patch_path": fixed_patch,
        "legacy_ignored_out": legacy_ignored_out,
        "hash_debug": bool(ns.hash_debug),
    }


def main():
    log_path = setup_logging()
    print(f"Logging to: {log_path}")

    args = parse_args(sys.argv)

    in_path = args["in_path"]
    patch_path = args["patch_path"]

    # Verify patch output directory exists
    patch_out_dir = Path(patch_path).resolve().parent
    if not patch_out_dir.exists():
        raise SystemExit(
            f"Error: patch output directory does not exist: {patch_out_dir}\n"
            "Create it (worlds/kirbyam/data/) and re-run. patch_rom.py will not create folders."
        )

    print("Patch output (fixed):", Path(patch_path).resolve())

    source_type = args["source_type"]
    legacy_ignored_out = args.get("legacy_ignored_out")
    hash_debug = bool(args.get("hash_debug"))

    if legacy_ignored_out is not None:
        print("Warning: legacy invocation detected (<in> <out> [patch]).")
        print(f"         Ignoring provided out ROM name: {legacy_ignored_out}")
        print(f"         Using intermediary ROM name: {INTERMEDIARY_ROM}")

    if source_type == "file":
        print(f"Source type: file (reading base ROM from '{ROM_PATH_TMP}')")
    else:
        print("Source type: arg")

    print("Base ROM path:", in_path)

    if hash_debug:
        hash_debug_report(in_path, source_type)

    if os.path.basename(in_path).lower() != "kirby.gba":
        print(f"Note: You specified input ROM '{in_path}'.")
        print("      Your canonical clean ROM is 'kirby.gba'.")
        print("      For consistency, consider using a file named 'kirby.gba' as the clean base.")

    # 1) Build step: make clean; make
    run_make()

    # 2) Load payload
    try:
        with open("payload.bin", "rb") as f:
            payload = f.read()
    except FileNotFoundError as e:
        raise SystemExit(
            "Error: payload.bin not found. Ensure your build produces payload.bin in the current directory."
        ) from e

    if len(payload) > 0x16A0:
        raise SystemExit(f"payload.bin too large: {len(payload)} bytes (max 0x16A0)")

    # 3) Load ROM
    try:
        with open(in_path, "rb") as f:
            rom = bytearray(f.read())
    except FileNotFoundError as e:
        raise SystemExit(f"Error: input ROM not found: {in_path}") from e

    # Basic size sanity for a 4MB ROM
    if len(rom) != 0x400000:
        print(f"Warning: ROM size is {len(rom):#x}, expected 0x400000. Proceeding anyway.")

    # 4) Insert payload
    rom[PAYLOAD_OFFSET:PAYLOAD_OFFSET + len(payload)] = payload

    # 5) Patch hook site with BL
    rom[HOOK_OFFSET:HOOK_OFFSET + 4] = BL_BYTES

    # 6) Write the intermediary patched ROM
    with open(INTERMEDIARY_ROM, "wb") as f:
        f.write(rom)

    # Optional: hash debug of intermediary patched ROM
    if hash_debug:
        try:
            patched_md5 = md5_file(INTERMEDIARY_ROM)
            print("")
            print("=== HASH DEBUG (PATCHED ROM OUTPUT) ===")
            print(f"Computed MD5 (expected base ROM):               {load_expected_rom_md5_from_rom_py()}")
            print(f"Computed MD5 (intermediary patched ROM output): {patched_md5}")
            print("Note: These are expected to differ (patched ROM is modified).")
            print("=== HASH DEBUG END ===")
            print("")
        except Exception as e:
            print(f"Warning: failed to compute intermediary patched ROM MD5: {e}")


    print("Intermediary patched ROM written:", INTERMEDIARY_ROM)
    print("Payload inserted at file offset:", hex(PAYLOAD_OFFSET))
    print("Hook patched at file offset:", hex(HOOK_OFFSET), "with bytes:", BL_BYTES.hex(" "))

    # 7) Generate base_patch.bsdiff4: clean base -> intermediary patched ROM
    bsdiff4 = require_bsdiff4()
    try:
        bsdiff4.file_diff(in_path, INTERMEDIARY_ROM, patch_path)
    except Exception as e:
        raise SystemExit(f"Error generating bsdiff patch '{patch_path}': {e}") from e

    print("BSdiff patch generated:", patch_path)
    print("Patch source (clean):", in_path)
    print("Patch target (baseline):", INTERMEDIARY_ROM)

    # 8) Delete intermediary ROM now that patch exists
    safe_unlink(INTERMEDIARY_ROM)


if __name__ == "__main__":
    main()
