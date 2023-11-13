from .cached_logic import CachedLogic, cache_rule
from .has_logic import HasLogic
from .logic_cache import CachedRules
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogic(CachedLogic):
    has: HasLogic

    def __init__(self, player: int, cached_rules: CachedRules, has: HasLogic):
        super().__init__(player, cached_rules)
        self.has = has

    @cache_rule
    def has_any_universal_love(self) -> StardewRule:
        return self.has(Gift.golden_pumpkin) | self.has(Gift.pearl) | self.has("Prismatic Shard") | self.has(AnimalProduct.rabbit_foot)

