"""
World registry: single facade for world list cache, loading, and data package.
"""
from __future__ import annotations

import dataclasses
import importlib
import io
import logging
import os
import time
import traceback
from collections.abc import MutableMapping
from pathlib import Path
from typing import TYPE_CHECKING, List

from NetUtils import DataPackage
from Utils import Version

from . import apworld_loader
from . import world_list_cache
from .AutoWorld import _world_types_storage, unregister_world as _unregister_world

if TYPE_CHECKING:
    from .AutoWorld import World


@dataclasses.dataclass(order=True)
class WorldSource:
    path: str
    is_zip: bool = False
    time_taken: float = -1.0
    version: Version = Version(0, 0, 0)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.path}, is_zip={self.is_zip})"

    @property
    def resolved_path(self) -> str:
        return self.path

    def load(self, failed_loads: List[str]) -> bool:
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


class _GamesDataMapping(MutableMapping[str, dict]):
    """Mapping from game name to data package dict. Keys/len from get_all_worlds; values loaded on demand."""

    def __init__(self, registry: WorldRegistry) -> None:
        self._registry = registry

    def __getitem__(self, game_name: str) -> dict:
        cache = self._registry._data_package_cache
        pkg = cache.get(game_name)
        if pkg is not None:
            return pkg
        cls = self._registry.get_world_class(game_name)
        pkg = cls.get_data_package_data()
        cache[game_name] = pkg
        return pkg

    def __setitem__(self, game_name: str, value: dict) -> None:
        self._registry.get_world_class(game_name)  # ensure world is loaded
        self._registry._data_package_cache[game_name] = value

    def __delitem__(self, game_name: str) -> None:
        raise NotImplementedError("cannot delete from games dict")

    def __iter__(self):
        return iter(self._registry.get_all_worlds())

    def __len__(self) -> int:
        return len(self._registry.get_all_worlds())

    def __contains__(self, key: str) -> bool:
        if key in self._registry._data_package_cache:
            return True
        if key in _world_types_storage:
            return True
        return world_list_cache.get_entry_by_game(key) is not None


class _NetworkDataPackageView:
    """DataPackage-like view with only 'games' key backed by registry's games mapping."""

    def __init__(self, registry: WorldRegistry) -> None:
        self._registry = registry
        self._games: _GamesDataMapping | None = None

    @property
    def _games_mapping(self) -> _GamesDataMapping:
        if self._games is None:
            self._games = _GamesDataMapping(self._registry)
        return self._games

    def __getitem__(self, key: str):
        if key == "games":
            return self._games_mapping
        raise KeyError(key)

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default


class WorldRegistry:
    """Single facade for world list cache, loading, and data package access."""

    def __init__(self) -> None:
        self.failed_world_loads: List[str] = []
        self._world_sources: List[WorldSource] = []
        self._data_package_cache: dict[str, dict | None] = {}
        self._ensuring_all_loaded = False
        self._network_data_package: _NetworkDataPackageView | None = None
        world_list_cache.register_on_cache_written(self._data_package_cache.clear)
        self._refresh_world_sources()

    def _world_sources_from_cache(self, entries: list) -> List[WorldSource]:
        return [
            WorldSource(path=entry["path"], is_zip=entry.get("is_zip", False))
            for entry in entries
        ]

    def _refresh_world_sources(self) -> None:
        entries = world_list_cache.get_world_list()
        self._world_sources.clear()
        self._world_sources.extend(self._world_sources_from_cache(entries))

    @property
    def world_sources(self) -> List[WorldSource]:
        return self._world_sources

    def list_entries(self, force_rebuild: bool = False) -> list:
        entries = world_list_cache.get_world_list(force_rebuild=force_rebuild)
        if force_rebuild:
            self._refresh_world_sources()
        return entries

    def add_world_to_cache(self, apworld_path: str) -> bool:
        if not world_list_cache.add_world_to_cache(apworld_path):
            return False
        self._refresh_world_sources()
        return True

    def unload_world(self, game_name: str) -> None:
        """Unload a world by game name so it can be loaded again (e.g. after updating an apworld).
        No-op if the game is not currently loaded."""
        if game_name not in _world_types_storage:
            return
        cls = _world_types_storage[game_name]
        module_name = cls.__module__
        _unregister_world(game_name)
        self._data_package_cache.pop(game_name, None)
        apworld_loader.forget_module(module_name)

    def _load_entry(self, entry: dict) -> bool:
        path = entry["path"]
        for ws in self._world_sources:
            if os.path.normpath(ws.path) == os.path.normpath(path):
                return ws.load(self.failed_world_loads)
        return False

    def get_loaded_world(self, game_name: str) -> type["World"] | None:
        """Return the World class for game_name if already loaded, else None. Does not load."""
        return _world_types_storage.get(game_name)

    def get_world_class(self, game_name: str) -> type["World"]:
        if game_name in _world_types_storage:
            return _world_types_storage[game_name]
        entry = world_list_cache.get_entry_by_game(game_name)
        if entry is None:
            raise KeyError(f"World '{game_name}' not found in cache or failed to load.")
        self._load_entry(entry)
        if game_name in _world_types_storage:
            return _world_types_storage[game_name]
        raise KeyError(f"World '{game_name}' not found in cache or failed to load.")

    def load_all(self) -> None:
        if self._ensuring_all_loaded:
            return
        self._ensuring_all_loaded = True
        try:
            entries = self.list_entries()
            for entry in entries:
                game = entry.get("game")
                if game and self.get_loaded_world(game) is None:
                    self._load_entry(entry)
        finally:
            self._ensuring_all_loaded = False

    def get_all_worlds(self) -> dict[str, type["World"]]:
        self.load_all()
        return _world_types_storage

    @property
    def network_data_package(self) -> DataPackage:  # type: ignore[valid-type]
        if self._network_data_package is None:
            self._network_data_package = _NetworkDataPackageView(self)
        return self._network_data_package  # type: ignore[return-value]


_registry: WorldRegistry | None = None


def get_registry() -> WorldRegistry:
    global _registry
    if _registry is None:
        _registry = WorldRegistry()
    return _registry
