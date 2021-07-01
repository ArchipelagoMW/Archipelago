import typing

from Options import Choice, OptionDict, Option, DefaultOnToggle


class MaxSciencePack(Choice):
    option_automation_science_pack = 0
    option_logistic_science_pack = 1
    option_military_science_pack = 2
    option_chemical_science_pack = 3
    option_production_science_pack = 4
    option_utility_science_pack = 5
    option_space_science_pack = 6
    default = 6

    def get_allowed_packs(self):
        return {option.replace("_", "-") for option, value in self.options.items() if value <= self.value} - \
               {"space-science-pack"}  # with rocket launch being the goal, post-launch techs don't make sense


class TechCost(Choice):
    option_very_easy = 0
    option_easy = 1
    option_kind = 2
    option_normal = 3
    option_hard = 4
    option_very_hard = 5
    option_insane = 6
    default = 3


class FreeSamples(Choice):
    option_none = 0
    option_single_craft = 1
    option_half_stack = 2
    option_stack = 3
    default = 3


class TechTreeLayout(Choice):
    option_single = 0
    option_small_diamonds = 1
    option_medium_diamonds = 2
    option_large_diamonds = 3
    option_small_pyramids = 4
    option_medium_pyramids = 5
    option_large_pyramids = 6
    option_small_funnels = 7
    option_medium_funnels = 8
    option_large_funnels = 9
    option_funnels = 4
    alias_pyramid = 6
    alias_funnel = 9
    default = 0


class TechTreeInformation(Choice):
    option_none = 0
    option_advancement = 1
    option_full = 2
    default = 2


class RecipeTime(Choice):
    option_vanilla = 0
    option_fast = 1
    option_normal = 2
    option_slow = 4
    option_chaos = 5


class FactorioStartItems(OptionDict):
    default = {"burner-mining-drill": 19, "stone-furnace": 19}


class FactorioWorldGen(OptionDict):
    default = {"terrain_segmentation": 0.5, "water": 1.5,
               "autoplace_controls": {"coal": {"frequency": 1, "size": 3, "richness": 6},
                                      "copper-ore": {"frequency": 1, "size": 3, "richness": 6},
                                      "crude-oil": {"frequency": 1, "size": 3, "richness": 6},
                                      "enemy-base": {"frequency": 1, "size": 1, "richness": 1},
                                      "iron-ore": {"frequency": 1, "size": 3, "richness": 6},
                                      "stone": {"frequency": 1, "size": 3, "richness": 6},
                                      "trees": {"frequency": 1, "size": 1, "richness": 1},
                                      "uranium-ore": {"frequency": 1, "size": 3, "richness": 6}},
               "starting_area": 1, "peaceful_mode": False,
               "cliff_settings": {"name": "cliff", "cliff_elevation_0": 10, "cliff_elevation_interval": 40,
                                  "richness": 1}}

factorio_options: typing.Dict[str, type(Option)] = {
    "max_science_pack": MaxSciencePack,
    "tech_tree_layout": TechTreeLayout,
    "tech_cost": TechCost,
    "free_samples": FreeSamples,
    "tech_tree_information": TechTreeInformation,
    "starting_items": FactorioStartItems,
    "recipe_time": RecipeTime,
    "imported_blueprints": DefaultOnToggle,
    "world_gen": FactorioWorldGen
}