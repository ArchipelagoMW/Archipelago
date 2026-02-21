"""
Startup benchmark: Launcher and Options Creator startup time with cold vs hot world list cache.
- Launcher startup (cache cold): clear cache, then time from start to Launcher ready.
- Options Creator startup (cache cold): clear cache, then time from start to Options Creator ready.
- Launcher startup (cache hot): pre-populate cache, then time from start to Launcher ready.
- Options Creator startup (cache hot): pre-populate cache, then time from start to Options Creator ready.

Run with: cd test/benchmark && python startup.py
"""
from __future__ import annotations

import os
import re
import subprocess
import sys
import time

BENCHMARK_TIMEOUT_S = 120


def _clear_cache() -> None:
    """Remove the world list cache file so the next process sees a cold cache."""
    import worlds.world_list_cache as wlc

    path = wlc.get_cache_path()
    if os.path.isfile(path):
        os.remove(path)


def _warm_cache() -> None:
    """Build and write the world list cache so the next process sees a hot cache."""
    import worlds.world_list_cache as wlc

    wlc.get_world_list(force_rebuild=True)


def _run_timed_import(cwd: str, module_name: str, label: str) -> tuple[float | None, str]:
    """Run script that starts timer, imports module, prints 'label X.XXXX'. Return (seconds or None, error)."""
    script = f"""
import time
import sys
sys.path.insert(0, ".")
t0 = time.perf_counter()
__import__("{module_name}")
t1 = time.perf_counter()
print("{label}", t1 - t0)
"""
    try:
        proc = subprocess.Popen(
            [sys.executable, "-c", script],
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        out, _ = proc.communicate(timeout=BENCHMARK_TIMEOUT_S)
        match = re.search(rf"{re.escape(label)}\s+([\d.]+)", out or "")
        if match:
            return (float(match.group(1)), "")
        return (None, out or "no output")
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        return (None, "timeout")
    except Exception as e:
        return (None, str(e))


def run_startup_benchmark() -> None:
    """Run four startup timings: Launcher/Options Creator each with cache cold then hot."""
    from path_change import change_home

    change_home()
    repo_root = os.getcwd()

    results: list[tuple[str, float | None, str]] = []

    # 1. Launcher startup when cache is cold: clear cache, then time import
    _clear_cache()
    elapsed, err = _run_timed_import(repo_root, "Launcher", "launcher_cold")
    results.append(("Launcher startup (cache cold)", elapsed, err))

    # 2. Options Creator startup when cache is cold: clear cache, then time import
    _clear_cache()
    elapsed, err = _run_timed_import(repo_root, "OptionsCreator", "options_cold")
    results.append(("Options Creator startup (cache cold)", elapsed, err))

    # 3. Launcher startup when cache is hot: pre-populate cache, then time import
    _warm_cache()
    elapsed, err = _run_timed_import(repo_root, "Launcher", "launcher_hot")
    results.append(("Launcher startup (cache hot)", elapsed, err))

    # 4. Options Creator startup when cache is hot: cache already warm from previous step
    elapsed, err = _run_timed_import(repo_root, "OptionsCreator", "options_hot")
    results.append(("Options Creator startup (cache hot)", elapsed, err))

    # Summary (use 4 decimal places so sub-second times are visible)
    for name, secs, err in results:
        if secs is not None:
            print(f"{name}: {secs:.4f}s")
        else:
            print(f"{name}: (failed: {err})")


if __name__ == "__main__":
    run_startup_benchmark()
