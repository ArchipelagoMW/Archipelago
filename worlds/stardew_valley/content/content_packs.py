import importlib
import os
import pathlib

from . import mods
from .mod_registry import by_mod
from .vanilla.base import base_game
from .vanilla.ginger_island import ginger_island
from .vanilla.pelican_town import pelican_town

assert base_game
assert ginger_island
assert pelican_town

# Dynamically register everything currently in the mods folder. This would ideally be done through a metaclass, but I have not looked into that yet.
mod_folder = pathlib.Path(next(iter(mods.__path__)))
module_files = [f for f in os.listdir(mod_folder) if f.endswith('.py')]

loaded_modules = {}
for file_name in module_files:
    module_name = file_name[:-3]
    module = importlib.import_module("." + module_name, mods.__name__)
    loaded_modules[module_name] = module

assert by_mod
