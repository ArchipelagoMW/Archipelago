import typing

from .base_logic import BaseLogicMixin, BaseLogic
from ..stardew_rule import StardewRule
from ..strings.building_names import Building
from ..strings.forageable_names import Forageable
from ..strings.machine_names import Machine


class AnimalLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animal = AnimalLogic(*args, **kwargs)


class AnimalLogic(BaseLogic):

    def can_incubate(self, egg_item: str) -> StardewRule:
        return self.logic.building.has_building(Building.coop) & self.logic.has(egg_item)

    def can_ostrich_incubate(self, egg_item: str) -> StardewRule:
        return self.logic.building.has_building(Building.barn) & self.logic.has(Machine.ostrich_incubator) & self.logic.has(egg_item)

    def has_animal(self, animal_name: str) -> StardewRule:
        animal = self.content.animals.get(animal_name)
        assert animal is not None, f"Animal {animal_name} not found."

        return self.logic.source.has_access_to_any(animal.sources) & self.logic.building.has_building(animal.required_building)

    def has_happy_animal(self, animal_name: str) -> StardewRule:
        return self.logic.animal.has_animal(animal_name) & self.logic.has(Forageable.hay)
