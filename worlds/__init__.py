from __future__ import annotations

import os
from typing import TYPE_CHECKING

from Utils import local_path, user_path

from . import world_list_cache
from .AutoWorld import AutoWorldRegister
from .registry import get_registry

if TYPE_CHECKING:
    from .AutoWorld import World

local_folder = os.path.dirname(__file__)
user_folder = user_path("worlds") if user_path() != local_path() else user_path("custom_worlds")
try:
    os.makedirs(user_folder, exist_ok=True)
except OSError:
    user_folder = None

_registry = get_registry()

__all__ = [
    "network_data_package",
    "AutoWorldRegister",
    "world_sources",
    "local_folder",
    "user_folder",
    "failed_world_loads",
    "get_world_list",
    "get_entry_by_path",
    "add_world_to_cache",
    "get_world_class",
    "get_loaded_world",
    "get_all_worlds",
    "ensure_world_loaded",
    "ensure_all_worlds_loaded",
    "unload_world",
]

# Registry-backed attributes
failed_world_loads = _registry.failed_world_loads
world_sources = _registry.world_sources
network_data_package = _registry.network_data_package


def get_world_list(force_rebuild: bool = False) -> list:
    """Return list of cache entries (dicts with game, path, is_zip, etc.). Cache is the source of truth;
    world_sources is the in-memory list refreshed from the cache when it changes."""
    return _registry.list_entries(force_rebuild=force_rebuild)


def get_entry_by_path(path: str):
    """Return the cache entry for the given world path (apworld file or folder), or None."""
    return world_list_cache.get_entry_by_path(path)


def unload_world(game_name: str) -> None:
    """Unload a world by game name so it can be loaded again (e.g. after updating an apworld). No-op if not loaded."""
    _registry.unload_world(game_name)


def add_world_to_cache(apworld_path: str) -> bool:
    """Add a single apworld to the cache and refresh world_sources. Returns False if path/manifest invalid."""
    return _registry.add_world_to_cache(apworld_path)


def get_world_class(game_name: str) -> type["World"]:
    """Return the World class for game_name; load it on demand if not yet loaded."""
    return _registry.get_world_class(game_name)


def get_loaded_world(game_name: str) -> type["World"] | None:
    """Return the World class for game_name if already loaded, else None. Does not load."""
    return _registry.get_loaded_world(game_name)


def get_all_worlds() -> dict[str, type["World"]]:
    """Ensure all worlds are loaded, then return the registry dict (game -> World class)."""
    return _registry.get_all_worlds()


def ensure_world_loaded(game_name: str) -> None:
    """Ensure the world for game_name is loaded; no return value."""
    _registry.get_world_class(game_name)


def ensure_all_worlds_loaded() -> None:
    """Load every world in the cache; used by MultiServer, Generate, etc."""
    _registry.load_all()
