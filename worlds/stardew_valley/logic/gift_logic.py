from functools import cached_property

from .base_logic import BaseLogic, BaseLogicMixin
from ..data.secret_note_data import RequiredGifts
from ..stardew_rule import StardewRule
from ..strings.animal_product_names import AnimalProduct
from ..strings.gift_names import Gift


class GiftLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gifts = GiftLogic(*args, **kwargs)


class GiftLogic(BaseLogic):

    @cached_property
    def has_any_universal_love(self) -> StardewRule:
        return self.logic.has_any(Gift.golden_pumpkin, Gift.pearl, "Prismatic Shard", AnimalProduct.rabbit_foot)

    def can_gift_to(self, npc: str, item: str) -> StardewRule:
        return self.logic.relationship.can_meet(npc) & self.logic.has(item)

    def can_gift_any_to(self, npc: str, *items: str) -> StardewRule:
        return self.logic.relationship.can_meet(npc) & self.logic.has_any(*items)

    def can_fulfill(self, required_gifts: RequiredGifts | list[RequiredGifts]) -> StardewRule:
        if isinstance(required_gifts, RequiredGifts):
            return self.can_gift_all_to(required_gifts)
        return self.can_gift_all_to_all(required_gifts)

    def can_gift_all_to(self, required_gifts: RequiredGifts) -> StardewRule:
        return self.logic.relationship.can_meet(required_gifts.npc) & self.logic.has_all(*required_gifts.gifts)

    def can_gift_all_to_all(self, required_gifts: list[RequiredGifts]) -> StardewRule:
        items = [gift for required_gift in required_gifts for gift in required_gift.gifts]
        return self.logic.relationship.can_meet_all(*[required_gift.npc for required_gift in required_gifts]) & self.logic.has_all(*items)

    def can_give_loved_gifts_to_everyone(self) -> StardewRule:
        rules = []

        for npc in self.content.villagers:
            meet_rule = self.logic.relationship.can_meet(npc)
            rules.append(meet_rule)

        rules.append(self.has_any_universal_love)

        return self.logic.and_(*rules)
