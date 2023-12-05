from Options import Toggle, Choice, Range, NamedRange, TextChoice, DeathLink

class DifficultyMode(Choice):
    """Start in Normal Mode with an "upgrade" to Easy Mode in the item pool,
    or start in Easy Mode with a Normal Mode "Trap" in the item pool"""
    display_name = "Difficulty Mode"
    option_normal_to_easy = 0
    option_easy_to_normal = 1
    default = 0

sml2options = {
    "difficulty_mode": DifficultyMode
}