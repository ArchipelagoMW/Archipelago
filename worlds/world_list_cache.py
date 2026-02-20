"""
World list cache: persist path + mtime and manifest-derived fields so we can list
worlds without loading them. Used by Options Creator and other list-only consumers.
"""
from __future__ import annotations

import json
import os
import zipfile
from typing import Any

from Utils import cache_path, local_path, user_path, version_tuple

CACHE_FILENAME = "worlds_cache.json"
CACHE_FORMAT_VERSION = 1


def _path_to_settings_key(path: str, is_zip: bool) -> str:
    """Path-derived key for host.yaml world options (stem.lower() + '_options')."""
    if is_zip:
        stem = os.path.splitext(os.path.basename(path))[0]
    else:
        stem = os.path.basename(path.rstrip(os.sep))
    return stem.lower() + "_options"


def get_cache_path() -> str:
    return cache_path(CACHE_FILENAME)


def read_cache() -> list[dict[str, Any]] | None:
    path = get_cache_path()
    if not os.path.isfile(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
    if not isinstance(data, dict):
        return None
    if data.get("format_version") != CACHE_FORMAT_VERSION:
        return None
    entries = data.get("entries")
    if not isinstance(entries, list):
        return None
    return entries


def _read_manifest_from_zip(zip_path: str) -> dict[str, Any] | None:
    """Read archipelago.json from an apworld zip. Returns manifest dict or None if not found."""
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            manifest_path = None
            for info in zf.infolist():
                if info.filename.endswith("archipelago.json"):
                    manifest_path = info.filename
                    break
            if manifest_path is None:
                return None
            with zf.open(manifest_path, "r") as f:
                return json.load(f)
    except (zipfile.BadZipFile, OSError, json.JSONDecodeError):
        return None


def _read_manifest_from_folder(manifest_full_path: str) -> dict[str, Any] | None:
    """Read archipelago.json from a file path."""
    try:
        with open(manifest_full_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _folders_to_scan(
    local_folder_path: str, user_folder_path: str | None
) -> list[tuple[str, bool]]:
    folders: list[tuple[str, bool]] = []
    if local_folder_path:
        folders.append((local_folder_path, True))
    if user_folder_path and user_folder_path != local_folder_path:
        folders.append((user_folder_path, False))
    return folders


def build_cache(local_folder_path: str, user_folder_path: str | None) -> list[dict[str, Any]]:
    """Full scan: no cache reuse. Use when cache is missing or force_rebuild."""
    return _scan_worlds(local_folder_path, user_folder_path, cache_by_path=None)


def _scan_worlds(
    local_folder_path: str,
    user_folder_path: str | None,
    cache_by_path: dict[str, dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    """Single scan over world folders. For each path found: reuse cache entry if mtime matches and
    not always_reload; otherwise read manifest and build entry. New paths (not in cache) always
    get a manifest read. Returns full list (existing + new), so new items are always picked up."""
    entries: list[dict[str, Any]] = []
    folders_to_scan = _folders_to_scan(local_folder_path, user_folder_path)

    for folder_path, _ in folders_to_scan:
        if not os.path.isdir(folder_path):
            continue
        for dirpath, _dirnames, filenames in os.walk(folder_path):
            for fname in filenames:
                if fname.endswith("archipelago.json"):
                    manifest_path = os.path.join(dirpath, fname)
                    world_root = dirpath
                    init_py = os.path.join(world_root, "__init__.py")
                    if not os.path.isfile(init_py):
                        continue
                    try:
                        mtime = os.stat(world_root).st_mtime
                    except OSError:
                        mtime = 0.0
                    key = os.path.normpath(os.path.abspath(world_root))
                    entry = _entry_for_path(
                        world_root, False, mtime, manifest_path, cache_by_path, key
                    )
                    if entry is not None:
                        entries.append(entry)
                    break  # one manifest per dir

    for folder_path, _ in folders_to_scan:
        if not os.path.isdir(folder_path):
            continue
        try:
            for entry_obj in os.scandir(folder_path):
                if not entry_obj.is_file() or not entry_obj.name.endswith(".apworld"):
                    continue
                apworld_path = entry_obj.path
                try:
                    mtime = entry_obj.stat().st_mtime
                except OSError:
                    mtime = 0.0
                key = os.path.normpath(os.path.abspath(apworld_path))
                entry = _entry_for_path(apworld_path, True, mtime, None, cache_by_path, key)
                if entry is not None:
                    entries.append(entry)
        except OSError:
            continue

    return entries


def _entry_for_path(
    path: str,
    is_zip: bool,
    mtime: float,
    manifest_path: str | None,
    cache_by_path: dict[str, dict[str, Any]] | None,
    key: str,
) -> dict[str, Any] | None:
    """Return cache entry to use, or build from manifest. Reuses cache only if mtime matches and not always_reload."""
    if cache_by_path is not None and key in cache_by_path:
        cached = cache_by_path[key]
        if not cached.get("always_reload") and cached.get("mtime") == mtime:
            return cached
    if is_zip:
        manifest = _read_manifest_from_zip(path)
    else:
        manifest_path = manifest_path or os.path.join(path, "archipelago.json")
        if not os.path.isfile(manifest_path):
            for _dirpath, _dirnames, filenames in os.walk(path):
                for fname in filenames:
                    if fname.endswith("archipelago.json"):
                        manifest_path = os.path.join(_dirpath, fname)
                        break
                break
        manifest = _read_manifest_from_folder(manifest_path) if os.path.isfile(manifest_path) else None
    if not manifest or "game" not in manifest:
        return None
    return {
        "path": path,
        "mtime": mtime,
        "is_zip": is_zip,
        "game": manifest["game"],
        "world_version": manifest.get("world_version"),
        "manifest_path": manifest_path if not is_zip else None,
        "always_reload": manifest.get("always_reload", False),
        "settings_key": _path_to_settings_key(path, is_zip),
    }


def _refresh_entry(entry: dict[str, Any]) -> bool:
    """Re-read manifest for this entry and update mtime/path. Returns True if still valid."""
    path = entry.get("path")
    if not path or not os.path.exists(path):
        return False
    is_zip = entry.get("is_zip", False)
    if is_zip:
        manifest = _read_manifest_from_zip(path)
        try:
            entry["mtime"] = os.stat(path).st_mtime
        except OSError:
            pass
    else:
        manifest_path = entry.get("manifest_path") or os.path.join(path, "archipelago.json")
        if not os.path.isfile(manifest_path):
            for _dirpath, _dirnames, filenames in os.walk(path):
                for fname in filenames:
                    if fname.endswith("archipelago.json"):
                        manifest_path = os.path.join(_dirpath, fname)
                        break
                break
        manifest = _read_manifest_from_folder(manifest_path) if os.path.isfile(manifest_path) else None
        try:
            entry["mtime"] = os.stat(path).st_mtime
        except OSError:
            pass
    if manifest and "game" in manifest:
        entry["game"] = manifest["game"]
        entry["world_version"] = manifest.get("world_version")
        entry["always_reload"] = manifest.get("always_reload", False)
        entry["settings_key"] = _path_to_settings_key(path, is_zip)
        return True
    return True  # keep entry with existing game if manifest read failed


def refresh_entries_in_place(
    entries: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    """Update entries that need refresh (missing path dropped; always_reload or mtime mismatch refreshed).
    Returns (valid_entries, changed): valid_entries are path-exists and refreshed in place where needed;
    changed is True if we dropped any entry or refreshed any entry (so caller should merge new items and write)."""
    result: list[dict[str, Any]] = []
    changed = False
    for entry in entries:
        path = entry.get("path")
        if not path or not os.path.exists(path):
            changed = True
            continue
        if entry.get("always_reload"):
            _refresh_entry(entry)
            changed = True
        else:
            try:
                if os.stat(path).st_mtime != entry.get("mtime"):
                    _refresh_entry(entry)
                    changed = True
            except OSError:
                changed = True
                continue
        result.append(entry)
    return result, changed


def _merge_new_entries(
    existing: list[dict[str, Any]], built: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Return existing entries plus any entry in built whose path is not already in existing."""
    known = {os.path.normpath(os.path.abspath(e.get("path", ""))) for e in existing}
    merged = list(existing)
    for e in built:
        key = os.path.normpath(os.path.abspath(e.get("path", "")))
        if key not in known:
            merged.append(e)
            known.add(key)
    return merged


# In-memory index by game name for O(1) lookup; invalidated when cache is written
_cached_entries: list[dict[str, Any]] | None = None
_cached_by_game: dict[str, dict[str, Any]] | None = None


_on_cache_written_callbacks: list[object] = []  # list of callables; typed as object to avoid typing.Callable import


def register_on_cache_written(callback: object) -> None:
    """Register a callable to be invoked whenever the disk cache is written (rebuild or add_world_to_cache).
    Used by worlds to clear its in-memory world/data cache so it stays in sync with the list."""
    _on_cache_written_callbacks.append(callback)


def write_cache(entries: list[dict[str, Any]]) -> None:
    path = get_cache_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    data = {
        "format_version": CACHE_FORMAT_VERSION,
        "core_version": list(version_tuple) if version_tuple else None,
        "entries": entries,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    global _cached_entries, _cached_by_game
    _cached_entries = None
    _cached_by_game = None
    for cb in _on_cache_written_callbacks:
        cb()  # type: ignore[misc]


def _get_folder_paths() -> tuple[str, str | None]:
    """Return (local_folder_path, user_folder_path) matching get_world_list resolution."""
    local_folder_path = os.path.dirname(__file__)
    _base = user_path()
    if _base != local_path():
        user_folder_path = user_path("worlds")
    else:
        user_folder_path = user_path("custom_worlds")
    if not os.path.isdir(user_folder_path):
        user_folder_path = None
    return local_folder_path, user_folder_path


def add_world_to_cache(apworld_path: str) -> bool:
    """Add a single apworld to the cache by path. Idempotent if path already present. Returns False if manifest invalid."""
    if not os.path.isfile(apworld_path) or not apworld_path.endswith(".apworld"):
        return False
    local_folder_path, user_folder_path = _get_folder_paths()
    # Optional guard: only allow paths under known world folders
    allowed_dirs = [os.path.abspath(local_folder_path)]
    if user_folder_path:
        allowed_dirs.append(os.path.abspath(user_folder_path))
    apworld_abs = os.path.abspath(apworld_path)
    if not any(apworld_abs.startswith(d + os.sep) or apworld_abs == d for d in allowed_dirs):
        return False
    entries = get_world_list()
    if any(os.path.abspath(e.get("path", "")) == apworld_abs for e in entries):
        return True
    manifest = _read_manifest_from_zip(apworld_path)
    if manifest is None or "game" not in manifest:
        return False
    try:
        mtime = os.stat(apworld_path).st_mtime
    except OSError:
        mtime = 0.0
    cache_entry: dict[str, Any] = {
        "path": apworld_path,
        "mtime": mtime,
        "is_zip": True,
        "game": manifest["game"],
        "world_version": manifest.get("world_version"),
        "manifest_path": None,
        "always_reload": manifest.get("always_reload", False),
        "settings_key": _path_to_settings_key(apworld_path, True),
    }
    entries.append(cache_entry)
    write_cache(entries)
    return True


def get_world_list(force_rebuild: bool = False) -> list[dict[str, Any]]:
    """Return cache entries (path, game, is_zip, etc.). When the cache is loaded (first use, or
    after in-memory was cleared), we run one scan over world folders that reuses cache entries when
    mtime matches and not always_reload, and reads manifest for new paths or when mtime changed or
    always_reload — so new items are picked up. Repeated calls return the in-memory list without
    scanning."""
    global _cached_entries, _cached_by_game
    local_folder_path, user_folder_path = _get_folder_paths()
    if not force_rebuild and _cached_entries is not None:
        return _cached_entries
    if force_rebuild:
        entries = build_cache(local_folder_path, user_folder_path)
        write_cache(entries)
        _cached_entries = entries
        _cached_by_game = {e["game"]: e for e in entries if e.get("game")}
        return entries
    entries = read_cache()
    if entries is None:
        entries = build_cache(local_folder_path, user_folder_path)
        write_cache(entries)
        _cached_entries = entries
        _cached_by_game = {e["game"]: e for e in entries if e.get("game")}
        return entries
    cache_by_path = {
        os.path.normpath(os.path.abspath(e.get("path", ""))): e for e in entries
    }
    result = _scan_worlds(local_folder_path, user_folder_path, cache_by_path=cache_by_path)
    write_cache(result)
    _cached_entries = result
    _cached_by_game = {e["game"]: e for e in result if e.get("game")}
    return result


def get_entry_by_game(game_name: str) -> dict[str, Any] | None:
    """Return the cache entry for the given game name, or None. O(1) after first get_world_list()."""
    get_world_list()
    if _cached_by_game is None:
        return None
    return _cached_by_game.get(game_name)


def get_entry_by_path(path: str) -> dict[str, Any] | None:
    """Return the cache entry for the given world path (apworld file or folder), or None."""
    entries = get_world_list()
    if not entries:
        return None
    norm_path = os.path.normpath(os.path.abspath(path))
    for entry in entries:
        if os.path.normpath(os.path.abspath(entry.get("path", ""))) == norm_path:
            return entry
    return None
