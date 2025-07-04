from .base_logic import BaseLogic, BaseLogicMixin
from ..data.artisan import MachineSource
from ..data.game_item import ItemTag
from ..stardew_rule import StardewRule
from ..strings.artisan_good_names import ArtisanGood
from ..strings.crop_names import Vegetable, Fruit
from ..strings.fish_names import Fish, all_fish
from ..strings.forageable_names import Mushroom
from ..strings.generic_names import Generic
from ..strings.machine_names import Machine


class ArtisanLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.artisan = ArtisanLogic(*args, **kwargs)


class ArtisanLogic(BaseLogic):
    def initialize_rules(self):
        # TODO remove this one too once fish are converted to sources
        self.registry.artisan_good_rules.update({ArtisanGood.specific_smoked_fish(fish): self.can_smoke(fish) for fish in all_fish})
        self.registry.artisan_good_rules.update({ArtisanGood.specific_bait(fish): self.can_bait(fish) for fish in all_fish})

    def has_jelly(self) -> StardewRule:
        return self.logic.artisan.can_preserves_jar(Fruit.any)

    def has_pickle(self) -> StardewRule:
        return self.logic.artisan.can_preserves_jar(Vegetable.any)

    def has_smoked_fish(self) -> StardewRule:
        return self.logic.artisan.can_smoke(Fish.any)

    def has_targeted_bait(self) -> StardewRule:
        return self.logic.artisan.can_bait(Fish.any)

    def has_dried_fruits(self) -> StardewRule:
        return self.logic.artisan.can_dehydrate(Fruit.any)

    def has_dried_mushrooms(self) -> StardewRule:
        return self.logic.artisan.can_dehydrate(Mushroom.any_edible)

    def has_raisins(self) -> StardewRule:
        return self.logic.artisan.can_dehydrate(Fruit.grape)

    def can_produce_from(self, source: MachineSource) -> StardewRule:
        return self.logic.has(source.item) & self.logic.has(source.machine)

    def can_preserves_jar(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.preserves_jar)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.logic.has_any(*(fruit.name for fruit in self.content.find_tagged_items(ItemTag.FRUIT)))
        if item == Vegetable.any:
            return machine_rule & self.logic.has_any(*(vege.name for vege in self.content.find_tagged_items(ItemTag.VEGETABLE)))
        return machine_rule & self.logic.has(item)

    def can_keg(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.keg)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            return machine_rule & self.logic.has_any(*(fruit.name for fruit in self.content.find_tagged_items(ItemTag.FRUIT)))
        if item == Vegetable.any:
            return machine_rule & self.logic.has_any(*(vege.name for vege in self.content.find_tagged_items(ItemTag.VEGETABLE)))
        return machine_rule & self.logic.has(item)

    def can_mayonnaise(self, item: str) -> StardewRule:
        return self.logic.has(Machine.mayonnaise_machine) & self.logic.has(item)

    def can_smoke(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.fish_smoker)
        return machine_rule & self.logic.has(item)

    def can_bait(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.bait_maker)
        return machine_rule & self.logic.has(item)

    def can_dehydrate(self, item: str) -> StardewRule:
        machine_rule = self.logic.has(Machine.dehydrator)
        if item == Generic.any:
            return machine_rule
        if item == Fruit.any:
            # Grapes make raisins
            return machine_rule & self.logic.has_any(*(fruit.name for fruit in self.content.find_tagged_items(ItemTag.FRUIT) if fruit.name != Fruit.grape))
        if item == Mushroom.any_edible:
            return machine_rule & self.logic.has_any(*(mushroom.name for mushroom in self.content.find_tagged_items(ItemTag.EDIBLE_MUSHROOM)))
        return machine_rule & self.logic.has(item)
