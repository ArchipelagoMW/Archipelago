"""Outputs a Factorio Mod to facilitate integration with Archipelago"""

import os
from typing import Optional
import threading
import json

import jinja2
import Utils
import shutil
from BaseClasses import MultiWorld
from .Technologies import tech_table

template: Optional[jinja2.Template] = None
locale_template: Optional[jinja2.Template] = None

template_load_lock = threading.Lock()

base_info = {
    "version": Utils.__version__,
    "title": "Archipelago",
    "author": "Berserker",
    "homepage": "https://archipelago.gg",
    "description": "Integration client for the Archipelago Randomizer",
    "factorio_version": "1.1"
}

def generate_mod(world: MultiWorld, player: int):
    global template, locale_template
    with template_load_lock:
        if not template:
            template = jinja2.Template(open(Utils.local_path("data", "factorio", "mod_template", "data-final-fixes.lua")).read())
            locale_template = jinja2.Template(open(Utils.local_path("data", "factorio", "mod_template", "locale", "en", "locale.cfg")).read())
    # get data for templates
    player_names = {x: world.player_names[x][0] for x in world.player_ids}
    locations = []
    for location in world.get_filled_locations(player):
        if not location.name.startswith("recipe-"):  # introduce this a new location property?
            locations.append((location.name, location.item.name, location.item.player))
    mod_name = f"archipelago-client-{world.seed}-{player}"
    template_data = {"locations": locations, "player_names" : player_names, "tech_table": tech_table,
                     "mod_name": mod_name}

    mod_code = template.render(**template_data)

    mod_dir = Utils.output_path(mod_name)
    en_locale_dir = os.path.join(mod_dir, "locale", "en")
    os.makedirs(en_locale_dir, exist_ok=True)
    shutil.copytree(Utils.local_path("data", "factorio", "mod"), mod_dir, dirs_exist_ok=True)
    with open(os.path.join(mod_dir, "data-final-fixes.lua"), "wt") as f:
        f.write(mod_code)
    locale_content = locale_template.render(**template_data)
    with open(os.path.join(en_locale_dir, "locale.cfg"), "wt") as f:
        f.write(locale_content)
    info = base_info.copy()
    info["name"] = mod_name
    with open(os.path.join(mod_dir, "info.json"), "wt") as f:
        json.dump(info, f, indent=4)
