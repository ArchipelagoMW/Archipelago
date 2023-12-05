from dataclasses import dataclass

from Options import Toggle, Choice, Option, PerGameCommonOptions
import typing


class DeathLink(Toggle):
    """Activate DeathLink"""
    display_name = "DeathLink"


class Act1DeathLinkBehaviour(Choice):
    """If DeathLink is enabled, determines what counts as a death in act 1. This affects deaths sent and received.
    Sacrificed: Send a death when sacrificed by Leshy. Receiving a death will extinguish all candles.
    Candle Extinguished: Send a death when a candle is extinguished. Receiving a death will extinguish a candle."""
    auto_display_name = True
    display_name = "Act 1 DeathLink Behaviour"
    option_sacrificed = 0
    option_candle_extinguished = 1


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


class EpitaphPiecesRandomization(Choice):
    """Determines how epitaph pieces in act 2 are randomized. This can affect your chances of getting stuck.
    All Pieces: Randomizes all nine pieces as their own item.
    In Groups: Randomizes pieces in groups of three.
    As One Item: Group all nine pieces as a single item."""
    auto_display_name = True
    display_name = "Epitaph Pieces Randomization"
    option_all_pieces = 0
    option_in_groups = 1
    option_as_one_item = 2


@dataclass
class InscryptionOptions(PerGameCommonOptions):
    deathlink: DeathLink
    act1_deathlink_behaviour: Act1DeathLinkBehaviour
    trap: Trap
    goal: Goal
    randomize_codes: RandomizeCodes
    randomize_deck: RandomizeDeck
    randomize_abilities: RandomizeAbilities
    optional_death_card: OptionalDeathCard
    skip_tutorial: SkipTutorial
    epitaph_pieces_randomization: EpitaphPiecesRandomization
