"""Per-slot options for Ducks Can Drive."""
from __future__ import annotations

from dataclasses import dataclass

from Options import PerGameCommonOptions, Range


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


@dataclass
class DucksOptions(PerGameCommonOptions):
    starting_money: StartingMoney
