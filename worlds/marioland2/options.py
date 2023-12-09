from Options import Toggle, Choice, Range, NamedRange, TextChoice, DeathLink


class DifficultyMode(Choice):
    """Start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "Trap" in the item pool."""
    display_name = "Difficulty Mode"
    option_normal_to_easy = 0
    option_easy_to_normal = 1
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


class RandomizeAutoScrollLevels(Toggle):
    """Randomize which three levels have auto-scrolling."""
    display_name = "Randomize Auto Scroll Levels"


sml2options = {
    "difficulty_mode": DifficultyMode,
    "shuffle_space_physics": ShuffleSpacePhysics,
    "randomize_enemies": RandomizeEnemies,
    "randomize_platforms": RandomizePlatforms,
    "randomize_auto_scroll_levels": RandomizeAutoScrollLevels,
}