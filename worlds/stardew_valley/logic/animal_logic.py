from typing import Union

from .base_logic import BaseLogicMixin, BaseLogic
from .building_logic import BuildingLogicMixin
from .has_logic import HasLogicMixin
from .money_logic import MoneyLogicMixin
from ..stardew_rule import StardewRule, true_
from ..strings.animal_names import Animal, coop_animals, barn_animals
from ..strings.building_names import Building
from ..strings.forageable_names import Forageable
from ..strings.generic_names import Generic
from ..strings.region_names import Region

cost_and_building_by_animal = {
    Animal.chicken: (800, Building.coop),
    Animal.cow: (1500, Building.barn),
    Animal.goat: (4000, Building.big_barn),
    Animal.duck: (1200, Building.big_coop),
    Animal.sheep: (8000, Building.deluxe_barn),
    Animal.rabbit: (8000, Building.deluxe_coop),
    Animal.pig: (16000, Building.deluxe_barn)
}


class AnimalLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal = AnimalLogic(*args, **kwargs)


class AnimalLogic(BaseLogic[Union[HasLogicMixin, MoneyLogicMixin, BuildingLogicMixin]]):

    def can_buy_animal(self, animal: str) -> StardewRule:
        try:
            price, building = cost_and_building_by_animal[animal]
        except KeyError:
            return true_
        return self.logic.money.can_spend_at(Region.ranch, price) & self.logic.building.has_building(building)

    def has_animal(self, animal: str) -> StardewRule:
        if animal == Generic.any:
            return self.has_any_animal()
        elif animal == Building.coop:
            return self.has_any_coop_animal()
        elif animal == Building.barn:
            return self.has_any_barn_animal()
        return self.logic.has(animal)

    def has_happy_animal(self, animal: str) -> StardewRule:
        return self.has_animal(animal) & self.logic.has(Forageable.hay)

    def has_any_animal(self) -> StardewRule:
        return self.has_any_coop_animal() | self.has_any_barn_animal()

    def has_any_coop_animal(self) -> StardewRule:
        return self.logic.has_any(*coop_animals)

    def has_any_barn_animal(self) -> StardewRule:
        return self.logic.has_any(*barn_animals)
