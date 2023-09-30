from Options import Toggle, Range, Choice, Option
import typing


class DeathLink(Toggle):
    """Activate DeathLink"""
    display_name = "DeathLink"


class Trap(Toggle):
    """Put some traps in the item pool"""
    display_name = "Trap"


class Goal(Choice):
    """Defines the goal to accomplish in order to complete the randomizer.
    Full Story In Order: Complete each act and the epilogue in order. You can return to previously completed acts.
    Full Story Any Order: Complete each act in any order, then the epilogue. All acts are available from the start.
    First Act: Complete Act 1 by finding the New Game button. Great for a smaller scale randomizer."""
    auto_display_name = True
    display_name = "Goal"
    option_full_story_in_order = 0
    option_full_story_any_order = 1
    option_first_act = 2


class RandomizeCodes(Toggle):
    """Randomize All codes in the game(Clock, safe, etc.)"""
    display_name = "Randomize Codes"


class RandomizeDeck(Choice):
    """Randomize cards in your deck for all 3 acts.
    Disable: Disable the feature.
    Randomize Within Same Type: Randomize card within the same type (A rare card will randomize to another rare card).
    Randomize All: Randomize card to any possible card."""
    auto_display_name = True
    display_name = "Randomize Deck"
    option_disable = 0
    option_randomize_within_same_type = 1
    option_randomize_all = 2


class RandomizeAbilities(Choice):
    """Randomize abilities in all 3 acts.
    Disable: Disable the feature.
    Randomize Modded: Randomize added ability only.
    Randomize All: Randomize all abilities."""
    auto_display_name = True
    display_name = "Randomize Abilities"
    option_disable = 0
    option_randomize_modded = 1
    """option_randomize_all = 2"""


class OptionalDeathCard(Choice):
    """Add a moment after death in act 1 where you can decide to create a death card or not.
    Disable: Disable the feature.
    Always on: The feature is always on.
    DeathLink Only: The feature only happens during a DeathLink death."""
    auto_display_name = True
    display_name = "Optional Death Card"
    option_disable = 0
    option_always_on = 1
    option_deathlink_only = 2


class SkipTutorial(Toggle):
    """Skips the first few tutorial runs of act 1. Bones are available from the start."""
    display_name = "Skip Tutorial"
    default = 1


inscryption_options: typing.Dict[str, type(Option)] = {
    "deathlink": DeathLink,
    "trap": Trap,
    "goal": Goal,
    "randomize_codes": RandomizeCodes,
    "randomize_deck": RandomizeDeck,
    "randomize_abilities": RandomizeAbilities,
    "optional_death_card": OptionalDeathCard,
    "skip_tutorial": SkipTutorial
}
