from __future__ import annotations

from pathlib import Path

from loguru import logger

from sc2.paths import Paths


def get(name: str) -> Map:
    # Iterate through 2 folder depths
    for map_dir in (p for p in Paths.MAPS.iterdir()):
        if map_dir.is_dir():
            for map_file in (p for p in map_dir.iterdir()):
                if Map.matches_target_map_name(map_file, name):
                    return Map(map_file)
        elif Map.matches_target_map_name(map_dir, name):
            return Map(map_dir)

    raise KeyError(f"Map '{name}' was not found. Please put the map file in \"/StarCraft II/Maps/\".")


class Map:

    def __init__(self, path: Path):
        self.path = path

        if self.path.is_absolute():
            try:
                self.relative_path = self.path.relative_to(Paths.MAPS)
            except ValueError:  # path not relative to basedir
                logger.warning(f"Using absolute path: {self.path}")
                self.relative_path = self.path
        else:
            self.relative_path = self.path

    @property
    def name(self):
        return self.path.stem

    @property
    def data(self):
        with open(self.path, "rb") as f:
            return f.read()

    def __repr__(self):
        return f"Map({self.path})"

    @classmethod
    def is_map_file(cls, file: Path) -> bool:
        return file.is_file() and file.suffix == ".SC2Map"

    @classmethod
    def matches_target_map_name(cls, file: Path, name: str) -> bool:
        return cls.is_map_file(file) and file.stem == name
