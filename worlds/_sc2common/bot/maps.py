from __future__ import annotations

from pathlib import Path

from worlds._sc2common.bot import logger

from .paths import Paths


def get(name: str) -> Map:
    for map_dir in (p for p in Paths.MAPS.iterdir()):
        map = find_map_in_dir(name, map_dir)
        if map is not None:
            return map

    raise KeyError(f"Map '{name}' was not found. Please put the map file in \"/StarCraft II/Maps/\".")


# Go deeper
def find_map_in_dir(name, path):
    if Map.matches_target_map_name(path, name):
        return Map(path)

    if path.name.endswith("SC2Map"):
        return None

    if path.is_dir():
        for childPath in (p for p in path.iterdir()):
            map = find_map_in_dir(name, childPath)
            if map is not None:
                return map

    return None


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
