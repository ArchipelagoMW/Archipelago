"""Per-slot options for Ducks Can Drive."""
from __future__ import annotations

from dataclasses import dataclass

from Options import PerGameCommonOptions, Range


class StartingMoney(Range):
    """Money the car spawns with every time the player enters the City scene.

    The stock game hard-codes $100 and `Car.Start` resets stats every time, so
    without a top-up sphere-1 requires grinding the Photon delivery loop before
    any AP check can fire. The default of 12,500 covers all 25 upgrade tiers in
    one session; lower values make money matter again and can be used for
    slower-paced seeds. Range covers everything from 'pure grind' to 'pure AP'.
    """
    display_name = "Starting Money"
    range_start = 100
    range_end = 100_000
    default = 12_500


@dataclass
class DucksOptions(PerGameCommonOptions):
    starting_money: StartingMoney
