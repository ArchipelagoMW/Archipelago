import importlib
import pkgutil

from . import mods
from .mod_registry import by_mod
from .vanilla.base import base_game
from .vanilla.ginger_island import ginger_island_content_pack
from .vanilla.pelican_town import pelican_town
from .vanilla.qi_board import qi_board_content_pack
from .vanilla.the_desert import the_desert
from .vanilla.the_farm import the_farm
from .vanilla.the_mines import the_mines

assert base_game
assert ginger_island_content_pack
assert pelican_town
assert qi_board_content_pack
assert the_desert
assert the_farm
assert the_mines

# Dynamically register everything currently in the mods folder. This would ideally be done through a metaclass, but I have not looked into that yet.
mod_modules = pkgutil.iter_modules(mods.__path__)

loaded_modules = {}
for mod_module in mod_modules:
    module_name = mod_module.name
    module = importlib.import_module("." + module_name, mods.__name__)
    loaded_modules[module_name] = module

assert by_mod
