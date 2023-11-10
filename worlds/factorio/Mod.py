"""Outputs a Factorio Mod to facilitate integration with Archipelago"""

import json
import os
import shutil
import threading
import zipfile
from typing import Optional, TYPE_CHECKING, Any, List, Callable, Tuple

import jinja2

import Utils
import worlds.Files
from . import Options
from .Technologies import tech_table, recipes, free_sample_exclusions, progressive_technology_table, \
    base_tech_table, tech_to_progressive_lookup, fluids, useless_technologies

if TYPE_CHECKING:
    from . import Factorio

template_env: Optional[jinja2.Environment] = None

data_template: Optional[jinja2.Template] = None
data_final_template: Optional[jinja2.Template] = None
locale_template: Optional[jinja2.Template] = None
control_template: Optional[jinja2.Template] = None
settings_template: Optional[jinja2.Template] = None

template_load_lock = threading.Lock()

base_info = {
    "version": Utils.__version__,
    "title": "Archipelago",
    "author": "Berserker",
    "homepage": "https://archipelago.gg",
    "description": "Integration client for the Archipelago Randomizer",
    "factorio_version": "1.1",
    "dependencies": [
        "base >= 1.1.0",
        "? science-not-invited",
        "? factory-levels"
    ]
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

recipe_time_ranges = {
    Options.RecipeTime.option_new_fast: (0.25, 2),
    Options.RecipeTime.option_new_normal: (0.25, 10),
    Options.RecipeTime.option_slow: (5, 10)
}


class FactorioModFile(worlds.Files.APContainer):
    game = "Factorio"
    compression_method = zipfile.ZIP_DEFLATED  # Factorio can't load LZMA archives
    writing_tasks: List[Callable[[], Tuple[str, str]]]

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.writing_tasks = []

    def write_contents(self, opened_zipfile: zipfile.ZipFile):
        # directory containing Factorio mod has to come first, or Factorio won't recognize this file as a mod.
        mod_dir = self.path[:-4]  # cut off .zip
        for root, dirs, files in os.walk(mod_dir):
            for file in files:
                filename = os.path.join(root, file)
                opened_zipfile.write(filename,
                                     os.path.relpath(filename,
                                                     os.path.join(mod_dir, '..')))
        for task in self.writing_tasks:
            target, content = task()
            opened_zipfile.writestr(target, content)
        # now we can add extras.
        super(FactorioModFile, self).write_contents(opened_zipfile)


def generate_mod(world: "Factorio", output_directory: str):
    player = world.player
    multiworld = world.multiworld
    global data_final_template, locale_template, control_template, data_template, settings_template
    with template_load_lock:
        if not data_final_template:
            def load_template(name: str):
                import pkgutil
                data = pkgutil.get_data(__name__, "data/mod_template/" + name).decode()
                return data, name, lambda: False

            template_env: Optional[jinja2.Environment] = \
                jinja2.Environment(loader=jinja2.FunctionLoader(load_template))

            data_template = template_env.get_template("data.lua")
            data_final_template = template_env.get_template("data-final-fixes.lua")
            locale_template = template_env.get_template(r"locale/en/locale.cfg")
            control_template = template_env.get_template("control.lua")
            settings_template = template_env.get_template("settings.lua")
    # get data for templates
    locations = [(location, location.item)
                 for location in world.science_locations]
    mod_name = f"AP-{multiworld.seed_name}-P{player}-{multiworld.get_file_safe_player_name(player)}"
    versioned_mod_name = mod_name + "_" + Utils.__version__

    random = multiworld.per_slot_randoms[player]

    def flop_random(low, high, base=None):
        """Guarantees 50% below base and 50% above base, uniform distribution in each direction."""
        if base:
            distance = random.random()
            if random.randint(0, 1):
                return base + (high - base) * distance
            else:
                return base - (base - low) * distance
        return random.uniform(low, high)

    template_data = {
        "locations": locations,
        "player_names": multiworld.player_name,
        "tech_table": tech_table,
        "base_tech_table": base_tech_table,
        "tech_to_progressive_lookup": tech_to_progressive_lookup,
        "mod_name": mod_name,
        "allowed_science_packs": multiworld.max_science_pack[player].get_allowed_packs(),
        "custom_technologies": multiworld.worlds[player].custom_technologies,
        "tech_tree_layout_prerequisites": world.tech_tree_layout_prerequisites,
        "slot_name": multiworld.player_name[player], "seed_name": multiworld.seed_name,
        "slot_player": player,
        "starting_items": multiworld.starting_items[player], "recipes": recipes,
        "random": random, "flop_random": flop_random,
        "recipe_time_scale": recipe_time_scales.get(multiworld.recipe_time[player].value, None),
        "recipe_time_range": recipe_time_ranges.get(multiworld.recipe_time[player].value, None),
        "free_sample_blacklist": {item: 1 for item in free_sample_exclusions},
        "progressive_technology_table": {tech.name: tech.progressive for tech in
                                         progressive_technology_table.values()},
        "custom_recipes": world.custom_recipes,
        "max_science_pack": multiworld.max_science_pack[player].value,
        "liquids": fluids,
        "goal": multiworld.goal[player].value,
        "energy_link": multiworld.energy_link[player].value,
        "useless_technologies": useless_technologies,
        "chunk_shuffle": multiworld.chunk_shuffle[player].value if hasattr(multiworld, "chunk_shuffle") else 0,
    }

    for factorio_option in Options.factorio_options:
        if factorio_option in ["free_sample_blacklist", "free_sample_whitelist"]:
            continue
        template_data[factorio_option] = getattr(multiworld, factorio_option)[player].value

    if getattr(multiworld, "silo")[player].value == Options.Silo.option_randomize_recipe:
        template_data["free_sample_blacklist"]["rocket-silo"] = 1

    if getattr(multiworld, "satellite")[player].value == Options.Satellite.option_randomize_recipe:
        template_data["free_sample_blacklist"]["satellite"] = 1

    template_data["free_sample_blacklist"].update({item: 1 for item in multiworld.free_sample_blacklist[player].value})
    template_data["free_sample_blacklist"].update({item: 0 for item in multiworld.free_sample_whitelist[player].value})

    mod_dir = os.path.join(output_directory, versioned_mod_name)

    zf_path = os.path.join(mod_dir + ".zip")
    mod = FactorioModFile(zf_path, player=player, player_name=multiworld.player_name[player])

    if world.zip_path:
        with zipfile.ZipFile(world.zip_path) as zf:
            for file in zf.infolist():
                if not file.is_dir() and "/data/mod/" in file.filename:
                    path_part = Utils.get_text_after(file.filename, "/data/mod/")
                    mod.writing_tasks.append(lambda arcpath=versioned_mod_name+"/"+path_part, content=zf.read(file):
                                             (arcpath, content))
    else:
        shutil.copytree(os.path.join(os.path.dirname(__file__), "data", "mod"), mod_dir, dirs_exist_ok=True)

    mod.writing_tasks.append(lambda: (versioned_mod_name + "/data.lua",
                                      data_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/data-final-fixes.lua",
                                      data_final_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/control.lua",
                                      control_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/settings.lua",
                                      settings_template.render(**template_data)))
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/locale/en/locale.cfg",
                                      locale_template.render(**template_data)))

    info = base_info.copy()
    info["name"] = mod_name
    mod.writing_tasks.append(lambda: (versioned_mod_name + "/info.json",
                                      json.dumps(info, indent=4)))

    # write the mod file
    mod.write()
    # clean up
    shutil.rmtree(mod_dir)
