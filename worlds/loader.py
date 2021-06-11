import importlib
import os
world_types = []
world_folder = os.path.dirname(__file__)
for entry in os.scandir(world_folder):
    if entry.is_dir():
        entryname = entry.name
        if not entryname.startswith("_"):
            world_module = importlib.import_module("."+entry.name, package="worlds")
            world_types.append(world_module)
print(world_folder)
print(world_types)