import math

from .base_logic import BaseLogicMixin, BaseLogic
from ..content.feature.friendsanity import pet_heart_item_name
from ..stardew_rule import StardewRule, True_
from ..strings.building_names import Building
from ..strings.region_names import Region


class PetLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pet = PetLogic(*args, **kwargs)


class PetLogic(BaseLogic):
    def has_pet_hearts(self, hearts: int = 1) -> StardewRule:
        if hearts <= 0:
            return True_()

        if self.content.features.friendsanity.is_pet_randomized:
            return self.received_pet_hearts(hearts)

        return self.can_befriend_pet(hearts)

    def received_pet_hearts(self, hearts: int) -> StardewRule:
        return self.logic.received(pet_heart_item_name,
                                   math.ceil(hearts / self.content.features.friendsanity.heart_size))

    def can_befriend_pet(self, hearts: int) -> StardewRule:
        if hearts <= 0:
            return True_()

        heart_size = self.content.features.friendsanity.heart_size
        previous_heart = max(hearts - heart_size, 0)
        previous_heart_rule = self.has_pet_hearts(previous_heart)
        points = hearts * 200
        points_per_month = 12 * 14
        points_per_water_month = 18 * 14
        farm_rule = self.logic.region.can_reach(Region.farm)
        time_with_water_rule = self.logic.tool.can_water() & self.logic.time.has_lived_months(points // points_per_water_month)
        time_without_water_rule = self.logic.time.has_lived_months(points // points_per_month)
        time_rule = time_with_water_rule | time_without_water_rule
        return farm_rule & time_rule & self.logic.building.has_building(Building.pet_bowl) & previous_heart_rule
