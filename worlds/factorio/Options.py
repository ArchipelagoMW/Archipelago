from __future__ import annotations
import typing

from Options import Choice, OptionDict, Option, DefaultOnToggle
from schema import Schema, Optional, And, Or

# schema helpers
FloatRange = lambda low,high: And(Or(int,float), lambda f: low<=f<=high)
LuaBool = Or(bool, And(int, lambda n: n in (0,1)))


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

    @classmethod
    def get_ordered_science_packs(cls):
        return [option.replace("_", "-") for option, value in sorted(cls.options.items(), key=lambda pair: pair[1])]

    def get_max_pack(self):
        return self.get_ordered_science_packs()[self.value].replace("_", "-")

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

# TODO: implement random
class Progressive(Choice):
    option_off = 0
    option_random = 1
    option_on = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_random else int(self.value)


class RecipeIngredients(Choice):
    option_rocket = 0
    option_science_pack = 1


class FactorioStartItems(OptionDict):
    default = {"burner-mining-drill": 19, "stone-furnace": 19}


class FactorioWorldGen(OptionDict):
    # FIXME: do we want default be a rando-optimized default or in-game DS?
    value: typing.Dict[str, typing.Dict[str, typing.Any]]
    default = {"terrain_segmentation": 0.5,
               "water": 1.5,
               "autoplace_controls": {"coal": {"frequency": 1, "size": 3, "richness": 6},
                                      "copper-ore": {"frequency": 1, "size": 3, "richness": 6},
                                      "crude-oil": {"frequency": 1, "size": 3, "richness": 6},
                                      "enemy-base": {"frequency": 1, "size": 1, "richness": 1},
                                      "iron-ore": {"frequency": 1, "size": 3, "richness": 6},
                                      "stone": {"frequency": 1, "size": 3, "richness": 6},
                                      "trees": {"frequency": 1, "size": 1, "richness": 1},
                                      "uranium-ore": {"frequency": 1, "size": 3, "richness": 6}},
               "seed": None,
               "starting_area": 1,
               "peaceful_mode": False,
               "cliff_settings": {"name": "cliff", "cliff_elevation_0": 10, "cliff_elevation_interval": 40,
                                  "richness": 1},
               "pollution": {"enabled": True, "diffusion_ratio": 0.02, "ageing": 1,
                             "enemy_attack_pollution_consumption_modifier": 1,
                             "min_pollution_to_damage_trees": 60,
                             "pollution_restored_per_tree_damage": 10}}
    schema = Schema({
        "basic": {
            Optional("terrain_segmentation"): FloatRange(0.166,6),
            Optional("water"): FloatRange(0.166,6),
            Optional("autoplace_controls"): {
                str: {
                    "frequency": FloatRange(0,6),
                    "size": FloatRange(0,6),
                    "richness": FloatRange(0.166,6)}},
            Optional("seed"): Or(None,And(int, lambda n: n>=0)),
            Optional("starting_area"): FloatRange(0.166,6),
            Optional("peaceful_mode"): LuaBool,
            Optional("cliff_settings"): {
                "name": str, "cliff_elevation_0": FloatRange(0,99),
                "cliff_elevation_interval": FloatRange(0.066,241),  # 40/frequency
                "richness": FloatRange(0,6)},
        },
        "advanced": {
            Optional("pollution"): {
                Optional("enabled"): LuaBool,
                Optional("diffusion_ratio"): FloatRange(0,0.25),
                Optional("ageing"): FloatRange(0.1,4),
                Optional("enemy_attack_pollution_consumption_modifier"): FloatRange(0.1,4),
                Optional("min_pollution_to_damage_trees"): FloatRange(0,9999),
                Optional("pollution_restored_per_tree_damage"): FloatRange(0,9999)}
        }
    })

    def __init__(self, value: typing.Dict[str, typing.Any]):
        advanced = {"pollution"}
        self.value = {
            "basic":    { key: value[key] for key in value.keys() - advanced },
            "advanced": { key: value[key] for key in value.keys() & advanced }
        }

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> FactorioWorldGen:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")


factorio_options: typing.Dict[str, type(Option)] = {
    "max_science_pack": MaxSciencePack,
    "tech_tree_layout": TechTreeLayout,
    "tech_cost": TechCost,
    "free_samples": FreeSamples,
    "tech_tree_information": TechTreeInformation,
    "starting_items": FactorioStartItems,
    "recipe_time": RecipeTime,
    "recipe_ingredients": RecipeIngredients,
    "imported_blueprints": DefaultOnToggle,
    "world_gen": FactorioWorldGen,
    "progressive": DefaultOnToggle
}