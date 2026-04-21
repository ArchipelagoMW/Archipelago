from .base_logic import BaseLogicMixin, BaseLogic
from ..data.game_item import ItemTag
from ..strings.ap_names.ap_weapon_names import APWeapon
from ..strings.meme_item_names import MemeItem
from ..strings.ring_names import all_ring_names
from ..strings.special_item_names import NotReallyAnItem


class MemeItemsLogicMixin(BaseLogicMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.meme = MemeItemsLogic(*args, **kwargs)


class MemeItemsLogic(BaseLogic):

    def initialize_rules(self):
        self.registry.meme_item_rules.update({
            MemeItem.trap: self.logic.true_,
            MemeItem.pot_of_gold: self.can_cheat(),
            MemeItem.seed_spot: self.can_cheat(),
            MemeItem.green_rain_weeds_0: self.can_cheat(),
            MemeItem.lumber: self.can_cheat(),
            MemeItem.weeds: self.can_cheat(),
            MemeItem.twig: self.can_cheat(),
            MemeItem.artifact_spot: self.can_cheat(),
            MemeItem.warp_totem_qis_arena: self.can_cheat(),
            MemeItem.supply_crate: self.can_cheat(),
            MemeItem.slime_crate: self.can_cheat(),
            MemeItem.decorative_pot: self.can_cheat(),
            MemeItem.camping_stove: self.can_cheat(),
            MemeItem.worn_pants: self.has_any_pants(),
            MemeItem.worn_left_ring: self.has_any_ring(),
            MemeItem.worn_right_ring: self.has_any_ring(),
            MemeItem.worn_shirt: self.has_any_shirt(),
            MemeItem.worn_boots: self.has_any_boots(),
            MemeItem.worn_hat: self.has_any_hat(),
            NotReallyAnItem.death: self.logic.true_,
        })

    def can_cheat(self):
        return self.logic.true_

    def has_any_pants(self):
        return self.logic.true_

    def has_any_shirt(self):
        return self.logic.true_

    def has_any_hat(self):
        return self.logic.has_any(*[item.name for item in self.content.find_tagged_items(ItemTag.HAT)])

    def has_any_ring(self):
        return self.logic.received_any(*all_ring_names)

    def has_any_boots(self):
        return self.logic.received(APWeapon.footwear)
