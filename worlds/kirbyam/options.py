"""
Option definitions for Kirby & The Amazing Mirror
"""
from dataclasses import dataclass

from Options import (
    Choice,
    DeathLink,
    ExcludeLocations,
    ItemLinks,
    LocalItems,
    NonLocalItems,
    PerGameCommonOptions,
    PlandoItems,
    PriorityLocations,
    StartHints,
    StartInventory,
    StartLocationHints,
    Toggle,
    Visibility,
)


class Goal(Choice):
    """
    Determines what your goal is to consider the game beaten.

    - Dark Mind: Defeat Dark Mind and beat the game.
    """
    display_name = "Goal"
    default = 0
    option_dark_mind = 0

    @classmethod
    def from_any(cls, data: object) -> "Goal":
        """Coerce legacy goal values (removed in v0.0.12) to Dark Mind."""
        if type(data) is int and data in {1, 2, 100}:
            return cls(cls.option_dark_mind)
        if isinstance(data, str) and data.lower() in {"1", "2", "100", "debug"}:
            return cls(cls.option_dark_mind)
        return super().from_any(data)  # type: ignore[return-value]


class RandomizeShards(Choice):
    """
    Controls where Mirror Shards can appear.

    - Vanilla: Each area's boss defeat location contains its matching shard.
    - Completely Random: Shards can appear at any physical check (boss and non-boss).
    """
    display_name = "Randomize Shards"
    default = 2
    option_vanilla = 0
    option_completely_random = 2


class EnemyCopyAbilityRandomization(Choice):
        """
        Controls randomization of enemy-granted copy abilities.

        - Vanilla: Enemy copy abilities stay at native defaults.
        - Shuffled: Experimental. Enemy types are remapped deterministically so
            all enemies of the same type grant the same ability.
        - Completely Random: Experimental. Eligible enemy ability sources are
            remapped independently (deterministic per source entry). Hidden
            from the generated player template for the first public build.
        """
        display_name = "Enemy Copy-Ability Randomization"
        default = 0
        option_vanilla = 0
        option_shuffled = 1
        option_completely_random = 2
        template_excluded_choices = frozenset({"completely_random"})


class RandomizeBossSpawnedAbilityGrants(Toggle):
    """Whether boss-spawned ability grants are randomized. Only applies when Enemy Copy-Ability Randomization is not Vanilla."""
    display_name = "Randomize Boss-Spawned Ability Grants"
    default = 1


class RandomizeMiniBossAbilityGrants(Toggle):
    """Whether mini-boss ability grants are randomized. Only applies when Enemy Copy-Ability Randomization is not Vanilla."""
    display_name = "Randomize Mini-Boss Ability Grants"
    default = 1


class EnableDebugLogging(Toggle):
    """Enable extra BizHawk client diagnostics for gameplay-state and mailbox delivery troubleshooting."""
    display_name = "Enable Debug Logging"
    default = 0


class RoomSanity(Toggle):
    """Adds room-visit checks (Room X-YY). Disabled by default because it adds 257 locations."""
    display_name = "Room Sanity"
    default = 0


class KirbyAmDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__


class _HiddenOptionMixin:
    # Hide unsupported common options from KirbyAM templates/UI while preserving
    # the underlying option types so external configs still parse consistently.
    # Visibility.none (not the "Removed" mechanism) is intentional: external
    # YAML configs that set these keys still parse without error rather than
    # failing fast, which keeps forward compatibility for shared multiworld configs.
    visibility = Visibility.none


class HiddenLocalItems(_HiddenOptionMixin, LocalItems):
    pass


class HiddenNonLocalItems(_HiddenOptionMixin, NonLocalItems):
    pass


class HiddenStartInventory(_HiddenOptionMixin, StartInventory):
    pass


class HiddenStartHints(_HiddenOptionMixin, StartHints):
    pass


class HiddenStartLocationHints(_HiddenOptionMixin, StartLocationHints):
    pass


class HiddenExcludeLocations(_HiddenOptionMixin, ExcludeLocations):
    pass


class HiddenPriorityLocations(_HiddenOptionMixin, PriorityLocations):
    pass


class HiddenItemLinks(_HiddenOptionMixin, ItemLinks):
    pass


class HiddenPlandoItems(_HiddenOptionMixin, PlandoItems):
    pass


@dataclass
class KirbyAmOptions(PerGameCommonOptions):
    local_items: HiddenLocalItems
    non_local_items: HiddenNonLocalItems
    start_inventory: HiddenStartInventory
    start_hints: HiddenStartHints
    start_location_hints: HiddenStartLocationHints
    exclude_locations: HiddenExcludeLocations
    priority_locations: HiddenPriorityLocations
    item_links: HiddenItemLinks
    plando_items: HiddenPlandoItems

    goal: Goal

    shards: RandomizeShards

    enemy_copy_ability_randomization: EnemyCopyAbilityRandomization

    randomize_boss_spawned_ability_grants: RandomizeBossSpawnedAbilityGrants

    randomize_miniboss_ability_grants: RandomizeMiniBossAbilityGrants

    room_sanity: RoomSanity

    enable_debug_logging: EnableDebugLogging

    death_link: KirbyAmDeathLink


OPTION_GROUPS = []
