"""Outputs a Factorio Mod to facilitate integration with Archipelago"""

import os
import zipfile
from typing import Optional
import threading
import json

import jinja2
import Utils
import shutil
from . import Options
from BaseClasses import MultiWorld
from .Technologies import tech_table, rocket_recipes, recipes, free_sample_blacklist, progressive_technology_table, \
    base_tech_table, tech_to_progressive_lookup, progressive_tech_table

template_env: Optional[jinja2.Environment] = None

data_template: Optional[jinja2.Template] = None
data_final_template: Optional[jinja2.Template] = None
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

recipe_time_scales = {
    # using random.triangular
    Options.RecipeTime.option_fast: (0.25, 1),
    # 0.5, 2, 0.5 average -> 1.0
    Options.RecipeTime.option_normal: (0.5, 2, 0.5),
    Options.RecipeTime.option_slow: (1, 4),
    # 0.25, 4, 0.25 average -> 1.5
    Options.RecipeTime.option_chaos: (0.25, 4, 0.25),
    Options.RecipeTime.option_vanilla: None
}

def generate_mod(world, output_directory: str):
    player = world.player
    multiworld = world.world
    global data_final_template, locale_template, control_template, data_template
    with template_load_lock:
        if not data_final_template:
            mod_template_folder = os.path.join(os.path.dirname(__file__), "data", "mod_template")
            template_env: Optional[jinja2.Environment] = \
                jinja2.Environment(loader=jinja2.FileSystemLoader([mod_template_folder]))
            data_template = template_env.get_template("data.lua")
            data_final_template = template_env.get_template("data-final-fixes.lua")
            locale_template = template_env.get_template(r"locale/en/locale.cfg")
            control_template = template_env.get_template("control.lua")
    # get data for templates
    player_names = {x: multiworld.player_name[x] for x in multiworld.player_ids}
    locations = []
    for location in multiworld.get_filled_locations(player):
        if location.address:
            locations.append((location.name, location.item.name, location.item.player, location.item.advancement))
    mod_name = f"AP-{multiworld.seed_name}-P{player}-{multiworld.player_name[player]}"
    tech_cost_scale = {0: 0.1,
                       1: 0.25,
                       2: 0.5,
                       3: 1,
                       4: 2,
                       5: 5,
                       6: 10}[multiworld.tech_cost[player].value]
    random = multiworld.slot_seeds[player]

    def flop_random(low, high, base=None):
        """Guarentees 50% below base and 50% above base, uniform distribution in each direction."""
        if base:
            distance = random.random()
            if random.randint(0, 1):
                return base + (high-base) * distance
            else:
                return base - (base-low) * distance
        return random.uniform(low, high)

    template_data = {"locations": locations, "player_names": player_names, "tech_table": tech_table,
                     "base_tech_table": base_tech_table, "tech_to_progressive_lookup": tech_to_progressive_lookup,
                     "mod_name": mod_name, "allowed_science_packs": multiworld.max_science_pack[player].get_allowed_packs(),
                     "tech_cost_scale": tech_cost_scale, "custom_technologies": multiworld.worlds[player].custom_technologies,
                     "tech_tree_layout_prerequisites": multiworld.tech_tree_layout_prerequisites[player],
                     "slot_name": multiworld.player_name[player], "seed_name": multiworld.seed_name,
                     "starting_items": multiworld.starting_items[player], "recipes": recipes,
                     "random": random, "flop_random": flop_random,
                     "static_nodes": multiworld.worlds[player].static_nodes,
                     "recipe_time_scale": recipe_time_scales[multiworld.recipe_time[player].value],
                     "free_sample_blacklist": {item : 1 for item in free_sample_blacklist},
                     "progressive_technology_table": {tech.name : tech.progressive for tech in
                                                      progressive_technology_table.values()},
                     "custom_recipes": world.custom_recipes}

    for factorio_option in Options.factorio_options:
        template_data[factorio_option] = getattr(multiworld, factorio_option)[player].value
        
    if getattr(multiworld, "silo")[player].value == Options.Silo.option_randomize_recipe:
        template_data["free_sample_blacklist"]["rocket-silo"] = 1

    control_code = control_template.render(**template_data)
    data_template_code = data_template.render(**template_data)
    data_final_fixes_code = data_final_template.render(**template_data)

    mod_dir = os.path.join(output_directory, mod_name + "_" + Utils.__version__)
    en_locale_dir = os.path.join(mod_dir, "locale", "en")
    os.makedirs(en_locale_dir, exist_ok=True)
    shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "mod"), mod_dir, dirs_exist_ok=True)
    with open(os.path.join(mod_dir, "data.lua"), "wt") as f:
        f.write(data_template_code)
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
    zf_path = os.path.join(mod_dir + ".zip")
    with zipfile.ZipFile(zf_path, compression=zipfile.ZIP_DEFLATED, mode='w') as zf:
        for root, dirs, files in os.walk(mod_dir):
            for file in files:
                zf.write(os.path.join(root, file),
                         os.path.relpath(os.path.join(root, file),
                                         os.path.join(mod_dir, '..')))
    shutil.rmtree(mod_dir)
