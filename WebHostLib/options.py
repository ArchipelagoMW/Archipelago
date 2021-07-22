import os
from Utils import __version__
from jinja2 import Template
import yaml

from worlds.AutoWorld import AutoWorldRegister

target_folder = os.path.join("WebHostLib", "static", "generated")

def create():
    for game_name, world in AutoWorldRegister.world_types.items():
        res = Template(open(os.path.join("WebHostLib", "templates", "options.yaml")).read()).render(
            options=world.options, __version__ = __version__, game=game_name, yaml_dump = yaml.dump
        )

        with open(os.path.join(target_folder, game_name+".yaml"), "w") as f:
            f.write(res)