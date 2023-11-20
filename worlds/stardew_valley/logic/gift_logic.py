from functools import cached_property

from .has_logic import HasLogicMixin
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogic:
    has: HasLogicMixin

    def __init__(self, player: int, has: HasLogicMixin):
        self.player = player
        self.has = has

    @cached_property
    def has_any_universal_love(self) -> StardewRule:
        return self.has(Gift.golden_pumpkin) | self.has(Gift.pearl) | self.has("Prismatic Shard") | self.has(AnimalProduct.rabbit_foot)
