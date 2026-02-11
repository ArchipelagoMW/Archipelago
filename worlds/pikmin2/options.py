from dataclasses import dataclass
from Options import Range, Choice, PerGameCommonOptions

class WinCondition(Choice):
    """
    Collect Louie: Beat the Titan Dweevil and collect the King of Bugs
    Collect Pokos: Collect a certain number of Pokos, defined by the poko_amount value. Logic and the client do not account for Pokos obtained from enemy corpses.
    Collect Treasure: Collect a certain number of treasures, defined by the treasure_amount value.
    """
    display_name = "Win Condition"
    option_collect_louie = 0
    option_collect_pokos = 1
    option_collect_treasure = 2
    default = 0

class PokoAmount(Range):
    """
    When Collect Pokos is selected as the goal, this will control how many Pokos are needed to beat the game. Does nothing in other goals.
    """
    display_name = "Poko Amount"
    range_start = 0
    range_end = 26985
    default = 10000

class TreasureAmount(Range):
    """
    When Collect Treasures is selected as the goal, this will control how many treasures are needed to beat the game. Does nothing in other goals.
    """
    display_name = "Treasure Amount"
    range_start = 1
    range_end = 201
    default = 201

class Debt(Range):
    """
    Controls how many Pokos need to be collected before Wistful Wild can be accessed. 
    """
    display_name = "Debt"
    range_start = 1
    range_end = 15000
    default = 10000

class ShuffleCaves(Choice):
    """
    Controls the settings for cave shuffling.

    No Shuffle: Caves are in their vanilla locations.
    Keep Dream Den: Dream Den's location does not change, but all other caves are shuffled.
    Wistful Wild Lock: The Wistful Wild caves are guaranteed to be shuffled within Wistful Wild, all other caves are shuffled wherever.
    Full Shuffle: All caves are shuffled.

    If caves are shuffled, Violet Candypop Buds will appear outside of Emergence Cave, and Ivory Candypop Buds will appear in Awakening Wood by the ship.
    """
    display_name = "Shuffle Caves"
    option_no_shuffle = 0
    option_keep_dream_den = 1
    option_wistful_wild_lock = 2
    option_full_shuffle = 3
    default = 0

class CaveKeys(Choice):
    """
    Controls whether caves are open or closed.

    All Unlocked: All caves are accessible as in vanilla.
    All Locked: Caves require a key to unlock.

    The keys will always unlock a cave's vanilla location. For example, if you collect the Emergence Cave Entrance Key, it will always unlock the first cave
    in Valley of Repose, no matter what cave has been shuffled to that location.

    Cave keys use the The Key model in game.
    """
    display_name = "Cave Keys"
    option_all_unlocked = 0
    option_all_locked = 1

class DeathLink(Choice):
    """
    Controls Death Link settings.

    No Deathlink: Deaths will not be sent or received.
    Pikmin Extinction: Deaths received will cause all active Pikmin to die.
    Captain Death: Deaths received will cause one of the two captains to die.
    Full Random: Deaths received will either cause a Pikmin extinction or a captain death.

    Deaths will be sent to other games if a Pikmin extinction that ends the day occurs or if both captains die.
    """
    display_name = "Death Link"
    option_no_deathlink = 0
    option_pikmin_extinction = 1
    option_captain_death = 2
    option_full_random = 3

class BossRando(Choice):
    """
    Controls boss randomization settings.

    Vanilla: Bosses will be in their vanilla locations.
    Shuffle: Bosses will be shuffled.
    Full Random: Bosses will be completely random.
    """
    display_name = "Boss Rando"
    option_vanilla = 0
    option_shuffle = 1
    option_full_random = 2

class EnemyRando(Choice):
    """
    Controls enemy randomization settings.
    Note that this only works in caves.

    Vanilla: Enemies will be in their vanilla locations.
    Full Random: Enemies will be completely random.
    """
    display_name = "Enemy Rando"
    option_vanilla = 0
    option_full_random = 1

class BossAndEnemyRando(Choice):
    """
    Randomizes bosses and enemies together, allowing enemies to be in boss spots and bosses to be in enemy spots.
    This setting overrides the enemy rando and boss rando options.
    Note that this setting only works in caves, and is extremely experimental and may cause crashes.

    No: Enemies and bosses will be randomized according to the Boss Rando and Enemy Rando settings. 
    Yes: Completely randomize all bosses and enemies. Enemies may be randomized to boss locations, and bosses may be randomized to enemy locations. Overrides other boss/enemy rando settings.
    """
    display_name = "Boss and Enemy Rando"
    option_no = 0
    option_yes = 1

class SublevelShuffle(Choice):
    """
    Controls sublevel shuffle settings.

    Vanilla: Sublevels are played through in their normal order.
    Shuffled: Sublevels within each cave are shuffled.
    """
    display_name = "Sublevel Shuffle"
    option_vanilla = 0
    option_shuffled = 1

class OnionShuffle(Choice):
    """
    Controls onion shuffle settings.

    Vanilla: Onions will be in their vanilla locations.
    Shuffle: Onions will be shuffled.
    Exclude Vanilla: Onions will be shuffled, and the onions will not be in their vanilla arrangement (Red in Vor, Blue in AW, Yellow in PP).
    In Pool: Onions will be added to the pool. Starting onion will be random.
    
    The water around the Blue Onion in Awakening Wood will always be removed. The electric gate will be replaced with a normal gate if the Yellow Onion is in Awakening Wood.
    """
    display_name = "Onion Shuffle"
    option_vanilla = 0
    option_shuffle = 1
    option_exclude_vanilla = 2
    option_in_pool = 3

class ProgressiveGlobes(Choice):
    """
    Controls whether globes are progressive or not.

    Non Progressive: Globes will unlock their vanilla area (Spherical Atlas will unlock Awakening Wood, Geographic Projection will unlock Perplexing Pool).
    Progressive: The first collected globe will unlock Awakening Wood, and the second will unlock Perplexing Pool.
    """
    display_name = "Progressive Globes"
    option_non_progressive = 0
    option_progressive = 1

class WeaponsInPool(Choice):
    """
    Controls whether the Titan Dweevil's weapons can appear in the pool.

    No: The Titan Dweevil's weapons will only appear on the Titan Dweevil.
    Yes: The Titan Dweevil's weapons will appear on the Titan Dweevil and also in the pool. Collecting a weapon from the pool (i.e., before the fight) will remove it from the fight completely.
    Collecting all four weapons before the fight will completely trivialize it.
    """
    display_name = "Titan Dweevil Weapons In Pool"
    option_no = 0
    option_yes = 1

class TreasureCollectionChecks(Choice):
    """
    Controls whether checks are added for collecting certain numbers of treasure.

    No: Checks will only exist at in-game locations.
    Yes: Checks will be added at certain treasure collection intervals, controllable by other options.
    """
    display_name = "Treasure Collection Checks"
    option_no = 0
    option_yes = 1

class TreasureCollectionStartValue(Range):
    """
    If treasure collection checks are enabled, they will be added starting at this number of treasures collected.
    For example, if this is set to 5, the first treasure collection check will be granted by collecting 5 treasures.
    """
    display_name = "Treasure Collection Start"
    range_start = 1
    range_end = 201
    default = 5

class TreasureCollectionEndValue(Range):
    """
    If treasure collection checks are enabled, they will be added ending at this number of treasures collected.
    For example, if this is set to 195, the last treasure collection check will be granted by collecting 195 treasures.
    """
    display_name = "Treasure Collection End"
    range_start = 1
    range_end = 201
    default = 200

class TreasureCollectionInterval(Range):
    """
    If treasure collection checks are enabled, they will be added at this interval.
    For example, the starting value is 5, the ending value is 50, and the interval is 10, treasure collection checks will be granted when 5, 15, 25, 35, and 45 treasures are collected.
    """
    display_name = "Treasure Collection Interval"
    range_start = 1
    range_end = 201
    default = 5

class PokoCollectionChecks(Choice):
    """
    Controls whether checks are added for collecting pokos. Checks will be added at 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, and 100% of the user-selected debt,
    coinciding with the in-game messages.

    No: Checks will only exist at in-game locations.
    Yes: Checks will be added at the poko collection interval specified above.
    """
    display_name = "Poko Collection Checks"
    option_no = 0
    option_yes = 1
    
@dataclass
class Pikmin2Options(PerGameCommonOptions):
    win_condition: WinCondition
    poko_amount: PokoAmount
    treasure_amount: TreasureAmount
    debt: Debt
    shuffle_caves: ShuffleCaves
    cave_keys: CaveKeys
    death_link: DeathLink
    boss_rando: BossRando
    enemy_rando: EnemyRando
    boss_and_enemy_rando: BossAndEnemyRando
    sublevel_shuffle: SublevelShuffle
    onion_shuffle: OnionShuffle
    progressive_globes: ProgressiveGlobes
    weapons_in_pool: WeaponsInPool
    treasure_collection_checks: TreasureCollectionChecks
    treasure_collection_start_value: TreasureCollectionStartValue
    treasure_collection_end_value: TreasureCollectionEndValue
    treasure_collection_interval: TreasureCollectionInterval
    poko_collection_checks: PokoCollectionChecks