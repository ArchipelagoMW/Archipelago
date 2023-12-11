from Options import Toggle, Choice, NamedRange


class GoldenCoins(Choice):
    """Vanilla: The coins are found in their original locations.
    Shuffled: The coins are shuffled into the item pool.
    Progressive: The coins are at the end of the Progressive Level item chains. For example, there will be a third
    Progressive Space Zone item, and the final one received will grant the Space Coin.

    You will see a Golden Coin being received when defeating bosses regardless of whether you are actually getting a coin."""
    display_name = "Golden Coins"
    option_vanilla = 0
    option_shuffled = 1
    option_progressive = 2
    default = 0


class DifficultyMode(Choice):
    """Play in normal or easy mode. You can also start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "Trap" in the item pool."""
    display_name = "Difficulty Mode"
    option_normal = 0
    option_easy = 1
    option_normal_to_easy = 2
    option_easy_to_normal = 3
    default = 0


class ShuffleSpacePhysics(Toggle):
    """Oh, no! There is Earth gravity on the moon and in space! Find the missing Space Physics item to restore
    proper order to the universe."""
    display_name = "Shuffle Space Physics"


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
    range_end = 20
    special_range_names = {"vanilla": -1}


class RandomizeMusic(Toggle):
    """Randomize the music that plays in levels and overworld areas."""
    display_name = "Randomize Music"


sml2options = {
    "golden_coins": GoldenCoins,
    "difficulty_mode": DifficultyMode,
    "shuffle_space_physics": ShuffleSpacePhysics,
    "randomize_enemies": RandomizeEnemies,
    "randomize_platforms": RandomizePlatforms,
    "auto_scroll_levels": AutoScrollLevels,
    "randomize_music": RandomizeMusic
}