from __future__ import annotations

from dataclasses import dataclass
import typing

from schema import Schema, Optional, And, Or

from Options import Choice, OptionDict, OptionSet, DefaultOnToggle, Range, DeathLink, Toggle, \
    StartInventoryPool, PerGameCommonOptions, OptionGroup

# schema helpers
FloatRange = lambda low, high: And(Or(int, float), lambda f: low <= f <= high)
LuaBool = Or(bool, And(int, lambda n: n in (0, 1)))


class MaxSciencePack(Choice):
    """Maximum level of science pack required to complete the game.
    This also affects the relative cost of silo and satellite recipes if they are randomized.
    That is the only thing in which the Utility Science Pack and Space Science Pack settings differ."""
    display_name = "Maximum Required Science Pack"
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
    display_name = "Goal"
    option_rocket = 0
    option_satellite = 1
    default = 0


class TechCost(Range):
    range_start = 1
    range_end = 10000
    default = 5


class MinTechCost(TechCost):
    """The cheapest a Technology can be in Science Packs."""
    display_name = "Minimum Science Pack Cost"
    default = 5


class MaxTechCost(TechCost):
    """The most expensive a Technology can be in Science Packs."""
    display_name = "Maximum Science Pack Cost"
    default = 500


class TechCostDistribution(Choice):
    """Random distribution of costs of the Science Packs.
    Even: any number between min and max is equally likely.
    Low: low costs, near the minimum, are more likely.
    Middle: medium costs, near the average, are more likely.
    High: high costs, near the maximum, are more likely."""
    display_name = "Tech Cost Distribution"
    option_even = 0
    option_low = 1
    option_middle = 2
    option_high = 3


class TechCostMix(Range):
    """Percent chance that a preceding Science Pack is also required.
    Chance is rolled per preceding pack."""
    display_name = "Science Pack Cost Mix"
    range_end = 100
    default = 70


class RampingTechCosts(Toggle):
    """Forces the amount of Science Packs required to ramp up with the highest involved Pack. Average is preserved.
    For example:
    off: Automation (red)/Logistics (green) sciences can range from 1 to 1000 Science Packs,
    on: Automation (red) ranges to ~500 packs and Logistics (green) from ~500 to 1000 Science Packs"""
    display_name = "Ramping Tech Costs"


class Silo(Choice):
    """Ingredients to craft rocket silo or auto-place if set to spawn."""
    display_name = "Rocket Silo"
    option_vanilla = 0
    option_randomize_recipe = 1
    option_spawn = 2
    default = 0


class Satellite(Choice):
    """Ingredients to craft satellite."""
    display_name = "Satellite"
    option_vanilla = 0
    option_randomize_recipe = 1
    default = 0


class FreeSamples(Choice):
    """Get free items with your technologies."""
    display_name = "Free Samples"
    option_none = 0
    option_single_craft = 1
    option_half_stack = 2
    option_stack = 3
    default = 3


class FreeSamplesQuality(Choice):
    """If free samples are on, determine the quality of the granted items.
    Requires the quality mod, which is part of the Space Age DLC. Without it, normal quality is given."""
    display_name = "Free Samples Quality"
    option_normal = 0
    option_uncommon = 1
    option_rare = 2
    option_epic = 3
    option_legendary = 4
    default = 0


class TechTreeLayout(Choice):
    """Selects how the tech tree nodes are interwoven.
    Single: No dependencies
    Diamonds: Several grid graphs (4/9/16 nodes each)
    Pyramids: Several top halves of diamonds (6/10/15 nodes each)
    Funnels: Several bottom halves of diamonds (6/10/15 nodes each)
    Trees: Several trees
    Choices: A single balanced binary tree
    """
    display_name = "Technology Tree Layout"
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
    """How much information should be displayed in the tech tree.
    None: No indication of what a research unlocks.
    Advancement: Indicates if a research unlocks an item that is considered logical advancement, but not who it is for.
    Full: Labels with exact names and recipients of unlocked items; all researches are prefilled into the !hint command.
    """
    display_name = "Technology Tree Information"
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
    display_name = "Recipe Time"
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
    display_name = "Progressive Technologies"
    option_off = 0
    option_grouped_random = 1
    option_on = 2
    default = 2

    def want_progressives(self, random):
        return random.choice([True, False]) if self.value == self.option_grouped_random else bool(self.value)


class RecipeIngredients(Choice):
    """Select if rocket, or rocket + science pack ingredients should be random."""
    display_name = "Random Recipe Ingredients Level"
    option_rocket = 0
    option_science_pack = 1


class RecipeIngredientsOffset(Range):
    """When randomizing ingredients, remove or add this many "slots" of items.
    For example, at -1 a randomized Automation Science Pack will only require 1 ingredient, instead of 2."""
    display_name = "Randomized Recipe Ingredients Offset"
    range_start = -1
    range_end = 5


class FactorioStartItems(OptionDict):
    """Mapping of Factorio internal item-name to amount granted on start."""
    display_name = "Starting Items"
    default = {"burner-mining-drill": 4, "stone-furnace": 4,  "raw-fish": 50}


class FactorioFreeSampleBlacklist(OptionSet):
    """Set of items that should never be granted from Free Samples"""
    display_name = "Free Sample Blacklist"


class FactorioFreeSampleWhitelist(OptionSet):
    """Overrides any free sample blacklist present. This may ruin the balance of the mod, be warned."""
    display_name = "Free Sample Whitelist"


class TrapCount(Range):
    range_end = 25


class AttackTrapCount(TrapCount):
    """Trap items that when received trigger an attack on your base."""
    display_name = "Attack Traps"


class TeleportTrapCount(TrapCount):
    """Trap items that when received trigger a random teleport."""
    display_name = "Teleport Traps"


class GrenadeTrapCount(TrapCount):
    """Trap items that when received trigger a grenade explosion on each player."""
    display_name = "Grenade Traps"


class ClusterGrenadeTrapCount(TrapCount):
    """Trap items that when received trigger a cluster grenade explosion on each player."""
    display_name = "Cluster Grenade Traps"


class ArtilleryTrapCount(TrapCount):
    """Trap items that when received trigger an artillery shell on each player."""
    display_name = "Artillery Traps"


class AtomicRocketTrapCount(TrapCount):
    """Trap items that when received trigger an atomic rocket explosion on each player.
    Warning: there is no warning. The launch is instantaneous."""
    display_name = "Atomic Rocket Traps"


class AtomicCliffRemoverTrapCount(TrapCount):
    """Trap items that when received trigger an atomic rocket explosion on a random cliff.
    Warning: there is no warning. The launch is instantaneous."""
    display_name = "Atomic Cliff Remover Traps"


class EvolutionTrapCount(TrapCount):
    """Trap items that when received increase the enemy evolution."""
    display_name = "Evolution Traps"
    range_end = 10


class EvolutionTrapIncrease(Range):
    """How much an Evolution Trap increases the enemy evolution.
    Increases scale down proportionally to the session's current evolution factor
    (40 increase at 0.50 will add 0.20... 40 increase at 0.75 will add 0.10...)"""
    display_name = "Evolution Trap % Effect"
    range_start = 1
    default = 10
    range_end = 100


class FactorioWorldGen(OptionDict):
    """World Generation settings. Overview of options at https://wiki.factorio.com/Map_generator,
    with in-depth documentation at https://lua-api.factorio.com/latest/Concepts.html#MapGenSettings"""
    display_name = "World Generation"
    # FIXME: do we want default be a rando-optimized default or in-game DS?
    value: dict[str, dict[str, typing.Any]]
    default = {
        "autoplace_controls": {
            # terrain
            "water": {"frequency": 1, "size": 1, "richness": 1},
            "nauvis_cliff": {"frequency": 1, "size": 1, "richness": 1},
            "starting_area_moisture": {"frequency": 1, "size": 1, "richness": 1},
            # resources
            "coal": {"frequency": 1, "size": 3, "richness": 6},
            "copper-ore": {"frequency": 1, "size": 3, "richness": 6},
            "crude-oil": {"frequency": 1, "size": 3, "richness": 6},
            "iron-ore": {"frequency": 1, "size": 3, "richness": 6},
            "stone": {"frequency": 1, "size": 3, "richness": 6},
            "uranium-ore": {"frequency": 1, "size": 3, "richness": 6},
            # misc
            "trees": {"frequency": 1, "size": 1, "richness": 1},
            "enemy-base": {"frequency": 1, "size": 1, "richness": 1},
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
            Optional("autoplace_controls"): {
                str: {
                    "frequency": FloatRange(0, 6),
                    "size": FloatRange(0, 6),
                    "richness": FloatRange(0.166, 6)
                }
            },
            Optional("seed"): Or(None, And(int, lambda n: n >= 0)),
            Optional("width"): And(int, lambda n: n >= 0),
            Optional("height"): And(int, lambda n: n >= 0),
            Optional("starting_area"): FloatRange(0.166, 6),
            Optional("peaceful_mode"): LuaBool,
            Optional("cliff_settings"): {
                "name": str, "cliff_elevation_0": FloatRange(0, 99),
                "cliff_elevation_interval": FloatRange(0.066, 241),  # 40/frequency
                "richness": FloatRange(0, 6)
            },
            Optional("property_expression_names"): Schema({
                Optional("control-setting:moisture:bias"): FloatRange(-0.5, 0.5),
                Optional("control-setting:moisture:frequency:multiplier"): FloatRange(0.166, 6),
                Optional("control-setting:aux:bias"): FloatRange(-0.5, 0.5),
                Optional("control-setting:aux:frequency:multiplier"): FloatRange(0.166, 6),
                Optional(str): object  # allow overriding all properties
            }),
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

    def __init__(self, value: dict[str, typing.Any]):
        advanced = {"pollution", "enemy_evolution", "enemy_expansion"}
        self.value = {
            "basic": {k: v for k, v in value.items() if k not in advanced},
            "advanced": {k: v for k, v in value.items() if k in advanced}
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
    def from_any(cls, data: dict[str, typing.Any]) -> FactorioWorldGen:
        if type(data) == dict:
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")


class ImportedBlueprint(DefaultOnToggle):
    """Allow or Disallow Blueprints from outside the current savegame."""
    display_name = "Blueprints"


class EnergyLink(Toggle):
    """Allow sending energy to other worlds. 25% of the energy is lost in the transfer."""
    display_name = "Energy Link"


@dataclass
class FactorioOptions(PerGameCommonOptions):
    max_science_pack: MaxSciencePack
    goal: Goal
    tech_tree_layout: TechTreeLayout
    min_tech_cost: MinTechCost
    max_tech_cost: MaxTechCost
    tech_cost_distribution: TechCostDistribution
    tech_cost_mix: TechCostMix
    ramping_tech_costs: RampingTechCosts
    silo: Silo
    satellite: Satellite
    free_samples: FreeSamples
    free_samples_quality: FreeSamplesQuality
    tech_tree_information: TechTreeInformation
    starting_items: FactorioStartItems
    free_sample_blacklist: FactorioFreeSampleBlacklist
    free_sample_whitelist: FactorioFreeSampleWhitelist
    recipe_time: RecipeTime
    recipe_ingredients: RecipeIngredients
    recipe_ingredients_offset: RecipeIngredientsOffset
    imported_blueprints: ImportedBlueprint
    world_gen: FactorioWorldGen
    progressive: Progressive
    teleport_traps: TeleportTrapCount
    grenade_traps: GrenadeTrapCount
    cluster_grenade_traps: ClusterGrenadeTrapCount
    artillery_traps: ArtilleryTrapCount
    atomic_rocket_traps: AtomicRocketTrapCount
    atomic_cliff_remover_traps: AtomicCliffRemoverTrapCount
    attack_traps: AttackTrapCount
    evolution_traps: EvolutionTrapCount
    evolution_trap_increase: EvolutionTrapIncrease
    death_link: DeathLink
    energy_link: EnergyLink
    start_inventory_from_pool: StartInventoryPool


option_groups: list[OptionGroup] = [
    OptionGroup(
        "Technologies",
        [
            TechTreeLayout,
            Progressive,
            MinTechCost,
            MaxTechCost,
            TechCostDistribution,
            TechCostMix,
            RampingTechCosts,
            TechTreeInformation,
        ]
    ),
    OptionGroup(
        "Traps",
        [
            AttackTrapCount,
            EvolutionTrapCount,
            EvolutionTrapIncrease,
            TeleportTrapCount,
            GrenadeTrapCount,
            ClusterGrenadeTrapCount,
            ArtilleryTrapCount,
            AtomicRocketTrapCount,
            AtomicCliffRemoverTrapCount,
        ],
        start_collapsed=True
    ),
]
