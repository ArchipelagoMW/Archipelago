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


class Goal(Choice):
    """Defines the goal to accomplish in order to complete the randomizer.
    Full Story In Order: Complete each act in order. You can return to previously completed acts.
    Full Story Any Order: Complete each act in any order. All acts are available from the start.
    First Act: Complete Act 1 by finding the New Game button. Great for a smaller scale randomizer."""
    auto_display_name = True
    display_name = "Goal"
    option_full_story_in_order = 0
    option_full_story_any_order = 1
    option_first_act = 2


class RandomizeCodes(Toggle):
    """Randomize codes and passwords in the game(clocks, safes, etc.)"""
    display_name = "Randomize Codes"


class RandomizeDeck(Choice):
    """Randomize cards in your deck into new cards.
    Disable: Disable the feature.
    Every Encounter Within Same Type: Randomize cards within the same type every encounter (keep rarity/scrybe type).
    Every Encounter Any Type: Randomize cards into any possible card every encounter.
    Starting Only: Only randomize cards given at the beginning of runs and acts."""
    auto_display_name = True
    display_name = "Randomize Deck"
    option_disable = 0
    option_every_encounter_within_same_type = 1
    option_every_encounter_any_type = 2
    option_starting_only = 3


class RandomizeSigils(Choice):
    """Randomize sigils printed on the cards into new sigils every encounter.
    Disable: Disable the feature.
    Randomize Addons: Only randomize sigils added from sacrifices or other means.
    Randomize All: Randomize all sigils."""
    auto_display_name = True
    display_name = "Randomize Abilities"
    option_disable = 0
    option_randomize_addons = 1
    option_randomize_all = 2


class OptionalDeathCard(Choice):
    """Add a moment after death in act 1 where you can decide to create a death card or not.
    Disable: Disable the feature.
    Always on: The choice is always offered after losing all candles.
    DeathLink Only: The choice is only offered after receiving a DeathLink event."""
    auto_display_name = True
    display_name = "Optional Death Card"
    option_disable = 0
    option_always_on = 1
    option_deathlink_only = 2


class SkipTutorial(Toggle):
    """Skips the first few tutorial runs of act 1. Bones are available from the start."""
    display_name = "Skip Tutorial"
    default = 1


class SkipEpilogue(Toggle):
    """Completes the goal as soon as the required acts are completed without the need of completing the epilogue."""
    display_name = "Skip Epilogue"


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


class PaintingChecksBalancing(Choice):
    """Generation options for the second and third painting checks in act 1.
    None: Adds no progression logic to these painting checks. They will all count as sphere 1 (early game checks).
    Balanced: Adds rules to these painting checks. Early game items are less likely to appear into these paintings.
    Force Filler: For when you dislike doing these last two paintings. Their checks will only contain filler items."""
    auto_display_name = True
    display_name = "Painting Checks Balancing"
    option_none = 0
    option_balanced = 1
    option_force_filler = 2

@dataclass
class InscryptionOptions(PerGameCommonOptions):
    deathlink: DeathLink
    act1_deathlink_behaviour: Act1DeathLinkBehaviour
    goal: Goal
    randomize_codes: RandomizeCodes
    randomize_deck: RandomizeDeck
    randomize_sigils: RandomizeSigils
    optional_death_card: OptionalDeathCard
    skip_tutorial: SkipTutorial
    skip_epilogue: SkipEpilogue
    epitaph_pieces_randomization: EpitaphPiecesRandomization
    painting_checks_balancing: PaintingChecksBalancing
