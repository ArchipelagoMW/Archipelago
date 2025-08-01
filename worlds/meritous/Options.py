# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass

import typing
from Options import Option, DeathLink, Toggle, DefaultOnToggle, Choice, PerGameCommonOptions


cost_scales = {
    0: [80, 5, 4],
    1: [60, 5, 3],
    2: [50, 4, 3]
}


class Goal(Choice):
    """Which goal must be achieved to trigger completion."""
    display_name = "Goal"
    option_return_the_cursed_seal = 0
    option_any_ending = 1
    option_true_ending = 2
    alias_normal_ending = 1
    alias_agate_knife = 2
    default = 0


class IncludePSIKeys(DefaultOnToggle):
    """Whether PSI Keys should be included in the multiworld pool. If not, they will be in their vanilla locations."""
    display_name = "Include PSI Keys"


class IncludeEvolutionTraps(Toggle):
    """
        Whether evolution traps should be included in the multiworld pool.
        If not, they will be activated by bosses, as in vanilla.
    """
    display_name = "Include Evolution Traps"


class ItemCacheCost(Choice):
    """
        Determines how the cost for Alpha, Beta, and Gamma caches will scale.
        Vanilla has a total cost of about 1B crystals on Normal difficulty;
        Reduced has about 750M; and Heavily Reduced has about 600M.
    """
    display_name = "Item cache cost scaling"
    option_vanilla = 0
    option_reduced = 1
    option_heavily_reduced = 2
    default = 0


@dataclass
class MeritousOptions(PerGameCommonOptions):
    goal: Goal
    include_psi_keys: IncludePSIKeys
    include_evolution_traps: IncludeEvolutionTraps
    item_cache_cost: ItemCacheCost
    death_link: DeathLink
