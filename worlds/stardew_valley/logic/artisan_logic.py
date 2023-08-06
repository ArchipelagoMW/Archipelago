from typing import Union

from .has_logic import HasLogic
from .time_logic import TimeLogic
from ..stardew_rule import StardewRule
from ..strings.crop_names import all_vegetables, all_fruits, Vegetable, Fruit
from ..strings.generic_names import Generic
from ..strings.machine_names import Machine


class ArtisanLogic:
    player: int
    has: HasLogic
    time: TimeLogic

    def __init__(self, player: int, has: HasLogic, time: TimeLogic):
        self.player = player
        self.has = has
        self.time = time

    def has_jelly(self) -> StardewRule:
        return self.can_preserves_jar(Fruit.any)

    def has_pickle(self) -> StardewRule:
        return self.can_preserves_jar(Vegetable.any)

    def can_preserves_jar(self, item: str) -> StardewRule:
        machine_rule = self.has(Machine.preserves_jar)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.has(all_fruits, 1)
        if item == Vegetable.any:
            return machine_rule & self.has(all_vegetables, 1)
        return machine_rule & self.has(item)

    def has_wine(self) -> StardewRule:
        return self.can_keg(Fruit.any)

    def has_juice(self) -> StardewRule:
        return self.can_keg(Vegetable.any)

    def can_keg(self, item: str) -> StardewRule:
        machine_rule = self.has(Machine.keg)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.has(all_fruits, 1)
        if item == Vegetable.any:
            return machine_rule & self.has(all_vegetables, 1)
        return machine_rule & self.has(item)

    def can_age(self, item: Union[str, StardewRule], quality: str) -> StardewRule:
        months = 1
        if quality == "Gold":
            months = 2
        elif quality == "Iridium":
            months = 3
        if isinstance(item, str):
            rule = self.has(item)
        else:
            rule: StardewRule = item
        return self.has(Machine.cask) & self.time.has_lived_months(months) & rule
