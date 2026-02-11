from dataclasses import dataclass

from Options import Toggle, Choice, PerGameCommonOptions, Range, NamedRange, DeathLink


class Goal(Choice):
    """Sets the goal of your world.

    - **Bosses once:** Defeat every main game boss at least once with either Sonic or Blaze. Sonic and Blaze as bosses
      of Zone 7 count as individual bosses.
    - **Bosses both:** Defeat every main game boss with both Sonic and Blaze.
    - **Extra zone:** Defeat the extra zone boss, requiring all chaos and sol emeralds.
    - **100 percent:** Clear all acts and defeat all bosses (main game and extra zone) with both Sonic and Blaze."""
    display_name = "Goal"
    rich_text_doc = True
    option_bosses_once = 0
    option_bosses_both = 1
    option_extra_zone = 2
    option_100_percent = 3
    default = 0


class ScrewFZone(Toggle):
    """
    Toggle whether F-Zone (Sonic and Blaze) should be **excluded**
    from goal conditions and having important items.
    """
    display_name = "Screw F-Zone"
    rich_text_doc = True
    default = True


class AmountOfStartingZones(Range):
    """Decides how many zones will be unlocked at the start of the game."""
    display_name = "Amount of starting zones"
    rich_text_doc = True
    range_start = 1
    range_end = 8
    default = 2


class IncludeSRankChecks(Choice):
    """Adds reaching S rank on acts and/or bosses (excluding F-Zone and Extra zone) as additional checks."""
    display_name = "Include S rank checks"
    rich_text_doc = True
    option_none = 0
    option_only_acts = 1
    option_only_bosses = 2
    option_all = 3
    default = 0


class TailsAndCreamSubstory(Choice):
    """Sets how the presence of Tails and Cream as sidekicks is handled.
    BE AWARE that this feature is not fully functional yet, only partially.

    - **Always present:** Both will always be present. RECOMMENDED FOR NOW.
    - **Appearing later:** Both will be turned into items that can be collected to make them appear.
    - **Getting kidnapped:** Both will be present first, but a one-time trap item will make them disappear, you monster.
    - **On vacation:** Both will never be present, as they will take a vacation at the Luxury Ball Resort... Wait, wrong franchise!"""
    display_name = "Tails and Cream substory"
    rich_text_doc = True
    option_always_present = 0
    option_appearing_later = 1
    option_getting_kidnapped = 2
    option_on_vacation = 3
    default = 0


class TrapsPercentage(NamedRange):
    """The probability of any filler item (in percent) being replaced by a trap."""
    display_name = "Traps Percentage"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 0
    special_range_names = {
        "none": 0,
        "rare": 4,
        "occasionally": 10,
        "maximum_suffering": 100,
    }


@dataclass
class SonicRushOptions(PerGameCommonOptions):
    goal: Goal
    screw_f_zone: ScrewFZone
    amount_of_starting_zones: AmountOfStartingZones
    include_s_rank_checks: IncludeSRankChecks
    tails_and_cream_substory: TailsAndCreamSubstory
    traps_percentage: TrapsPercentage
    deathlink: DeathLink
