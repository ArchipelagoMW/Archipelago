"""
Option definitions for Kirby & The Amazing Mirror
"""
from dataclasses import dataclass

from Options import Choice, DeathLink, PerGameCommonOptions, Toggle


class Goal(Choice):
    """
    Determines what your goal is to consider the game beaten.

    - Dark Mind: Defeat Dark Mind and beat the game
    - 100% Save File: Reserved for future player-template exposure
    - DEBUG: Testing-only goal
    """
    display_name = "Goal"
    default = 0
    option_dark_mind = 0
    option_100 = 1
    option_debug = 2
    template_excluded_choices = frozenset({"100", "debug"})


class RandomizeShards(Choice):
    """
    Adds Shards to the pool.

    - Vanilla: Area bosses give their own shard
    - Shuffle: Area bosses give a random shard
    - Completely Random: Shards can be found anywhere
    """
    display_name = "Randomize Shards"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class EnemyCopyAbilityRandomization(Choice):
        """
        Controls randomization of enemy-granted copy abilities.

        - Vanilla: Enemy copy abilities stay at native defaults.
        - Shuffled: Enemy types are remapped deterministically so all enemies of
            the same type grant the same ability.
        - Completely Random: Each eligible enemy ability grant can roll a different
            ability.
        """
        display_name = "Enemy Copy-Ability Randomization"
        default = 0
        option_vanilla = 0
        option_shuffled = 1
        option_completely_random = 2


class RandomizeBossSpawnedAbilityGrants(Toggle):
    """Whether ability-granting objects spawned by bosses are randomized."""
    display_name = "Randomize Boss-Spawned Ability Grants"
    default = 1


class RandomizeMiniBossAbilityGrants(Toggle):
    """Whether mini-boss ability grants are randomized."""
    display_name = "Randomize Mini-Boss Ability Grants"
    default = 1


class KirbyAmDeathLink(DeathLink):
    __doc__ = (DeathLink.__doc__ or "") + (
        "\n\n    KirbyAM DeathLink uses native Kirby HP semantics: incoming DeathLink queues a gameplay-gated"
        " local defeat, and local alive-to-dead transitions send one outgoing DeathLink event."
    )


@dataclass
class KirbyAmOptions(PerGameCommonOptions):
    goal: Goal

    shards: RandomizeShards

    enemy_copy_ability_randomization: EnemyCopyAbilityRandomization

    randomize_boss_spawned_ability_grants: RandomizeBossSpawnedAbilityGrants

    randomize_miniboss_ability_grants: RandomizeMiniBossAbilityGrants

    death_link: KirbyAmDeathLink


OPTION_GROUPS = []
