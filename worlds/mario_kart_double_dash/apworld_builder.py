from fnmatch import fnmatch
import os
from pathlib import Path
import zipfile

def build_apworld(world_name: str, ignore: list[str] = ["*__pycache__/*", "*.gitignore"], directory: str = "worlds"):
    world_directory = Path(directory, world_name)
    with zipfile.ZipFile(f"output/{world_name}.apworld", "w", zipfile.ZIP_DEFLATED, compresslevel = 9) as zf:
        paths = world_directory.rglob("*.*")
        for path in paths:
            include = True
            for i in ignore:
                if fnmatch(path, i):
                    include = False
                    break
            if include:
                relative_path = os.path.join(*path.parts[path.parts.index(directory) + 1:])
                zf.write(path, relative_path)

build_apworld("mario_kart_double_dash",
              [
                  "*__pycache__/*",
                  "*.ignore/*",
                  "*asm/*",
                  "*.yaml",
                  "*.gitignore",
              ])
