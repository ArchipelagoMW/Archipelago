from dataclasses import dataclass

from Options import DeathLinkMixin, DefaultOnToggle, OptionCounter, OptionSet, PerGameCommonOptions, Range, Toggle


ESSENTIAL_ITEMS = frozenset({
    "Graphics",
    "Progressive Room",
    "Bombs",
    "Gun",
    "Fire",
    "Sword",
    "Pickaxe",
    "Water Walkers",
    "Tank Treads",
    "Tank Chassis",
    "Tank Cannon",
    "SFX",
    "BGM",
})

MAX_RESOURCE_UPGRADES = frozenset({
    "Max HP",
    "Max Rounds",
})

TRAPS = frozenset({
    "Stun Trap",
    "Invisible Trap",
    "Fast Trap",
    "Slow Trap",
    "Reverse Trap",
    "Screen Flip Trap",
    "Zoom In Trap",
    "Instant Death Trap",
    "Snake Trap",
})

class ShuffleEssentialItems(DefaultOnToggle):
    """Shuffle essential Shellipelago progression items."""

    display_name = "Shuffle Essential Items"


class ShuffleMaxResourceUpgrades(DefaultOnToggle):
    """Shuffle max HP and max rounds upgrades."""

    display_name = "Shuffle Max Resource Upgrades"


class AddEasyDestructibleChecks(Toggle):
    """Add destructible tiles as locations."""

    display_name = "Add Destructible Tiles to Locations"


class EnemiesAreChecks(Toggle):
    """Add defeated enemies as locations."""

    display_name = "Add Enemies to Locations"


class ShuffleShops(DefaultOnToggle):
    """Shuffle shop item locations. Fixed shop progression can still be shuffled when this is off."""

    display_name = "Shuffle Shops"


class EnemiesAreHints(Toggle):
    """Defeated enemies can create Archipelago hints for useful Shellipelago locations."""

    display_name = "Enemies Are Hints"


class ShowEssentialPickupHints(DefaultOnToggle):
    """Show special graphics for essential pickups in the client."""

    display_name = "Show Essential Pickup Hints"


class AddTrapsToPool(Toggle):
    """Allow trap items to be placed as rewards. Vanilla trap locations become filler when this is off."""

    display_name = "Add Traps To Pool"


class TrapFillPercentage(Range):
    """Percentage of filler item slots that will be replaced with traps."""

    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 25


class TrapPoolSpawn(OptionSet):
    """Trap types that can spawn from the trap item pool."""

    display_name = "Trap Pool Spawn"
    valid_keys = TRAPS
    default = TRAPS


class TrapWeights(OptionCounter):
    """Relative weights for traps in the item pool. Set a trap to 0 to prevent it from appearing."""

    display_name = "Trap Weights"
    valid_keys = TRAPS
    min = 0
    default = {trap_name: 1 for trap_name in sorted(TRAPS)}


class OtherPlayersCanFindItemPoolDrops(Toggle):
    """Expose item-pool-only drops as Archipelago locations."""

    display_name = "Other Players Can Find Item Pool Drops"


class RingLink(Toggle):
    """Sync Rounds with rings in other games that have Ring Link enabled.
    As rounds are spent and gained, ring and round counts fluctuate for all players with this option enabled.
    """

    display_name = "Ring Link"


class EnergyLink(Toggle):
    """Sync Energy with other clients that have Energy Link enabled.
    """

    display_name = "Energy Link"


class TrapLink(Toggle):
    """Send linked traps to other players with Trap Link enabled.
    If another linked game supports the received trap effect, that game applies the same trap.
    """

    display_name = "Trap Link"


@dataclass
class ShellipelagoOptions(PerGameCommonOptions, DeathLinkMixin):
    shuffle_essential_items: ShuffleEssentialItems
    shuffle_max_resource_upgrades: ShuffleMaxResourceUpgrades
    add_easy_destructible_checks: AddEasyDestructibleChecks
    enemies_are_checks: EnemiesAreChecks
    enemies_are_hints: EnemiesAreHints
    shuffle_shops: ShuffleShops
    show_essential_pickup_hints: ShowEssentialPickupHints
    add_traps_to_pool: AddTrapsToPool
    trap_fill_percentage: TrapFillPercentage
    trap_pool_spawn: TrapPoolSpawn
    trap_weights: TrapWeights
    other_players_can_find_item_pool_drops: OtherPlayersCanFindItemPoolDrops
    ring_link: RingLink
    energy_link: EnergyLink
    trap_link: TrapLink
