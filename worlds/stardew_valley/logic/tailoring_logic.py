from dataclasses import dataclass
from typing import Tuple

from .base_logic import BaseLogicMixin, BaseLogic
from ..data.game_item import Source
from ..data.shirt_data import Shirt
from ..stardew_rule import StardewRule
from ..strings.artisan_good_names import ArtisanGood
from ..strings.machine_names import Machine
from ..strings.region_names import Region
from ..strings.villager_names import NPC


@dataclass(frozen=True, kw_only=True)
class TailoringSource(Source):
    tailoring_items: Tuple[str, ...]


class TailoringLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tailoring = TailoringLogic(*args, **kwargs)


class TailoringLogic(BaseLogic):

    def can_tailor_shirt(self, shirt: Shirt) -> StardewRule:
        return self.can_tailor(*shirt.required_items)

    def can_tailor(self, *items: str) -> StardewRule:
        return self.has_tailoring() & self.logic.has(ArtisanGood.cloth) & self.logic.has_any(*items)

    def has_tailoring(self) -> StardewRule:
        sewing_machine_rule = self.logic.region.can_reach(Region.haley_house) | self.logic.has(Machine.sewing_machine)
        return sewing_machine_rule & self.logic.relationship.can_meet(NPC.emily)
