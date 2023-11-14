from functools import lru_cache

from .cached_logic import CachedLogic
from .has_logic import HasLogic, CachedRules
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogic(CachedLogic):
    has: HasLogic

    def __init__(self, player: int, cached_rules: CachedRules, has: HasLogic):
        super().__init__(player, cached_rules)
        self.has = has

    @lru_cache(maxsize=None)
    def has_any_universal_love(self) -> StardewRule:
        return self.has(Gift.golden_pumpkin) | self.has(Gift.pearl) | self.has("Prismatic Shard") | self.has(
            AnimalProduct.rabbit_foot)
