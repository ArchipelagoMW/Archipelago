# Copyright (c) 2022 FelicitusNeko
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import typing
from Options import Option, DeathLink, Toggle, DefaultOnToggle, Choice


class Goal(Choice):
    """Which goal must be achieved to trigger completion."""
    display_name = "Goal"
    option_return_the_cursed_seal = 0
    option_any_ending = 1
    option_true_ending = 2
    alias_normal_ending = 1
    alias_agate_knife = 2
    default = 1


class IncludePSIKeys(DefaultOnToggle):
    """Whether PSI Keys should be included in the multiworld pool. If not, they will be in their vanilla locations."""
    display_name = "Include PSI Keys"


class IncludeEvolutionTraps(Toggle):
    """
        Whether evolution traps should be included in the multiworld pool.
        If not, they will be activated by bosses, as in vanilla.
    """
    display_name = "Include Evolution Traps"


meritous_options: typing.Dict[str, type(Option)] = {
    "goal": Goal,
    "include_psi_keys": IncludePSIKeys,
    "include_evolution_traps": IncludeEvolutionTraps,
    "death_link": DeathLink
}
