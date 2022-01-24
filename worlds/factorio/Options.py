from __future__ import annotations
import typing

from Options import Choice, OptionDict, OptionSet, ItemDict, Option, DefaultOnToggle, Range, DeathLink
from schema import Schema, Optional, And, Or

# schema helpers
FloatRange = lambda low, high: And(Or(int, float), lambda f: low <= f <= high)
LuaBool = Or(bool, And(int, lambda n: n in (0, 1)))


class MaxSciencePack(Choice):
    """Maximum level of science pack required to complete the game."""
    displayname = "Maximum Required Science Pack"
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


class Goal(Choice):
    """Goal required to complete the game."""
    displayname = "Goal"
    option_rocket = 0
    option_satellite = 1
    default = 0


class TechCost(Choice):
    """How expensive are the technologies."""
    displayname = "Technology Cost Scale"
    option_very_easy = 0
    option_easy = 1
    option_kind = 2
    option_normal = 3
    option_hard = 4
    option_very_hard = 5
    option_insane = 6
    default = 3


class Silo(Choice):
    """Ingredients to craft rocket silo or auto-place if set to spawn."""
    displayname = "Rocket Silo"
    option_vanilla = 0
    option_randomize_recipe = 1
    option_spawn = 2
    default = 0


class Satellite(Choice):
    """Ingredients to craft satellite."""
    displayname = "Satellite"
    option_vanilla = 0
    option_randomize_recipe = 1
    default = 0


class FreeSamples(Choice):
    """Get free items with your technologies."""
    displayname = "Free Samples"
    option_none = 0
    option_single_craft = 1
    option_half_stack = 2
    option_stack = 3
    default = 3


class TechTreeLayout(Choice):
    """Selects how the tech tree nodes are interwoven."""
    displayname = "Technology Tree Layout"
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
    option_trees = 10
    option_choices = 11
    default = 0


class TechTreeInformation(Choice):
    """How much information should be displayed in the tech tree."""
    displayname = "Technology Tree Information"
    option_none = 0
    option_advancement = 1
    option_full = 2
    default = 2


class RecipeTime(Choice):
    """Randomize the time it takes for any recipe to craft, this includes smelting, chemical lab, hand crafting etc.
    Fast: 0.25X - 1X
    Normal: 0.5X - 2X
    Slow: 1X - 4X
    Chaos: 0.25X - 4X
    New category: ignores vanilla recipe time and rolls new one
    New Fast: 0.25 - 2 seconds
    New Normal: 0.25 - 10 seconds
    New Slow:  5 - 10 seconds
    """
    displayname = "Recipe Time"
    option_vanilla = 0
    option_fast = 1
    option_normal = 2
    option_slow = 4
    option_chaos = 5
    option_new_fast = 6
    option_new_normal = 7
    option_new_slow = 8


class Progressive(Choice):
    """Merges together Technologies like "automation-1" to "automation-3" into 3 copies of "Progressive Automation",
    which awards them in order."""
    displayname = "Progressive Technologies"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    alias_false = 0
    alias_true = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class RecipeIngredients(Choice):
    """Select if rocket, or rocket + science pack ingredients should be random."""
    displayname = "Random Recipe Ingredients Level"
    option_rocket = 0
    option_science_pack = 1


class FactorioStartItems(ItemDict):
    """Mapping of Factorio internal item-name to amount granted on start."""
    displayname = "Starting Items"
    verify_item_name = False
    default = {"burner-mining-drill": 19, "stone-furnace": 19}


class FactorioFreeSampleBlacklist(OptionSet):
    """Set of items that should never be granted from Free Samples"""
    displayname = "Free Sample Blacklist"


class FactorioFreeSampleWhitelist(OptionSet):
    """Overrides any free sample blacklist present. This may ruin the balance of the mod, be warned."""
    displayname = "Free Sample Whitelist"


class TrapCount(Range):
    range_end = 4


class AttackTrapCount(TrapCount):
    """Trap items that when received trigger an attack on your base."""
    displayname = "Attack Traps"


class EvolutionTrapCount(TrapCount):
    """Trap items that when received increase the enemy evolution."""
    displayname = "Evolution Traps"


class EvolutionTrapIncrease(Range):
    """How much an Evolution Trap increases the enemy evolution.
    Increases scale down proportionally to the session's current evolution factor
    (40 increase at 0.50 will add 0.20... 40 increase at 0.75 will add 0.10...)"""
    displayname = "Evolution Trap % Effect"
    range_start = 1
    default = 10
    range_end = 100


class FactorioWorldGen(OptionDict):
    """World Generation settings. Overview of options at https://wiki.factorio.com/Map_generator,
    with in-depth documentation at https://lua-api.factorio.com/latest/Concepts.html#MapGenSettings"""
    displayname = "World Generation"
    # FIXME: do we want default be a rando-optimized default or in-game DS?
    value: typing.Dict[str, typing.Dict[str, typing.Any]]
    default = {
        "terrain_segmentation": 0.5,
        "water": 1.5,
        "autoplace_controls": {
            "coal": {"frequency": 1, "size": 3, "richness": 6},
            "copper-ore": {"frequency": 1, "size": 3, "richness": 6},
            "crude-oil": {"frequency": 1, "size": 3, "richness": 6},
            "enemy-base": {"frequency": 1, "size": 1, "richness": 1},
            "iron-ore": {"frequency": 1, "size": 3, "richness": 6},
            "stone": {"frequency": 1, "size": 3, "richness": 6},
            "trees": {"frequency": 1, "size": 1, "richness": 1},
            "uranium-ore": {"frequency": 1, "size": 3, "richness": 6}
        },
        "seed": None,
        "starting_area": 1,
        "peaceful_mode": False,
        "cliff_settings": {
            "name": "cliff",
            "cliff_elevation_0": 10,
            "cliff_elevation_interval": 40,
            "richness": 1
        },
        "property_expression_names": {
            "control-setting:moisture:bias": 0,
            "control-setting:moisture:frequency:multiplier": 1,
            "control-setting:aux:bias": 0,
            "control-setting:aux:frequency:multiplier": 1
        },
        "pollution": {
            "enabled": True,
            "diffusion_ratio": 0.02,
            "ageing": 1,
            "enemy_attack_pollution_consumption_modifier": 1,
            "min_pollution_to_damage_trees": 60,
            "pollution_restored_per_tree_damage": 10
        },
        "enemy_evolution": {
            "enabled": True,
            "time_factor": 40.0e-7,
            "destroy_factor": 200.0e-5,
            "pollution_factor": 9.0e-7
        },
        "enemy_expansion": {
            "enabled": True,
            "max_expansion_distance": 7,
            "settler_group_min_size": 5,
            "settler_group_max_size": 20,
            "min_expansion_cooldown": 14400,
            "max_expansion_cooldown": 216000
        }
    }
    schema = Schema({
        "basic": {
            Optional("terrain_segmentation"): FloatRange(0.166, 6),
            Optional("water"): FloatRange(0.166, 6),
            Optional("autoplace_controls"): {
                str: {
                    "frequency": FloatRange(0, 6),
                    "size": FloatRange(0, 6),
                    "richness": FloatRange(0.166, 6)
                }
            },
            Optional("seed"): Or(None, And(int, lambda n: n >= 0)),
            Optional("starting_area"): FloatRange(0.166, 6),
            Optional("peaceful_mode"): LuaBool,
            Optional("cliff_settings"): {
                "name": str, "cliff_elevation_0": FloatRange(0, 99),
                "cliff_elevation_interval": FloatRange(0.066, 241),  # 40/frequency
                "richness": FloatRange(0, 6)
            },
            Optional("property_expression_names"): Schema({
                "control-setting:moisture:bias": FloatRange(-0.5, 0.5),
                "control-setting:moisture:frequency:multiplier": FloatRange(0.166, 6),
                "control-setting:aux:bias": FloatRange(-0.5, 0.5),
                "control-setting:aux:frequency:multiplier": FloatRange(0.166, 6)
            }, ignore_extra_keys=True)
        },
        "advanced": {
            Optional("pollution"): {
                Optional("enabled"): LuaBool,
                Optional("diffusion_ratio"): FloatRange(0, 0.25),
                Optional("ageing"): FloatRange(0.1, 4),
                Optional("enemy_attack_pollution_consumption_modifier"): FloatRange(0.1, 4),
                Optional("min_pollution_to_damage_trees"): FloatRange(0, 9999),
                Optional("pollution_restored_per_tree_damage"): FloatRange(0, 9999)
            },
            Optional("enemy_evolution"): {
                Optional("enabled"): LuaBool,
                Optional("time_factor"): FloatRange(0, 1000e-7),
                Optional("destroy_factor"): FloatRange(0, 1000e-5),
                Optional("pollution_factor"): FloatRange(0, 1000e-7),
            },
            Optional("enemy_expansion"): {
                Optional("enabled"): LuaBool,
                Optional("max_expansion_distance"): FloatRange(2, 20),
                Optional("settler_group_min_size"): FloatRange(1, 20),
                Optional("settler_group_max_size"): FloatRange(1, 50),
                Optional("min_expansion_cooldown"): FloatRange(3600, 216000),
                Optional("max_expansion_cooldown"): FloatRange(18000, 648000)
            }
        }
    })

    def __init__(self, value: typing.Dict[str, typing.Any]):
        advanced = {"pollution", "enemy_evolution", "enemy_expansion"}
        self.value = {
            "basic": {key: value[key] for key in value.keys() - advanced},
            "advanced": {key: value[key] for key in value.keys() & advanced}
        }

        # verify min_values <= max_values
        def optional_min_lte_max(container, min_key, max_key):
            min_val = container.get(min_key, None)
            max_val = container.get(max_key, None)
            if min_val is not None and max_val is not None and min_val > max_val:
                raise ValueError(f"{min_key} can't be bigger than {max_key}")

        enemy_expansion = self.value["advanced"].get("enemy_expansion", {})
        optional_min_lte_max(enemy_expansion, "settler_group_min_size", "settler_group_max_size")
        optional_min_lte_max(enemy_expansion, "min_expansion_cooldown", "max_expansion_cooldown")

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> FactorioWorldGen:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")


class ImportedBlueprint(DefaultOnToggle):
    """Allow or Disallow Blueprints from outside the current savegame."""
    displayname = "Blueprints"


factorio_options: typing.Dict[str, type(Option)] = {
    "max_science_pack": MaxSciencePack,
    "goal": Goal,
    "tech_tree_layout": TechTreeLayout,
    "tech_cost": TechCost,
    "silo": Silo,
    "satellite": Satellite,
    "free_samples": FreeSamples,
    "tech_tree_information": TechTreeInformation,
    "starting_items": FactorioStartItems,
    "free_sample_blacklist": FactorioFreeSampleBlacklist,
    "free_sample_whitelist": FactorioFreeSampleWhitelist,
    "recipe_time": RecipeTime,
    "recipe_ingredients": RecipeIngredients,
    "imported_blueprints": ImportedBlueprint,
    "world_gen": FactorioWorldGen,
    "progressive": Progressive,
    "evolution_traps": EvolutionTrapCount,
    "attack_traps": AttackTrapCount,
    "evolution_trap_increase": EvolutionTrapIncrease,
    "death_link": DeathLink
}
