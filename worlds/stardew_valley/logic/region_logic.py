from typing import Iterable

from ..stardew_rule import StardewRule, And, Or, Reach, Count


class RegionLogic:
    player: int

    def __init__(self, player: int):
        self.player = player

    def can_reach(self, spot: str) -> StardewRule:
        return Reach(spot, "Region", self.player)

    def can_reach_any(self, spots: Iterable[str]) -> StardewRule:
        return Or(self.can_reach(spot) for spot in spots)

    def can_reach_all(self, spots: Iterable[str]) -> StardewRule:
        return And(self.can_reach(spot) for spot in spots)

    def can_reach_all_except_one(self, spots: Iterable[str]) -> StardewRule:
        num_required = len(list(spots)) - 1
        if num_required <= 0:
            num_required = len(list(spots))
        return Count(num_required, [self.can_reach(spot) for spot in spots])

    def can_reach_location(self, spot: str) -> StardewRule:
        return Reach(spot, "Location", self.player)

    def can_reach_entrance(self, spot: str) -> StardewRule:
        return Reach(spot, "Entrance", self.player)

