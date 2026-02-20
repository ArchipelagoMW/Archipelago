"""Low-level, internal world registry and cache-backed world access.

This module intentionally owns the implementation details for world lifecycle
operations (load, unload, lookup, cache-backed metadata reads). APWorld authors
should prefer the high-level `AutoWorldRegister` facade instead of importing
or mutating internals in this module directly.
"""
from __future__ import annotations

import dataclasses
import importlib
import io
import logging
import os
import time
import traceback
from collections.abc import Iterator, MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, TypedDict, cast

from NetUtils import DataPackage, GamesPackage
from Utils import Version

from . import apworld_loader
from . import world_list_cache


class WorldListEntry(TypedDict, total=False):
    """Internal shape of world-list cache entries consumed by the registry."""

    path: str
    is_zip: bool
    game: str


WorldType = type["World"]
WorldDataPackage = GamesPackage

# Backing storage for loaded world classes.
_world_types_storage: dict[str, WorldType] = {}


class _WorldTypesMapping(MutableMapping[str, WorldType]):
    """Internal world mapping with lazy-load semantics.

    This mapping mirrors legacy `AutoWorldRegister.world_types` behavior while
    routing all world loading and registration through `WorldRegistry`.
    """

    @staticmethod
    def _ensure_all_loaded() -> None:
        """Ensure all known worlds are loaded before full-map operations."""
        get_registry().load_all()

    def __getitem__(self, game_name: str) -> WorldType:
        """Return a loaded world class, loading from cache metadata if needed."""
        world = _world_types_storage.get(game_name)
        if world is not None:
            return world
        return get_registry().get_world_class(game_name)

    def __setitem__(self, game_name: str, world_type: WorldType) -> None:
        """Register a world class under a specific game name."""
        get_registry().register_world_internal(world_type, game_name=game_name)

    def __delitem__(self, game_name: str) -> None:
        """Unregister a world class by game name."""
        if game_name not in _world_types_storage:
            raise KeyError(game_name)
        get_registry().unregister_world_internal(game_name)

    def __iter__(self) -> Iterator[str]:
        """Iterate game names, ensuring all cache-listed worlds are loaded."""
        self._ensure_all_loaded()
        return iter(_world_types_storage)

    def __len__(self) -> int:
        """Return count of loaded worlds after loading all known entries."""
        self._ensure_all_loaded()
        return len(_world_types_storage)

    def __contains__(self, game_name: object) -> bool:
        """Return whether a game is loaded or known by cache metadata."""
        if not isinstance(game_name, str):
            return False
        if game_name in _world_types_storage:
            return True
        return world_list_cache.get_entry_by_game(game_name) is not None

    def get(self, game_name: str, default: WorldType | None = None) -> WorldType | None:
        """Return world class for game_name, or default if unavailable."""
        try:
            return self[game_name]
        except KeyError:
            return default

    def copy(self) -> dict[str, WorldType]:
        """Return a shallow copy after loading all known worlds."""
        self._ensure_all_loaded()
        return _world_types_storage.copy()


_world_types_mapping = _WorldTypesMapping()


@dataclasses.dataclass(order=True)
class WorldSource:
    """A single cached world source entry (folder module or .apworld zip)."""

    path: str
    is_zip: bool = False
    time_taken: float = -1.0
    version: Version = Version(0, 0, 0)

    def __repr__(self) -> str:
        """Return a short debug representation for logging and diagnostics."""
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip})"

    @property
    def resolved_path(self) -> str:
        """Return this source path as resolved by cache metadata."""
        return self.path

    def load(self, failed_loads: list[str]) -> bool:
        """Load this world source and append failures to failed_loads.

        Returns True when the source is imported successfully.
        """
        start = time.perf_counter()
        try:
            if self.is_zip:
                result = apworld_loader.load_apworld_by_path(self.path, failed_loads)
            else:
                importlib.import_module(f".{Path(self.path).stem}", "worlds")
                result = True
            self.time_taken = time.perf_counter() - start
            return result
        except Exception:
            file_like = io.StringIO()
            print(f"Could not load world {self}:", file=file_like)
            traceback.print_exc(file=file_like)
            file_like.seek(0)
            logging.exception(file_like.read())
            failed_loads.append(os.path.basename(self.path).rsplit(".", 1)[0])
            return False


class _GamesDataMapping(MutableMapping[str, WorldDataPackage]):
    """Lazy mapping from game name to per-game data package payload."""

    def __init__(self, registry: WorldRegistry) -> None:
        """Bind this mapping to a specific registry instance."""
        self._registry = registry

    def __getitem__(self, game_name: str) -> WorldDataPackage:
        """Return a game package, loading world class and caching on demand."""
        cache = self._registry._data_package_cache
        pkg = cache.get(game_name)
        if pkg is not None:
            return pkg
        cls = self._registry.get_world_class(game_name)
        pkg = cls.get_data_package_data()
        cache[game_name] = pkg
        return pkg

    def __setitem__(self, game_name: str, value: WorldDataPackage) -> None:
        """Store a package override after ensuring the world exists/loads."""
        self._registry.get_world_class(game_name)
        self._registry._data_package_cache[game_name] = value

    def __delitem__(self, game_name: str) -> None:
        """Disallow deletes to keep package view stable and cache-backed."""
        raise NotImplementedError("cannot delete from games dict")

    def __iter__(self) -> Iterator[str]:
        """Iterate game names from the registry's full world set."""
        return iter(self._registry.get_all_worlds())

    def __len__(self) -> int:
        """Return number of games available through the registry."""
        return len(self._registry.get_all_worlds())

    def __contains__(self, key: object) -> bool:
        """Return whether key is a valid game name in cache or world list."""
        if not isinstance(key, str):
            return False
        if key in self._registry._data_package_cache:
            return True
        if key in _world_types_storage:
            return True
        return world_list_cache.get_entry_by_game(key) is not None


class _NetworkDataPackageView:
    """Minimal DataPackage-like object backed by registry-owned game mapping."""

    def __init__(self, registry: WorldRegistry) -> None:
        """Initialize a lazy view over registry-provided game package data."""
        self._registry = registry
        self._games: _GamesDataMapping | None = None

    @property
    def _games_mapping(self) -> _GamesDataMapping:
        """Return the lazily-created games mapping."""
        if self._games is None:
            self._games = _GamesDataMapping(self._registry)
        return self._games

    def __getitem__(self, key: str) -> _GamesDataMapping:
        """Return the 'games' mapping for DataPackage-style access."""
        if key == "games":
            return self._games_mapping
        raise KeyError(key)

    def get(self, key: str, default: object = None) -> _GamesDataMapping | object:
        """Return key value or default, mirroring dict-like get semantics."""
        try:
            return self[key]
        except KeyError:
            return default


class WorldRegistry:
    """Internal owner for world loading, registration, and cache-backed access.

    This class is intentionally low-level. Callers should generally go through
    `AutoWorldRegister` for public, APWorld-facing interactions.
    """

    def __init__(self) -> None:
        """Initialize registry state and bootstrap world source cache view."""
        self.failed_world_loads: list[str] = []
        self._world_sources: list[WorldSource] = []
        self._data_package_cache: dict[str, WorldDataPackage] = {}
        self._ensuring_all_loaded: bool = False
        self._network_data_package: _NetworkDataPackageView | None = None
        # settings_key -> game (from world list); None = need rebuild. Cleared when world list cache is written.
        self._settings_key_to_game: dict[str, str] | None = None
        # settings_key -> World class; cleared per-game on unload so we don't hold stale refs.
        self._settings_key_to_world_class: dict[str, WorldType] = {}
        world_list_cache.register_on_cache_written(self._data_package_cache.clear)
        world_list_cache.register_on_cache_written(self._clear_settings_key_caches)
        self._refresh_world_sources()

    def _clear_settings_key_caches(self) -> None:
        """Clear settings_key caches so they are rebuilt from world list. Called when world list cache is written."""
        self._settings_key_to_game = None
        self._settings_key_to_world_class.clear()

    def _build_settings_key_map(self) -> None:
        """Populate _settings_key_to_game from world list entries."""
        if self._settings_key_to_game is not None:
            return
        self._settings_key_to_game = {}
        for entry in self.list_entries():
            game = entry.get("game")
            sk = entry.get("settings_key")
            if game and sk:
                self._settings_key_to_game[sk] = game

    def get_settings_keys(self) -> list[str]:
        """Return list of settings_key values from the world list (for host.yaml world sections)."""
        self._build_settings_key_map()
        assert self._settings_key_to_game is not None
        return list(self._settings_key_to_game)

    def get_world_class_for_settings_key(self, settings_key: str) -> WorldType | None:
        """Return World class for this settings_key, loading on demand. None if not found or load failed."""
        if settings_key in self._settings_key_to_world_class:
            return self._settings_key_to_world_class[settings_key]
        self._build_settings_key_map()
        assert self._settings_key_to_game is not None
        game = self._settings_key_to_game.get(settings_key)
        if not game:
            # Canonical key (e.g. apquest.world_options) may not be in cache; resolve by loading worlds
            for path_derived_key in list(self._settings_key_to_game):
                world = self.get_world_class_for_settings_key(path_derived_key)
                if world is not None and getattr(world, "settings_key", None) == settings_key:
                    self._settings_key_to_game[settings_key] = self._settings_key_to_game[path_derived_key]
                    return world
            return None
        try:
            world = self.get_world_class(game)
        except KeyError:
            return None
        # Cache under both path-derived key and world.settings_key so both resolve to same class
        self._settings_key_to_world_class[world.settings_key] = world
        self._settings_key_to_world_class[settings_key] = world
        # Expose canonical key so get_settings_keys() includes it (YAML/dump use canonical key)
        if world.settings_key not in self._settings_key_to_game:
            self._settings_key_to_game[world.settings_key] = game
        return world

    def _world_sources_from_cache(self, entries: list[WorldListEntry]) -> list[WorldSource]:
        """Convert cached world-list entries into WorldSource objects."""
        return [
            WorldSource(path=entry["path"], is_zip=entry.get("is_zip", False))
            for entry in entries
        ]

    def _refresh_world_sources(self) -> None:
        """Refresh in-memory world source list from cache metadata."""
        entries = cast(list[WorldListEntry], world_list_cache.get_world_list())
        self._world_sources.clear()
        self._world_sources.extend(self._world_sources_from_cache(entries))

    @property
    def world_sources(self) -> list[WorldSource]:
        """Return in-memory world source descriptors."""
        return self._world_sources

    def list_entries(self, force_rebuild: bool = False) -> list[WorldListEntry]:
        """Return world-list cache entries, optionally forcing a cache rebuild."""
        entries = cast(list[WorldListEntry], world_list_cache.get_world_list(force_rebuild=force_rebuild))
        if force_rebuild:
            self._refresh_world_sources()
        return entries

    def add_world_to_cache(self, apworld_path: str) -> bool:
        """Add one .apworld path to cache and refresh source tracking."""
        if not world_list_cache.add_world_to_cache(apworld_path):
            return False
        self._refresh_world_sources()
        return True

    def get_entry_by_path(self, path: str) -> WorldListEntry | None:
        """Return cache entry matching path, or None if absent."""
        return cast(WorldListEntry | None, world_list_cache.get_entry_by_path(path))

    def get_entry_by_game(self, game_name: str) -> WorldListEntry | None:
        """Return cache entry for the given game name, or None. O(1) after first list_entries()."""
        return cast(WorldListEntry | None, world_list_cache.get_entry_by_game(game_name))

    def register_world_internal(self, world_class: WorldType, game_name: str | None = None) -> None:
        """Register a world class in internal storage.

        Raises RuntimeError on duplicate game name to preserve existing behavior.
        """
        game_name = game_name or world_class.game
        if game_name in _world_types_storage:
            raise RuntimeError(
                f"""Game {game_name} already registered in
                {_world_types_storage[game_name].__file__} when attempting to register from
                {world_class.__file__}."""
            )
        _world_types_storage[game_name] = world_class

    def unregister_world_internal(self, game_name: str) -> None:
        """Remove a world class from internal storage if present."""
        _world_types_storage.pop(game_name, None)

    def unload_world(self, game_name: str) -> None:
        """Unload one world class and forget its module import state.

        This is a no-op when game_name is not currently loaded.
        """
        if game_name not in _world_types_storage:
            return
        cls = _world_types_storage[game_name]
        module_name = cls.__module__
        self.unregister_world_internal(game_name)
        self.clear_data_package_cache(game_name)
        apworld_loader.forget_module(module_name)
        # Clear settings_key cache for this game so we don't hold a stale World class ref
        self._settings_key_to_world_class = {
            k: v for k, v in self._settings_key_to_world_class.items()
            if getattr(v, "game", None) != game_name
        }

    def clear_data_package_cache(self, game_name: str) -> None:
        """Remove cached data package for game_name so next access refetches. Used by tests."""
        self._data_package_cache.pop(game_name, None)

    def _load_entry(self, entry: WorldListEntry) -> bool:
        """Load one cache entry by matching it to a tracked world source."""
        path = entry["path"]
        for world_source in self._world_sources:
            if os.path.normpath(world_source.path) == os.path.normpath(path):
                return world_source.load(self.failed_world_loads)
        return False

    def get_loaded_world(self, game_name: str) -> WorldType | None:
        """Return a loaded world class, without triggering load."""
        return _world_types_storage.get(game_name)

    def get_world_class(self, game_name: str) -> WorldType:
        """Return world class for game_name, loading from cache when needed."""
        if game_name in _world_types_storage:
            return _world_types_storage[game_name]
        entry = cast(WorldListEntry | None, world_list_cache.get_entry_by_game(game_name))
        if entry is None:
            raise KeyError(f"World '{game_name}' not found in cache or failed to load.")
        self._load_entry(entry)
        if game_name in _world_types_storage:
            return _world_types_storage[game_name]
        raise KeyError(f"World '{game_name}' not found in cache or failed to load.")

    def load_all(self) -> None:
        """Load all worlds currently known by the world-list cache."""
        if self._ensuring_all_loaded:
            return
        self._ensuring_all_loaded = True
        try:
            entries = self.list_entries()
            for entry in entries:
                game = entry.get("game")
                if isinstance(game, str) and self.get_loaded_world(game) is None:
                    self._load_entry(entry)
        finally:
            self._ensuring_all_loaded = False

    def get_all_worlds(self) -> dict[str, WorldType]:
        """Return the loaded world map after ensuring full cache coverage."""
        self.load_all()
        return _world_types_storage

    @property
    def network_data_package(self) -> DataPackage:
        """Return a DataPackage-compatible view backed by lazy game mapping."""
        if self._network_data_package is None:
            self._network_data_package = _NetworkDataPackageView(self)
        return cast(DataPackage, self._network_data_package)


_registry: WorldRegistry | None = None


def get_registry() -> WorldRegistry:
    """Return process-global registry singleton."""
    global _registry
    if _registry is None:
        _registry = WorldRegistry()
    return _registry
