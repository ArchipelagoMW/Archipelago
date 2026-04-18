"""Per-slot options for Ducks Can Drive."""
from __future__ import annotations

from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Toggle


class StartingMoney(Range):
    """Lifetime money budget the client mod grants for this seed.

    The stock game resets Car.money to $500 on every City entry, so "starting
    money" as a per-entry top-up was trivially farmable by re-entering the
    city. Under the current policy the mod overwrites the stock prefab money
    with (starting_money - lifetime_spent) on every City entry and tracks each
    Garage purchase in PlayerPrefs, so the option is a true one-shot pool
    shared across all city entries. Deliveries still earn money in-session
    (stock PayDay) but those earnings don't carry across scene loads.
    12,500 covers every tier in the seed; lower values force budget choices.
    """
    display_name = "Starting Money"
    range_start = 100
    range_end = 100_000
    default = 12_500


class IncludeBanana(Toggle):
    """Include the secret Banana track in the seed.

    Banana Offline has no Track Select menu button — in the stock game it
    only loads when a time-trial timer runs past 10 minutes without the
    player finishing. Enabling this adds one finish location and one
    track-unlock item to the pool, but the player has to know the secret
    timeout path to actually reach Banana. Off by default so most seeds
    don't contain a location that's practically unreachable without
    meta-knowledge.
    """
    display_name = "Include Banana Track"


@dataclass
class DucksOptions(PerGameCommonOptions):
    starting_money: StartingMoney
    include_banana: IncludeBanana
