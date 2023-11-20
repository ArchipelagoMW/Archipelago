from functools import cached_property

from .base_logic import BaseLogic
from .has_logic import HasLogicMixin
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogicMixin(BaseLogic):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gifts = GiftLogic(*args, **kwargs)


class GiftLogic(HasLogicMixin):

    @cached_property
    def has_any_universal_love(self) -> StardewRule:
        return self.has(Gift.golden_pumpkin) | self.has(Gift.pearl) | self.has("Prismatic Shard") | self.has(AnimalProduct.rabbit_foot)
