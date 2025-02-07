from dataclasses import dataclass
from Options import Toggle, PerGameCommonOptions, Choice, OptionSet, DeathLink, Range


class FillWithDetermination(Toggle):
    """Either fills the rat with determination, or does nothing. Perhaps both.

    This option was added early on for technical reasons. It does not directly affect the game."""
    display_name = "Fill With Determination"


class VictoryLocation(Choice):
    """Optionally moves the final victory location earlier to reduce the number of locations in the multiworld.

    - **Snakes on a Planet (default):** The game goes all the way to "Moon, The". This gives the longest game.
    - **Secret Cache**: The game stops at the end of Cool World. This gives the middlest-length game.
    - **Captured Goldfish**: The game stops at the end of The Sewers. This gives the shortest game."""
    display_name = "Victory Location"
    option_snakes_on_a_planet = 0
    option_secret_cache = 1
    option_captured_goldfish = 2
    default = 0


class EnabledBuffs(OptionSet):
    """Enables various buffs that affect how the rat behaves. All are enabled by default.
    Well Fed: Gets more done
    Lucky: One free success
    Energized: Moves faster
    Stylish: Better RNG
    Confident: Ignore a trap
    Smart: Next check is progression-tier
    """
    display_name = "Enabled Buffs"
    valid_keys = frozenset({"Well Fed", "Lucky", "Energized", "Stylish", "Confident", "Smart"})
    default = frozenset({"Well Fed", "Lucky", "Energized", "Stylish", "Confident", "Smart"})
    map = {
        "Well Fed": "well_fed",
        "Lucky": "lucky",
        "Energized": "energized",
        "Stylish": "stylish",
        "Confident": "confident",
        "Smart": "smart",
    }


class EnabledTraps(OptionSet):
    """Enables various traps that affect how the rat behaves. All are enabled by default.
    Upset Tummy: Gets less done
    Unlucky: Worse RNG
    Sluggish: Moves slower
    Distracted: Skip a "step"
    Startled: Run towards start
    Conspiratorial: Next check is trap-tier
    """
    display_name = "Enabled Traps"
    valid_keys = frozenset({"Upset Tummy", "Unlucky", "Sluggish", "Distracted", "Startled", "Conspiratorial"})
    default = frozenset({"Upset Tummy", "Unlucky", "Sluggish", "Distracted", "Startled", "Conspiratorial"})

    map = {
        "Upset Tummy": "upset_tummy",
        "Unlucky": "unlucky",
        "Sluggish": "sluggish",
        "Distracted": "distracted",
        "Startled": "startled",
        "Conspiratorial": "conspiratorial",
    }


class DeathDelaySeconds(Range):
    """Sets the delay (in seconds) from a death trigger to when the rat actually "dies". Has no effect if DeathLink is disabled.

    Default: 5 (seconds)
    """
    display_name = "Death Link Delay"
    range_start = 0
    range_end = 60
    default = 5

@dataclass
class ArchipelagoGameOptions(PerGameCommonOptions):
    fill_with_determination: FillWithDetermination
    victory_location: VictoryLocation
    enabled_buffs: EnabledBuffs
    enabled_traps: EnabledTraps
    death_link: DeathLink
    death_delay_seconds: DeathDelaySeconds
