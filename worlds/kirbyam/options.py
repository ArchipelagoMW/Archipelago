"""
Option definitions for Kirby & The Amazing Mirror
"""
from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    OptionGroup,
    PerGameCommonOptions,
    Range,
    Toggle,
)


class Goal(Choice):
    """
    Determines what your goal is to consider the game beaten.

    - Dark Mind: Defeat Dark Mind and beat the game.
    
    NOTE: Dark Mind is the only supported value. This option is here for the future.
    """
    display_name = "Goal"
    default = 0
    option_dark_mind = 0


class RandomizeShards(Choice):
    """
    Controls where Mirror Shards can appear.

    - Vanilla: Each area's boss defeat location contains its matching shard.
    - Completely Random: Shards can appear from any location. Default.
    """
    display_name = "Randomize Shards"
    default = 2
    option_vanilla = 0
    option_completely_random = 2


class AbilityRandomizationMode(Choice):
    """
    Controls randomization of enemy-granted copy abilities. Does not affect ability statues.

    - Off: Enemy copy abilities stay at native defaults. Default.
    - Shuffled: Experimental. Enemy types are remapped deterministically so
        all enemies of the same type grant the same ability. Bugs are expected.
    - Completely Random: Experimental. Eligible enemy ability sources are remapped
        independently (deterministic per source entry). Hidden from the
        generated player template for the first public build. Bugs are expected.
    """
    display_name = "Ability Randomization Mode"
    default = 0
    option_off = 0
    option_shuffled = 1
    option_completely_random = 2
    template_excluded_choices = frozenset({"completely_random"})


# The following three options only apply when Ability Randomization Mode is not Off.
# Regular enemy sources (kind: enemy) with a non-zero native copy ability are always included
# regardless of these settings; miniboss and boss-spawn ability sources are controlled by the
# toggles below.

class AbilityRandomizationBossSpawns(Toggle):
    """
    Include boss-spawned ability grants in randomization.
      Only applies when Ability Randomization Mode is not Off.
      On by Default, but ability_randomization_mode is Off by Default.
    """
    display_name = "Ability Randomization: Boss Spawns"
    default = 1


class AbilityRandomizationMinibosses(Toggle):
    """
    Include mini-boss ability grants in randomization.
      Only applies when Ability Randomization Mode is not Off.
      On by Default, but ability_randomization_mode is Off by Default.
    """
    display_name = "Ability Randomization: Minibosses"
    default = 1


class AbilityRandomizationMinny(Toggle):
    """
    Include Minny in enemy copy-ability randomization.
      Only applies when Ability Randomization Mode is not Off.
      On by Default, but ability_randomization_mode is Off by Default.
    """
    display_name = "Ability Randomization: Minny"
    default = 1


class AbilityRandomizationPassiveEnemies(Toggle):
    """
    When enabled, enemies that normally do not grant a copy ability can receive a
    randomized ability.
      Only applies when Ability Randomization Mode is not Off.
      On by Default, but ability_randomization_mode is Off by Default.
    """
    display_name = "Ability Randomization: Passive Enemies"
    default = 1


class AbilityRandomizationNoAbilityWeight(Range):
    """
    Sets the percentage chance that an included randomized enemy grant resolves to
    no ability instead of a copy ability.

    - 0: Included randomized enemies always grant a copy ability.
    - 55: 55% of included randomized enemies grant no ability, 45% grant a copy ability.
            Default. This matches the in-game percentage when enemies that normally grant no ability are included in the randomization pool.
    - 100: Included randomized enemies always grant no ability.

    This only affects enemies already included by the ability randomization mode and
    the boss/miniboss/passive-enemy toggles.

        You can set a custom percentage by adding a custom number as the subkey and then supply the "percentage" chance for generation to roll that value.
      For example:
        25: 50
      The above says you want 25% of ability granting enemies to provide no ability instead of a copy ability, and 75% to provide a copy ability. Further,
        25: 10
        50: 10
        75: 10
            The above says you want generation to have equal chances of creating worlds where 25%, 50%, and 75% of ability granting enemies provide no ability instead of a copy ability.
    """
    display_name = "Ability Randomization: No Ability Weight"
    range_start = 0
    range_end = 100
    # 55% is rounded from 827 / 1510 = 54.77% vanilla no-ability regular-enemy placements
    # in the USA ROM across the current randomized-enemy dataset.
    default = 55


class EnableDebugLogging(Toggle):
    """
    Enable extra BizHawk client diagnostics for gameplay-state and mailbox delivery troubleshooting.
      Useful if you want to report a bug to the world developers. Off by default.
    """
    display_name = "Enable Debug Logging"
    default = 0


class NoExtraLives(Toggle):
    """
    Start with zero lives and clamp all extra-life gains to zero during gameplay.
      Starts after the tutorial. Off by default.
      
      Yes, you can combine this with One-Hit Mode for an extra challenge.
    """
    display_name = "No Extra Lives"
    default = 0


class OneHitMode(Choice):
    """
    Controls whether Kirby's maximum health is reduced to 1 HP at the start (one-hit mode).
      Starts after the tutorial. Off by default.
      Yes, you can combine this with No Extra Lives for an extra challenge.

    - Off: Kirby's maximum health is unmodified (native 6 HP base, plus 1 per Vitality Counter found).
    - Exclude Vitality Counters: Kirby starts with a maximum of 1 HP. All four Vitality Counter items are
        removed from the item pool and replaced with filler. Kirby's HP cap stays at 1 for the entire run.
    - Include Vitality Counters: Kirby starts with a maximum of 1 HP. Vitality Counter items remain in the
        pool; each one received increases Kirby's HP cap by 1 (up to 5 with all four). This is known to
        cause a visual artifact on the screen when a vitality counter is received, but it is functional.
    """
    display_name = "One-Hit Mode"
    default = 0
    option_off = 0
    option_exclude_vitality_counters = 1
    option_include_vitality_counters = 2


class RoomSanity(Toggle):
    """Adds room-visit checks (Room X-YY). Off by default because it adds 257 locations."""
    display_name = "Room Sanity"
    default = 0


class KirbyAmDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__


@dataclass
class KirbyAmOptions(PerGameCommonOptions):
    goal: Goal

    shards: RandomizeShards

    no_extra_lives: NoExtraLives

    one_hit_mode: OneHitMode

    ability_randomization_mode: AbilityRandomizationMode

    ability_randomization_boss_spawns: AbilityRandomizationBossSpawns

    ability_randomization_minibosses: AbilityRandomizationMinibosses

    ability_randomization_minny: AbilityRandomizationMinny

    ability_randomization_passive_enemies: AbilityRandomizationPassiveEnemies

    ability_randomization_no_ability_weight: AbilityRandomizationNoAbilityWeight

    room_sanity: RoomSanity

    enable_debug_logging: EnableDebugLogging

    death_link: KirbyAmDeathLink


OPTION_GROUPS = [
    OptionGroup("Make the game last longer", [
        RoomSanity,
    ]),
    OptionGroup("Make the game harder", [
        NoExtraLives,
        OneHitMode,
        KirbyAmDeathLink,
    ]),
    OptionGroup("Ability Randomization", [
        AbilityRandomizationMode,
        AbilityRandomizationBossSpawns,
        AbilityRandomizationMinibosses,
        AbilityRandomizationMinny,
        AbilityRandomizationPassiveEnemies,
        AbilityRandomizationNoAbilityWeight,
    ]),
]
