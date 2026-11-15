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

# Dynamically register everything currently in the mods folder. This would ideally be done through a metaclass, but I have not looked into that yet.
mod_modules = pkgutil.iter_modules(mods.__path__)

loaded_modules = {}
for mod_module in mod_modules:
    module_name = mod_module.name
    module = importlib.import_module("." + module_name, mods.__name__)
    loaded_modules[module_name] = module

vanilla_content_pack_names = frozenset({
    base_game.name,
    ginger_island_content_pack.name,
    pelican_town.name,
    qi_board_content_pack.name,
    the_desert.name,
    the_farm.name,
    the_mines.name
})
all_content_pack_names = vanilla_content_pack_names | frozenset(by_mod.keys())
