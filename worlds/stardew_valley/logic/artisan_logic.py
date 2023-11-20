from .has_logic import HasLogicMixin
from .time_logic import TimeLogicMixin
from ..stardew_rule import StardewRule
from ..strings.crop_names import all_vegetables, all_fruits, Vegetable, Fruit
from ..strings.generic_names import Generic
from ..strings.machine_names import Machine


class ArtisanLogicMixin(TimeLogicMixin, HasLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artisan = self

    def has_jelly(self) -> StardewRule:
        return self.artisan.can_preserves_jar(Fruit.any)

    def has_pickle(self) -> StardewRule:
        return self.artisan.can_preserves_jar(Vegetable.any)

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
        return self.artisan.can_keg(Fruit.any)

    def has_juice(self) -> StardewRule:
        return self.artisan.can_keg(Vegetable.any)

    def can_keg(self, item: str) -> StardewRule:
        machine_rule = self.has(Machine.keg)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.has(all_fruits, 1)
        if item == Vegetable.any:
            return machine_rule & self.has(all_vegetables, 1)
        return machine_rule & self.has(item)

    def can_mayonnaise(self, item: str) -> StardewRule:
        return self.has(Machine.mayonnaise_machine) & self.has(item)
