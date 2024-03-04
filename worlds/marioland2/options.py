from Options import Toggle, Choice, NamedRange, Range, PerGameCommonOptions
from dataclasses import dataclass


class GoldenCoins(Toggle):
    """Shuffle the Golden Coins into the item pool.
    You will see a Golden Coin being received when defeating bosses regardless of whether you are actually getting a coin."""
    display_name = "Coinsanity"
    default = 0


class GoldenCoinsRequired(Range):
    """Number of Golden Coins required to enter Wario's Castle."""
    display_name = "Golden Coins Required"
    range_start = 0
    range_end = 6
    default = 6


class DifficultyMode(Choice):
    """Play in normal or easy mode. You can also start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "trap" in the item pool."""
    display_name = "Difficulty Mode"
    option_normal = 0
    option_easy = 1
    option_normal_to_easy = 2
    option_easy_to_normal = 3
    default = 0


class ShuffleMidwayBells(Toggle):
    """Shuffle the Midway Bells into the item pool. Ringing a bell will trigger a location check.
    Obtaining a Midway Bell will be permanent, and some levels will require backtracking from the midway point to reach
    secret exits."""
    display_name = "Shuffle Midway Bells"


class ShufflePipeTraversal(Choice):
    """Single: Shuffle a Pipe Traversal item into the item pool, which is required to enter any pipes.
    Split: Shuffle 4 Pipe Traversal items, one required for entering pipes from each direction.
    Note that being unable to enter pipes is very limiting and affects nearly half of all levels."""
    display_name = "Shuffle Pipe Traversal"
    option_off = 0
    option_single = 1
    option_split = 2
    default = 0


class RandomizeEnemies(Toggle):
    """Randomize enemies throughout levels."""
    display_name = "Randomize Enemies"


class RandomizePlatforms(Toggle):
    """Randomize platforms throughout levels."""
    display_name = "Randomize Platforms"


class AutoScrollLevels(NamedRange):
    """Keep auto scroll levels vanilla or choose a number of levels to be randomly selected to have auto-scrolling.
    Certain levels are excluded."""
    display_name = "Auto Scroll Levels"
    range_start = 0
    range_end = 18
    special_range_names = {"vanilla": -1, "none": 0, "all": 18}
    default = -1


class AutoScrollTrap(Toggle):
    """If on, auto scroll levels will not auto scroll until you've received the Auto Scroll trap item."""
    display_name = "Auto Scroll Trap"


class RandomizeMusic(Toggle):
    """Randomize the music that plays in levels and overworld areas."""
    display_name = "Randomize Music"


class EnergyLink(Toggle):
    """All extra lives beyond 1 are transferred into the server's shared EnergyLink storage. If you drop to 0,
    1 will be replenished if there is sufficient energy stored."""
    display_name = "Energy Link"
    default = 1

@dataclass
class SML2Options(PerGameCommonOptions):
    coinsanity: GoldenCoins
    required_golden_coins: GoldenCoinsRequired
    difficulty_mode: DifficultyMode
    shuffle_midway_bells: ShuffleMidwayBells
    shuffle_pipe_traversal: ShufflePipeTraversal
    randomize_enemies: RandomizeEnemies
    randomize_platforms: RandomizePlatforms
    auto_scroll_levels: AutoScrollLevels
    auto_scroll_trap: AutoScrollTrap
    randomize_music: RandomizeMusic
    energy_link: EnergyLink
