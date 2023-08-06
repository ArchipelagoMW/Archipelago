from .has_logic import HasLogic
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogic:
    player: int
    has: HasLogic

    def __init__(self, player: int, has: HasLogic):
        self.player = player
        self.has = has

    def has_any_universal_love(self) -> StardewRule:
        return self.has(Gift.golden_pumpkin) | self.has("Magic Rock Candy") | self.has(Gift.pearl) | self.has("Prismatic Shard") | self.has(AnimalProduct.rabbit_foot)

