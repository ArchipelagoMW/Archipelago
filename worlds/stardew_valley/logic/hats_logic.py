from functools import cached_property

from .base_logic import BaseLogicMixin, BaseLogic
from ..data.hats_data import HatItem
from ..stardew_rule import StardewRule
from ..strings.fish_names import Fish
from ..strings.region_names import LogicRegion


class HatLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hat = HatLogic(*args, **kwargs)


class HatLogic(BaseLogic):

    @cached_property
    def can_get_unlikely_hat_at_outfit_services(self) -> StardewRule:
        return self.logic.region.can_reach(LogicRegion.desert_festival) & self.logic.time.has_lived_months(12)

    @cached_property
    def has_bucket_hat(self) -> StardewRule:
        trout_derby_rule = self.logic.region.can_reach(LogicRegion.trout_derby) & self.logic.fishing.can_catch_fish(self.content.fishes[Fish.rainbow_trout])
        return trout_derby_rule

    def can_wear(self, hat: HatItem) -> StardewRule:
        return self.logic.has(hat.clarified_name)
