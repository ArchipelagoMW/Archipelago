"""Outputs a Factorio Mod to facilitate integration with Archipelago"""

import os
import zipfile
from typing import Optional
import threading
import json

import jinja2
import Utils
import shutil
import Options
from BaseClasses import MultiWorld
from .Technologies import tech_table

template: Optional[jinja2.Template] = None
locale_template: Optional[jinja2.Template] = None
control_template: Optional[jinja2.Template] = None

template_load_lock = threading.Lock()

base_info = {
    "version": Utils.__version__,
    "title": "Archipelago",
    "author": "Berserker",
    "homepage": "https://archipelago.gg",
    "description": "Integration client for the Archipelago Randomizer",
    "factorio_version": "1.1"
}

# TODO: clean this up, probably as a jinja macro; then add logic for the recipes in completion condition
rocket_recipes = {
    Options.MaxSciencePack.option_space_science_pack:
        '{{"rocket-control-unit", 10}, {"low-density-structure", 10}, {"rocket-fuel", 10}}',
    Options.MaxSciencePack.option_utility_science_pack:
        '{{"speed-module", 10}, {"steel-plate", 10}, {"solid-fuel", 10}}',
    Options.MaxSciencePack.option_production_science_pack:
        '{{"speed-module", 10}, {"steel-plate", 10}, {"solid-fuel", 10}}',
    Options.MaxSciencePack.option_chemical_science_pack:
        '{{"advanced-circuit", 10}, {"steel-plate", 10}, {"solid-fuel", 10}}',
    Options.MaxSciencePack.option_military_science_pack:
        '{{"defender-capsule", 10}, {"stone-wall", 10}, {"coal", 10}}',
    Options.MaxSciencePack.option_logistic_science_pack:
        '{{"electronic-circuit", 10}, {"stone-brick", 10}, {"coal", 10}}',
    Options.MaxSciencePack.option_automation_science_pack:
        '{{"copper-cable", 10}, {"iron-plate", 10}, {"wood", 10}}'
}

def generate_mod(world: MultiWorld, player: int):
    global template, locale_template, control_template
    with template_load_lock:
        if not template:
            mod_template_folder = Utils.local_path("data", "factorio", "mod_template")
            template = jinja2.Template(open(os.path.join(mod_template_folder, "data-final-fixes.lua")).read())
            locale_template = jinja2.Template(open(os.path.join(mod_template_folder, "locale", "en", "locale.cfg")).read())
            control_template = jinja2.Template(open(os.path.join(mod_template_folder, "control.lua")).read())
    # get data for templates
    player_names = {x: world.player_names[x][0] for x in world.player_ids}
    locations = []
    for location in world.get_filled_locations(player):
        locations.append((location.name, location.item.name, location.item.player))
    mod_name = f"AP-{world.seed_name}-P{player}-{world.player_names[player][0]}"
    tech_cost = {0: 0.1,
                 1: 0.25,
                 2: 0.5,
                 3: 1,
                 4: 2,
                 5: 5,
                 6: 10}[world.tech_cost[player].value]
    template_data = {"locations": locations, "player_names" : player_names, "tech_table": tech_table,
                     "mod_name": mod_name, "allowed_science_packs": world.max_science_pack[player].get_allowed_packs(),
                     "tech_cost_scale": tech_cost, "custom_data": world.custom_data[player],
                     "tech_tree_layout_prerequisites": world.tech_tree_layout_prerequisites[player],
                     "rocket_recipe" : rocket_recipes[world.max_science_pack[player].value],
                     "slot_name": world.player_names[player][0], "seed_name": world.seed_name,
                     "starting_items": world.starting_items[player]}

    for factorio_option in Options.factorio_options:
        template_data[factorio_option] = getattr(world, factorio_option)[player].value

    control_code = control_template.render(**template_data)
    data_final_fixes_code = template.render(**template_data)

    mod_dir = Utils.output_path(mod_name)+"_"+Utils.__version__
    en_locale_dir = os.path.join(mod_dir, "locale", "en")
    os.makedirs(en_locale_dir, exist_ok=True)
    shutil.copytree(Utils.local_path("data", "factorio", "mod"), mod_dir, dirs_exist_ok=True)
    with open(os.path.join(mod_dir, "data-final-fixes.lua"), "wt") as f:
        f.write(data_final_fixes_code)
        with open(os.path.join(mod_dir, "control.lua"), "wt") as f:
            f.write(control_code)
    locale_content = locale_template.render(**template_data)
    with open(os.path.join(en_locale_dir, "locale.cfg"), "wt") as f:
        f.write(locale_content)
    info = base_info.copy()
    info["name"] = mod_name
    with open(os.path.join(mod_dir, "info.json"), "wt") as f:
        json.dump(info, f, indent=4)

    # zip the result
    zf_path = os.path.join(mod_dir+".zip")
    with zipfile.ZipFile(zf_path, compression=zipfile.ZIP_DEFLATED, mode='w') as zf:
        for root, dirs, files in os.walk(mod_dir):
            for file in files:
                zf.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(mod_dir, '..')))
    shutil.rmtree(mod_dir)

