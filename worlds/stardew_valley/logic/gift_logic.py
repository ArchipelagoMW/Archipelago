from functools import cached_property

from .base_logic import BaseLogic, BaseLogicMixin
from .has_logic import HasLogicMixin
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gifts = GiftLogic(*args, **kwargs)


class GiftLogic(BaseLogic[HasLogicMixin]):

    @cached_property
    def has_any_universal_love(self) -> StardewRule:
        return self.logic.has(Gift.golden_pumpkin) | self.logic.has(Gift.pearl) | self.logic.has("Prismatic Shard") | self.logic.has(AnimalProduct.rabbit_foot)
