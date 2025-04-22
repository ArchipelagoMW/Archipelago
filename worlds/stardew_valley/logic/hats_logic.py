from .base_logic import BaseLogicMixin, BaseLogic
from ..strings.hat_names import Hat
from ..strings.region_names import LogicRegion, Region


class HatLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hat = HatLogic(*args, **kwargs)


class HatLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.meme_item_rules.update({
            Hat.laurel_wreath_crown: self.logic.region.can_reach(LogicRegion.desert_festival) & self.logic.time.has_lived_months(4),
            Hat.dark_cowboy_hat: self.logic.region.can_reach(Region.skull_cavern_100),
        })
