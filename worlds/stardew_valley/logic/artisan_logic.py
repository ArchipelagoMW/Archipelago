from typing import Union

from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from .time_logic import TimeLogicMixin
from ..stardew_rule import StardewRule
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import all_vegetables, all_fruits, Vegetable, Fruit
from ..strings.fish_names import Fish, all_fish
from ..strings.forageable_names import Mushroom, all_edible_mushrooms
from ..strings.generic_names import Generic
from ..strings.machine_names import Machine


class ArtisanLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artisan = ArtisanLogic(*args, **kwargs)


class ArtisanLogic(BaseLogic[Union[ArtisanLogicMixin, TimeLogicMixin, HasLogicMixin]]):
    def initialize_rules(self):
        self.registry.artisan_good_rules.update({ArtisanGood.specific_wine(fruit): self.can_keg(fruit) for fruit in all_fruits})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_juice(vegetable): self.can_keg(vegetable) for vegetable in all_vegetables})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_jelly(fruit): self.can_preserves_jar(fruit) for fruit in all_fruits})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_pickles(vegetable): self.can_preserves_jar(vegetable) for vegetable in all_vegetables})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_smoked(fish): self.can_smoke(fish) for fish in all_fish})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_dried(fruit): self.can_dehydrate(fruit) for fruit in all_fruits})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_dried(mushroom): self.can_dehydrate(mushroom) for mushroom in all_edible_mushrooms})

    def has_jelly(self) -> StardewRule:
        return self.logic.artisan.can_preserves_jar(Fruit.any)

    def has_pickle(self) -> StardewRule:
        return self.logic.artisan.can_preserves_jar(Vegetable.any)

    def has_smoked_fish(self) -> StardewRule:
        return self.logic.artisan.can_smoke(Fish.any)

    def has_dried_fruits(self) -> StardewRule:
        return self.logic.artisan.can_dehydrate(Fruit.any)

    def has_dried_mushrooms(self) -> StardewRule:
        return self.logic.artisan.can_dehydrate(Mushroom.any_edible)

    def has_wine(self) -> StardewRule:
        return self.logic.artisan.can_keg(Fruit.any)

    def has_juice(self) -> StardewRule:
        return self.logic.artisan.can_keg(Vegetable.any)

    def can_preserves_jar(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.preserves_jar)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.logic.has_any(*all_fruits)
        if item == Vegetable.any:
            return machine_rule & self.logic.has_any(*all_vegetables)
        return machine_rule & self.logic.has(item)

    def can_keg(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.keg)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.logic.has_any(*all_fruits)
        if item == Vegetable.any:
            return machine_rule & self.logic.has_any(*all_vegetables)
        return machine_rule & self.logic.has(item)

    def can_mayonnaise(self, item: str) -> StardewRule:
        return self.logic.has(Machine.mayonnaise_machine) & self.logic.has(item)

    def can_smoke(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.fish_smoker)
        return machine_rule & self.logic.has(item)

    def can_dehydrate(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.dehydrator)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.logic.has_any(*all_fruits)
        if item == Mushroom.any_edible:
            return machine_rule & self.logic.has_any(*all_edible_mushrooms)
        return machine_rule & self.logic.has(item)
