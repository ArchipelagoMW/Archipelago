from Options import Toggle, Choice, NamedRange, Range


class GoldenCoins(Choice):
    """Vanilla: The coins are found in their original locations.
    Shuffled: The coins are shuffled into the item pool.
    Progressive: The coins are at the end of the Level Progression chains. For example, there will be a third
    Space Zone Progression item, and the final one received will grant the Space Coin.

    You will see a Golden Coin being received when defeating bosses regardless of whether you are actually getting a coin."""
    display_name = "Golden Coins"
    option_vanilla = 0
    option_shuffled = 1
    option_progressive = 2
    default = 0


class GoldenCoinsRequired(Range):
    """Number of Golden Coins required to enter Wario's Castle."""
    display_name = "Golden Coins Required"
    range_start = 0
    range_end = 6
    default = 6


class DifficultyMode(Choice):
    """Play in normal or easy mode. You can also start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "Trap" in the item pool."""
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


class ShufflePipeTraversal(Toggle):
    """Shuffle a Pipe Traversal item into the item pool, which is required to enter pipes.
    Note that being unable to enter pipes is very limiting and affects nearly half of all levels."""
    display_name = "Shuffle Pipe Traversal"


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
    special_range_names = {"vanilla": -1}
    default = -1


class AutoScrollTrap(Toggle):
    """If on, auto scroll levels will not auto scroll until you've received the Auto Scroll trap item."""
    display_name = "Auto Scroll Trap"


class RandomizeMusic(Toggle):
    """Randomize the music that plays in levels and overworld areas."""
    display_name = "Randomize Music"


sml2options = {
    "golden_coins": GoldenCoins,
    "required_golden_coins": GoldenCoinsRequired,
    "difficulty_mode": DifficultyMode,
    "shuffle_midway_bells": ShuffleMidwayBells,
    "shuffle_pipe_traversal": ShufflePipeTraversal,
    "randomize_enemies": RandomizeEnemies,
    "randomize_platforms": RandomizePlatforms,
    "auto_scroll_levels": AutoScrollLevels,
    "auto_scroll_trap": AutoScrollTrap,
    "randomize_music": RandomizeMusic
}