from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, OptionDict, PerGameCommonOptions, Range, Toggle


class RetirementYear(Range):
    """The goal is always to keep your studio alive until you retire in this year.
    The vanilla campaign ends at Year 35.
    Go bankrupt and the game is over, so you'll have to load a save and try again."""

    display_name = "Retirement Year"
    range_start = 20
    range_end = 50
    default = 35


class SuccessLevel(Choice):
    """How successful your studio must be when you retire.
    - Just Retire: Reaching the retirement year is enough.
    - Millionaire: Retire with at least $10,000,000 in Cash and 100,000 Fans.
    - Tycoon: Retire with at least $100,000,000 in Cash and 1,000,000 Fans.
    If you reach the retirement year short of the target, keep playing: you win as soon as you hit it."""

    display_name = "Retirement Success Level"
    option_just_retire = 0
    option_millionaire = 1
    option_tycoon = 2
    default = 0


class FriendlyStart(DefaultOnToggle):
    """Randomizes your 2 starting Topics and 2 starting Genres every seed.
    - On (Friendly Start): Guarantees at least one Great Combo (+++) pairing between your starting Topics and Genres.
    - Off (Challenge Mode): Purely random starting Topics and Genres with no guaranteed combo synergy."""

    display_name = "Friendly Start (Guaranteed Starting Combo)"


class ShuffleGameSizes(Toggle):
    """Adds three Progressive Game Size items: Medium, then Large, then AAA.
    You can only make a size once its item arrives. Researching a size is still a check.
    This can make a run much slower, especially with the Millionaire or Tycoon success levels."""

    display_name = "Shuffle Game Sizes"


class ModdedContent(OptionDict):
    """Content added by your other Game Dev Tycoon mods, so it can be part of the multiworld.
    Don't type this yourself: in game, open the Archipelago box and press "Export modded content", then paste the
    block it copies into your YAML. Each entry becomes an item and a check:
    - topics: "Modded Topic N" unlocks it; researching it is a check.
    - platforms: "Modded Platform N" unlocks it (licence included); releasing a game on it is a check.
    - genres: "Modded Genre N" unlocks it; releasing a game in it is a check.
    - research: "Modded Feature N" grants it; researching it yourself is a check.
    - events: "Modded Event N" makes it happen (it waits until the event's own conditions, like office or staff,
      are met); the event happening is a check.
    Limits: 30 topics, 15 platforms, 10 genres, 30 research, 30 events."""

    display_name = "Modded Content"
    default = {}
    valid_keys = ["topics", "platforms", "genres", "research", "events"]


@dataclass
class GDTOptions(PerGameCommonOptions):
    retirement_year: RetirementYear
    success_level: SuccessLevel
    friendly_start: FriendlyStart
    shuffle_game_sizes: ShuffleGameSizes
    modded_content: ModdedContent
