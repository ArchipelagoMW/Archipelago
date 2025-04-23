from .base_logic import BaseLogicMixin, BaseLogic
from ..stardew_rule import StardewRule
from ..strings.artisan_good_names import ArtisanGood
from ..strings.machine_names import Machine
from ..strings.region_names import Region
from ..strings.villager_names import NPC


class TailoringLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tailoring = TailoringLogic(*args, **kwargs)


class TailoringLogic(BaseLogic):

    def can_tailor(self, *items: str) -> StardewRule:
        sewing_machine_rule = self.logic.region.can_reach(Region.haley_house) | self.logic.has(Machine.sewing_machine)
        return sewing_machine_rule & self.logic.relationship.can_meet(NPC.emily) & self.logic.has(ArtisanGood.cloth) & self.logic.has_any(*items)
