from dataclasses import dataclass

from Options import DefaultOnToggle, OptionSet, PerGameCommonOptions, Toggle


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
    "Energy",
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
    "Zoom Trap",
    "Death Trap",
    "Suddenly Snake",
})


class ShuffleEssentialItems(DefaultOnToggle):
    """Shuffle essential Shellipelago progression items."""

    display_name = "Shuffle Essential Items"


class EssentialItemsInMyWorld(OptionSet):
    """Essential items allowed to appear in this player's world."""

    display_name = "Essential Items In My World"
    valid_keys = ESSENTIAL_ITEMS
    default = ESSENTIAL_ITEMS


class EssentialItemsInOtherWorlds(OptionSet):
    """Essential items allowed to appear in other players' worlds."""

    display_name = "Essential Items In Other Worlds"
    valid_keys = ESSENTIAL_ITEMS
    default = ESSENTIAL_ITEMS


class ShuffleMaxResourceUpgrades(DefaultOnToggle):
    """Shuffle max HP and max rounds upgrades."""

    display_name = "Shuffle Max Resource Upgrades"


class MaxResourceUpgradesInMyWorld(OptionSet):
    """Max resource upgrades allowed to appear in this player's world."""

    display_name = "Max Resource Upgrades In My World"
    valid_keys = MAX_RESOURCE_UPGRADES
    default = MAX_RESOURCE_UPGRADES


class MaxResourceUpgradesInOtherWorlds(OptionSet):
    """Max resource upgrades allowed to appear in other players' worlds."""

    display_name = "Max Resource Upgrades In Other Worlds"
    valid_keys = MAX_RESOURCE_UPGRADES
    default = MAX_RESOURCE_UPGRADES


class AddEasyDestructibleChecks(Toggle):
    """Add normal destructible objects as checks."""

    display_name = "Add Easy Destructible Checks"


class EnemiesAreChecks(Toggle):
    """Enemies grant checks when defeated."""

    display_name = "Enemies Are Checks"


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


class TrapPoolSpawn(OptionSet):
    """Trap types that can spawn from the trap item pool."""

    display_name = "Trap Pool Spawn"
    valid_keys = TRAPS
    default = TRAPS


class TrapPoolInMyWorld(OptionSet):
    """Trap items allowed in this player's world."""

    display_name = "Trap Pool In My World"
    valid_keys = TRAPS
    default = TRAPS


class TrapPoolInOtherWorlds(OptionSet):
    """Trap items allowed in other players' worlds."""

    display_name = "Trap Pool In Other Worlds"
    valid_keys = TRAPS
    default = TRAPS


class OtherPlayersCanFindItemPoolDrops(Toggle):
    """Expose item-pool-only drops as Archipelago locations."""

    display_name = "Other Players Can Find Item Pool Drops"


class RingLink(Toggle):
    """Enable Ring Link."""

    display_name = "Ring Link"


class EnergyLink(Toggle):
    """Enable Energy Link."""

    display_name = "Energy Link"


class DeathLink(Toggle):
    """Enable Death Link."""

    display_name = "Death Link"


class TrapLink(Toggle):
    """Enable Trap Link."""

    display_name = "Trap Link"


class ItemLink(Toggle):
    """Enable Item Link."""

    display_name = "Item Link"


@dataclass
class ShellipelagoOptions(PerGameCommonOptions):
    shuffle_essential_items: ShuffleEssentialItems
    essential_items_in_my_world: EssentialItemsInMyWorld
    essential_items_in_other_worlds: EssentialItemsInOtherWorlds
    shuffle_max_resource_upgrades: ShuffleMaxResourceUpgrades
    max_resource_upgrades_in_my_world: MaxResourceUpgradesInMyWorld
    max_resource_upgrades_in_other_worlds: MaxResourceUpgradesInOtherWorlds
    add_easy_destructible_checks: AddEasyDestructibleChecks
    enemies_are_checks: EnemiesAreChecks
    enemies_are_hints: EnemiesAreHints
    shuffle_shops: ShuffleShops
    show_essential_pickup_hints: ShowEssentialPickupHints
    add_traps_to_pool: AddTrapsToPool
    trap_pool_spawn: TrapPoolSpawn
    trap_pool_in_my_world: TrapPoolInMyWorld
    trap_pool_in_other_worlds: TrapPoolInOtherWorlds
    other_players_can_find_item_pool_drops: OtherPlayersCanFindItemPoolDrops
    ring_link: RingLink
    energy_link: EnergyLink
    death_link: DeathLink
    trap_link: TrapLink
    item_link: ItemLink
